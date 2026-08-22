# Spec: SpecKit Companion — spec-kit Extension (v1, tracking-first)

**Slug**: 024-speckit-extension-foundation | **Date**: 2026-05-24

## Summary

Ship the first slice of the **SpecKit Companion** spec-kit extension: a new `speckit-extension/` in the **`speckit-companion` monorepo** (beside the VS Code GUI) that captures activity into `.spec-context.json` via spec-kit lifecycle hooks, so the Companion GUI lights up on a user's **existing** spec-kit flow — no template change required. Because the extension lives in the Companion repo, it writes that repo's **canonical** `spec-context.schema.json` natively (no cross-repo schema reconciliation). Commands are namespaced `/speckit.companion.*`. Architecture is decided and validated in **ADR 0003** (`.sdd/decisions/0003-sdd-as-speckit-extension.md`); this spec implements its v1 scope only. (Note: spec/ADR are authored in the `sdd` repo as the migration's planning home; the v1 *code* lands in the `speckit-companion` repo.)

## Requirements

### Foundation & home

- **R001** (MUST): the spec-kit extension lives in the `speckit-companion` repo under `speckit-extension/` (monorepo beside the VS Code extension). Extension `id` is `companion`, so all commands are `/speckit.companion.<cmd>`.
- **R002** (MUST): ship an `extension.yml` valid against spec-kit's extension schema — `id: companion`, namespaced commands, lifecycle-hook registrations. Declare version floors in `requires.speckit_version`: `>=0.8.5` (workflow `integration: auto`) and the release that wired `after_specify`/`after_plan` hooks.
- **R003** (MUST): `.spec-context.json` stays at `specs/<NNN>-<slug>/.spec-context.json` — no path change, no migration. Active-feature-dir resolution follows spec-kit's order (`SPECIFY_FEATURE_DIRECTORY` env → `.specify/feature.json` → branch-name prefix), not "most-recently-modified dir containing `tasks.md`."

### Canonical schema (owned in the Companion repo)

- **R004** (MUST): the Companion repo's `spec-context.schema.json` is the single canonical schema; the extension reads/writes it directly — no vendoring, no cross-repo reconciliation.
- **R005** (MUST): extend the canonical schema backward-compatibly to cover every field the extension writes — `currentStep`, `status`, `transitions[].by` (incl. `extension`/`cli`/`ai`), `stepHistory`, plus SDD-carried fields (`type`, `step_summaries`, …) — preserving unknown-field tolerance.
- **R006** (MUST): the extension never emits the legacy `currentStep: "done"`; terminal state is expressed as `status: implemented|completed`. Step values stay within the Companion's set (`specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`).
- **R007** (SHOULD): the legacy SDD plugin (`sdd` repo) is updated to the canonical enums (drop `done`, adopt the `status` vocabulary, widen `transitions[].by`) and `docs/STATE.md`'s status-enum contradiction is fixed, so plugin output also renders correctly during the transition. Transition polish — **not a v1 blocker**.

### Hook-driven activity capture

- **R008** (MUST): register lifecycle hooks (`after_specify`, `after_plan`, `after_tasks`, `after_implement`) whose command-markdown instructs the agent to run a script that writes/updates `.spec-context.json` (append-only `transitions`, atomic temp-then-rename write, unknown-field preservation).
- **R009** (MUST): capture is best-effort and agent-mediated; a **derive-from-files** path reconstructs `currentStep`/`status` from the artifacts present (`spec.md`/`plan.md`/`tasks.md` + checklist + git) when hooks did not fire. First-class path, not a gap-filler.
- **R010** (SHOULD): the writer preserves Companion-owned fields (e.g. `reviewComments`) via read-then-merge, never clobbering unknown top-level keys.

### Status + resume commands

- **R011** (MUST): `/speckit.companion.status` reads state and prints a pipeline view (features × stage, task completion); supports `--json` for tooling.
- **R012** (MUST): `/speckit.companion.resume` detects the current phase from state (or the derived fallback) and suggests the next step.

### Constraints carried from ADR 0003

- **R013** (MUST): `.sdd.json` remains SDD's own config (hooks/branch/domains); spec-kit's `extensions.yml` carries only the thin hook registrations that trigger our scripts — SDD's `shell`/`skill`/blocking hook model has no host equivalent.
- **R014** (MUST): branch creation defers to spec-kit's bundled `git` extension when present (avoid double-branching); the extension retains only the main-branch push guard.
- **R015** (SHOULD): two publish targets from the one repo (VS Code Marketplace + spec-kit catalog), path-filtered and versioned independently; document `--ai-skills` non-overwrite-on-update (installed `SKILL.md` files need `--force`/re-init to upgrade).

## Scenarios

### Companion lights up on an existing spec-kit flow

**When** a user with the extension installed runs their normal spec-kit `specify`/`plan` on Claude Code
**Then** `.spec-context.json` is written with the canonical schema, and the Companion GUI renders the correct step and status with no code change on its side.

### A shipped spec renders correctly (the bug this fixes)

**When** a spec reaches its terminal state
**Then** `status` is `implemented`/`completed` (never the legacy `currentStep: "done"`), and the Companion shows it as done rather than silently coercing it back to an earlier step.

### Hooks didn't fire — fallback keeps the view honest

**When** work happened outside spec-kit commands, or the agent skipped the hook prompt
**Then** `/speckit.companion.status` derives `currentStep`/`status` from the artifacts on disk + git, so the view is still correct (best-effort, never silently wrong).

### Resume after interruption

**When** a session stops mid-pipeline
**Then** `/speckit.companion.resume` reads state (or the derived fallback) and points to the exact next step.

### Legacy SDD repo, no migration

**When** the extension reads an existing SDD `.spec-context.json` carrying legacy `active`/`done`
**Then** it is accepted as-is and normalized to canonical values only on the next write — no migration step, no breakage.

## Non-Functional Requirements

- **NFR001** (MUST): writes to `.spec-context.json` are atomic (temp + rename) and `transitions` are append-only (never rewritten or shrunk), matching the Companion's write contract.
- **NFR002** (SHOULD): the extension is agent-agnostic; Claude-only assets ship via install-time emission (`--ai-skills`) and never break non-Claude installs.
- **NFR003** (SHOULD): schema changes ship docs-forward in the same change (the canonical schema + any STATE.md/pointer updates), per the Docs Sync Rule.

## Out of Scope

Deferred to later phases (noted, not built here):
- Our own pipeline commands (`/speckit.companion.specify|plan|tasks|implement`) and the `sdd-lean` **preset** template pack.
- Complexity detector / simple-fix fast path.
- Living specs + drift (the differentiator) ported to the extension.
- Auto-mode `workflow.yml` riding spec-kit's workflow engine.
- Agent-team (`[P]`) parallel sub-agent execution.
- Any change to the SpecKit Companion GUI beyond the canonical-schema extensions in R004–R006.
