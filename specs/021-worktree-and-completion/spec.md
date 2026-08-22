# Spec: Worktree Mode and Pre-Commit Completion

**Slug**: 021-worktree-and-completion | **Date**: 2026-05-09

## Summary

Extend SDD's branch-creation pipeline with an opt-in worktree mode (so users can run `/sdd:implement` in an isolated `git worktree` instead of switching the main checkout) and reorder the implement-time ship sequence so `status: "completed"` is written **before** the implementation commit — landing completion state in the same commit as the code, rather than a follow-up `chore(specs): mark NNN shipped` commit. The existing `branchStage` field (`"specify"` / `"implement"` / `"manual"`) is preserved as-is; the new behavior layers on top.

## Modified Capabilities

- **specify** — see `.specs/specify/spec.md` (branch creation at specify-time may now produce a worktree)
- **implement** — see `.specs/implement/spec.md` (branch creation at implement-time may now produce a worktree; ship sequence reorders status write)
- **state-tracking** — see `.specs/state-tracking/spec.md` (new `worktreePath` field; existing `status` field set earlier in the pipeline)

## Requirements

- **R001** (MUST): `.sdd.json` accepts a new `branchMode` field with values `"branch"` (default — current behavior) and `"worktree"`. When `branchMode: "worktree"` and `branchStage` is `"specify"` or `"implement"`, `lib/instructions/branch-creation.md` MUST run `git worktree add <path> -b {branch}` (or `git worktree add <path> {branch}` if the branch already exists) instead of `git checkout -b`. When `branchMode` is absent or `"branch"`, behavior is unchanged.
- **R002** (MUST): The worktree path is resolved from a new `worktreePathFormat` field in `.sdd.json`, defaulting to `"../{repo}-{branch}"` where `{repo}` is the basename of the current git toplevel and `{branch}` is the resolved branch name. Variables `{NNN}`, `{slug}`, `{branch}`, `{repo}` MUST be supported.
- **R003** (MUST): When a worktree is created, `.spec-context.json` MUST record `workingBranch: "{branch}"` AND a new `worktreePath: "<absolute path>"` field. When `branchMode` is `"branch"` (or absent), `worktreePath` MUST be `null` / unset. The state-tracking schema (`docs/STATE.md` + `lib/schemas/spec-context.schema.json`) MUST document the new field per the Docs Sync Rule.
- **R004** (MUST): Worktree creation MUST follow the same decision table as branch creation (skip if dirty tree, skip if already on a non-main branch, skip with warning if `git worktree add` fails). On worktree-add success the skill prints `✓ Created worktree at <path> on branch <branch>` and continues — it does NOT automatically `cd` into the worktree (the user manages where their next command runs). The skill prints a follow-up hint: `→ cd <path> && /sdd:resume {NNN}-{slug}`.
- **R005** (MUST): `/sdd:implement` Step 8 MUST set `status: "completed"`, `currentStep: "done"`, `next: "done"`, and `checkpointStatus.commit: true` **before** the `git commit` that ships the implementation, so the completed-state lands in the impl commit. The existing pre-commit hook order (run hooks → stage → commit) MUST be preserved; the state write happens before hooks fire.
- **R006** (MUST): `/sdd:implement` Step 8b MUST still write `prUrl`, `prNumber`, and final `last_action` after `gh pr create` succeeds, and MUST still ship them in a finalize commit (`chore(specs): mark {NNN} shipped — PR #{N}`). Step 8b MUST NOT re-set `status` — `status` is already `"completed"` from Step 8. If `gh pr create` fails, Step 8b is skipped (unchanged).
- **R007** (SHOULD): The main-branch push guard in `branch-creation.md` MUST also halt when `branchMode: "worktree"` is configured but the current working directory is the original repo root (not the worktree) — i.e., catches the user who set `branchMode: "worktree"` but tried to push without `cd`-ing into the worktree first.

## Scenarios

### Worktree creation at implement-time

