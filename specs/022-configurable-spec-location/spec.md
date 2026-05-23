# Spec: Configurable Living-Spec Location

**Slug**: 022-configurable-spec-location | **Date**: 2026-05-23

## Summary

Today every Layer 1 living spec is forced to live at `.specs/<domain>/spec.md` (centralized). This feature lets each domain in `.sdd.json` choose where its living spec lives — keep it centralized, or **colocate** it inside the code tree next to the component or API it describes (e.g. `src/app/auth/auth.spec.md`). A single path resolver becomes the one place that maps a domain to its spec file, and every consumer (specify, plan, implement, drift) reads through it instead of hardcoding the `.specs/` path. This is the unshipped half of enhancement #12 and the prerequisite for the brownfield-adoption wizard's "centralized vs colocated" question.

## Modified Capabilities

- **specify** — see `.specs/specify/spec.md`
- **plan** — see `.specs/plan/spec.md`
- **implement** — see `.specs/implement/spec.md`
- **templates** — see `.specs/templates/spec.md`

## Requirements

- **R001** (MUST): Each entry in `.sdd.json` `domains.<name>` accepts new optional fields: `location` (`"centralized"` default | `"colocated"`), `specPath` (repo-relative path; required when colocated), `specFormat` (**open value** → `lib/templates/spec-<specFormat>.md`, fallback `spec-living.md`), and `include`/`exclude` (glob arrays).
- **R002** (MUST): A single **executable** resolver — `lib/scripts/resolve-spec-paths.py` (with `test_resolve_spec_paths.py`) — is the only place path logic lives. It computes membership, resolution (`colocated → specPath`, else `{specDir}/{domain}/spec.md`), discovery, ordering, tier files, and orphans. The four consuming skills **call** it; `lib/instructions/layered-context.md` documents the contract.
- **R009** (MUST): Domain membership = matches `pattern` **OR** any `include` glob, **minus** any `exclude` glob — so scattered legacy code can be captured without one over-broad regex.
- **R010** (MUST): `--changed` results are ordered **most-specific first** (deepest scope path prefixing the file), preserving the zero-config parent-dir-basename fallback. Reads load all matched domains (leaf primary); CP3 delta-sync writes to the **most-specific** domain only, unless a `<!-- domain: <name> -->` marker overrides.
- **R011** (MUST): The resolver reserves a tiered file set per domain — `.spec.md` (wired), `.arch.md` and `.coverage.md` (reserved: recognized, never orphan-flagged). Their consumption is out of scope here.
- **R003** (MUST): Domain discovery is the **union** of (a) every domain declared in `.sdd.json#domains` and (b) the existing `.specs/*/spec.md` glob — so colocated domains (which live outside `.specs/`) are still discovered.
- **R004** (MUST): The four consumers resolve the living-spec path through the resolver instead of the hardcoded `.specs/<domain>/spec.md` literal: `/sdd:specify` (Step 3b load), `/sdd:plan` (Step 1 load + Domain Alignment Check), `/sdd:implement` (CP3 delta-sync write + git staging of the synced file), `/sdd:drift` (domain iteration + `git log` of the resolved path).
- **R005** (MUST): Two new templates exist — `lib/templates/spec-component.md` and `lib/templates/spec-endpoint.md` — as format variants of `spec-living.md`, selected by a domain's `specFormat`.
- **R006** (MUST): When `location` is `"colocated"` but `specPath` is missing, the resolver/consumers surface a clear configuration error naming the offending domain rather than silently falling back.
- **R007** (SHOULD): `/sdd:drift` (and the loader where cheap) warns when it encounters a `*.spec.md` file inside the code tree that does not correspond to any configured colocated domain (orphan colocated spec).
- **R008** (MUST): Docs are synced in the same change per the repo's Docs Sync Rule — `docs/CONFIGURATION.md` (new `domains` fields), `lib/instructions/layered-context.md` (resolver + union discovery), `docs/STATE.md` (`loadedDomains` resolves via config), `README.md`, and the `CLAUDE.md` pointer — and the plugin version + CHANGELOG are bumped in the same change.

## Scenarios

### Colocated domain load

**When** `.sdd.json` declares `"ui": { "pattern": "\\.tsx$", "location": "colocated", "specPath": "src/ui/ui.spec.md" }` and `/sdd:specify` touches a `.tsx` file
**Then** the `ui` domain is discovered and its living spec is loaded from `src/ui/ui.spec.md`, not `.specs/ui/spec.md`

### Centralized domain still works (backward compatible)

**When** a domain has no `location` field (or `location: "centralized"`)
**Then** its living spec resolves to `{specDir}/{domain}/spec.md` exactly as before, and existing `.specs/`-only repos behave identically

### CP3 sync to a colocated path

**When** `/sdd:implement` reaches CP3 and a feature spec carries delta blocks for a colocated domain
**Then** the deltas are applied to the resolved colocated file and that file is staged into the same commit as the implementation

### Missing specPath

**When** a domain sets `location: "colocated"` but omits `specPath`
**Then** the consumer stops with a config error naming the domain, instead of writing to a wrong path

### Orphan colocated spec

**When** `/sdd:drift` finds `src/legacy/legacy.spec.md` but no configured domain points at it
**Then** drift emits an informational warning that the file is an unconfigured (orphan) colocated spec

## Out of Scope

- **Per-component / per-file specs** (one `*.spec.md` per component file, e.g. `Drawer.spec.md` beside every `Drawer.tsx`). This feature keeps the model at **exactly one living spec per domain**, merely relocatable. Per-file fanout across loader/sync/drift is a future, separate effort.
- The brownfield-adoption wizard that *generates* these specs and *asks* the location question — that is the follow-up PR; this PR only makes location configurable.
- Auto-migration of existing `.specs/<domain>/spec.md` files into colocated paths.
