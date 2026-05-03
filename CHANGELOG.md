# Changelog

## 1.16.0 (2026-05-03)

### Features

- **Added `/sdd:adr <slug>`** — scaffold the next ADR in `.sdd/decisions/{NNNN}-<slug>.md` from `lib/templates/adr.md`. Numbering auto-increments from the highest existing 4-digit prefix. Substitutes `{NNNN}`, `{Title}`, `{TODAY}`, and `{deciders}` (defaulting to `git config user.name`). Halts with `Run /sdd:init first.` if `.sdd/decisions/` is missing.

## 1.15.0 (2026-05-03)

### Features

- **Added `/sdd:init`** — scaffold a `.sdd/` folder for project-wide context. Creates `.sdd/principles.md` (from `lib/templates/principles.md`), `.sdd/decisions/.gitkeep`, and a minimal `.sdd.json` if none exists. Idempotent — re-running on an initialized project reports `✓ .sdd/ already initialized` and never overwrites existing files. Pairs with the Layer 0 Principles Check shipped in 1.14.x.

### Docs

- **CLAUDE.md** — new "Project setup" section pointing at `/sdd:init` and `/sdd:adr`.
- **docs/CONFIGURATION.md** — new "`.sdd/` folder" section documenting the layered-context artifacts (principles.md, decisions/) as siblings to `.sdd.json`.

## 1.14.0 (2026-05-03)

### Docs

- **Consolidated `.spec-context.json` schema docs** into a new canonical reference at `docs/STATE.md`. Adds machine-readable JSON Schema (draft 2020-12) at `lib/schemas/spec-context.schema.json`. Replaces the inline schema block in `CLAUDE.md` and the field-by-field section in `docs/ARCHITECTURE.md` with pointers — those files used to disagree (some fields were documented in one and not the other; `prUrl`, `prNumber`, `paused`, and `transitions` were missing from the CLAUDE.md schema block entirely). `docs/STATE.md` now covers all ~28 fields, lifecycle, multi-author write rules, substep enumeration per step, deprecation table, and required-vs-optional contract. Marks `step_summaries.plan.approach_summary` as deprecated (duplicates the top-level `approach` field; validators warn, skills strip on next rewrite).
- **Strengthened CLAUDE.md Docs Sync Rule**. Adds the new `docs/STATE.md` ↔ `lib/schemas/spec-context.schema.json` triangle. Adds an explicit catch-all closer: any non-trivial behavior change ships docs forward in the same commit. If a reader of the affected doc would now be wrong, the doc is part of the change.

No behavior changes — schema, lifecycle, and write rules remain identical to 1.13.0; this PR is documentation consolidation only.

## 1.13.0 (2026-05-03)

### Refactors

- **Tidied per-spec template boilerplate** (D2/D3/D4 from the SDD doc-quality eval). `lib/templates/tasks.md` no longer ships the 4-line `## Format` `[P]` block in every generated `tasks.md` — replaced with a single one-line pointer to `skills/tasks/SKILL.md` § Phase rules. `lib/templates/plan.md` Technical Context drops the verbatim `**Stack**: ...` example line; `Key Dependencies` and `Constraints` remain. Both `plan.md` and `tasks.md` template headers drop `| **Date**: {TODAY}` (spec.md remains the single source of truth for date). `skills/plan/SKILL.md` Step 2 instructs the agent to omit Technical Context entirely unless the spec changes language, runtime, or test framework.

## 1.12.0 (2026-05-03)

### Features

- **`/sdd:tasks` biased toward parallel decomposition** — `skills/tasks/SKILL.md` Phase rules now include an explicit parallelism-pass instruction ("group tasks by file path; any task whose file appears nowhere else is a `[P]` candidate") and a sanity-check that flags any 5+ task spec emerging with zero `[P]` markers as likely missing a pass. The conservative-bias closer "When unsure, omit `[P]`. Sequential is always safe." has been replaced with "prefer the interpretation with more `[P]` markers; sequential is the safe-but-slow fallback, not the default." `[P]` semantics themselves (file-disjoint + no data dep) are unchanged.

