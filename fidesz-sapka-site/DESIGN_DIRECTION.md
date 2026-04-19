# FIDESZ SAPKA — Design Direction (v3)

> Living document. Updated by multiple sessions.
> Last updated: 2026-04-19 by Codex.

## Core Concept

**Google Drive folder-browsing aesthetic, treated as a damaged artifact instead of a themed clone.**

The site should feel like clicking through someone's shared Drive folders — file lists, folder icons, breadcrumbs, "last modified" columns — but as if the whole thing has already been screen-captured, cropped, re-uploaded, and compressed a few times. Not parody-Drive, not UI cosplay. The degradation has to feel incidental and material.

This connects to the existing visual identity: the actual low-resolution Google Drive logo reference used on Instagram, the "archive leak" tone from the operator profile, and the white/purple/black compression arc across the catalog.

## Resolved Decisions

- **Light mode.** Warmed, corrupted white/light gray — like Drive after recompression.
- **Glitch as event, not decoration.** Brief scan passes, chroma slip, and slice tears. Kill the fake typo / wrong-row-height gags.
- **Folder navigation.** Root `/` shows folders (`tracks/`, `photos/`, `videos/`). Clicking a folder opens the file listing. Clicking a file plays or opens it.
- **Iconic elements only.** Keep breadcrumb path, column headers, folder/file icons, selection highlight, toolbar shape, and a detail-pane logic. Kill everything else.
- **Real logo source.** Use the provided low-resolution raster Drive logo directly, not a vector redraw.

## Visual Spec

### Palette
- Background: warm Drive white in the `#f3efe7` range, not clean product white.
- Foreground: `#202124`.
- Muted: `#5f6368`.
- Blue accent: `#1a73e8`.
- Folder yellow: `#f4b400`.
- Rules: warm divider lines around `#d6d0c7`.
- Surface bruising: pale green/yellow/blue tints sampled from the logo should appear as subtle stains, not graphic blocks.

### Typography
- Primary: `IBM Plex Sans`.
- Mono elements: `IBM Plex Mono`.
- Typography should feel technical and load-bearing, not generic product UI.

### Layout
```text
/
├── toolbar
├── breadcrumb
├── file list
└── details pane
```

The details pane should behave like a browser affordance, not a promotional hero. It is there to reinforce the archive metaphor and show the raster mark with weight.

### Corruption Vocabulary
- Low-opacity full-surface noise/grain.
- Rare global scanline passes, like a partial capture refresh.
- Brief horizontal slice tears that shift one band of the page.
- Chroma split on the title/logo only during pulses.
- Raster imagery stays visibly low-res and uses `image-rendering: pixelated`.
- No constant RGB text shadow, no fake typo corruption, no hover gimmicks.

## What This Replaces

The previous Drive pass had the correct navigation grammar but handled glitch mostly as decorative CSS. This v3 pass keeps the Drive grammar while making the damage feel structural and the overall surface feel more authored.

## Invariants That Carry Over

- **Posture:** archive, not showcase.
- **No catalog IDs** on the visible surface.
- **No about / press / merch / newsletter.**
- **Pending or unreleased entries = `—` / `pending`, never hype.**
- **The album does not appear until rollout.**
- **Hungarian slang, deadpan tone.**

## Assets

- 3 audio tracks: adide, kia, kiraly.
- 12 photos.
- 3 ambient video clips.
- 1 canonical low-resolution Drive mark at `/public/brand/drive-logo-source.jpeg`.
