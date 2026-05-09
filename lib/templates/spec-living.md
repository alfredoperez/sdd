# {Domain} Specification

**Domain:** `{domain}` · **Last updated:** {TODAY}

> Living spec for the `{domain}` capability. The current truth — what this domain does *today*.
> Per-feature deltas land in `specs/{NNN}-{slug}/spec.md` and merge into this file at CP3 of `/sdd:implement`.

## Purpose

[1–2 sentences: what this capability is responsible for in the system.]

## Capabilities

- [Short, name-able capability — e.g., "Username + password login"]
- [Capability]
- [Capability]

## Requirements

### R001: [Requirement Name]

[Statement — what the system MUST do.]

**Acceptance:**
- Scenario: [name]
  - Given [precondition]
  - When [action]
  - Then [expected result]

### R002: [Requirement Name]

[Statement.]

**Acceptance:**
- Scenario: [name]
  - Given …
  - When …
  - Then …

## Out of scope

- [Things this domain does NOT do — links to where they live instead.]

## Related

- ADRs: [`.sdd/decisions/NNNN-<slug>.md`](../../.sdd/decisions/) — relevant architectural decisions
- Specs: [`specs/{NNN}-{slug}/`](../../specs/) — per-feature deltas that shaped this spec
