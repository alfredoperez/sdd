# Spec: Align Spec-Context Schema with SpecKit Companion

**Slug**: 001-align-speckit-schema | **Date**: 2026-04-05

## Summary

Migrate `.spec-context.json` field names across all SDD skills and documentation to match the SpecKit Companion schema. Also ensure task completion uses markdown checkboxes consistently (no emoji markers).

## Requirements

- **R001** (MUST): Rename `step` to `currentStep` in all skill SKILL.md files and CLAUDE.md
- **R002** (MUST): Rename `substep` to `progress` in all skill SKILL.md files and CLAUDE.md
- **R003** (MUST): Rename `task` to `currentTask` in all skill SKILL.md files and CLAUDE.md
- **R004** (MUST): Remove `next` field — it is now derived from `currentStep` + workflow step array at read time
- **R005** (MUST): Remove `updated` field — it is now derived from latest `stepHistory` timestamp
- **R006** (MUST): Add `workflow: "sdd"` to all spec-context writes
- **R007** (MUST): Add `selectedAt` (ISO timestamp) on spec creation
- **R008** (MUST): Add `specName` (human-readable feature name) on spec creation
- **R009** (MUST): Add `branch` (git branch) on spec creation
- **R010** (MUST): Add `createdAt` (ISO timestamp) on spec creation
- **R011** (MUST): Update resume skill to derive next step from `currentStep` instead of reading `next` field
- **R012** (SHOULD): Add `checkpointStatus` tracking for commit/PR checkpoints in implement skill
- **R013** (MUST): Task completion uses `- [ ]`/`- [x]` checkboxes only — no emoji markers like `✅` for task completion status

## Scenarios

### Schema Migration in Specify Skill

**When** `/sdd:specify` creates a new spec
**Then** `.spec-context.json` uses `currentStep`, `progress`, `currentTask` and includes `workflow`, `selectedAt`, `specName`, `branch`, `createdAt`

### Resume Without Next Field

**When** `/sdd:resume` determines the next step
**Then** it derives the next step from `currentStep` + artifact presence instead of reading a `next` field

### Implement Reads New Fields

**When** `/sdd:implement` loads context or resumes mid-implementation
**Then** it reads `currentStep`, `progress`, `currentTask` (not old field names)

### Status Dashboard Uses New Fields

**When** `/sdd:status` displays the dashboard
**Then** it reads `currentStep`, `currentTask`, and `progress` from `.spec-context.json`

## Out of Scope

- Migrating existing spec directories with old-format `.spec-context.json` files
- Changing the SpecKit Companion extension itself
- Adding any new workflow steps beyond the existing specify/plan/tasks/implement
