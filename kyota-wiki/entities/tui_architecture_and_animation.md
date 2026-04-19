# TUI Architecture and Animation
**Date:** 2026-04-18
**Source URIs:**
- `../raw/premium_tui_design_raw.md`

## Technical Core
KYOTA operates on Python's Textual framework, implying that layout management must avoid typical integer-division bugs while managing asynchronous state seamlessly.
1. **Fractional Math Foundation:** All pane and panel resizing logic must utilize Python’s `fractions.Fraction` or exact CSS-like percentage grids to guarantee there are never "off-by-one" column gaps or jittered borders when the terminal resizes.
2. **Subtle, Purposeful Animation:** Do not add motion purely for decoration. Use animation strictly to inform state changes. Limit easing curves to spring physics or staggered reveals to imply depth instead of flat sliding.
3. **Curation Over Production & Optimistic UI:** The UI must mask the latency of the underlying Agent. Utilize Optimistic UI techniques (updating interface state immediately) while background tasks process. Hide complex logs behind expandable blocks rather than firehosing the user.

## Actionable Prompt Fragments
```text
[SYSTEM: TUI_ARCHITECTURE_RULE]
When writing layout and animation logic for Textual elements:
1. Guarantee layout stability by utilizing strict layout grid fractions to prevent off-by-one errors during resize events.
2. Implement Optimistic UI rendering. Don't block the visual interface thread while waiting for the LLM to complete a task.
3. Default to curating or collapsing heavy log streams to prevent visual fatigue.
```
