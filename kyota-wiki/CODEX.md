# CODEX Routing

You are a Specialist Agent in the KYOTA workspace. Claude and Codex are peer specialists under one file-first contract: recover state from `index.md` and `NOW.md`, keep context bounded, write durable state back to the repo, and report concise outcomes.

## Use When

- you are starting cold in KYOTA and need the Codex-side startup contract
- the task spans repo state, architecture, model routing, or research ingestion
- a handoff needs the current shared vocabulary for goal, exclusions, budget, selected context, omitted context, and verification

## Do Not Load When

- [`schema/fidesz_sapka_single_prompt_workflow.md`](./schema/fidesz_sapka_single_prompt_workflow.md) already covers a bounded site edit
- a task contract in `kyota-wiki/tasks/` already fixes the exact file scope
- the task is a one-line fix whose touched files are already explicit

## Startup Order

1. Read [`index.md`](./index.md).
2. Read [`NOW.md`](./NOW.md).
3. If the task is a concrete `fidesz-sapka-site/` edit, follow [`schema/fidesz_sapka_single_prompt_workflow.md`](./schema/fidesz_sapka_single_prompt_workflow.md).
4. For non-trivial Codex repo work, read [`entities/codex_memory_core.md`](./entities/codex_memory_core.md).
5. Create a context-selection record using [`schema/context_selection_contract.md`](./schema/context_selection_contract.md): `goal`, `exclusions`, `budget`, `selected context`, `omitted context`, `execution pattern`, `verify method`.
6. `SELECT` only the files, entities, prompt fragments, and tool schemas the task needs.
7. If the task is a larger implementation or debugging effort and the current runtime exposes Superpowers skills, load [`entities/superpowers_operating_notes.md`](./entities/superpowers_operating_notes.md) and use that as an optional execution lane.
8. If the task depends on Claude/Codex/ChatGPT/OpenAI behavior, load [`schema/multi_model_operating_contract.md`](./schema/multi_model_operating_contract.md) and [`entities/openai_chatgpt_codex_operating_notes.md`](./entities/openai_chatgpt_codex_operating_notes.md).
9. If the task is reviewing frontier Codex sources or deciding what should enter canon, load [`tasks/codex-frontier-source-program.md`](./tasks/codex-frontier-source-program.md).
10. `GENERATE` after selection is complete.
11. `VERIFY` with the smallest fitting evidence surface.

## Operating Rules

- `/schema/` is the normative rules layer. `/entities/` is derived operational guidance.
- Follow [`schema/version_control_workflow.md`](./schema/version_control_workflow.md) for any lasting repo change.
- Read [`schema/research_protocol.md`](./schema/research_protocol.md) before ingesting external sources.
- Treat [`schema/kyota_agent_schemas.md`](./schema/kyota_agent_schemas.md) as a modular prompt library; load only the modules the task needs.
- Use [`entities/index.md`](./entities/index.md) and [`raw/index.md`](./raw/index.md) for discovery. Prefer entity pages over raw files unless verification or ingestion is the work.
- Default to `tight` or `standard` budget. `large` needs a concrete justification.
- For non-trivial tasks, make omitted context explicit. “What we did not load” is part of the contract now.
- Treat [`entities/codex_memory_core.md`](./entities/codex_memory_core.md) as the standing Codex workflow brain: small default core, deeper retrieval only when triggered.
- Treat [`entities/superpowers_operating_notes.md`](./entities/superpowers_operating_notes.md) as an optional execution lane for larger implementation or debugging work only when the active runtime actually exposes Superpowers skills.
- Do not auto-load Superpowers for small direct edits, wiki work, source ingestion, architecture-only work, or the bounded `fidesz-sapka-site/` fast path.
- If a workflow matters more than once, convert it into a skill, task contract, or durable entity instead of growing one-off prompt boilerplate.
- Use [`tasks/kyota-architecture-evolution.md`](./tasks/kyota-architecture-evolution.md) as the current roadmap for workflow evolution. Do not promote tactical ideas into schema until they survive real use.
- Keep user-facing output concise: `Outcome`, `State changes`, `Risks / Needed reroute`.

## Updating NOW.md

`NOW.md` is rewritten in place, not appended to. When current state changes materially:

- Move stale items out of **Active work** or **Blockers** when they no longer apply.
- Bump **Recent decisions** and keep roughly the last 5.
- Keep the file small enough that a cold-start session can recover quickly.

## Coordination

This workspace is single-operator and serial by default. If work ever needs isolation, use git branches, task contracts, and repo files for handoff rather than a parallel in-repo mailbox.
