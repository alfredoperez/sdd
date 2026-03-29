---
name: sdd:continue
description: "SDD — Spec-Driven Development: advance to the next pipeline step."
---

## Steps

### 1. Find Spec

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains a `state.json`.

If no spec directory found, stop and say: "Nothing in progress. Run `/sdd:specify <description>` to start."

Read `specs/{NNN}-{slug}/state.json`.

---

### 2. Determine Next Step

**Check `next` field first (fast path):**

| `next` value | Action |
|-------------|--------|
| `"plan"` | Invoke `/sdd:plan {NNN}-{slug}` |
| `"tasks"` | Invoke `/sdd:tasks {NNN}-{slug}` |
| `"implement"` | Invoke `/sdd:implement {NNN}-{slug}` |
| `"done"` | Display: "✅ Feature is complete. Nothing to advance." and stop |

**Artifact-based fallback** (if `next` is `null`, missing, or the file it implies already exists):

Check which files exist in `specs/{NNN}-{slug}/`:

| Artifacts present | Next step |
|-------------------|-----------|
| `spec.md` only | Invoke `/sdd:plan {NNN}-{slug}` |
| `spec.md` + `plan.md` | Invoke `/sdd:tasks {NNN}-{slug}` |
| `spec.md` + `plan.md` + `tasks.md` | Invoke `/sdd:implement {NNN}-{slug}` |
| `state.json` shows `step: "implement"` | Invoke `/sdd:implement {NNN}-{slug}` (resume) |

If none of the above match, stop and say: "Could not determine next step. Check `specs/{NNN}-{slug}/` for missing artifacts."

---

### 3. Invoke

Call the determined skill using the **Skill** tool, passing the spec slug (`{NNN}-{slug}`) as the argument.

If the Skill tool is not available, display the command for the user to run manually:

```
👉 Run `/sdd:{step} {NNN}-{slug}` to continue
```
