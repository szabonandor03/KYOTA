# Superpowers Operating Notes

## Source Basis

- Derived from [`../raw/superpowers_plugin_2026-04-21_raw.md`](../raw/superpowers_plugin_2026-04-21_raw.md)
- Consistent with [`../schema/multi_model_operating_contract.md`](../schema/multi_model_operating_contract.md) and [`../schema/version_control_workflow.md`](../schema/version_control_workflow.md)

## Purpose

Explain what Superpowers is and how it fits into KYOTA as an optional Codex execution lane without turning it into a memory system or a second canonical workflow layer.

## Use When

- Codex is handling a larger implementation or debugging task and the active runtime exposes the needed Superpowers skills
- you want stricter execution discipline such as plan-first work, systematic debugging, TDD, isolated worktrees, review gates, or subagent-driven task execution
- the session needs to decide whether Superpowers should shape execution or whether the normal KYOTA Codex flow is enough

## Do Not Load When

- the single-prompt `fidesz-sapka-site/` workflow already covers the task
- the work is wiki curation, research ingestion, architecture-only planning, or another non-execution task
- the change is a small direct edit whose file scope is already obvious
- the plugin is installed locally but unavailable in the active runtime and the base KYOTA contract already fits

## What Superpowers Is

- Superpowers is a runtime-local workflow plugin built around skills, not a repo memory system.
- Its strongest default posture is `brainstorm/spec -> plan -> isolated worktree -> TDD -> subagent execution -> review -> finish branch`.
- Inside KYOTA, its value is execution discipline for larger Codex tasks, not ownership of state, memory, or project truth.

## KYOTA Mapping

- `brainstorming` maps to KYOTA planning and spec work, but durable outputs should land in `kyota-wiki/tasks/`, roadmap files, or other KYOTA-native locations.
- `writing-plans` maps to detailed implementation planning, but saved plans should use KYOTA-native artifact locations rather than defaulting to `docs/superpowers/plans`.
- `subagent-driven-development`, `systematic-debugging`, `requesting-code-review`, and `using-git-worktrees` are execution techniques that may operate under KYOTA contracts.
- `finishing-a-development-branch` must defer to [`../schema/version_control_workflow.md`](../schema/version_control_workflow.md) for branch, PR, and landing rules.

## Availability Rule

1. Use Superpowers only when the active Codex runtime actually exposes the required skills or tools.
2. Local installation or local config enablement is not enough to count as availability.
3. If the plugin is unavailable or only partially available, fall back to the standard KYOTA Codex flow without changing canonical state.

## Conflict Rule

1. User instructions outrank Superpowers defaults.
2. KYOTA contracts, active task files, and version-control rules outrank Superpowers defaults when they conflict.
3. Do not force Superpowers onto doc-only work, bounded site edits, ingestion decisions, architecture-only conversations, or tiny direct fixes.
4. Treat TDD, worktree isolation, and subagent-heavy execution as task-fit tools, not as mandatory behavior for every Codex action.

## Durable Output Rule

1. Superpowers must not create a parallel canonical `docs/superpowers/` memory layer inside KYOTA.
2. Durable specs, plans, task notes, architecture notes, and state updates belong in existing KYOTA locations such as `kyota-wiki/tasks/`, `kyota-wiki/schema/`, `kyota-wiki/entities/`, and `NOW.md`.
3. If temporary Superpowers-native artifacts are ever used later, they do not count as durable project state until they are projected back into KYOTA files.
4. Repeated workflow value belongs in repo files or durable skills, not only in one successful plugin-driven session.

## Task Fit

- Prefer Superpowers for multi-step implementation, debugging that benefits from a systematic root-cause process, or plan-first builds that are likely to benefit from subagents, worktrees, and review loops.
- Avoid Superpowers for small direct edits, wiki curation, research ingestion, architecture-only conversations, and routine `fidesz-sapka-site/` tasks already covered by the fast path.

## See Also

- [`codex_memory_core.md`](./codex_memory_core.md)
- [`../schema/multi_model_operating_contract.md`](../schema/multi_model_operating_contract.md)
- [`../schema/version_control_workflow.md`](../schema/version_control_workflow.md)
