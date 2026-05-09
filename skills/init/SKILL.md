---
name: sdd:init
description: "SDD — Spec-Driven Development: scaffold .sdd/ folder (principles, decisions) for a project."
---

## Steps

### 1. Detect current state

Check the project root (cwd) for:
- `.sdd.json` (existing JSON workflow config)
- `.sdd/principles.md`
- `.sdd/decisions/` directory

### 2. Plan + confirm

Build a list of artifacts to create (only those that don't exist). If the list is empty, output `✓ .sdd/ already initialized` and stop.

Present via `AskUserQuestion`:
- Options: "Create all", "Customize", "Cancel"
- If "Customize": ask per-artifact yes/no via `AskUserQuestion`.

### 3. Create artifacts

For each confirmed artifact:
- `.sdd/principles.md`: copy `lib/templates/principles.md`, no variable substitution.
- `.sdd/decisions/`: create directory + `.gitkeep` (empty file) so git tracks the empty folder.
- `.sdd.json`: only create if completely absent. Write a minimal default:
  ```json
  {
    "specsDir": "specs",
    "commitFormat": "conventional",
    "noAttribution": true
  }
  ```

Never overwrite existing files. If a file exists, skip it (idempotent).

### 4. Summary

```
✓ SDD project initialized

Created:
  .sdd/principles.md       — edit to add your project's MUSTs
  .sdd/decisions/.gitkeep  — ADR storage (use /sdd:adr <slug> to create)
  .sdd.json                — workflow config

Next: edit .sdd/principles.md and run /sdd:specify to start your first feature.
```
