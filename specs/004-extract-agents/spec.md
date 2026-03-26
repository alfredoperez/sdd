# Spec: Extract Agents from Core

**Slug**: 004-extract-agents | **Date**: 2026-03-26

## Summary

Remove `test-expert` and `docs-expert` agents from the SDD plugin. They are generic agents (not SDD-specific) that happen to be bundled. The implement skill should reference agents by convention without shipping them. Users provide their own agents or use defaults from a separate plugin.

## Requirements

- **R001** (MUST): Delete `agents/test-expert.md` and `agents/docs-expert.md` from the repo
- **R002** (MUST): Update `skills/implement/SKILL.md` Phase 2 to reference agents by name convention (`test-expert`, `docs-expert`) without assuming they exist in this plugin
- **R003** (MUST): Phase 2 gracefully skips agent tasks if the referenced agent is not available
- **R004** (SHOULD): Document in README how users can provide their own agents

## Scenarios

### Agents not installed

**When** implement reaches Phase 2 and no `test-expert` agent is available
**Then** Phase 2 agent tasks are skipped with a note, implementation continues to CP1

### Agents installed externally

**When** user has `test-expert` agent installed globally or via another plugin
**Then** implement spawns it as before, no behavior change

## Out of Scope

- Creating a separate agents plugin
- Changing Phase 2 task format in tasks.md
