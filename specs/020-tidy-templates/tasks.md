# Tasks: Tidy Spec Templates

**Plan**: [plan.md](./plan.md)

## Phase 1: Core Implementation

- [x] **T001** [P] Strip Format block + Date from tasks template — `lib/templates/tasks.md` | R001, R004
  - **Do**: Remove the `## Format` heading and the 4-line `[P]` block (current lines 7–12) plus the trailing `---` separator. Replace with a single pointer line: `> Format reference: `[P]` markers and parallel groups — see `skills/tasks/SKILL.md` § Phase rules.`. On the header line, drop `| **Date**: {TODAY}` so the line reads `**Plan**: [plan.md](./plan.md)`.
  - **Verify**: `grep -c "## Format" lib/templates/tasks.md` returns `0`; `grep -c "Date" lib/templates/tasks.md` returns `0`; the header reads `**Plan**: [plan.md](./plan.md)` exactly.

- [x] **T002** [P] Strip Stack line + Date from plan template — `lib/templates/plan.md` | R002, R004
  - **Do**: Drop the `**Stack**: [e.g., TypeScript, Node 20, Vitest]` line from Technical Context. Keep `**Key Dependencies**:` and `**Constraints**:`. On the header line, drop `| **Date**: {TODAY}` so the line reads `**Spec**: [spec.md](./spec.md)`.
  - **Verify**: `grep -c "Stack" lib/templates/plan.md` returns `0`; `grep -c "Date" lib/templates/plan.md` returns `0`; the header reads `**Spec**: [spec.md](./spec.md)` exactly.

- [x] **T003** [P] Tighten plan SKILL Technical-Context omit-guidance — `skills/plan/SKILL.md` | R003
  - **Do**: Edit Step 2 (around current line 38) — append guidance after the existing optional-sections sentence: "**Technical Context (Stack/Dependencies/Constraints) is project-fixed — omit the section entirely unless this spec changes language, runtime, or test framework.**".
  - **Verify**: `grep -c "language, runtime, or test framework" skills/plan/SKILL.md` returns `1`.

- [x] **T004** Bump version + CHANGELOG — `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CHANGELOG.md` *(depends on T001, T002, T003)* | R006
  - **Do**: Bump `"version"` to `"1.13.0"` in both `.claude-plugin/plugin.json` and `marketplace.json`. Prepend a `## 1.13.0 — 2026-05-03` entry to `CHANGELOG.md` describing the cleanup (D2: drop Format block; D3: drop Stack line + tighten Technical-Context omit-guidance; D4: drop per-file Date from plan/tasks headers).
  - **Verify**: `grep -E '"version": "1\.13\.0"' .claude-plugin/plugin.json marketplace.json` matches both files; `head -5 CHANGELOG.md` shows the new entry.
