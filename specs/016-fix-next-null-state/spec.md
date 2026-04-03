# Spec: Fix next-null state during skill execution

**Slug**: 016-fix-next-null-state | **Date**: 2026-04-03

## Summary

When a skill (implement, tasks, plan) starts executing, it sets `next: null` in `.spec-context.json`. If the user interrupts and runs `/sdd:resume`, it sees `next: null` and must fall through to artifact-based detection. The `next` field should always contain the logical successor step so resume can use the fast path.

## Requirements

- **R001** (MUST): `implement/SKILL.md` must set `next: "done"` on entry instead of `null`
- **R002** (MUST): `tasks/SKILL.md` must set `next: "implement"` on entry instead of `null`
- **R003** (MUST): `plan/SKILL.md` must set `next: "tasks"` on entry instead of `null`
- **R004** (MUST): Resume skill must continue to work correctly with the updated values

## Scenarios

### Resume during implement

**When** user interrupts during implement and runs `/sdd:resume`
**Then** resume reads `next: "done"` but `step: "implement"` indicates work is in progress, so it correctly resumes implementation via the artifact fallback (step=implement check)

### Resume during tasks generation

**When** user interrupts during tasks and runs `/sdd:resume`
**Then** resume reads `next: "implement"` and sees tasks.md doesn't exist yet, falls to artifact fallback which correctly routes to tasks

## Out of Scope

- Changing the resume skill's fallback logic (it already handles all cases correctly)
- Adding new state transitions or substeps
