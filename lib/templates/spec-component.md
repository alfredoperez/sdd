# {Domain} Specification

**Domain:** `{domain}` · **Last updated:** {TODAY}

> Living spec for the `{domain}` component. The current truth — what this component does *today*.
> Per-feature deltas land in `specs/{NNN}-{slug}/spec.md` and merge into this file at CP3 of `/sdd:implement`.

## Purpose

[1–2 sentences: what this component is and what it's responsible for in the UI.]

## Capabilities

- [Short, name-able capability — e.g., "Renders a list of selectable options"]
- [Capability]
- [Capability]

## Props

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `[propName]` | `[type]` | yes/no | `[default]` | [What it controls.] |
| `[propName]` | `[type]` | yes/no | `[default]` | [What it controls.] |

## States

- **default** — [appearance/behavior in the resting state.]
- **loading** — [what the user sees while data is pending.]
- **empty** — [what renders when there's no data.]
- **error** — [how failures are surfaced.]
- **disabled** — [non-interactive appearance/behavior.]

## Interactions

- [User action] → [outcome.]
- [User action] → [outcome.]
- [User action] → [outcome.]

## Requirements

### R001: [Requirement Name]

[Statement — what the component MUST do.]

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

- [Things this component does NOT do — links to where they live instead.]

## Related

- ADRs: [`.sdd/decisions/NNNN-<slug>.md`](../../.sdd/decisions/) — relevant architectural decisions
- Specs: [`specs/{NNN}-{slug}/`](../../specs/) — per-feature deltas that shaped this spec
