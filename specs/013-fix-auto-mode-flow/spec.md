# Spec: Fix Auto Mode Flow

**Slug**: 013-fix-auto-mode-flow | **Date**: 2026-03-29

## Summary

When `/sdd:auto` runs, each skill (plan, tasks, specify) displays "👉 Run `/sdd:{next}` ..." hints in its summary output. These hints confuse the auto-advance loop, causing it to stop between steps instead of continuing. The fix adds an `auto` boolean to `state.json` so skills can detect auto mode and suppress manual next-step hints.

## Requirements

- **R001** (MUST): Add `auto` field to state.json schema — boolean, default `false`
- **R002** (MUST): `/sdd:auto` sets `auto: true` in state.json after specify completes (before the auto-advance loop begins)
- **R003** (MUST): Each skill's summary output conditionally omits the `👉 Run /sdd:...` hint line when `state.json` has `auto: true`
- **R004** (MUST): When auto is true, skills still display the status summary (feature name, counts, file path) — only the manual hint line is suppressed
- **R005** (MUST): `/sdd:auto` sets `auto` back to `false` when the pipeline completes (next == "done")
- **R006** (SHOULD): Document the `auto` field in ARCHITECTURE.md alongside other core fields

## Scenarios

### Auto mode runs end-to-end without stopping

**When** user runs `/sdd:auto "some feature"`
**Then** state.json gets `auto: true` before the loop starts, each skill omits the "👉 Run..." line, and the loop continues uninterrupted through plan → tasks → implement

### Manual mode unchanged

**When** user runs `/sdd:plan 013-fix-auto-mode-flow` directly (not via auto)
**Then** state.json has `auto: false` (or no `auto` field), and the "👉 Run..." hint displays as before

### Auto mode cleans up on completion

**When** the auto-advance loop detects `next: "done"`
**Then** `auto` is set back to `false` in state.json

## Out of Scope

- Persisting auto mode across conversation restarts (if conversation drops, user re-runs manually)
- Adding auto tracking for `/sdd:continue` when invoked standalone
