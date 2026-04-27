---
name: sdd:auto
description: "SDD — Spec-Driven Development: run the full pipeline automatically."
---

## Shared Instructions

- [Transition Logging](../../lib/instructions/transition-logging.md) — append a transition entry on every `.spec-context.json` write

## User Input

```text
$ARGUMENTS
```

If `$ARGUMENTS` is empty, stop and say: "Provide a feature description: `/sdd:auto <description>`"

---

## Steps

### 1. Run Specify, Mark Auto, and Gate

**CRITICAL: This entire step is one continuous action — your turn is not complete until either the AskUserQuestion (sub-actions 5 + 6, normal mode) has been called, or you have entered the auto-advance loop (Step 2, minimal mode). The sub-actions below are NOT separate stop points.**

1. Invoke `/sdd:specify` via the **Skill** tool, passing `$ARGUMENTS` as the argument.

2. When specify completes, find the most recently modified directory under `specs/` that contains a `.spec-context.json`. Record its slug (`{NNN}-{slug}`).

3. Read `specs/{NNN}-{slug}/.spec-context.json` and set `auto` to `true`. Write the updated file back, preserving all existing fields and appending a transition entry per [transition-logging](../../lib/instructions/transition-logging.md). Do not set `auto` earlier — specify's footer behavior depends on `auto` being `false` during its run.

4. Determine complexity from the file you just read:
   - `currentStep: "tasks"` → **minimal** (specify already wrote plan.md + tasks.md). Proceed directly to Step 2 (Auto-Advance Loop). No gate.
   - `currentStep: "specify"` → **normal**. Continue to sub-actions 5 + 6 in this same step.

5. **Normal mode only** — read `specs/{NNN}-{slug}/spec.md` and display exactly:

   ```
   📋 **Spec review — approval needed**

   {Feature Name} (`{NNN}-{slug}`)

   {1-line summary from the spec's Summary section}
   {N} requirements · {N} scenarios

   📂 `specs/{NNN}-{slug}/spec.md`
   ```

6. **Normal mode only** — call **AskUserQuestion** with these options:
   - **Continue** — proceed with auto-advance through remaining phases
   - **Edit spec** — user provides edit notes in the "Other" field; apply changes to spec.md, then re-do sub-actions 5 + 6

   Do not proceed past sub-action 6 until the user approves.

---

### 2. Auto-Advance Loop

**CRITICAL: This is a loop. Do NOT stop or end your response after a Skill tool invocation returns. You MUST read `.spec-context.json` and continue the loop until a termination condition is met.**

Loop until complete:

1. Read `specs/{NNN}-{slug}/.spec-context.json`. If `paused` is `true`, display: "⏸ Spec is paused. Run `/sdd:resume` to continue." and stop.
2. Invoke `/sdd:resume {NNN}-{slug}` via the **Skill** tool
3. **After the Skill tool returns, you MUST continue — do NOT stop.** Read `specs/{NNN}-{slug}/.spec-context.json`
4. If `next` is `"done"`, set `auto` to `false` in .spec-context.json (append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md)), then stop — the pipeline is complete
5. If `currentStep` is `"implement"` and `progress` is `null` and `next` is `"done"`, set `auto` to `false` in .spec-context.json (append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md)), then stop — shipped
6. **Otherwise, loop back to step 1. Do NOT stop.**

**Notes:**
- CP1 (Code Review) is handled by the implement skill's own AskUserQuestion — it will pause for user approval automatically. This skill does not bypass it.
- If any skill stops with a blocker (architectural change, impossible task), the loop naturally stops because the skill will have asked the user a question.
- The loop reads .spec-context.json after each invocation to determine if the pipeline is done, rather than counting steps.
- The only valid reasons to stop are: `next` is `"done"`, spec is paused, or a skill asked the user a question.
