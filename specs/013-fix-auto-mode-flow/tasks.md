# Tasks: Fix Auto Mode Flow

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-29

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Add auto flag to auto skill — `skills/auto/SKILL.md` | R001, R002, R005
  - **Do**: After Step 1 (specify completes), add a new step that reads state.json and sets `auto: true`. In Step 5 (auto-advance loop), after detecting `next: "done"`, set `auto` back to `false`.
  - **Verify**: SKILL.md contains auto set/clear logic
  - **Leverage**: `skills/auto/SKILL.md` (existing state.json read in Step 3)

- [x] **T002** Add conditional hint to specify skill *(depends on T001)* — `skills/specify/SKILL.md` | R003, R004
  - **Do**: In Step 7 (Summary), wrap the `👉 Run /sdd:...` line in both minimal and normal output blocks with a condition: only display if state.json `auto` is not `true`. When auto is true, replace with `🔄 Auto mode — continuing...`
  - **Verify**: Both summary formats have conditional hint logic

- [x] **T003** Add conditional hint to plan skill *(depends on T001)* — `skills/plan/SKILL.md` | R003, R004
  - **Do**: In Step 3 (Summary), read `auto` from state.json. If `auto` is `true`, omit the `👉 Run /sdd:tasks...` line and display `🔄 Auto mode — continuing...` instead.
  - **Verify**: Summary format has conditional hint logic

- [x] **T004** Add conditional hint to tasks skill *(depends on T001)* — `skills/tasks/SKILL.md` | R003, R004
  - **Do**: In Step 3 (Summary), read `auto` from state.json. If `auto` is `true`, omit the `👉 Run /sdd:implement...` line and display `🔄 Auto mode — continuing...` instead.
  - **Verify**: Summary format has conditional hint logic

- [x] **T005** Document auto field *(depends on T001)* — `docs/ARCHITECTURE.md` | R006
  - **Do**: Add `auto` to the Core Fields table with type `boolean`, written by `auto`, description: "true when running via /sdd:auto, false otherwise. Skills read this to suppress manual next-step hints."
  - **Verify**: Field appears in Core Fields table

---

## Phase 2: Quality (Parallel — launch agents in single message)

> No unit tests needed — these are markdown instruction files, not executable code.
> No docs task — T005 already covers ARCHITECTURE.md documentation.

---

## Progress

- Phase 1: T001–T005 [x]
