# Plan: Decouple Templates from Skills

**Spec**: [spec.md](./spec.md) | **Date**: 2026-03-26

## Approach

Remove inline template markdown from SKILL.md files and replace with instructions to load from `lib/templates/`. Each skill step that writes an artifact will say "Read `lib/templates/{name}.md`, fill placeholders, write to `specs/{slug}/{name}.md`" instead of embedding the full template.

## Technical Context

**Stack**: Markdown skill definitions, markdown templates
**Constraints**: No runtime template engine — Claude reads the file and fills placeholders contextually

## Flow

```mermaid
graph LR
    S[Skill SKILL.md] -->|"reads"| T[lib/templates/*.md]
    T -->|"fills placeholders"| O[specs/slug/*.md]
```

## Files

### Create

_None_

### Modify

| File | Change |
|------|--------|
| `skills/specify/SKILL.md` | Step 5: replace inline spec template with "Load `lib/templates/spec-normal.md`, fill placeholders". Step 6 minimal: replace inline plan+tasks templates with references to `lib/templates/plan.md` and `lib/templates/tasks.md` |
| `skills/plan/SKILL.md` | Step 2: replace inline plan template with "Load `lib/templates/plan.md`, fill placeholders" |
| `skills/tasks/SKILL.md` | Step 2: replace inline tasks template with "Load `lib/templates/tasks.md`, fill placeholders" |
| `lib/templates/spec-normal.md` | Ensure it matches the current inline template in specify (sync any drift) |
| `lib/templates/spec-minimal.md` | Ensure it matches the minimal-mode inline template in specify |

## Risks

- Templates and skills may have drifted apart. Mitigation: diff inline vs file versions before changing, use file version as source of truth.
