---
name: sdd:implement
description: "SDD — Spec-Driven Development: execute tasks, run checkpoints, commit and open PR."
---

## Steps

### 1. Load

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains `tasks.md`.

Read in parallel:

- `specs/{NNN}-{slug}/tasks.md` — all Phase 1 and Phase 2 tasks
- `specs/{NNN}-{slug}/spec.md` — feature name, requirements, scenarios (for CP1 verification)
- `specs/{NNN}-{slug}/plan.md` — approach, files, issue number if present
- `specs/{NNN}-{slug}/state.json` — current step/task (if exists; note if resuming mid-implement)

Determine commit scope from the primary directory being modified (e.g., `toolbar`, `ui`, `core`). If unclear, omit scope.

Determine issue number from plan.md or spec.md if present.

If no tasks found, stop: "Run `/sdd:specify`, `/sdd:plan`, and `/sdd:tasks` first."

Update `specs/{NNN}-{slug}/state.json`:

```json
{ "step": "implement", "task": "T001", "substep": "phase1", "next": null, "updated": "{TODAY}" }
```

---

### Context Recovery (if resuming)

If `state.json` shows `step = "implement"`:

1. Read `spec.md` for feature context
2. Read `tasks.md` — `[x]` = done, `[ ]` = remaining
3. Read `substep` from `state.json` and use it to skip completed phases:

| `substep` value | Resume point |
|-----------------|-------------|
| `phase1` | Resume from first unchecked task in Phase 1 |
| `phase2` | Skip Phase 1, resume at Phase 2 |
| `code-review` | Skip Phase 1 + Phase 2, resume at CP1 — Code Review |
| `test-results` | Skip through CP1, resume at CP2 — Test Results |
| `commit-review` | Skip through CP2, resume at CP3 — Commit Review |
| `commit` | Skip through CP3, resume at Step 8 (stage + commit) |
| `push` | Skip through commit, resume at Step 8 (push) |
| `pr` | Skip through push, resume at Step 8 (PR creation) |
| `null` or missing | Fall back to task-based recovery: resume from first unchecked task |

4. Do NOT re-run completed phases — trust the substep marker and existing checkmarks

---

### 2. Phase 1 — Sequential Core Implementation

Execute tasks T001 → T002 → ... through all Phase 1 tasks in order.

For each task:

1. Perform the work described in the **Do** field
2. Run the **Verify** check
3. Mark complete in `specs/{NNN}-{slug}/tasks.md`: `- [ ]` → `- [x]`
4. Update `specs/{NNN}-{slug}/state.json` — set `task` to the next task ID (or `null` after the last task)

**Deviation rules:**

| Situation                              | Action                                            |
| -------------------------------------- | ------------------------------------------------- |
| Bug, import error, or type mismatch    | Fix silently — note for CP1                       |
| Missing dependency                     | Fix silently — note for CP1                       |
| Architectural approach needs to change | **STOP. Explain to user and ask how to proceed.** |
| Task is impossible as written          | **STOP. Explain why and ask how to proceed.**     |

After the last Phase 1 task, check if a build command is configured in `.sdd.json`. If so, start the build in background. Otherwise, check if common build commands exist (e.g., `package.json` scripts) and run the appropriate one.

---

### 4. Phase 2 — Parallel Agents (normal mode only)

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"phase2"`.

Skip if the spec shows mode is `"minimal"` or if Phase 2 is omitted from tasks.md.

For each `[P][A]` task in tasks.md:

1. Parse the agent name from the task line — the value in backticks after the `—` delimiter (e.g., `` `test-expert` ``, `` `docs-expert` ``, `` `security-expert` ``)
2. Check `.sdd.json` `agents` config (if present). If `agents.{name}.enabled` is `false`, log: `⏭ Skipping {name} — disabled in .sdd.json` and continue
3. Build the agent prompt from the task's fields: **Do**, **Verify**, **Files**, **Pattern**, **Reference** (include whichever fields are present)
4. Attempt to spawn the named agent as a parallel subagent, passing it:
   - The constructed prompt with all task fields
   - Instruction to mark the task complete in `specs/{NNN}-{slug}/tasks.md` when done
5. If the agent is not available or the spawn fails, log: `⏭ Skipping {name} — agent not available` and continue (do not block other agents or CP1)

Wait for all successfully spawned subagents to complete before proceeding to CP1.

---

### 5. Checkpoint 1 — Code Review

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"code-review"`.

Display exactly this format, then use the **AskUserQuestion** tool:

```
🔍 **Code Review**

All {N} tasks complete. Here's what changed:

**Changes** ({N} files):
- `path/to/file` — [one line description]
- `path/to/file` — [one line description]

⚠️ **Silent fixes**: [list any deviations, or "none"]

**Does it match the spec?**
- [ ] {scenario from spec} → expected result
- [ ] {edge case from spec} → expected result
```

Call **AskUserQuestion** with these options:
- **Continue** — proceed to commit
- **Fix** — user provides fix notes in the "Other" field; address the issue, update `tasks.md`, return to CP1

---

### 6. Checkpoint 2 — Test Results

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"test-results"`.

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

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"commit-review"`.

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

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"commit"`.

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

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"push"`.

Push:

```bash
git push -u origin $(git branch --show-current)
```

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `"pr"`.

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

Update `specs/{NNN}-{slug}/state.json` — set `substep` to `null` and `next` to `"done"`.

Display exactly this format:

```
✅ **Shipped!**

{Feature Name} is live.

**Commit**: `{type}({scope}): {description}`
**PR**:     {PR URL}
**Scope**:  {N} files changed
```
