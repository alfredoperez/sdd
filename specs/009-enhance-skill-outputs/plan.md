# Plan: Enhance Skill Outputs

**Spec**: [spec.md](./spec.md) | **Date**: 2026-03-26

## Approach

Redesign the "Display exactly this format" blocks in all 5 skill SKILL.md files. Add emojis as visual anchors with a consistent vocabulary, improve structure with markdown headers and sections, and add contextual info (mode badge, file counts). The emoji vocabulary is defined once and reused everywhere.

## Technical Context

**Stack**: Markdown skill definitions — output is rendered by Claude Code's terminal markdown
**Constraints**: No ANSI codes. Emojis render in Claude Code terminal. Markdown tables and headers work.

## Emoji Vocabulary

| Emoji | Meaning | Used in |
|-------|---------|---------|
| 📋 | Spec/specify | specify summary, status |
| 📐 | Plan | plan summary, status |
| 📝 | Tasks | tasks summary, status |
| 🚀 | Implement/ship | implement summary, status |
| ⚡ | Fast path/minimal | specify minimal summary |
| 🔍 | Code review | CP1 |
| 🧪 | Test results | CP2 |
| 💾 | Commit & PR | CP3 |
| ✅ | Done/complete | implement done, task checkmarks |
| 📂 | File reference | file paths in summaries |
| 👉 | Next step | all summaries |
| ⚠️ | Silent fix/warning | CP1 silent fixes |
| 🔄 | Resuming | context recovery |

## Files

### Modify

| File | Change |
|------|--------|
| `skills/specify/SKILL.md` | Redesign Step 7 summary (both minimal and normal modes) |
| `skills/plan/SKILL.md` | Redesign Step 3 summary |
| `skills/tasks/SKILL.md` | Redesign Step 3 summary |
| `skills/implement/SKILL.md` | Redesign CP1, CP2, CP3 outputs + Step 9 done summary |
| `skills/status/SKILL.md` | Add emoji indicators per step in dashboard table |
