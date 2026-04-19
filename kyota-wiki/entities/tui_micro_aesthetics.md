# TUI Micro-Aesthetics
**Date:** 2026-04-18
**Source URIs:**
- `../raw/premium_tui_design_raw.md`

## Technical Core
KYOTA utilizes character block encoding to simulate high-resolution graphics within the strictly monospaced terminal canvas. We treat the terminal as a matrix of sub-cells.
1. **Braille Mapping for Telemetry:** To achieve sub-cell resolution, use the Braille block ($U+2800$ to $U+28FF$) to increase terminal resolution by $8\times$. This provides smooth edge rendering for graphs and load bars.
2. **Structural Block Elements:** Use block elements ($U+2580$) to simulate drop-shadows under persistent UI modals and create half-block anti-aliasing for dense UI boundaries.
3. **Empty Space as Interface:** Empty space is not a vacuum. Utilize CSS-tier margins (1-2 cells) to let components breathe, mimicking the grid structure of modern desktop apps rather than the squashed layout of legacy terminal monitors.

## Actionable Prompt Fragments
```text
[SYSTEM: UI_MICRO_AESTHETICS_RULE]
When designing structural boundaries or data readouts in the terminal:
1. Ensure the layout includes 1-2 cell margins around core panels.
2. If displaying performance graphs, agent metrics, or loading states, use Braille Unicode mapping to achieve smooth curves and higher resolution constraints.
3. Don't rely solely on basic ASCII (| and -) for borders.
```
