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

## Open content / metadata TBDs
- `src/data/tracks.ts` has `YYYY-XX-XX` placeholders for adide/kia release dates, `TBD` for kiraly day.
- No credits or lyric fragments yet.
- `layouts/Base.astro` footer: `—` placeholders for spotify/yt handles, `szabonandor03@gmail.com` as contact — verify with operator.

## Next actions (in order)
1. Start a fresh Codex task for this repo and verify local `.git` write access at task start; this session can edit files and use the GitHub connector, but cannot create local git lockfiles.
2. Continue stabilization from remote branch `codex/stabilize-worktree-20260421` if the current dirty worktree needs to be preserved or landed through PR.
3. Only touch `fidesz-sapka-site/` for concrete post-launch fixes or content updates after the repo state is stable.
4. If the missing metadata matters, collect the remaining dates, credits, lyric fragments, and footer handles from the operator.
5. Record the actual production host in the wiki once verified; the live domain is confirmed, but the deploy provider is not yet documented here.

## Withheld / not shipped
- Album entirely — per FS-003 rollout plan, do not surface.
- Polished MP4s in `site-assets/videos/` (Untitled Project 1–3, frequency_final1, mellownsimi_final1). Phase 2 reveal, not shipped to `public/`.
- `fidesz-sapka-archive/` is the rejected terminal-cosplay version. Do NOT follow its direction; operator rejected "too much terminal."

## Recent decisions (rolling, keep to ~5)
- **2026-04-21** — Fixed GitHub connector access for `szabonandor03/KYOTA`; the app can now see the repo and create remote branches. Created `codex/stabilize-worktree-20260421` as the stabilization branch.
- **2026-04-21** — Confirmed this specific Codex session still cannot write under `.git` (`.lock` creation fails with `Operation not permitted`). Repo cleanup must continue in a fresh task that re-tests local git permissions.
- **2026-04-21** — Confirmed the FIDESZ SAPKA site is live at `https://fideszsapka.hu`. Updated `NOW.md` to remove stale pre-launch actions and treat deployment as complete.
- **2026-04-21** — Formalized the repo git contract in [`schema/version_control_workflow.md`](./schema/version_control_workflow.md): clean start from `main`, short-lived task branches, PR-first landing, explicit exceptions for direct `main` commits, and branch cleanup after merge.
- **2026-04-19** — Ripped out the kyota coordination CLI + TUI dashboard + `log.md` ledger + multi-agent coordination schema. Was built for concurrent-agent coordination; operator runs agents serially. Replaced with this file. See also `fidesz-sapka-site/` design pass.
- **2026-04-19** — FS site redesign: replaced vectorized Drive mark with low-res raster; file-browser + details-pane homepage; IBM Plex Sans/Mono; removed decorative fake-glitch; added brief event-based scan/slice/chroma corruption grounded in KYOTA design canon.

## Plan file (external)
`~/.claude/plans/what-were-we-doing-deep-moonbeam.md` — deeper spec for the FS site build.
