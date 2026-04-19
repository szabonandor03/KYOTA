# Specialist Playbook

## Purpose
Operational quickstart for any KYOTA specialist agent: startup flow, CLI cheatsheet, symptom-to-action troubleshooting, VERIFY evidence standards, and slice-selection heuristics. Read this after `../index.md` and `../log.md` whenever the task is non-routine.

## Canonical Authority
- Normative rules: [`../schema/`](../schema/) files.
- Operational guidance: this page plus the rest of `/entities/`.
- If this page conflicts with a schema file, the schema wins. File an `UPDATE` to this page.

## Startup Quickstart
1. Read [`../index.md`](../index.md).
2. Read the recent tail of [`../log.md`](../log.md) - enough records to see the newest unreleased `CLAIM`s, any unresolved `BLOCKER`s, and the last few `HISTORY` records.
3. Read [`./multi_agent_coordination.md`](./multi_agent_coordination.md) for record catalog and flows.
4. Read [`../schema/maintenance_protocol.md`](../schema/maintenance_protocol.md) before any ingest or shared-file edit.
5. Set `BUDGET` (`tight` / `standard` / `large`).
6. `SELECT` only the additional entity pages, prompt fragments, and raw sources the task needs.
7. Choose execution pattern: direct execution, explicit RCI, deterministic reflector, or formal-gated tool use.
8. `GENERATE` only after selection is complete.

## CLI Cheatsheet
All coordination mutations go through [`../bin/kyota`](../bin/kyota). Hand-editing `../log.md` bypasses lifecycle validation and is what `kyota lint` exists to catch.

| Command | Use |
| --- | --- |
| `kyota status` | List active claims, unresolved blockers, stale markers |
| `kyota doctor` | One-shot workspace health summary |
| `kyota lint` | Structural health checks on registries, routers, log format, claim lifecycle |
| `kyota claim --agent <id> --files <A B ...> --note "..."` | Assert ownership before editing hotspots |
| `kyota blocker --agent <id> --files <...> --note "..."` | Announce an impasse on an active claim |
| `kyota unblock --agent <id> --files <...> --note "..."` | Clear a blocker without releasing the claim |
| `kyota handoff --agent <id> --files <...> --audience <id> --note "..."` | Transfer ownership; auto-clears any open blocker on the scope |
| `kyota verify --agent <id> --files <...> --note "..."` | Record deterministic evidence before release |
| `kyota release --agent <id> --files <...> --note "..."` | Close ownership after verification (normal completion) |
| `kyota recover --agent <id> --files <...> --note "..."` | Close an abandoned stale claim or blocker (recovery only) |
| `kyota history --agent <id> --files <...> --note "..."` | Append a `HISTORY` record for maintenance/ingest work |

### CLI Gotchas
- `--files` takes **space-separated** paths, not comma-separated.
- `verify`, `release`, `handoff`, `recover` require the `--files` set to match the active `CLAIM` exactly. Run `kyota status` and copy the paths verbatim if the command rejects your file set.
- `kyota status` prints files alphabetically, but the underlying `CLAIM` stores the order you passed. The match check compares as a set, not a list - spelling and presence are what matters.
- `HISTORY` does not grant ownership. If you need to edit a hotspot, you still need an active `CLAIM` first.

