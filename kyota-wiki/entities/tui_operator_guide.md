# TUI Operator Guide

## Purpose
How to actually use the KYOTA dashboard (`kyota tui`) during coordination work. This is the operator-facing companion to [`./tui_framework_evaluation.md`](./tui_framework_evaluation.md), which covers the framework choice and implementation architecture.

## Launch Prerequisites
1. Install the optional Textual extra once:
   ```bash
   python3 -m pip install '.[tui]'
   ```
2. Export an agent identity in the shell that will launch the TUI:
   ```bash
   export KYOTA_AGENT=<your-agent-id>
   ```
   Without `KYOTA_AGENT`, the dashboard still opens in read-only mode. The status strip shows `writes disabled`, and all action keys surface a warning notification instead of mutating.
3. Launch from the repo root:
   ```bash
   kyota tui
   ```
   The dashboard auto-refreshes every 5 seconds by default and reads the same workspace state as `kyota status` / `kyota doctor`.

## Panel Layout
- **Status strip** (top) - workspace name, agent, write-enabled flag, refresh interval.
- **Doctor panel** (`F1`) - health summary: required files, log readability, router parity, active-claim count, blocker count, issue list, and a concrete `Next step`.
- **Active Claims** (`F2`) - agent, verify state (`Pending` / `Verified`), branch, files (first two plus count), note.
- **Unresolved Blockers** (`F3`) - agent, audience, files, note.
- **Recent Records** (`F4`) - type, agent, status, note (filters out system-generated empty HISTORY rows).
- **Detail pane** (`F5`) - full fields for the selected row, including the verification label and whether a claim is `release_eligible`.
- **Help overlay** (`?`) - keyboard cheatsheet.

## Keybindings
| Key | Action |
| --- | --- |
| `q` | Quit |
| `r` | Manual refresh (the auto-refresh keeps running) |
| `/` | Focus the filter input; filter applies to the currently focused table |
| `c` | Claim files (opens multi-select file picker + note) |
| `v` | Verify the selected claim (requires a row in Active Claims) |
| `x` | Release the selected claim (blocked in the TUI until a `VERIFY` exists) |
| `b` | Record a blocker on the selected claim |
| `u` | Unblock the selected blocker (requires a row in Unresolved Blockers) |
| `h` | Hand off the selected claim to another agent |
| `?` | Toggle the help overlay |
| `F1`-`F5` | Jump to doctor, claims, blockers, recent, detail |
| `Tab` / `Shift+Tab` | Move between panels |
| Arrow keys | Move within the focused table |

## Writable Action Modals
Each write opens a Textual modal that validates the inputs before calling the shared action layer (`src/kyota/actions.py`). The CLI and the TUI share that layer, so invariants are identical.

- **Claim (`c`)** - multi-select picker over tracked repo files with a live filter. Requires at least one file and a non-empty note.
- **Verify (`v`)** - single-note modal. Write what evidence justified verification (for example `kyota lint passed + pytest green`).
- **Release (`x`)** - single-note modal. Only opens when the selected claim is already verified. In v2 the TUI intentionally refuses to override an unverified release; use the CLI if you need that override.
- **Blocker (`b`)** - note plus audience field (defaults to `all`).
- **Unblock (`u`)** - single-note modal, applied to the selected blocker row.
- **Handoff (`h`)** - target-agent field plus note. Auto-clears any open blocker on the scope.

All modals accept `Enter` on the note input to submit and `Escape` to cancel. Errors render inline in the modal instead of closing it.

## TUI vs CLI: When to Use Which
Prefer the **TUI** when:
- You want a live view of active claims, blockers, and verification state while editing in a separate editor.
- You are walking through a multi-step flow (for example claim -> blocker -> unblock -> verify -> release) and benefit from seeing state refresh between steps.
- You are learning the workspace and want the doctor panel's guidance and the record detail pane visible at once.

Prefer the **CLI** when:
- You are scripting coordination (one-shot commands in shell history are auditable).
- You need an action the TUI does not expose, specifically `RECOVER` or `HISTORY`.
- You need to override the verify-before-release guard (the TUI v2 enforces it; the CLI `release` action is the escape hatch).
- You are running headless or without the `[tui]` extra installed.

In both cases the mutation path is the same `actions.py` module, so record format, blocker auto-clear on handoff, and lifecycle checks are identical.

## Known Limitations (v2)
- No `RECOVER` binding in the TUI. Stale-scope cleanup happens via `kyota recover` in the CLI after `kyota doctor` / `kyota status` surfaces the stale claim.
- No `HISTORY` binding in the TUI. Append maintenance notes with `kyota history`.
- Release is guarded by the `VERIFY` check. If you need to release an unverified claim intentionally, use the CLI.
- The file picker lists tracked repo files. Untracked paths that still need claims should be added via `kyota claim` on the CLI (or tracked first, then re-opened in the TUI).
- The dashboard is read-mostly unless `KYOTA_AGENT` is set in the shell that launched it; the status strip makes this visible.

## Minimal TUI Workflow
1. `export KYOTA_AGENT=<id>` in the launch shell.
2. `kyota tui` from the repo root; confirm the doctor panel shows `Healthy`.
3. `c` to claim the exact files you will edit; add a scoped note.
4. Leave the TUI open while you edit in your normal editor; the auto-refresh picks up the new records.
5. Run external checks (`kyota lint`, tests) in another shell.
6. Focus the claims table (`F2`), select your claim, press `v`, paste the evidence summary.
7. With the claim now showing `Verified`, press `x` to release and add a short close-out note.
8. Switch to the CLI for `kyota history` to document the completed work.

## Cross-References
- Record catalog, lifecycle flows, and the shared-action-layer principle: [`./multi_agent_coordination.md`](./multi_agent_coordination.md).
- Keybinding-agnostic operator playbook (CLI cheatsheet, troubleshooting, VERIFY evidence standards): [`./specialist_playbook.md`](./specialist_playbook.md).
- Framework rationale and implementation advice: [`./tui_framework_evaluation.md`](./tui_framework_evaluation.md).
