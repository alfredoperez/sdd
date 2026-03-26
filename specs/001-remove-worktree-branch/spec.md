# Spec: Remove Worktree and Branch Creation from SDD

**Slug**: 001-remove-worktree-branch | **Date**: 2026-03-26

## Summary

Remove all git worktree creation (`EnterWorktree`/`ExitWorktree`) and branch creation/management logic from the SDD implement skill. Implementation should run directly in the current working directory on whatever branch the user is already on, leaving git workflow decisions to the user.

## Requirements

- **R001** (MUST): Remove `EnterWorktree`/`ExitWorktree` usage and all worktree setup/fallback logic from `skills/implement/SKILL.md`
- **R002** (MUST): Remove branch creation, renaming (`git branch -m`), and verification steps from `skills/implement/SKILL.md`
- **R003** (MUST): Remove the spec-artifact copy step (`cp -r ... specs/`) that was only needed for worktree isolation
- **R004** (MUST): Remove `"branch"` field from `state.json` schema in all files that define or reference it (`CLAUDE.md`, `skills/specify/SKILL.md`, `skills/implement/SKILL.md`)
- **R005** (MUST): Update `git push` / `gh pr create` step to use current branch instead of a worktree-derived branch name
- **R006** (SHOULD): Update docs (`PHILOSOPHY.md`, `WORKFLOWS.md`) to remove worktree/branch references
- **R007** (SHOULD): Update the implement summary output to remove the `Branch:` line

## Scenarios

### Normal Implementation

**When** user runs `/sdd:implement {slug}`
**Then** all tasks execute in the current working directory with no worktree or branch creation

### Resume Mid-Implementation

**When** `state.json` has `step = "implement"` and `task = "T00N"`
**Then** implementation resumes in the current directory without checking for worktrees

### Push and PR

**When** all tasks are complete and push/PR step runs
**Then** it pushes the current branch (from `git branch --show-current`) without assuming a specific branch name

## Out of Scope

- Providing an alternative isolation mechanism
- Changing the specify/plan/tasks workflow steps
- Modifying commit conventions or PR template content
