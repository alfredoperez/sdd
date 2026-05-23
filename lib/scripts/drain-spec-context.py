#!/usr/bin/env python3
"""
Drain the per-spec event journal into `.spec-context.json`.

SDD's `/sdd:implement` (and resume/status) append compact, ordered events to a
sidecar write-ahead log instead of doing a read-merge-write of the growing
`.spec-context.json` on every task. This script is the SINGLE writer that folds
those events into the materialized state file.

  specs/{NNN}-{slug}/.spec-context.json          materialized state (consumer-facing)
  specs/{NNN}-{slug}/.spec-context.events.jsonl  append-only event journal (WAL)
  specs/{NNN}-{slug}/.spec-context.events.lock   mkdir-based drain lock

Usage:
  python3 drain-spec-context.py <spec-dir>

Each journal line is one JSON event. Common fields:
  seq      int    monotonic; folded only when > json.drainedSeq (idempotent)
  at       str    ISO 8601, millisecond precision (used verbatim for the transition)
  kind     str    label (progress|task_done|group_done|field_set) — informational
  step     str    step at write time            -> transition.step
  substep  str?   substep at write time         -> transition.substep
  from     obj?   {step, substep} | null        -> transition.from

Operation fields (any combination; applied set -> union -> append):
  set    {key: value}    shallow replace; dotted keys nest one+ levels
                         (e.g. "task_summaries.T001", "step_summaries.specify")
  union  {key: [items]}  append items not already present (files_modified, syncedDomains)
  append {key: [items]}  append all items (decisions, concerns)

Each folded event appends exactly one transition:
  { step, substep, from, by: "sdd", at }

Guarantees:
  - Read-then-merge: every field not touched by an event (incl. extension-owned
    `status` / `stepHistory` and foreign transitions) is preserved verbatim.
  - transitions[] is append-only; folded in `seq` order.
  - Exactly-once: `drainedSeq` is advanced atomically with the fold (temp+rename),
    so a crashed drain re-folds from the same watermark on the next run.
  - Single writer: a `mkdir` lock serializes against an optional accelerator hook.

Exit codes: 0 = drained (or nothing to do, or lock held); 1 = error.
"""
import json
import os
import sys
import time
from datetime import date, timezone, datetime


LOCK_STALE_SECONDS = 30


def log(msg: str) -> None:
    print(f"drain-spec-context: {msg}", file=sys.stderr)


def load_json(path: str):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except ValueError as e:
        raise SystemExit(f"drain-spec-context: {path} is not valid JSON: {e}")


def read_events(path: str) -> list:
    events = []
    try:
        with open(path) as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except ValueError as e:
                    log(f"skipping malformed journal line {lineno}: {e}")
    except FileNotFoundError:
        return []
    return events


def set_path(ctx: dict, dotted: str, value) -> None:
    """Set ctx[a][b][...] = value, creating intermediate dicts."""
    keys = dotted.split(".")
    node = ctx
    for k in keys[:-1]:
        nxt = node.get(k)
        if not isinstance(nxt, dict):
            nxt = {}
            node[k] = nxt
        node = nxt
    node[keys[-1]] = value


def apply_event(ctx: dict, event: dict) -> None:
    for key, value in (event.get("set") or {}).items():
        set_path(ctx, key, value)

    for key, items in (event.get("union") or {}).items():
        existing = ctx.get(key)
        if not isinstance(existing, list):
            existing = []
        for item in items:
            if item not in existing:
                existing.append(item)
        ctx[key] = existing

    for key, items in (event.get("append") or {}).items():
        existing = ctx.get(key)
        if not isinstance(existing, list):
            existing = []
        existing.extend(items)
        ctx[key] = existing

    # Every folded event yields exactly one transition.
    transitions = ctx.get("transitions")
    if not isinstance(transitions, list):
        transitions = []
    transitions.append({
        "step": event.get("step"),
        "substep": event.get("substep"),
        "from": event.get("from"),
        "by": "sdd",
        "at": event.get("at"),
    })
    ctx["transitions"] = transitions


def atomic_write(path: str, data: dict) -> None:
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def acquire_lock(lock_dir: str) -> bool:
    try:
        os.mkdir(lock_dir)
        return True
    except FileExistsError:
        try:
            age = time.time() - os.path.getmtime(lock_dir)
        except OSError:
            age = 0
        if age > LOCK_STALE_SECONDS:
            log(f"stealing stale lock ({age:.0f}s old)")
            try:
                os.rmdir(lock_dir)
                os.mkdir(lock_dir)
                return True
            except OSError:
                return False
        return False


def release_lock(lock_dir: str) -> None:
    try:
        os.rmdir(lock_dir)
    except OSError:
        pass


def drain(spec_dir: str) -> int:
    json_path = os.path.join(spec_dir, ".spec-context.json")
    journal_path = os.path.join(spec_dir, ".spec-context.events.jsonl")
    lock_dir = os.path.join(spec_dir, ".spec-context.events.lock")

    if not os.path.exists(journal_path):
        return 0  # nothing to drain

    if not acquire_lock(lock_dir):
        log("lock held; another drain is running")
        return 0

    try:
        ctx = load_json(json_path)
        if ctx is None:
            ctx = {}

        drained_seq = ctx.get("drainedSeq", 0)
        if not isinstance(drained_seq, int):
            drained_seq = 0

        events = [e for e in read_events(journal_path)
                  if isinstance(e.get("seq"), int) and e["seq"] > drained_seq]
        if not events:
            return 0  # idempotent no-op

        events.sort(key=lambda e: e["seq"])
        for event in events:
            apply_event(ctx, event)

        ctx["drainedSeq"] = events[-1]["seq"]
        ctx["updated"] = date.today().isoformat()

        atomic_write(json_path, ctx)
        log(f"folded {len(events)} event(s); drainedSeq={ctx['drainedSeq']}")
        return 0
    finally:
        release_lock(lock_dir)


def main(argv: list) -> int:
    if len(argv) != 2:
        log("usage: drain-spec-context.py <spec-dir>")
        return 1
    spec_dir = argv[1]
    if not os.path.isdir(spec_dir):
        log(f"not a directory: {spec_dir}")
        return 1
    return drain(spec_dir)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
