# Python TUI Framework Evaluation (2026 Edition)

**Date:** 2026-04-17
**Source URIs:**
- textualize.io & pytest-textual-snapshot github

## Technical Core
Based on the `kyota` workspace requirements—which demand a file-backed, multi-panel dashboard for operational safety rather than a simple CLI command wrapper—**Textual** is the definitive 2025/2026 framework of choice. While `prompt_toolkit` remains the standard for REPLs and raw CLI input loops, Textual offers a complete DOM, CSS-like deterministic styling, and a pre-built widget library (`DataTable`, `Tree`) that aligns flawlessly with dashboard architectures.

**Key Architecture Advice for KYOTA TUI:**
1. **Async & Refreshing**: To prevent UI locking when reading heavily from `kyota-wiki/log.md`, leverage Textual's `Worker API` (`@work`, `run_worker`) coupled with `asyncio.sleep` polling and custom application Messages (`post_message`). Do not run synchronous file reads directly in the reactive event loop.
2. **Layout & Focus**: Utilize `Container` classes with CSS grid/horizontal split layouts. Rely on standard browser-like Tab/Shift-Tab focus loops, but explicit programmatic focus (`widget.focus()`) bound to function keys (e.g., F1 for claimed tickets, F2 for blockers) should be mapped for operations.
3. **Safety via Testability**: Textual provides a `Pilot` class (`app.run_test()`) to programmatically click/type through the UI and assert DOM updates headless. Use `pytest-textual-snapshot` to generate SVG assertions of the dashboard state to guarantee UI invariables without manual inspection.
4. **Color Resilience**: Terminal compatibility varies wildly across OS defaults. Rely entirely on Textual's core color mapping which falls back to 256 colors gracefully. Use the `auto` contrast property on text instead of hardcoding ANSI strings, preventing unreadable layouts in light-mode terminals.

## Actionable Prompt Fragments

```text
[SYSTEM: TUI_IMPLEMENTATION_AGENT]
You are tasked with building the KYOTA operational dashboard using Textual.
- Use `<Container>` and CSS for all split layouts. 
- Use `@work` for async polling of the Markdown files, and `post_message` to update reactive widget properties.
- NEVER block the main thread with synchronously heavy file I/O operations.
- Bind F-keys to `action_focus_x` methods for rapid dashboard navigation.
- Your output must explicitly include the necessary `pytest` stubs utilizing `app.run_test()` to verify logic paths for claim/release UI components.
```
