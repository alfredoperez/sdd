# Spec: Add Transition Logging

**Slug**: 017-add-transition-logging | **Date**: 2026-04-09

## Summary

Add a `transitions` array to `.spec-context.json` that records every state change made by SDD skills. Each write to `.spec-context.json` appends a transition entry capturing the current step/substep, the previous step/substep, the actor ("sdd"), and an ISO timestamp. A reusable instruction snippet in `lib/` keeps the logic DRY across all skill prompts.

## Requirements

- **R001** (MUST): Every skill that writes `.spec-context.json` must append a transition entry to the `transitions` array before/during the write
- **R002** (MUST): Each transition entry contains `step`, `substep`, `from` (object with previous `step`/`substep` or `null` on first write), `by` (always `"sdd"`), and `at` (ISO timestamp)
- **R003** (MUST): `from` captures the previous `currentStep`/`progress` values read BEFORE the write occurs
- **R004** (MUST): Transitions array is append-only — never truncated or rewritten
- **R005** (MUST): All existing `.spec-context.json` fields are preserved on every write
- **R006** (MUST): A reusable instruction or template in `lib/` defines the transition logging pattern so logic is not duplicated across skill files
- **R007** (MUST): No changes to existing field names, values, workflow logic, or step ordering

## Scenarios

### First Write (File Creation)

**When** a skill creates `.spec-context.json` for the first time (e.g., specify creating a new spec)
**Then** the `transitions` array contains one entry with `from: null`

### Subsequent Write

**When** a skill updates `.spec-context.json` (e.g., plan sets progress to "writing-plan")
**Then** the entry's `from` contains the previous `step` and `substep` values, and the new entry is appended (not replacing previous entries)

### Resume After Pause

**When** the resume skill unpauses a spec and advances it
**Then** a transition is logged for the unpause write, with `from` capturing the paused state

### Auto Mode Loop

**When** auto mode invokes multiple skills in sequence
**Then** each skill's writes independently append transitions, building a complete audit trail

## Out of Scope

- UI or CLI display of transitions
- Transition pruning or rotation
- Changes to files outside of skill prompts (`skills/*/SKILL.md`) and `lib/`
- Changes to the SpecKit Companion extension or `state.json`
