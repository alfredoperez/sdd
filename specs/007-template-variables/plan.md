# Plan: Standardize Template Variables

**Spec**: [spec.md](./spec.md) | **Date**: 2026-03-26

## Approach

Audit all templates for placeholder usage, define a canonical variable set, add a comment header to each template documenting available variables, and normalize any inconsistencies.

## Technical Context

**Stack**: Markdown templates with `{placeholder}` syntax
**Constraints**: Depends on 006-decouple-templates being done first (templates must be the single source of truth)

## Files

### Create

| File | Purpose |
|------|---------|
| `lib/templates/README.md` | Documents the canonical variable set and template authoring guide |

### Modify

| File | Change |
|------|--------|
| `lib/templates/spec-normal.md` | Add variable comment header, normalize placeholders |
| `lib/templates/spec-minimal.md` | Add variable comment header, normalize placeholders |
| `lib/templates/plan.md` | Add variable comment header, normalize placeholders |
| `lib/templates/tasks.md` | Add variable comment header, normalize placeholders |
