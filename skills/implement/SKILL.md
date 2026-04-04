---
name: sdd:implement
description: "SDD — Spec-Driven Development: execute tasks, run checkpoints, commit and open PR."
---

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

Update `specs/{NNN}-{slug}/.spec-context.json`:

```json
{ "step": "implement", "task": "T001", "substep": "phase1", "next": "implement", "updated": "{TODAY}" }
```

---

### Context Recovery (if resuming)

If `.spec-context.json` shows `step = "implement"`:

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
6. Read `substep` from `.spec-context.json` and use it to skip completed phases:

| `substep` value | Resume point |
|-----------------|-------------|
| `phase1` | Resume from first unchecked task in Phase 1 |
| `hooks` | Skip Phase 1, resume at hooks execution |
| `code-review` | Skip Phase 1 + hooks, resume at CP1 — Code Review |
| `test-results` | Skip through CP1, resume at CP2 — Test Results |
| `commit-review` | Skip through CP2, resume at CP3 — Commit Review |
| `commit` | Skip through CP3, resume at Step 8 (stage + commit) |
| `null` or missing | Fall back to task-based recovery: resume from first unchecked task |

4. Do NOT re-run completed phases — trust the substep marker and existing checkmarks

---

### 2. Phase 1 — Sequential Core Implementation

Execute tasks T001 → T002 → ... through all Phase 1 tasks in order.

For each task:

1. Perform the work described in the **Do** field
2. Run the **Verify** check
3. Mark complete in `specs/{NNN}-{slug}/tasks.md`: `- [ ]` → `- [x]`
4. Update `specs/{NNN}-{slug}/.spec-context.json` atomically (single Write call) with all of the following:
   - Set `task` to the next task ID (or `null` after the last task)
   - Write `task_summaries.{taskId}` with:
     - `status`: `"DONE"` or `"DONE_WITH_CONCERNS"` (use DONE_WITH_CONCERNS if any silent fixes, type workarounds, or edge cases were noted)
     - `did`: one-line summary of what was actually done (not what was planned — what happened)
     - `files`: array of file paths actually modified by this task
     - `concerns`: array of concern strings (empty `[]` if none)
   - Update top-level `files_modified` array — deduplicated union of all files modified across all completed tasks
   - Append to `decisions[]` if a non-trivial decision was made during this task (e.g., chose one approach over another)
   - Append to `concerns[]` array with `{ "task": "{taskId}", "note": "description" }` for any concerns (silent fixes, type workarounds, edge cases found)
   - Set `last_action` to a short description of what just completed (e.g., "T003 complete — added route guards to all /api/* endpoints")
   - Preserve all existing fields (`step`, `substep`, `approach`, `step_summaries`, previous `task_summaries`, etc.)

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

Update `specs/{NNN}-{slug}/.spec-context.json` — set `substep` to `"hooks"`.

Read `.sdd.json` from the project root (if it exists).

1. If `.sdd.json` has a `hooks` key, proceed with hook execution below
2. If `.sdd.json` has no `hooks` key but has an `agents` key, log: `⚠ "agents" config is deprecated — migrate to "hooks". See docs/CONFIGURATION.md` and skip to CP1
3. If no `.sdd.json` exists or it has neither `hooks` nor `agents`, skip to CP1

**Hook execution at `pre:code-review`:**

For each prompt string in `hooks["pre:code-review"]`:

1. Substitute template variables in the prompt string:
   - `{files}` → space-separated list from `files_modified` in .spec-context.json
   - `{slug}` → the spec slug (e.g., `014-configurable-hooks`)
   - `{spec-dir}` → the spec directory path (e.g., `specs/014-configurable-hooks`)
2. Spawn each hook as a parallel subagent with the substituted prompt
3. If a subagent spawn fails, log: `⏭ Skipping hook — agent not available` and continue

Wait for all successfully spawned hook subagents to complete before proceeding to CP1.

**Hook execution at `post:task`:**

If `hooks["post:task"]` exists, execute after each Phase 1 task completes (in Step 2):

1. For each prompt string in the array, substitute template variables:
   - `{files}` → space-separated list of files modified by that specific task (from `task_summaries.{taskId}.files`)
   - `{slug}` → the spec slug
   - `{spec-dir}` → the spec directory path
2. Spawn each hook as a parallel subagent with the substituted prompt
3. Wait for all hook subagents to complete before proceeding to the next task

---

### 5. Checkpoint 1 — Code Review

Update `specs/{NNN}-{slug}/.spec-context.json` — set `substep` to `"code-review"`.

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

Update `specs/{NNN}-{slug}/.spec-context.json` — set `substep` to `"test-results"`.

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

Update `specs/{NNN}-{slug}/.spec-context.json` — set `substep` to `"commit-review"`.

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

Update `specs/{NNN}-{slug}/.spec-context.json` — set `substep` to `null` and `next` to `"done"`.

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
