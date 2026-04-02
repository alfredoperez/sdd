# Plan: Configurable Hooks

**Spec**: [spec.md](./spec.md) | **Date**: 2026-04-02

## Approach

Replace the hardcoded Phase 2 agent-spawning logic in `skills/implement/SKILL.md` with a hooks system driven by `.sdd.json` config. The implement skill reads `hooks` from config, substitutes template variables (`{files}`, `{slug}`, `{spec-dir}`), and spawns each hook as a parallel subagent at the matching hook point. The tasks template and tasks skill drop Phase 2 entirely. The `agents` config key is deprecated with a warning.

## Files

### Modify

- `skills/implement/SKILL.md` — Rewrite Phase 2 section (step 4, lines ~101-117): instead of parsing `[P][A]` agent names from tasks.md, read `hooks` from `.sdd.json`, match the current hook point (`pre:code-review`), substitute template vars, and spawn each hook string as a parallel subagent. Add `post:task` hook execution after each Phase 1 task. Add deprecation warning when `agents` key is present.
- `skills/tasks/SKILL.md` — Remove Phase 2 generation rules (lines ~34-39): drop `[P][A]` marker references, agent identifier instructions, and the "always include unit tests" Phase 2 rule. Tasks skill only generates Phase 1 sequential tasks.
- `lib/templates/tasks.md` — Remove the entire "Phase 2: Quality" section (lines ~31-44). Keep only Phase 1.
- `docs/CONFIGURATION.md` — Add `hooks` section documenting the schema, supported hook points (`pre:code-review`, `post:task`), template variables (`{files}`, `{slug}`, `{spec-dir}`), and examples. Mark `agents` as deprecated. Update the main `.sdd.json` reference block.
- `CLAUDE.md` — Update any references to Phase 2 agents or `agents` config to reflect hooks.

## Risks

- Existing specs with Phase 2 tasks in their `tasks.md` won't break — implement just won't find `[P][A]` tasks to parse anymore, and hooks take over. No migration needed.
