# Hook Execution

When a skill reaches a hook point, it follows this procedure to execute any configured hooks from `.sdd.json`.

## Calling convention

A skill invokes this by specifying:
- `hookPoint` — a canonical name from the table below
- `vars` — a map of `{files, slug, spec-dir}` values available for template substitution

## Canonical hook points

| Hook point                      | Where it fires                                                           |
|---------------------------------|--------------------------------------------------------------------------|
| `pre:plan`                      | `/sdd:plan` — after Step 1 (Load), before Step 2 (Write) |
| `post:plan`                     | `/sdd:plan` — after Step 2 (Write), before Step 3 (Summary) |
| `pre:implement`                 | `/sdd:implement` — after Step 1 (Load), before Step 2 (Phase 1). First entry only; skipped on resume. |
| `post:task`                     | `/sdd:implement` — after each Phase 1 task completes |
| `pre:code-review`               | **Alias** of `pre:checkpoint:code-review` (kept for backward compatibility) |
| `pre:checkpoint:code-review`    | `/sdd:implement` — after Phase 1, before CP1 display |
| `pre:checkpoint:test-results`   | `/sdd:implement` — before CP2 display |
| `pre:checkpoint:commit-review`  | `/sdd:implement` — before CP3 display |
| `pre:commit`                    | `/sdd:implement` — after CP3 approval, before `git commit` |
| `post:pr`                       | `/sdd:implement` — after `gh pr create` succeeds |

Unknown hook-point keys in `.sdd.json` → log `⚠ Unknown hook point "{name}" — ignoring` and skip.

## Procedure

1. Read `.sdd.json` from the project root. If it does not exist or has no `hooks` key, return immediately (no hooks to run).

2. Let `entries = hooks[hookPoint]` (or `[]` if absent).
   - If `hookPoint = "pre:checkpoint:code-review"`, prepend any entries from `hooks["pre:code-review"]` (alias merge). Deduplicate by canonical JSON string.
   - If `entries` is empty, return.

3. For each entry in `entries`, normalize to an object form:
   - Plain string → `{ prompt: <string> }`
   - Object with exactly **one** of `prompt` / `shell` / `skill` → keep as-is
   - Object with zero or more than one discriminator → log `⚠ Invalid hook entry at hooks.{hookPoint}[{i}] — must specify exactly one of prompt/shell/skill. Skipping.` and drop that entry

4. Substitute template variables in every string field of each entry (this includes `prompt`, `shell`, and `args`):

   | Variable      | Replaced with                                                  |
   |---------------|----------------------------------------------------------------|
   | `{files}`     | `vars.files` — space-separated list of relevant files         |
   | `{slug}`      | `vars.slug` — spec slug (e.g., `014-configurable-hooks`)       |
   | `{spec-dir}`  | `vars.spec-dir` — spec directory path                         |

5. Dispatch each entry by payload type. By default, entries within a hook point run **in parallel** (spawn each as part of the same tool-call turn) unless an entry sets `parallel: false`. Skill entries always run sequentially.

   | Payload form                      | Tool used | Notes |
   |-----------------------------------|-----------|-------|
   | `{ prompt: "..." }`               | Agent     | Existing subagent behavior. Non-blocking by default — on spawn failure, log `⏭ Skipping hook — agent not available` and continue. |
   | `{ shell: "cmd" }`                | Bash      | Surface stdout and stderr inline. Default timeout 120s (override with `timeoutSeconds`). |
   | `{ skill: "/name", args: "..." }` | Skill     | Invoke the skill with `args` as the skill argument string. Skills run sequentially regardless of `parallel`. |

6. Wait for all dispatched entries at this hook point to complete before returning.

## Failure handling

**Blocking behavior** controls whether a failed hook halts the pipeline.

Per-hook-point defaults:

| Hook point                      | Default blocking | Rationale |
|---------------------------------|------------------|-----------|
| `pre:plan`, `post:plan`         | Warn only        | Plan is cheap to redo |
| `pre:implement`                 | **Halt**         | "Is the tree clean" guards |
| `post:task`                     | Warn only        | Don't block next task on a lint warning |
| `pre:checkpoint:code-review` (and alias `pre:code-review`) | Warn only | CP1 is already a user gate |
| `pre:checkpoint:test-results`   | Warn only        | Tests are the checkpoint content |
| `pre:checkpoint:commit-review`  | Warn only        | CP3 is already a user gate |
| `pre:commit`                    | **Halt**         | Last guard before a permanent git action |
| `post:pr`                       | Warn only        | PR is already open |

Per-entry override: `blocking: true` or `blocking: false` wins over the default for that entry.

- **Prompt/subagent** — a failed spawn is always treated as warn-only (consistent with existing behavior).
- **Shell** — non-zero exit code is a failure. If blocking, print `🛑 Hook {hookPoint}[{i}] (shell) failed with exit {code}: <stderr>` and stop the pipeline. If warn-only, print `⚠ Hook {hookPoint}[{i}] (shell) exit {code}` and continue.
- **Skill** — if the skill errors or returns a failure signal, treat as a failure per the blocking rule above.

## Backward compatibility

- Plain-string entries (today's format) keep working identically — they resolve to subagent prompts.
- The `pre:code-review` key keeps working — it is aliased to `pre:checkpoint:code-review`.
- Unknown hook-point keys never halt the pipeline; they are logged and skipped.
- The `agents` deprecation warning in `/sdd:implement` is unchanged.
