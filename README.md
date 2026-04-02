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

### Auto mode (recommended)
```
/sdd:auto "add user authentication with OAuth2"
```

One command runs the full pipeline. For normal-complexity changes, it pauses after spec generation for your review. For small changes, it runs straight through.

### Step-by-step with continue
```
/sdd:specify "add rate limiting"
/sdd:continue                      # advances to plan
/sdd:continue                      # advances to tasks
/sdd:continue                      # advances to implement
```

### Manual (full control)
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
| `/sdd:auto <description>` | Run the full pipeline automatically |
| `/sdd:continue [slug]` | Advance one pipeline step |
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
└── .spec-context.json    # Current workflow state
```

### Building Blocks

| Block | Location | Purpose |
|-------|----------|---------|
| **Skills** | `skills/{name}/SKILL.md` | Workflow steps — each skill is a standalone command |
| **Templates** | `lib/templates/*.md` | Markdown stubs filled in by skills (single source of truth) |
| **State** | `specs/{slug}/.spec-context.json` | Tracks workflow progress per feature |

Skills load templates from `lib/templates/` and fill placeholders. See `lib/templates/README.md` for the canonical variable set.

### Complexity Detection

| Signal | Mode |
|--------|------|
| ≤3 existing files, <10 lines | **minimal** → fast path |
| Pure style or config tweak | **minimal** → fast path |
| 4+ files, new component/service | **normal** → full path |
| New public behavior or API | **normal** → full path |

### State Tracking

Each spec tracks progress in `.spec-context.json`:

```json
{
  "step": "implement",
  "task": "T003",
  "substep": "code-review",
  "next": "done",
  "updated": "2026-03-26"
}
```

- **step**: Current phase (specify, plan, tasks, implement)
- **task**: Current task ID during implement
- **substep**: Granular position within a step for precise recovery after context loss
- **next**: Next pipeline step for `/sdd:continue` auto-advance (plan, tasks, implement, done, or null)
- **updated**: Last modification date

If a session ends mid-workflow, re-running the same command resumes from exactly where it left off.

### Checkpoints

The implement step has 3 gates:
1. **CP1 — Code Review**: Review changes, verify scenarios
2. **CP2 — Test Results**: Verify tests pass (if run)
3. **CP3 — Commit & PR**: Review commit message and PR body

## Design Principles

1. **Right-sized process** — A one-line CSS fix and a new auth system shouldn't go through the same ceremony. SDD auto-detects complexity and adjusts.
2. **Specs as artifacts** — Specifications are committed alongside code in `specs/`. They travel with the PR.
3. **Checkpoints, not bureaucracy** — Every gate prevents a real category of mistake. No checkpoint exists "just because."
4. **State enables continuity** — `.spec-context.json` + `substep` tracking means no work is lost on context loss.
5. **Convention over configuration** — Works with zero config. Everything customizable via `.sdd.json` when needed.

## Configuration

Optional `.sdd.json` in project root:

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
| [CONFIGURATION.md](docs/CONFIGURATION.md) | `.sdd.json` reference |

## License

MIT
