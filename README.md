# SDD — Spec-Driven Development

A Claude Code plugin for structured, spec-driven development workflows. Every feature goes through **specify → plan → tasks → implement** with auto-complexity detection that fast-tracks small changes.

## Installation

```bash
# Add the SDD marketplace
/plugin marketplace add alfredoperez/sdd

# Install the plugin
/plugin install sdd@sdd-marketplace
```

## Quick Start

### New feature (full path)
```
/sdd:specify "add user authentication with OAuth2"
/sdd:plan 001-add-oauth2-auth
/sdd:tasks 001-add-oauth2-auth
/sdd:implement 001-add-oauth2-auth
```

### Small fix (fast path — auto-detected)
```
/sdd:specify "fix button hover color"
/sdd:implement 002-fix-button-hover
```

SDD auto-detects that small changes (≤3 files, <10 lines) don't need separate plan/tasks steps and generates everything in one shot.

## Commands

| Command | Description |
|---------|-------------|
| `/sdd:specify <description>` | Create a spec from a feature description |
| `/sdd:plan [slug]` | Generate an implementation plan from a spec |
| `/sdd:tasks [slug]` | Generate a phased task list from a plan |
| `/sdd:implement [slug]` | Execute tasks, run checkpoints, commit and PR |
| `/sdd:status` | Show dashboard of all spec states |

## How It Works

### Spec Structure
Every feature gets a directory under `specs/`:
```
specs/001-my-feature/
├── spec.md       # What to build and why
├── plan.md       # How to build it (files, approach)
├── tasks.md      # Step-by-step task list
└── state.json    # Current workflow state
```

### Building Blocks

SDD is composed of three core building blocks:

| Block | Location | Purpose |
|-------|----------|---------|
| **Skills** | `skills/{name}/SKILL.md` | Workflow steps — each skill is a standalone command |
| **Templates** | `lib/templates/*.md` | Markdown stubs filled in by skills (single source of truth) |
| **State** | `specs/{slug}/state.json` | Tracks workflow progress per feature |

Skills load templates from `lib/templates/` and fill placeholders. See `lib/templates/README.md` for the canonical variable set.

### Complexity Detection
SDD automatically classifies changes:
- **Minimal**: ≤3 files, <10 lines, style/config tweaks → fast path
- **Normal**: 4+ files, new components, public API changes → full path

### State Tracking

Each spec tracks its progress in `state.json`:

```json
{
  "step": "implement",
  "task": "T003",
  "substep": "cp1",
  "updated": "2026-03-26"
}
```

- **step**: Current workflow phase (specify, plan, tasks, implement)
- **task**: Current task ID during implement (null otherwise)
- **substep**: Granular position within a step for precise recovery after context loss
- **updated**: Last modification date

If a session ends mid-workflow, re-running the same command resumes from exactly where it left off — no work is re-executed.

### Checkpoints
The implement step has 3 gates:
1. **CP1 — Code Review**: Review changes, verify scenarios
2. **CP2 — Test Results**: Verify tests pass (if run)
3. **CP3 — Commit & PR**: Review commit message and PR body

### Agents (Phase 2)

During implement, Phase 2 spawns agents for parallel quality work (tests, docs). Agents are **not bundled** — SDD reads agent names from `[A]` tasks in `tasks.md` and spawns them by name. If an agent isn't installed, the task is skipped gracefully.

To use agents, install them separately (globally or via another plugin) and reference them in your task files:
```markdown
- [ ] **T004** [P][A] Unit tests — `test-expert`
- [ ] **T005** [P][A] Update docs — `docs-expert`
```

You can disable specific agents in `.sdd.json`:
```json
{
  "agents": {
    "docs-expert": { "enabled": false }
  }
}
```

## Configuration

Create an optional `.sdd.json` in your project root:

```json
{
  "specsDir": "specs",
  "buildCommand": "npm run build",
  "testCommand": "npm test",
  "commitFormat": "conventional",
  "noAttribution": true
}
```

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for all options.

## Documentation

| Doc | Description |
|-----|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | How SDD is built — building blocks, data flow, state machine |
| [WORKFLOWS.md](docs/WORKFLOWS.md) | Full path vs fast path, resume, status |
| [CONFIGURATION.md](docs/CONFIGURATION.md) | `.sdd.json` reference |
| [PHILOSOPHY.md](docs/PHILOSOPHY.md) | Design principles and lineage |
| [MIGRATION.md](docs/MIGRATION.md) | Migrating from inline commands |

## License

MIT
