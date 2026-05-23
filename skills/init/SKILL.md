---
name: sdd:init
description: "SDD — Spec-Driven Development: scaffold .sdd/ and adopt living specs for an existing repo, one area at a time."
---

`/sdd:init` does two things, both optional and idempotent:

1. **Scaffold** — create the `.sdd/` folder for project-wide context (principles, ADR storage, config).
2. **Adopt** — incrementally bootstrap Layer 1 living specs from an existing codebase, **one area at a time**.

You can stop after the scaffold. Adoption is never forced, never whole-repo, and safe to re-run — it only adds new areas and never overwrites a spec you've reviewed.

## Shared Instructions

- [Layered Context](../../lib/instructions/layered-context.md) — living-spec paths, the resolver script (`lib/scripts/resolve-spec-paths.py`), tier files, and the `domains` registry.

## Steps

### 1. Detect state

Check the project root for: `.sdd.json`, `.sdd/principles.md`, `.sdd/decisions/`, and whether `.sdd.json` already has a `domains` map.

- If the scaffold artifacts are missing → first run: do **Phase 1**, then offer **Phase 2**.
- If they all already exist → already initialized: **skip Phase 1** and go straight to **Phase 2** (adopt another area).

---

### Phase 1 — Scaffold (Layer 0)

Build a list of only the artifacts that don't exist (never overwrite). If the list is empty, say `✓ .sdd/ already initialized` and go to Phase 2.

1. Present via **AskUserQuestion**: `Create all` / `Customize` / `Cancel`. (`Customize` → ask per-artifact yes/no.)
2. Create the chosen artifacts:
   - `.sdd.json` (only if absent): minimal default
     ```json
     { "specsDir": "specs", "commitFormat": "conventional", "noAttribution": true }
     ```
   - `.sdd/decisions/.gitkeep` (empty file so git tracks the folder).
   - `.sdd/principles.md` — ask via **AskUserQuestion** how to seed it:
     - **Blank template** — copy `lib/templates/principles.md` verbatim.
     - **Infer from codebase** — spawn one subagent: read lint/format/test/build config (e.g. eslint, prettier, tsconfig, `package.json` scripts, CI files), `CLAUDE.md`, and the folder layout, then draft 5–10 candidate project MUSTs in the `principles.md` bullet shape. **Ground every rule in something it actually saw**; mark anything uncertain for the user. Show the draft; the user confirms/edits before you write the file.
3. Output the created files.

---

### Phase 2 — Adopt an area (Layer 1)

**Optional and incremental.** Offer via **AskUserQuestion**: `Adopt living specs for an area now?` → `Yes` / `Not now`. If `Not now`, skip to Phase 3.

Adoption works **one area at a time** — it never scans the whole repo.

#### 2a. Survey (cheap — no source reading yet)

Read only the framework manifests (`package.json`, `nx.json`, `angular.json`, `pnpm-workspace.yaml`, etc.) and the **top-level folder layout**. From those, propose a short list of candidate areas (e.g. `auth`, `checkout`, `ui`, or an nx project name). Do **not** read source files in this step.

Present via **AskUserQuestion**: the candidate areas plus a `Type a path` option. The user picks **one**.

#### 2b. Propose a domain tree (one subagent)

Spawn **one** subagent scoped to the chosen area. It explores that subtree and returns a proposed **tree of domains** — a parent plus leaves when the area is large. For each node it proposes:

- `name` (kebab-case), `pattern` (regex), and `include`/`exclude` globs when the code is scattered across folders;
- `location` — prefer `colocated` (spec next to the area) with a `specPath`, or `centralized`;
- `specFormat` — pick from the available `lib/templates/spec-*.md`: `component` for UI, `endpoint` for APIs, else `feature`/generic.

The subagent **only returns the proposal** — it must not write files or edit `.sdd.json`.

Present the proposed tree via **AskUserQuestion**: `Confirm all` / `Edit` / `Drop some`. Let the user rename nodes, change paths/formats, or remove any.

#### 2c. Idempotency filter

Run `python3 lib/scripts/resolve-spec-paths.py --all` to list registered domains and existing spec paths. Drop any confirmed node whose `name` is already registered, or whose resolved `specPath` already exists **without** a `[DRAFT]` marker (i.e. a spec a human has reviewed). Tell the user what was skipped and why.

#### 2d. Surface-first extraction (parallel)

For each remaining leaf, spawn one subagent — **all in a single message** (parallel), each token-capped. Each subagent:

- Reads the **public surface** of its node's files: exports, route definitions, component props / inputs / outputs, exported types, function signatures. It goes one level into behavior only for the 1–3 primary files.
- Drafts the requirements spec from the node's `specFormat` template (`spec-living.md` / `spec-component.md` / `spec-endpoint.md`).
- Marks the whole spec `[DRAFT]` at the top. Tags each requirement `(observed)` or `(inferred)`. Marks anything uncertain `[NEEDS CLARIFICATION: <question>]`. Lists any files it could not read or confidently interpret under a `## Uncovered` section.
- **Returns the drafted markdown only** — it must not write files or touch `.sdd.json`. The main thread owns all writes.

Never fabricate requirements. If the surface is thin, write fewer requirements and say so under `## Uncovered`.

#### 2e. Write registry + specs (main thread)

1. **Read-merge** `.sdd.json` and append each confirmed domain to its `domains` map (keep all existing entries). Each entry carries `pattern` (+ `include`/`exclude` if proposed), `location`, `specPath`, `specFormat`.
2. Resolve each spec's path with `python3 lib/scripts/resolve-spec-paths.py --changed <a file in that domain>` (or `--all`) and write the drafted markdown there. Create **only** the `.spec.md` (requirements) tier — never `.arch.md` / `.coverage.md`.
3. Never overwrite a spec that lacks the `[DRAFT]` marker.

---

### Phase 3 — Summary

Display:

```
✓ SDD adoption — {area}

Registered {N} domain(s) in .sdd.json:
  - {name} → {specPath} ({specFormat}, {location})

Drafted {N} living spec(s)  [DRAFT — review before trusting]
  ⚠ {N} open question(s) marked [NEEDS CLARIFICATION]
  {N} file(s) listed under ## Uncovered

Next:
  • Review the drafts; remove the [DRAFT] line when you're happy.
  • Run /sdd:drift to see whether code has moved past these specs.
  • Run /sdd:init again to adopt another area.
```

If Phase 2 was skipped, show the original scaffold summary instead:

```
✓ SDD project initialized

Created:
  .sdd/principles.md       — edit to add your project's MUSTs
  .sdd/decisions/.gitkeep  — ADR storage (use /sdd:adr <slug>)
  .sdd.json                — workflow config

Next: edit .sdd/principles.md, then run /sdd:init again to adopt an area, or /sdd:specify to start a feature.
```
