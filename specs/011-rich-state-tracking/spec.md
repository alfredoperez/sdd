# Spec: Richer State Tracking

**Slug**: 011-rich-state-tracking | **Date**: 2026-03-29

## Summary

Enrich state.json with structured context (approach, decisions, concerns, files_modified, task_summaries, step_summaries) so that fresh sessions can resume intelligently without re-deriving everything from spec/plan/tasks artifacts. This feeds smarter CP1 displays, future auto mode orchestration, and quality tracking.

## Requirements

- **R001** (MUST): specify writes `step_summaries.specify` to state.json on completion with complexity, requirement count, scenario count, and key finding
- **R002** (MUST): plan writes `step_summaries.plan` and `approach` to state.json on completion with approach summary, planned file count, and identified risks
- **R003** (MUST): implement writes `task_summaries.{taskId}` after each task completes with status, did, files, and concerns
- **R004** (MUST): implement updates top-level `files_modified`, `decisions`, `concerns`, and `last_action` after each task
- **R005** (MUST): implement resume logic reads new state.json fields to reconstruct context without full artifact re-read
- **R006** (SHOULD): CP1 displays concerns grouped by task and flags files not in the original plan
- **R007** (MUST): ARCHITECTURE.md documents the full enriched state.json schema with field descriptions, write timing, and examples

## Scenarios

### Specify Completion

**When** specify finishes writing spec.md
**Then** state.json contains `step_summaries.specify` with complexity, requirements count, scenario count, and key finding

### Plan Completion

**When** plan finishes writing plan.md
**Then** state.json contains `step_summaries.plan` with approach summary, file count, risks; and top-level `approach` field

### Task Completion

**When** an implement task completes
**Then** state.json contains `task_summaries.{taskId}` with status/did/files/concerns, updated `files_modified` array, and `last_action` string

### Resume After Context Loss

**When** implement resumes from a fresh session with tasks already completed
**Then** it reads `approach`, `last_action`, and `task_summaries` from state.json to reconstruct context instead of fully re-reading spec.md and plan.md

### CP1 With Concerns

**When** CP1 code review runs and concerns exist
**Then** concerns are displayed grouped by task, and files not in the original plan are flagged

## Out of Scope

- Full context bracket awareness (Phase 2)
- Auto-unify/reconciliation drift detection algorithm (Phase 2)
- Structured status codes as formal agent protocol (Phase 4)
- Auto mode reading state for orchestration decisions
