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
- Each spec directory contains: `spec.md`, `plan.md`, `tasks.md`, `state.json`

### state.json Format
```json
{
  "step": "specify | plan | tasks | implement",
  "task": "T001 | null",
  "substep": "string | null",
  "updated": "YYYY-MM-DD"
}
```

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

### Full Path (normal mode)
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
```
