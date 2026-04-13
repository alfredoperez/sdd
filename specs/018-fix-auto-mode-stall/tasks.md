# Tasks: Fix Auto Mode Stall

**Plan**: [plan.md](./plan.md) | **Date**: 2026-04-13

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Set auto flag before specify — `skills/auto/SKILL.md` | R001
  - **Do**: Move Step 2 (Set Auto Flag) before Step 1 (Run Specify). Create `.spec-context.json` with `auto: true` + metadata fields, then invoke specify. Remove the old Step 2.
  - **Verify**: Read the skill and confirm auto flag is set before specify invocation

- [x] **T002** Add explicit loop continuation instructions — `skills/auto/SKILL.md` | R002, R003
  - **Do**: In Step 5 (Auto-Advance Loop), add a bold instruction: "**CRITICAL: Do NOT stop or end your response after a Skill tool invocation returns. You MUST continue executing the loop.**" Also add a note after each Skill invocation point reinforcing continuation.
  - **Verify**: Read the skill and confirm loop has explicit anti-stall instructions

---

## Progress

- Phase 1: T001–T002 [ ]
