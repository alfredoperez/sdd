# Plan: Add Sub-step Tracking

**Spec**: [spec.md](./spec.md) | **Date**: 2026-03-26

## Approach

Add a `substep` field to `state.json` and update all 4 workflow skills to write substep values at each phase boundary. The implement skill's context recovery logic reads `substep` to skip already-completed phases instead of re-parsing everything.

## Technical Context

**Stack**: Markdown skill definitions, JSON state files
**Constraints**: Skills are stateless between invocations — `state.json` is the only persistence mechanism

## Data Model

| Entity/Type | Fields / Shape | Notes |
|-------------|---------------|-------|
| `state.json` | `step, task, substep, updated` | Add `substep` (nullable string) |

## Files

### Create

_None_

### Modify

| File | Change |
|------|--------|
| `skills/specify/SKILL.md` | Add `substep` updates at each step: `parsing` → `exploring` → `detecting` → `writing-spec` → `null` |
| `skills/plan/SKILL.md` | Add `substep` updates: `loading` → `writing-plan` → `null` |
| `skills/tasks/SKILL.md` | Add `substep` updates: `loading` → `writing-tasks` → `null` |
| `skills/implement/SKILL.md` | Add `substep` updates: `phase1` → `phase2` → `cp1` → `cp2` → `cp3` → `commit` → `push` → `pr` → `null`. Update context recovery to use `substep` for precise resume. |
| `skills/status/SKILL.md` | Display `substep` in status dashboard when present |
| `CLAUDE.md` | Update state.json format documentation |
| `docs/CONFIGURATION.md` | Update state.json format reference |
