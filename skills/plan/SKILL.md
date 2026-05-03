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
- `.sdd/principles.md` — **Layer 0 of the layered context model.** Optional. If the file exists at the project root, load it; the bullet list of MUSTs will be checked against the Approach in Step 2 (Principles Check). If absent, skip the check entirely — `principles.md` is opt-in by presence.

If no spec found, stop: "Run `/sdd:specify` first."

Update `specs/{NNN}-{slug}/.spec-context.json` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md):

```json
{ "currentStep": "plan", "currentTask": null, "progress": "loading", "next": "tasks", "updated": "{TODAY}" }
```

Run `pre:plan` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir }`.

---

### 2. Write `specs/{NNN}-{slug}/plan.md`

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `"writing-plan"` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).

Read `lib/templates/plan.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), include or omit optional sections (Technical Context, Flow, Data Model, Risks) based on feature complexity, and write to `specs/{NNN}-{slug}/plan.md`. **Technical Context (Key Dependencies / Constraints) is project-fixed — omit the section entirely unless this spec changes language, runtime, or test framework.**

**Skip**: research.md, contracts/, quickstart.md, auxiliary work flags.
**Optional** (include when relevant): Technical Context, Data Model table, Mermaid flow diagram, Principles Check (see 2a below).

#### 2a. Principles Check (only if `.sdd/principles.md` was loaded in Step 1)

After the Approach section is drafted, scan the Approach text against each principle bullet from `.sdd/principles.md`. The check is **soft-warning only — never blocks the pipeline**.

For each principle, ask: does the Approach contain wording that contradicts this principle?
- Match on intent, not exact strings (e.g., principle "All UI strings must go through i18n" → flag if Approach says "hardcode the dialog text")
- Skip principles that don't apply to this feature's domain (e.g., a backend change need not be checked against a UI accessibility principle)

If **any conflicts** found, append this section to `plan.md` (after Approach, before Files):

```markdown
## ⚠ Principles Check

- **<principle one-line summary>** — <how the Approach conflicts; one line>
- **<principle one-line summary>** — <how the Approach conflicts; one line>

> Soft warning. The plan can proceed; address before implement or acknowledge in CP1.
```

If **no conflicts** found, **omit the section entirely** (per template convention — never leave empty sections).

Record the count: set `step_summaries.plan.principles_concerns` to the integer count (0 if none, or if no `.sdd/principles.md` was loaded). This is read in Step 3 to surface the count in the footer.

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
- `step_summaries.plan.principles_concerns`: integer count from Step 2a Principles Check (0 if no concerns, or if `.sdd/principles.md` was not loaded)
- Preserve any existing `step_summaries.specify` from the specify step

Read `auto` from `specs/{NNN}-{slug}/.spec-context.json`. If `auto` is `true`, use the **(auto)** variant. Otherwise use the **(manual)** variant.

**Manual** — display exactly this format:

```
📐 **Plan ready**

{Feature Name} — {1-line summary of approach from plan's Approach section}
{N} files to create · {N} to modify
{principles-line}

📂 `specs/{NNN}-{slug}/plan.md`

👉 Run `/sdd:tasks {NNN}-{slug}` to break it into tasks
```

**Auto** — display exactly this format:

```
📐 **Plan ready**

{Feature Name} — {1-line summary of approach from plan's Approach section}
{N} files to create · {N} to modify
{principles-line}

📂 `specs/{NNN}-{slug}/plan.md`

🔄 Auto mode — continuing...
```

**`{principles-line}` rules:**
- If `.sdd/principles.md` was not loaded in Step 1: omit the line entirely.
- If loaded with 0 concerns: `✓ Principles check passed`
- If loaded with N concerns (N > 0): `⚠ {N} principles concern{s} — see plan.md § Principles Check`

---

### 4. Auto Self-Chain

**Only runs when `auto` is `true`.** Skip entirely in manual mode.

After displaying the Auto summary above, invoke `/sdd:resume {NNN}-{slug}` via the **Skill** tool. This makes the "continuing..." footer real when `/sdd:plan` is invoked directly (outside the `/sdd:auto` orchestrator loop) on a spec that has `auto: true`.

Safe under nesting: when `/sdd:auto` invokes `/sdd:plan`, this self-chain fires first and advances to `/sdd:tasks`; when control returns to `/sdd:auto`'s loop, `/sdd:resume` is idempotent — it reads `currentStep` from `.spec-context.json` and resumes or no-ops as appropriate.
