# Spec: Remove Plan Checkpoint

**Slug**: 002-remove-plan-checkpoint | **Date**: 2026-03-26

## Summary

Remove the interactive "Plan ready for review" checkpoint from the `sdd:plan` skill. The plan should be written and the summary displayed without pausing for user approval, streamlining the workflow.

## Requirements

- **R001** (MUST): Remove the AskUserQuestion checkpoint (Step 3) from `skills/plan/SKILL.md`
- **R002** (MUST): Plan still displays its summary with the `Next:` prompt after writing `plan.md`
- **R003** (MUST): Step numbering remains sequential after removal

## Scenarios

### Normal Plan Run

**When** user runs `/sdd:plan {slug}`
**Then** plan.md is written and summary is displayed immediately — no approval prompt

## Out of Scope

- Changes to any other skill's checkpoints
