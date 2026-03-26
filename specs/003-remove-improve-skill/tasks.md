# Tasks: Remove Improve Skill

## Phase 1 — Core

- [x] **T001** · Delete improve skill directory
  - **Do**: Remove `skills/improve/` directory entirely
  - **Verify**: `ls skills/improve` returns not found

- [x] **T002** · Remove improve references from docs
  - **Do**: Remove `/sdd:improve` lines from CLAUDE.md, README.md, CHANGELOG.md
  - **Verify**: `grep -ri improve` across repo returns no skill references