### Docs

- **CLAUDE.md Surface Guide** — added a `### Surface Guide` rubric under `## Core Concepts` mapping types of SDD changes to their correct surface (skill prompt / template / shared instruction / CLAUDE.md). Codifies the decision rule used when picking where SDD behavior changes belong so future eval-card decisions route consistently.

## 1.11.1 (2026-04-27)

### Fixes

- **`/sdd:auto` normal-mode spec-review handoff** — in normal complexity, `/sdd:specify` could end with a misleading "🔄 Auto mode — continuing…" footer that read like an end-of-turn signal, after which the orchestrator's spec-review approval gate would not fire until the user prompted "are you continuing?". Two fixes: (1) `/sdd:specify` no longer prints a "continuing…" footer in the normal-mode auto branch — instead it announces "orchestrator will gate for approval next", since `/sdd:auto` displays the gate immediately on return; (2) `/sdd:auto` collapses the previous Step 1 (run specify) + Step 2 (detect complexity) + Step 3 (gate) into a single continuous Step 1 so the gate-display is no longer behind a step boundary the model can interpret as a turn end. The "set `auto` to `true`" sub-action also explicitly tells the model not to set the field early. Closes #17.

## 1.11.0 (2026-04-22)

### Features

- **Parallel task grouping (`[P]`)** — restores the ability to flag independent tasks for concurrent execution. `/sdd:tasks` now marks tasks `[P]` when they touch disjoint files and share no data dependency; `/sdd:implement` collects consecutive `[P]` tasks into a parallel group and spawns them as concurrent subagents in a single message. The main thread owns all writes to `tasks.md` and `.spec-context.json` to avoid races.

### Fixes

- **Checkbox placement in tasks template** — the phase-aggregate progress line (`- Phase 1: T001–T003 [ ]`) put the checkbox at the end of the line, which isn't standard Markdown task-list syntax and wasn't clickable or parseable. Removed the vestigial `## Progress` footer entirely — per-task `[ ]` / `[x]` markers already show state.

### Backward Compatibility

- Existing specs with tasks generated under the old single-phase sequential model continue to work — `[P]` is opt-in. Any task without `[P]` runs solo exactly as before.

## 1.10.2 (2026-04-21)

### Fixes

- **Spec lifecycle status on ship** — `/sdd:implement` Step 8 now writes `status: "completed"` and `currentStep: "done"` to `.spec-context.json` when the PR is opened. Previously only `progress`, `next`, and `checkpointStatus` were updated, so downstream tools that group by `status` (like the SpecKit Companion tree view) left shipped specs in the Active group forever.

### Backward Compatibility

- Specs shipped before 1.10.2 whose `.spec-context.json` still has `status: "active"` (or missing) can be manually updated by setting `status: "completed"` — or by re-running `/sdd:implement` idempotently on the same spec.

## 1.10.1 (2026-04-21)

### Features

- **`{type}` variable in `branchNameFormat`** — `/sdd:specify` infers the conventional-commit type (`feat`, `fix`, `refactor`, `docs`, `chore`) from the feature description and stores it as `type` on `.spec-context.json`. `branch-creation.md` exposes it as `{type}`, so formats like `"{type}/{slug}"` produce `feat/add-oauth` or `fix/payment-timeout` automatically.
- **`type` field in `.spec-context.json`** — new string field written by `/sdd:specify`. Defaults to `feat` for older specs that lack it, so existing branches keep working.

### Backward Compatibility

- Existing `.sdd.json` files without `{type}` in `branchNameFormat` are unaffected.
- Specs created before 1.10.1 that lack the `type` field resolve `{type}` to `feat`.

## 1.10.0 (2026-04-21)

### Features

