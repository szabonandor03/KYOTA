# Premium DX Philosophies
**Date:** 2026-04-18
**Source URIs:**
- `../raw/premium_tui_design_raw.md`

## Technical Core
KYOTA aims to emulate the "Creators-First" ethos found in premium desktop tools like Linear and Raycast, bringing high-end Developer Experience (DX) into the terminal.
1. **Decision-to-Motion Ratio:** Delay and multi-level nesting cause friction. Command routing must be extremely fast, heavily favoring a flat, search-first `Cmd+K` command palette over a nested GUI menu. 
2. **Typography (Geist Methodology):** Typographic execution should represent the coding spirit—minimal, extremely fast to read, and contemporary. Avoid cliché system fonts where a bespoke tech-focused font (if targetable) or strict x-height control provides immediate visual elevation.
3. **Minimalism as Performance:** A UI feels premium when it only shows exactly what is needed at any given second. Manage the backlog of visual information aggressively by hiding complexity until explicitly summoned.

## Actionable Prompt Fragments
```text
[SYSTEM: UI_DX_RULE]
When laying out TUI interfaces:
1. Embed the Command Palette as the centerpiece of interaction. Favor keyboard-first navigation above all else.
2. Optimize for the lowest decision-to-motion latency. Keep menus flat.
3. Suppress visual clutter and treat UI minimalism not just as an aesthetic choice, but as a critical performance feature.
```
