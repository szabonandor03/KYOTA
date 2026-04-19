# FIDESZ SAPKA — Design Invariants (v3 — Drive Artifact)

Any edit that breaks one of these is a bug. Read before touching styles or markup.
Full design spec: see `DESIGN_DIRECTION.md`.

## Posture
Archive, not showcase. Drive folder that leaked. Deadpan, Hungarian slang, zero hype language. Never explain the name.

## Visual Concept
Google Drive folder-browsing interface, light mode, real low-res Drive mark, event-based corruption. Pages are folders. Clicking navigates deeper. The feeling is a shared Drive copy that has been screenshotted, re-saved, and passed around too many times.

## Palette
- Background: warm Drive white around `#f3efe7`, not pure white.
- Toolbar bg: pale Drive toolbar tint with translucency.
- Foreground: `#202124`.
- Muted: `#5f6368`.
- Rule: warm divider around `#d6d0c7`.
- Blue accent: `#1a73e8`.
- Folder: `#f4b400`.
- Audio / video: `#ea4335`.
- Image: `#34a853`.

## Type
- **IBM Plex Sans** for body, rows, toolbar, headings.
- **IBM Plex Mono** for dates, file sizes, footer, metadata.
- Body 14/1.45. Mono 11–12.

## Chrome
- Drive-style rows: 48px height, 3-column grid (`Name / Last modified / File size`).
- Blue hover highlight `#e8f0fe`, blue selected `#d2e3fc`.
- 1px borders in `--color-rule`. No shadows. Minimal radius only if a clipped raster surface needs it.
- Use contained surfaces and exposed edges so the archive feels packaged rather than flat.
- Transitions stay brief and linear.

## Corruption
- The old static glitch classes are deprecated. No decorative fake mistakes.
- Corruption should be intermittent and structural: scan pass, horizontal slice, brief chroma split, mild desaturation drift.
- The provided low-resolution Drive image at `/public/brand/drive-logo-source.jpeg` is the canonical brand mark for this phase.
- Any glitch motion must feel like compression failure or screen-capture damage, not a cyberpunk effect pack.
- Reduced-motion users get the static artifact without the pulses.

## Content Shape
- Root `/` remains a folder listing for `tracks/`, `photos/`, `videos/`.
- Root may use a detail pane as a file-browser affordance, not as a hero section.
- `tracks/` lists audio files. Click opens inline player.
- `photos/` is a grid surface with filenames in mono.
- `videos/` lists video files. Click opens inline player.
- Pending / unreleased rows render grayed out with `—`, never hype.
- No `about`, press, merch, newsletter, or social-icon strip.

## Withheld
- The album does **not** appear on the site until the album rollout.
- Do not surface polished hidden videos from `site-assets/videos/` unless the rollout plan changes.
