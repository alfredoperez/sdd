# Plan: Extract Agents from Core

**Spec**: [spec.md](./spec.md) | **Date**: 2026-03-26

## Approach

Delete the bundled agent files and rewrite Phase 2 in the implement skill to be agent-agnostic. Instead of hardcoded prompts for `test-expert` and `docs-expert`, Phase 2 will attempt to spawn agents by name from `[A]` tasks and gracefully skip if unavailable.

## Technical Context

**Stack**: Markdown skill definitions (no runtime code)
**Key Dependencies**: Claude Code agent spawning mechanism
**Constraints**: No way to programmatically check if an agent exists — must handle failure gracefully

## Files

### Create

_None_

### Modify

| File | Change |
|------|--------|
| `skills/implement/SKILL.md` | Rewrite Phase 2 (lines 69-91): replace hardcoded agent prompts with generic "spawn agent named in task" logic + graceful skip |
| `skills/tasks/SKILL.md` | Update Phase 2 template to show agent name is the spawned agent (e.g., `— test-expert`) |

### Delete

| File | Reason |
|------|--------|
| `agents/test-expert.md` | Generic agent, not SDD-specific |
| `agents/docs-expert.md` | Generic agent, not SDD-specific |

## Risks

- Users who rely on bundled agents will lose them after update. Mitigation: document in CHANGELOG that agents must now be installed separately.
