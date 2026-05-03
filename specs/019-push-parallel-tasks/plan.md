# Plan: Push Parallel Tasks

**Spec**: [spec.md](./spec.md)

## Approach

Two file edits, both pure prompt/doc changes. (1) Replace the Phase rules block in `skills/tasks/SKILL.md` lines 38–42: keep the existing `[P]` semantics unchanged (they're correct), append a parallelism-scan instruction, flip the conservative-bias sentence, and add a 5+-task sanity-check. (2) Add a **Surface Guide** section to `CLAUDE.md` after "Shared Instruction Files" that codifies where SDD behavior changes belong (skill prompt / template / shared instruction / CLAUDE.md). The Surface Guide makes D1's surface-pick (skill prompt, not template) explicit and reusable for the remaining D2–D12 eval cards.

## Files

### Modify

- `skills/tasks/SKILL.md` — replace Phase rules bullets at lines 38–42 with a 4-bullet block: keep semantics, add parallelism-scan, flip the bias sentence, add the 5+-task sanity-check. No other edits to this file.
- `CLAUDE.md` — add a new `### Surface Guide` subsection under `## Core Concepts` (placed after "Shared Instruction Files"). ~12 lines: a 4-row table mapping change types to surfaces plus a one-line decision rule.
