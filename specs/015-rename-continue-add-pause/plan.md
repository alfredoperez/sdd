# Plan: Rename Continue to Resume & Add Pause

**Spec**: [spec.md](./spec.md) | **Date**: 2026-04-02

## Approach

Rename the `skills/continue/` directory to `skills/resume/`, update all cross-references, and create a new `skills/pause/` skill. The resume skill gains a paused-check gate that clears `paused: true` before advancing. The pause skill sets the flag and confirms. Status and auto skills get minor updates to respect the paused state.

## Files

### Create

- `skills/pause/SKILL.md` — new skill that sets `paused: true` in `.spec-context.json`
- `skills/resume/SKILL.md` — renamed from `skills/continue/SKILL.md` with paused-check gate added

### Modify

- `CLAUDE.md` — replace all `/sdd:continue` references with `/sdd:resume`, add `/sdd:pause` to workflow docs
- `skills/auto/SKILL.md` — replace `/sdd:continue` with `/sdd:resume` in auto-advance loop (line 77)
- `skills/status/SKILL.md` — add paused indicator (e.g., "⏸ paused") to dashboard display
- `skills/specify/SKILL.md` — update any `/sdd:continue` references in summary output

### Delete

- `skills/continue/SKILL.md` — replaced by `skills/resume/SKILL.md`

## Data Model

- `.spec-context.json` — new optional field: `"paused": true | false` — when true, resume must clear it before advancing; auto skips paused specs

## Risks

- Existing specs with `next` pointing to continue-based workflows: no risk, the `next` field stores step names (`plan`, `tasks`, `implement`), not skill names
