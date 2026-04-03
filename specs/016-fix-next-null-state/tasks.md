# Tasks: Fix next-null state during skill execution

**Date**: 2026-04-03

## Phase 1 — Core

- [x] **T001**: Update implement SKILL.md entry state
  - **Do**: In `skills/implement/SKILL.md`, change `"next": null` to `"next": "done"` in the Load step's JSON block (line 29)
  - **Verify**: The JSON block reads `"next": "done"`

- [x] **T002**: Update tasks SKILL.md entry state
  - **Do**: In `skills/tasks/SKILL.md`, change `"next": null` to `"next": "implement"` in the Load step's JSON block (line 23)
  - **Verify**: The JSON block reads `"next": "implement"`

- [x] **T003**: Update plan SKILL.md entry state
  - **Do**: In `skills/plan/SKILL.md`, change `"next": null` to `"next": "tasks"` in the Load step's JSON block (line 22)
  - **Verify**: The JSON block reads `"next": "tasks"`
