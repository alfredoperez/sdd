# Spec: Enhance Skill Outputs

**Slug**: 009-enhance-skill-outputs | **Date**: 2026-03-26

## Summary

Redesign the summary/output format of all SDD skills to be more visually distinct, informative, and scannable. Add emojis as visual anchors, improve structure with clear sections, and make outputs more meaningful by including key context (file counts, mode, timing).

## Requirements

- **R001** (MUST): Every skill summary uses emojis as visual anchors for key elements (status, files, next step)
- **R002** (MUST): Implement checkpoint outputs (CP1, CP2, CP3) get visual refresh with clearer sections
- **R003** (MUST): Status dashboard uses emoji indicators for step progress
- **R004** (SHOULD): Outputs include contextual info — mode (minimal/normal), file counts, spec number
- **R005** (SHOULD): Consistent visual language across all skills (same emoji for same concept)

## Scenarios

### Specify complete (normal)

**When** specify finishes in normal mode
**Then** output shows feature name, slug, mode badge, and next command with visual formatting

### Specify complete (minimal/fast)

**When** specify finishes in minimal mode
**Then** output shows fast-path indicator, all generated files, and next command

### Implement checkpoints

**When** CP1 (code review) is displayed
**Then** output has clear visual separation between changes list, silent fixes, and verification scenarios

### Status dashboard

**When** user runs /sdd:status
**Then** each spec row has emoji indicator for its step (e.g., 📝 specify, 📐 plan, ✅ implement)

## Out of Scope

- Color/ANSI codes (Claude Code markdown rendering handles this)
- Interactive or animated outputs
- Custom emoji configuration
