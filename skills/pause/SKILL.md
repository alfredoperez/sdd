---
name: sdd:pause
description: "SDD — Spec-Driven Development: pause a spec to prevent auto-advance."
---

## Steps

### 1. Find Spec

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains a `.spec-context.json`.

If no spec directory found, stop and say: "Nothing in progress. Run `/sdd:specify <description>` to start."

Read `specs/{NNN}-{slug}/.spec-context.json`.

---

### 2. Set Paused

If `.spec-context.json` already has `"paused": true`, display: "Already paused." and stop.

Otherwise, set `"paused": true` in `.spec-context.json` (preserve all other fields) and display:

```
⏸ Paused {NNN}-{slug}
```
