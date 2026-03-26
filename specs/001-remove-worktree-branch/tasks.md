# Tasks: Remove Worktree and Branch Creation from SDD

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-26

## Format

- `[P]` = Can run in parallel  |  `[A]` = Agent-eligible

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Remove worktree + branch from implement skill — `skills/implement/SKILL.md`
  - **Do**: Delete entire "Step 2. Create Worktree + Branch" section (lines 48–97). In "Context Recovery" section, remove worktree checks (lines 38–40) and simplify to: read spec.md, read tasks.md, resume from first unchecked task. Remove the spec-artifact copy step. Update Step 8 push command to use `$(git branch --show-current)` instead of `{branch-name}`. Remove `Branch:` line from Step 9 summary.
  - **Verify**: `grep -c "worktree\|EnterWorktree\|ExitWorktree\|branch -m" skills/implement/SKILL.md` returns 0

- [x] **T002** Remove `"branch"` from state.json in implement skill *(depends on T001)* — `skills/implement/SKILL.md`
  - **Do**: In Step 1 Load section, remove `"branch"` field from the `state.json` template (line 29 area)
  - **Verify**: `grep -c '"branch"' skills/implement/SKILL.md` returns 0

- [x] **T003** Remove `"branch"` from specify skill — `skills/specify/SKILL.md`
  - **Do**: Remove `"branch": "{NNN}-{slug}"` from all 3 `state.json` templates (Steps 2, 6, 7). Remove `Branch: {NNN}-{slug}` from both summary output formats (minimal and normal mode).
  - **Verify**: `grep -c '"branch"\|Branch:' skills/specify/SKILL.md` returns 0

- [x] **T004** Remove `"branch"` from CLAUDE.md — `CLAUDE.md`
  - **Do**: Remove the `"branch": "{NNN}-{slug}",` line from the state.json format example
  - **Verify**: `grep -c '"branch"' CLAUDE.md` returns 0

- [x] **T005** Update docs — `docs/PHILOSOPHY.md`, `docs/WORKFLOWS.md`
  - **Do**: In `PHILOSOPHY.md`: remove the "Worktree isolation" bullet (line 24) and the entire "5. Isolation by default" section (lines 46–47). In `WORKFLOWS.md`: change implement description (line 28) to remove "Creates a worktree,". In resume section, remove worktree line (line 71) and simplify. Remove `Branch` column from status table (lines 84–87).
  - **Verify**: `grep -c "worktree\|Worktree" docs/PHILOSOPHY.md docs/WORKFLOWS.md` returns 0

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001–T005 | [x] |
