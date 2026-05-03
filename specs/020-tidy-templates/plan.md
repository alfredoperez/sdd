# Plan: Tidy Spec Templates

**Spec**: [spec.md](./spec.md)

## Approach

Edit two templates and one skill prompt: drop the verbatim `## Format` block from `lib/templates/tasks.md` (replace with a one-line pointer to `skills/tasks/SKILL.md` § Phase rules), drop the `**Stack**:` example line from `lib/templates/plan.md` Technical Context, drop `| **Date**: {TODAY}` from both plan.md and tasks.md template headers, and tighten `skills/plan/SKILL.md` Step 2 so Technical Context is omitted unless the spec genuinely changes language/runtime/test framework. All edits are surgical; no behavior changes for already-shipped specs.

## Files

### Modify

- `lib/templates/tasks.md` — remove the `## Format` block (current lines 7–14) and the trailing `---` separator; replace with a single-line pointer. Drop `| **Date**: {TODAY}` from the header.
- `lib/templates/plan.md` — drop the `**Stack**: ...` line from Technical Context. Drop `| **Date**: {TODAY}` from the header.
- `skills/plan/SKILL.md` — tighten Step 2 instruction so Technical Context is omitted unless the spec changes language/runtime/test framework.
- `CHANGELOG.md` — prepend a `1.13.0` entry summarizing the template cleanup.
- `.claude-plugin/plugin.json` — bump `version` to `1.13.0`.
- `marketplace.json` — bump plugin `version` to `1.13.0`.

## Problem and solution

Every new spec ships three pieces of boilerplate that don't earn their keep: a 4-line `[P]` Format block in tasks.md, a "TypeScript / Node / Vitest" Stack line in plan.md, and a date stamp on plan.md and tasks.md that just restates spec.md's date. We're removing them from the templates so future specs come out clean, and tightening one skill prompt so Technical Context is only included when the project's language or test framework actually changes.
