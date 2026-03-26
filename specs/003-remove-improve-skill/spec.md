# Spec: Remove Improve Skill

**Slug**: 003-remove-improve-skill | **Date**: 2026-03-26

## Summary

Remove the `/sdd:improve` skill from the published plugin. It is a personal Obsidian vault tracker hardcoded to a specific file path and does not belong in a public plugin that others install.

## Requirements

- **R001** (MUST): Delete `skills/improve/` directory entirely
- **R002** (MUST): Remove all references to `/sdd:improve` from CLAUDE.md, README.md, and CHANGELOG.md
- **R003** (MUST): No broken references remain in any doc or skill file after removal

## Scenarios

### Clean removal

**When** a user installs SDD after this change
**Then** `/sdd:improve` does not appear in available skills

### Docs consistency

**When** a user reads CLAUDE.md, README.md, or CHANGELOG.md
**Then** there is no mention of `improve` or personal tracker

## Out of Scope

- Moving improve to a separate personal plugin
- Replacing improve with a generic alternative
