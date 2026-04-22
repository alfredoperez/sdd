---
name: sdd:implement
description: "SDD — Spec-Driven Development: execute tasks, run checkpoints, commit and open PR."
---

## Shared Instructions

- [Transition Logging](../../lib/instructions/transition-logging.md) — append a transition entry on every `.spec-context.json` write
- [Hook Execution](../../lib/instructions/hook-execution.md) — run user-configured hooks at supported pipeline points
- [Branch Creation](../../lib/instructions/branch-creation.md) — optional feature-branch creation driven by `.sdd.json` `branchStage`

## Steps

### 1. Load

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains `tasks.md`.

Read in parallel:

- `specs/{NNN}-{slug}/tasks.md` — all Phase 1 tasks
- `specs/{NNN}-{slug}/spec.md` — feature name, requirements, scenarios (for CP1 verification)
- `specs/{NNN}-{slug}/plan.md` — approach, files, issue number if present
- `specs/{NNN}-{slug}/.spec-context.json` — current step/task (if exists; note if resuming mid-implement)

Determine commit scope from the primary directory being modified (e.g., `toolbar`, `ui`, `core`). If unclear, omit scope.

Determine issue number from plan.md or spec.md if present.

If no tasks found, stop: "Run `/sdd:specify`, `/sdd:plan`, and `/sdd:tasks` first."

Update `specs/{NNN}-{slug}/.spec-context.json` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md):

```json
{ "currentStep": "implement", "currentTask": "T001", "progress": "phase1", "next": "implement", "updated": "{TODAY}" }
```

---

### 1b. Optional Branch Creation

**Skip this step on resume** — if `.spec-context.json` already showed `currentStep = "implement"` on entry, branch creation has already run (or been skipped) on the first pass.

Follow [branch-creation](../../lib/instructions/branch-creation.md) with `stage="implement"`. It is a no-op unless `.sdd.json` has `branchStage: "implement"`.

Run `pre:implement` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir, files: <empty string — no files modified yet> }`.

---

### Context Recovery (if resuming)

If `.spec-context.json` shows `currentStep = "implement"`:

1. Read `.spec-context.json` fully — extract `approach`, `last_action`, `task_summaries`, `concerns`, `decisions`, `files_modified`, and `step_summaries` if present
2. Use these fields to reconstruct context efficiently:
   - `approach` tells you the implementation strategy without re-reading plan.md
   - `last_action` tells you what just happened before context was lost
   - `task_summaries` for completed tasks tells you what each task did, what files it touched, and any concerns — without re-deriving from code
   - `step_summaries.plan` (if present) provides the planned approach, file count, and risks — skip re-reading plan.md
   - `concerns` and `decisions` carry forward flagged issues and key choices
3. Read `tasks.md` — `[x]` = done, `[ ]` = remaining (still needed for remaining task definitions)
4. Read `spec.md` for scenarios (needed at CP1 for verification). If `step_summaries.specify` exists in .spec-context.json, you can skip re-reading spec.md for feature context (use the key_finding instead) — but still read it for CP1 scenario verification.
5. Skip re-reading `plan.md` if `step_summaries.plan` and `approach` exist in .spec-context.json — these provide sufficient context
6. Read `progress` from `.spec-context.json` and use it to skip completed phases:

| `progress` value | Resume point |
|-----------------|-------------|
| `phase1` | Resume from first unchecked task in Phase 1 |
| `hooks` | Skip Phase 1, resume at hooks execution |
| `code-review` | Skip Phase 1 + hooks, resume at CP1 — Code Review |
| `test-results` | Skip through CP1, resume at CP2 — Test Results |
| `commit-review` | Skip through CP2, resume at CP3 — Commit Review |
| `commit` | Skip through CP3, resume at Step 8 (stage + commit) |
| `null` or missing | Fall back to task-based recovery: resume from first unchecked task |

4. Do NOT re-run completed phases — trust the progress marker and existing checkmarks

---

### 2. Phase 1 — Core Implementation

Walk Phase 1 tasks in order. Tasks group into two execution shapes:

- **Solo task** — any task that does not start with `[P]`. Execute it by itself.
- **Parallel group** — a run of consecutive `[P]` tasks. Execute them as a batch of concurrent subagents.

#### 2a. Solo task execution

For each solo task:

1. Perform the work described in the **Do** field.
2. Run the **Verify** check.
3. Mark complete in `specs/{NNN}-{slug}/tasks.md`: `- [ ]` → `- [x]`.
4. Update `specs/{NNN}-{slug}/.spec-context.json` atomically (single Write call) with all of the following (also append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md)):
   - Set `currentTask` to the next task ID (or `null` after the last task).
   - Write `task_summaries.{taskId}` with:
     - `status`: `"DONE"` or `"DONE_WITH_CONCERNS"` (use DONE_WITH_CONCERNS if any silent fixes, type workarounds, or edge cases were noted).
     - `did`: one-line summary of what was actually done.
     - `files`: array of file paths actually modified by this task.
     - `concerns`: array of concern strings (empty `[]` if none).
   - Update top-level `files_modified` array — deduplicated union of all files modified across all completed tasks.
   - Append to `decisions[]` if a non-trivial decision was made during this task.
   - Append to `concerns[]` array with `{ "task": "{taskId}", "note": "description" }` for any concerns.
   - Set `last_action` to a short description of what just completed.
   - Preserve all existing fields (`currentStep`, `progress`, `approach`, `step_summaries`, previous `task_summaries`, etc.).
5. Run `post:task` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir, files: <space-separated files from task_summaries.{taskId}.files> }` before proceeding.

