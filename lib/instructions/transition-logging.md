# Transition Logging

Every write to `.spec-context.json` must append a transition entry to the `transitions` array.

> Broader schema reference: [`docs/STATE.md`](../../docs/STATE.md). This file owns the `transitions[]` write rules specifically; STATE.md owns the full state model.

## Entry Schema

```json
{
  "step": "current step at time of write",
  "substep": "current substep/progress at time of write (or null)",
  "from": { "step": "previous currentStep", "substep": "previous progress" },
  "by": "sdd",
  "at": "ISO 8601 timestamp"
}
```

## Rules

1. **Read before write**: Before updating `.spec-context.json`, read the existing file and capture the current `currentStep` and `progress` values — these become the `from` field of the new entry.
2. **First-write case**: When creating `.spec-context.json` for the first time, set `from` to `null`.
3. **Append-only**: Never truncate or rewrite the `transitions` array. Always append to the existing array.
4. **Include on every write**: Every `.spec-context.json` update — whether setting progress, advancing steps, or completing tasks — must append a transition entry.
