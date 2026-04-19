# Raw Search Summary: Python TUI Frameworks (2025/2026)

### Framework Verdict
*   **Textual** is the modern standard for full-screen dashboards (DOM architecture, CSS styling, complex widgets).
*   **prompt_toolkit** is best for interactive REPLs and granular keystroke input handling.
For KYOTA's multi-panel operator dashboard interface, Textual is the correct choice.

### Capability Implementations (Textual)
*   **Async Refresh/Polling**: Do not block the UI. Use Textual's **Worker API** (`@work` or `run_worker()`). Sleep in the worker via `asyncio.sleep()`, and post custom messages (`self.post_message`) to the UI event loop.
*   **Layout and Focus**: Use grid/flexbox CSS on `Container` types to split panels. Focus navigation automatically supports Tab/Shift-Tab. Arrow keys operate inside focused `DataTable`/`Tree`. Use programmatic focus (`self.query_one("#id").focus()`) synced to `BINDINGS` (like "F1") for power navigation.
*   **DOM & Snapshot Testing**: Install `pytest-textual-snapshot` for SVG-based visual regression testing. For logic testing, use `app.run_test()` to return a `Pilot` object, capable of headless `.press()` and `.click()`. Query the UI via `query_one()` and standard python assertions.
*   **Color Limitations**: Native S-tier support for Truecolor. It automatically downscales to 256 colors on fragile terminals. Rely on the `auto` property for automatic black/white threshold contrasting against dynamic background statuses.
