# ADR 0001: Layered Context Loading

**Status:** Proposed
**Date:** 2026-05-03
**Deciders:** alfredo

## Context

SDD currently treats every spec as standalone. When a `/sdd:specify` runs in a brownfield codebase, the agent re-discovers the surrounding architecture every time. There is no global "principles" file (the comparative analysis surfaced this gap as N5; the dropped `/sdd:clarify` command per A-1 confirmed users do not invoke separate quality commands), no domain-level accumulator, and no record of why prior architectural choices were made.

Two reference systems exist in the spec-driven workflow space:
- **spec-kit** has a versioned Constitution (`.specify/memory/constitution.md`) gated at plan time, with semver and a Sync Impact Report propagating changes through templates.
- **OpenSpec** has capability-scoped specs (`specs/<capability>/spec.md`) and a schema-driven artifact graph (`schemas/spec-driven/schema.yaml`) where context loading is dynamic via `generateApplyInstructions`.

Neither alone fits SDD's leanness goals: spec-kit's ceremony is too heavy; OpenSpec's capability-scoping forces per-capability spec files at the change-spec layer, which breaks SDD's feature-scoped flow.

## Decision

Adopt a **4-layer cascading context model**:

| Layer | File | Role |
|---|---|---|
| 0 | `.sdd/principles.md` | Global, lightweight, optional |
| 1 | `.specs/<domain>/spec.md` | Per-domain living specs — accumulated requirements that act as the de-facto domain constitution |
| 2 | `specs/{NNN}-{slug}/spec.md` | Feature delta spec (ADDED/MODIFIED/REMOVED/RENAMED format) |
| 3 | `.sdd/decisions/NNNN-<slug>.md` | Cross-feature ADRs |

**Per-stage cascading load:**

- `/sdd:specify` reads Layer 0 + Layer 1 (matching domains for files touched). Writes Layer 2 in delta format.
- `/sdd:plan` re-loads 0 + 1 + 2 + Layer 3 (relevant ADRs). Runs Principles Check, Domain Alignment Check, and Decision Significance Heuristic.
- `/sdd:tasks` is pass-through.
- `/sdd:implement` at CP3 syncs Layer 2 delta into Layer 1 using the operations from enhancement #14.

## Rationale

- **Living specs already function as a domain constitution.** Accumulating ADDED requirements over time IS that domain's MUSTs. We don't need a separate `domains/auth/principles.md` file — the living spec at `.specs/auth/spec.md` is already the right artifact.

- **Lightweight global principles** avoid the heavy spec-kit ceremony (no semver, no Sync Impact Report, no propagation rules). Free-form bullets are enough for SDD's solo and small-team target.

- **ADRs as a sibling artifact** (not just a section inside `design.md`) make cross-feature architectural decisions discoverable independently of any one spec. Per-feature decisions stay in `design.md` Decisions sections; ADRs are reserved for choices that outlive a single feature.

- **Cascading load is a borrowed pattern** from OpenSpec's `instructions.ts` `generateApplyInstructions`, adapted to SDD's per-feature delta model. OpenSpec uses a static artifact graph from `schema.yaml`; SDD uses dynamic domain detection from file paths touched by the change.

- **Principles Check is a soft warning, not a hard gate.** Spec-kit makes the Constitution Check blocking. SDD's leanness suggests warning-only — surface the conflict in plan output but don't block the pipeline. The author can acknowledge or revise.

## Alternatives Considered

- **Full spec-kit constitution** with semver + Sync Impact Report + propagation through every template:
  - **Tradeoff:** rigorous but high-ceremony.
  - **Rejected** (this is N13 in `Projects/sdd/v2/comparative/recommendations.md` — REJECT). Too heavy for SDD's target.

- **Capability-scoped specs as the change unit** (OpenSpec model — one spec file per capability changed):
  - **Tradeoff:** clean per-capability ownership but forces fanout when a feature touches multiple capabilities.
  - **Rejected as default** (N14 in recommendations.md). Feature-scoping fits greenfield. Capability-scoping emerges naturally at Layer 1 (living specs) instead.

- **Decisions section inside `design.md` only, no standalone ADRs:**
  - **Tradeoff:** keeps decisions co-located with their feature.
  - **Rejected** because cross-feature decisions need to be discoverable without reading every feature's design.md. ADR files give them a top-level home.

- **Domain-specific principles files** (`.sdd/domains/<domain>.md`) as a separate Layer 1.5:
  - **Tradeoff:** explicit per-domain MUSTs.
  - **Rejected** because living specs (Layer 1) already serve this role. Adding a sibling file would duplicate intent and create drift.

## Consequences

**Easier:**
- New contributors get global principles + relevant domain spec automatically loaded into context. No need to ask "what are the conventions here?"
- Architectural decisions become discoverable as numbered ADRs.
- Brownfield work is first-class: every change knows the existing requirements before proposing a delta.

**Harder:**
- `/sdd:specify` and `/sdd:plan` skills get more complex (cascading load + conflict-surfacing logic).
- Implementation requires sequencing: Layer 0 (principles) is cheap to ship; Layer 1 (living specs) is the heavy lift (#12).
- Drift between Layer 1 (domain spec) and actual code becomes a tracked concern (handled by `#13` `/sdd:drift`).

**New constraint:**
- When modifying an existing capability, the change must appear as `## MODIFIED Requirements` in the delta spec (Layer 2). Implicit changes that contradict Layer 1 will be flagged at plan time.
- ADRs are append-only for accuracy: superseding an old ADR creates a new ADR with `Status: Supersedes ADR-NNNN`, rather than editing the old one in place.

## Related

- **Enhancements:** #6, #7, #12, #13, #14, #16, #17, #18, #19 in `Projects/sdd/v2/enhancements.md` (in the Obsidian vault)
- **Comparative recommendations:** N1, N2, N4, N5, N9 in `Projects/sdd/v2/comparative/recommendations.md`
- **Source patterns:**
  - spec-kit `templates/constitution-template.md` (lightweight skeleton)
  - spec-kit `templates/commands/specify.md` (`[NEEDS CLARIFICATION]` markers)
  - openspec `schemas/spec-driven/templates/spec.md` (Layer 1 living spec format)
  - openspec `schemas/spec-driven/schema.yaml` (artifact graph dependency model)
  - openspec `src/commands/workflow/instructions.ts` `generateApplyInstructions` (cascading-load pattern)
- **Plan file:** `~/.claude/plans/it-should-go-into-fuzzy-starlight.md` (full implementation roadmap, 7 stages)
