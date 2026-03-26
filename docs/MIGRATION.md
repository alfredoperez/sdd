# Migration Guide

## From Inline Commands to Plugin

If you've been using SDD as inline `.claude/commands/` files, follow these steps to migrate to the plugin.

### 1. Install the Plugin

```bash
# Add the marketplace
/plugin marketplace add alfredoperez/sdd

# Install the plugin
/plugin install sdd@sdd-marketplace
```

### 2. Update Command References

| Old Command | New Command |
|-------------|-------------|
| `/sdd.specify` | `/sdd:specify` |
| `/sdd.plan` | `/sdd:plan` |
| `/sdd.tasks` | `/sdd:tasks` |
| `/sdd.implement` | `/sdd:implement` |

Note: the separator changed from `.` to `:`.

### 3. Remove Inline Files

Delete these files from your project:

```
.claude/commands/sdd.specify.md
.claude/commands/sdd.plan.md
.claude/commands/sdd.tasks.md
.claude/commands/sdd.implement.md
.claude/templates/sdd-spec.md
.claude/templates/sdd-plan.md
.claude/templates/sdd-tasks.md
```

### 4. Existing Specs

Your existing `specs/` directory and all spec artifacts (`spec.md`, `plan.md`, `tasks.md`, `state.json`) are fully compatible. No changes needed.

### 5. Optional: Add `.sdd.json`

If you had project-specific settings in your inline commands (build commands, test commands), move them to `.sdd.json`:

```json
{
  "buildCommand": "nx build my-lib",
  "testCommand": "nx test my-lib"
}
```

## What Changed

### Removed: `handoffs` Frontmatter
Inline commands used `handoffs` in YAML frontmatter to chain commands. The plugin uses text-based handoffs instead — each skill's summary includes a "Next:" line telling you what to run next.

### Added: `/sdd:status`
New command to view all spec states in a dashboard table.

### Changed: Project-Agnostic
The plugin no longer references project-specific commands (like `nx build ngx-dev-toolbar`). Instead, it reads `.sdd.json` or auto-detects build/test commands from your project's `package.json`.
