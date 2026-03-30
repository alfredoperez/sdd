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
{ "step": "plan", "task": null, "substep": "loading", "next": null, "updated": "{TODAY}" }
```

---

### 2. Write `specs/{NNN}-{slug}/plan.md`

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"writing-plan"`.

Read `lib/templates/plan.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), include or omit optional sections (Technical Context, Flow, Data Model, Risks) based on feature complexity, and write to `specs/{NNN}-{slug}/plan.md`.

**Skip**: research.md, contracts/, quickstart.md, constitution checks, auxiliary work flags.
**Optional** (include when relevant): Technical Context, Data Model table, Mermaid flow diagram.

---

### 3. Summary

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `null`, `next` to `"tasks"`, and include `approach` and `step_summaries.plan`:

```json
{
  "step": "plan",
  "task": null,
  "substep": null,
  "next": "tasks",
  "updated": "{TODAY}",
  "approach": "one-line summary from the plan's Approach section",
  "step_summaries": {
    "specify": { "..." : "preserve existing step_summaries.specify if present" },
    "plan": {
      "approach_summary": "one-line summary from the plan's Approach section",
      "files_planned": N,
      "risks": ["risk string 1", "risk string 2"]
    }
  }
}
```

Where:
- `approach`: one-line summary extracted from the first sentence of the plan's ## Approach section
- `step_summaries.plan.approach_summary`: same as `approach`
- `step_summaries.plan.files_planned`: total count of files in the Create + Modify tables in plan.md
- `step_summaries.plan.risks`: array of risk strings from the ## Risks section; empty array `[]` if no risks
- Preserve any existing `step_summaries.specify` from the specify step

Display exactly this format:

```
📐 **Plan ready**

{Feature Name} — {1-line summary of approach from plan's Approach section}
{N} files to create · {N} to modify

📂 `specs/{NNN}-{slug}/plan.md`

👉 Run `/sdd:tasks {NNN}-{slug}` to break it into tasks
```
