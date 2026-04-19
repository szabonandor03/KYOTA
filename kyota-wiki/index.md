# KYOTA Startup Manifest

This file is the lean startup surface for every specialist agent. Use it to recover the workspace contract, then open only the registries, prompt schemas, and rules required by the current task.

## Startup Order
1. Read [`log.md`](./log.md) for recent `HISTORY` records and any active coordination records.
2. Set `BUDGET` to `tight`, `standard`, or `large`.
3. `SELECT` only the needed schema, prompt schema, registry, entity, and raw sources.
4. Decide whether the task needs direct execution, explicit RCI, a deterministic reflector, or a formal verification gate.
5. `GENERATE` only after selection is complete.

## Canonical State
- [`log.md`](./log.md) - Current state ledger, history, and fallback mailbox.
- [`schema/maintenance_protocol.md`](./schema/maintenance_protocol.md) - Canonical ingest, query, lint, and SPL workflow.
- [`schema/multi_agent_coordination.md`](./schema/multi_agent_coordination.md) - Canonical claim, handoff, verify, and release contract.
- [`schema/kyota_agent_schemas.md`](./schema/kyota_agent_schemas.md) - Modular prompt library for JIT tool loading, explicit RCI, deterministic reflectors, and formal verification gates.
- [`schema/research_protocol.md`](./schema/research_protocol.md) - Source-of-truth and acquisition rules.

## Detailed Registries
- [`entities/specialist_playbook.md`](./entities/specialist_playbook.md) - First-open operator playbook: startup flow, CLI cheatsheet, troubleshooting, VERIFY evidence standards, and slice-selection heuristics.
- [`entities/index.md`](./entities/index.md) - Detailed entity map for operational knowledge.
- [`raw/index.md`](./raw/index.md) - Raw-source registry for provenance and source verification.
- [`bin/kyota`](./bin/kyota) - Workspace CLI for `HISTORY`, `CLAIM`, `BLOCKER`, `UNBLOCK`, `HANDOFF`, `VERIFY`, `RELEASE`, `status`, and `lint`.
- [`CODEX.md`](./CODEX.md) - Specialist entry contract for Codex.
- [`CLAUDE.md`](./CLAUDE.md) - Specialist entry contract for Claude.
