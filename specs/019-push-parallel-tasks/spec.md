# Spec: Push Parallel Tasks

**Slug**: 019-push-parallel-tasks | **Date**: 2026-05-03

## Summary

Bias `/sdd:tasks` toward emitting `[P]` markers when tasks are file-disjoint and have no data dependency. Today the skill prompt closes its Phase rules with "When unsure, omit `[P]`. Sequential is always safe." — which actively discourages parallelism even when it is legal. Result: the largest, most parallelizable specs (e.g. `070-design-tighten-safety`: 28 tasks across 15+ disjoint files) ship with zero `[P]` markers. Adds a parallelism-scan instruction, flips the conservative-bias sentence, and introduces a sanity-check ("5+ tasks with zero `[P]` should be reviewed"). Also adds a one-time **Surface Guide** to `CLAUDE.md` so future SDD prompt edits land on the right surface (skill vs template vs shared instruction vs CLAUDE.md).

## Requirements

- **R001** (MUST): `skills/tasks/SKILL.md` Phase rules include a parallelism-scan instruction directing the agent, after listing tasks, to group by file path and mark file-disjoint tasks (with no data dep) as `[P]` candidates.
- **R002** (MUST): `skills/tasks/SKILL.md` removes the "When unsure, omit `[P]`. Sequential is always safe." sentence and replaces it with guidance preferring more `[P]` markers when two interpretations are both legal — reframing sequential as a safe-but-slow fallback, not the default.
- **R003** (MUST): `skills/tasks/SKILL.md` adds a sanity-check rule: a Phase 1 with 5+ tasks and zero `[P]` markers should be reviewed before completing the skill, because that almost always indicates a missed parallelism pass.
- **R004** (MUST): `CLAUDE.md` gains a **Surface Guide** section that maps types of SDD changes to the correct file surface (skill prompt / template / shared instruction / CLAUDE.md) so future eval-card decisions route consistently.

## Scenarios

### Multi-file disjoint task list

**When** `/sdd:tasks` produces a task list of 5+ tasks where multiple tasks touch entirely disjoint files (e.g. one CSS file, one webpack config, one package.json, one README)
**Then** the resulting `tasks.md` contains at least one `[P]` group covering those file-disjoint tasks, OR the agent self-reviews and explicitly justifies why none qualify before declaring the skill complete

### Single-file or trivial spec

**When** `/sdd:tasks` produces ≤4 tasks, or all tasks modify the same file
**Then** no `[P]` markers appear and the sanity-check does not fire (small specs and shared-file specs are not flagged as missed-parallelism)

## Out of Scope

- Changing the `[P]` semantics themselves (file-disjoint + no data dependency) — those are sound (W3 in the eval doc)
- Editing `lib/templates/tasks.md` or any skill other than `skills/tasks/SKILL.md`
- Retroactively rewriting existing specs' `tasks.md` to add `[P]` markers
- Auto-enforcing the sanity-check via tooling (this spec is prompt-language only)
- Applying the new Surface Guide retroactively to other eval cards (D2–D12) — those are separate specs
