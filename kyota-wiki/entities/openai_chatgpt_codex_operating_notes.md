# OpenAI ChatGPT + Codex Operating Notes

## Source Basis

- Derived from [`../raw/openai_chatgpt_codex_2026-04-21_raw.md`](../raw/openai_chatgpt_codex_2026-04-21_raw.md)
- Official sources checked on 2026-04-21:
  - ChatGPT pricing page
  - OpenAI Help Center article on Pro tiers
  - OpenAI developer docs for `gpt-5.4-pro`
  - OpenAI developer docs for `gpt-5.2-codex`

## Purpose

Convert current official OpenAI product facts into stable workflow rules for KYOTA without treating OpenAI-native surfaces as the memory substrate of the repo.

## Use When

- the task depends on OpenAI subscription leverage, Codex posture, ChatGPT-native workflow features, or future API adoption
- model-lane choice matters for planning or execution
- a future session needs to distinguish durable repo memory from ChatGPT or Codex execution state

## Do Not Load When

- the task is a normal repo edit that does not depend on OpenAI product behavior
- the single-prompt website workflow already gives a sufficient bounded load set
- the task only needs recurring Codex workflow posture; use [`codex_memory_core.md`](./codex_memory_core.md) for that
- the question is purely about local repo state, not about model choice or product capability

## Canonical Rules

1. OpenAI product surfaces are execution layers around KYOTA, not replacements for repo memory.
2. ChatGPT `Projects` may help keep active work organized, but they are not canonical project state.
3. ChatGPT `Tasks` are useful as reminders or recurring triggers, but they do not define backlog state or architecture truth.
4. ChatGPT `Memory` can help preserve operator preferences, but it must not be trusted as the current record of architecture facts, workflow rules, or task state.
5. Current paid ChatGPT plans expose workflow-relevant features such as `Projects`, `Tasks`, `Memory`, and `Codex`, so KYOTA must explicitly decide what stays in files instead of letting product convenience become an accidental source of truth.
6. OpenAI plan facts are volatile. Re-verify official sources before promoting new plan or feature assumptions into durable guidance.
7. If OpenAI API usage becomes operational later, `gpt-5.4-pro` is the current official pro reasoning surface for hard problems, while `gpt-5.2-codex` is the current official long-horizon coding surface. That is a routing hint, not a standing ownership rule.
8. Keep recurring Codex workflow rules separate from volatile product facts. Product-surface guidance belongs here; default Codex working posture belongs in [`codex_memory_core.md`](./codex_memory_core.md).

## KYOTA Implications

- Inference: a higher OpenAI subscription should expand throughput, parallelism, and convenience, not loosen the file-first contract of the repo.
- Inference: the meaningful architectural boundary is `repo memory vs. execution surface`, not `Claude vs. OpenAI`.
- Inference: if ChatGPT-native projects or tasks start to matter operationally, the durable projection of that state still belongs in `NOW.md`, task files, or schema/entity updates.
- Inference: once OpenAI-native features are treated as execution surfaces, Claude Code and Codex can stay peer specialists under the same KYOTA contract instead of splitting into separate systems.

## Evidence Notes

- The 2026-04-21 pricing page shows `Plus` and `Pro` both include workflow-relevant features such as projects, tasks, memory/context expansion, and Codex access, with `Pro` positioned as the higher-throughput tier.
- The 2026-04-21 Pro help article documents two current Pro tiers, `$100` and `$200`, with the same core capabilities and different usage allowances.
- The official developer docs position `gpt-5.4-pro` as a slower, harder-thinking Responses API surface and recommend `background mode` for long-running requests.
- The official developer docs position `gpt-5.2-codex` as the current OpenAI coding model optimized for long-horizon, agentic coding tasks.

## See Also

- [`codex_memory_core.md`](./codex_memory_core.md) for the small standing Codex repo brain
- [`../tasks/codex-frontier-source-program.md`](../tasks/codex-frontier-source-program.md) for the curated frontier source canon and monthly refresh loop
