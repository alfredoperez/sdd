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
```json
{
  "workflow": "sdd",
  "currentStep": "specify | plan | tasks | implement",
  "currentTask": "T001 | null",
  "progress": "string | null",
  "next": "plan | tasks | implement | done | null",
  "updated": "YYYY-MM-DD",
  "auto": "boolean",
  "selectedAt": "ISO timestamp",
  "specName": "string",
  "branch": "string",
  "workingBranch": "string | null",
  "type": "feat | fix | refactor | docs | chore",
  "createdAt": "ISO timestamp",
  "approach": "string | null",
  "decisions": ["string"],
  "concerns": [{ "task": "T002", "note": "string" }],
  "files_modified": ["string"],
  "last_action": "string | null",
  "checkpointStatus": { "commit": "boolean", "pr": "boolean" },
  "step_summaries": {
    "specify": { "complexity": "string", "requirements": "N", "scenarios": "N", "key_finding": "string" },
    "plan": { "approach_summary": "string", "files_planned": "N", "risks": ["string"] }
  },
  "task_summaries": {
    "T001": { "status": "DONE | DONE_WITH_CONCERNS", "did": "string", "files": ["string"], "concerns": ["string"] }
  },
  "status": "active | completed | archived",
  "stepHistory": {
    "specify": { "startedAt": "ISO", "completedAt": "ISO | null" }
  }
}
```

Extension-managed fields (`status`, `stepHistory`) are written by SpecKit Companion. SDD skills should preserve these fields when writing (read-then-merge, never overwrite the whole file).

Core fields (`currentStep`, `currentTask`, `progress`, `next`, `updated`) are always present. `workflow`, `selectedAt`, `specName`, `branch`, and `createdAt` are written once at spec creation. `branch` records the branch at specify time; `workingBranch` is populated only when `.sdd.json` `branchStage` auto-creates a branch (see `docs/CONFIGURATION.md`). `auto` is set to `true` by `/sdd:auto` and cleared on completion; skills read it to suppress manual next-step hints. Context fields are added progressively: `step_summaries.specify` by specify, `step_summaries.plan` + `approach` by plan, remaining fields by implement. See `docs/ARCHITECTURE.md` for full field documentation.

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
In `tasks.md`, a task prefixed with `[P]` (e.g., `- [ ] **T002** [P] …`) is safe to run alongside adjacent `[P]` tasks. A run of consecutive `[P]` tasks forms a **parallel group** that `/sdd:implement` spawns as concurrent subagents in a single message; the main thread ticks checkboxes and writes `.spec-context.json` after the group returns. A task without `[P]` is a gate — it waits for everything above it. Two tasks that modify the same file must never both be `[P]`.

### Configuration
SDD works with zero config. Optionally create `.sdd.json` in your project root — see `docs/CONFIGURATION.md` for details.

Key settings:
- `branchStage` — `"specify"`, `"implement"`, or `"manual"` (default). Controls when SDD auto-creates the feature branch.
- `hooks` — map of hook-point keys to arrays of entries. Supported hook points: `pre:plan`, `post:plan`, `pre:implement`, `post:task`, `pre:code-review` (alias of `pre:checkpoint:code-review`), `pre:checkpoint:{code-review,test-results,commit-review}`, `pre:commit`, `post:pr`. Each entry is a plain subagent-prompt string, or an object with exactly one of `prompt` / `shell` / `skill`.

### Shared Instruction Files
Cross-cutting logic lives in `lib/instructions/`:
- `transition-logging.md` — append to `.spec-context.json#transitions` on every write
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

When any of these change, update **every** place the schema is documented in the same PR:
- `.sdd.json` schema fields or defaults → `docs/CONFIGURATION.md` and `README.md`
- `.spec-context.json` fields → `docs/ARCHITECTURE.md` and this file (`CLAUDE.md`)
- Hook-point list → `docs/CONFIGURATION.md` and `lib/instructions/hook-execution.md`
- Commit/PR/branch conventions → this file and relevant skill files

Do not ship a behavior change without bringing the docs forward with it.

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