#### 2b. Parallel group execution

When you reach a run of consecutive `[P]` tasks:

1. Collect the full run (stop at the first non-`[P]` task or end-of-phase). That run is the parallel group.
2. For each task in the group, build a subagent prompt from its **Do**, **Verify**, and (if present) **Files** / **Leverage** fields. State explicitly that the subagent must only do the described work and return a short report — it must **not** edit `.spec-context.json` or tick checkboxes in `tasks.md`. The main thread owns those writes to avoid races.
3. **In a single message**, spawn one `Agent` call per task (`subagent_type: "general-purpose"`). Do not spawn them one at a time.
4. When every subagent has returned:
   - For each task in order: tick `- [ ]` → `- [x]` in `tasks.md`.
   - Write one atomic `.spec-context.json` update that contains every task's `task_summaries.{Tn}` entry (each with `status`, `did`, `files`, `concerns`), merges all modified files into `files_modified`, appends any new `decisions` / `concerns`, sets `currentTask` to the task after the group (or `null`), sets `last_action` to a one-line group summary (e.g., "T004–T006 complete — updated three independent call sites in parallel"), and appends a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).
   - Run `post:task` hooks **once per task in the group**, sequentially, each with that task's own `files` in `vars`.
5. If any subagent fails or reports a concern, record that task as `DONE_WITH_CONCERNS` (or stop per the Deviation rules below). Partial success is fine — the main thread still ticks only the tasks that completed successfully.

**Resume note:** if execution is interrupted mid-group, none of the group's checkboxes will be ticked (the main thread only ticks after the whole group returns). On resume, `progress: "phase1"` will land on the group's first task and the group will re-run in full. Task work should be idempotent where possible.

**Deviation rules:**

| Situation                              | Action                                            |
| -------------------------------------- | ------------------------------------------------- |
| Bug, import error, or type mismatch    | Fix silently — note for CP1                       |
| Missing dependency                     | Fix silently — note for CP1                       |
| Architectural approach needs to change | **STOP. Explain to user and ask how to proceed.** |
| Task is impossible as written          | **STOP. Explain why and ask how to proceed.**     |

After the last Phase 1 task, check if a build command is configured in `.sdd.json`. If so, start the build in background. Otherwise, check if common build commands exist (e.g., `package.json` scripts) and run the appropriate one.

---

### 4. Phase 2 — Hooks

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `"hooks"` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).

Read `.sdd.json` from the project root (if it exists):

1. If `.sdd.json` has no `hooks` key but has an `agents` key, log: `⚠ "agents" config is deprecated — migrate to "hooks". See docs/CONFIGURATION.md` and skip to CP1.
2. Otherwise run `pre:checkpoint:code-review` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir, files: <space-separated files_modified> }`. The executor automatically merges `hooks["pre:code-review"]` entries for backward compatibility.

Proceed to CP1 when hooks complete.

---

### 5. Checkpoint 1 — Code Review

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `"code-review"` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).

Read `concerns[]`, `files_modified`, `task_summaries`, and `step_summaries.plan` from .spec-context.json for the display below.

Display exactly this format, then use the **AskUserQuestion** tool:

```
🔍 **Code Review**

All {N} tasks complete. Here's what changed:

**Task Summaries**:
- **T001**: {task_summaries.T001.did}
- **T002**: {task_summaries.T002.did}
- ...

**Changes** ({N} files):
- `path/to/file` — [one line description]
- `path/to/file` — [one line description] (not in plan)

For each file in `files_modified`, check if it appears in the plan's file list (from `step_summaries.plan` or plan.md). If a file was NOT in the original plan, append "(not in plan)" to its line.

⚠️ **Concerns** ({N}):
- **T002**: {concern note from concerns[]}
- **T004**: {concern note from concerns[]}
(If no concerns, display: "none")

⚠️ **Silent fixes**: [list any deviations beyond what's in concerns[], or "none"]

**Does it match the spec?**
- [ ] {scenario from spec} → expected result
- [ ] {edge case from spec} → expected result
```

Call **AskUserQuestion** with these options:
- **Continue** — proceed to commit
- **Fix** — user provides fix notes in the "Other" field; address the issue, update `tasks.md`, return to CP1

---

### 6. Checkpoint 2 — Test Results

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `"test-results"` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).

Run `pre:checkpoint:test-results` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir, files: <space-separated files_modified> }`.

Only show this checkpoint if the user ran tests after CP1.

Display exactly this format, then use the **AskUserQuestion** tool:

```
🧪 **Test Results**

✅ All {N} tests passing — ready to commit

  — or —

❌ {N} tests failed:
- `test name` — {brief diagnosis}
```

Call **AskUserQuestion** with these options:
- **Continue** — proceed to CP3
- **Fix** — user provides fix notes in the "Other" field; fix failing tests, return to CP2

---

### 7. Checkpoint 3 — Commit + PR

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `"commit-review"` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).

