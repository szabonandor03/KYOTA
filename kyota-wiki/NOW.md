# NOW

One file. Current state, blockers, next actions. Updated in place, not appended. Replaces the old `log.md` ledger.

## Active work
**FIDESZ SAPKA site** (`fidesz-sapka-site/`) — Phase 0 locally verified.
- Astro + Tailwind, IBM Plex Sans / Mono, near-black `#0a0a0c` (no pure black).
- File-browser + details-pane artifact layout; Drive raster logo; event-based scan/slice/chroma pulses (not decorative fake-glitch).
- Three pages: `/` (tabular tracks + inline expand/audio), `/photos` (11-photo filename grid), `/videos` (3 raw ambient clips).
- Masters transcoded to 192k MP3 (adide 3:40, kia 2:48, kiraly 2:40). Raw `.mov` clips → web MP4 with posters.
- Build output: 31MB static bundle.
- Design invariants live in [`fidesz-sapka-site/CLAUDE.md`](../fidesz-sapka-site/CLAUDE.md). Read before touching styles.

## Blockers / TBDs before ship
- `src/data/tracks.ts` has `YYYY-XX-XX` placeholders for adide/kia release dates, `TBD` for kiraly day.
- No credits or lyric fragments yet.
- `layouts/Base.astro` footer: `—` placeholders for spotify/yt handles, `szabonandor03@gmail.com` as contact — verify with operator.

## Next actions (in order)
1. Collect TBDs from operator (dates, credits, lyric fragments, handles).
2. Register domain (plan suggests `fideszsapka.hu`).
3. Deploy to Cloudflare Pages via GitHub (static output, 31MB dist).

## Withheld / not shipped
- Album entirely — per FS-003 rollout plan, do not surface.
- Polished MP4s in `site-assets/videos/` (Untitled Project 1–3, frequency_final1, mellownsimi_final1). Phase 2 reveal, not shipped to `public/`.
- `fidesz-sapka-archive/` is the rejected terminal-cosplay version. Do NOT follow its direction; operator rejected "too much terminal."

## Recent decisions (rolling, keep to ~5)
- **2026-04-19** — Ripped out the kyota coordination CLI + TUI dashboard + `log.md` ledger + multi-agent coordination schema. Was built for concurrent-agent coordination; operator runs agents serially. Replaced with this file. See also `fidesz-sapka-site/` design pass.
- **2026-04-19** — FS site redesign: replaced vectorized Drive mark with low-res raster; file-browser + details-pane homepage; IBM Plex Sans/Mono; removed decorative fake-glitch; added brief event-based scan/slice/chroma corruption grounded in KYOTA design canon.
- **2026-04-18** — FS-003 "király" campaign plan persisted at [`entities/rollout_fs003_campaign_plan.md`](./entities/rollout_fs003_campaign_plan.md). Catalog: FS-001 adide, FS-002 kia, FS-003 király on Drive-logo covers (black/purple). Album direction: Drive logo on white, more pixelated than singles.
- **2026-04-18** — Operator profile at [`entities/operator_profile.md`](./entities/operator_profile.md) points to FS-003 as the tactical priority; prep window 2026-04-18 → 2026-04-25, campaign 2026-04-26 → 2026-05-09, paid boost 2026-05-02.

## Plan file (external)
`~/.claude/plans/what-were-we-doing-deep-moonbeam.md` — deeper spec for the FS site build.
