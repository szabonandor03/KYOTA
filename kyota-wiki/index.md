# KYOTA Startup

Lean startup surface. Read this, then `NOW.md`, ask the operator a few scoping questions, then open only what the task needs.

## Startup order
1. Read [`NOW.md`](./NOW.md) — current state, blockers, next actions.
2. If the task is a routine `fidesz-sapka-site/` edit and the prompt is concrete, follow [`schema/fidesz_sapka_single_prompt_workflow.md`](./schema/fidesz_sapka_single_prompt_workflow.md) and skip the clarification loop.
3. Otherwise, ask the operator 1-3 short questions about what they are thinking about, desired outcome, and exclusions.
4. Decide `BUDGET`: `tight`, `standard`, or `large`.
5. `SELECT` only the entities, prompt schemas, and raw sources the task needs.
6. `GENERATE` after selection is complete.

## Core method

```text
ASK -> BUDGET -> SELECT -> GENERATE
```

Selection happens after operator intake, not before. The point is to load context based on declared intent instead of broad repo guessing.

For routine FIDESZ SAPKA website edits, the exception is explicit:

```text
CONCRETE SITE REQUEST -> LOAD MINIMAL SITE CONTEXT -> IMPLEMENT -> VERIFY
```

Use that fast path only within the bounds of [`schema/fidesz_sapka_single_prompt_workflow.md`](./schema/fidesz_sapka_single_prompt_workflow.md).

## Canonical files
- [`NOW.md`](./NOW.md) — current state (replaces the old append-only `log.md`).
- [`schema/kyota_agent_schemas.md`](./schema/kyota_agent_schemas.md) — modular prompt library for JIT tool loading, RCI, deterministic reflectors, formal verification gates.
- [`schema/research_protocol.md`](./schema/research_protocol.md) — source-of-truth and ingestion rules.
- [`schema/fidesz_sapka_single_prompt_workflow.md`](./schema/fidesz_sapka_single_prompt_workflow.md) — one-prompt fast path for bounded `fidesz-sapka-site/` changes.
- [`schema/version_control_workflow.md`](./schema/version_control_workflow.md) — inferred git workflow for branch, PR, and merge practice in this repo.

## Registries
- [`entities/index.md`](./entities/index.md) — operational knowledge entities.
- [`raw/index.md`](./raw/index.md) — raw source registry for provenance.
- [`CLAUDE.md`](./CLAUDE.md) / [`CODEX.md`](./CODEX.md) — specialist entry contracts.

## Writing discipline
- Treat `/raw/` as immutable once stored.
- Treat `/schema/` as the only normative rules layer.
- Prefer targeted entity updates over duplicating guidance.
- Load prompt fragments just in time; unload after the task ends.
- Update `NOW.md` in place when current state changes — do not append a new record below the old one.
