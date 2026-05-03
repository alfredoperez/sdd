# Templates Specification

**Domain:** `templates` · **Last updated:** 2026-05-03

> Living spec for `lib/templates/`. The templates themselves are the artifact; this file captures the contract each template MUST satisfy.

## Purpose

Templates define the *shape* of every artifact SDD produces. Skills decide *whether* to write a section; templates define *what* the section looks like. Per CLAUDE.md's Surface Guide: changes to artifact shape land here, not in skills.

## Capabilities

- Per-feature spec templates (minimal + normal complexity)
- Per-feature plan template
- Per-feature tasks template
- Per-feature README template
- Living spec (Layer 1) template
- Spec delta (Layer 2 operations) template
- Principles starter template
- ADR template

## Requirements

### R001: Use `{placeholder}` syntax for substitutions

Every template MUST mark substitution points with curly-brace placeholders (`{Feature Name}`, `{NNN}`, `{slug}`, `{TODAY}`, `{NNNN}`, `{Title}`, `{deciders}`, `{domain}`). Skills are responsible for substituting them; templates make every placeholder explicit and self-describing.

### R002: Never include empty sections

Templates that contain optional sections (Principles Check, Domain Alignment, Risks, Out of scope, etc.) MUST be written so the producing skill can omit the section entirely when there is nothing to fill it. Skills omit; templates do not leave behind empty headings.

### R003: Spec templates MUST distinguish minimal vs normal

`spec-minimal.md` and `spec-normal.md` are separate files. The minimal template carries the lean fast-path shape (Summary + Requirements + Files); the normal template carries the full shape (Summary + Requirements + Scenarios + Out of scope).

### R004: Living spec template MUST anchor on capability identity

`spec-living.md` MUST include `Domain`, `Last updated`, `Purpose`, `Capabilities`, `Requirements` (numbered `R<id>`), `Out of scope`, and `Related`. The R-id is the merge key for `/sdd:implement` Step 7b sync operations.

### R005: Delta template MUST enumerate all four operations

`spec-delta.md` MUST contain headers for `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements`, `## RENAMED Requirements` so authors know the menu. Each section is independently optional — authors omit the entire section if empty.

### R006: ADR template MUST carry Status, Date, Deciders, and Alternatives Considered

`adr.md` MUST scaffold `Status: Proposed`, `{TODAY}`, `{deciders}` (defaulting to `git config user.name`), and a non-empty `Alternatives Considered` section. The "Considered alternatives" requirement is what makes the ADR useful in retrospect.

## Out of scope

- Skill behavior (lives in `skills/*/SKILL.md`).
- Cross-cutting logic shared by 2+ skills (lives in `lib/instructions/`).
- Project-wide invariants (live in `CLAUDE.md`).

## Related

- Surface Guide: `CLAUDE.md` § Surface Guide
- Templates: [`lib/templates/`](../../lib/templates/)
