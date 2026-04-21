---
name: sdd:plan
description: "SDD — Spec-Driven Development: write a lean implementation plan."
---

## Shared Instructions

- [Transition Logging](../../lib/instructions/transition-logging.md) — append a transition entry on every `.spec-context.json` write
- [Hook Execution](../../lib/instructions/hook-execution.md) — run user-configured hooks at supported pipeline points

## Steps

### 1. Load Context

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains a `spec.md`.

Read in parallel:
- `specs/{NNN}-{slug}/spec.md` — feature name, requirements, scenarios
- `specs/{NNN}-{slug}/.spec-context.json` — current step/task (if exists)

If no spec found, stop: "Run `/sdd:specify` first."

Update `specs/{NNN}-{slug}/.spec-context.json` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md):

```json
{ "currentStep": "plan", "currentTask": null, "progress": "loading", "next": "tasks", "updated": "{TODAY}" }
```

Run `pre:plan` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir }`.

---

### 2. Write `specs/{NNN}-{slug}/plan.md`

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `"writing-plan"` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).

Read `lib/templates/plan.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), include or omit optional sections (Technical Context, Flow, Data Model, Risks) based on feature complexity, and write to `specs/{NNN}-{slug}/plan.md`.

**Skip**: research.md, contracts/, quickstart.md, constitution checks, auxiliary work flags.
**Optional** (include when relevant): Technical Context, Data Model table, Mermaid flow diagram.

Run `post:plan` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir }`.

---

### 3. Summary

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `null`, `next` to `"tasks"`, and include `approach` and `step_summaries.plan`. Append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md):

```json
{
  "currentStep": "plan",
  "currentTask": null,
  "progress": null,
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

Read `auto` from `specs/{NNN}-{slug}/.spec-context.json`. If `auto` is `true`, use the **(auto)** variant. Otherwise use the **(manual)** variant.

**Manual** — display exactly this format:

```
📐 **Plan ready**

{Feature Name} — {1-line summary of approach from plan's Approach section}
{N} files to create · {N} to modify

📂 `specs/{NNN}-{slug}/plan.md`

👉 Run `/sdd:tasks {NNN}-{slug}` to break it into tasks
```

**Auto** — display exactly this format:

```
📐 **Plan ready**

{Feature Name} — {1-line summary of approach from plan's Approach section}
{N} files to create · {N} to modify

📂 `specs/{NNN}-{slug}/plan.md`

🔄 Auto mode — continuing...
```
