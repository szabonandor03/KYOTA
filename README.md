# KYOTA

KYOTA is a local-first LLM wiki for agent work.

The center of gravity is [`kyota-wiki/`](./kyota-wiki/): a Markdown source-of-truth for current project state, durable operational knowledge, working rules, and raw source material. The system is built to help future Claude Code or Codex sessions recover context quickly, ask a few scoping questions, select only the files they need, and execute with bounded startup cost.

Use this README for cold-start orientation only. Once you're inside `kyota-wiki/`, switch to the narrower startup and task contracts instead of reloading broad repo context.

This repo is optimized for single-operator, serial-agent work. It is not primarily a concurrent in-repo coordination system.

## What KYOTA Is For

Use KYOTA when you want to keep project context in files instead of in a long chat transcript:

- current state lives in a small startup surface
- durable knowledge is distilled into reusable notes
- raw sources are preserved for provenance and later re-checking
- future agent sessions can recover context cheaply instead of reloading everything

The operating assumption is simple: better Markdown beats bigger prompts.

## Start Here

For a normal session:

1. Read [`kyota-wiki/index.md`](./kyota-wiki/index.md).
2. Read [`kyota-wiki/NOW.md`](./kyota-wiki/NOW.md).
3. If the task is a concrete `fidesz-sapka-site/` edit, use the one-prompt fast path in [`kyota-wiki/schema/fidesz_sapka_single_prompt_workflow.md`](./kyota-wiki/schema/fidesz_sapka_single_prompt_workflow.md).
4. Otherwise ask the operator a few short questions about what they are thinking about, what outcome matters, and what should be excluded.
5. Create a compact context-selection record: goal, exclusions, budget, selected context, omitted context, execution pattern, verify method.
6. Choose a context budget: `tight`, `standard`, or `large`.
7. Select only the files needed for the task.
8. Then generate or execute.

Core method:

```text
ASK -> BUDGET -> SELECT -> GENERATE
```

The goal is a minimal startup surface, bounded context selection, and fewer expensive re-reads. The questions come before file loading so selection is driven by operator intent rather than by agent guesswork.

There is one deliberate exception: routine FIDESZ SAPKA website edits can run in one pass when the operator prompt is concrete and the task stays within [`kyota-wiki/schema/fidesz_sapka_single_prompt_workflow.md`](./kyota-wiki/schema/fidesz_sapka_single_prompt_workflow.md).

## Wiki Structure

[`kyota-wiki/`](./kyota-wiki/) is the real system.

- [`NOW.md`](./kyota-wiki/NOW.md): volatile current-state control surface. This is the first place to look for active work, blockers, and next actions.
- [`schema/`](./kyota-wiki/schema/): normative rules. Use this layer for operating contracts, research protocol, and reusable prompt or execution schemas.
- [`entities/`](./kyota-wiki/entities/): distilled operational knowledge. These files turn research and prior work into compact, reusable guidance.
- [`raw/`](./kyota-wiki/raw/): evidence and provenance layer. Preserve source material here so later sessions can verify claims or re-distill knowledge without losing the original basis.
- [`tasks/`](./kyota-wiki/tasks/): task-specific contracts when a piece of work needs a bounded working document.
- [`schema/context_selection_contract.md`](./kyota-wiki/schema/context_selection_contract.md) and [`schema/multi_model_operating_contract.md`](./kyota-wiki/schema/multi_model_operating_contract.md): new workflow contracts for explicit context selection and file-first multi-model coordination.
- [`tasks/kyota-architecture-evolution.md`](./kyota-wiki/tasks/kyota-architecture-evolution.md): active roadmap for workflow OS evolution until the rules are stable enough for `schema/`.
- [`CLAUDE.md`](./kyota-wiki/CLAUDE.md) and [`CODEX.md`](./kyota-wiki/CODEX.md): specialist entry contracts for the two main agent environments.

In practice:

- open `index.md` and `NOW.md` first
- ask a few short operator questions before selecting deeper context
- use the registries in [`entities/index.md`](./kyota-wiki/entities/index.md) and [`raw/index.md`](./kyota-wiki/raw/index.md) for discovery
- avoid loading large amounts of material until the task actually needs it

## Operating Philosophy

- Keep startup small. Most sessions should begin with `index.md`, `NOW.md`, and a narrow file selection.
- Ask before loading. Use a brief operator-intake pass to decide what is worth putting in context.
- Bound context deliberately. Do not treat the whole repo as the prompt.
- Preserve raw sources. Distill reusable knowledge into `entities/`, but keep evidence in `raw/`.
- Keep rules separate from observations. `schema/` is normative; `entities/` is derived guidance.
- Optimize for future sessions. The wiki should make restart and handoff cheap for the next Claude Code or Codex run.

## Repo Orientation

The repo contains the wiki plus project workspaces that the wiki tracks and supports. If you are opening the repository for the first time, start in [`kyota-wiki/`](./kyota-wiki/) before touching the surrounding project directories.

Historical context: KYOTA originally included a coordination-oriented CLI, claim and recovery workflow, verification and release records, and an optional TUI dashboard. That is no longer the main identity of the repo. The current contract is the wiki-first, single-operator workflow described above.
