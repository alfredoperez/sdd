---
name: sdd:drift
description: "SDD — Spec-Driven Development: detect code that drifted from .specs/<domain>/spec.md (changed without spec update)."
---

Usage: `/sdd:drift` (no arguments — scans every domain in `.specs/`).

Detects files that have changed since the corresponding `.specs/<domain>/spec.md` was last updated. Useful for catching code that evolved without going through `/sdd:specify` → `/sdd:plan` → `/sdd:implement`, so the living spec is now lying.

## Steps

### 1. Load configuration

Read `.sdd.json` (if present):
- `specExempt`: glob list of paths to ignore. Default: `["*.config.*", "*.test.*", "**/migrations/**", "scripts/**"]`.
- `driftCheck`: `"off"` | `"warn"` | `"gate"`. Default: `"warn"`. `off` short-circuits the skill (`✓ Drift check disabled (.sdd.json#driftCheck = off)`); `warn` and `gate` both run the report — `gate` is informational here (the gating decision is up to the surrounding workflow / CI).
- `domains`: same map used by [layered-context](../../lib/instructions/layered-context.md). Used to resolve which files belong to which domain.

If `.specs/` does not exist, stop with: `No .specs/ folder — nothing to check. Run /sdd:init or seed .specs/<domain>/spec.md first.`

### 2. Discover domains + last-spec-update commit

Glob `.specs/*/spec.md`. For each match:

1. The domain name is the parent directory basename.
2. Get the last commit that modified that file:
   ```bash
   git log -n 1 --format=%H -- .specs/<domain>/spec.md
   ```
   Skip the domain if the file is untracked (no commits yet) — log `ℹ <domain>: spec.md not yet committed; skipping drift check`.

### 3. Find drifted files per domain

For each domain with a tracked spec:

1. Resolve the domain's file pattern:
   - If `.sdd.json#domains.<domain>.pattern` exists, use that regex.
   - Otherwise, fall back to a path prefix match against `<domain>/` and `src/<domain>/` (anything inside a directory whose basename equals the domain name).
2. List files changed since the spec's last commit:
   ```bash
   git log --since-commit=<spec-commit> --name-only --pretty=format: -- <pattern-paths>
   ```
   Or equivalently `git diff --name-only <spec-commit>..HEAD -- <pattern-paths>`. Pick the form that respects the pattern.
3. Filter out:
   - Files matching any glob in `specExempt`.
   - The spec.md itself.
   - Files outside the matching pattern.
4. The result is the drift list for this domain.

### 4. Severity heuristic

Per drifted file, classify:

| Signal | Severity |
|---|---|
| File listed in any `specs/*/.spec-context.json#files_modified` since the spec's last commit | `tracked` (changed via SDD pipeline — Layer 1 wasn't synced; treat as a missed sync) |
| File outside `files_modified` of any spec | `unspeced` (changed entirely outside SDD) |
| File matches `specExempt` | (filtered out earlier; never appears) |

`unspeced` is more concerning than `tracked` — `tracked` may just mean the spec author didn't add a delta block, while `unspeced` means SDD never saw the change at all.

### 5. Report

Display per-domain:

```
🔍 Spec drift report

📁 .specs/<domain>/spec.md   (last updated <YYYY-MM-DD>, commit <abbrev>)
   <N> files changed since spec was last updated:

   tracked  src/auth/login.ts        — touched in spec 014-add-rate-limit (no delta block)
   tracked  src/auth/session.ts      — touched in spec 014-add-rate-limit (no delta block)
   unspeced src/auth/oauth.ts        — changed outside SDD pipeline

   👉 Run /sdd:specify to add a delta spec, or add the path to specExempt in .sdd.json.
```

If a domain has no drift, output `✓ <domain> — in sync` on a single line.

If every domain is in sync, the final line is `✓ All domains in sync.` and nothing else.

Always exit with success (this skill never halts the pipeline). Surrounding workflows can choose to treat `unspeced` rows as gates.
