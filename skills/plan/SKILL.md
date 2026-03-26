---
name: sdd:plan
description: "SDD — Spec-Driven Development: write a lean implementation plan."
---

## Steps

### 1. Load Context

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains a `spec.md`.

Read in parallel:
- `specs/{NNN}-{slug}/spec.md` — feature name, requirements, scenarios
- `specs/{NNN}-{slug}/state.json` — current step/task (if exists)

If no spec found, stop: "Run `/sdd:specify` first."

Update `specs/{NNN}-{slug}/state.json`:

```json
{ "step": "plan", "task": null, "substep": "loading", "updated": "{TODAY}" }
```

---

### 2. Write `specs/{NNN}-{slug}/plan.md`

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"writing-plan"`.

Read `lib/templates/plan.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), include or omit optional sections (Technical Context, Flow, Data Model, Risks) based on feature complexity, and write to `specs/{NNN}-{slug}/plan.md`.

**Skip**: research.md, contracts/, quickstart.md, constitution checks, auxiliary work flags.
**Optional** (include when relevant): Technical Context, Data Model table, Mermaid flow diagram.

---

### 3. Summary

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `null`.

Display exactly this format:

```
--- Plan complete ---
Feature: {Feature Name}
Plan:    specs/{NNN}-{slug}/plan.md  —  {N} files to create, {N} to modify

Next: /sdd:tasks {NNN}-{slug}
```
