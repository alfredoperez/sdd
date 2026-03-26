# Spec: Decouple Templates from Skills

**Slug**: 006-decouple-templates | **Date**: 2026-03-26

## Summary

Skills currently inline their templates as markdown blocks instead of loading from `lib/templates/`. This means every template change requires editing both the template file and the skill file. Decouple them so skills reference templates by path and templates are the single source of truth.

## Requirements

- **R001** (MUST): Skills load templates from `lib/templates/` instead of inlining them
- **R002** (MUST): `lib/templates/` is the single source of truth — no duplicate template content in SKILL.md files
- **R003** (MUST): Skill instructions reference template path (e.g., "Load and fill `lib/templates/plan.md`") with clear placeholder descriptions
- **R004** (SHOULD): Templates use consistent placeholder syntax (e.g., `{Feature Name}`, `{TODAY}`)
- **R005** (MUST): Minimal-mode inline templates in specify skill also reference shared templates or are clearly marked as separate

## Scenarios

### Template update

**When** a template in `lib/templates/` is modified
**Then** only that one file needs to change — no skill files need updating

### Skill reads template

**When** plan skill runs Step 2
**Then** it reads `lib/templates/plan.md`, fills placeholders, and writes to `specs/{slug}/plan.md`

## Out of Scope

- User-overridable templates via `.sdd.json` (future: 008)
- Template inheritance or composition
- Programmatic template engine (keep it simple — read file, replace placeholders)
