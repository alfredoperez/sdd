# Tasks: Enhance Skill Outputs

**Plan**: [plan.md](./plan.md) | **Date**: 2026-03-26

---

## Phase 1: Core Implementation (Sequential)

- [x] **T001** Redesign specify summary — `skills/specify/SKILL.md`
  - **Do**: Replace Step 7 "Display exactly this format" blocks (both minimal and normal) with new emoji-enhanced formats:
    - **Normal mode**:
      ```
      📋 **Specify complete**

      **Feature**: {Feature Name}
      **Slug**:    `{NNN}-{slug}`
      **Mode**:    Normal

      📂 `specs/{NNN}-{slug}/spec.md`

      👉 Next: `/sdd:plan {NNN}-{slug}`
      ```
    - **Minimal mode**:
      ```
      ⚡ **Specify complete — Fast Path**

      **Feature**: {Feature Name}
      **Slug**:    `{NNN}-{slug}`
      **Mode**:    Minimal

      📂 `specs/{NNN}-{slug}/spec.md`
      📂 `specs/{NNN}-{slug}/plan.md`
      📂 `specs/{NNN}-{slug}/tasks.md`

      👉 Next: `/sdd:implement {NNN}-{slug}`
      ```
  - **Verify**: Read the file, confirm both format blocks are updated with emojis

- [x] **T002** Redesign plan summary *(depends on T001)* — `skills/plan/SKILL.md`
  - **Do**: Replace Step 3 "Display exactly this format" block with:
    ```
    📐 **Plan complete**

    **Feature**: {Feature Name}
    📂 `specs/{NNN}-{slug}/plan.md` — {N} create, {N} modify

    👉 Next: `/sdd:tasks {NNN}-{slug}`
    ```
  - **Verify**: Read the file, confirm format block is updated

- [x] **T003** Redesign tasks summary *(depends on T002)* — `skills/tasks/SKILL.md`
  - **Do**: Replace Step 3 "Display exactly this format" block with:
    ```
    📝 **Tasks complete**

    **Feature**: {Feature Name}
    📂 `specs/{NNN}-{slug}/tasks.md` — {N} tasks ({N} sequential, {N} parallel)

    👉 Next: `/sdd:implement {NNN}-{slug}`
    ```
  - **Verify**: Read the file, confirm format block is updated

- [x] **T004** Redesign implement checkpoints *(depends on T003)* — `skills/implement/SKILL.md`
  - **Do**: Replace CP1, CP2, CP3 "Display exactly this format" blocks:
    - **CP1 — Code Review**:
      ```
      🔍 **CP1 — Code Review**

      **Phase 1**: T001–T00N ✅
      **Phase 2**: tests written, docs updated (or "N/A — minimal mode")

      **Changes**:
      - `path/to/file` — [one line description]
      - `path/to/file` — [one line description]

      **Silent fixes**: ⚠️ [list any, or "none"]

      **Verification**:
      - [ ] {scenario from spec} → expected result
      - [ ] {edge case from spec} → expected result
      ```
    - **CP2 — Test Results**:
      ```
      🧪 **CP2 — Test Results**

      ✅ All {N} tests passing

        — or —

      ❌ {Which tests failed and why (brief diagnosis)}
      ```
    - **CP3 — Commit & PR**:
      ```
      💾 **CP3 — Commit & PR**

      **Commit**: `{type}({scope}): {short description}`
               `Closes #{N}` (omit if no issue)

      **PR title**: {type}({scope}): {short description}
      **PR body**:
        ## What
        - [bullet from spec]

        ## Why
        [one sentence from spec]

        ## Testing
        - [verify step from tasks]

        Closes #{N} (omit if no issue)
      ```
  - **Verify**: Read the file, confirm all 3 checkpoint format blocks are updated

- [x] **T005** Redesign implement done summary *(depends on T004)* — `skills/implement/SKILL.md`
  - **Do**: Replace Step 9 "Display exactly this format" block with:
    ```
    ✅ **Done**

    **Feature**: {Feature Name}
    **Commit**:  `{type}({scope}): {description}`
    **PR**:      {PR URL}
    ```
  - **Verify**: Read the file, confirm format block is updated

- [x] **T006** Redesign status dashboard *(depends on T005)* — `skills/status/SKILL.md`
  - **Do**: Update Step 2 dashboard format and step display values:
    - New format:
      ```
      📊 **SDD Status**

      | # | Spec | Step | Updated |
      |---|------|------|---------|
      | 001 | {Feature Name} | 📋 specify | {date} |
      | 002 | {Feature Name} | 📐 plan | {date} |
      | ... | ... | ... | ... |

      **Total**: {N} specs
      ```
    - Update step display values:
      - `specify` → `📋 specify`
      - `plan` → `📐 plan`
      - `tasks` → `📝 tasks`
      - `implement` → `🚀 implement`
    - Task/substep appending still works: e.g., `🚀 implement (T003) [code-review]`
  - **Verify**: Read the file, confirm dashboard format and step values are updated

---

## Progress

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 | T001–T006 | [ ] |
