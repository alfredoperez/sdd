# Plan: Fix Auto Mode Stall

**Spec**: [spec.md](./spec.md) | **Date**: 2026-04-13

## Approach

Move the `auto: true` flag write from Step 2 (after specify) to Step 1 (before specify). Add explicit "DO NOT STOP" instructions to the auto-advance loop to prevent AI stalling after Skill tool returns.

## Files to Change

### Modify

- `skills/auto/SKILL.md` — reorder steps so auto flag is set before specify invocation; add explicit loop continuation instructions
