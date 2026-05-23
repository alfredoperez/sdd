# Spec: Init Adoption Wizard

**Slug**: 023-init-adoption-wizard | **Date**: 2026-05-23

## Summary

Extend `/sdd:init` from a static Layer-0 scaffold into a friendly, incremental, idempotent **brownfield-adoption wizard**. Today adopting SDD on an existing repo means hand-writing every `.specs/<domain>/spec.md`; neither `/sdd:init` (scaffold only) nor `/sdd:drift` (a checker) can bootstrap living specs. This adds a guided flow that analyzes **one area at a time**, proposes a tree of domains for the user to confirm, AI-drafts the requirements tier from the code surface, and appends the result to the `.sdd.json` registry. It builds directly on the PR1 resolver (`lib/scripts/resolve-spec-paths.py`) and the decisions in ADR 0002 (§9 incremental adoption, §12 surface-first extraction, §11 include/exclude, §7 tiered files).

## Requirements

- **R001** (MUST): `/sdd:init` keeps its existing Phase 1 scaffold (create `.sdd.json`, `.sdd/principles.md`, `.sdd/decisions/` when absent) and stays idempotent — it never overwrites existing files.
- **R002** (SHOULD): During Phase 1, when `.sdd/principles.md` is absent, offer (via `AskUserQuestion`) either the blank template **or** AI-inferred principles — a subagent reads lint/test/build config + `CLAUDE.md` + folder conventions and drafts candidate project MUSTs for the user to confirm before writing.
- **R003** (MUST): Phase 2 (adoption) is **incremental — one area at a time, never whole-repo**. The user picks a single area (or types a path); only that subtree is analyzed.
- **R004** (MUST): Phase 2 begins with a **cheap survey** — read framework manifests (`package.json`, `nx.json`, `angular.json`, etc.) + top-level folders to propose a short list of candidate areas. No deep code reading happens before the user chooses.
- **R005** (MUST): For the chosen area, a subagent proposes a **tree of domains** (parent + leaves), each with `name`, `pattern` (or `include`/`exclude` globs when code is scattered), `location` (`centralized`|`colocated`), `specPath`, and `specFormat`. The proposal is confirmed/edited/dropped per node via `AskUserQuestion`.
- **R006** (MUST): Requirements are drafted **surface-first** (exports, routes, component props, types, signatures), going one level into behavior only for primary files; per-leaf extraction runs as **parallel, token-capped subagents**.
- **R007** (MUST): Every drafted spec is honest: marked `[DRAFT]` overall, each requirement tagged *observed* vs *inferred*, low-confidence items marked `[NEEDS CLARIFICATION: …]`, and unreadable/skipped files listed under `## Uncovered`.
- **R008** (MUST): Only the **`.spec.md` (requirements) tier** is created. `.arch.md` / `.coverage.md` are reserved and NOT generated.
- **R009** (MUST): The wizard resolves every spec path through `lib/scripts/resolve-spec-paths.py` (never hardcodes `.specs/<domain>/spec.md`) and appends confirmed domains to the `.sdd.json` `domains` registry.
- **R010** (MUST): Phase 2 is **idempotent** — skip domains already in the registry, and never overwrite a spec that lacks the `[DRAFT]` marker (i.e., one a human has reviewed/edited).
- **R011** (MUST): When `/sdd:init` runs on an already-initialized project, it skips Phase 1 and goes straight to Phase 2 ("adopt another area").
- **R012** (SHOULD): Phase 3 summarizes created files, flags that drafts need review, and points to next steps (`/sdd:drift` is now meaningful; adopt more areas later).
- **R013** (MUST): Docs are synced in the same change (`CLAUDE.md` `/sdd:init` description, `README.md`, `docs/CONFIGURATION.md` if needed) and the plugin version + CHANGELOG are bumped.

## Scenarios

### First-time adoption

**When** a dev runs `/sdd:init` in a brownfield repo and picks the `checkout` area
**Then** the wizard surveys, proposes a domain tree, drafts `[DRAFT]` requirement specs from the code surface, writes them at their resolved paths, and registers the domains in `.sdd.json`

### Always skippable

**When** the dev declines Phase 2 (or any sub-prompt)
**Then** `/sdd:init` finishes after the scaffold without analyzing any code — adoption is never forced

### Re-run adds, never clobbers

**When** the dev runs `/sdd:init` again after reviewing/editing a generated spec (removing its `[DRAFT]` marker)
**Then** that spec is left untouched; only new, unregistered areas/domains are added

### Honest drafts

**When** the extractor can't confidently infer a behavior from a function body
**Then** the requirement is tagged *inferred* or marked `[NEEDS CLARIFICATION]`, and unreadable files appear under `## Uncovered` — never silently fabricated

### Already initialized

**When** `/sdd:init` runs and `.sdd.json` + `.sdd/` already exist
**Then** Phase 1 is skipped and the wizard opens directly at Phase 2 (adopt another area)

## Out of Scope

- **Whole-repo adoption** in one pass (deliberately — incremental only).
- Generating `.arch.md` / `.coverage.md` tiers, and consuming them (separate spec).
- Auto-migrating existing centralized specs to colocated paths.
- The standalone `/sdd:grill` interview skill (separate candidate; this wizard only *drafts*, it doesn't interrogate).
