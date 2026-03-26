# Spec: Add Sub-step Tracking

**Slug**: 005-add-substep-tracking | **Date**: 2026-03-26

## Summary

Add a `substep` field to `state.json` so every skill tracks granular progress. This enables fast recovery after context loss — instead of re-reading everything to figure out where we left off, the substep tells us exactly what was happening.

## Requirements

- **R001** (MUST): Add `substep` field to `state.json` format (nullable string)
- **R002** (MUST): `specify` skill updates substep through: `parsing`, `exploring`, `detecting`, `writing-spec`
- **R003** (MUST): `plan` skill updates substep through: `loading`, `writing-plan`
- **R004** (MUST): `tasks` skill updates substep through: `loading`, `writing-tasks`
- **R005** (MUST): `implement` skill updates substep through: `phase1`, `phase2`, `cp1`, `cp2`, `cp3`, `commit`, `push`, `pr`
- **R006** (MUST): Context recovery in implement reads `substep` to skip completed phases (e.g., if substep is `cp1`, skip Phase 1 and Phase 2)
- **R007** (MUST): All skills set `substep: null` on completion

## Scenarios

### Context loss during commit

**When** implement is at substep `commit` and context is lost
**Then** on resume, implement skips Phase 1, Phase 2, CP1, CP2 and picks up at commit step

### Context loss during specify exploration

**When** specify is at substep `exploring` and context is lost
**Then** on resume, specify skips parsing and restarts from exploration

### Normal completion

**When** any skill completes successfully
**Then** `substep` is set to `null` in state.json

## Out of Scope

- Substep tracking for `status` skill (read-only, no state)
- Substep tracking for `improve` skill (being removed in 003)
- UI display of substep in status dashboard (future enhancement)
