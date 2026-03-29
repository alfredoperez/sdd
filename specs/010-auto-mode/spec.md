# Spec: Auto Mode

**Slug**: 010-auto-mode | **Date**: 2026-03-29

## Summary

Add `/sdd:continue` (advance one pipeline step) and `/sdd:auto` (run the full pipeline) skills so users no longer have to manually copy slugs and invoke each phase. A `next` field in state.json enables skills to declare what comes after them, with artifact-based detection as a fallback for crash recovery.

## Requirements

- **R001** (MUST): `/sdd:continue` reads state.json from the most recently modified spec directory and advances to the next pipeline step
- **R002** (MUST): `/sdd:continue` falls back to artifact-based detection (presence of spec.md, plan.md, tasks.md) when `next` field is missing or stale
- **R003** (MUST): `/sdd:auto` accepts a feature description, runs `/sdd:specify`, then loops `/sdd:continue` until completion or a blocker
- **R004** (MUST): `/sdd:auto` pauses after specify for normal-complexity changes and shows the spec summary for user approval before continuing
- **R005** (MUST): `/sdd:auto` auto-advances through all phases for minimal-complexity changes without pausing after specify
- **R006** (MUST): CP1 (Code Review) still requires user approval in auto mode — no bypass
- **R007** (MUST): All existing skills (specify, plan, tasks, implement) write a `next` field to state.json on completion
- **R008** (SHOULD): Running `/sdd:continue` after implementation is complete shows "Feature is complete. Nothing to advance."
- **R009** (SHOULD): Direct skill invocation (`/sdd:implement 010-slug`) continues to work independently of auto mode

## Scenarios

### Full auto on minimal change

**When** user runs `/sdd:auto "fix typo in button"`
**Then** specify detects minimal, writes spec+plan+tasks, auto-advances to implement, executes tasks, hits CP1 for approval, commits and opens PR — no manual intervention between phases

### Pause after specify on normal change

**When** user runs `/sdd:auto "add auth middleware"`
**Then** specify detects normal, writes spec.md, pauses and shows spec summary with requirement/scenario counts, waits for user approval, then auto-advances through plan → tasks → implement → CP1

### Context loss recovery

**When** session crashes after plan.md is written but before tasks
**Then** `/sdd:continue` in a new session reads state.json `next: "tasks"`, validates plan.md exists, and runs `/sdd:tasks`

### Artifact-based fallback

**When** state.json `next` field is missing or stale after a crash
**Then** `/sdd:continue` checks which artifacts exist (spec.md, plan.md, tasks.md) and determines the correct next step

### Manual step-by-step with continue

**When** user runs `/sdd:specify "feature"` then `/sdd:continue` four times
**Then** each continue advances one phase (plan → tasks → implement → done), and a fifth continue says "Feature is complete"

### Direct skill still works

**When** user runs `/sdd:specify "feature"` then `/sdd:implement 005-feature` directly
**Then** implement skill works as before — auto mode does not break direct invocation

## Out of Scope

- Full return envelope protocol (Phase 5)
- Per-phase model assignment via `.sdd.json`
- DAG-based phase dependencies
- `--no-review` flag to skip CP1 in auto mode
- Analyze gate between tasks and implement
- Drift check gate
- Auto mode config in `.sdd.json`
