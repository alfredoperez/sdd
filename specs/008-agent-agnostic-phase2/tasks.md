# Tasks: Make Phase 2 Agent-Agnostic

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-26

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Rewrite Phase 2 to parse agent tasks — `skills/implement/SKILL.md`
  - **Do**: Replace the hardcoded "Phase 2 — Parallel Agents" section (lines 69–91) with a generic version that: (1) reads all `[A]` tasks from tasks.md, (2) extracts the agent name from the task line (the value after `—` in backticks, e.g., `` `test-expert` ``), (3) builds each agent's prompt from the task's **Do**/**Verify**/**Files**/**Pattern**/**Reference** fields, (4) spawns each agent by parsed name in a single message, (5) if an agent is unavailable or fails to spawn, logs a warning and skips it (does not block other agents or CP1)
  - **Verify**: Read the updated section — no references to hardcoded `test-expert` or `docs-expert` remain; the instructions clearly describe parsing `[A]` tasks and spawning by extracted name

- [x] **T002** Update tasks.md template agent name convention *(depends on T001)* — `skills/tasks/SKILL.md`
  - **Do**: In the Phase 2 template section, update the example task and add a note clarifying that the value in backticks after `—` is the agent identifier used by implement to spawn the subagent (e.g., `` `test-expert` ``, `` `docs-expert` ``, `` `security-expert` ``). Add a second example showing a docs-expert task so the pattern is clear.
  - **Verify**: Read the updated template — the agent name convention is documented inline and two example agent tasks are shown

- [x] **T003** Document agents config in CONFIGURATION.md *(depends on T001)* — `docs/CONFIGURATION.md`
  - **Do**: Add an `### agents` section after the `checkpoints` section documenting the optional `agents` key in `.sdd.json`. Format: `"agents": { "<agent-name>": { "enabled": true } }`. Setting `"enabled": false` skips that agent even if tasks.md references it. Include a short example showing how to disable `docs-expert`.
  - **Verify**: Read the updated file — `agents` section exists with description, default, and example

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001–T003 | [x] |
