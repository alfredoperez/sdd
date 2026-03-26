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

## Authoring New Templates

1. Use only the canonical variables listed above.
2. Wrap variable names in curly braces exactly as shown (case-sensitive).
3. Add the HTML comment header at the top of the file (after the title line) listing the variables the template uses. Copy the header from any existing template.
4. Register the new template and its variables in the table above.
