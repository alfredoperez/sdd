# Changelog

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
