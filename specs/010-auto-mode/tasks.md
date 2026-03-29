# Tasks: Auto Mode

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-29

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Add `next` field to specify state.json writes — `skills/specify/SKILL.md`
  - **Do**: Add `"next": null` to the initial state.json write in Step 2. In Step 6 (minimal mode), change the state.json write to include `"next": "implement"`. In Step 7, add `"next": "plan"` to the normal-mode final state.json (substep null) and `"next": "implement"` to the minimal-mode final state.json.
  - **Verify**: All three state.json code blocks in SKILL.md include the `next` field with correct values

- [x] **T002** Add `next` field to plan state.json writes — `skills/plan/SKILL.md`
  - **Do**: In Step 1, add `"next": null` to the initial state.json write. In Step 3 (summary), change the final state.json write to include `"next": "tasks"`.
  - **Verify**: Both state.json code blocks in SKILL.md include the `next` field

- [x] **T003** Add `next` field to tasks state.json writes — `skills/tasks/SKILL.md`
  - **Do**: In Step 1, add `"next": null` to the initial state.json write. In Step 3 (summary), change the final state.json write to include `"next": "implement"`.
  - **Verify**: Both state.json code blocks in SKILL.md include the `next` field

- [x] **T004** Add `next` field to implement state.json writes — `skills/implement/SKILL.md`
  - **Do**: In Step 1, add `"next": null` to the initial state.json write. In Step 9 (summary), change the final state.json write to include `"next": "done"`.
  - **Verify**: Both state.json code blocks in SKILL.md include the `next` field

- [x] **T005** Create `/sdd:continue` skill — `skills/continue/SKILL.md`
  - **Do**: Create the skill with frontmatter (name: `sdd:continue`). Logic: (1) if `$ARGUMENTS` provided, use that spec dir, else find most recently modified spec dir with a state.json; (2) read state.json; (3) if `next` is `"done"`, display "Feature is complete. Nothing to advance."; (4) if `next` is present and valid, invoke that skill via the Skill tool passing the slug; (5) if `next` is missing/null, fall back to artifact detection: check for spec.md/plan.md/tasks.md presence and determine the next step; (6) if no spec dir found, say "Nothing in progress. Run `/sdd:specify <description>` to start."
  - **Verify**: SKILL.md is valid, covers all scenarios from spec (R001, R002, R008)

- [x] **T006** Create `/sdd:auto` skill — `skills/auto/SKILL.md`
  - **Do**: Create the skill with frontmatter (name: `sdd:auto`). Logic: (1) require `$ARGUMENTS` as feature description; (2) invoke `/sdd:specify` with the description via Skill tool; (3) read the generated spec.md to determine complexity (check for "minimal" in plan.md presence or state.json step); (4) complexity gate — if minimal, proceed; if normal, display spec summary (feature name, requirement count, scenario count) and use AskUserQuestion with options "Continue" / "Edit spec" before proceeding; (5) loop: invoke `/sdd:continue` with the slug, re-read state.json after each invocation, stop when `next` is `"done"` or a blocker is hit (CP1 handles its own approval via AskUserQuestion); (6) CP1 is not bypassed — implement skill handles it as usual.
  - **Verify**: SKILL.md is valid, covers R003–R006

- [x] **T007** Update CLAUDE.md — `CLAUDE.md`
  - **Do**: (1) Add `"next": "plan | tasks | implement | done | null"` to the state.json format block. (2) Add `/sdd:continue` and `/sdd:auto` to the Workflow section. (3) Add an "Auto Mode" workflow example showing both minimal and normal flows.
  - **Verify**: state.json format block shows all 5 fields, workflow section lists all 7 skills

---

## Phase 2: Quality (Parallel — launch agents in single message)

> The name in backticks after `—` is the **agent identifier** that `/sdd:implement` uses to spawn the subagent.

- [x] **T008** [P][A] Update docs for new skills — `docs-expert`
  - **Files**: `docs/SKILLS.md` (if exists), `docs/CONFIGURATION.md`
  - **Do**: Add documentation for `/sdd:continue` and `/sdd:auto` skills, including usage examples and the complexity gate behavior
  - **Verify**: Docs accurately reflect the implemented behavior

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001–T007 | [x] |
| Phase 2 | T008 | [x] |
