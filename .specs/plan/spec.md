# Plan Specification

**Domain:** `plan` · **Last updated:** 2026-05-03

> Living spec for the `/sdd:plan` skill. Current truth.

## Purpose

`/sdd:plan` reads `spec.md` and produces `plan.md`: the implementation strategy, files to create/modify, and risk surface. Runs Layer 0 (Principles), Layer 1 (Domain Alignment), and the Decision Significance Heuristic as soft-warning checks.

## Capabilities

- Spec lookup (by `$ARGUMENTS` or most-recently-modified spec dir)
- Parallel context load: `spec.md`, `.spec-context.json`, `.sdd/principles.md` (Layer 0), `.specs/<domain>/spec.md` (Layer 1 via `loadedDomains`)
- `pre:plan` and `post:plan` hook execution
- `plan.md` write from `lib/templates/plan.md` (omit Technical Context unless language/runtime/test framework changes)
- Step 2a Principles Check — append `## ⚠ Principles Check` when conflicts found, count tracked in `step_summaries.plan.principles_concerns`
- Step 2b Domain Alignment Check — append `## ⚠ Domain Alignment` when conflicts found, count tracked in `step_summaries.plan.domain_concerns`
- Step 2c Decision Significance Heuristic — score 0–3, prompt to draft an ADR when score ≥2
- Step 3 summary footer with optional `{principles-line}` / `{domain-line}`
- Auto self-chain (Step 4) — invokes `/sdd:resume` when `auto: true`

## Requirements

### R001: Locate the active spec

The skill MUST resolve the target spec directory from `$ARGUMENTS` if provided, otherwise the most recently modified `specs/*` dir containing `spec.md`. If none found, halt with `Run /sdd:specify first.`.

### R002: Load all four context layers in parallel

Step 1 MUST issue parallel reads for `spec.md`, `.spec-context.json`, `.sdd/principles.md` (if present), and the Layer 1 specs named in `loadedDomains` (or computed via `layered-context.md` precedence if not yet set).

### R003: Write `plan.md` from the template

Step 2 MUST instantiate `lib/templates/plan.md` with `{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`. Optional sections (Technical Context, Data Model, Mermaid flow, Risks) are included only when relevant; Technical Context is omitted unless this spec changes language, runtime, or test framework.

### R004: Run Principles Check (Layer 0) when `principles.md` is loaded

The skill MUST scan the Approach against each principle bullet. Conflicts append `## ⚠ Principles Check` to `plan.md`. The count (0 if no concerns or no `principles.md`) is recorded in `step_summaries.plan.principles_concerns`. The check NEVER blocks the pipeline.

### R005: Run Domain Alignment Check (Layer 1) when domains are loaded

The skill MUST scan the Approach against each loaded `.specs/<domain>/spec.md`'s requirements for contradictions, silent surface expansion, and unannotated modifications. Conflicts append `## ⚠ Domain Alignment` to `plan.md`. The count is recorded in `step_summaries.plan.domain_concerns`. NEVER blocks.

### R006: Run Decision Significance Heuristic

The skill MUST score the Approach across 3 signals (≥3 alternatives, 2+ domains, new external dependency). When score ≥2, prompt the user via `AskUserQuestion`. On `Yes`, invoke `/sdd:adr` with a slug derived from the spec slug and record `step_summaries.plan.adr_drafted`. On `No`, record `false`. Skip silently if `.sdd/decisions/` does not exist.

### R007: Surface principles + domain status in the footer

Step 3's footer MUST omit / show / warn per the documented `{principles-line}` and `{domain-line}` rules.

## Out of scope

- Task breakdown (handled by `/sdd:tasks`).
- ADR file format / numbering (handled by `/sdd:adr`).
- CP1/2/3 checkpoints (handled by `/sdd:implement`).

## Related

- ADRs: [`.sdd/decisions/0001-layered-context-loading.md`](../../.sdd/decisions/0001-layered-context-loading.md)
- Skill: [`skills/plan/SKILL.md`](../../skills/plan/SKILL.md)
- Template: [`lib/templates/plan.md`](../../lib/templates/plan.md)
