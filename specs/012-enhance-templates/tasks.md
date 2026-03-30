# Tasks: Enhance Templates

<!-- Template variables: {Feature Name}, {TODAY}, {NNN}, {slug}, {NNN}-{slug} -->

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-29

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Add NFR section and MAY priority to spec-normal — `lib/templates/spec-normal.md` | R001, R002
  - **Do**: Add `R004 (MAY)` example to Requirements section. Add Non-Functional Requirements section between Scenarios and Out of Scope with NFR001/NFR002/NFR003 examples, category hints comment (Performance, Security, Reliability, Accessibility, Observability), and "omit if no NFRs apply" guidance comment
  - **Verify**: Template is valid markdown; NFR section appears after Scenarios, before Out of Scope

- [x] **T002** Add Architecture, Testing Strategy, convert tables to lists in plan — `lib/templates/plan.md` | R003, R004, R005
  - **Do**: Rename `## Flow` to `## Architecture`, change threshold comment from "4+ files" to "3+ components or non-obvious data flow". Convert Files Create/Modify from tables to `- path -- description` lists. Convert Data Model from table to `- Entity -- fields -- notes` list. Add `## Testing Strategy` section after Data Model with Unit/Integration/Edge cases bullet structure and "omit for trivial changes" comment
  - **Verify**: No tables remain in template; Architecture and Testing Strategy sections present

- [x] **T003** Add requirement refs, Leverage field, convert Progress to list in tasks — `lib/templates/tasks.md` | R006, R007, R008
  - **Do**: Add `| R001` requirement refs after file path on Phase 1 task headers (T001, T002, T003). Add optional `**Leverage**: path/to/similar-file ([what pattern to follow])` field to T001 and T003. Add `| R001, R002, R003` refs to Phase 2 T004 header. Convert Progress table to `- Phase 1: T001-T003 [ ]` list format
  - **Verify**: Each task header has requirement refs; Leverage field present on T001/T003; Progress is a list not a table

- [x] **T004** Update template README — `lib/templates/README.md` | R009
  - **Do**: Document new sections added (Non-Functional Requirements in spec-normal, Testing Strategy in plan, Leverage in tasks), renamed sections (Flow → Architecture in plan), and formatting changes (tables → lists in plan and tasks)
  - **Verify**: README accurately reflects all template changes from T001-T003

---

## Phase 2: Quality (Parallel — launch agents in single message)

> The name in backticks after `—` is the **agent identifier** that `/sdd:implement` uses to spawn the subagent.

- [ ] **T005** [P][A] Unit tests — `test-expert` | R001-R009
  - **Files**: `lib/templates/spec-normal.md`, `lib/templates/plan.md`, `lib/templates/tasks.md`
  - **Pattern**: Verify template content matches spec requirements — check for NFR section, Architecture heading, Testing Strategy, Leverage field, requirement refs, list formatting
  - **Reference**: Current templates as baseline

---

## Progress

- Phase 1: T001-T004 [ ]
- Phase 2: T005 [ ]
