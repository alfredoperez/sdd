# Configuration

SDD works with zero configuration. All settings have sensible defaults. To customize behavior, create a `.sdd.json` file in your project root.

`.sdd.json` lives at the project root (per-project, committed to the repo). There is no user-global config file — each project has its own tech stack, so build commands, hooks, and workflow preferences all live with the project they apply to.

## `.sdd.json` Reference

```json
{
  "specsDir": "specs",
  "buildCommand": "npm run build",
  "testCommand": "npm test",
  "commitFormat": "conventional",
  "noAttribution": true,
  "branchStage": "manual",
  "branchNameFormat": "{NNN}-{slug}",
  "minimalThreshold": {
    "maxFiles": 3,
    "maxLines": 10
  },
  "checkpoints": {
    "planReview": true,
    "codeReview": true,
    "commitReview": true
  },
  "hooks": {
    "pre:code-review": ["/test-expert write tests for {files}"],
    "post:task": ["/lint {files}"]
  }
}
```

## Options

### `specsDir`
- **Default**: `"specs"`
- **Description**: Directory where spec artifacts are stored. Relative to project root.

### `buildCommand`
- **Default**: auto-detected from `package.json` scripts
- **Description**: Command to run after Phase 1 implementation. Used to verify the build passes.

### `testCommand`
- **Default**: auto-detected from `package.json` scripts
- **Description**: Command to run tests. Shown in CP2 checkpoint.

### `commitFormat`
- **Default**: `"conventional"`
- **Description**: Commit message format. Currently only `"conventional"` is supported (e.g., `feat(scope): description`).

### `noAttribution`
- **Default**: `true`
- **Description**: When `true`, no AI attribution lines (Co-Authored-By, "Generated with...") are added to commits or PRs.

### `branchStage`
- **Default**: `"manual"`
- **Values**: `"specify"`, `"implement"`, `"manual"`
- **Description**: When SDD auto-creates the feature branch.
  - `"specify"` — branch created at the end of `/sdd:specify`, before the spec is written.
  - `"implement"` — branch created at the start of `/sdd:implement`, before Phase 1 tasks.
  - `"manual"` (default) — SDD never creates a branch. You are responsible for checking out a branch before the pipeline starts.

Behavior rules (identical regardless of `stage`):
- If the current branch is `main`/`master`, run `git checkout -b {branch}` (or `git checkout {branch}` if it already exists).
- If the current branch is already the target, no-op.
- If the current branch is some other non-main branch, skip with a warning — SDD never switches branches automatically.
- If the working tree has uncommitted changes, skip with a warning.
- If `branchStage` is `"specify"` or `"implement"` (i.e., not `"manual"`) and Step 8 of `/sdd:implement` is about to push from `main`/`master`, it halts with `🛑 On main but branchStage=<stage> — refusing to push.` Manual mode trusts the user.

### `branchNameFormat`
- **Default**: `"{NNN}-{slug}"`
- **Description**: Template for the auto-created branch name. Variables:
  - `{NNN}` — zero-padded spec number (`014`)
  - `{slug}` — spec slug (`configurable-hooks`)
  - `{Feature Name}` — feature name lowercased, spaces → hyphens
  - `{type}` — conventional-commit type inferred during `/sdd:specify` from the feature description (`feat`, `fix`, `refactor`, `docs`, `chore`). Defaults to `feat` when missing.

Examples:
- `"{type}/{slug}"` → `feat/add-oauth`, `fix/payment-timeout`
- `"{type}/{NNN}-{slug}"` → `feat/014-add-oauth`
- `"{NNN}-{slug}"` (default) → `014-add-oauth`

### `minimalThreshold`
- **Default**: `{ "maxFiles": 3, "maxLines": 10 }`
- **Description**: Thresholds for auto-detecting minimal mode in `/sdd:specify`.
  - `maxFiles`: Maximum number of files touched for a change to be considered minimal.
  - `maxLines`: Maximum lines of change for a change to be considered minimal.

### `checkpoints`
- **Default**: `{ "planReview": true, "codeReview": true, "commitReview": true }`
- **Description**: Control which checkpoints require user approval.
  - `planReview`: Pause for review in `/sdd:plan` step 3.
  - `codeReview`: Pause at CP1 in `/sdd:implement`.
  - `commitReview`: Pause at CP3 in `/sdd:implement`.

### `hooks`
- **Default**: none (no hooks run)
- **Description**: Map of hook-point keys to arrays of hook entries. Each entry is dispatched at the matching pipeline point.

#### Supported hook points

