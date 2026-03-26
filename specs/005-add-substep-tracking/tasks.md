# Tasks: Add Sub-step Tracking

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-26

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Add substep to state.json format docs — `CLAUDE.md`
  - **Do**: In `CLAUDE.md`, update the `state.json` format block to include `"substep": "string | null"`. Change the example from `{ "step": "...", "task": "...", "updated": "..." }` to `{ "step": "...", "task": "...", "substep": "...", "updated": "..." }`.
  - **Verify**: Read `CLAUDE.md` and confirm the state.json format section shows the `substep` field.

- [x] **T002** Add substep to configuration docs *(depends on T001)* — `docs/CONFIGURATION.md`
  - **Do**: No state.json format reference exists in `docs/CONFIGURATION.md` currently — skip this task if no reference to update. If a state.json section is added later, document `substep` there.
  - **Verify**: Confirm no stale state.json references exist in `docs/CONFIGURATION.md`.

- [x] **T003** Add substep tracking to specify skill *(depends on T001)* — `skills/specify/SKILL.md`
  - **Do**: In `skills/specify/SKILL.md`:
    1. In Step 1 (Parse Input), after "Write `specs/{NNN}-{slug}/state.json`", change the JSON to: `{ "step": "specify", "task": null, "substep": "parsing", "updated": "{TODAY}" }`
    2. At the start of Step 3 (Explore Inline), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `exploring`."
    3. At the start of Step 4 (Detect Complexity), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `detecting`."
    4. At the start of Step 5 (Write spec.md), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `writing-spec`."
    5. In Step 7 (Summary), before displaying output, add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `null`."
    6. In the minimal-mode state.json update (Step 6), add `"substep": null` to the JSON.
  - **Verify**: Read `skills/specify/SKILL.md` and confirm substep updates at each boundary: `parsing` → `exploring` → `detecting` → `writing-spec` → `null`.

- [x] **T004** Add substep tracking to plan skill *(depends on T001)* — `skills/plan/SKILL.md`
  - **Do**: In `skills/plan/SKILL.md`:
    1. In Step 1 (Load Context), change the state.json update to: `{ "step": "plan", "task": null, "substep": "loading", "updated": "{TODAY}" }`
    2. At the start of Step 2 (Write plan.md), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `writing-plan`."
    3. In Step 3 (Summary), before displaying output, add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `null`."
  - **Verify**: Read `skills/plan/SKILL.md` and confirm substep updates: `loading` → `writing-plan` → `null`.

- [x] **T005** Add substep tracking to tasks skill *(depends on T001)* — `skills/tasks/SKILL.md`
  - **Do**: In `skills/tasks/SKILL.md`:
    1. In Step 1 (Load Context), change the state.json update to: `{ "step": "tasks", "task": null, "substep": "loading", "updated": "{TODAY}" }`
    2. At the start of Step 2 (Write tasks.md), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `writing-tasks`."
    3. In Step 3 (Summary), before displaying output, add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `null`."
  - **Verify**: Read `skills/tasks/SKILL.md` and confirm substep updates: `loading` → `writing-tasks` → `null`.

- [x] **T006** Add substep tracking to implement skill *(depends on T001)* — `skills/implement/SKILL.md`
  - **Do**: In `skills/implement/SKILL.md`:
    1. In Step 1 (Load), change the state.json update to: `{ "step": "implement", "task": "T001", "substep": "phase1", "updated": "{TODAY}" }`
    2. At the start of Step 4 (Phase 2), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `phase2`."
    3. At the start of Step 5 (CP1), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `cp1`."
    4. At the start of Step 6 (CP2), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `cp2`."
    5. At the start of Step 7 (CP3), add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `cp3`."
    6. At the start of Step 8 (Commit + PR), add two substep updates: set `substep` to `commit` before the git commit, then set `substep` to `push` before `git push`, then set `substep` to `pr` before `gh pr create`.
    7. In Step 9 (Summary), before displaying output, add: "Update `specs/{NNN}-{slug}/state.json` — set `substep` to `null`."
  - **Verify**: Read `skills/implement/SKILL.md` and confirm substep updates: `phase1` → `phase2` → `cp1` → `cp2` → `cp3` → `commit` → `push` → `pr` → `null`.

- [x] **T007** Update context recovery to use substep *(depends on T006)* — `skills/implement/SKILL.md`
  - **Do**: In `skills/implement/SKILL.md`, replace the "Context Recovery" section with logic that reads `substep` from `state.json` and skips completed phases:
    1. If `substep` is `phase1` — resume from first unchecked task in Phase 1 (existing behavior)
    2. If `substep` is `phase2` — skip Phase 1, resume Phase 2
    3. If `substep` is `cp1` — skip Phase 1 + Phase 2, resume at CP1
    4. If `substep` is `cp2` — skip through CP1, resume at CP2
    5. If `substep` is `cp3` — skip through CP2, resume at CP3
    6. If `substep` is `commit`, `push`, or `pr` — skip through CP3, resume at Step 8 (Commit + PR) from the appropriate point
    7. If `substep` is `null` or missing — fall back to existing task-based recovery
  - **Verify**: Read the Context Recovery section and confirm substep-based skip logic covers all values.

- [x] **T008** Display substep in status dashboard *(depends on T003–T006)* — `skills/status/SKILL.md`
  - **Do**: In `skills/status/SKILL.md`, update Step 2 (Display Dashboard):
    1. Change the display rule for `implement` step: if `substep` is present, display as "implement (T003) [cp1]" (append substep in brackets).
    2. For all other steps with a non-null substep, append it similarly: e.g., "specify [exploring]", "plan [writing-plan]".
  - **Verify**: Read `skills/status/SKILL.md` and confirm substep display logic for all step types.

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001–T008 | [x] |
