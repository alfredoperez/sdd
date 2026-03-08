# Workflows

SDD has two paths through the pipeline, automatically selected based on change complexity.

## Full Path (Normal Mode)

For features that touch 2+ files, add new components/services, or introduce new public APIs.

```
/sdd:specify "add user authentication with OAuth2"
    ↓ creates spec.md, state.json
/sdd:plan 001-add-oauth2-auth
    ↓ creates plan.md (with review checkpoint)
/sdd:tasks 001-add-oauth2-auth
    ↓ creates tasks.md
/sdd:implement 001-add-oauth2-auth
    ↓ executes tasks, runs checkpoints, commits, opens PR
```

### What happens at each step

**Specify**: Explores the codebase, classifies complexity, writes a structured spec with requirements (R001, R002...) and scenarios (When/Then).

**Plan**: Reads the spec, designs the implementation approach, lists files to create/modify, identifies risks. Pauses for user review before proceeding.

**Tasks**: Reads spec + plan, generates a phased task list. Phase 1 is sequential core implementation. Phase 2 is parallel quality work (tests, docs).

**Implement**: Creates a worktree, executes tasks in order, runs 3 checkpoints (code review, test results, commit/PR review), then commits and opens a PR.

## Fast Path (Minimal Mode)

For small changes: 1 file, <10 lines, style/config tweaks.

```
/sdd:specify "fix button hover color"
    ↓ creates spec.md, plan.md, tasks.md, state.json (all in one step)
/sdd:implement 002-fix-button-hover
    ↓ executes tasks, runs checkpoints, commits, opens PR
```

### How it's detected

During `/sdd:specify`, after exploring the codebase, SDD classifies the change:

| Signal | Mode |
|--------|------|
| Touches 1 existing file, change is <10 lines | **minimal** |
| Pure style or config tweak | **minimal** |
| Touches 2+ files, or adds a new component/service | **normal** |
| Introduces new public behavior or API | **normal** |

When minimal mode is detected, specify generates all three artifacts (spec, plan, tasks) and skips the plan review checkpoint. You jump straight to implement.

### What's different in minimal mode

- Plan is a simplified single-table format (no Create/Modify sections)
- Tasks are a single Phase 1 with no Phase 2 (no separate test/docs tasks)
- Implementation skips Phase 2 subagents
- All 3 implement checkpoints (CP1, CP2, CP3) still run — no corners cut on review

## Resuming Work

If a session ends mid-workflow, SDD uses `state.json` to track progress:

```json
{ "step": "implement", "task": "T003", "branch": "001-my-feature", "updated": "2026-03-08" }
```

When you run `/sdd:implement 001-my-feature` again:
1. It reads `state.json` and sees you're mid-implementation at T003
2. It finds the existing worktree at `.claude/worktrees/001-my-feature/`
3. It reads `tasks.md` — tasks marked `[x]` are skipped
4. It resumes from the first unchecked task (T003)

No work is re-executed. Completed tasks are trusted.

## Checking Status

At any point, run `/sdd:status` to see all specs:

```
--- SDD Status ---

| # | Spec | Step | Branch | Updated |
|---|------|------|--------|---------|
| 001 | OAuth2 Auth | implement (T003) | 001-add-oauth2-auth | 2026-03-08 |
| 002 | Fix Button Hover | tasks | 002-fix-button-hover | 2026-03-08 |

Total: 2 specs
```
