# Tasks: Init Adoption Wizard

**Plan**: [plan.md](./plan.md)

> Format reference: `[P]` markers and parallel groups — see `skills/tasks/SKILL.md` § Phase rules.

## Phase 1: Core Implementation

- [x] **T001** Rewrite init into the phased wizard — `skills/init/SKILL.md` | R001, R002, R003, R004, R005, R006, R007, R008, R009, R010, R011, R012
  - **Do**: Restructure into Phase 1 (scaffold, keep current behavior + optional infer-principles subagent), Phase 2 (adopt-an-area: survey → propose domain tree → surface-first parallel extraction → write registry + specs at resolved paths via `resolve-spec-paths.py`), Phase 3 (summary). Idempotent: skip registered domains, never overwrite non-`[DRAFT]` specs. Already-initialized → skip Phase 1. All choices via `AskUserQuestion`; always skippable.
  - **Verify**: SKILL.md describes all three phases, references the resolver script, and the honest-draft markers ([DRAFT]/observed-vs-inferred/[NEEDS CLARIFICATION]/## Uncovered).
  - **Leverage**: existing `skills/init/SKILL.md` (Phase 1), `lib/scripts/resolve-spec-paths.py`, `lib/templates/spec-living.md`/`spec-component.md`/`spec-endpoint.md`.

- [x] **T002** [P] Update the init description *(depends on T001)* — `CLAUDE.md` | R013
  - **Do**: In "Project setup", expand the `/sdd:init` line to mention incremental brownfield adoption (survey → propose → draft → register), idempotent re-runs.
  - **Verify**: line reflects the wizard; pointer only, no duplicated steps.

- [x] **T003** [P] Note adoption in the README *(depends on T001)* — `README.md` | R013
  - **Do**: Mention `/sdd:init` can adopt an existing repo one area at a time, drafting living specs from code.
  - **Verify**: README mentions adoption.

- [x] **T004** [P] Note the registry write *(depends on T001)* — `docs/CONFIGURATION.md` | R013
  - **Do**: Short note under `domains` that `/sdd:init` adoption appends entries (the registry) and writes `[DRAFT]` specs.
  - **Verify**: note present.

- [x] **T005** Bump version + CHANGELOG *(depends on T002–T004)* — `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CHANGELOG.md` | R013
  - **Do**: Minor bump to 1.25.0 in both manifests; add a 1.25.0 CHANGELOG entry describing the init adoption wizard.
  - **Verify**: both manifests at 1.25.0; CHANGELOG entry present.
