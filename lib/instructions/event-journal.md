# Event Journal

`/sdd:implement` updates `.spec-context.json` **indirectly**: instead of a
read-merge-write of the growing JSON on every task, the main thread appends a
compact, ordered event to a per-spec write-ahead log, and a single drain script
folds those events into `.spec-context.json` at batched boundaries. This keeps
the bookkeeping off the main thread's hot loop while preserving full transition
granularity, crash-safety, and the consumer-facing file shape.

> Owns the journal format + drain algorithm. Transition entry shape and `at`
> precision live in [`transition-logging.md`](./transition-logging.md); the full
> state model lives in [`docs/STATE.md`](../../docs/STATE.md).

## Files

```
specs/{NNN}-{slug}/.spec-context.json          materialized state (consumer-facing; shape unchanged + drainedSeq)
specs/{NNN}-{slug}/.spec-context.events.jsonl  append-only event journal (SDD-internal, gitignored)
specs/{NNN}-{slug}/.spec-context.events.lock   mkdir-based drain lock (transient, gitignored)
```

The journal is a write-ahead log; `.spec-context.json` is a materialized view
derived from it. Nothing is "lost" while the journal is undrained — resume
replays it (see [Replay on resume](#replay-on-resume)).

## Event line schema

One JSON object per line. Common fields:

| Field | Type | Meaning |
|---|---|---|
| `seq` | int | Monotonic. Folded only when `> json.drainedSeq` (idempotency). |
| `at` | string | ISO 8601, **millisecond precision** (`date -u +%Y-%m-%dT%H:%M:%S.%3NZ`). Used verbatim as the transition's `at`. |
| `kind` | string | Label: `progress` · `task_done` · `group_done` · `field_set`. Informational. |
| `step` | string | Step at write time → `transition.step`. |
| `substep` | string \| null | Substep at write time → `transition.substep`. Matches `progress`. |
| `from` | object \| null | `{step, substep}` of the prior state → `transition.from`. Null on first write. |

Operation fields (any combination; the drainer applies **set → union → append**):

| Field | Shape | Effect |
|---|---|---|
| `set` | `{key: value}` | Shallow replace. Dotted keys nest (`"task_summaries.T001"`, `"step_summaries.specify"`). |
| `union` | `{key: [items]}` | Append items not already present (e.g. `files_modified`, `syncedDomains`). |
| `append` | `{key: [items]}` | Append all items (e.g. `decisions`, `concerns`). |

Each folded event appends exactly **one** transition:
`{ step, substep, from, by: "sdd", at }`.

### `seq` rule

At skill entry, set the run counter to `max(json.drainedSeq or 0, last journal
line's seq or 0)`. Increment by 1 for each append. `seq` gives a total order
independent of filesystem timestamp resolution and is what makes draining
idempotent.

## Appending (the cheap, non-blocking path)

Append one line with a plain shell append — **no read, no merge, no
re-serialization** of `.spec-context.json`:

```bash
AT=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)
printf '%s\n' "{\"seq\":7,\"at\":\"$AT\",\"kind\":\"task_done\",\"step\":\"implement\",\"substep\":\"phase1\",\"from\":{\"step\":\"implement\",\"substep\":\"phase1\"},\"set\":{\"task_summaries.T004\":{\"status\":\"DONE\",\"did\":\"...\",\"files\":[\"a.ts\"],\"concerns\":[]},\"currentTask\":\"T005\",\"last_action\":\"T004 done\"},\"union\":{\"files_modified\":[\"a.ts\"]}}" \
  >> specs/{NNN}-{slug}/.spec-context.events.jsonl
```

Rules:
- The `from` is captured at append time (the skill knows its prior step/substep
  from its entry read) — so no read is needed in the hot loop.
- **Subagents never append** to the journal or write `.spec-context.json`. They
  return reports; the main thread appends a `group_done` on their behalf.
- The journal is append-only — never rewrite or reorder existing lines.

### Common event kinds

- `progress` — `set: {progress, next?, currentStep?, currentTask?}`.
- `task_done` — `set: {"task_summaries.T###": {...}, currentTask, last_action}`,
  `union: {files_modified}`, `append: {decisions?, concerns?}`.
- `group_done` — like `task_done` but `set`s every task's summary at once and a
  group-level `last_action`.
- `field_set` — any other field write (`syncedDomains` via `union`;
  `checkpointStatus`/`step_summaries.*`/`approach`/`prUrl`/`prNumber`/`status`/
  `currentStep`/`next` via `set`).

## Draining (the single writer)

Run the drainer to materialize the journal into `.spec-context.json`:

```bash
python3 lib/scripts/drain-spec-context.py specs/{NNN}-{slug}/
```

It reads the current JSON (preserving **all** fields, including extension-owned
`status`/`stepHistory` and foreign transitions), folds journal events with
`seq > drainedSeq` in `seq` order, appends one transition per event, sets
`drainedSeq = max(seq)` and `updated`, then writes atomically (temp + rename).
A `mkdir` lock serializes it against an optional accelerator hook. Re-running with
no new events is a no-op.

### When to drain (`/sdd:implement` boundaries)

- **Context Recovery on resume** — drain FIRST, before reading any field.
- Every ~3 solo tasks, and before yielding the turn (bounds viewer staleness).
- At each parallel-group end.
- **Before each checkpoint display (CP1/CP2/CP3)** — the displays read
  materialized `concerns`/`files_modified`/`task_summaries`. Mandatory.
- Before `git add` in Step 8 and the finalize commit in Step 8b.

## Replay on resume

`/sdd:implement` (and `/sdd:resume`, `/sdd:status`) **drain before they read**.
Because the drainer is idempotent (watermarked on `drainedSeq`) and advances the
watermark atomically with the fold, calling it on every resume is safe and
guarantees no appended event is lost — even if a prior session died mid-phase
with an undrained journal.

## Crash-safety & idempotency

- An event is durable once appended; the JSON merely lags. Crash exposure is
  unchanged from synchronous writing: a crash between "task verified" and "append"
  loses only that one summary (not the code or the ticked `tasks.md`).
- `drainedSeq` advances atomically with the fold (single temp+rename), so a
  crashed drain re-folds from the same point — exactly-once materialization.
- The `mkdir` lock + watermark make a concurrent built-in drain and accelerator
  hook degrade to one effective fold.
