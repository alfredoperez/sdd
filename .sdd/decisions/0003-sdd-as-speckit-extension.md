# ADR 0003: SDD as a spec-kit Extension — Migration Architecture

**Status:** Proposed
**Date:** 2026-05-24
**Deciders:** alfredo
**Validated:** red-teamed against spec-kit source, the SpecKit Companion, and SDD itself on 2026-05-24 (see [Validation](#validation)). Corrections from that review are folded in below.

## Context

SDD today is a standalone Claude Code plugin. Adoption is the hard problem: a spec-driven AI workflow is difficult to grow alone. spec-kit already has a large user base, a 150+ extension catalog, and a real extension model. The proposal: migrate SDD to live as a spec-kit product so it rides that distribution, while keeping SDD's depth and going deeper on Claude Code where possible.

This ADR records the migration architecture, decided through a design interview and grounded in a source read of `github/spec-kit` (main, May 2026), the local `speckit-companion` VS Code extension, and SDD's own implementation — then revised after an adversarial validation pass.

**Grounded facts (corrected after validation):**
- spec-kit writes feature artifacts to `specs/<NNN>-<feature>/` at repo root (not under `.specify/`) — the **same path shape SDD uses**. `.specify/` holds tooling/config (templates, scripts, extensions, presets, memory, `extensions.yml`, `integration.json`, optional `feature.json`). **Caveat:** spec-kit resolves the *active* feature dir by env → `.specify/feature.json` → branch-name prefix; SDD resolves by "most-recently-modified dir containing `tasks.md`." Same path shape, **different active-dir logic** — must be reconciled.
- The **SpecKit Companion reads/writes `<spec-dir>/.spec-context.json`** and is workflow-agnostic + already spec-kit-aware. **But the schemas do NOT match field-for-field** (see [schema diff](#schema-diff)). SDD's `currentStep: "done"` and SDD's `status` enum (`active|completed|archived`) fall outside the Companion's enums; the Companion **silently coerces**, which *mis-renders a shipped spec's terminal state*. So the path needs no change, but a **schema reconciliation is required** — the integration is not literally "free."
- spec-kit extension **hooks are prompt-driven** (the core command markdown tells the agent to read `.specify/extensions.yml` and run registered hooks; `optional:false` auto-runs). A hook entry has **only `command:`** (+ `optional:`/`prompt:`) pointing to **another command-markdown file** — there is **no `shell:` or `skill:` payload**. A script runs only if that command markdown instructs the agent to run it (as `extensions/git/commands/speckit.git.feature.md` does). State-writing is therefore **agent-mediated, not a deterministic engine call**. SDD's richer hook model (`shell`/`skill`/blocking/parallel in `.sdd.json`) has **no host equivalent**.
- spec-kit has a **first-class Workflow engine** (`specify workflow run|resume`, state at `.specify/workflows/runs/<id>/`); the bundled `speckit` workflow IS specify→plan→tasks→implement with review **gate** steps, dispatching each command headless via the agent CLI (Claude has a `-p` headless path). Needs `speckit_version >= 0.8.5` for `integration: auto`. Gates **pause** by design.
- Extensions can supply templates (resolver priority above core); **presets** sit above extensions and support **selection + composition** per project (confirmed). Per-agent command emission is built-in (`--ai-skills` renders Claude `SKILL.md`, **non-destructively — won't overwrite an existing SKILL.md on update**). There is **no runtime agent detection**; `.specify/integration.json` is a best-effort install-time hint.

## Decision

### 1. One product — "SpecKit Companion" — in the speckit-companion monorepo
The product is **SpecKit Companion**: the existing VS Code extension (GUI) plus a new spec-kit extension (commands/hooks/state), living together in the **`speckit-companion` repo** as a monorepo — `vscode/` (the GUI) + `speckit-extension/` (the new extension) + a shared canonical schema. It replaces today's standalone SDD Claude Code plugin. Agent-agnostic by default; Claude-only assets baked in. The extension **`id` is `companion`**, so commands are `/speckit.companion.<cmd>`. "SDD" survives as the **methodology name** (the article series), not the product or command brand.

### 2. Packaging spans three spec-kit artifact types (still "one product, not a patchwork")
An **extension** (commands, hooks, rich-state scripts), a **workflow** (auto mode), and a **preset** (selectable template packs) — all under `speckit-extension/` in the `speckit-companion` repo, beside the VS Code GUI. Two publish targets from one repo: the **VS Code Marketplace** (GUI) and the **spec-kit catalog** (extension), path-filtered and versioned independently. One product we own end-to-end; "no patchwork" was about not depending on *other people's* extensions.

### 3. Pipeline: additive net-new + namespaced parallel + preset template override (NOT transparent supersede)
- Net-new commands (auto, resume, status, classify, living-specs/drift) always install.
- For overlaps we **cannot transparently supersede** core `/speckit.specify` etc. — spec-kit has no command-redirect. Instead: (a) ship namespaced parallel commands `/speckit.companion.specify…` the user opts into, and (b) ship a **preset** that overrides the *template* the core commands use, so even `/speckit.specify` produces our shape (no user-stories). "Replace" = the user picks our command **or** the preset reshapes core output. There is no auto-redirect.
- Open question for the spec: whether preset-template-override alone satisfies the templates requirement, making parallel pipeline commands optional.

### 4. Activity tracking: best-effort + agent-mediated, deterministic only in our own surfaces
The extension registers lifecycle hooks (`after_specify`, …) whose command-markdown runs a script writing the rich `.spec-context.json`. This is **independent of which templates are used**, but it is **not** "regardless of pipeline/agent": it fires only when the user runs a spec-kit command **and** the agent obeys the hook prompts. Deterministic capture happens only inside **our own commands** and the **workflow engine's dispatch/`shell` steps**. **Derive-from-files is a first-class capture path**, not a gap-filler. Our `implement` adds the per-task event journal. Pin spec-kit to a version where `after_specify`/`after_plan` hooks are wired.

### 5. The Companion repo owns the canonical schema; the extension writes it natively
`spec-context.schema.json` already lives in the `speckit-companion` repo and is the single source of truth. Because the spec-kit extension lives in the **same repo**, it reads/writes that schema **directly — no cross-repo reconciliation, no vendoring**. v1 schema work is therefore only: (a) extend the canonical schema backward-compatibly to cover every field the extension writes (`currentStep`, `status`, `transitions[].by` incl. `cli`/`ai`, `stepHistory`, plus SDD-carried fields like `type`/`step_summaries`); (b) the extension never emits the legacy `currentStep: "done"` — terminal state is `status: implemented|completed`. The **legacy SDD plugin** (sdd repo) is updated to the canonical enums (and STATE.md's status contradiction fixed) so its output also renders during the transition — transition polish, **not a v1 blocker**. `.spec-context.json` stays at `specs/<NNN>-<slug>/.spec-context.json` (no path change/migration); active-feature-dir resolution follows spec-kit's order (env → `.specify/feature.json` → branch prefix).

### 6. Auto mode = a spec-kit Workflow
Ship a `workflow.yml`; run via `specify workflow run`, resume via the engine. Pin `speckit_version >= 0.8.5`. Provide a **no-gate variant** for truly unattended runs (the bundled workflow's gates pause for review by design).

### 7. Template packs ship as a selectable preset
Selectable per project, priority above extensions, composition supported. Default pack `sdd-lean` (files/deps task axis, no user-stories). **Note:** complexity-detection *logic* (minimal vs normal) is command behavior, not template shape — it lives in our command markdown/scripts, not the preset, so it only applies on our pipeline commands.

### 8. Claude depth via install-time emission
Emit Claude `SKILL.md` assets and sub-agent prompts (`--ai-skills`) only Claude picks up; read `.specify/integration.json` as a best-effort hint. **Document the non-destructive install**: SKILL.md updates won't overwrite an existing file without `--force`/re-init — the upgrade path must handle this. Parallelism uses the workflow engine's `fan_out`/`fan_in` (agent-agnostic) and richer Claude sub-agents where present.

### 9. `.sdd.json` survives as SDD's own config
spec-kit's `extensions.yml` cannot express SDD's hook model (`shell`/`skill`/blocking/parallel) or domain/branch config. Keep `.sdd.json` as a parallel, SDD-owned config that our commands read — do **not** try to fold it into `.specify/`. spec-kit's `extensions.yml` is used only for the thin lifecycle-hook registrations that trigger our scripts.

### 10. Branch creation defers to spec-kit's git extension
spec-kit's bundled `git` extension already creates feature branches (`before_specify: speckit.git.feature`). To avoid double-branching, **rely on it** when present and gate SDD's own branch logic off; keep only SDD's main-branch push-guard (in our `implement` command markdown).

### 11. MVP: plan whole, ship phased — tracking-first v1 (schema reconciliation first)
Design the full architecture in one spec; release in phases. **v1 = schema reconciliation + foundation + lifecycle-hook activity capture + `status` + `resume`**, working on the user's existing spec-kit flow with the Companion lit up correctly. Pipeline/templates/complexity, living-specs, and auto mode follow.

### 12. Keep the standalone plugin alive during transition
Until the extension reaches parity, then deprecate. No hard switch.

## Rationale

The source read collapsed much of the perceived build cost (auto/resume ride the workflow engine; templates ride the preset/resolver stack; the file path already matches). The validation pass then corrected the two over-optimistic load-bearing claims: the Companion integration needs a small schema reconciliation rather than nothing, and hook-based capture is best-effort rather than guaranteed. With those fixed, the architecture holds. Effort and differentiation concentrate where the ecosystem has nothing: **rich activity traceability** (after reconciliation) and **domain living-specs + drift**.

## Alternatives Considered

- **Stay standalone Claude-only.** Deepest control, but keeps fighting adoption alone. Rejected — adoption is binding.
- **Augment-only (don't touch core pipeline).** Least build, most native; forfeits template control. Superseded by #3 (preset override gives template control without parallel commands — possibly sufficient).
- **Spec-kit-light state (`progress.yml`/derive-only).** Simpler, but loses per-task/decision precision and the Companion's richer view. Rejected — traceability is #1. (Derive-from-files is kept as a fallback, not the primary store.)
- **Transparent command supersede / runtime "if-Claude" branching.** Neither exists in spec-kit. Replaced by namespaced commands + preset override (#3) and install-time emission (#8).
- **Build our own auto-mode orchestrator.** Unnecessary — the workflow engine chains headless with resume (#6).

## Consequences

**Easier:** path already matches (no migration); auto/resume/templates reuse spec-kit machinery; one codebase; broad multi-agent reach; gentle opt-in adoption; living-specs + drift port with no host conflict.

**Harder / new constraints:**
- **Schema reconciliation is real work** (not free): `done` + `status` vocabularies must align, or the Companion mis-renders shipped specs. v1 task #1.
- **Tracking is best-effort, agent-mediated** — strongest on Claude; weaker/none when the agent ignores hook prompts or work happens outside commands. Mitigations: workflow `shell`/dispatch path, our own commands' direct writes, derive-from-files.
- **Hook expressiveness collapses on the host** — spec-kit hooks are `command:`-only; SDD's `shell`/`skill`/blocking model lives on only via `.sdd.json` read by our commands (#9).
- **`[P]` parallel sub-agents are Claude-only**; on other agents they degrade to sequential. Substep vocabulary doesn't match the Companion's (stored as opaque strings; its substep UI won't render them semantically).
- **Event journal is invisible to the Companion** until drained (freshness gap on the Companion's view).
- **Version floors** to pin: `>=0.8.5` (workflow `integration: auto`), and the spec-kit release that wired `after_specify`/`after_plan`. Document `--ai-skills` non-overwrite-on-update and the branch-creation collision with the git extension.
- Command branding becomes `/speckit.companion.*`; we live in spec-kit's `.specify/` house and depend on its version.

## Validation

Red-teamed 2026-05-24 against primary sources. Verdicts: **CONFIRMED** — repo layout/path, the Workflow engine as auto-mode (pin ≥0.8.5, gates pause), presets for selectable templates, no-runtime-detection + `--ai-skills`, living-specs/drift as the true differentiator. **REFUTED/QUALIFIED** — "Companion lights up with no schema change" (schemas diverge; coercion mis-renders terminal state), "tracking regardless of pipeline" (triple-gated agent compliance), "hooks can run a shell script" (only `command:` → agent-run markdown; the earlier `auto-commit.sh` citation was wrong), and "opt-in supersede" (namespaced coexistence + preset override, not redirection). All four corrections are folded into the Decisions above.

### Schema diff
| Field | SDD | Companion | Action |
|---|---|---|---|
| `currentStep` | `…implement·done` | `specify·clarify·plan·tasks·analyze·implement` | Drop `done` → map terminal to `implemented`/`completed` |
| `status` | `active·completed·archived` | 11 values (`draft…archived`) | Adopt Companion's vocabulary as canonical |
| `transitions[].by` | `sdd·extension` | `+user·cli·ai` | Widen SDD's enum to match |
| `transitions[].from` | object \| `null` | object required | Tolerated (Companion doesn't validate transitions); keep `null` first-write |
| substeps | 12 SDD names | 6 canonical | Stored as opaque strings; no break, no semantic render |
| required | `+createdAt` | `+branch·status·stepHistory·transitions` | Ensure fresh files carry the Companion's required set |

### Top risks (impact × likelihood)
1. Schema divergence silently corrupts the headline feature — **fix before any spec**.
2. "Tracking" is best-effort, agent-mediated — pin versions, elevate derive-from-files.
3. Hook expressiveness collapse — keep `.sdd.json` as parallel config.
4. "Supersede" not possible — namespaced + preset override only.
5. `[P]` parallelism / substep precision are Claude-only and partly invisible to the Companion.

## Related
- Brief: `Projects/sdd/briefs/2026-05-24-sdd-to-speckit-extension-migration.html` (vault) — note: predates this validation; auto-mode is **not** net-new (engine exists) and branching is install-time, not runtime.
- Spec: `{the migration spec — to be created by /sdd:specify}`
- Other ADRs: [[0001]] (4-layer context), [[0002]] (living-spec location & tiering)
