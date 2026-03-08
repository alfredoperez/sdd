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
    "maxFiles": 1,
    "maxLines": 10
  },
  "checkpoints": {
    "planReview": true,
    "codeReview": true,
    "commitReview": true
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
- **Default**: `{ "maxFiles": 1, "maxLines": 10 }`
- **Description**: Thresholds for auto-detecting minimal mode in `/sdd:specify`.
  - `maxFiles`: Maximum number of files touched for a change to be considered minimal.
  - `maxLines`: Maximum lines of change for a change to be considered minimal.

### `checkpoints`
- **Default**: `{ "planReview": true, "codeReview": true, "commitReview": true }`
- **Description**: Control which checkpoints require user approval.
  - `planReview`: Pause for review in `/sdd:plan` step 3.
  - `codeReview`: Pause at CP1 in `/sdd:implement`.
  - `commitReview`: Pause at CP3 in `/sdd:implement`.

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
- Use default minimal thresholds (1 file, 10 lines)
- Skip AI attribution
