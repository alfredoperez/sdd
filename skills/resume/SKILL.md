---
name: sdd:resume
description: "SDD — Spec-Driven Development: advance to the next pipeline step."
---

## Shared Instructions

- [Transition Logging](../../lib/instructions/transition-logging.md) — append a transition entry on every `.spec-context.json` write

## Steps

### 1. Find Spec

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains a `.spec-context.json`.

If no spec directory found, stop and say: "Nothing in progress. Run `/sdd:specify <description>` to start."

Read `specs/{NNN}-{slug}/.spec-context.json`.

---

### 2. Check Paused State

If `.spec-context.json` has `"paused": true`:

1. Set `"paused": false` in `.spec-context.json` (preserve all other fields) and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md)
2. Display: "Resumed {NNN}-{slug}"

Then proceed to Step 3.

---

### 3. Determine Next Step

**Check `next` field first (fast path):**

| `next` value | Action |
|-------------|--------|
| `"plan"` | Invoke `/sdd:plan {NNN}-{slug}` |
| `"tasks"` | Invoke `/sdd:tasks {NNN}-{slug}` |
| `"implement"` | Invoke `/sdd:implement {NNN}-{slug}` |
| `"done"` | Display: "Done. Nothing to advance." and stop |

**Artifact-based fallback** (if `next` is `null`, missing, or the file it implies already exists):

Check which files exist in `specs/{NNN}-{slug}/`:

| Artifacts present | Next step |
|-------------------|-----------|
| `spec.md` only | Invoke `/sdd:plan {NNN}-{slug}` |
| `spec.md` + `plan.md` | Invoke `/sdd:tasks {NNN}-{slug}` |
| `spec.md` + `plan.md` + `tasks.md` | Invoke `/sdd:implement {NNN}-{slug}` |
| `.spec-context.json` shows `currentStep: "implement"` | Invoke `/sdd:implement {NNN}-{slug}` (resume) |

If none of the above match, stop and say: "Could not determine next step. Check `specs/{NNN}-{slug}/` for missing artifacts."

---

### 4. Invoke

Call the determined skill using the **Skill** tool, passing the spec slug (`{NNN}-{slug}`) as the argument.

If the Skill tool is not available, display the command for the user to run manually:

```
Run `/sdd:{step} {NNN}-{slug}` to continue
```
