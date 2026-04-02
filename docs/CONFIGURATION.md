# Configuration

SDD works with zero configuration. All settings have sensible defaults. To customize behavior, create a `.sdd.json` file in your project root.

## `.sdd.json` Reference

```json
{
  "specsDir": "specs",
  "buildCommand": "npm run build",
  "testCommand": "npm test",
  "commitFormat": "conventional",
  "noAttribution": true,
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
- **Description**: Map of hook point strings to arrays of prompt strings. Each prompt is spawned as a parallel subagent at the matching pipeline point during `/sdd:implement`.

**Supported hook points:**

| Hook point | When it fires |
|---|---|
| `pre:code-review` | After all Phase 1 tasks complete, before CP1 |
| `post:task` | After each individual Phase 1 task completes |

**Template variables** (substituted in each prompt string):

| Variable | Value |
|---|---|
| `{files}` | Space-separated list of modified files (all files for `pre:code-review`, task-specific files for `post:task`) |
| `{slug}` | Spec slug (e.g., `014-configurable-hooks`) |
| `{spec-dir}` | Spec directory path (e.g., `specs/014-configurable-hooks`) |

Hook point keys are free-form strings — additional hook points (e.g., `post:specify`, `pre:checkpoint:commit`) can be added in the future without schema changes.

```json
{
  "hooks": {
    "pre:code-review": [
      "/test-expert write tests for {files}",
      "/docs-expert update docs for {slug}"
    ],
    "post:task": ["/lint {files}"]
  }
}
```

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
