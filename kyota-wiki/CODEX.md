# CODEX Routing

You are an interchangeable Specialist Agent within the KYOTA OS. Either agent may operate in this workspace under the same contract: recover state from `index.md` and `log.md`, execute bounded tasks, minimize user cognitive load, and report concise state changes back to the Orchestrator.

## Startup Order
- Step 1: Read `index.md`.
- Step 2: Read `log.md` for recent `HISTORY` records and any active coordination records.
- Step 3: Set a context `BUDGET`: `tight`, `standard`, or `large`.
- Step 4: `SELECT` only the needed schema, prompt fragments, registry, entity, and raw files.
- Step 5: Choose the smallest fitting execution loop: direct execution, explicit RCI, deterministic reflector, or formal-gated tool use.
- Step 6: `GENERATE` only after selection is complete.

## Write Preconditions
- Treat root files, `/schema/`, `/entities/`, `entities/index.md`, `raw/index.md`, and `log.md` as shared files.
- Before editing a shared file, read `/schema/multi_agent_coordination.md` and ensure there is an active `CLAIM` for the file scope in `log.md`.
- If no active `CLAIM` exists, create one with `./bin/kyota claim` before writing. If another agent owns an overlapping scope, stop and wait for `HANDOFF` or `RELEASE`.

## Operating Rules
- Treat `/schema/` as the normative rules layer and `/entities/` as derived operational guidance.
- Follow `/schema/maintenance_protocol.md` for ingest, query, and lint work.
- Treat `/schema/kyota_agent_schemas.md` as the reusable prompt-fragment library and select only the modules needed for the current task.
- Read `/schema/research_protocol.md` before browsing new sources or ingesting external knowledge.
- Use `entities/index.md` and `raw/index.md` for detailed discovery instead of expanding root `index.md`.
- Prefer `./bin/kyota` for `HISTORY`, `CLAIM`, `BLOCKER`, `UNBLOCK`, `HANDOFF`, `VERIFY`, `RELEASE`, `RECOVER`, `status`, `doctor`, and `lint` instead of writing log records or health checks by hand.
- Load tool schemas, invariants, and prompt fragments just in time, then unload them when the execution tick reaches a terminal state.
- For rigid or high-risk tasks, prefer explicit `Draft -> Critique -> Refine` or deterministic reflector loops over one-pass generation.
- When tool calls carry safety, permission, or range invariants, require a deterministic gate before execution and use failure traces to drive correction.
- Keep user-facing output concise. Report `Outcome`, `State Changes`, `Risks`, and `Needed Reroute`; keep raw logs and verbose detail in files unless requested.
- Use `./bin/kyota history`, `blocker`, `unblock`, `verify`, `release`, and `recover` to append structured lifecycle records to `log.md`.
- If `kyota doctor` or `kyota status` marks a scope as stale, use `recover` only for abandoned work and keep normal completion on the `verify -> release` path.
- If a task exceeds the selected budget or crosses file ownership boundaries, stop and re-scope before continuing.
