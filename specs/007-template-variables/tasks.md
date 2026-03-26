# Tasks: Standardize Template Variables

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-26

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Documentation (Sequential)

- [x] **T001** Create template variable reference — `lib/templates/README.md`
  - **Do**: Create `lib/templates/README.md` documenting the canonical variable set (`{Feature Name}`, `{TODAY}`, `{NNN}`, `{slug}`, `{NNN}-{slug}`) with a description of each variable, its format, and which templates use it. Include a section on authoring new templates.
  - **Verify**: File exists and lists all 5 canonical variables with descriptions

---

## Phase 2: Normalize Templates (Parallel — all independent)

- [x] **T002** [P][A] Add variable header to spec-normal template — `lib/templates/spec-normal.md`
  - **Do**: Add an HTML comment block at the top of the file listing all canonical variables: `{Feature Name}`, `{TODAY}`, `{NNN}`, `{slug}`, `{NNN}-{slug}`. Audit existing placeholders and ensure they match the canonical set exactly (no deviations like `{feature-name}` or `{date}`).
  - **Verify**: Comment header present; all placeholders in file body match canonical names

- [x] **T003** [P][A] Add variable header to spec-minimal template — `lib/templates/spec-minimal.md`
  - **Do**: Add the same HTML comment block at the top listing canonical variables. Audit existing placeholders and normalize any that deviate from the canonical set.
  - **Verify**: Comment header present; all placeholders in file body match canonical names

- [x] **T004** [P][A] Add variable header to plan template — `lib/templates/plan.md`
  - **Do**: Add the same HTML comment block at the top listing canonical variables. Audit existing placeholders and normalize any that deviate from the canonical set.
  - **Verify**: Comment header present; all placeholders in file body match canonical names

- [x] **T005** [P][A] Add variable header to tasks template — `lib/templates/tasks.md`
  - **Do**: Add the same HTML comment block at the top listing canonical variables. Audit existing placeholders and normalize any that deviate from the canonical set.
  - **Verify**: Comment header present; all placeholders in file body match canonical names

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001 | [x] |
| Phase 2 | T002–T005 | [x] |
