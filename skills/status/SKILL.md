---
name: sdd:status
description: "SDD — Spec-Driven Development: show spec states dashboard."
---

## Steps

### 1. Scan Specs

Look for all directories under `specs/` matching `[0-9]+-*`.

For each directory, read `.spec-context.json` if it exists. If `.spec-context.json` is missing, infer state from which files exist:
- Only `spec.md` → step: "specify"
- `spec.md` + `plan.md` → step: "plan"
- `spec.md` + `plan.md` + `tasks.md` → step: "tasks"

Also read `spec.md` first line to extract the feature name (from `# Spec: {name}`).

If no spec directories found, display: "No specs found. Run `/sdd:specify <description>` to create one."

---

### 2. Display Dashboard

Display exactly this format:

```
📊 **SDD Status**

| # | Spec | Step | Updated |
|---|------|------|---------|
| 001 | {Feature Name} | {step} | {date} |
| 002 | {Feature Name} | {step} | {date} |
| ... | ... | ... | ... |

**Total**: {N} specs
```

Step values and their display:
- `specify` → "📋 specify"
- `plan` → "📐 plan"
- `tasks` → "📝 tasks"
- `implement` → "🚀 implement"

If a spec has a `task` value in .spec-context.json, append it: e.g., "🚀 implement (T003)"

If a spec has a non-null `substep` value in .spec-context.json, append it in brackets: e.g., "🚀 implement (T003) [code-review]", "📋 specify [exploring]", "📐 plan [writing-plan]"

If a spec has `"paused": true` in .spec-context.json, prepend "⏸ paused · " to the step display: e.g., "⏸ paused · 🚀 implement (T003)"
