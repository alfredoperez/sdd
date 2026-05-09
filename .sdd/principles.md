# SDD Project Principles

> Principles for developing the SDD plugin itself. These are the project-wide MUSTs that any change to the SDD codebase must respect or explicitly amend (via PR + ADR).
>
> **Format:** lightweight bullet list. No semver. No Sync Impact Report. Discovered by presence at `.sdd/principles.md`.
> **Status:** initial draft, derived from the comparative analysis in `Projects/sdd/research/tools/13-sdd/research.md`. Edit freely.

- **Specs are committed artifacts.** Every shipped feature has a numbered spec in `specs/`; specs travel with code and are never thrown away. The spec, plan, tasks, and `.spec-context.json` are part of the deliverable, not scaffolding.

- **Adaptive ceremony.** Minimal-complexity changes (≤3 files, <10 lines, or pure style/config) skip plan and tasks; normal-complexity changes use the full pipeline. Don't impose ceremony where it doesn't pay rent.

- **Resumability is a feature, not an afterthought.** Every skill writes enough state to `.spec-context.json` that a fresh session can resume mid-flow without re-reading source artifacts. Cache projections (`approach`, `task_summaries`, `step_summaries`) prevent the resume tax.

- **Post-write checkpoints, not pre-write rigor.** CP1 reviews actual code; CP2 reviews tests; CP3 reviews commit and PR. We don't gate planning on heavy validation — we gate *shipping* on human review.

- **Single agent target.** SDD is a Claude Code plugin. We don't fork the design to support 25+ agents. Portability is out of scope.

- **Hooks are the extension point.** Customization happens through the 10 canonical hook points in `.sdd.json`, not by forking templates or adding new pipeline stages. If a behavior needs to be project-specific, expose it as a hook payload (prompt / shell / skill).

- **Templates are lean by default.** Required sections only: Approach, Files (plan); Phase 1 (tasks); Summary, Requirements, Scenarios, Out of Scope (spec-normal). Optional sections must be deleted when not used (no "N/A").

- **No AI attribution lines.** Commits and PRs do not include `Co-Authored-By: Claude` or "Generated with..." lines. Configurable via `.sdd.json` (`noAttribution: true` is the default).

- **Conventional commits.** All commits use `feat`, `fix`, `refactor`, `docs`, or `chore` types. Scope from primary directory modified. Imperative mood, lowercase, no trailing period, max 72 chars.

- **State changes are append-only.** `.spec-context.json` `transitions[]` is an audit log; never edited, only appended. Extension-managed fields (`status`, `stepHistory`) are read-merge only — never overwritten.
