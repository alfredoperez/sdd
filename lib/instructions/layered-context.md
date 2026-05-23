# Layered Context Loading

How SDD skills locate and load **Layer 1** (per-domain "living specs") so that `/sdd:specify` and `/sdd:plan` can ground feature work in the current truth of each affected capability.

Reference: `.sdd/decisions/0001-layered-context-loading.md`.

## Layers

| Layer | What | Where | Loaded by |
|---|---|---|---|
| 0 — Principles | Project-wide MUSTs | `.sdd/principles.md` | `/sdd:plan` (Principles Check) |
| 1 — Living specs | Current truth per capability | resolved path (default `.specs/<domain>/spec.md`, or a colocated `specPath`) | `/sdd:specify` + `/sdd:plan` (this file) |
| 2 — Feature delta | Per-feature change | `specs/{NNN}-{slug}/spec.md` | All skills (existing) |

All layers are **opt-in by presence** — each layer is silently skipped if the file/folder isn't there.

## The resolver script (single source of truth)

A domain's living spec is **not** always at `.specs/<domain>/spec.md`. All path logic — membership, resolution, discovery, ordering, tier files, orphans — lives in **one executable**: [`lib/scripts/resolve-spec-paths.py`](../scripts/resolve-spec-paths.py) (evals: `test_resolve_spec_paths.py`). Skills **call** it and consume its JSON; they MUST NOT re-implement or hardcode `.specs/<domain>/spec.md`. This is what keeps specify / plan / implement / drift from drifting apart.

```bash
python3 lib/scripts/resolve-spec-paths.py --changed <file>...   # domains in scope (most-specific first)
python3 lib/scripts/resolve-spec-paths.py --all                 # every domain (union) + orphans
python3 lib/scripts/resolve-spec-paths.py --orphans             # orphan *.spec.md only
```

The rules it implements (so readers know what to expect):

**Membership** — a file belongs to a domain if it matches `pattern` (regex) **OR** any `include` glob, **minus** any `exclude` glob. One regex assumes tidy code; `include`/`exclude` handle scattered legacy layouts (prefer globs over individual files so the list doesn't rot).

**Resolution** — `colocated` → `specPath` (error if missing); else `{specDir}/<domain>/spec.md` (`specDir` defaults to `.specs`).

**Discovery (`--all`)** — the **union** of `.sdd.json` `domains` and the `.specs/*/spec.md` glob, de-duplicated by resolved path. Covers colocated specs (outside `.specs/`) and centralized ones with no config entry.

**Ordering (`--changed`)** — matches are returned **most-specific first** (deepest scope path that prefixes the changed file). So a change under `src/checkout/cart/` lists `cart` before `checkout` — the **leaf is primary context**, the parent is the frame. A zero-config fallback also matches a file's parent-directory basename against an existing `{specDir}/<dir>/spec.md`.

**Tier files** — each domain resolves to a tiered set: `<base>.spec.md` (hot — requirements), `<base>.arch.md` (cold — architecture + diagrams), `<base>.coverage.md` (test — R###→tests). PR-current SDD loads/syncs **only `.spec.md`**; `.arch.md`/`.coverage.md` are reserved (recognized, never flagged as orphans). Their consumption (arch lazy-load, coverage→conformance) is a separate spec. See `.sdd/decisions/0002-living-spec-location-tiering.md`.

**Orphans** — a `*.spec.md` in the tree not claimed by any configured `specPath` (excluding `specs/`, `specDir`, and `specExempt`) is flagged `ℹ Orphan living spec <path> — not referenced by any .sdd.json domain` and skipped. `.spec.md` is reserved for SDD living specs.

**Template selection** (`specFormat`, used when *creating* a living spec) — an **open value**, resolving by convention to `lib/templates/spec-<specFormat>.md`, falling back to `spec-living.md` (generic) when no such template exists. Built-ins: `component`, `endpoint`. Projects add their own (`feature`, `service`, `page`, `overview`, …) by dropping a template file — no code change.

**Authoring convention (tree of specs):** parent/area specs hold high-level rules, cross-cutting constraints, and diagrams (use the `overview` format); leaf specs hold the detailed requirements. Reading only the leaf gets ~90% of the context; the parent adds the architectural frame.

## Loading procedure

1. Run `resolve-spec-paths.py --changed <touched files>`; the touched set is the Layer 2 spec.md "Files to Change" list (or recently-modified files when no plan yet).
2. Read each matched domain's `.spec.md` in parallel, **in returned order** (most-specific first → treat the leaf as primary). Record the domain names in `.spec-context.json#loadedDomains` (string array) so `/sdd:plan` and `/sdd:implement` reuse the result.
3. Never modify a Layer 1 file from `/sdd:specify` or `/sdd:plan` — Layer 1 is mutated **only** by `/sdd:implement` at CP3 sync time.

## Delta operations (Layer 2 → Layer 1 sync)

`/sdd:implement` parses the per-feature `specs/{NNN}-{slug}/spec.md` for delta blocks and applies them to each loaded domain's living spec — at the path from `resolve(<domain>)` (centralized or colocated) — at CP3 closure (after the user approves the commit, before `git commit` runs).

Block heading detection (case-sensitive, top-level `##`):

| Block | Operation | Applied to `.specs/<domain>/spec.md` |
|---|---|---|
| `## ADDED Requirements` | append | each `### R<id>` subsection appended to the Requirements section in order |
| `## MODIFIED Requirements` | replace | each `### R<id>` subsection replaces the existing block with the same id |
| `## REMOVED Requirements` | delete | for each `- **R<id>**` bullet, delete the matching `### R<id>` subsection |
| `## RENAMED Requirements` | rename | for each `- **R<id>**: `Old` → `New`` bullet, update only the heading name on the matching `### R<id>` subsection |

Multi-domain deltas — **write to the most-specific domain only.** When `loadedDomains` has more than one entry (a parent + leaf tree), each delta operation is applied to the **most-specific** matched domain (the first/leaf in the most-specific-first order from `resolve-spec-paths.py`), **not** to every loaded domain. To target a different or additional domain, annotate the block with `<!-- domain: <name> -->` immediately above the operation — markered blocks apply only to the named domain(s). This prevents a single requirement from being duplicated up and down the tree (read-all for context, write-most-specific for precision).

Sync writes log a one-line summary per domain (`✓ Synced 2 added, 1 modified into .specs/auth/spec.md`) and update `.spec-context.json#syncedDomains` so re-runs are observable.

## When the spec has no delta blocks

If `specs/{NNN}-{slug}/spec.md` contains no recognised delta block, sync is a no-op. This is the common case for purely additive features that don't intersect any existing domain — Layer 1 isn't grown unless the author explicitly writes a delta.
