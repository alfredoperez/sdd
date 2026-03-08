# Tasks: {Feature Name}

**Plan**: [plan.md](./plan.md) | **Date**: {TODAY}

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [ ] **T001** {title} — `path/to/file`
  - **Do**: [Exact action — file path + what to write or change]
  - **Verify**: [build passes / UI shows X / type checks]

- [ ] **T002** {title} *(depends on T001)* — `path/to/file`
  - **Do**: [...]
  - **Verify**: [...]

- [ ] **T003** {title} *(depends on T002)* — `path/to/file`
  - **Do**: [...]
  - **Verify**: [...]

---

## Phase 2: Quality (Parallel — launch agents in single message)

- [ ] **T004** [P][A] Unit tests — `test-expert`
  - **Files**: `path/to/file.spec.ts`
  - **Pattern**: [test framework and patterns used in this project]
  - **Reference**: `path/to/existing.spec.ts`

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001–T003 | [ ] |
| Phase 2 | T004 | [ ] |
