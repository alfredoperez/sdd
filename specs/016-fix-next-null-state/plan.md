# Plan: Fix next-null state during skill execution

**Slug**: 016-fix-next-null-state | **Date**: 2026-04-03

## Approach

Change the initial `.spec-context.json` write in each skill's Load step to set `next` to the logical successor instead of `null`. This ensures `/sdd:resume` always sees a meaningful `next` value.

## Files to Change

- `skills/implement/SKILL.md` — change `"next": null` to `"next": "done"` in the Load step
- `skills/tasks/SKILL.md` — change `"next": null` to `"next": "implement"` in the Load step
- `skills/plan/SKILL.md` — change `"next": null` to `"next": "tasks"` in the Load step
