---
name: sdd:tasks
description: "SDD — Spec-Driven Development: generate a lean phased task list."
---

## Steps

### 1. Load Context

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains both `spec.md` and `plan.md`.

Read in parallel:
- `specs/{NNN}-{slug}/spec.md` — feature name, requirements, scenarios
- `specs/{NNN}-{slug}/plan.md` — approach, files to create/modify
- `specs/{NNN}-{slug}/.spec-context.json` — current step/task (if exists)

If no spec/plan found, stop: "Run `/sdd:specify` and `/sdd:plan` first."

Update `specs/{NNN}-{slug}/.spec-context.json`:

```json
{ "step": "tasks", "task": null, "substep": "loading", "next": null, "updated": "{TODAY}" }
```

---

### 2. Write `specs/{NNN}-{slug}/tasks.md`

Update `specs/{NNN}-{slug}/.spec-context.json` — set `substep` to `"writing-tasks"`.

Read `lib/templates/tasks.md`, fill placeholders (`{Feature Name}`, `{TODAY}`), generate tasks based on the plan's file list, and write to `specs/{NNN}-{slug}/tasks.md`.

**Phase rules:**
- Phase 1: all core implementation tasks in dependency order (T001, T002, ...) — always sequential
- Phase 2: always include unit tests; only include a docs task if plan.md explicitly flagged docs work
- Omit Phase 2 entirely for trivial single-file changes
- Use `[P][A]` markers only in Phase 2
- The name in backticks after `—` in Phase 2 tasks is the **agent identifier** that `/sdd:implement` spawns (e.g., `` `test-expert` ``, `` `docs-expert` ``, `` `security-expert` ``)

**Skip**: dependency graphs, user story labels ([US1] etc.), parallel execution analysis, formal validation steps.

---

### 3. Summary

Update `specs/{NNN}-{slug}/.spec-context.json` — set `substep` to `null` and `next` to `"implement"`.

Read `auto` from `specs/{NNN}-{slug}/.spec-context.json`. If `auto` is `true`, use the **(auto)** variant. Otherwise use the **(manual)** variant.

**Manual** — display exactly this format:

```
📝 **Tasks ready**

{Feature Name} — {N} tasks to implement

{T001}: {title}
{T002}: {title}
{T003}: {title}
...

📂 `specs/{NNN}-{slug}/tasks.md`

👉 Run `/sdd:implement {NNN}-{slug}` to start building
```

**Auto** — display exactly this format:

```
📝 **Tasks ready**

{Feature Name} — {N} tasks to implement

{T001}: {title}
{T002}: {title}
{T003}: {title}
...

📂 `specs/{NNN}-{slug}/tasks.md`

🔄 Auto mode — continuing...
```
