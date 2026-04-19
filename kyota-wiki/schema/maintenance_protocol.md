# KYOTA Maintenance Protocol

## Purpose
This file defines the ingest, query, and lint workflows for maintaining a high-signal LLM knowledge base with minimal context waste and a predictable startup surface for dynamically verifiable, self-healing agents.

## Required Task Gate
1. Start from `../index.md`.
2. Set `BUDGET` to `tight`, `standard`, or `large` before reading deeply.
3. `SELECT` only the schema, prompt schema, registry, entity, log span, and raw sources needed for the task.
4. Choose the smallest fitting execution pattern: direct execution, explicit RCI, deterministic reflector, or formal verification gate.
5. `GENERATE` only after selection is complete.
6. Record resulting state changes in `../log.md` using the canonical log format.
7. Prefer `../bin/kyota` for structured `HISTORY`, `CLAIM`, `BLOCKER`, `UNBLOCK`, `HANDOFF`, `VERIFY`, `RELEASE`, and `RECOVER` records instead of manual log entry authoring.

## Ingest Workflow
1. When a new file enters `/raw/`, add or update its one-line entry in `../raw/index.md`.
2. Read the raw source directly before consulting derivative summaries.
3. Create or update the smallest relevant `/entities/` page rather than broadening unrelated files.
4. When an entity contains reusable prompt fragments or execution patterns, distill them into modular blocks in `../schema/kyota_agent_schemas.md`.
5. Update `../entities/index.md` with a one-line summary for each new or materially changed entity.
6. Update `../index.md` only when the startup contract or registry links change.
7. Update `../CODEX.md` and `../CLAUDE.md` when specialist execution behavior changes materially.
8. Append a `HISTORY` record with `../bin/kyota history` describing the ingestion, files touched, and source used.

## Query Workflow
1. Read `../index.md` first, then `../log.md`, before opening detailed registries or entity files.
2. Decide whether the task requires direct execution, explicit RCI, a deterministic reflector, or a formal verification gate before selecting detailed evidence.
3. Prefer `../entities/index.md` for discovery and open only the minimum set of entity pages required by the selected `BUDGET`.
4. Load only the prompt fragments, invariants, and tool schemas required for the current execution tick, then unload them after the task reaches a terminal state.
5. Prefer `/entities/` over `/raw/` unless source verification or new ingestion is required.
6. Load only the relevant log window needed to understand current ownership, recent changes, or unresolved blockers.
7. If the selected evidence exceeds the chosen budget, reduce scope or split the task before continuing.

## Lint Workflow
1. Run health checks across `../index.md`, `../entities/index.md`, `../raw/index.md`, `/entities/`, `/schema/`, and `../log.md`.
2. Flag contradictions between entity pages instead of silently reconciling them.
3. Verify that `../CODEX.md` and `../CLAUDE.md` are identical except for the title line.
4. Flag any duplicated normative rule that exists in both `/schema/` and `/entities/` without an explicit canonical pointer.
5. Verify that every entity and raw source listed in the registries exists on disk and that every on-disk entity or raw source is indexed.
6. Verify that reusable prompt fragments referenced by entity pages are mirrored in `../schema/kyota_agent_schemas.md` or intentionally excluded.
7. Verify that high-risk tool-execution paths document a deterministic verification or invariant gate instead of intuition-only review.
8. Verify that `../log.md` uses the structured record format and that claim and blocker lifecycles remain valid.
9. Use `../bin/kyota doctor` or `../bin/kyota status` to surface stale claims/blockers, and use `../bin/kyota recover` to close abandoned stale scopes explicitly.
10. Append a `HISTORY` record to `../log.md` when contradictions, drift, or stale claims are found or resolved during maintenance work.
11. Prefer `../bin/kyota lint` for the executable health-check pass before performing deeper manual audits.

## Editing Discipline
- Treat `/raw/` as immutable once a source is stored.
- Treat `/schema/` as the only normative rules layer unless a file explicitly says otherwise.
- Prefer targeted entity updates over duplicating guidance across multiple files.
- Load tool schemas and prompt fragments just in time; do not turn them into always-on prompt bulk.
- Update registries and `../log.md` as part of the same unit of work when knowledge changes.
- Use `../bin/kyota status` to inspect ownership before shared-file edits when coordination is unclear.
- Treat `RECOVER` as abandoned-work cleanup only; use `RELEASE` for normal completion.
