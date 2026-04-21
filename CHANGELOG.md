# Changelog

## 1.10.0 (2026-04-21)

### Features

- **Branch-stage config** — new `branchStage` option in `.sdd.json` controls when SDD auto-creates the feature branch: `"specify"`, `"implement"`, or `"manual"` (default). Accompanying `branchNameFormat` (default `{NNN}-{slug}`) with variables `{NNN}`, `{slug}`, `{Feature Name}`, and `{type}` (conventional-commit type inferred from the feature description during `/sdd:specify`). When any non-manual stage is set, a main-branch push guard in `/sdd:implement` Step 8 halts if the push would come from `main`/`master`.
- **`type` field in `.spec-context.json`** — `/sdd:specify` infers the conventional-commit type (`feat`, `fix`, `refactor`, `docs`, `chore`) from the feature description and stores it in `.spec-context.json`. Used by `branchNameFormat` (via `{type}`) and available for future commit-message consistency.
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
