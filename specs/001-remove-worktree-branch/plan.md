# Plan: Remove Worktree and Branch Creation from SDD

**Spec**: [spec.md](./spec.md) | **Date**: 2026-03-26

## Approach

Delete all worktree/branch logic from the implement skill and update every file that references worktrees, branch creation, or the `"branch"` field in `state.json`. The implement skill will work directly in the current working directory; git push/PR will use `git branch --show-current` at runtime.

## Files

### Modify

| File | Change |
|------|--------|
| `skills/implement/SKILL.md` | Remove Step 2 (worktree+branch), strip worktree references from Context Recovery, remove spec-artifact copy step, update push/PR to use current branch, remove `Branch:` from summary |
| `skills/specify/SKILL.md` | Remove `"branch"` from `state.json` template (3 occurrences), remove `Branch:` from summary output |
| `CLAUDE.md` | Remove `"branch"` from `state.json` format example |
| `docs/PHILOSOPHY.md` | Remove "Worktree isolation" bullet and "Isolation by default" section |
| `docs/WORKFLOWS.md` | Remove worktree references from implement description, resume section, and status table |
