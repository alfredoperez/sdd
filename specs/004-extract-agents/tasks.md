# Tasks: Extract Agents from Core

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-26

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Delete bundled agent files — `agents/`
  - **Do**: Delete `agents/test-expert.md` and `agents/docs-expert.md` from the repository. If the `agents/` directory is now empty, delete the directory as well.
  - **Verify**: `ls agents/` returns "No such file or directory" or directory contains no agent files

- [x] **T002** Rewrite Phase 2 in implement skill — `skills/implement/SKILL.md`
  - **Do**: Replace lines 69–91 (the "Phase 2 — Parallel Agents" section) with agent-agnostic logic. The new section should:
    1. Keep the header `### 4. Phase 2 — Parallel Agents (normal mode only)`
    2. Keep the skip condition for minimal mode / Phase 2 omitted
    3. For each `[P][A]` task in tasks.md, attempt to spawn the agent named after the task's agent label (e.g., `test-expert`, `docs-expert`)
    4. If the agent is not available or the spawn fails, log a note: `⏭ Skipping {agent-name} — agent not available` and continue
    5. Wait for all successfully spawned subagents before proceeding to CP1
    6. Remove all hardcoded `test-expert` and `docs-expert` prompt blocks
  - **Verify**: Read `skills/implement/SKILL.md` — Phase 2 no longer contains hardcoded agent names; mentions graceful skip behavior

- [x] **T003** Update Phase 2 template in tasks skill — `skills/tasks/SKILL.md`
  - **Do**: In the Phase 2 template section (lines 57–63), update the example task to clarify the agent name is the spawned agent convention. Change the example from `— test-expert` to `— {agent-name}` and add a comment that `{agent-name}` should be the name of an available agent (e.g., `test-expert`, `docs-expert`). Keep the `[P][A]` markers.
  - **Verify**: Read `skills/tasks/SKILL.md` — Phase 2 template shows generic agent-name convention

- [x] **T004** Update tasks template — `lib/templates/tasks.md`
  - **Do**: In `lib/templates/tasks.md`, update the Phase 2 example task (line 29) to use a generic agent-name convention instead of hardcoded `test-expert`. Change `— \`test-expert\`` to `— \`{agent-name}\`` and keep the `[P][A]` markers. This aligns the template with the updated tasks skill.
  - **Verify**: Read `lib/templates/tasks.md` — Phase 2 example shows `{agent-name}` not `test-expert`

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001–T004 | [x] |
