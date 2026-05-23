# Transition Logging

Every logical state change yields exactly one entry in the `transitions` array.
There are two materialization paths — both produce the same entry shape:

- **Direct write** (most skills: `specify`, `plan`, `tasks`, `resume`, `pause`,
  `auto`, and the extension): read `.spec-context.json`, append a transition,
  write back. Rules below apply directly.
- **Journaled** (`/sdd:implement`, per [event-journal](./event-journal.md)): the
  skill appends a compact event carrying `step`/`substep`/`from`/`at`; the drain
  script materializes **one transition per event, in `seq` order**. The rules
  below are satisfied by the event (which carries `from`) plus the drainer
  (which appends).

> Broader schema reference: [`docs/STATE.md`](../../docs/STATE.md). This file owns the `transitions[]` write rules specifically; STATE.md owns the full state model.

## Entry Schema

```json
{
  "step": "current step at time of write",
  "substep": "current substep/progress at time of write (or null)",
  "from": { "step": "previous currentStep", "substep": "previous progress" },
  "by": "sdd",
  "at": "ISO 8601 timestamp, millisecond precision"
}
```

The `at` value **must** carry millisecond precision so consecutive
transitions sort correctly and the viewer's timeline can compute real
per-substep durations. Generate it with
`date -u +%Y-%m-%dT%H:%M:%S.%3NZ` (→ `2026-05-21T12:08:57.431Z`). Never
round to the whole second or minute, and never reuse one timestamp for
multiple entries in the same write — each entry gets its own fresh `at`.

## Rules

1. **Capture `from`**: the `from` field is the prior `currentStep` + `progress`.
   Direct-write skills read the existing file to capture it; journaled events
   capture it at append time (the skill knows its prior state from its entry read).
2. **First-write case**: When creating `.spec-context.json` for the first time, set `from` to `null`.
3. **Append-only**: Never truncate or rewrite the `transitions` array. Always append to the existing array — the drainer appends in `seq` order; direct writers append after reading.
4. **One per logical change**: Every state change — setting progress, advancing steps, completing tasks — yields exactly one transition entry (appended directly, or materialized from one journal event).