## Symptom to Action
| Symptom | Action |
| --- | --- |
| `kyota doctor` flags a stale claim I do not own and the owner is unreachable | `kyota recover --files <scope> --note "..."`, then re-claim if you are continuing the work |
| `kyota doctor` flags my own claim as stale | Record a `VERIFY`, `BLOCKER`, or other lifecycle record to refresh the activity window, or `RELEASE` if it is done |
| `kyota lint` flags router drift | Make `CLAUDE.md` and `CODEX.md` identical except for the title line, then re-run lint |
| `kyota lint` flags registry drift | Reconcile on-disk `/entities/` and `/raw/` files against `entities/index.md` and `raw/index.md` one-for-one |
| Overlapping active claim blocks my work | Stop. Wait for a `RELEASE`, request a `HANDOFF` from the current owner, or `RECOVER` only if the owner is abandoned |
| `verify`/`release`/`recover` reports "no active claim matches this exact file set" | Your file set does not match the `CLAIM`. Run `kyota status`, copy the exact paths, pass them as space-separated args |
| Blocker I cannot clear myself | `HANDOFF` to an agent who can, or `RECOVER` only if the whole scope is abandoned |
| I need to edit a hotspot and no claim exists | Run `kyota claim` first. Appending a single coordination record to `log.md` is the only edit allowed without a claim |
| New raw source without an entity yet | Add the `/raw/` file, update `raw/index.md`, then create the smallest relevant `/entities/` page and update `entities/index.md` in the same unit of work |
| Entity contradicts a schema file | Update the entity to match the schema and log a `HISTORY` record; the schema is normative |
| Log record I just wrote looks malformed | Do not rewrite earlier records (that is a hotspot edit). Append a corrective `HISTORY` record and run `kyota lint` to confirm |

## VERIFY Evidence Standards
Non-trivial shared changes should not be released without a `VERIFY` that cites deterministic evidence. What counts:

- **Wiki edits**: `kyota lint` clean, `kyota doctor` clean, and for routing-file touches, confirmation that `CLAUDE.md` / `CODEX.md` remain identical except for the title line.
- **Code edits**: green `pytest` (packaged install), plus `kyota lint` clean if registries were touched.
- **Schema or CLI changes**: `kyota lint` clean plus a live probe cycle on a disposable scope (for example `claim -> blocker -> unblock -> verify -> release`) exercising the changed path.
- **Ingestion**: new `/raw/` file linked from `raw/index.md`, new or updated `/entities/` page linked from `entities/index.md`, and `kyota lint` clean.
- **Reflector / formal-gate work**: the reflector or solver trace itself, captured in the `VERIFY` note.

Intuition-only review is not enough for non-trivial shared changes. If no deterministic check fits, either build one or narrow the slice until one does.

## Slice-Selection Heuristics
When choosing the next wiki improvement, prefer by value-to-scope:

1. **Undistilled raw knowledge** - new schema, CLI, or action-layer capabilities with no operational entity page yet.
2. **Thin entity pages** - under roughly fifteen lines, or pages with no examples, no checklist, and no failure modes.
3. **Registry gaps** - on-disk file not indexed, or index line without a file.
4. **Schema-vs-entity drift** - entity contradicts or lags the canonical schema.
5. **Duplicated normative rules** - the same rule stated in two places without a canonical pointer.
6. **Repeated user corrections** - the user had to give the same guidance twice.

Deprioritize:
- Polishing entities already at high signal density.
- Thickening `/raw/` summaries unless provenance or auditability is actively blocked.
- Cross-entity rewrites; prefer one-file slices that leave the rest of the wiki stable.

## Handoff Note Template
A good `HANDOFF` note lets the next agent start without reopening the full history. Include:
- Current progress (what is drafted, what is not).
- Any deterministic checks already passed (`kyota lint`, tests, reflector traces).
- Exact next action and its acceptance check.
- Known blockers or decisions left open.

Example:
```text
Draft sections 1-3 complete in entities/foo.md; section 4 (failure modes) still needed.
kyota lint passes. Next: write section 4 and update entities/index.md one-liner
before VERIFY. Open question: whether to cross-link from persona_orchestrator_specialist.md.
```

## Report Shape
User-facing summaries follow progressive disclosure:
- `Outcome`: what changed and why, in one or two sentences.
- `State Changes`: files touched, lifecycle records appended.
- `Risks / Needed Reroute`: follow-up gaps, anything left un-verified, anything that needs the Orchestrator to decide.

Hide raw tool output, verbose deliberation, and full log dumps unless the user explicitly asks.
