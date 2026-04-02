# Spec: Rename Continue to Resume & Add Pause

**Slug**: 015-rename-continue-add-pause | **Date**: 2026-04-02

## Summary

Rename the `/sdd:continue` skill to `/sdd:resume` for clearer semantics and add a new `/sdd:pause` skill that marks a spec as paused, preventing auto-advance. Resume should unpause before advancing.

## Requirements

- **R001** (MUST): Rename `skills/continue/` to `skills/resume/` and update the skill name to `sdd:resume`
- **R002** (MUST): All references to `/sdd:continue` across CLAUDE.md, auto SKILL.md, and other skills must update to `/sdd:resume`
- **R003** (MUST): Add a new `skills/pause/SKILL.md` that sets a `paused` flag in `.spec-context.json`
- **R004** (MUST): `/sdd:resume` must clear the `paused` flag before advancing the pipeline
- **R005** (SHOULD): `/sdd:status` should display paused state for specs that are paused
- **R006** (SHOULD): `/sdd:auto` should not advance a paused spec without explicit resume

## Scenarios

### Resuming a spec

**When** user runs `/sdd:resume` or `/sdd:resume {NNN}-{slug}`
**Then** the system advances to the next pipeline step (same behavior as current `/sdd:continue`)

### Pausing a spec

**When** user runs `/sdd:pause {NNN}-{slug}`
**Then** `.spec-context.json` gets `"paused": true` and a confirmation message is shown

### Resuming a paused spec

**When** user runs `/sdd:resume` on a spec that has `"paused": true`
**Then** the paused flag is cleared and the pipeline advances normally

### Status shows paused specs

**When** user runs `/sdd:status` and a spec is paused
**Then** the paused state is visible in the status output

## Out of Scope

- Pause reasons or metadata beyond the boolean flag
- Automatic pause triggers
- Pause/resume history tracking
