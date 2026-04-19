# TUI Color and Perception
**Date:** 2026-04-18
**Source URIs:**
- `../raw/premium_tui_design_raw.md`

## Technical Core
KYOTA relies on strict contrast math and perceptual uniformity to ensure the terminal environment feels like a premium desktop application.
1. **The Pure Black Ban:** Never use `#000000` for backgrounds. It causes visual blooming and eye fatigue. Adopt warmup, deep grays similar to the "Mocha" palette (e.g., `#1e1e2e`).
2. **HSL Consistency:** Establish depth and semantic linking using the HSL model rather than raw hex guessing. Maintain consistent Hue angles for neutral elements while varying Saturation and Lightness to distinguish depth.
3. **WCAG Contrast Ratios:** Core content must pass a $4.5:1$ contrast ratio, but secondary/metadata can use explicitly muted tones to establish immediate visual hierarchy without relying on borders. Let the color weight define the border.

## Actionable Prompt Fragments
```text
[SYSTEM: UI_COLOR_RULE]
When assigning colors or themes to the Textual TUI:
1. Ban pure black boundaries. Use warm, deep-gray HSL values for the base application.
2. Employ alpha transparency and contrast math to establish depth, rather than relying on heavy box-drawing characters for basic separation. 
3. Code semantic layers: Ensure the user can visually identify active vs inactive states by color temperature alone.
```
