# Spec: Configurable Hooks

**Slug**: 014-configurable-hooks | **Date**: 2026-04-02

## Summary

Replace the hardcoded Phase 2 agent-spawning logic (`test-expert`, `docs-expert`) with a configurable `hooks` system in `.sdd.json`. Hooks let users attach skill invocations to specific pipeline points (e.g., before code review). Each hook runs as an agent (own context, parallel execution). This removes the phantom agent dependency, gives users full control over quality checks, and deprecates the `agents` config.

## Requirements

- **R001** (MUST): Add a `hooks` key to `.sdd.json` schema that maps hook points to arrays of prompt strings
- **R002** (MUST): Support hook point `pre:code-review` — fires after Phase 1 tasks complete, before CP1, replacing current Phase 2
- **R003** (MUST): Each hook at a given hook point runs as a subagent (own context, parallel with other hooks at that same point)
- **R004** (MUST): Support template variable `{files}` in hook strings, substituted with the list of files modified during Phase 1
- **R005** (MUST): Remove Phase 2 section from `lib/templates/tasks.md`
- **R006** (MUST): Update `skills/tasks/SKILL.md` to stop generating Phase 2 `[P][A]` tasks
- **R007** (MUST): Update `skills/implement/SKILL.md` Phase 2 logic to read and execute hooks from `.sdd.json` instead of parsing agent names from tasks.md
- **R008** (MUST): Deprecate `agents` config key in `.sdd.json` — document as deprecated, still honor if present (log warning)
- **R009** (MUST): Update `docs/CONFIGURATION.md` with `hooks` documentation
- **R010** (SHOULD): Support hook point `post:task` — fires after each Phase 1 task completes
- **R011** (SHOULD): Support template variable `{slug}` and `{spec-dir}` in hook strings
- **R012** (MAY): Support additional hook points in the future (`post:specify`, `post:plan`, `pre:checkpoint:commit`) without schema changes — the hook point key is a free-form string

## Scenarios

### User configures pre:code-review hooks

**When** `.sdd.json` contains:
```json
{
  "hooks": {
    "pre:code-review": ["/test-expert write tests for {files}", "/docs-expert update docs"]
  }
}
```
**Then** after Phase 1 completes, both hooks spawn as parallel subagents before CP1 displays

### No hooks configured

**When** `.sdd.json` has no `hooks` key (or no `.sdd.json` exists)
**Then** implement skips Phase 2 entirely and proceeds directly to CP1 — no agents spawned, no errors

### Hook with template variable substitution

**When** a hook string contains `{files}` and Phase 1 modified `src/foo.ts` and `src/bar.ts`
**Then** the hook prompt receives the expanded file list

### Legacy agents config present

**When** `.sdd.json` has `agents` key but no `hooks` key
**Then** log a deprecation warning: `⚠ "agents" config is deprecated — migrate to "hooks". See docs/CONFIGURATION.md`
**Then** skip Phase 2 (do not attempt to honor old `agents` config)

### post:task hook fires per task

**When** `.sdd.json` contains `"post:task": ["/lint {files}"]`
**Then** after each Phase 1 task completes, the hook spawns as an agent with that task's changed files

## Out of Scope

- Shipping vanilla test-expert or docs-expert skills inside SDD
- Hook points for non-implement steps (post:specify, post:plan) — future work
- Inline (non-agent) hook execution mode
- Hook ordering/priority within a single hook point
- Conditional hooks (run only if certain files match a pattern)
