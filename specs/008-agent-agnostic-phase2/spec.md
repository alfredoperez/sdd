# Spec: Make Phase 2 Agent-Agnostic

**Slug**: 008-agent-agnostic-phase2 | **Date**: 2026-03-26

## Summary

The implement skill hardcodes `test-expert` and `docs-expert` agent names and their prompt templates. Make Phase 2 agent-agnostic so it reads agent configuration from tasks.md `[A]` markers or `.sdd.json` and spawns whatever agents are configured, making it easy to add or swap agents.

## Requirements

- **R001** (MUST): Implement reads `[A]` tasks from tasks.md and spawns the agent named in the task (e.g., `test-expert`, `docs-expert`, `security-expert`)
- **R002** (MUST): Agent prompt templates are derived from the task's Do/Verify fields, not hardcoded in implement
- **R003** (SHOULD): `.sdd.json` can optionally map agent names to custom prompts or disable specific agents
- **R004** (MUST): If a referenced agent doesn't exist, skip with a warning (don't fail)

## Scenarios

### Custom agent in tasks.md

**When** tasks.md contains `- [ ] **T005** [P][A] Security review — `security-expert``
**Then** implement spawns `security-expert` agent with context from the task's Do field

### Agent not available

**When** tasks.md references an agent that isn't installed
**Then** implement logs a warning and skips that task, continues to CP1

### Default behavior preserved

**When** tasks.md contains standard `test-expert` and `docs-expert` tasks
**Then** behavior is identical to current implementation

## Out of Scope

- Agent marketplace or discovery
- Agent versioning
- Custom agent definitions in `.sdd.json` (only mapping/disabling)
