# KYOTA Startup

Lean startup surface. Read this, then `NOW.md`, then open only what the task needs.

## Startup order
1. Read [`NOW.md`](./NOW.md) — current state, blockers, next actions.
2. Decide `BUDGET`: `tight`, `standard`, or `large`.
3. `SELECT` only the entities, prompt schemas, and raw sources the task needs.
4. `GENERATE` after selection is complete.

## Canonical files
- [`NOW.md`](./NOW.md) — current state (replaces the old append-only `log.md`).
- [`schema/kyota_agent_schemas.md`](./schema/kyota_agent_schemas.md) — modular prompt library for JIT tool loading, RCI, deterministic reflectors, formal verification gates.
- [`schema/research_protocol.md`](./schema/research_protocol.md) — source-of-truth and ingestion rules.

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
