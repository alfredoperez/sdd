---
name: sdd:specify
description: "SDD — Spec-Driven Development: write a lean spec for rapid iteration."
---

## User Input

```text
$ARGUMENTS
```

If `$ARGUMENTS` is empty, stop and say: "Provide a feature description: `/sdd:specify <description>`"

---

## Steps

### 1. Parse Input

Extract the feature description from `$ARGUMENTS`.

Generate a concise slug (2–4 words, action-noun format, lowercase, hyphens):
- "add clickable file references" → `clickable-file-refs`
- "fix payment timeout bug" → `fix-payment-timeout`
- Preserve technical terms (OAuth2, JWT, API)

---

### 2. Determine Spec Number + Create Directory

Scan `specs/` locally for directories matching `[0-9]+-*`:

- Extract the highest number N found; use N+1 as the new number.
- If no spec dirs exist, start at 1.

```bash
mkdir -p specs/{NNN}-{slug}
```

Write `specs/{NNN}-{slug}/state.json`:

```json
{ "step": "specify", "task": null, "substep": "parsing", "updated": "{TODAY}" }
```

---

### 3. Explore Inline

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"exploring"`.

Without spawning a subagent, read 2–3 relevant files to understand the feature area:
- Run Glob and Grep searches in parallel (single message, multiple tool calls) to find files related to the feature description
- Read key sections to understand patterns, architecture, and constraints

---

### 4. Detect Complexity

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"detecting"`.

Based on what you found in Explore, classify the change:

| Signal | Mode |
|--------|------|
| Touches ≤3 existing files, change is <10 lines | **minimal** |
| Pure style or config tweak | **minimal** |
| Touches 4+ files, or adds a new component/service | **normal** |
| Introduces new public behavior or API | **normal** |

If unclear, default to **normal**.

---

### 5. Write `specs/{NNN}-{slug}/spec.md`

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"writing-spec"`.

Read `lib/templates/spec-normal.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), and write the result to `specs/{NNN}-{slug}/spec.md`.

**Skip**: clarification rounds, formal edge case analysis, exploration findings section, quality checklists.

---

### 6. Minimal Mode — Write `plan.md` + `tasks.md`

Skip this step if mode is **normal**.

Write `specs/{NNN}-{slug}/plan.md`:

Read `lib/templates/plan.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), simplify optional sections (omit Technical Context, Flow, Data Model, Risks — keep only Approach and a `## Files to Change` list), and write to `specs/{NNN}-{slug}/plan.md`.

Write `specs/{NNN}-{slug}/tasks.md`:

Read `lib/templates/tasks.md`, fill placeholders (`{Feature Name}`, `{TODAY}`), keep only Phase 1 with the relevant tasks (omit Phase 2 for minimal changes), and write to `specs/{NNN}-{slug}/tasks.md`.

Update `specs/{NNN}-{slug}/state.json`:

```json
{ "step": "tasks", "task": null, "substep": null, "updated": "{TODAY}" }
```

---

### 7. Summary

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `null`.

**Minimal mode** — display exactly this format:

```
--- Specify complete (Fast Mode) ---
Feature: {Feature Name}  |  Slug: {NNN}-{slug}
Spec:    specs/{NNN}-{slug}/spec.md
Plan:    specs/{NNN}-{slug}/plan.md
Tasks:   specs/{NNN}-{slug}/tasks.md

Next: /sdd:implement {NNN}-{slug}
```

**Normal mode** — display exactly this format:

```
--- Specify complete ---
Feature: {Feature Name}  |  Slug: {NNN}-{slug}
Spec:    specs/{NNN}-{slug}/spec.md

Next: /sdd:plan {NNN}-{slug}
```
