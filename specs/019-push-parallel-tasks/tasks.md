# Tasks: Push Parallel Tasks

**Plan**: [plan.md](./plan.md)

## Format

- `[P]` marks tasks that can run in parallel with adjacent `[P]` tasks.
- Consecutive `[P]` tasks form a **parallel group** — `/sdd:implement` spawns them as concurrent subagents.
- Tasks without `[P]` are **gates**: they start only after all prior tasks complete.
- Two tasks that touch the same file are never both `[P]`.

---

## Phase 1: Core Implementation

- [x] **T001** [P] Add Surface Guide section to CLAUDE.md — `CLAUDE.md` | R004
  - **Do**: Insert a new `### Surface Guide` subsection inside `## Core Concepts`, placed immediately after the existing "Shared Instruction Files" subsection. Content: a 4-row markdown table mapping change types (one-skill behavior / artifact shape / cross-cutting / project-wide invariant) to surfaces (skill prompt / template / shared instruction / CLAUDE.md), followed by a single-sentence decision rule.
  - **Verify**: Open `CLAUDE.md`, confirm the new subsection sits between "Shared Instruction Files" and "Docs Sync Rule", renders as a table in markdown preview, and is ≤15 lines.
  - **Leverage**: The "Shared Instruction Files" subsection already in `CLAUDE.md` (matches voice and depth).

- [x] **T002** [P] Update Phase rules block in tasks skill — `skills/tasks/SKILL.md` | R001, R002, R003
  - **Do**: Replace lines 38–42 (the `**Phase rules:**` block) with a 4-bullet block that:
    1. Keeps bullet 1 unchanged (`Phase 1: all core implementation tasks ordered by dependency`).
    2. Keeps bullet 2 unchanged (the `[P]` semantics: file-disjoint + no data dep).
    3. Keeps bullet 3 unchanged (parallel group / gate behavior).
    4. **Replaces** the old "When unsure, omit `[P]`. Sequential is always safe." bullet with a new bullet pair: (a) "After listing tasks, do a parallelism pass: group tasks by file path. Any task whose file appears nowhere else in Phase 1 (and has no data dep on siblings) is a `[P]` candidate. **A 5+ task spec with zero `[P]` markers should be reviewed before completing — that almost always means a missed pass.**" (b) "When two interpretations are both legal, prefer the one with more `[P]` markers. Sequential is the safe-but-slow fallback, not the default."
  - **Verify**: `grep -n 'Sequential is always safe' skills/tasks/SKILL.md` returns no match; `grep -n 'parallelism pass' skills/tasks/SKILL.md` returns one match; `grep -n '5+ task spec' skills/tasks/SKILL.md` returns one match. Read the file and confirm the **Skip** line at line 44 and Step 3 are unchanged.
  - **Leverage**: The existing block at `skills/tasks/SKILL.md:38-42` (preserve formatting, indentation, and the `**Phase rules:**` header).
