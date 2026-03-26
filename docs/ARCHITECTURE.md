# Architecture

How SDD is built internally.

## High-Level Workflow

```mermaid
flowchart LR
    A[Feature Description] --> B[/sdd:specify/]
    B -->|normal| C[/sdd:plan/]
    B -->|minimal| F[/sdd:implement/]
    C --> D[/sdd:tasks/]
    D --> F
    F --> G[Commit + PR]
```

## Building Blocks

```mermaid
graph TD
    subgraph Plugin["SDD Plugin"]
        subgraph Skills
            S1[specify]
            S2[plan]
            S3[tasks]
            S4[implement]
            S5[status]
        end
        subgraph Templates
            T1[spec-normal.md]
            T2[spec-minimal.md]
            T3[plan.md]
            T4[tasks.md]
        end
    end

    S1 -->|"reads"| T1 & T2
    S2 -->|"reads"| T3
    S3 -->|"reads"| T4
    S4 -.->|"spawns external"| Agents["Agents (not bundled)"]
```

### Skills

Each skill is a standalone command defined in `skills/{name}/SKILL.md`. Skills load templates from `lib/templates/` and fill placeholders.

| Skill | Purpose | Reads | Writes |
|-------|---------|-------|--------|
| specify | Create spec from description | Codebase files | spec.md, state.json (+ plan.md, tasks.md if minimal) |
| plan | Design implementation approach | spec.md | plan.md, state.json |
| tasks | Generate phased task list | spec.md, plan.md | tasks.md, state.json |
| implement | Execute tasks, checkpoint, commit | spec.md, plan.md, tasks.md | Source code, state.json, commit + PR |
| status | Show dashboard | All state.json files | (display only) |

### Templates

Templates live in `lib/templates/` and are the single source of truth. Skills reference them instead of inlining.

| Template | Used by | Variables |
|----------|---------|-----------|
| `spec-normal.md` | specify (normal mode) | `{Feature Name}`, `{NNN}-{slug}`, `{TODAY}` |
| `spec-minimal.md` | specify (minimal mode) | `{Feature Name}`, `{NNN}-{slug}`, `{TODAY}` |
| `plan.md` | plan, specify (minimal) | `{Feature Name}`, `{TODAY}` |
| `tasks.md` | tasks, specify (minimal) | `{Feature Name}`, `{TODAY}` |

See `lib/templates/README.md` for the canonical variable set.

## Data Flow

```mermaid
flowchart TD
    subgraph specify["/sdd:specify"]
        S1[Explore codebase] --> S2[Detect complexity]
        S2 --> S3[Write spec.md]
    end

    subgraph plan["/sdd:plan"]
        P1[Read spec.md] --> P2[Write plan.md]
    end

    subgraph tasks["/sdd:tasks"]
        K1[Read spec.md + plan.md] --> K2[Write tasks.md]
    end

    subgraph implement["/sdd:implement"]
        I1[Read spec + plan + tasks] --> I2[Execute Phase 1]
        I2 --> I3[Spawn Phase 2 agents]
        I3 --> I4[Checkpoints]
        I4 --> I5[Commit + PR]
    end

    specify --> plan --> tasks --> implement
```

## State Machine

```mermaid
stateDiagram-v2
    [*] --> specify: /sdd:specify
    specify --> plan: /sdd:plan (normal)
    specify --> tasks: auto (minimal)
    plan --> tasks: /sdd:tasks
    tasks --> implement: /sdd:implement
    implement --> implement: resume (context loss)
    implement --> [*]: commit + PR
```

### state.json

```json
{
  "step": "implement",
  "task": "T003",
  "substep": "cp1",
  "updated": "2026-03-26"
}
```

| Field | Values | Purpose |
|-------|--------|---------|
| `step` | specify, plan, tasks, implement | Current workflow phase |
| `task` | T001–T00N or null | Current task during implement |
| `substep` | See below or null | Granular position for precise recovery |
| `updated` | YYYY-MM-DD | Last modification date |

### Substep Values

| Skill | Substeps |
|-------|----------|
| specify | parsing → exploring → detecting → writing-spec |
| plan | loading → writing-plan |
| tasks | loading → writing-tasks |
| implement | phase1 → phase2 → cp1 → cp2 → cp3 → commit → push → pr |

On resume, the skill reads `substep` and skips completed phases.

## Implement Detail

```mermaid
flowchart TD
    Start([/sdd:implement]) --> Load[Load spec + plan + tasks + state]
    Load --> Resume{substep set?}
    Resume -->|yes| Skip[Skip to substep phase]
    Resume -->|no| Phase1

    subgraph Phase1["Phase 1 — Sequential"]
        Do[Execute task] --> Verify[Run verification]
        Verify --> Mark["Mark [x] in tasks.md"]
        Mark --> Next{More tasks?}
        Next -->|yes| Do
    end

    Next -->|no| Mode{Normal mode?}
    Mode -->|minimal| CP1
    Mode -->|normal| Phase2[Phase 2 — Spawn agents] --> CP1

    CP1[CP1: Code Review] --> CP2[CP2: Test Results]
    CP2 --> CP3[CP3: Commit & PR]
    CP3 --> Done([Commit + PR])
```

### Phase 2 Agents

Agents are not bundled with SDD. The implement skill reads `[A]` tasks from `tasks.md`, extracts the agent name, and spawns it. If an agent isn't installed, the task is skipped with a warning.

Configure agents in `.sdd.json`:
```json
{
  "agents": {
    "test-expert": { "enabled": true },
    "docs-expert": { "enabled": false }
  }
}
```

## File Tree

```
sdd/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata + version
│   └── marketplace.json     # Marketplace listing
├── skills/
│   ├── specify/SKILL.md     # Step 1: spec from description
│   ├── plan/SKILL.md        # Step 2: implementation design
│   ├── tasks/SKILL.md       # Step 3: phased task list
│   ├── implement/SKILL.md   # Step 4: execute + commit + PR
│   └── status/SKILL.md      # Utility: dashboard
├── lib/templates/
│   ├── README.md            # Template variable reference
│   ├── spec-normal.md       # Full spec template
│   ├── spec-minimal.md      # Minimal spec template
│   ├── plan.md              # Plan template
│   └── tasks.md             # Tasks template
├── docs/
│   ├── ARCHITECTURE.md      # This file
│   ├── WORKFLOWS.md         # Full/fast path details
│   ├── CONFIGURATION.md     # .sdd.json reference
│   ├── PHILOSOPHY.md        # Design principles
│   └── MIGRATION.md         # Migration guide
└── specs/                   # Generated specs
    └── {NNN}-{slug}/
        ├── spec.md
        ├── plan.md
        ├── tasks.md
        └── state.json
```
