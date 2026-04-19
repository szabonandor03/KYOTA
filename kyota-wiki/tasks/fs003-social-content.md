# Task: FS-003 social content prep (prep window)

Authored: 2026-04-19. Window: 2026-04-19 → 2026-04-25 per `entities/rollout_fs003_campaign_plan.md` prep phase.

## Scope

Prepare the social content queue for the FS-003 "király" 14-day catch-up campaign (campaign run: 2026-04-26 → 2026-05-09). This task covers caption drafting, post sequencing, and asset selection from material that already exists. It does not cover: shooting new material, design of new graphics, paid boost setup (that is a separate task scheduled for 2026-05-02), or anything cross-promoted with Gyuris (rejected per memory).

## Done criteria

- [ ] Caption queue exists at `tasks/fs003-social-content.queue.md` with at least 8 posts spanning the campaign window
- [ ] Each post specifies: date, channel (IG / TikTok), asset reference (file in `Desktop/FIDESZ SAPKA/video/` or photo set), caption text, post-type (raw video / photo / archive leak)
- [ ] No post uses composed-typography graphics, lyric posters, or "OUT NOW" overlays (rejected per `feedback_authenticity_over_composed_graphics.md`)
- [ ] No post leverages Gyuris cross-promo (rejected per `feedback_no_gyuris_cross_promo.md`)
- [ ] All captions read deadpan, Hungarian-slang-aware, archive-leak tone (per `fidesz-sapka-site/CLAUDE.md` posture)
- [ ] Queue references the four rollout principles where applicable (Hidden Hand, Moral Economy, Narrative Labor, Historical Artifact) — agent annotates which principle each post enacts

## Autonomy scope

- Decide caption phrasing without checking — use operator profile and FS posture as the calibration
- Decide post-type mix and channel split (IG vs TikTok) — bias toward TikTok per handoff finding
- Decide post sequencing across the 14-day window
- Choose between available raw assets — prefer the rawest, most documentary-feeling material
- Default to "release as-is" over "polish first" when a raw asset is borderline
- Skip the Day 11–12 playlist question (open per handoff; not blocking content prep)
- If a caption draft feels even slightly hype-y, rewrite without asking

## Escalation conditions

- If preparing a post would require touching the album (withheld until rollout) — stop and ask
- If a post would require surfacing the FS-001/FS-002/FS-003 catalog IDs publicly — stop and ask
- If you find raw assets that read as "polished MP4s" rather than camcorder-grade — confirm before queueing
- If the rollout principles feel like they're producing the same post twice in a row — flag for operator review

## Context budget

standard

## Files to load

- `kyota-wiki/NOW.md`
- `kyota-wiki/entities/operator_profile.md`
- `kyota-wiki/entities/rollout_fs003_campaign_plan.md`
- `kyota-wiki/entities/rollout_hidden_hand.md`
- `kyota-wiki/entities/rollout_moral_economy.md`
- `kyota-wiki/entities/rollout_narrative_labor.md`
- `kyota-wiki/entities/rollout_historical_artifact.md`
- `kyota-wiki/handoff_from_antigravity.md`
- `fidesz-sapka-site/CLAUDE.md` (posture/tone reference only)
- Directory listing of `~/Desktop/FIDESZ SAPKA/video/` to identify available raw assets

Do not load: schema/, execution-pattern entities, tui_*, web design canon, raw/ source files.

## Output artifact

- Write `kyota-wiki/tasks/fs003-social-content.queue.md` containing the post queue in a single-table format (one row per post)
- Add one line to `kyota-wiki/NOW.md` under **Recent decisions**: `YYYY-MM-DD — FS-003 social queue drafted at tasks/fs003-social-content.queue.md, N posts across [channels]`
- Do not commit; leave staged for operator review
