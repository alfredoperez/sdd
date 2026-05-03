# State Tracking Specification

**Domain:** `state-tracking` · **Last updated:** 2026-05-03

> Living spec for `.spec-context.json` — the runtime state file every spec carries.

## Purpose

`.spec-context.json` is the single source of truth for in-flight pipeline state. Skills (and the optional SpecKit Companion VS Code extension) read it to resume work, write it to record progress. Co-authored — every author MUST follow read-then-merge and append-only `transitions[]`.

## Capabilities

- Per-spec runtime state at `specs/{NNN}-{slug}/.spec-context.json`
- Lifecycle fields (`status`, `currentStep`, `progress`, `next`)
- Identity fields (`specName`, `branch`, `workingBranch`, `type`, `selectedAt`, `createdAt`)
- Rolling state (`approach`, `decisions`, `concerns`, `files_modified`, `last_action`, `loadedDomains`, `syncedDomains`)
- Per-step summaries (`step_summaries.specify`, `step_summaries.plan` with principles_concerns / domain_concerns / significance_score / adr_drafted, `step_summaries.tasks`, `step_summaries.implement`)
- Per-task summaries (`task_summaries.{T###}` with status / did / files / concerns)
- Append-only audit log (`transitions[]`)
- Pause flag (`paused: true`) for `/sdd:pause` opt-out of auto-advance
- Auto-mode flag (`auto: true`) for `/sdd:auto` orchestrator
- PR finalization (`prUrl`, `prNumber`, `checkpointStatus`)

## Requirements

### R001: Multi-author write contract

Every writer MUST: (1) read the file before writing, (2) merge changes into the existing object (preserving fields it does not own), (3) append (not overwrite) entries to `transitions[]`. Single Write call per logical update — no partial writes.

### R002: `transitions[]` is append-only and seeded at creation

The first write (by `/sdd:specify`) MUST initialise `transitions` with one entry whose `from: null`. Every subsequent write MUST append a new entry per `lib/instructions/transition-logging.md` with `step`, `substep`, `from`, `by`, `at` fields.

### R003: `currentStep` and `progress` drive resume

`/sdd:resume` and `/sdd:implement` MUST be able to determine the next action from `currentStep` (specify / plan / tasks / implement / done) and `progress` (substep within the current step). The substep enumeration is canonical in `docs/STATE.md`.

### R004: `status` is separate from `currentStep`

`status` (`active` / `tasks-done` / `completed` / `archived`) is the lifecycle field used by tree views and dashboards. It MUST be set independently from `currentStep`. PR-open transitions to `status: "completed"`.

### R005: Schema is documented in two synchronised places

Any schema change MUST update both `docs/STATE.md` (narrative + field tables) and `lib/schemas/spec-context.schema.json` (machine-readable JSON Schema draft 2020-12) in the same PR. `CLAUDE.md` and `docs/ARCHITECTURE.md` carry pointers, not duplicate field tables.

### R006: Layered Context fields integrate cleanly

`loadedDomains: string[]` is set by `/sdd:specify` Step 3b and reused by `/sdd:plan` and `/sdd:implement`. `syncedDomains: string[]` is appended by `/sdd:implement` Step 7b after each successful Layer 1 sync. Both default to empty arrays.

### R007: Plan summary fields cover all soft-warning checks

`step_summaries.plan` MUST carry `principles_concerns` (Step 2a), `domain_concerns` (Step 2b), `significance_score` (Step 2c), and `adr_drafted` (Step 2c outcome) so downstream tooling and resume logic can reason about what the plan check found without re-running it.

### R008: Deprecated fields are warned, not failed

Deprecation table is in `docs/STATE.md`. Validators warn (not fail) when deprecated fields are present. Skills strip deprecated fields on next rewrite.

## Out of scope

- Other state files (`tasks.md` checkboxes — those are markdown, not state).
- VS Code extension specifics (companion product; this spec covers the schema, not the consumer).

## Related

- Canonical reference: [`docs/STATE.md`](../../docs/STATE.md)
- Machine-readable schema: [`lib/schemas/spec-context.schema.json`](../../lib/schemas/spec-context.schema.json)
- Multi-author write rules: `CLAUDE.md` § `.spec-context.json` Format
