# Spec: Standardize Template Variables

**Slug**: 007-template-variables | **Date**: 2026-03-26

## Summary

Define a shared set of template variables used across all templates so placeholders are consistent and documented. Currently different templates use slightly different placeholder formats. Standardize them so templates are truly swappable and self-documenting.

## Requirements

- **R001** (MUST): Define canonical variable set: `{Feature Name}`, `{TODAY}`, `{NNN}`, `{slug}`, `{NNN}-{slug}`
- **R002** (MUST): All templates in `lib/templates/` use the canonical variable syntax
- **R003** (MUST): Document the variable set in a comment block at the top of each template or in a shared reference file
- **R004** (SHOULD): Skills pass the same variable map when filling any template

## Scenarios

### Consistent placeholders

**When** a contributor reads any template in `lib/templates/`
**Then** all placeholders use the same `{Variable Name}` syntax and are documented

### New template creation

**When** someone creates a new template
**Then** they can reference the documented variable set and use the same placeholders

## Out of Scope

- Runtime template engine or variable interpolation code
- Custom user-defined variables
- Conditional template sections
