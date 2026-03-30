# Template Variables

Canonical variable set used across all SDD templates.

## Variables

| Variable | Format | Description |
|----------|--------|-------------|
| `{Feature Name}` | Title case, spaces allowed | Feature title from the spec |
| `{TODAY}` | `YYYY-MM-DD` | Current date when the file is generated |
| `{NNN}` | Zero-padded 3 digits (`001`, `002`) | Spec sequence number |
| `{slug}` | Lowercase, hyphen-separated | Short identifier for the spec |
| `{NNN}-{slug}` | Combined (`007-template-variables`) | Full spec directory name |

## Template Usage

| Template | Variables Used |
|----------|---------------|
| `spec-normal.md` | `{Feature Name}`, `{NNN}-{slug}`, `{TODAY}` |
| `spec-minimal.md` | `{Feature Name}`, `{NNN}-{slug}`, `{TODAY}` |
| `plan.md` | `{Feature Name}`, `{TODAY}` |
| `tasks.md` | `{Feature Name}`, `{TODAY}` |

## Template Sections

### spec-normal.md

- **Requirements** — MUST/SHOULD/MAY priority levels with R001-prefixed IDs
- **Scenarios** — When/Then behavioral specifications
- **Non-Functional Requirements** — Optional section for performance, security, reliability, accessibility, observability constraints. Uses NFR001 prefix. Omit entirely if no NFRs apply.
- **Out of Scope** — Explicit exclusions

### plan.md

- **Approach** — Key architectural decision and reasoning
- **Technical Context** — Stack, dependencies, constraints
- **Architecture** — Mermaid diagram for 3+ components or non-obvious data flow (formerly "Flow")
- **Files** — Create/Modify lists (list format, not tables)
- **Data Model** — Entity definitions (list format, not tables)
- **Testing Strategy** — Optional section for unit/integration/edge case testing guidance. Omit for trivial changes.
- **Risks** — Non-obvious risks and mitigations

### tasks.md

- **Phase 1 tasks** — Sequential core implementation with requirement traceability (`| R001, R002` refs on headers)
- **Leverage field** — Optional per-task pointer to existing code patterns (e.g., `**Leverage**: path/to/file ([what to reuse])`)
- **Phase 2 tasks** — Parallel agent-eligible quality tasks with `[P][A]` markers
- **Progress** — Phase completion tracking (list format, not table)

## Authoring New Templates

1. Use only the canonical variables listed above.
2. Wrap variable names in curly braces exactly as shown (case-sensitive).
3. Add the HTML comment header at the top of the file (after the title line) listing the variables the template uses. Copy the header from any existing template.
4. Register the new template and its variables in the table above.
