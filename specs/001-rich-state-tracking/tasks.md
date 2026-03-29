# Tasks: Richer State Tracking

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-29

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Update specify SKILL.md to write step_summaries.specify — `skills/specify/SKILL.md`
  - **Do**: In the specify skill's Step 7 (Summary), before updating state.json with `substep: null`, add instructions to write `step_summaries.specify` to state.json with fields: `complexity` (minimal/normal), `requirements` (count of R### items from spec.md), `scenarios` (count of scenario sections), `key_finding` (one-line summary of the most important codebase pattern discovered during exploration). For minimal mode, also include this in the state.json written in Step 6.
  - **Verify**: Read the updated SKILL.md and confirm the step_summaries.specify write is present in both normal and minimal mode paths, with all 4 fields documented.

- [x] **T002** Update plan SKILL.md to write step_summaries.plan and approach *(depends on T001)* — `skills/plan/SKILL.md`
  - **Do**: In the plan skill's Step 3 (Summary), before updating state.json with `substep: null`, add instructions to write `step_summaries.plan` to state.json with fields: `approach_summary` (one-line from plan's Approach section), `files_planned` (count of files in Create + Modify tables), `risks` (array of risk strings from Risks section, empty array if none). Also write top-level `approach` field with the same one-line summary.
  - **Verify**: Read the updated SKILL.md and confirm step_summaries.plan and approach writes are present with all fields documented.

- [x] **T003** Update implement SKILL.md task execution loop *(depends on T002)* — `skills/implement/SKILL.md`
  - **Do**: In Step 2 (Phase 1), after marking each task `[x]` and updating `task` in state.json, add instructions to: (1) Write `task_summaries.{taskId}` with `status` (DONE or DONE_WITH_CONCERNS), `did` (one-line summary of what was actually done), `files` (array of files actually modified), `concerns` (array of concern strings, empty if none). (2) Update top-level `files_modified` array (deduplicated union). (3) Append to `decisions[]` if a non-trivial decision was made. (4) Append to `concerns[]` array (objects with `task` and `note`) if any concerns arose (silent fixes, type workarounds, edge cases). (5) Update `last_action` string. State.json must be written atomically (full JSON in one Write call).
  - **Verify**: Read the updated SKILL.md and confirm per-task writes cover all 5 fields. Confirm the deviation rules table still references noting for CP1.

- [x] **T004** Update implement SKILL.md resume logic *(depends on T003)* — `skills/implement/SKILL.md`
  - **Do**: In the Context Recovery section, update the resume logic: (1) Read `approach`, `last_action`, and `task_summaries` from state.json. (2) Use these to construct a focused context summary instead of fully re-reading spec.md and plan.md. (3) Still read tasks.md for remaining task definitions (unchecked tasks). (4) Still read spec.md for scenarios (needed at CP1). (5) Add a note that plan.md re-read can be skipped if `step_summaries.plan` exists in state.json.
  - **Verify**: Read the updated Context Recovery section and confirm it references the new state.json fields and describes the reduced re-read strategy.

- [x] **T005** Update implement SKILL.md CP1 display *(depends on T004)* — `skills/implement/SKILL.md`
  - **Do**: In Step 5 (Checkpoint 1 — Code Review), enhance the display format: (1) After the Changes section, add a **Concerns** section that reads `concerns[]` from state.json and displays them grouped by task ID. (2) In the Changes file list, compare `files_modified` against `step_summaries.plan.files_planned` — if a file wasn't in the original plan, append "(not in plan)" to its line. (3) Add a **Task Summaries** section showing `task_summaries.{taskId}.did` for each completed task.
  - **Verify**: Read the updated CP1 display format and confirm it includes concerns grouped by task, unplanned file flags, and per-task summaries.

- [x] **T006** Update ARCHITECTURE.md state.json documentation *(depends on T005)* — `docs/ARCHITECTURE.md`
  - **Do**: Replace the current state.json section (the 4-field example and table) with the full enriched schema. Include: (1) Complete JSON example showing all fields populated. (2) Field table with columns: Field, Type, Written By, Description. (3) Write timing section explaining when each field gets written. (4) Keep the existing substep values tables unchanged.
  - **Verify**: Read the updated ARCHITECTURE.md and confirm the state.json section has the full schema example, field table with all new fields, and write timing documentation.

---

## Phase 2: Quality (Parallel — launch agents in single message)

> The name in backticks after `—` is the **agent identifier** that `/sdd:implement` uses to spawn the subagent.

- [x] **T007** [P][A] Review SKILL.md consistency — `docs-expert`
  - **Files**: `skills/specify/SKILL.md`, `skills/plan/SKILL.md`, `skills/implement/SKILL.md`
  - **Do**: Verify all three SKILL.md files use consistent field names, JSON structure, and write patterns for state.json. Check that the schema documented in ARCHITECTURE.md matches what the skills actually write.
  - **Verify**: No field name mismatches or schema inconsistencies across the 4 files.

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001–T006 | [ ] |
| Phase 2 | T007 | [ ] |
