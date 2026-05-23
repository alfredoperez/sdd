# SDD — Spec-Driven Development

## Overview

SDD is a structured workflow for AI-assisted development. Every feature goes through: **specify → plan → tasks → implement**. Small changes auto-detect and fast-track through the pipeline.

## Core Concepts

### Slug Rules
- 2–4 words, action-noun format, lowercase, hyphens
- Examples: `clickable-file-refs`, `fix-payment-timeout`
- Preserve technical terms (OAuth2, JWT, API)

### Spec Directory
- All specs live in `specs/{NNN}-{slug}/`
- NNN is zero-padded to 3 digits (001, 002, ...)
- Each spec directory contains: `spec.md`, `plan.md`, `tasks.md`, `.spec-context.json`

### .spec-context.json Format

The runtime state file is `specs/{NNN}-{slug}/.spec-context.json`. Every spec has one. SDD skills and (optionally) the SpecKit Companion VS Code extension both read and write it; both authors must follow read-then-merge and append-only `transitions[]`. `/sdd:implement` updates it via a per-spec [event journal](lib/instructions/event-journal.md) (a write-ahead log drained into the file at batched boundaries) rather than writing on every task.

**Canonical reference**: [`docs/STATE.md`](docs/STATE.md) — narrative + field tables.
**Machine-readable schema**: [`lib/schemas/spec-context.schema.json`](lib/schemas/spec-context.schema.json) (JSON Schema draft 2020-12).

When changing the schema (adding/renaming/removing a field, changing an enum, deprecating something), update **both** files in the same PR. See the [Docs Sync Rule](#docs-sync-rule) below.

### Commit Conventions
- Use conventional commits: `feat`, `fix`, `refactor`, `docs`, `chore`
- Scope from primary directory modified (lowercase)
- Imperative mood, lowercase, no period, max 72 chars
- No AI attribution lines (no Co-Authored-By, no "Generated with...")

### Complexity Detection
| Signal | Mode |
|--------|------|
| Touches ≤3 existing files, change is <10 lines | **minimal** |
| Pure style or config tweak | **minimal** |
| Touches 4+ files, or adds a new component/service | **normal** |
| Introduces new public behavior or API | **normal** |

If unclear, default to **normal**.

### Fast Path (Minimal Mode)
When `/sdd:specify` detects a minimal change, it auto-generates `plan.md` + `tasks.md` in one shot. Jump straight to `/sdd:implement`.

### Parallel Tasks (`[P]`)
In `tasks.md`, a task prefixed with `[P]` (e.g., `- [ ] **T002** [P] …`) is safe to run alongside adjacent `[P]` tasks. A run of consecutive `[P]` tasks forms a **parallel group** that `/sdd:implement` spawns as concurrent subagents in a single message; the main thread ticks checkboxes and appends a `group_done` event to the spec's [event journal](lib/instructions/event-journal.md) after the group returns (subagents never write `.spec-context.json` or the journal). A task without `[P]` is a gate — it waits for everything above it. Two tasks that modify the same file must never both be `[P]`.

### Project setup
SDD works with zero config. Optionally scaffold a `.sdd/` folder for project-wide context:

- `/sdd:init` — creates `.sdd/principles.md` (project MUSTs read by `/sdd:plan`), `.sdd/decisions/` (ADR storage), and a minimal `.sdd.json` if absent. Idempotent — never overwrites existing files.
- `/sdd:adr <slug>` — scaffolds the next 4-digit ADR in `.sdd/decisions/` from `lib/templates/adr.md`.

### Configuration
SDD works with zero config. Optionally create `.sdd.json` in your project root — see `docs/CONFIGURATION.md` for details.

Key settings:
- `branchStage` — `"specify"`, `"implement"`, or `"manual"` (default). Controls when SDD auto-creates the feature branch.
- `hooks` — map of hook-point keys to arrays of entries. Supported hook points: `pre:plan`, `post:plan`, `pre:implement`, `post:task`, `pre:code-review` (alias of `pre:checkpoint:code-review`), `pre:checkpoint:{code-review,test-results,commit-review}`, `pre:commit`, `post:pr`. Each entry is a plain subagent-prompt string, or an object with exactly one of `prompt` / `shell` / `skill`.

### Shared Instruction Files
Cross-cutting logic lives in `lib/instructions/`:
- `event-journal.md` — `/sdd:implement` appends context updates to a per-spec write-ahead log; `lib/scripts/drain-spec-context.py` materializes them into `.spec-context.json` at batched boundaries
- `transition-logging.md` — transition entry shape + millisecond `at`; one transition per write (directly, or materialized per journal event)
- `hook-execution.md` — execute `.sdd.json` hooks at the canonical hook points
- `branch-creation.md` — optional branch auto-creation + main-branch push guard

Skills reference these via `## Shared Instructions` blocks — they are the single source of truth for their behavior.

### Surface Guide

When changing SDD behavior, pick the right surface:

| Change | Surface |
|---|---|
| Behavior one skill must perform (steps, decisions, output formatting) | Skill prompt — `skills/*/SKILL.md` |
| Shape of a produced artifact (headings, placeholders, omit-comments) | Template — `lib/templates/*.md` |
| Cross-cutting behavior referenced by 2+ skills | Shared instruction — `lib/instructions/*.md` |
| Project-wide invariant every agent must know on every turn (schemas, conventions, naming) | This file (`CLAUDE.md`) |

Decision rule: if it changes how *one* skill behaves → skill prompt. If it changes the *shape of output* → template. If 2+ skills do the same thing → shared instruction. If every agent needs it on every turn → CLAUDE.md.

### Docs Sync Rule

When any of these change, update **every** listed surface in the same PR:

- `.sdd.json` schema fields or defaults → `docs/CONFIGURATION.md` and `README.md`
- `.spec-context.json` schema (any field) → `docs/STATE.md` AND `lib/schemas/spec-context.schema.json`. `CLAUDE.md` and `docs/ARCHITECTURE.md` carry pointers, not duplicate field tables — update those pointers only when the doc location itself moves.
- Hook-point list → `docs/CONFIGURATION.md` and `lib/instructions/hook-execution.md`
- Commit/PR/branch conventions → this file and relevant skill files
- Substep enumeration (per-step `progress` values) → `docs/STATE.md` (the canonical list) and any skill that introduces a new substep

**Catch-all**: any non-trivial behavior change ships docs forward in the same commit. If a reader of the affected doc would now be wrong, the doc is part of the change. Skipping docs is technical debt, not a shortcut.

## Workflow

### Auto Mode (recommended)
```
/sdd:auto "feature description"    — Run the full pipeline automatically
/sdd:resume                      — Advance one step (reads .spec-context.json)
/sdd:resume {NNN}-{slug}         — Advance a specific spec one step
```

For normal-complexity changes, `/sdd:auto` pauses after specify for spec review. For minimal changes, it runs straight through to implementation.

### Full Path (normal mode — manual)
```
/sdd:specify "feature description"
/sdd:plan {NNN}-{slug}
/sdd:tasks {NNN}-{slug}
/sdd:implement {NNN}-{slug}
```

### Fast Path (minimal mode — auto-detected)
```
/sdd:specify "small fix description"
/sdd:implement {NNN}-{slug}
```

### Utilities
```
/sdd:status              — Show all spec states
/sdd:pause {NNN}-{slug}  — Pause a spec (prevents auto-advance)
```
