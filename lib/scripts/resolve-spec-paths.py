#!/usr/bin/env python3
"""Resolve living-spec paths for SDD domains.

Single source of truth for the rules in lib/instructions/layered-context.md:
  - domain membership: pattern OR any include glob, minus exclude globs
  - path resolution:   colocated -> specPath, else {specDir}/<domain>/spec.md
  - discovery:         union of .sdd.json domains and the .specs/*/spec.md glob
  - ordering:          most-specific first (deepest scope path that prefixes the file)
  - tiered files:      <base>.spec.md (hot) / .arch.md (cold) / .coverage.md (test)
  - orphans:           *.spec.md in the tree not claimed by any configured domain

Skills call this script instead of re-interpreting the prose, so the four
consumers (specify / plan / implement / drift) cannot drift apart.

Usage:
  resolve-spec-paths.py --changed <file>...   # domains in scope for a change (ordered)
  resolve-spec-paths.py --all                 # every domain (union) — used by drift
  resolve-spec-paths.py --orphans             # orphan *.spec.md files only
  add --json for machine-readable output (default for --changed/--all).
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from glob import glob

CONFIG = ".sdd.json"
DEFAULT_SPEC_DIR = ".specs"
DEFAULT_EXEMPT = ["*.config.*", "*.test.*", "**/migrations/**", "scripts/**"]
TIERS = ("spec", "arch", "coverage")


def load_config(root: str) -> dict:
    path = os.path.join(root, CONFIG)
    if not os.path.isfile(path):
        return {}
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"resolve-spec-paths: cannot read {CONFIG}: {exc}\n")
        return {}


def spec_dir(cfg: dict) -> str:
    return cfg.get("specDir", DEFAULT_SPEC_DIR)


def _literal_prefix(pattern: str) -> str:
    """Longest leading literal path of a regex (for specificity + scope).

    `^src/checkout/` -> `src/checkout`; stops at the first regex metachar.
    """
    p = pattern[1:] if pattern.startswith("^") else pattern
    out = []
    for ch in p:
        if ch in ".*+?()[]{}|\\$":
            break
        out.append(ch)
    return "".join(out).rstrip("/")


def scope_path(name: str, dom: dict, cfg: dict) -> str:
    """Directory that represents how 'deep' a domain sits — used for ordering."""
    if dom.get("location") == "colocated" and dom.get("specPath"):
        return os.path.dirname(dom["specPath"])
    lit = _literal_prefix(dom.get("pattern", ""))
    if lit:
        return lit
    # fall back to the common dir of include globs
    inc = dom.get("include") or []
    dirs = [g.split("*")[0].rstrip("/") for g in inc if g]
    return os.path.dirname(dirs[0]) if dirs else os.path.join(spec_dir(cfg), name)


def resolve_spec_path(name: str, dom: dict, cfg: dict) -> str:
    if dom.get("location") == "colocated":
        sp = dom.get("specPath")
        if not sp:
            raise ValueError(
                f'domain "{name}" is colocated but has no specPath in {CONFIG}'
            )
        return sp
    return os.path.join(spec_dir(cfg), name, "spec.md")


def tier_paths(spec_path: str) -> dict:
    """Sibling tier files for a resolved .spec.md path."""
    if spec_path.endswith(".spec.md"):
        base = spec_path[: -len(".spec.md")]
        return {"spec": spec_path, "arch": base + ".arch.md", "coverage": base + ".coverage.md"}
    # centralized .specs/<d>/spec.md -> arch.md / coverage.md in the same folder
    d = os.path.dirname(spec_path)
    return {"spec": spec_path, "arch": os.path.join(d, "arch.md"),
            "coverage": os.path.join(d, "coverage.md")}


def matches(dom: dict, f: str) -> bool:
    """File belongs to domain if: pattern OR any include glob, minus exclude."""
    for ex in dom.get("exclude") or []:
        if fnmatch.fnmatch(f, ex):
            return False
    pat = dom.get("pattern")
    if pat and re.search(pat, f):
        return True
    for inc in dom.get("include") or []:
        if fnmatch.fnmatch(f, inc):
            return True
    return False


def _specificity(name: str, dom: dict, cfg: dict, f: str) -> int:
    """How specific this domain is for file f: length of its scope path
    when that scope is a prefix of f, else the raw scope length (weak)."""
    sp = scope_path(name, dom, cfg)
    if sp and (f == sp or f.startswith(sp + "/")):
        return len(sp)
    return 0


def _domain_entry(name: str, dom: dict, cfg: dict, root: str) -> dict:
    sp = resolve_spec_path(name, dom, cfg)
    tiers = tier_paths(sp)
    return {
        "domain": name,
        "specPath": sp,
        "location": dom.get("location", "centralized"),
        "specFormat": dom.get("specFormat", "generic"),
        "exists": os.path.isfile(os.path.join(root, sp)),
        "tiers": {k: {"path": v, "exists": os.path.isfile(os.path.join(root, v))}
                  for k, v in tiers.items()},
    }


def match_changed(files: list[str], cfg: dict, root: str) -> list[dict]:
    domains = cfg.get("domains") or {}
    hits = []
    matched_files = set()
    for name, dom in domains.items():
        hit_files = [f for f in files if matches(dom, f)]
        if not hit_files:
            continue
        matched_files.update(hit_files)
        entry = _domain_entry(name, dom, cfg, root)
        entry["specificity"] = max(_specificity(name, dom, cfg, f) for f in hit_files)
        hits.append(entry)
    # Fallback (preserves zero-config behavior): for files no configured domain
    # claimed, match the parent-directory basename against an existing
    # {specDir}/<dir>/spec.md. See layered-context.md precedence step 3.
    sd = spec_dir(cfg)
    seen = {os.path.normpath(e["specPath"]) for e in hits}
    for f in files:
        if f in matched_files:
            continue
        base = os.path.basename(os.path.dirname(f))
        if not base:
            continue
        sp = os.path.join(sd, base, "spec.md")
        if os.path.normpath(sp) in seen or not os.path.isfile(os.path.join(root, sp)):
            continue
        entry = _domain_entry(base, {}, cfg, root)
        entry["specificity"] = len(os.path.dirname(f))
        hits.append(entry)
        seen.add(os.path.normpath(sp))
    # most-specific first; stable tiebreak by name
    hits.sort(key=lambda e: (-e["specificity"], e["domain"]))
    return hits


def discover_all(cfg: dict, root: str) -> list[dict]:
    domains = cfg.get("domains") or {}
    out, seen = [], set()
    for name, dom in domains.items():
        entry = _domain_entry(name, dom, cfg, root)
        out.append(entry)
        seen.add(os.path.normpath(entry["specPath"]))
    # union with centralized .specs/*/spec.md not already configured
    sd = spec_dir(cfg)
    for sp in sorted(glob(os.path.join(root, sd, "*", "spec.md"))):
        rel = os.path.relpath(sp, root)
        if os.path.normpath(rel) in seen:
            continue
        name = os.path.basename(os.path.dirname(rel))
        out.append(_domain_entry(name, {}, cfg, root))
        seen.add(os.path.normpath(rel))
    out.sort(key=lambda e: e["domain"])
    return out


def find_orphans(cfg: dict, root: str) -> list[str]:
    """*.spec.md in the tree not claimed by a configured domain's specPath.

    .arch.md / .coverage.md siblings of a claimed spec are recognized tiers,
    never orphans. Excludes specs/, the spec dir, and specExempt globs.
    """
    sd = spec_dir(cfg)
    exempt = cfg.get("specExempt", DEFAULT_EXEMPT)
    claimed = set()
    for e in discover_all(cfg, root):
        claimed.add(os.path.normpath(e["specPath"]))
    orphans = []
    for sp in glob(os.path.join(root, "**", "*.spec.md"), recursive=True):
        rel = os.path.normpath(os.path.relpath(sp, root))
        top = rel.split(os.sep, 1)[0]
        if top in ("specs", sd.strip("./")):
            continue
        if any(fnmatch.fnmatch(rel, g) for g in exempt):
            continue
        if rel not in claimed:
            orphans.append(rel)
    return sorted(orphans)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Resolve SDD living-spec paths.")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("--changed", nargs="*", help="changed files -> domains in scope")
    ap.add_argument("--all", action="store_true", help="every domain (union)")
    ap.add_argument("--orphans", action="store_true", help="orphan *.spec.md files")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    root = args.root
    cfg = load_config(root)

    if args.orphans:
        orphans = find_orphans(cfg, root)
        if args.json:
            print(json.dumps({"orphans": orphans}, indent=2))
        else:
            for o in orphans:
                print(f"ℹ Orphan living spec {o} — not referenced by any .sdd.json domain")
        return 0

    try:
        if args.all:
            result = {"domains": discover_all(cfg, root), "orphans": find_orphans(cfg, root)}
        else:
            files = args.changed or []
            result = {"changed": files, "matched": match_changed(files, cfg, root)}
    except ValueError as exc:
        sys.stderr.write(f"⚠ {exc}\n")
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
