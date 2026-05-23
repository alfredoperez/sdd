# ADR 0002: Living-Spec Location, Tiering & Incremental Adoption

**Status:** Proposed
**Date:** 2026-05-23
**Deciders:** alfredo

## Context

ADR 0001 established the 4-layer context model and shipped Layer 1 (living specs) as centralized files at `.specs/<domain>/spec.md`. Two gaps remained, surfaced while planning brownfield adoption:

1. **Location is not configurable.** A living spec can only live in the central `.specs/` folder. Teams want a domain's spec to sit *next to the code it describes* (e.g. `src/checkout/checkout.spec.md`), especially for component/feature folders.
2. **There is no adoption path for existing repos.** Neither `/sdd:init` (scaffolds Layer 0 only) nor `/sdd:drift` (a checker that requires `.specs/` to already exist) can bootstrap living specs from an existing, often-legacy codebase. Today adoption means hand-writing every living spec.

This ADR records the decisions made to close both gaps. It is the architectural frame for spec `022-configurable-spec-location` (the mechanism) and the follow-up specs it enables (tiered content consumption; the adoption wizard).

## Decision

### 1. Configurable per-domain location
Each `.sdd.json` `domains.<name>` gains `location` (`"centralized"` default | `"colocated"`) and `specPath` (required when colocated). A spec resolves to `specPath` when colocated, else `{specDir}/<domain>/spec.md`. Backward-compatible: a repo with no `location` fields behaves exactly as today.

### 2. `specFormat` is an open, convention-based value
`specFormat` resolves to `lib/templates/spec-<specFormat>.md`, falling back to the generic `spec-living.md` when no such template exists. SDD ships `component` and `endpoint` as built-ins; projects add their own (`feature`, `service`, `page`, `model`, `overview`, …) by dropping a template file — no code change. It is **not** a fixed enum.

### 3. A "tree of specs" is a flat set of domains, not a nesting primitive
A spec tree (`checkout`, `checkout-cart`, `checkout-payment`) is just multiple domains whose `specPath`s nest in the filesystem. There is no parent/child type in the config or format. Each node carries its own `pattern`/`specPath`, so messy legacy layouts don't have to follow one uniform rule.

### 4. Discovery = union, ordered most-specific-first
The set of all domains is the **union** of (a) every `domains` entry in `.sdd.json` and (b) the `.specs/*/spec.md` glob, de-duplicated by resolved path. When several domains match a changed file, results are ordered **most-specific-first** (longest matching path), so consumers treat the leaf as primary context and the parent as supporting frame.

### 5. Read-all / write-most-specific
On **read** (specify/plan), load *all* matching domains for full context. On **write** (CP3 delta-sync), target only the **most-specific** matching domain by default; write to multiple domains only when a delta block carries an explicit `<!-- domain: <name> -->` marker. This prevents a single requirement from being duplicated up and down the tree.

### 6. The resolver is an executable, tested script — not prose
`resolve(domain)` + union discovery + ordering + orphan detection live in `lib/scripts/resolve-spec-paths.py` (with `test_resolve_spec_paths.py`), mirroring the `drain-spec-context.py` precedent. The four consuming skills (specify/plan/implement/drift) **call** the script rather than re-implementing the logic in prose. This eliminates "resolver drift across skills" and makes the behavior eval-able.

### 7. Tiered per-domain file set (reserve now, implement later)
A domain's living spec is a **tiered file set**, split by how often each file needs to be in context:

| File | Tier | When loaded |
|---|---|---|
| `<domain>.spec.md` | hot — requirements | whenever the domain is in scope |
| `<domain>.arch.md` | cold — architecture + diagrams + deep explanation | only when understanding/modifying architecture (e.g. `plan` for a significant change) |
| `<domain>.coverage.md` | test-time — `R###` → test(s) map | shift-left traceability; on-ramp to PF-1 conformance |

PR1 (spec 022) wires only the **requirements** tier into default load + CP3 sync, and **reserves** the `.arch.md` / `.coverage.md` conventions (recognized by the resolver, not flagged as orphans). Their *consumption* — arch lazy-load, coverage→conformance — is a separate spec.

### 8. Authoring convention: parent = frame, leaf = detail
Parent/area specs hold high-level rules, cross-cutting constraints, and diagrams (the `overview` format). Leaf specs hold the detailed requirements. Reading only the leaf gets ~90% of the context for a local change; the parent adds the architectural frame.

### 9. Adoption is incremental and registry-driven
There is no whole-repo bootstrap. A dev adopts the **area they are working in**: point at it, the AI proposes a tree of domains for *just that area*, the dev confirms/edits, and entries are appended to the **registry** (the `.sdd.json` `domains` map). The registry grows over time as more areas get specced. Living-spec requirements are AI-drafted from code and marked `[DRAFT]` for review.

