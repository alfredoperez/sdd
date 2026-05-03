---
name: sdd:adr
description: "SDD — Spec-Driven Development: scaffold a new Architectural Decision Record."
---

Usage: `/sdd:adr <slug>` — `<slug>` is kebab-case, descriptive (e.g., `cache-strategy`, `auth-provider-choice`).

## Steps

### 1. Validate inputs

Require `$ARGUMENTS` (the slug). If empty, stop: `Usage: /sdd:adr <slug>`.

Slug rules: 2–4 words, kebab-case. If invalid, suggest a corrected version.

### 2. Determine ADR number

Scan `.sdd/decisions/*.md`. Find the highest existing 4-digit prefix. New ADR number is highest + 1, zero-padded to 4 digits (e.g., `0001`, `0002`, ..., `0042`).

If `.sdd/decisions/` doesn't exist, prompt: `Run /sdd:init first.` and stop.

### 3. Create file

Write `.sdd/decisions/{NNNN}-{slug}.md` from `lib/templates/adr.md`, substituting:
- `{NNNN}` → 4-digit number from Step 2
- `{Title}` → ask user via `AskUserQuestion` for a one-line title (or derive Title Case from slug if user accepts)
- `{TODAY}` → current date (YYYY-MM-DD)
- `{deciders}` → `git config user.name` (default), user can override

### 4. Summary

```
✓ ADR {NNNN} drafted

📂 .sdd/decisions/{NNNN}-{slug}.md

Status: Proposed
Title: {Title}

Edit the file to fill Context, Decision, Rationale, Alternatives, and Consequences sections.
Commit when ready: `git add .sdd/decisions/{NNNN}-{slug}.md && git commit -m "docs(adr): add ADR {NNNN}..."`.
```
