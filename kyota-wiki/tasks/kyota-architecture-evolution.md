# KYOTA Workflow OS Evolution Roadmap

Authored: 2026-04-21

## Purpose

This file is the active roadmap for evolving KYOTA from a lean wiki-first workflow into a stricter workflow operating system that can coordinate Claude Code, Codex, ChatGPT-native features, and future OpenAI API usage without wasting context or losing canonical state.

## Use When

- the task changes KYOTA architecture, workflow rules, model routing, or knowledge-ingestion behavior
- a session needs the current backlog for workflow evolution instead of the stable schema layer
- a handoff needs the latest picture of what has been proven, what is still tentative, and what the next implementation steps are

## Do Not Load When

- a bounded site or code task is already covered by a tighter task contract or the single-prompt website workflow
- the work only needs the stable normative contract in `schema/`
- a session already knows the exact file scope and does not need roadmap context

## Current Architecture

- Startup is centered on `kyota-wiki/index.md` and `kyota-wiki/NOW.md`.
- The governing workflow shape is `ASK -> BUDGET -> SELECT -> GENERATE`.
- `schema/` holds normative rules, `entities/` holds distilled guidance, `raw/` holds provenance, and `tasks/` holds bounded working documents.
- Claude Code and Codex already operate as interchangeable specialists under the same repo, but the cross-model rules are only partially implicit.
- Knowledge hygiene is a strong philosophy in the repo, but the “what was intentionally not loaded” decision is not yet formalized as a first-class contract.
- OpenAI-native workflow features, Codex workflow sources, and the optional Superpowers lane now have initial raw and entity coverage, but the small-core-plus-retrieval pattern and Superpowers task fit have not yet been stress-tested across enough real tasks to count as fully proven.

## Target Architecture

- KYOTA stays file-first and hybrid-ready.
- Repo markdown remains canonical for project state, durable knowledge, and architecture decisions.
- Context selection becomes explicit and auditable through a reusable contract that records goal, exclusions, budget, selected context, omitted context, execution pattern, and verification method.
- Cross-model work is governed by one file-first operating contract instead of drifting into model-specific habits.
- ChatGPT-native surfaces and Codex/OpenAI API surfaces are treated as execution layers around the repo, not as the repo’s memory substrate.
- Codex gets a compact standing memory core plus a curated frontier-source watchlist instead of a broad wiki preload.
- Runtime-local execution helpers such as Superpowers may tighten implementation discipline without becoming memory systems or creating a second canonical layer.
- The workflow is tightened through pilots on recurring task classes, with only proven rules graduating into `schema/`.

## Operating Rules

1. Default to `tight` or `standard` budget unless ingestion, contradiction resolution, or audit work proves `large` is necessary.
2. Every non-trivial task must declare what was intentionally not loaded.
3. Prefer `/entities/` over `/raw/` unless source verification or ingestion is the work.
4. Default new research to `NOOP` unless it changes behavior, policy, or execution quality.
5. Treat repo files as canonical across Claude, Codex, ChatGPT Projects, ChatGPT Tasks, and future OpenAI API workflows.
6. Treat model lanes as routing preferences, not permanent ownership.
7. Update this roadmap in place. Promote only tested, durable rules into `schema/`.
8. Keep the `Decisions` section short and rolling; rely on git history for the full archive.

## Model Lanes

- `Claude Code ("Kim")` remains in the loop as a peer specialist under the shared KYOTA contract.
- `OpenAI / Codex` is preferred for long-horizon coding, large-context repo reasoning, and high-throughput workflows when the operator’s paid limits make that worthwhile.
- `Superpowers` is an optional Codex-side execution lane when the active session exposes it; it is not a required default and does not change canonicality.
- `Claude` is preferred when local conventions, MCP integrations, or a second-pass critique posture are the tighter fit.
- `ChatGPT Projects` are useful as work containers; `Tasks` are useful as reminders or recurring triggers; `Memory` is useful for operator preferences. None of those are canonical project state.
- Future OpenAI API adoption should wrap the repo rather than replace repo memory. If API work becomes operational, use the current official pro and Codex docs as routing hints, then re-check them before durable updates.

## Next Steps

### Phase 1 - Landed

- [x] Add `schema/context_selection_contract.md`.
- [x] Add `schema/multi_model_operating_contract.md`.
- [x] Add this roadmap file as the architecture control document.
- [x] Add lightweight retrieval guidance to startup surfaces and high-traffic workflow pages.
- [x] Add official OpenAI vendor notes to `raw/` and `entities/`.
- [x] Add `tasks/codex-frontier-source-program.md` as the high-value source radar for Codex, agent, and memory guidance.
- [x] Add `entities/codex_memory_core.md` as the default Codex repo brain.
- [x] Add `raw/superpowers_plugin_2026-04-21_raw.md` and `entities/superpowers_operating_notes.md`.
- [x] Document Superpowers as an optional Codex execution lane in the shared contract and Codex routing docs.