### 10. Orphan detection
The resolver globs `**/*.spec.md`, excludes the feature dir (`specs/`), `.specs/`, and `specExempt`, and warns on any remaining `*.spec.md` not equal to a configured `specPath`. `.spec.md` is **reserved** for SDD living specs (safe: test files use `.spec.ts`/`.spec.js`, not `.md`).

### 11. Domain membership: `pattern` ∪ `include` − `exclude`
A single regex assumes tidy code; legacy capabilities are scattered across folders. A domain may therefore be defined by `pattern` (regex), `include` (globs/paths to add), and/or `exclude` (globs to remove). **Membership** = matches `pattern` OR any `include` glob, minus `exclude`. Prefer directory/globs over individual files so the list doesn't rot; explicit files are a last resort. The adoption wizard, when it can't derive a clean regex for a messy area, proposes an explicit `include` list of the files it actually found (deterministic, reviewable). `/sdd:drift` can later flag in-area files no domain claims, so the registry can be topped up. In scope for PR1 (the resolver script handles it; evals cover it). `docs/CONFIGURATION.md` carries a worked legacy example (scattered checkout files) as durable reference.

### 12. Extraction depth (adoption wizard)
When AI-drafting a leaf's requirements from existing code: **surface-first** — read the public surface (exports, routes, component props, types, signatures) to draft Capabilities + requirement stubs, then one level into behavior only for primary files to add acceptance scenarios; token-capped per leaf. Low-confidence inferences are marked inline with `[NEEDS CLARIFICATION: …]` (reuses enhancement #16), each requirement tagged *observed* vs *inferred*, and unreadable files listed under `## Uncovered`. Whole spec stays `[DRAFT]` until human review. Behavioral deep-read is a possible opt-in `--deep` later, not the default.

## Rationale

- **Flat domains over a nesting primitive** — the union-discovery mechanism already supports trees; a nesting type would complicate the loader, sync, and drift for no real gain. "We can always adapt" since it's pure config with no migration.
- **Script over prose** — a pure, deterministic mapping is exactly what should be code, not re-interpreted prose in four skills. It removes drift and is the only way to actually *eval* correctness.
- **Tiering by load-frequency** — keeps the always-on context lean (the recurring concern across this design) while still making architecture and test-coverage first-class, just on-demand.
- **Incremental adoption** — devs don't work on the whole repo; forcing a full bootstrap wastes tokens and produces specs nobody asked for. Growing the registry as work happens matches how brownfield adoption actually proceeds.

## Alternatives Considered

- **Closed `specFormat` enum (`generic|component|endpoint`)** — rejected: arbitrarily constrains teams that organize by feature/service/page.
- **First-class parent/child nesting** — rejected: complexity without payoff; trees emerge from paths.
- **Prose resolver re-interpreted per skill** — rejected: drift risk + not eval-able.
- **Per-file / per-component specs** (`Drawer.spec.md` beside every component) — deferred: fans out loader/sync/drift across hundreds of files; revisit if users ask after the per-domain model is in use.
- **Whole-repo adoption pass** — rejected: not suitable; devs work in slices.
- **Heavy multi-artifact plan stage** (spec-kit `plan-template.md`: data-model.md, contracts/, research.md, Constitution Check) — rejected (logged as N15 in comparative research). The `.arch.md` tier captures the *useful* part (architecture + diagrams) without the ceremony.

## Consequences

**Easier:**
- Living specs sit next to the code they describe; brownfield adoption becomes incremental and AI-assisted.
- The resolver is testable (evals) and has one implementation.
- Default context stays lean (requirements tier only); architecture/coverage load on demand.

**Harder:**
- More moving parts per domain (up to three files) and a script dependency in four skills.
- AI-drafted specs need a human review pass (mitigated by `[DRAFT]` marking).

**New constraints:**
- `.spec.md` is reserved for SDD living specs.
- CP3 sync writes to the most-specific domain unless explicitly markered.
- Skills must call `resolve-spec-paths.py` rather than hardcode `.specs/<domain>/spec.md`.

## Related

- **ADRs:** extends [0001-layered-context-loading](./0001-layered-context-loading.md)
- **Specs:** `specs/022-configurable-spec-location/` (mechanism); follow-ups — tiered content consumption (arch lazy-load + coverage/conformance), adoption wizard
- **Enhancements:** #6, #12, #13, #14, #19, and PF-1 (conformance) in `Projects/sdd/v2/`
- **Process note:** these decisions were produced by an interview/grill loop (one question at a time, recommended answer per question, codebase-grounded). Capturing that loop as an SDD step — emitting an ADR as its output — is a tracked candidate feature.
