# Spec: Tidy Spec Templates

**Slug**: 020-tidy-templates | **Date**: 2026-05-03

**Key Finding**: The three pieces of per-spec boilerplate flagged in the eval (Format block, Stack line, per-file Date) are shipped *literally* by `lib/templates/{plan,tasks}.md` — the agent isn't improvising; the templates print these strings into every output. Fix lives on the template surface.

## Summary

Strip three pieces of redundant boilerplate that ship in every generated spec via `lib/templates/{plan,tasks}.md`: the verbatim `## Format` block in tasks.md (D2), the project-fixed `Stack:` line in plan.md Technical Context (D3), and the per-file `| **Date**: {TODAY}` headers (D4). All three regress because the templates literally ship them — fix is at the template surface, not author behavior. D3 also tightens the plan skill so Technical Context is omitted unless the spec genuinely changes language/runtime/test framework.

## Requirements

- **R001** (MUST): `lib/templates/tasks.md` no longer carries the 4-line `## Format` block. The semantics are documented exactly once in `skills/tasks/SKILL.md` § Phase rules; tasks.md replaces the block with a single one-line pointer.
- **R002** (MUST): `lib/templates/plan.md` Technical Context no longer prescribes a `**Stack**:` example line. `Key Dependencies` and `Constraints` remain.
- **R003** (MUST): `skills/plan/SKILL.md` Step 2 instructs the agent to omit the entire Technical Context section unless the spec genuinely changes language/runtime/test framework — Stack is project-fixed and lives in `CLAUDE.md`.
- **R004** (MUST): `lib/templates/plan.md` and `lib/templates/tasks.md` headers drop `| **Date**: {TODAY}`; the cross-link (`**Spec**:` / `**Plan**:`) is preserved.
- **R005** (MUST): `lib/templates/spec-normal.md` keeps its `Date` header — spec.md remains the single source of truth for the spec's date.
- **R006** (MUST): `.claude-plugin/plugin.json` and `marketplace.json` versions bump to `1.13.0`; `CHANGELOG.md` records the change in the same commit.

## Scenarios

### Tasks template generates a clean tasks.md

**When** `/sdd:tasks` runs on any new spec
**Then** the produced `tasks.md` contains no `## Format` heading and no 4-line `[P]` boilerplate; instead a single one-line pointer near the top references `skills/tasks/SKILL.md` § Phase rules.

### Plan template generates a clean plan.md

**When** `/sdd:plan` runs on a spec that does not change language/runtime/test framework
**Then** the produced `plan.md` omits the Technical Context section entirely (or, if Constraints/Key Dependencies are needed, includes those without a `**Stack**:` line).

### Plan and tasks headers omit per-file Date

**When** any new `plan.md` or `tasks.md` is written from the templates
**Then** the header line is exactly `**Spec**: [spec.md](./spec.md)` / `**Plan**: [plan.md](./plan.md)` — no `| **Date**:` segment. `spec.md` still carries the date.

## Out of Scope

- D1 (push-parallelism on `/sdd:tasks`) — already shipped.
- D5–D12 from the eval (Decisions section, Independent Test, Success Criteria, Phases/Dependencies graph, scenario tagging, count-based omit triggers, Key Finding header, Approach widening) — separate decision cards, separate specs.
- Backfilling already-shipped specs to remove the boilerplate. Templates are forward-looking only.
