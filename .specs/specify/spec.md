# Specify Specification

**Domain:** `specify` · **Last updated:** 2026-05-03

> Living spec for the `/sdd:specify` skill. Current truth — what specify does today.

## Purpose

`/sdd:specify` turns a one-line feature description into the structured starting point of the SDD pipeline: a slug, a numbered spec directory, an initial `.spec-context.json`, and `spec.md`. Detects complexity (minimal vs normal) and on the minimal fast-path also writes `plan.md` + `tasks.md` in one shot.

## Capabilities

- Slug generation (2–4 words, action-noun, kebab-case; preserves OAuth2 / JWT / API)
- Conventional-commit type inference (`feat` / `fix` / `refactor` / `docs` / `chore`)
- Spec numbering (highest existing N+1, zero-padded to 3)
- Spec directory + `.spec-context.json` initialisation (with `transitions` seed)
- Optional branch creation via `branchStage = "specify"` (delegates to `branch-creation.md`)
- Inline exploration (parallel Glob/Grep + 2–3 file reads)
- Layer 1 loading (Step 3b) — domain detection per `layered-context.md`, records `loadedDomains`, prepends `## Modified Capabilities` callout when matches found
- Complexity detection (file count, line count, public-API signals)
- `spec.md` write from `lib/templates/spec-normal.md`
- Minimal mode: also writes `plan.md` + `tasks.md` in Step 6
- Auto-mode and manual-mode summary footers

## Requirements

### R001: Generate a stable slug from a free-text description

The skill MUST produce a slug that is 2–4 words, lowercase, hyphen-separated, action-noun in shape, and that preserves common technical terms (OAuth2, JWT, API, GraphQL, etc.) verbatim.

### R002: Allocate a sequential, zero-padded spec number

The skill MUST scan `specs/` for directories matching `[0-9]+-*`, find the highest numeric prefix, and use `N+1` zero-padded to 3 digits as the new spec number. If no spec dirs exist, start at 1.

### R003: Initialise `.spec-context.json` with a transition seed

On creation, `specs/{NNN}-{slug}/.spec-context.json` MUST contain `workflow`, `currentStep: "specify"`, `progress: "parsing"`, `selectedAt`, `specName`, `branch`, `type`, `createdAt`, and a `transitions` array seeded with one entry whose `from: null` (per `transition-logging.md`).

### R004: Load Layer 1 specs when a domain matches

After exploration (Step 3) and before complexity detection (Step 4), the skill MUST run the domain-detection precedence from `layered-context.md` against the files surfaced during exploration. Matching `.specs/<domain>/spec.md` files are loaded; their names are recorded in `.spec-context.json#loadedDomains`. When at least one domain matches, `spec.md` MUST include a `## Modified Capabilities` callout immediately after the Summary section.

### R005: Detect complexity and select fast-path when warranted

The skill MUST classify the change as `minimal` or `normal` per the published thresholds. In `minimal` mode it MUST also write `plan.md` and `tasks.md` from their templates (omitting Phase 2 from tasks) so the user can jump straight to `/sdd:implement`.

### R006: Surface a footer matching the auto/manual + minimal/normal matrix

The Step 7 summary MUST select one of four exact formats (minimal-manual, minimal-auto, normal-manual, normal-auto) based on detected complexity and `auto` flag in `.spec-context.json`.

## Out of scope

- Spec review / approval gating (handled by `/sdd:auto` orchestrator).
- Plan / task generation in normal mode (handled by `/sdd:plan`, `/sdd:tasks`).
- Layer 1 mutation (handled by `/sdd:implement` Step 7b).

## Related

- ADRs: [`.sdd/decisions/0001-layered-context-loading.md`](../../.sdd/decisions/0001-layered-context-loading.md)
- Skill: [`skills/specify/SKILL.md`](../../skills/specify/SKILL.md)
- Templates: [`lib/templates/spec-normal.md`](../../lib/templates/spec-normal.md), [`lib/templates/spec-minimal.md`](../../lib/templates/spec-minimal.md)
