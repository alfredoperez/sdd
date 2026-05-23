# Plan: Configurable Living-Spec Location

**Spec**: [spec.md](./spec.md)

## Approach

Introduce a single **living-spec path resolver** as the one place that maps a domain to its `spec.md` file, then route every consumer through it. The resolver reads three new optional `.sdd.json` `domains.<name>` fields — `location`, `specPath`, `specFormat` — and returns `specPath` when `location` is `"colocated"`, otherwise `{specDir}/{domain}/spec.md`. Discovery becomes the union of configured domains and the legacy `.specs/*/spec.md` glob so colocated specs (which live outside `.specs/`) are still found. Because SDD has no runtime — skills are prompts — the "resolver" is a documented procedure in `lib/instructions/layered-context.md` that the four consuming skills reference, exactly like the existing domain-detection precedence. This keeps the change additive and fully backward-compatible: a repo with no `location` fields behaves identically to today.

## Files

### Create

- `lib/templates/spec-component.md` — living-spec format variant for UI/component domains (Props / States / Interactions sections)
- `lib/templates/spec-endpoint.md` — living-spec format variant for API/endpoint domains (Routes / Request / Response / Errors sections)

### Modify

- `lib/instructions/layered-context.md` — define the path resolver + `specFormat` selection; change discovery to union(config domains, `.specs/*/spec.md`); add orphan-spec warning rule
- `skills/specify/SKILL.md` — Step 3b loads Layer 1 via the resolver
- `skills/plan/SKILL.md` — Step 1 load + Step 2b Domain Alignment via the resolver
- `skills/implement/SKILL.md` — CP3 delta-sync writes to the resolved path and stages it
- `skills/drift/SKILL.md` — iterate domains via discovery union; `git log` the resolved path; warn on orphan colocated specs
- `docs/CONFIGURATION.md` — document `location`, `specPath`, `specFormat` under `domains`
- `docs/STATE.md` — note `loadedDomains` resolves to paths via `.sdd.json`/resolver
- `README.md` — mention colocated living specs in the `.specs/` / config section
- `CLAUDE.md` — update the layered-context / `.spec-context` pointer text if needed
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CHANGELOG.md` — version bump (minor) in the same change

## ⚠ Domain Alignment

- **specify** — Step 3b's load behavior changes (path now resolved, not hardcoded). Add a `## MODIFIED Requirements` block to spec.md so CP3 syncs it into `.specs/specify/spec.md`.
- **plan** — Domain Alignment Check now resolves paths. Add a `## MODIFIED Requirements` block for `.specs/plan/spec.md`.
- **implement** — CP3 sync writes to a resolved (possibly colocated) path + stages it. Add a `## MODIFIED Requirements` block for `.specs/implement/spec.md`.
- **templates** — two new living-spec format variants added. Add an `## ADDED Requirements` block for `.specs/templates/spec.md`.

> Soft warning. Add the matching delta block(s) to `specs/022-configurable-spec-location/spec.md` before/at implement so CP3 can sync them into Layer 1. (Dogfoods the very feature being built.)

## Testing Strategy

- **Manual / dogfood**: convert one of this repo's existing centralized domains (e.g. `templates`) to a colocated `specPath`, then run `/sdd:drift` and confirm it resolves the new path and still reports correctly.
- **Edge cases**: missing `specPath` when colocated → config error; orphan `*.spec.md` with no domain → warning; centralized repo with zero `location` fields → unchanged behavior.

## Risks

- **Resolver drift across skills**: four prompts must reference the same resolver rule. Mitigation: define it once in `layered-context.md` and have each skill link to it (no copy-paste of the path logic).