| Hook point | When it fires | Default blocking |
|---|---|---|
| `pre:plan` | `/sdd:plan` — after Step 1 (Load), before Step 2 (Write) | Warn |
| `post:plan` | `/sdd:plan` — after plan.md is written | Warn |
| `pre:implement` | `/sdd:implement` — after Step 1 (Load), before Phase 1. First entry only; skipped on resume | **Halt** |
| `post:task` | `/sdd:implement` — after each Phase 1 task completes | Warn |
| `pre:code-review` | Alias of `pre:checkpoint:code-review` (backward compat) | Warn |
| `pre:checkpoint:code-review` | `/sdd:implement` — after Phase 1, before CP1 display | Warn |
| `pre:checkpoint:test-results` | `/sdd:implement` — before CP2 display | Warn |
| `pre:checkpoint:commit-review` | `/sdd:implement` — before CP3 display | Warn |
| `pre:commit` | `/sdd:implement` — after CP3 approval, before `git commit` | **Halt** |
| `post:pr` | `/sdd:implement` — after `gh pr create` succeeds | Warn |

Unknown hook-point keys are logged with a warning and skipped — they never halt the pipeline.

#### Payload forms

Each entry in a hook-point array can be one of:

| Form | Shape | Meaning |
|---|---|---|
| Plain string | `"/test-expert write tests for {files}"` | Subagent prompt (default — unchanged from previous behavior) |
| Subagent (explicit) | `{ "prompt": "..." }` | Same as plain string, in object form |
| Shell command | `{ "shell": "npm test" }` | Executed via Bash. Exit code determines pass/fail |
| Skill invocation | `{ "skill": "/security-review", "args": "..." }` | Invokes a skill with the `args` string |

Per-entry overrides on object form:
- `blocking: true \| false` — override the per-hook-point default for this entry
- `timeoutSeconds: N` — shell payload timeout (default 120)
- `parallel: false` — force this entry to run sequentially instead of in parallel with siblings

#### Template variables

Substituted in every string field of every entry (including `prompt`, `shell`, and `args`):

| Variable | Value |
|---|---|
| `{files}` | Space-separated list of relevant files — `files_modified` at most hook points, task-specific files at `post:task`, empty at `pre:implement` (nothing modified yet) |
| `{slug}` | Spec slug (e.g., `014-configurable-hooks`) |
| `{spec-dir}` | Spec directory path (e.g., `specs/014-configurable-hooks`) |

#### Full example

```json
{
  "hooks": {
    "pre:plan":                    ["Review spec {spec-dir}/spec.md for ambiguity."],
    "post:plan":                   [{ "skill": "/impeccable:critique", "args": "plan for {slug}" }],
    "pre:implement":               [{ "shell": "git status --porcelain" }],
    "post:task":                   ["/lint {files}"],
    "pre:checkpoint:code-review":  [
      "/test-expert write tests for {files}",
      { "shell": "npx tsc --noEmit" }
    ],
    "pre:checkpoint:test-results": [{ "shell": "npm test" }],
    "pre:checkpoint:commit-review":[{ "skill": "/security-review" }],
    "pre:commit":                  [{ "shell": "npx prettier --check {files}", "blocking": true }],
    "post:pr":                     ["Post PR link for {slug} to the team."]
  }
}
```

**Security note**: shell hooks run with the same privileges as the Claude Code session. Only commit trusted `.sdd.json` files.

### `agents` *(deprecated)*
- **Description**: Previously used to enable/disable Phase 2 agents. Superseded by `hooks`. If present without a `hooks` key, `/sdd:implement` logs a deprecation warning and skips Phase 2. Migrate to `hooks` — see examples above.

## Example: Nx Monorepo

```json
{
  "specsDir": "specs",
  "buildCommand": "nx build my-lib",
  "testCommand": "nx test my-lib",
  "noAttribution": true
}
```

## Example: Branch-on-implement + linting

```json
{
  "branchStage": "implement",
  "hooks": {
    "post:task": [{ "shell": "pnpm lint {files}" }],
    "pre:commit": [{ "shell": "pnpm typecheck", "blocking": true }]
  }
}
```

## Example: Simple Node Project

```json
{
  "buildCommand": "npm run build",
  "testCommand": "npm test"
}
```

## No Config Needed

If you don't create `.sdd.json`, SDD will:
- Store specs in `specs/`
- Auto-detect build/test commands from `package.json`
- Use conventional commits
- Enable all checkpoints
- Use default minimal thresholds (3 files, 10 lines)
- Skip AI attribution
- Never auto-create a branch (`branchStage: "manual"`)
- Run no hooks
