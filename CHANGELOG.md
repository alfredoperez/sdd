# Changelog

## 1.4.0 (2026-03-26)

### Breaking Changes

- Removed `/sdd:improve` skill (personal Obsidian tracker, not core SDD)
- Removed bundled agents (`test-expert`, `docs-expert`) — install separately or use your own

### Features

- **Substep tracking** — `state.json` now tracks `substep` for precise recovery after context loss. Every skill writes substep boundaries (e.g., `code-review`, `phase1`, `exploring`)
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
- `state.json` for workflow resume
- Zero-config with optional `.sdd.json` customization
