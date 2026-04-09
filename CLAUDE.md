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

Core fields (`currentStep`, `currentTask`, `progress`, `next`, `updated`) are always present. `workflow`, `selectedAt`, `specName`, `branch`, and `createdAt` are written once at spec creation. `auto` is set to `true` by `/sdd:auto` and cleared on completion; skills read it to suppress manual next-step hints. Context fields are added progressively: `step_summaries.specify` by specify, `step_summaries.plan` + `approach` by plan, remaining fields by implement. See `docs/ARCHITECTURE.md` for full field documentation.

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

### Configuration
SDD works with zero config. Optionally create `.sdd.json` in your project root — see `docs/CONFIGURATION.md` for details.

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
