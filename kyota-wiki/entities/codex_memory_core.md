# Codex Memory Core

## Source Basis

- Derived from [`../raw/openai_codex_workflow_sources_2026-04-21_raw.md`](../raw/openai_codex_workflow_sources_2026-04-21_raw.md)
- Derived from [`../raw/anthropic_context_and_agent_sources_2026-04-21_raw.md`](../raw/anthropic_context_and_agent_sources_2026-04-21_raw.md)
- Derived from [`../raw/karpathy_llm_wiki_autoresearch_2026-04-21_raw.md`](../raw/karpathy_llm_wiki_autoresearch_2026-04-21_raw.md)
- Derived from [`../raw/simon_willison_codex_notes_2026-04-21_raw.md`](../raw/simon_willison_codex_notes_2026-04-21_raw.md)
- Consistent with [`../schema/context_selection_contract.md`](../schema/context_selection_contract.md) and [`../schema/multi_model_operating_contract.md`](../schema/multi_model_operating_contract.md)

## Purpose

Provide the smallest reliable default brain for Codex repo work so it starts from the right workflow posture without preloading broad wiki context.

## Use When

- Codex is doing non-trivial repo work in KYOTA
- the task is long-horizon, architectural, repetitive, or spans unfamiliar code
- you want Codex to start from durable workflow memory instead of a giant one-off prompt

## Do Not Load When

- the single-prompt website workflow already gives a tighter bounded load set
- the task is a tiny fix whose touched files are already obvious
- the work is not Codex-style repo work and this file would only duplicate narrower task instructions

## Load By Default

- `kyota-wiki/index.md`
- `kyota-wiki/NOW.md`
- `kyota-wiki/CODEX.md`
- `kyota-wiki/schema/context_selection_contract.md`
- `kyota-wiki/entities/codex_memory_core.md`

## Do Not Load By Default

- the entire `kyota-wiki/entities/` directory
- `kyota-wiki/raw/`
- the architecture roadmap
- research-source watchlists
- design canon or rollout entities unless the task actually depends on them

## Core Rules

1. Start from repo contracts, not chat memory.
2. Keep the standing context small. Retrieve deeper wiki files only when the task triggers them.
3. Prefer durable structures over repeated prompt paste. Use `AGENTS.md`, skills, task files, and wiki entities for repeatable workflows.
4. For unfamiliar code, trace before editing: request flow, module ownership, validation points, gotchas, then the next files to read.
5. Use skills for workflows you repeat. Keep skill metadata clear and narrow so Codex can load full instructions only when the task matches.
6. Treat Codex as `model + harness + surfaces`, not as “just the model.” Better instructions, tools, skills, and workflows are often the biggest leverage.
7. Give the agent a real loop: gather context, take action, verify, repeat.
8. Keep examples canonical and compact. Prefer a few strong examples over laundry-list prompting.
9. Keep toolsets minimal and unambiguous. Overlapping tools create noisy choices and worse context.
10. Externalize memory to files. If a pattern matters again later, it should live in the repo, not only in one successful thread or one plugin-driven execution flow.

## Retrieval Triggers

- Model/product behavior question: load [`openai_chatgpt_codex_operating_notes.md`](./openai_chatgpt_codex_operating_notes.md)
- Large implementation or debugging task with explicit execution discipline: if the active runtime exposes Superpowers skills, load [`superpowers_operating_notes.md`](./superpowers_operating_notes.md)
- Source review or canon refresh: load [`../tasks/codex-frontier-source-program.md`](../tasks/codex-frontier-source-program.md), [`ingestion_workflow.md`](./ingestion_workflow.md), and [`../schema/research_protocol.md`](../schema/research_protocol.md)
- Context, memory, or architecture question: load [`spl_declarative_context.md`](./spl_declarative_context.md), [`context_degradation_safeguards.md`](./context_degradation_safeguards.md), and the active architecture roadmap
- Unfamiliar repo area: ask for a request-flow map, validation points, gotchas, and the next files worth reading before editing
- Repeated workflow: create or consult a skill before growing the default prompt
- Long-running teammate-style work: prefer a durable thread or automation pattern plus repo state, not broad permanent preload

## Escalation Triggers

- the selected context is drifting toward `large` without a clear justification
- a source is second-hand, blocked, or paywalled
- the same workflow has now been explained enough times that it should become a skill or task contract
- the task depends on external tools or inbox context that is not yet mirrored in repo files

## KYOTA Implications

- Inference: a smooth Codex workflow comes more from the right durable scaffolding than from stuffing more wiki pages into every session.
- Inference: KYOTA should preserve the small-core-plus-retrieval pattern even as Codex surfaces add more features such as skills, automations, and teammate threads.
