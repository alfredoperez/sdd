# {Domain} Specification

**Domain:** `{domain}` · **Last updated:** {TODAY}

> Living spec for the `{domain}` API. The current truth — what these endpoints do *today*.
> Per-feature deltas land in `specs/{NNN}-{slug}/spec.md` and merge into this file at CP3 of `/sdd:implement`.

## Purpose

[1–2 sentences: what this API surface is responsible for in the system.]

## Capabilities

- [Short, name-able capability — e.g., "Create and list users"]
- [Capability]
- [Capability]

## Routes

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/{resource}` | [List {resources}] |
| POST | `/api/{resource}` | [Create a {resource}] |
| GET | `/api/{resource}/{id}` | [Fetch one {resource}] |

## Request

- **Path params:** [`{id}` — the {resource} identifier]
- **Query params:** [`?limit`, `?cursor` — pagination, etc.]
- **Body shape:** [JSON fields and types — e.g., `{ "email": string, "name": string }`]
- **Auth:** [Required scope / token type — e.g., "Bearer token, `users:write` scope"]

## Response

- **Success:** [Status code + body shape — e.g., `200 OK` → `{ "id": string, "email": string }`]
- **Created:** [`201 Created` → resource representation]
- **No content:** [`204 No Content` for deletes, etc.]

## Errors

| Status | Code | Meaning |
|--------|------|---------|
| 400 | `bad_request` | [Malformed or missing required fields] |
| 401 | `unauthorized` | [Missing or invalid credentials] |
| 404 | `not_found` | [{Resource} does not exist] |
| 409 | `conflict` | [e.g., Duplicate email] |

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

- [Things this API does NOT do — links to where they live instead.]

## Related

- ADRs: [`.sdd/decisions/NNNN-<slug>.md`](../../.sdd/decisions/) — relevant architectural decisions
- Specs: [`specs/{NNN}-{slug}/`](../../specs/) — per-feature deltas that shaped this spec
