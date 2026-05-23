# Plan: Init Adoption Wizard

**Spec**: [spec.md](./spec.md)

## Approach

Rewrite `skills/init/SKILL.md` into a three-phase wizard. **Phase 1** keeps today's scaffold (create `.sdd.json` / `.sdd/principles.md` / `.sdd/decisions/` when missing, idempotent), adding an optional "infer principles from the codebase" branch (a subagent drafts candidate MUSTs, user confirms). **Phase 2** is the new, incremental adoption flow: a cheap survey proposes candidate areas; the user picks one; a subagent proposes a domain tree for that area; parallel token-capped subagents draft the requirements specs surface-first; results are written at resolved paths and the domains appended to `.sdd.json`. **Phase 3** summarizes and points to next steps. The wizard reuses `lib/scripts/resolve-spec-paths.py` (from PR1) as the single source for paths and registry shape, uses `AskUserQuestion` for every choice, and is fully idempotent (skip registered domains, never overwrite a reviewed spec). Stacked on the PR1 branch because it depends on the resolver script.

## Files

### Modify

- `skills/init/SKILL.md` — the wizard rewrite (Phases 1–3, subagent prompts inline)
- `CLAUDE.md` — update the `/sdd:init` line under "Project setup" to describe adoption
- `README.md` — note `/sdd:init` can adopt an existing repo incrementally
- `docs/CONFIGURATION.md` — short note that adoption writes `domains` entries (registry)
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CHANGELOG.md` — version bump (minor)

## Testing Strategy

- **Manual / dogfood**: run the rewritten `/sdd:init` against a real repo (e.g. `ngx-dev-toolbar`) — confirm it surveys, proposes a tree, drafts `[DRAFT]` specs, writes `.sdd.json` domains, and is safe to re-run.
- **Idempotency**: re-run after removing a `[DRAFT]` marker → that spec is untouched; only new areas added.
- No automated suite (the change is a skill prompt); the resolver it calls is already covered by `test_resolve_spec_paths.py`.

## Risks

- **Extraction quality on legacy code**: drafts are approximations. Mitigated by surface-first scope, `[DRAFT]`/`[NEEDS CLARIFICATION]`/`## Uncovered`, and the human review pass.
- **Token cost on large areas**: mitigated by the cheap survey first, one-area-at-a-time, and token-capped per-leaf subagents.
