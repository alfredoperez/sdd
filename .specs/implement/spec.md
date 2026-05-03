# Implement Specification

**Domain:** `implement` · **Last updated:** 2026-05-03

> Living spec for the `/sdd:implement` skill.

## Purpose

`/sdd:implement` executes Phase 1 tasks from `tasks.md`, runs hooks, walks the three checkpoints (Code Review → Test Results → Commit Review), syncs Layer 1 from any delta blocks in `spec.md`, and ships the change as a commit + PR.

## Capabilities

- Spec lookup, parallel load of `tasks.md` + `spec.md` + `plan.md` + `.spec-context.json`
- Resume detection via `progress` marker (`phase1` / `hooks` / `code-review` / `test-results` / `commit-review` / `commit`)
- Optional branch creation via `branchStage = "implement"`
- Phase 1 task execution: solo and parallel-group (`[P]` runs)
- Atomic per-task `.spec-context.json` updates (`task_summaries.{Tn}`, `files_modified`, `decisions`, `concerns`, `last_action`, transition append)
- `pre:implement`, `post:task`, `pre:checkpoint:code-review`, `pre:checkpoint:test-results`, `pre:checkpoint:commit-review`, `pre:commit`, `post:pr` hooks
- CP1 Code Review (file diff vs plan, concerns, scenario verification)
- CP2 Test Results (only shown if user ran tests)
- CP3 Commit + PR preview
- Step 7b — Layer 2 → Layer 1 delta sync (ADDED / MODIFIED / REMOVED / RENAMED) into every `.specs/<domain>/spec.md` named in `loadedDomains`
- Step 8 — explicit `git add`, conventional commit, push, `gh pr create`, main-branch push guard
- Step 8b — finalize `.spec-context.json` with `prUrl`, `prNumber`, `last_action`; ship in second commit on the same branch

## Requirements

### R001: Resume from any in-flight progress marker

The skill MUST read `progress` from `.spec-context.json` and skip phases already marked complete (`hooks` skips Phase 1, `code-review` skips through to CP1, etc.). On resume, plan.md re-reads are skipped when `step_summaries.plan` and `approach` are present.

### R002: Execute solo and parallel-group tasks correctly

Solo tasks (no `[P]` prefix) run one at a time. A run of consecutive `[P]` tasks forms a parallel group spawned as concurrent subagents in a single message. Subagents NEVER edit `.spec-context.json` or `tasks.md` — the main thread owns those writes after the group returns.

### R003: Update `.spec-context.json` atomically per task

After each solo task (or per parallel group), a single Write call MUST update `currentTask`, append to `task_summaries.{Tn}`, merge `files_modified`, append `decisions` / `concerns`, set `last_action`, and append a `transitions[]` entry. Existing fields are preserved (read-then-merge).

### R004: Run hooks at the canonical hook points

`pre:implement` (first pass only), `post:task` (per task), `pre:checkpoint:code-review` (alias `pre:code-review`), `pre:checkpoint:test-results`, `pre:checkpoint:commit-review`, `pre:commit`, `post:pr` MUST fire per `hook-execution.md` with the documented `vars`.

### R005: Sync Layer 1 at CP3 closure

Step 7b MUST parse `specs/{NNN}-{slug}/spec.md` for delta blocks and apply ADDED / MODIFIED / REMOVED / RENAMED operations against every `.specs/<domain>/spec.md` named in `loadedDomains`. Synced files are staged into the same commit as the implementation. `syncedDomains` is appended (deduplicated). No-op when `loadedDomains` is empty or no delta blocks exist.

### R006: Block pushes from `main`/`master` when `branchStage` is set

Before `git push`, the main-branch push guard MUST halt with the documented refusal message when `.sdd.json#branchStage` is `"specify"` or `"implement"` and the current branch is `main`/`master`. Manual mode trusts the user.

### R007: Commit + PR follow conventional commits with no AI attribution

Conventional commit format (`{type}({scope}): {description}`), imperative lowercase ≤72 chars, `Closes #N` only when an issue exists, NO `Co-Authored-By` or "Generated with…" lines, ever.

### R008: Ship a finalize commit with `prUrl` after PR opens

Step 8b MUST update `.spec-context.json` with `prUrl`, `prNumber`, and a final `last_action`, then commit + push that single file under `chore(specs): mark {NNN} shipped — PR #{N}`. Skipped if `gh pr create` failed.

## Out of scope

- Spec / plan / task generation (earlier pipeline steps).
- Phase 2 enrichment via `agents` config (deprecated; superseded by `hooks`).

## Related

- ADRs: [`.sdd/decisions/0001-layered-context-loading.md`](../../.sdd/decisions/0001-layered-context-loading.md)
- Skill: [`skills/implement/SKILL.md`](../../skills/implement/SKILL.md)
- Shared instructions: [`lib/instructions/`](../../lib/instructions/) — transition-logging, hook-execution, branch-creation, layered-context
