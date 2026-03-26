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

SDD auto-detects that small changes (1 file, <10 lines) don't need separate plan/tasks steps and generates everything in one shot.

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

### Complexity Detection
SDD automatically classifies changes:
- **Minimal**: 1 file, <10 lines, style/config tweaks → fast path
- **Normal**: 2+ files, new components, public API changes → full path

### Checkpoints
The implement step has 3 gates:
1. **CP1 — Code Review**: Review changes, verify scenarios
2. **CP2 — Test Results**: Verify tests pass (if run)
3. **CP3 — Commit & PR**: Review commit message and PR body

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

## Design Philosophy

SDD combines the best ideas from:
- **spec-kit**: Structured specs with requirement IDs, scenarios
- **superpowers**: Skill-per-step modularity, checkpoint gates
- Plus: auto-complexity detection, state management

See [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) for the full design philosophy.

## License

MIT