### Phase 2 - Tighten The Workflow

- [x] Pilot the context-selection contract on one routine `fidesz-sapka-site/` edit and record the selected vs. omitted context.
- [x] Pilot the contract on one research-ingestion task and confirm the end state is exactly one of `ADD`, `UPDATE`, `DELETE`, or `NOOP`.
- [ ] Pilot the contract on one architecture/planning task and capture what context was actually wasted.
- [ ] Run the first monthly review of `tasks/codex-frontier-source-program.md` and confirm the canon stays high-signal instead of drifting into commentary.
- [ ] Pilot the optional Superpowers lane on one real implementation or debugging task and record whether it improved execution quality enough to keep using it.
- [ ] Update this roadmap with any rule changes discovered during those pilots.

### Pilot Notes

- **2026-04-21 — Site-context pilot**
  Task class: routine `fidesz-sapka-site/` fast-path edit.
  Selected context: `kyota-wiki/NOW.md`, `kyota-wiki/schema/fidesz_sapka_single_prompt_workflow.md`, `fidesz-sapka-site/CLAUDE.md`, and `fidesz-sapka-site/src/layouts/Base.astro`.
  Omitted context: broader KYOTA entities, raw source packs, `tasks/codex-frontier-source-program.md`, `entities/superpowers_operating_notes.md`, and unrelated site files.
  Wasted context: `NOW.md` still contained stale metadata notes that no longer matched the site files, so a separate cleanup was needed after the pilot.
  Rule changes: none; the minimal fast path worked and `npm run build` in `fidesz-sapka-site/` passed.

- **2026-04-21 — Research-ingestion pilot**
  Task class: candidate-queue source review.
  Selected context: `tasks/codex-frontier-source-program.md`, `schema/research_protocol.md`, `entities/ingestion_workflow.md`, `entities/hierarchical_memory_rules.md`, and Simon Willison's `Codex for Open Source` post.
  Omitted context: site files, broader design canon, Superpowers notes, and unrelated raw/entity pages.
  Wasted context: none material.
  Rule changes: source resolved as `NOOP`; it adds ecosystem news but no new recurring Codex workflow behavior for KYOTA.

### Phase 3 - Promote What Proves Durable

- [ ] Move only the rules that survive multiple pilots from this roadmap into `schema/`.
- [ ] Keep tactical backlog, pilot notes, and evolving model-lane guidance here rather than bloating stable schemas.
- [ ] Re-check official OpenAI product guidance before any later revision that depends on plan features, pricing, or model surfaces.

### Pilot Recording Rule

For each pilot above, append or rewrite the relevant note in this file with:

- task class
- selected context
- omitted context
- wasted context, if any
- rule changes, if any

## Decisions

- 2026-04-21 - This roadmap lives in `kyota-wiki/tasks/` until the workflow stabilizes; it is not yet normative schema.
- 2026-04-21 - KYOTA remains file-first even as OpenAI-native workflow features become more attractive.
- 2026-04-21 - Claude Code “Kim” and OpenAI/Codex are peer specialists under one shared KYOTA contract.
- 2026-04-21 - New research defaults to `NOOP` unless it changes behavior, policy, or execution quality.
- 2026-04-21 - Official OpenAI plan assumptions were checked against the current pricing page, Pro help article, and current developer docs for `gpt-5.4-pro` and `gpt-5.2-codex`.
- 2026-04-21 - Codex now uses a small standing wiki core plus targeted retrieval; frontier sources live in a curated monthly watchlist instead of broad preload.
- 2026-04-21 - Superpowers is documented as an optional Codex execution lane only; durable state stays in KYOTA-native files and fallback remains the base KYOTA contract.
- 2026-04-21 - Completed the first site-context and research-ingestion pilots; the fast path held on a minimal load set and the first candidate-queue source resolved cleanly as `NOOP`.

## Update Protocol

1. Rewrite this file in place instead of appending an external ledger.
2. Keep the section structure fixed: `Purpose`, `Current Architecture`, `Target Architecture`, `Operating Rules`, `Model Lanes`, `Next Steps`, `Decisions`, `Update Protocol`.
3. When architecture changes materially, update the affected sections and then roll the newest fact into `Decisions`.
4. If a rule becomes stable across repeated real tasks, promote it into `schema/` and remove the tactical phrasing here.
5. If a workflow idea has not yet survived a pilot, keep it here as roadmap material rather than elevating it into a normative contract.
