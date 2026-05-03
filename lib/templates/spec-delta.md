# {Feature Name} — Spec Delta

**Spec:** `{NNN}-{slug}` · **Domain(s):** `{domains}` · **Date:** {TODAY}

> Per-feature delta against living spec(s) `.specs/{domain}/spec.md`.
> At CP3 of `/sdd:implement`, the operations below merge into the matching living spec(s):
>
> - **ADDED** → appended to `## Requirements`
> - **MODIFIED** → replace the matching `### R<id>` block in place (matched by R-id)
> - **REMOVED** → delete the matching `### R<id>` block
> - **RENAMED** → update the requirement name on the matching `### R<id>` heading

## Summary

[1-line description of the change at the domain level.]

## Why

[1-2 sentences — the trigger.]

---

## ADDED Requirements

> Requirements introduced by this feature. Omit the section if none.

### R<new-id>: [Requirement Name]

[Statement.]

**Acceptance:**
- Scenario: [name]
  - Given …
  - When …
  - Then …

---

## MODIFIED Requirements

> Existing requirements changed by this feature. Header line: `### R<existing-id>: [New Name (was: Old Name)]`. Omit the section if none.

### R<existing-id>: [Requirement Name]

[Updated statement.]

**Acceptance:**
- Scenario: [updated]
  - Given …
  - When …
  - Then …

---

## REMOVED Requirements

> Requirements deleted by this feature. List by id with one-line reason. Omit the section if none.

- **R<existing-id>** — [why it's removed]

---

## RENAMED Requirements

> Requirement headings being renamed without other changes. Omit the section if none.

- **R<existing-id>**: `[Old Name]` → `[New Name]`

---

## Out of scope

[What this delta deliberately does NOT change.]
