# Creator Web Reference Set (2024–2026)

**Date:** 2026-04-18
**Source URIs:**
- `../raw/creator_websites_and_ai_tools_raw.md` (Section 3)

## Purpose

A curated list of creator and artist sites worth studying as design references. Each entry names the *specific move* the site makes well, the design system in use, and the transferable lesson — so a future agent can borrow the principle without copying the site.

For the principles these references illustrate, see [`creator_web_design_canon.md`](./creator_web_design_canon.md). For tool selection when building inspired by these, see [`ai_creator_website_tools_and_stack.md`](./ai_creator_website_tools_and_stack.md).

## Technical Core

### Category A — Musician and Band Sites

**blonded.co — Frank Ocean.**
- Move: Extreme minimalist e-commerce; releases as "found artifacts."
- System: High-contrast monochrome, geometric sans-serif, no traditional navigation header. Massive whitespace, oversized typography.
- Lesson: Scarcity plus structural rawness creates more desire than a polished store.

**nin.com — Nine Inch Nails.**
- Move: Definitive band archive functioning as a chronological record / news terminal.
- System: Dark-mode brutalism, rigid grid, high-resolution artwork over UI fluff.
- Lesson: Use the site to own your history, not to sell the latest tour.

**nickcave.com — Nick Cave.**
- Move: Unified editorial layout integrating music, ceramics, literature, and the Red Hand Files newsletter.
- System: Serif typography, spacious margins, newsletter integrated as a primary design element.
- Lesson: Large bodies of work require a *publishing* mindset, not a *portfolio* mindset.

**paulmccartney.com — Paul McCartney.**
- Move: Massive legacy archive with modern accessibility and fast interactive timeline.
- System: Clear navigation hierarchy (4–7 items), fast-loading mobile-first structure.
- Lesson: Even massive archives must prioritize performance and mobile navigation.

### Category B — Visual Artist and Designer Sites

**Paul Macgregor — personal site.**
- Move: "Technical Mono" pioneer — site looks like a terminal window.
- System: Monospaced fonts, black/white palette, ASCII art elements.
- Lesson: A site that looks like a tool signals that the creator is a *builder*.

**Samantha Keely Smith — Squarespace-built.**
- Move: Single full-page hero painting as the only landing element.
- System: Minimalist navigation hidden behind an "Enter" button, gallery-grade layouts.
- Lesson: For visual artists, the work is the interface — don't frame it with buttons.

**Jennifer Xiao — Wix-built.**
- Move: "COOL effect" interactive center animation, hover-responsive graphics.
- System: No header or footer, kawaii-inflected brutalism.
- Lesson: If you reject standard navigation, you must give clear visual feedback for every interaction.

**Steeven Salvat — Squarespace-built.**
- Move: Extreme structural simplicity that mirrors the detail of his hand-drawn work.
- System: Slideshow hero, clear tagline, 5-item navigation bar.
- Lesson: The more complex your work, the simpler your website should be.

### Category C — One-Pager / Archive / Experimental Sites

**Canary Yellow — Virgil Abloh archive.**
- Move: Treat products as database entries with unique ID codes (VAA-YYYY-NNN).
- System: File-system listing style; technical specifications presented as metadata.
- Lesson: Identity elasticity is achieved by presenting work as *documented evidence*. **Highest-leverage reference for FIDESZ SAPKA's Drive-archive aesthetic.**

**Studio Brot.**
- Move: Interactive bold typography that changes the entire background on hover.
- System: Brutalist grid lines, monochromatic, unapologetic.
- Lesson: Small bold interaction *moments* can replace complex animations.

**Hot Buro.**
- Move: Simple geometry plus monochromatic palette for a "clean and functional" register.
- System: Asymmetrical grids, minimal text, raw project core.
- Lesson: Monochromatic design directs attention strictly to content.

**Freak Mag.**
- Move: High-contrast, unconventional layouts mirroring edgy editorial content.
- System: Aggressive color blocking, asymmetrical grids.
- Lesson: Brutalism shines when the aesthetic matches the rebellious nature of the content.

## KYOTA Implications

### Direct Mapping for FIDESZ SAPKA

For the FS website specifically, the highest-leverage references are:
1. **Canary Yellow (Virgil Abloh archive)** — closest aesthetic match. The catalog-ID + file-listing logic is exactly what the FS Drive-folder identity gestures at. Study this first.
2. **blonded.co (Frank Ocean)** — for whitespace discipline and "found artifact" presentation of single releases.
3. **Paul Macgregor's personal site** — for "Technical Mono" execution and the terminal-window posture.
4. **nin.com** — for archive-as-news-terminal grammar if the FS site needs a chronological record dimension.

Skip Cute-alism-leaning examples (Jennifer Xiao) for FS — the deadpan posture forbids playful warmth. See [`creator_web_design_canon.md`](./creator_web_design_canon.md).

### General-Purpose Reference Use

When asked to recommend reference sites for any future creator-web project, default to retrieving from this list rather than re-searching the web. Add new entries via the standard ingestion workflow ([`./ingestion_workflow.md`](./ingestion_workflow.md)) when a new exemplar emerges.

## Evidence Notes

- All site URLs and "build platform if known" attributions in the source report come from listicle-style aggregators (Bandtheme, Muzli, Colorlib, SiteBuilderReport). Verify each URL by direct inspection before quoting to a user — sites move, get redesigned, or go dark.
- Build-platform attributions (Squarespace for Smith / Salvat, Wix for Xiao) are particularly weak — verify by view-source or the platform's own showcase pages before relying on them for a stack decision.
- Canary Yellow's "VAA-2026-001" archive-ID format is named in the report's contemporary-exemplar prose — confirm the exact format on the live site before reproducing it as a literal pattern.

## Actionable Prompt Fragments

```text
[SYSTEM: CREATOR_REFERENCE_LOOKUP]
When the operator asks for "sites to study" or "references for the look of X":

1. Retrieve from this entity first. Do not re-search the web unless the operator's project requires a register not represented here.
2. Match the operator's identity posture to the right category:
   - Musician with a back catalog → Category A (blonded, nin, nickcave).
   - Visual artist with hero work → Category B (Smith, Salvat).
   - Archive / catalog / experimental posture → Category C (Canary Yellow, Studio Brot, Hot Buro).
3. For each reference: state the *specific move*, the *system*, and the *transferable lesson*. Do not say "look at this site" without naming what to take from it.
4. For FIDESZ SAPKA specifically, lead with Canary Yellow + blonded.co + Paul Macgregor; skip Cute-alism examples.
5. Always verify each URL is live before sending to the operator.
```