- **Branch-stage config** — new `branchStage` option in `.sdd.json` controls when SDD auto-creates the feature branch: `"specify"`, `"implement"`, or `"manual"` (default). Accompanying `branchNameFormat` (default `{NNN}-{slug}`). When any non-manual stage is set, a main-branch push guard in `/sdd:implement` Step 8 halts if the push would come from `main`/`master`.
- **Expanded hook points** — `hooks` in `.sdd.json` now supports 10 canonical hook points: `pre:plan`, `post:plan`, `pre:implement`, `post:task`, `pre:code-review` (alias of `pre:checkpoint:code-review`), `pre:checkpoint:code-review`, `pre:checkpoint:test-results`, `pre:checkpoint:commit-review`, `pre:commit`, `post:pr`. Per-hook-point blocking defaults (halt on `pre:implement` and `pre:commit`, warn elsewhere).
- **Three hook payload types** — entries can be plain subagent-prompt strings (unchanged), or object form with exactly one of `{ prompt }`, `{ shell }`, or `{ skill, args }`. Optional per-entry flags: `blocking`, `timeoutSeconds`, `parallel`. Template variables `{files}`, `{slug}`, `{spec-dir}` are substituted in every string field including `args`.
- **`workingBranch` field in `.spec-context.json`** — populated when `branchStage` auto-creates a branch. `branch` remains the audit-trail field (branch at specify time).
- **Shared instruction files** for cross-cutting behavior: `lib/instructions/hook-execution.md` and `lib/instructions/branch-creation.md`. Skills reference them via `## Shared Instructions` blocks.

### Docs

- `docs/CONFIGURATION.md` rewritten to cover branch config, 10 hook points, and three payload forms.
- `docs/ARCHITECTURE.md` adds the shared-instructions table and `workingBranch` field.
- `README.md` surfaces `branchStage` + `hooks` in the Configuration section.
- `CLAUDE.md` documents the hook-point list, `workingBranch` field, shared-instruction files, and a new Docs Sync Rule requiring doc updates in the same PR as schema/hook/convention changes.

### Backward Compatibility

- Zero-config projects behave identically to 1.9.x.
- Plain-string hook entries continue to resolve to subagent prompts.
- `pre:code-review` remains as an alias of `pre:checkpoint:code-review` (both arrays merged, deduplicated).
- Unknown hook-point keys log a warning and are skipped — never halt the pipeline.

## 1.9.1 (2026-04-13)

### Fixes

- **Auto mode stall** — Set `auto: true` immediately after specify (in Step 1) instead of in a separate step, preventing the flag from being missed. Added explicit loop continuation instructions to prevent AI from stalling after Skill tool invocations return.

## 1.9.0 (2026-04-05)

### Features

- **SpecKit Companion schema alignment** — `.spec-context.json` field names now match the SpecKit Companion extension schema: `step` → `currentStep`, `substep` → `progress`, `task` → `currentTask`
- **New metadata fields on spec creation** — `workflow`, `selectedAt`, `specName`, `branch`, `createdAt` are now written by `/sdd:specify` so specs display correctly in VS Code without extension gap-filling
- **Checkpoint status tracking** — `/sdd:implement` now writes `checkpointStatus` with commit/PR flags

### Breaking Changes

- `.spec-context.json` uses new field names (`currentStep`, `currentTask`, `progress`). Old field names (`step`, `task`, `substep`) are no longer written. Existing completed specs are not migrated.
- `next` and `updated` are kept as SDD-specific fields for CLI workflow use

## 1.8.0 (2026-04-02)

### Features

- **Resume skill** (`/sdd:resume`) — Renamed from `/sdd:continue` with clearer semantics. Clears paused state before advancing.
- **Pause skill** (`/sdd:pause`) — New skill that sets `paused: true` in `.spec-context.json` to prevent auto-advance
- **Paused indicator in status** — `/sdd:status` now shows "⏸ paused" for paused specs
- **Auto mode paused guard** — `/sdd:auto` stops with a message when encountering a paused spec

### Breaking Changes

- `/sdd:continue` renamed to `/sdd:resume` — old command no longer exists

