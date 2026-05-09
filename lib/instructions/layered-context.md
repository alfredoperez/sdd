# Layered Context Loading

How SDD skills locate and load **Layer 1** (per-domain "living specs") so that `/sdd:specify` and `/sdd:plan` can ground feature work in the current truth of each affected capability.

Reference: `.sdd/decisions/0001-layered-context-loading.md`.

## Layers

| Layer | What | Where | Loaded by |
|---|---|---|---|
| 0 — Principles | Project-wide MUSTs | `.sdd/principles.md` | `/sdd:plan` (Principles Check) |
| 1 — Living specs | Current truth per capability | `.specs/<domain>/spec.md` | `/sdd:specify` + `/sdd:plan` (this file) |
| 2 — Feature delta | Per-feature change | `specs/{NNN}-{slug}/spec.md` | All skills (existing) |

All layers are **opt-in by presence** — each layer is silently skipped if the file/folder isn't there.

## Domain detection precedence

When a skill needs to determine which Layer 1 specs to load, it walks the precedence list below for the set of files the change touches (Layer 2 spec.md "Files to Change" section, or recently-modified files when no plan yet):

1. **Configured patterns**: read `.sdd.json` `domains` map. For each `<name>` in `domains`, test the regex `domains.<name>.pattern` against each touched file path. If **any** files match, the domain is in scope.
2. **Multiple matches**: if more than one configured domain matches, load **all** matching specs.
3. **Fallback** (no `domains` key, or no matches): for each touched file, try the basename of the parent directory as `<dir>` and look for `.specs/<dir>/spec.md`. Load any that exist.
4. **No matches**: return an empty list. Skills proceed as if no Layer 1 exists for this change.

Loaded domain names are recorded in `.spec-context.json#loadedDomains` (string array) so that `/sdd:plan` and `/sdd:implement` can reuse the result without recomputing.

## Loading procedure

Once domains are determined:

1. Read each `.specs/<domain>/spec.md` in parallel.
2. Surface them to the caller (specify uses them to seed delta operations; plan uses them for Domain Alignment Check).
3. Never modify a Layer 1 file from `/sdd:specify` or `/sdd:plan` — Layer 1 is mutated **only** by `/sdd:implement` at CP3 sync time.

## Delta operations (Layer 2 → Layer 1 sync)

`/sdd:implement` parses the per-feature `specs/{NNN}-{slug}/spec.md` for delta blocks and applies them to the corresponding `.specs/<domain>/spec.md` files at CP3 closure (after the user approves the commit, before `git commit` runs).

Block heading detection (case-sensitive, top-level `##`):

| Block | Operation | Applied to `.specs/<domain>/spec.md` |
|---|---|---|
| `## ADDED Requirements` | append | each `### R<id>` subsection appended to the Requirements section in order |
| `## MODIFIED Requirements` | replace | each `### R<id>` subsection replaces the existing block with the same id |
| `## REMOVED Requirements` | delete | for each `- **R<id>**` bullet, delete the matching `### R<id>` subsection |
| `## RENAMED Requirements` | rename | for each `- **R<id>**: `Old` → `New`` bullet, update only the heading name on the matching `### R<id>` subsection |

Multi-domain deltas: when `loadedDomains` has more than one entry, each delta operation is applied to **every** loaded domain unless the delta block is annotated `<!-- domain: <name> -->` immediately above the operation.

Sync writes log a one-line summary per domain (`✓ Synced 2 added, 1 modified into .specs/auth/spec.md`) and update `.spec-context.json#syncedDomains` so re-runs are observable.

## When the spec has no delta blocks

If `specs/{NNN}-{slug}/spec.md` contains no recognised delta block, sync is a no-op. This is the common case for purely additive features that don't intersect any existing domain — Layer 1 isn't grown unless the author explicitly writes a delta.
