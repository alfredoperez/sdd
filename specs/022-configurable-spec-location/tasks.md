# Tasks: Configurable Living-Spec Location

**Plan**: [plan.md](./plan.md)

> Format reference: `[P]` markers and parallel groups — see `skills/tasks/SKILL.md` § Phase rules.

## Phase 1: Core Implementation

- [x] **T001** Define the path resolver, union discovery, and orphan-warning rule — `lib/instructions/layered-context.md` | R002, R003, R006, R007
  - **Do**: Add a "Living-spec path resolution" section: `resolve(domain)` = `specPath` when `domains.<name>.location == "colocated"` else `{specDir}/{domain}/spec.md`; error when colocated and `specPath` missing (R006). Change "Domain detection precedence" so discovery is the **union** of `.sdd.json#domains` keys and the `.specs/*/spec.md` glob (R003). Add `specFormat` → template mapping. Add the orphan-spec warning rule: a `*.spec.md` in the tree not pointed at by any colocated domain is flagged (R007).
  - **Verify**: The file documents one resolver rule that the four skills can reference; centralized default is explicit and unchanged.
  - **Leverage**: existing "Domain detection precedence" + "Loading procedure" sections in this file.

- [x] **T002** [P] Create component living-spec template *(depends on T001)* — `lib/templates/spec-component.md` | R005
  - **Do**: Author a format variant of `spec-living.md` for UI/component domains (Purpose, Capabilities, Props, States, Interactions, Requirements, Out of scope, Related). Keep the `{domain}`/`{TODAY}` placeholders.
  - **Verify**: File parallels `spec-living.md` structure; component-specific sections present.
  - **Leverage**: `lib/templates/spec-living.md`.

- [x] **T003** [P] Create endpoint living-spec template *(depends on T001)* — `lib/templates/spec-endpoint.md` | R005
  - **Do**: Author a format variant of `spec-living.md` for API/endpoint domains (Purpose, Routes, Request, Response, Errors, Requirements, Out of scope, Related).
  - **Verify**: File parallels `spec-living.md`; endpoint-specific sections present.
  - **Leverage**: `lib/templates/spec-living.md`.

- [x] **T004** [P] Route specify Layer 1 load through the resolver *(depends on T001)* — `skills/specify/SKILL.md` | R004
  - **Do**: Update Step 3b to load each domain's living spec via the resolver (not the hardcoded `.specs/<domain>/spec.md`); link to the layered-context resolver rule.
  - **Verify**: No hardcoded `.specs/<domain>/spec.md` literal remains in the load instruction; references the resolver.

- [x] **T005** [P] Route plan load + Domain Alignment through the resolver *(depends on T001)* — `skills/plan/SKILL.md` | R004
  - **Do**: Update Step 1 load and Step 2b Domain Alignment Check to resolve paths via the resolver.
  - **Verify**: Both references go through the resolver rule.

- [x] **T006** [P] Route implement CP3 sync + staging through the resolver *(depends on T001)* — `skills/implement/SKILL.md` | R004
  - **Do**: Update CP3 delta-sync to write to the resolved path and `git add` that resolved path (handle colocated paths outside `.specs/`).
  - **Verify**: Sync write + staging both use the resolved path; colocated example noted.

- [x] **T007** [P] Route drift through union discovery + resolver + orphan warning *(depends on T001)* — `skills/drift/SKILL.md` | R004, R007
  - **Do**: Replace the `.specs/*/spec.md`-only glob with the union discovery; `git log` the resolved path per domain; emit the orphan-spec warning for unconfigured `*.spec.md`.
  - **Verify**: Drift iterates configured colocated domains and warns on orphans.

- [x] **T008** [P] Document the new domain fields *(depends on T002–T007)* — `docs/CONFIGURATION.md` | R001, R008
  - **Do**: Under `domains`, document `location`, `specPath`, `specFormat` with examples (one colocated, one centralized).
  - **Verify**: Fields, defaults, and the colocated example are present.

- [x] **T009** [P] Note loadedDomains path resolution *(depends on T002–T007)* — `docs/STATE.md` | R008
  - **Do**: Update the `loadedDomains` row to note paths resolve via `.sdd.json`/the resolver (centralized or colocated).
  - **Verify**: STATE.md reflects resolution.

- [x] **T010** [P] Mention colocated living specs *(depends on T002–T007)* — `README.md` | R008
  - **Do**: In the `.specs/` / config section, mention specs can be colocated next to code via `domains.<name>.location`.
  - **Verify**: README mentions the option.

- [x] **T011** [P] Update layered-context pointer *(depends on T002–T007)* — `CLAUDE.md` | R008
  - **Do**: Adjust the layered-context / living-specs pointer text to mention configurable location (pointer only, no duplicate field table).
  - **Verify**: Pointer accurate; no duplicated field docs.

- [x] **T012** Bump version + CHANGELOG *(depends on T008–T011)* — `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CHANGELOG.md` | R008
  - **Do**: Minor bump to 1.24.0 in both manifests; add a 1.24.0 CHANGELOG entry describing configurable living-spec location.
  - **Verify**: Both manifests at 1.24.0; CHANGELOG entry present.

## Phase 1b: ADR 0002 revision (resolver-as-script + interview decisions)

- [x] **T013** Build the resolver script — `lib/scripts/resolve-spec-paths.py` | R002, R009, R010
  - **Do**: membership (`pattern ∪ include − exclude`), resolution (colocated/centralized), union discovery, most-specific ordering, zero-config fallback, tier paths, orphan detection. CLI: `--changed`, `--all`, `--orphans`, `--json`.
  - **Verify**: `--all` lists this repo's 5 domains; `--changed` orders most-specific first.

- [x] **T014** Eval suite — `lib/scripts/test_resolve_spec_paths.py` | R002
  - **Do**: 20 unittest cases — resolution, missing specPath, membership, ordering, fallback, discovery, orphans (arch/coverage not flagged), tiers.
  - **Verify**: `python3 lib/scripts/test_resolve_spec_paths.py` → OK.

- [x] **T015** Rewire skills to call the script *(depends on T013)* — `skills/{specify,plan,implement,drift}/SKILL.md` | R002, R010
  - **Do**: specify/plan load via `--changed`; drift via `--all`; implement CP3 writes to most-specific; remove prose resolver re-interpretation.
  - **Verify**: each skill invokes `resolve-spec-paths.py`.

- [x] **T016** Point layered-context.md at the script *(depends on T013)* — `lib/instructions/layered-context.md` | R002
  - **Do**: replace prose resolver/discovery with "call the script"; document membership, ordering, tiers, write-most-specific, authoring convention.
  - **Verify**: names the script as single source of truth.

- [x] **T017** Document include/exclude + legacy example — `docs/CONFIGURATION.md` | R009
  - **Do**: add `include`/`exclude` docs + worked legacy (scattered checkout) example.
  - **Verify**: example + globs-preferred note present.

- [x] **T018** Update CHANGELOG 1.24.0 entry — `CHANGELOG.md` | R008
  - **Do**: reflect script, include/exclude, most-specific, tiering, ADR 0002 link.
  - **Verify**: entry updated.