## 1.7.0 (2026-03-29)

### Features

- **Template enhancements** (#3) — Added NFR section and MAY priority to spec template, renamed Flow to Architecture, added Testing Strategy and Leverage field to plan/tasks templates, converted tables to lists
- **Auto mode `auto` flag** — `.spec-context.json` now tracks `auto: true` when running via `/sdd:auto`. Skills read this flag to suppress manual `👉 Run /sdd:...` hints and show `🔄 Auto mode — continuing...` instead, preventing the auto-advance loop from stopping between steps.

## 1.6.0 (2026-03-29)

### Features

- **Auto mode** (`/sdd:auto`) — Run the full specify→plan→tasks→implement pipeline with a single command. Pauses for spec review on normal-complexity changes, runs straight through for minimal changes
- **Continue mode** (`/sdd:resume`, formerly `/sdd:continue`) — Advance one pipeline step at a time. Reads `.spec-context.json` `next` field with artifact-based fallback for crash recovery
- **`next` field in .spec-context.json** — All skills now write a `next` field on completion, enabling auto-advance and context recovery

## 1.5.0 (2026-03-26)

### Features

- **Enhanced skill outputs** — All skill summaries redesigned with emoji anchors (📋📐📝🚀✅) and natural language. Outputs now include contextual info: spec summaries, approach descriptions, task lists with IDs, file change counts
- **Human-readable checkpoints** — CP1/CP2/CP3 renamed to "Code Review", "Test Results", "Ready to ship" with clearer formatting
- **Status dashboard emojis** — Step column shows emoji indicators per workflow phase

## 1.4.0 (2026-03-26)

### Breaking Changes

- Removed `/sdd:improve` skill (personal Obsidian tracker, not core SDD)
- Removed bundled agents (`test-expert`, `docs-expert`) — install separately or use your own

### Features

- **Substep tracking** — `.spec-context.json` now tracks `substep` for precise recovery after context loss. Every skill writes substep boundaries (e.g., `code-review`, `phase1`, `exploring`)
- **Agent-agnostic Phase 2** — implement reads agent names from `[A]` tasks in `tasks.md` and spawns by name. Graceful skip if unavailable. Configurable via `.sdd.json` `agents` section
- **Named checkpoints** — `code-review`, `test-results`, `commit-review` replace `cp1`/`cp2`/`cp3`

### Refactors

- **Decoupled templates from skills** — skills load from `lib/templates/` instead of inlining. Single source of truth for all templates
- **Standardized template variables** — canonical variable set documented in `lib/templates/README.md`

### Docs

- Added `docs/ARCHITECTURE.md` with Mermaid diagrams (workflow, data flow, state machine, substep tables)
- Rewrote README with building blocks, state tracking, design principles
- Consolidated docs: removed WORKFLOWS.md, PHILOSOPHY.md, MIGRATION.md (merged into README)
- Fixed `minimalThreshold.maxFiles` default from 1 to 3 in CONFIGURATION.md

## 1.3.0 (2026-03-26)

### Features

- **Plan template enriched** — added Technical Context, optional Mermaid flow diagram, and Data Model sections to plan template

## 1.2.0 (2026-03-26)

### Features

- Relaxed minimal mode threshold from 1 to 3 files

## 1.1.1 (2026-03-25)

### Fixes

- Version bump for marketplace sync

## 1.1.0 (2026-03-25)

### Refactors

- Removed interactive checkpoint from plan skill
- Removed worktree and branch creation from SDD workflow

## 1.0.0 (2026-03-08)

### Features

- Initial release as standalone Claude Code plugin
- `/sdd:specify` — create specs with auto-complexity detection
- `/sdd:plan` — generate implementation plans
- `/sdd:tasks` — generate phased task lists
- `/sdd:implement` — execute tasks with 3 checkpoints
- `/sdd:status` — spec state dashboard
- Fast path for minimal changes (auto-detected)
- `.spec-context.json` for workflow resume
- Zero-config with optional `.sdd.json` customization