Run `pre:checkpoint:commit-review` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir, files: <space-separated files_modified> }`.

Display exactly this format, then use the **AskUserQuestion** tool:

```
💾 **Ready to ship**

**Commit**: `{type}({scope}): {short description}`

**PR**:
> ## What
> - [bullet from spec]
>
> ## Why
> [one sentence from spec]
>
> ## Testing
> - [verify step from tasks]
>
> Closes #{N} (if issue exists)
```

Call **AskUserQuestion** with these options:
- **Approve** — proceed to commit and PR
- **Edit commit** — user provides notes in the "Other" field; apply changes to commit message, redisplay CP3
- **Edit PR** — user provides notes in the "Other" field; apply changes to PR body, redisplay CP3

---

### 8. Commit + PR

Update `specs/{NNN}-{slug}/.spec-context.json`:

- Set `progress` to `null`
- Set `next` to `"done"`
- Set `currentStep` to `"done"` (terminal state — nothing left to execute)
- Set `status` to `"completed"` (drives tree-view grouping; without this, the spec stays in the Active group forever)
- Set `checkpointStatus` to `{ "commit": true, "pr": true }` (update each flag as each step completes)
- Append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md)

> `status` is separate from `currentStep`: it is the lifecycle field (`active` | `tasks-done` | `completed` | `archived`) that downstream tools (tree views, dashboards) group by. PR-open is treated as "completed" — if you need a distinct merged-vs-open gate, wire a post-merge hook that sets `status: "archived"` or equivalent.

Run `pre:commit` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir, files: <space-separated files_modified> }`. A blocking failure here halts the pipeline before any commit is made.

Stage the changed files explicitly (no `git add -A`). **Always include the spec artifacts** (`specs/{NNN}-{slug}/`) alongside implementation files:

```bash
git add path/to/file1 path/to/file2 ... specs/{NNN}-{slug}/
```

Commit using conventional commit format:

```bash
git commit -m "{type}({scope}): {short description}" -m "Closes #{N}"
```

Rules:

- `type`: `feat`, `fix`, `refactor`, `docs`, or `chore`
- `scope`: lowercase, from primary directory modified. Omit if unclear.
- Short description: imperative, lowercase, no period, max 72 chars
- `Closes #N` line: only if issue number exists
- **No Co-Authored-By or attribution lines**

Before pushing, apply the **main-branch push guard** per [branch-creation](../../lib/instructions/branch-creation.md): if `.sdd.json` has `branchStage` set to `"specify"` or `"implement"` and the current branch is `main`/`master`, halt with the refusal message. When `branchStage` is `"manual"` (default), skip the guard — the user is responsible for their branch.

Push:

```bash
git push -u origin $(git branch --show-current)
```

Open PR:

```bash
gh pr create \
  --title "{type}({scope}): {short description}" \
  --body "$(cat <<'EOF'
## What

- [bullet from spec]
- [bullet from spec]

## Why

[one sentence from spec]

## Testing

- [verify step from tasks]
- [verify step from tasks]

Closes #{N}
EOF
)"
```

Rules:

- PR title matches commit message exactly
- `Closes #N` only if issue exists — omit otherwise
- No "Generated with Claude Code" or any AI attribution

Run `post:pr` hooks per [hook-execution](../../lib/instructions/hook-execution.md) with `vars = { slug, spec-dir, files: <space-separated files_modified> }` after `gh pr create` succeeds.

---

### 8b. Finalize spec context

The Step 8 commit captures `.spec-context.json` in its pre-PR state — `prUrl` and the final `last_action` cannot exist until `gh pr create` returns. Ship those in a second commit on the same branch so the PR carries the fully finalized context.

Update `specs/{NNN}-{slug}/.spec-context.json`:

- Set `prUrl` to the URL returned by `gh pr create`
- Set `prNumber` to the numeric PR number
- Set `last_action` to `"PR #{N} opened — {type}({scope}): {short description}"`
- Append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md)

Stage, commit, and push — context file only, no `-A`:

```bash
git add specs/{NNN}-{slug}/.spec-context.json
git commit -m "chore(specs): mark {NNN} shipped — PR #{N}"
git push
```

Skip this step if `gh pr create` failed or no `prUrl` was captured — leave the context in its pre-PR state rather than committing half-finalized data.

---

### 9. Summary

Display exactly this format:

```
✅ **Shipped!**

{Feature Name} is live.

**Commit**: `{type}({scope}): {description}`
**PR**:     {PR URL}
**Scope**:  {N} files changed
```
