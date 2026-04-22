---
name: sdd:tasks
description: "SDD — Spec-Driven Development: generate a lean phased task list."
---

## Shared Instructions

- [Transition Logging](../../lib/instructions/transition-logging.md) — append a transition entry on every `.spec-context.json` write

## Steps

### 1. Load Context

If `$ARGUMENTS` is provided, use `specs/{$ARGUMENTS}/` as the target directory.
Otherwise, find the most recently modified directory under `specs/` that contains both `spec.md` and `plan.md`.

Read in parallel:
- `specs/{NNN}-{slug}/spec.md` — feature name, requirements, scenarios
- `specs/{NNN}-{slug}/plan.md` — approach, files to create/modify
- `specs/{NNN}-{slug}/.spec-context.json` — current step/task (if exists)

If no spec/plan found, stop: "Run `/sdd:specify` and `/sdd:plan` first."

Update `specs/{NNN}-{slug}/.spec-context.json` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md):

```json
{ "currentStep": "tasks", "currentTask": null, "progress": "loading", "next": "implement", "updated": "{TODAY}" }
```

---

### 2. Write `specs/{NNN}-{slug}/tasks.md`

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `"writing-tasks"` and append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).

Read `lib/templates/tasks.md`, fill placeholders (`{Feature Name}`, `{TODAY}`), generate tasks based on the plan's file list, and write to `specs/{NNN}-{slug}/tasks.md`.

**Phase rules:**
- Phase 1: all core implementation tasks ordered by dependency (T001, T002, ...).
- Mark a task `[P]` when it (a) touches files that no other task in its parallel group touches AND (b) has no data dependency on its siblings in the group. Two tasks that modify the same file are never both `[P]`.
- Consecutive `[P]` tasks form a parallel group that `/sdd:implement` runs as a batch of concurrent subagents. A task without `[P]` acts as a gate — it waits for everything above it.
- When unsure, omit `[P]`. Sequential is always safe.

**Skip**: dependency graphs, user story labels ([US1] etc.), formal validation steps.

---

### 3. Summary

Update `specs/{NNN}-{slug}/.spec-context.json` — set `progress` to `null` and `next` to `"implement"`. Append a transition entry per [transition-logging](../../lib/instructions/transition-logging.md).

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

---

### 4. Auto Self-Chain

**Only runs when `auto` is `true`.** Skip entirely in manual mode.

After displaying the Auto summary above, invoke `/sdd:resume {NNN}-{slug}` via the **Skill** tool. This makes the "continuing..." footer real when `/sdd:tasks` is invoked directly (outside the `/sdd:auto` orchestrator loop) on a spec that has `auto: true`.

Safe under nesting: when `/sdd:auto` invokes `/sdd:tasks`, this self-chain fires first and advances to `/sdd:implement`; when control returns to `/sdd:auto`'s loop, `/sdd:resume` is idempotent — it reads `currentStep` from `.spec-context.json` and no-ops or resumes as appropriate.
