# NOW

One file. Current state, blockers, next actions. Updated in place, not appended. Replaces the old `log.md` ledger.

## Active work
**FIDESZ SAPKA site** (`fidesz-sapka-site/`) — Phase 0 shipped and live at `https://fideszsapka.hu` as of 2026-04-21.
- Astro + Tailwind, IBM Plex Sans / Mono, near-black `#0a0a0c` (no pure black).
- File-browser + details-pane artifact layout; Drive raster logo; event-based scan/slice/chroma pulses (not decorative fake-glitch).
- Three pages: `/` (tabular tracks + inline expand/audio), `/photos` (11-photo filename grid), `/videos` (3 raw ambient clips).
- Masters transcoded to 192k MP3 (adide 3:40, kia 2:48, kiraly 2:40). Raw `.mov` clips → web MP4 with posters.
- Build output: 31MB static bundle.
- Design invariants live in [`fidesz-sapka-site/CLAUDE.md`](../fidesz-sapka-site/CLAUDE.md). Read before touching styles.
**KYOTA workflow OS** (`kyota-wiki/`) — architecture evolution docs landed on 2026-04-21.
- Roadmap lives at [`tasks/kyota-architecture-evolution.md`](./tasks/kyota-architecture-evolution.md).
- New schema contracts: [`schema/context_selection_contract.md`](./schema/context_selection_contract.md) and [`schema/multi_model_operating_contract.md`](./schema/multi_model_operating_contract.md).
- Current focus: explicit omitted-context records, file-first multi-model rules, optional Superpowers execution-lane rules, and pilot tasks to prove what actually needs loading.
- Codex frontier canon now lives at [`tasks/codex-frontier-source-program.md`](./tasks/codex-frontier-source-program.md).
- Codex default repo brain now lives at [`entities/codex_memory_core.md`](./entities/codex_memory_core.md).
- Optional Codex Superpowers lane now lives at [`entities/superpowers_operating_notes.md`](./entities/superpowers_operating_notes.md).

## Open content / metadata TBDs
- No credits or lyric fragments yet.

## Next actions (in order)
1. Start a fresh Codex task for this repo and verify local `.git` write access at task start; this session can edit files and use the GitHub connector, but cannot create local git lockfiles.
2. Continue stabilization from remote branch `codex/stabilize-worktree-20260421` if the current dirty worktree needs to be preserved or landed through PR.
3. Pilot the context-selection contract on one architecture/planning task and record selected context, omitted context, and wasted context in the roadmap.
4. Run the next candidate-queue source review from `tasks/codex-frontier-source-program.md`.
5. Pilot the optional Superpowers lane on one medium implementation or debugging task if the runtime actually exposes the plugin in-session.

## Withheld / not shipped
- Album entirely — per FS-003 rollout plan, do not surface.
- Polished MP4s in `site-assets/videos/` (Untitled Project 1–3, frequency_final1, mellownsimi_final1). Phase 2 reveal, not shipped to `public/`.
- `fidesz-sapka-archive/` is the rejected terminal-cosplay version. Do NOT follow its direction; operator rejected "too much terminal."

## Recent decisions (rolling, keep to ~5)
- **2026-04-21** — Added repo-root `AGENTS.md` and `fidesz-sapka-site/AGENTS.md` so fresh Codex sessions automatically bootstrap into KYOTA startup rules and the site fast path.
- **2026-04-21** — Site-context fast-path pilot succeeded on a minimal load set: updated the visible archive stamp in `fidesz-sapka-site/src/layouts/Base.astro` and verified with `npm run build`.
- **2026-04-21** — Reviewed Simon Willison's `Codex for Open Source` as the first candidate-queue ingestion pilot and resolved it as `NOOP`; preserved the raw review but made no behavior/entity change.
- **2026-04-21** — Documented Superpowers as an optional Codex execution lane only; durable plans and state stay in KYOTA-native files and fallback remains the standard KYOTA contract when the plugin is not exposed in-session.
- **2026-04-21** — Added `tasks/codex-frontier-source-program.md` and `entities/codex_memory_core.md`; Codex now has a small standing wiki core plus a curated frontier-source watchlist instead of relying on broad preload.

## Plan file (external)
`~/.claude/plans/what-were-we-doing-deep-moonbeam.md` — deeper spec for the FS site build.
