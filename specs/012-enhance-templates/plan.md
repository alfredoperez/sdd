# Plan: Enhance Templates

<!-- Template variables: {Feature Name}, {TODAY}, {NNN}, {slug}, {NNN}-{slug} -->

**Spec**: [spec.md](./spec.md) | **Date**: 2026-03-29

## Approach

Direct modification of 4 existing template files under `lib/templates/`. Each template gets targeted additions (new sections, new fields) and formatting changes (tables to lists). No new files, no logic changes, no dependency updates -- pure template content changes that improve the quality of every future generated artifact.

## Technical Context

**Stack**: Markdown templates with `{variable}` placeholders
**Key Dependencies**: None -- templates are static markdown consumed by SDD skills
**Constraints**: Templates must remain valid markdown; optional sections use HTML comments to guide agents on when to omit

## Files

### Modify

- `lib/templates/spec-normal.md` -- Add NFR section between Scenarios and Out of Scope; add MAY priority example to Requirements (R001, R002)
- `lib/templates/plan.md` -- Rename Flow to Architecture, lower threshold to 3+ components, add Testing Strategy section, convert Files and Data Model from tables to lists (R003, R004, R005)
- `lib/templates/tasks.md` -- Add `| R001` requirement refs on task headers, add Leverage field, convert Progress from table to list (R006, R007, R008)
- `lib/templates/README.md` -- Document new sections (NFR, Testing Strategy, Leverage), updated section names (Architecture), and formatting changes (R009)

## Testing Strategy

- **Manual**: Run `/sdd:specify` on a test feature and verify NFR section appears in generated spec
- **Manual**: Run `/sdd:plan` and verify Architecture heading (not Flow) and Testing Strategy section
- **Manual**: Run `/sdd:tasks` and verify `| R001` refs and Leverage field on task headers
- **Visual**: Confirm all tables are replaced with lists in plan.md and tasks.md templates

## Risks

- Existing specs in `specs/` use the old template format -- not a concern, they are already generated and won't be regenerated
