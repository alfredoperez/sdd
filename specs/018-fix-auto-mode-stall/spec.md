# Spec: Fix Auto Mode Stall

**Slug**: 018-fix-auto-mode-stall | **Date**: 2026-04-13

## Summary

Fix `/sdd:auto` stopping after specify completes instead of continuing through the auto-advance loop. The AI loses track of the loop after Skill tool invocations return, causing the pipeline to stall.

## Requirements

- **R001** (MUST): Auto skill must set `auto: true` BEFORE invoking specify, so specify's summary output correctly shows the auto variant
- **R002** (MUST): Auto skill Step 5 loop instructions must explicitly state "DO NOT stop after the Skill tool returns — continue the loop" to prevent AI stalling
- **R003** (MUST): After each Skill tool invocation in the loop, the auto skill must read `.spec-context.json` and decide the next action without stopping

## Scenarios

### Auto Flag Set Before Specify

**When** `/sdd:auto` is invoked with a feature description
**Then** the auto skill sets `auto: true` in `.spec-context.json` before invoking specify, and specify sees the flag and shows the auto output variant

### Loop Continues After Each Skill Return

**When** the auto-advance loop invokes `/sdd:resume` and it returns
**Then** the auto skill reads `.spec-context.json`, checks completion conditions, and either loops again or stops — it never stalls

## Out of Scope

- Changes to the specify, plan, tasks, or implement skills
- Changes to the resume skill
