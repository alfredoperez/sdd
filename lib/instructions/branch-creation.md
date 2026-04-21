# Branch Creation

When a skill reaches its configured branch-creation stage, it follows this procedure to optionally create the feature branch.

## Calling convention

A skill invokes this by specifying:
- `stage` — either `"specify"` or `"implement"`
- `NNN` — zero-padded spec number (e.g., `014`)
- `slug` — spec slug (e.g., `configurable-hooks`)
- `featureName` — human-readable feature name

## Procedure

1. Read `.sdd.json` from the project root.
   - If missing, or `branchStage` is absent or set to `"manual"`, return immediately (no branch action).
   - If `branchStage` does not equal the caller's `stage`, return immediately.

2. Resolve the target branch name from `branchNameFormat` (default `"{NNN}-{slug}"`). Supported variables: `{NNN}`, `{slug}`, `{Feature Name}` (lowercased, spaces → hyphens).

3. Check the current git state:

   ```bash
   git branch --show-current
   git status --porcelain
   ```

4. Decide based on the decision table below:

   | Situation | Action |
   |---|---|
   | Current branch is `main` or `master` | Run `git checkout -b {branch}`. If the branch already exists locally, run `git checkout {branch}` instead and log `ℹ Reusing existing branch {branch}`. Update `workingBranch` in `.spec-context.json`. |
   | Current branch already equals `{branch}` | No-op. Log `ℹ Already on {branch}`. Update `workingBranch`. |
   | Current branch differs from `{branch}` and is not main/master | Skip. Log `⚠ On branch {current} — SDD will not switch branches. Set branchStage to "manual" to silence.` Leave `workingBranch` unset (or equal to current). |
   | Working tree has uncommitted changes | Skip. Log `⚠ Uncommitted changes — skipping auto branch. Commit or stash first.` Leave `workingBranch` unset. |
   | Git command fails (not a repo, detached HEAD, etc.) | Log `⚠ Branch auto-creation failed: <stderr>` and continue. Never halt the pipeline. |

5. When a checkout succeeds, update `.spec-context.json` with `workingBranch: "{branch}"` and append a transition entry per `transition-logging.md`.

## Main-branch push guard

Called by `/sdd:implement` Step 8 before `git push`:

1. Read `branchStage` from `.sdd.json` (default `"manual"`).
2. Let `current = git branch --show-current`.
3. If `branchStage != "manual"` AND `current` is `main` or `master`:
   - Stop with: `🛑 On {current} but branchStage={stage} — refusing to push. Create a branch manually or rerun from specify.`
4. Otherwise proceed (manual mode trusts the user).

## `.spec-context.json` fields

- `branch` (existing): the branch the user was on when `/sdd:specify` ran. Audit trail — never updated after specify.
- `workingBranch` (new, nullable): the branch implementation actually runs on. Populated by this instruction when a checkout succeeds. Fallback reader: `git branch --show-current` when null.
