# Tasks: Add Transition Logging

**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Date**: 2026-04-09

## Phase 1 — Core Implementation

### T001: Create shared transition-logging instruction snippet ✅

**File**: `lib/instructions/transition-logging.md` (create)

- Define the transition entry schema: `step`, `substep`, `from`, `by`, `at`
- Document the read-before-write rule: capture previous `currentStep`/`progress` before updating
- Document the append-only rule: never truncate or rewrite `transitions`
- Document the first-write case: `from: null` when `.spec-context.json` is being created
- Keep concise — this is referenced inline by all skill prompts

### T002: Add transition logging to specify skill ✅

**File**: `skills/specify/SKILL.md` (modify)

- Add reference to `lib/instructions/transition-logging.md`
- Update `.spec-context.json` creation step to initialize `transitions` array with first entry (`from: null`)
- Update any subsequent `.spec-context.json` writes to append transitions

### T003: Add transition logging to plan skill ✅

**File**: `skills/plan/SKILL.md` (modify)

- Add reference to `lib/instructions/transition-logging.md`
- Update all `.spec-context.json` write steps to read previous state and append transition entry

### T004: Add transition logging to tasks skill ✅

**File**: `skills/tasks/SKILL.md` (modify)

- Add reference to `lib/instructions/transition-logging.md`
- Update all `.spec-context.json` write steps to read previous state and append transition entry

### T005: Add transition logging to implement skill ✅

**File**: `skills/implement/SKILL.md` (modify)

- Add reference to `lib/instructions/transition-logging.md`
- Audit all `.spec-context.json` write sites (per-task updates, checkpoint updates, completion)
- Update each write site to read previous state and append transition entry

### T006: Add transition logging to auto skill ✅

**File**: `skills/auto/SKILL.md` (modify)

- Add reference to `lib/instructions/transition-logging.md`
- Update all `.spec-context.json` write steps to read previous state and append transition entry

### T007: Add transition logging to pause skill ✅

**File**: `skills/pause/SKILL.md` (modify)

- Add reference to `lib/instructions/transition-logging.md`
- Update `.spec-context.json` write step to read previous state and append transition entry

### T008: Add transition logging to resume skill ✅

**File**: `skills/resume/SKILL.md` (modify)

- Add reference to `lib/instructions/transition-logging.md`
- Update `.spec-context.json` write step to read previous state and append transition entry

## Phase 2 — Validation

### T009: Unit tests `[P][A]` — `test-expert`

- Verify transition entry schema matches spec (all 5 fields present)
- Verify first-write produces `from: null`
- Verify subsequent writes capture correct previous state in `from`
- Verify append-only behavior (existing entries preserved)
- Verify all 7 skill SKILL.md files reference the shared snippet
