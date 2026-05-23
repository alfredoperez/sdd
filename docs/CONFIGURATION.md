# Configuration

SDD works with zero configuration. All settings have sensible defaults. To customize behavior, create a `.sdd.json` file in your project root.

`.sdd.json` lives at the project root (per-project, committed to the repo). There is no user-global config file — each project has its own tech stack, so build commands, hooks, and workflow preferences all live with the project they apply to.

## `.sdd/` folder (project context)

Sibling to `.sdd.json`. Scaffold with `/sdd:init`. All artifacts are optional — SDD reads each one only if present.

| Path | Purpose | Read by |
|---|---|---|
| `.sdd/principles.md` | Project-wide MUSTs (architecture, quality, operations). Plain markdown — no schema. | `/sdd:plan` Step 1 (Layer 0). Surfaces ✓/⚠ in plan footer. |
| `.sdd/decisions/NNNN-<slug>.md` | Architectural Decision Records. 4-digit prefix. Created by `/sdd:adr <slug>`. | Loaded on demand by `/sdd:plan` and `/sdd:specify` when relevant to the change. |
| `.sdd/decisions/.gitkeep` | Empty file so git tracks the empty folder before any ADR exists. | — |

This is the "Layered Context" model — see ADR `.sdd/decisions/0001-layered-context-loading.md` for the design rationale.

## `.specs/` folder (Layer 1 living specs)

Per-capability "current truth" specs that accumulate as features ship. Sibling to `specs/` (the per-feature delta directory). Scaffold per domain by hand or via the spec-living template.

| Path | Purpose | Read by |
|---|---|---|
| `.specs/<domain>/spec.md` | Living spec for the `<domain>` capability — what the system does *today*. From `lib/templates/spec-living.md`. | `/sdd:specify` Step 3b + `/sdd:plan` Step 1 (Layer 1). Mutated by `/sdd:implement` CP3 sync. |

**Domain detection** (see `lib/instructions/layered-context.md` for full precedence):

1. `.sdd.json` `domains.<name>.pattern` regex against changed file paths.
2. Multiple matches → load all matching specs.
3. Fallback: parent-directory basename match against `.specs/<dir>/spec.md`.

Per-feature `specs/{NNN}-{slug}/spec.md` may carry delta blocks (`## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements`, `## RENAMED Requirements`) that `/sdd:implement` syncs into the matching `.specs/<domain>/spec.md` at CP3 closure.

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
- **Description**: Directory where per-feature spec artifacts (Layer 2) are stored. Relative to project root.

### `specDir`
- **Default**: `".specs"`
- **Description**: Directory where per-capability *living* specs (Layer 1) are stored. One subdirectory per domain (e.g., `.specs/auth/spec.md`). Read by `/sdd:specify` and `/sdd:plan`; mutated by `/sdd:implement` at CP3 sync.

### `specExempt`
- **Default**: `["*.config.*", "*.test.*", "**/migrations/**", "scripts/**"]`
- **Description**: Globs of files to ignore when computing spec drift. Read by `/sdd:drift`. Add paths here for files that change frequently but are not behavioral (config, tests, generated migrations, ops scripts).

### `driftCheck`
- **Default**: `"warn"`
- **Values**: `"off"`, `"warn"`, `"gate"`
- **Description**: How `/sdd:drift` behaves. `off` short-circuits the skill. `warn` runs the report and exits successfully. `gate` runs the same report but signals to surrounding workflows / CI that drift findings should block — the skill itself never halts.

### `domains`
- **Default**: none (falls back to parent-directory-basename matching against `.specs/<dir>/spec.md`)
- **Description**: Map of `<name>` → domain config object. Each entry supports the following fields:
  - **`pattern`** — regex tested against changed file paths (POSIX-style, repo-relative). Files that match include the `<name>` domain in the Layer 1 load. Multiple matches are allowed — each matching domain spec is loaded.
  - **`include`** — array of globs to **add** to the domain, on top of `pattern`. For legacy/scattered code where one regex can't capture the capability. Prefer directory globs (`"src/legacy/order*.js"`) over individual files so the list doesn't go stale.
  - **`exclude`** — array of globs to **remove** from the domain (e.g. `["**/*.test.*"]`). Applied after `pattern`/`include`.
  - **`location`** — `"centralized"` (default) | `"colocated"`. Where the domain's living spec lives. `centralized` keeps the spec under `specDir` (e.g. `.specs/<domain>/spec.md`); `colocated` places it next to the code it describes.
  - **`specPath`** — repo-relative path to the living spec (e.g. `"src/app/auth/auth.spec.md"`). **Required when `location` is `"colocated"`**. Ignored when centralized.
  - **`specFormat`** — **open value** (default `"generic"`). Resolves by convention to `lib/templates/spec-<specFormat>.md`, falling back to the generic `spec-living.md` if no such template exists. SDD ships `component` and `endpoint` as built-ins, but projects can add their own (e.g. `spec-feature.md`, `spec-service.md`, `spec-page.md`, `spec-model.md`) and reference them by name — no code change required, just drop the template file.

  **Membership**: a file belongs to the domain if it matches `pattern` **OR** any `include` glob, **minus** any `exclude` glob. **Spec resolution**: when `location` is `"colocated"`, the living spec is read from `specPath`; otherwise it resolves to `{specDir}/<domain>/spec.md`. Domain discovery is the union of the configured `domains` map and the `.specs/*/spec.md` glob, and matches are ordered most-specific first. All of this is implemented by `lib/scripts/resolve-spec-paths.py` (the single source of truth) — see [`lib/instructions/layered-context.md`](../lib/instructions/layered-context.md).

  Example (a centralized domain with just `pattern`, and a colocated domain with the full set of fields):

  ```json
  {
    "domains": {
      "auth":    { "pattern": "^src/auth/" },
      "billing": { "pattern": "^(src|server)/billing/" },
      "ui":      { "pattern": "\\.tsx$", "location": "colocated", "specPath": "src/ui/ui.spec.md", "specFormat": "component" },
      "orders":  { "pattern": "^src/orders/", "location": "colocated", "specPath": "src/orders/orders.spec.md", "specFormat": "feature" }
    }
  }
  ```

  **Legacy / scattered code.** A single regex assumes one capability lives in one folder. Real codebases scatter it. Say "checkout" logic lives in `src/checkout/`, *plus* `src/services/cart-service.ts`, *plus* `src/legacy/order*.js` — but the shared `PriceBox.tsx` is **not** really checkout. No single `pattern` captures that without over- or under-matching. Use `include` to add the strays and `exclude` to drop noise:

  ```json
  {
    "domains": {
      "checkout": {
        "pattern": "^src/checkout/",
        "include": ["src/services/cart-service.ts", "src/legacy/order*.js"],
        "exclude": ["**/*.test.*"],
        "location": "colocated",
        "specPath": "src/checkout/checkout.spec.md"
      }
    }
  }
  ```

  Prefer globs (`src/legacy/order*.js`) over naming individual files — a glob auto-includes new matching files, an explicit path goes stale. `/sdd:drift` can later flag in-area files no domain claims, so you can top up the registry.

  **The registry.** The `domains` map is the **registry** of adopted capabilities. Hand-write it, or let `/sdd:init` grow it: its adoption flow appends a confirmed domain (and writes a `[DRAFT]` living spec) per area you adopt, one area at a time. Re-running `/sdd:init` adds new entries and never overwrites a reviewed spec.

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
