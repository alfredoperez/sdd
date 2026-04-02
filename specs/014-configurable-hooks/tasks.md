# Tasks: Configurable Hooks

**Plan**: [plan.md](./plan.md) | **Date**: 2026-04-02

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Remove Phase 2 from tasks template — `lib/templates/tasks.md` | R005
  - **Do**: Delete the entire "Phase 2: Quality" section (lines 31-44) including the separator, heading, blockquote, example tasks, and the Phase 2 line from Progress. Update the Progress section to only reference Phase 1 tasks.
  - **Verify**: Template only contains Phase 1 section and Progress references Phase 1 only

- [x] **T002** Remove Phase 2 generation rules from tasks skill *(depends on T001)* — `skills/tasks/SKILL.md` | R006
  - **Do**: In Step 2 "Phase rules", remove the Phase 2 bullet points (lines 36-39): "Phase 2: always include unit tests...", "Omit Phase 2 entirely...", "Use `[P][A]` markers only in Phase 2", and the agent identifier bullet. Tasks skill should only describe Phase 1 sequential task generation.
  - **Verify**: `skills/tasks/SKILL.md` has no references to Phase 2, `[P][A]`, or agent identifiers

- [x] **T003** Rewrite implement Phase 2 to execute hooks from config *(depends on T002)* — `skills/implement/SKILL.md` | R002, R003, R004, R007, R008, R010, R011
  - **Do**: Replace Step 4 "Phase 2 — Parallel Agents" (lines 101-117) with a new "Phase 2 — Hooks" section that: (1) reads `hooks` from `.sdd.json`, (2) if no `hooks` key exists, checks for deprecated `agents` key and logs warning `⚠ "agents" config is deprecated — migrate to "hooks". See docs/CONFIGURATION.md`, then skips Phase 2, (3) if no hooks config at all, skips Phase 2 entirely, (4) for `pre:code-review` hook point: after Phase 1 completes, substitute template variables (`{files}` → files_modified list, `{slug}` → spec slug, `{spec-dir}` → spec directory path) in each hook string and spawn all hooks at that point as parallel subagents, (5) for `post:task` hook point: add execution after each Phase 1 task in Step 2, substituting `{files}` with that task's changed files. Also update Context Recovery table to remove `phase2` substep reference and replace with `hooks`.
  - **Verify**: implement SKILL.md references hooks config instead of `[P][A]` parsing; no references to parsing agent names from tasks.md remain
  - **Leverage**: Existing Phase 2 section structure (lines 101-117) for the replacement pattern

- [x] **T004** Document hooks in CONFIGURATION.md *(depends on T003)* — `docs/CONFIGURATION.md` | R009, R008, R012
  - **Do**: (1) Add a `hooks` section after `checkpoints` documenting: schema (`hooks` is an object mapping hook point strings to arrays of prompt strings), supported hook points (`pre:code-review`, `post:task`), template variables (`{files}`, `{slug}`, `{spec-dir}`), example config, and note that hook point keys are free-form strings for future extensibility. (2) Update the `agents` section to mark it as deprecated with a note to migrate to `hooks`. (3) Update the main `.sdd.json` reference block at the top to replace `agents` with `hooks` example.
  - **Verify**: `docs/CONFIGURATION.md` has `hooks` section with examples, `agents` section marked deprecated, reference block updated

- [x] **T005** Update CLAUDE.md Phase 2 and agents references *(depends on T003)* — `CLAUDE.md` | R005, R006
  - **Do**: Update the tasks skill Phase rules in the `### 2. Write` step description to remove Phase 2 references (`[P][A]` markers, agent identifiers, "always include unit tests" Phase 2 rule). These lines in CLAUDE.md mirror the tasks skill instructions.
  - **Verify**: `CLAUDE.md` has no references to Phase 2 agents or `[P][A]` markers in tasks context

---

## Progress

- Phase 1: T001–T005 [x]
