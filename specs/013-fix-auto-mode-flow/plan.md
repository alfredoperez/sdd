# Plan: Fix Auto Mode Flow

**Spec**: [spec.md](./spec.md) | **Date**: 2026-03-29

## Approach

Add an `auto` boolean to `state.json` that `/sdd:auto` sets to `true` before entering the advance loop. Each skill reads this field in its Summary step and conditionally omits the `👉 Run /sdd:...` hint line when `auto` is `true`, showing `🔄 Auto mode — continuing...` instead. Auto clears the field on completion. This keeps manual invocations unchanged while preventing the hints from confusing the auto-advance loop.

## Files

### Create

(none)

### Modify

- `skills/auto/SKILL.md` — set `auto: true` in state.json after specify, clear on completion
- `skills/specify/SKILL.md` — conditional `👉` hint in both minimal and normal summary outputs
- `skills/plan/SKILL.md` — conditional `👉` hint in summary output
- `skills/tasks/SKILL.md` — conditional `👉` hint in summary output
- `docs/ARCHITECTURE.md` — document `auto` field in core fields table

## Risks

- LLM may still stop despite suppressed hints if it interprets the summary as a stopping point: mitigation is to show explicit `🔄 Auto mode — continuing...` line when auto is true
