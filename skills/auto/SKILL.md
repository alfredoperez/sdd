---
name: sdd:auto
description: "SDD — Spec-Driven Development: run the full pipeline automatically."
---

## User Input

```text
$ARGUMENTS
```

If `$ARGUMENTS` is empty, stop and say: "Provide a feature description: `/sdd:auto <description>`"

---

## Steps

### 1. Run Specify

Invoke `/sdd:specify` via the **Skill** tool, passing `$ARGUMENTS` as the argument.

When specify completes, find the most recently modified directory under `specs/` that contains a `state.json`. This is the spec that was just created. Record its slug (`{NNN}-{slug}`).

---

### 2. Set Auto Flag

Read `specs/{NNN}-{slug}/state.json` and set `auto` to `true`:

```json
{ "auto": true, ... }
```

Write the updated state.json back, preserving all existing fields.

---

### 3. Detect Complexity

Read `specs/{NNN}-{slug}/state.json`.

Determine complexity:
- If `state.json` shows `step: "tasks"` → **minimal** (specify already wrote plan.md + tasks.md)
- If `state.json` shows `step: "specify"` → **normal** (only spec.md was written)

---

### 4. Complexity Gate

**Minimal mode** — skip to Step 5 (auto-advance). No pause needed.

**Normal mode** — read `specs/{NNN}-{slug}/spec.md` and display:

```
📋 **Spec review — approval needed**

{Feature Name} (`{NNN}-{slug}`)

{1-line summary from the spec's Summary section}
{N} requirements · {N} scenarios

📂 `specs/{NNN}-{slug}/spec.md`
```

Use the **AskUserQuestion** tool with these options:
- **Continue** — proceed with auto-advance through remaining phases
- **Edit spec** — user provides edit notes in the "Other" field; apply changes to spec.md, then redisplay this gate

Do not proceed until the user approves.

---

### 5. Auto-Advance Loop

Loop until complete:

1. Invoke `/sdd:continue {NNN}-{slug}` via the **Skill** tool
2. After it returns, read `specs/{NNN}-{slug}/state.json`
3. If `next` is `"done"`, set `auto` to `false` in state.json, then stop — the pipeline is complete
4. If `step` is `"implement"` and `substep` is `null` and `next` is `"done"`, set `auto` to `false` in state.json, then stop — shipped
5. Otherwise, loop back to step 1

**Notes:**
- CP1 (Code Review) is handled by the implement skill's own AskUserQuestion — it will pause for user approval automatically. This skill does not bypass it.
- If any skill stops with a blocker (architectural change, impossible task), the loop naturally stops because the skill will have asked the user a question.
- The loop reads state.json after each invocation to determine if the pipeline is done, rather than counting steps.
