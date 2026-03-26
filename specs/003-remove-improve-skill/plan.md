# Plan: Remove Improve Skill

**Spec**: specs/003-remove-improve-skill/spec.md | **Date**: 2026-03-26

## Approach

Delete the `skills/improve/` directory and remove all references to `/sdd:improve` from documentation files.

## Files to Change

- `skills/improve/SKILL.md` — delete entire directory
- `CLAUDE.md` — remove `/sdd:improve` line from Utilities section
- `README.md` — remove `/sdd:improve` row from command table
- `CHANGELOG.md` — remove `/sdd:improve` line from feature list

## Phase 1 Tasks

| ID | Do | Verify |
|----|-----|--------|
| T001 | Delete `skills/improve/` directory | `ls skills/improve` returns not found |
| T002 | Remove improve references from CLAUDE.md, README.md, CHANGELOG.md | `grep -ri improve` returns no skill references |
