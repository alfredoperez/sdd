# Tasks: {Feature Name}

<!-- Template variables: {Feature Name}, {TODAY}, {NNN}, {slug}, {NNN}-{slug} -->

**Plan**: [plan.md](./plan.md)

> Format reference: `[P]` markers and parallel groups — see `skills/tasks/SKILL.md` § Phase rules.

## Phase 1: Core Implementation

- [ ] **T001** {title} — `path/to/file` | R001
  - **Do**: [Exact action — file path + what to write or change]
  - **Verify**: [build passes / UI shows X / type checks]
  - **Leverage**: `path/to/similar-file.ts` ([what pattern to follow])

- [ ] **T002** [P] {title} *(depends on T001)* — `path/to/other-file` | R001, R002
  - **Do**: [...]
  - **Verify**: [...]

- [ ] **T003** [P] {title} *(depends on T001)* — `path/to/third-file` | R003
  - **Do**: [...]
  - **Verify**: [...]
  - **Leverage**: `path/to/existing-pattern.ts` ([what to reuse])

- [ ] **T004** {title} *(depends on T002, T003)* — `path/to/wire-up` | R004
  - **Do**: [...]
  - **Verify**: [...]
