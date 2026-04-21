# Multi-Model Operating Contract

## Purpose

Define how KYOTA stays file-first while Claude Code, Codex, ChatGPT-native features, and future OpenAI API surfaces remain interchangeable execution layers instead of competing memory systems.

## Use When

- the task spans Claude, Codex, ChatGPT-native features, or future OpenAI API adoption
- the operator asks about workflow design, model roles, handoffs, or subscription leverage
- vendor-specific product behavior could change routing, context handling, or recurring work

## Do Not Load When

- a normal code or site edit can be completed entirely inside one bounded runtime
- the task does not depend on model choice, handoff rules, or vendor product behavior
- the relevant task contract already fixes the runtime and file scope

## Canonicality Rules

1. Repo markdown is the source of truth for project state, durable knowledge, architecture decisions, and reusable operating rules.
2. `NOW.md` and any active task file in `kyota-wiki/tasks/` outrank chat memory, project surfaces, or tool-session state when there is a conflict.
3. ChatGPT `Projects` are working containers, not canonical memory.
4. ChatGPT `Tasks` are reminder and automation surfaces, not project state.
5. ChatGPT `Memory` may hold operator preferences or stable stylistic tendencies, but it must not be trusted as the live source of architecture facts.
6. Deep research, Codex runs, and any other model-generated findings become durable only after `raw -> entity -> registry` ingestion or an explicit `NOOP` decision.

## Model-Lane Rules

Model lanes are routing preferences, not permanent ownership.

- OpenAI/Codex is preferred when the task benefits from long-horizon coding, large-context repo reasoning, or high-throughput paid workflows where usage ceilings matter.
- Claude is preferred when existing local conventions, MCP integrations, or a second-pass critique posture make it the tighter fit.
- Either specialist may execute a bounded task if it can honor the same KYOTA startup, context-selection, verification, and handoff rules.
- No model owns a project lane forever. Route by task shape, context cost, and verification surface.

## Handoff Rules

1. Before switching runtimes, write the durable state to repo files rather than expecting the next model to inherit chat context.
2. Keep user-facing request shape stable across models: same goal, same exclusions, same budget logic, same verification expectations.
3. If a task relied on vendor-specific behavior, name that dependency in the task note or roadmap so the next runtime can decide whether it matters.
4. If a handoff changes the preferred model lane, record why in `NOW.md` or the active task file.
5. Keep cross-model coordination lightweight. Use repo files and git history, not duplicated orchestration ledgers.

## Runtime-Plugin Rules

1. Runtime-local plugins, such as `Superpowers`, are execution helpers, not canonical memory.
2. Plugins may change how a task is executed, but they must not change where durable truth lives.
3. Plugin availability is session-local. A plugin enabled in local config does not count as available unless the active runtime exposes the needed tools or skills.
4. If a plugin is unavailable or only partially available, fall back to the base KYOTA contract instead of inventing a new local workflow.
5. User instructions, active task contracts, and repo operating rules outrank plugin defaults.

## OpenAI-Specific Rules

1. OpenAI product facts are temporally unstable. Re-verify pricing, plan features, and model availability against official OpenAI sources before changing durable guidance.
2. Current OpenAI workflow guidance for KYOTA lives in [`../entities/openai_chatgpt_codex_operating_notes.md`](../entities/openai_chatgpt_codex_operating_notes.md).
3. If future OpenAI API adoption becomes operational, add it as a lane around the repo rather than replacing the repo as the memory substrate.
4. Business and Enterprise-only features should not silently become assumptions for individual-plan workflows.

## Cross-References

- Shared specialist boundary: [`../entities/persona_orchestrator_specialist.md`](../entities/persona_orchestrator_specialist.md)
- Context selection contract: [`./context_selection_contract.md`](./context_selection_contract.md)
- Optional Superpowers lane: [`../entities/superpowers_operating_notes.md`](../entities/superpowers_operating_notes.md)
- Current architecture roadmap: [`../tasks/kyota-architecture-evolution.md`](../tasks/kyota-architecture-evolution.md)
