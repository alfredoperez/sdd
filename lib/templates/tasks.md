# Tasks: {Feature Name}

<!-- Template variables: {Feature Name}, {TODAY}, {NNN}, {slug}, {NNN}-{slug} -->

**Plan**: [plan.md](./plan.md) | **Date**: {TODAY}

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [ ] **T001** {title} — `path/to/file` | R001
  - **Do**: [Exact action — file path + what to write or change]
  - **Verify**: [build passes / UI shows X / type checks]
  - **Leverage**: `path/to/similar-file.ts` ([what pattern to follow])

- [ ] **T002** {title} *(depends on T001)* — `path/to/file` | R001, R002
  - **Do**: [...]
  - **Verify**: [...]

- [ ] **T003** {title} *(depends on T002)* — `path/to/file` | R003
  - **Do**: [...]
  - **Verify**: [...]
  - **Leverage**: `path/to/existing-pattern.ts` ([what to reuse])

---

## Phase 2: Quality (Parallel — launch agents in single message)

> The name in backticks after `—` is the **agent identifier** that `/sdd:implement` uses to spawn the subagent.
> Use any installed agent name (e.g., `test-expert`, `docs-expert`, `security-expert`).

- [ ] **T004** [P][A] Unit tests — `test-expert` | R001, R002, R003
  - **Files**: `path/to/file.spec.ts`
  - **Pattern**: [test framework and patterns used in this project]
  - **Reference**: `path/to/existing.spec.ts`

- [ ] **T005** [P][A] Update usage docs — `docs-expert`
  - **Files**: `docs/usage.md`
  - **Do**: Add section documenting the new feature
  - **Verify**: Docs build passes, new section is accurate

---

## Progress

- Phase 1: T001–T003 [ ]
- Phase 2: T004–T005 [ ]
