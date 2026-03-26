# Design Philosophy

## Lineage

SDD draws from two existing approaches and adds its own innovations:

### From spec-kit
- **Structured specs with requirement IDs** (R001, R002) — makes requirements traceable and testable
- **Scenarios** (When/Then format) — unambiguous behavioral specifications
- **Out-of-scope sections** — prevents scope creep by explicitly stating what's excluded

**Dropped from spec-kit**: constitution overhead, clarification agents, prerequisite scripts. These added ceremony without proportional value for most changes.

### From superpowers
- **Skill-per-step modularity** — each workflow phase is a self-contained skill that can be invoked independently
- **Hard gates before implementation** — checkpoints prevent shipping unreviewed code
- **Subagent parallelism** — Phase 2 tasks (tests, docs) run in parallel for speed

**Dropped from superpowers**: generic skill library approach. SDD is opinionated about what steps exist rather than being a general-purpose skill framework.

### What SDD adds
- **Auto-complexity detection** in `/sdd:specify` — analyzes the codebase to classify changes as minimal or normal, then fast-tracks small changes through the entire pipeline in one step
- **`state.json` for resume** — workflow state is persisted so you can pick up mid-implementation after context loss or session interruption
- **Right-sized ceremony** — a CSS fix shouldn't need the same process as a new feature

## Core Principles

### 1. Right-sized process
A one-line CSS fix and a new authentication system shouldn't go through the same ceremony. SDD auto-detects complexity and adjusts: minimal changes get spec + plan + tasks generated in one shot, while complex features get dedicated review at each step.

### 2. Specs as artifacts
Specifications are committed alongside implementation code in `specs/`. They travel with the PR, providing context for reviewers and future maintainers. They're not throwaway documents — they're part of the codebase's history.

### 3. Checkpoints, not bureaucracy
Every checkpoint in the implement phase prevents a real category of mistake:
- **CP1 (Code Review)**: Catches implementation errors before they're committed
- **CP2 (Test Results)**: Ensures tests pass before creating a PR
- **CP3 (Commit & PR)**: Reviews the commit message and PR body for accuracy

No checkpoint exists "just because." If a gate doesn't prevent a real mistake, it shouldn't exist.

### 4. State enables continuity
`state.json` tracks which step and task you're on. When a Claude session ends mid-implementation (context limit, network issue, user interruption), you can resume exactly where you left off. No work is lost, no tasks are re-executed.

### 5. Convention over configuration
SDD works with zero configuration. The default spec directory is `specs/`, commits use conventional format, and complexity detection uses sensible thresholds. Everything is customizable via `.sdd.json` when needed, but you shouldn't need to configure anything to get started.
