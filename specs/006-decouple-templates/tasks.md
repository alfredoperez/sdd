# Tasks: Decouple Templates from Skills

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-26

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Sync spec-normal template drift — `lib/templates/spec-normal.md`
  - **Do**: In `lib/templates/spec-normal.md`, change `**Branch**:` to `**Slug**:` to match the inline template in `skills/specify/SKILL.md` Step 5. The file template says `**Branch**: {NNN}-{slug}` but the skill inline says `**Slug**: {NNN}-{slug}`. Use `**Slug**:` as the correct version.
  - **Verify**: `lib/templates/spec-normal.md` header line reads `**Slug**: {NNN}-{slug} | **Date**: {TODAY}`

- [x] **T002** Sync spec-minimal template drift *(depends on T001)* — `lib/templates/spec-minimal.md`
  - **Do**: In `lib/templates/spec-minimal.md`, change `**Branch**:` to `**Slug**:` and add `**Mode**: Minimal` to match the inline minimal spec pattern. Header should read `**Slug**: {NNN}-{slug} | **Mode**: Minimal | **Date**: {TODAY}`.
  - **Verify**: `lib/templates/spec-minimal.md` header line reads `**Slug**: {NNN}-{slug} | **Mode**: Minimal | **Date**: {TODAY}`

- [x] **T003** Replace inline spec template in specify skill *(depends on T002)* — `skills/specify/SKILL.md`
  - **Do**: In Step 5, replace the entire inline markdown code block (the spec template from ` ```markdown ` to ` ``` `) with an instruction: "Read `lib/templates/spec-normal.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), and write the result to `specs/{NNN}-{slug}/spec.md`." Keep the `**Skip**:` line after it.
  - **Verify**: Step 5 contains no inline markdown template block, only a reference to `lib/templates/spec-normal.md`

- [x] **T004** Replace inline plan template in specify minimal mode *(depends on T003)* — `skills/specify/SKILL.md`
  - **Do**: In Step 6 (Minimal Mode), replace the inline plan markdown code block with: "Read `lib/templates/plan.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), simplify optional sections (omit Technical Context, Flow, Data Model, Risks — keep only Approach and a `## Files to Change` list), and write to `specs/{NNN}-{slug}/plan.md`."
  - **Verify**: Step 6 has no inline plan template block, references `lib/templates/plan.md`

- [x] **T005** Replace inline tasks template in specify minimal mode *(depends on T004)* — `skills/specify/SKILL.md`
  - **Do**: In Step 6 (Minimal Mode), replace the inline tasks markdown code block with: "Read `lib/templates/tasks.md`, fill placeholders (`{Feature Name}`, `{TODAY}`), keep only Phase 1 with the relevant tasks (omit Phase 2 for minimal changes), and write to `specs/{NNN}-{slug}/tasks.md`."
  - **Verify**: Step 6 has no inline tasks template block, references `lib/templates/tasks.md`

- [x] **T006** Replace inline plan template in plan skill *(depends on T005)* — `skills/plan/SKILL.md`
  - **Do**: In Step 2, replace the entire inline markdown code block (the plan template) with: "Read `lib/templates/plan.md`, fill placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`), include or omit optional sections (Technical Context, Flow, Data Model, Risks) based on feature complexity, and write to `specs/{NNN}-{slug}/plan.md`." Keep the `**Skip**:` and `**Optional**:` lines after it.
  - **Verify**: Step 2 contains no inline markdown template block, only a reference to `lib/templates/plan.md`

- [x] **T007** Replace inline tasks template in tasks skill *(depends on T006)* — `skills/tasks/SKILL.md`
  - **Do**: In Step 2, replace the entire inline markdown code block (the tasks template) with: "Read `lib/templates/tasks.md`, fill placeholders (`{Feature Name}`, `{TODAY}`), generate tasks based on the plan's file list, and write to `specs/{NNN}-{slug}/tasks.md`." Keep the `**Phase rules**:` and `**Skip**:` lines after it.
  - **Verify**: Step 2 contains no inline markdown template block, only a reference to `lib/templates/tasks.md`

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001-T007 | [x] |
