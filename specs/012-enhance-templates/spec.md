# Spec: Enhance Templates

<!-- Template variables: {Feature Name}, {TODAY}, {NNN}, {slug}, {NNN}-{slug} -->

**Slug**: 012-enhance-templates | **Date**: 2026-03-29

## Summary

Enhance SDD templates to improve output quality for every generated artifact. Adds non-functional requirements to spec-normal.md, testing strategy and list-based formatting to plan.md, and leverage annotations with requirement traceability to tasks.md. These are multiplicative improvements -- every spec, plan, and task file generated from this point forward benefits.

## Requirements

- **R001** (MUST): spec-normal.md includes a Non-Functional Requirements section between Scenarios and Out of Scope, with NFR001-prefixed items and category hints (Performance, Security, Reliability, Accessibility, Observability)
- **R002** (MUST): spec-normal.md Requirements section includes a MAY priority example alongside existing MUST/SHOULD
- **R003** (MUST): plan.md renames Flow section to Architecture and lowers threshold from "4+ files" to "3+ components or non-obvious data flow"
- **R004** (MUST): plan.md includes a Testing Strategy section with Unit/Integration/Edge cases guidance
- **R005** (MUST): plan.md Files and Data Model sections use lists instead of tables
- **R006** (MUST): tasks.md task headers include requirement traceability refs (e.g., `| R001, R002`)
- **R007** (MUST): tasks.md includes an optional Leverage field pointing to existing code patterns
- **R008** (MUST): tasks.md Progress section uses a list instead of a table
- **R009** (SHOULD): README.md documents all template changes and any new variables or sections

## Scenarios

### Generating a spec with NFRs

**When** `/sdd:specify` generates a spec-normal for a feature with performance constraints
**Then** the NFR section appears between Scenarios and Out of Scope with NFR001-prefixed items

### Generating a spec without NFRs

**When** `/sdd:specify` generates a spec-normal for a simple feature with no operational concerns
**Then** the NFR section is omitted entirely (guided by the template comment)

### Generating a plan with testing strategy

**When** `/sdd:plan` generates a plan for a non-trivial feature
**Then** the plan includes an Architecture section (not Flow) and a Testing Strategy section with unit/integration/edge case guidance

### Generating tasks with leverage annotations

**When** `/sdd:tasks` generates tasks for brownfield work modifying existing code
**Then** relevant tasks include a Leverage field pointing to existing files with pattern descriptions

### Requirement traceability in tasks

**When** `/sdd:tasks` generates task headers
**Then** each task header includes `| R001, R002` refs linking back to spec requirements

## Out of Scope

- Delta spec template (ADDED/MODIFIED/REMOVED format) -- deferred to future work
- spec-minimal.md table-to-list conversion
- New design.md template (Phase 3)
- Living spec sync or component-level spec formats
