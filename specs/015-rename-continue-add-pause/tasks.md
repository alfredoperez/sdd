# Tasks: Rename Continue to Resume & Add Pause

**Plan**: [plan.md](./plan.md) | **Date**: 2026-04-02

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Create resume skill — `skills/resume/SKILL.md` | R001, R004
  - **Do**: Copy `skills/continue/SKILL.md` to `skills/resume/SKILL.md`. Rename skill from `sdd:continue` to `sdd:resume`. Add a paused-check gate in Step 2: before determining next step, check if `paused` is `true` in `.spec-context.json`; if so, clear the flag (set `paused: false`) and log "Resumed {NNN}-{slug}" before advancing.
  - **Verify**: `skills/resume/SKILL.md` exists with correct name, description, and paused-check logic
  - **Leverage**: `skills/continue/SKILL.md` (base structure to copy)

- [x] **T002** Create pause skill *(depends on T001)* — `skills/pause/SKILL.md` | R003
  - **Do**: Create `skills/pause/SKILL.md` with frontmatter `name: sdd:pause`. Skill accepts `$ARGUMENTS` as spec slug (or finds most recent spec). Reads `.spec-context.json`, sets `"paused": true`, writes it back, and displays: "⏸ Paused {NNN}-{slug}". If already paused, display: "Already paused."
  - **Verify**: `skills/pause/SKILL.md` exists with correct structure

- [x] **T003** Delete old continue skill *(depends on T001)* — `skills/continue/SKILL.md` | R001
  - **Do**: Delete `skills/continue/SKILL.md` and the `skills/continue/` directory
  - **Verify**: `skills/continue/` no longer exists

- [x] **T004** Update CLAUDE.md references *(depends on T001)* — `CLAUDE.md` | R002
  - **Do**: Replace all `/sdd:continue` with `/sdd:resume`. Add `/sdd:pause {NNN}-{slug}` to the Utilities section. Update any workflow descriptions mentioning continue.
  - **Verify**: No remaining `/sdd:continue` references in `CLAUDE.md`

- [x] **T005** Update auto skill *(depends on T001)* — `skills/auto/SKILL.md` | R002, R006
  - **Do**: Replace `/sdd:continue` with `/sdd:resume` in the auto-advance loop. Add check: if spec is `paused: true`, stop auto-advance and display: "⏸ Spec is paused. Run `/sdd:resume` to continue."
  - **Verify**: No remaining `/sdd:continue` references in `skills/auto/SKILL.md`

- [x] **T006** Update status skill *(depends on T002)* — `skills/status/SKILL.md` | R005
  - **Do**: Add paused indicator to dashboard display — when a spec has `paused: true`, show "⏸ paused" alongside the spec's current step
  - **Verify**: Status output includes paused indicator for paused specs

- [x] **T007** Update specify skill references *(depends on T001)* — `skills/specify/SKILL.md` | R002
  - **Do**: Replace any `/sdd:continue` references with `/sdd:resume` in summary output text
  - **Verify**: No remaining `/sdd:continue` references in `skills/specify/SKILL.md`

---

## Progress

- Phase 1: T001–T007 [x]