**When** a user has `.sdd.json` with `branchStage: "implement"` and `branchMode: "worktree"`, and runs `/sdd:implement {NNN}-{slug}` from `main`
**Then** SDD runs `git worktree add ../{repo}-{branch} -b {branch}`, records `workingBranch` + `worktreePath` in `.spec-context.json`, prints the `✓ Created worktree…` line + `→ cd …` hint, and **stops** so the user can `cd` into the worktree before resuming. (No automatic step continuation — worktree creation is a deliberate context switch.)

### Default behavior unchanged

**When** a user has `.sdd.json` with `branchStage: "implement"` and no `branchMode` set (or `branchMode: "branch"`), and runs `/sdd:implement`
**Then** SDD runs `git checkout -b {branch}` exactly as today and continues into Phase 1 without pause. `worktreePath` stays `null`.

### Pre-commit completion lands in same commit

**When** a user runs `/sdd:implement` and reaches Step 8 with all CPs approved
**Then** SDD updates `.spec-context.json` to `{ status: "completed", currentStep: "done", next: "done", checkpointStatus: { commit: true } }`, runs `pre:commit` hooks, stages files (including the now-completed `.spec-context.json`), and commits. The single implementation commit contains both the code and the completed-state. Step 8b adds only the `prUrl`/`prNumber` finalize commit afterward.

### Worktree push from wrong directory

**When** a user has `branchMode: "worktree"` set, ran the worktree creation, but then runs `/sdd:implement` again from the original repo root (not the worktree) and reaches the push step
**Then** the main-branch push guard halts with: `🛑 branchMode=worktree but you are on {current} in {cwd} — cd into the worktree at {worktreePath} before pushing.`

## Non-Functional Requirements

- **NFR001** (MUST): Backward compatibility — existing specs that pre-date this change MUST continue to ship without modification. Specs created without `worktreePath` in `.spec-context.json` are treated as `branchMode: "branch"`. The Step 8 reorder is unconditional; specs already past Step 8 (i.e., resumed mid-Step-8b) MUST detect `status: "completed"` is already set and skip the new pre-commit write.

## Out of Scope

- Auto-detection of which Claude harness tool to invoke (`EnterWorktree` vs raw `git worktree add`). The shared instruction uses raw `git worktree add` shell commands so the skill is portable across Claude Code, Claude API, and any other agent runtime. Harness-specific worktree tooling can wrap this behavior externally (e.g., via the existing hook system) without the skill knowing.
- Worktree cleanup after merge (`git worktree remove`). Out of scope for this spec — users manage their own worktrees. A future spec could add a `post:pr` hook recipe.
- Migration of existing in-flight specs from `branchMode: "branch"` to `branchMode: "worktree"` mid-pipeline. Switching mode mid-spec is undefined behavior — the spec finishes in whichever mode it started.
- Removing the Step 8b finalize commit entirely (one-commit-only ship). The two-commit pattern is preserved because `prUrl` is unknowable until after `gh pr create` returns; collapsing to one commit would require either dropping `prUrl` from git or an `--amend` after push. Either is out of scope here.
- New hook points (`pre:branch-create`, `post:worktree-add`, etc.). The existing `pre:implement` / `pre:commit` hooks already cover the timing the user asked about.

## Open Questions

- **OQ001** (decision needed at `/sdd:plan`): Should `worktreePathFormat` default to `"../{repo}-{branch}"` (sibling), `"../worktrees/{branch}"` (sibling subdir for tidiness), or `".worktrees/{branch}"` (in-repo, gitignored)? R002 currently picks sibling; plan should confirm.
- **OQ002** (decision needed at `/sdd:plan`): When worktree mode is on at implement-time and the user runs `/sdd:implement` from the original repo root, should the skill (a) create the worktree and stop, or (b) create the worktree and attempt to continue Phase 1 inside it? R004 currently picks (a) — explicit user `cd` — because no skill-runtime `cd` mechanism is reliable across Claude harnesses. Plan should validate.
