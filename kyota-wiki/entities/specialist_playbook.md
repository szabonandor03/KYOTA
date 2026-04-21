# Specialist Playbook

## Purpose
Operational quickstart for any KYOTA specialist agent: startup flow, operator-intake before context selection, slice-selection heuristics, VERIFY evidence standards, report shape. Read this after `../index.md` and `../NOW.md` whenever the task is non-routine.

## Canonical Authority
- Normative rules: [`../schema/`](../schema/) files.
- Operational guidance: this page plus the rest of `/entities/`.
- If this page conflicts with a schema file, the schema wins.

## Startup Quickstart
1. Read [`../index.md`](../index.md).
2. Read [`../NOW.md`](../NOW.md) — active work, blockers, next actions, recent decisions.
3. Read [`../schema/research_protocol.md`](../schema/research_protocol.md) before any ingest or new-source browsing.
4. Ask the operator 1-3 short questions about what they are thinking about, desired outcome, and exclusions.
5. Set `BUDGET` (`tight` / `standard` / `large`).
6. `SELECT` only the entity pages, prompt fragments, and raw sources the task needs.
7. Choose execution pattern: direct execution, explicit RCI, deterministic reflector, or formal-gated tool use.
8. `GENERATE` after selection is complete.

## VERIFY Evidence Standards
Non-trivial changes should not be called done without deterministic evidence cited in the reply. What counts:

- **Wiki edits**: routing files (`CLAUDE.md` / `CODEX.md`) identical except for the title line. Registry one-liners match on-disk files one-for-one.
- **Code edits**: the relevant test or build command green, named explicitly (for example `npm run build` in `fidesz-sapka-site/`).
- **UI edits**: preview server exercised and the change observed — screenshot or log excerpt in the reply. Never ask the operator to verify manually.
- **Ingestion**: new `/raw/` file linked from `raw/index.md`, new or updated `/entities/` page linked from `entities/index.md`.
- **Reflector / formal-gate work**: the reflector or solver trace itself, in the reply.

Intuition-only review is not enough. If no deterministic check fits, either build one or narrow the slice until one does.

## Slice-Selection Heuristics
When choosing the next wiki improvement, prefer by value-to-scope:

1. **Undistilled raw knowledge** — new capability or research with no operational entity page yet.
2. **Thin entity pages** — under ~15 lines, or pages with no examples, no checklist, and no failure modes.
3. **Registry gaps** — on-disk file not indexed, or index line without a file.
4. **Schema-vs-entity drift** — entity contradicts or lags the canonical schema.
5. **Duplicated normative rules** — the same rule stated in two places without a canonical pointer.
6. **Repeated operator corrections** — the operator had to give the same guidance twice.

Deprioritize:
- Polishing entities already at high signal density.
- Thickening `/raw/` summaries unless provenance is actively blocked.
- Cross-entity rewrites; prefer one-file slices that leave the rest of the wiki stable.

## Updating NOW.md
- Rewrite in place; do not append a new block below the old one.
- When active work shifts, move stale items out.
- Keep **Recent decisions** to roughly the last 5.
- Target <100 lines. If it grows beyond that, trim — `NOW.md` bloat defeats the purpose.

## Report Shape
User-facing summaries follow progressive disclosure:
- `Outcome`: what changed and why, in one or two sentences.
- `State changes`: files touched, any `NOW.md` updates.
- `Risks / Needed reroute`: follow-up gaps, anything left un-verified, anything that needs an operator decision.

Hide raw tool output, verbose deliberation, and full file dumps unless the operator asks.
