# Multi-Agent Coordination

## Canonical Source
- The normative contract lives in [`../schema/multi_agent_coordination.md`](../schema/multi_agent_coordination.md). This page is operational guidance only; if they conflict, the schema wins.
- The executable mutation path is [`../bin/kyota`](../bin/kyota) (CLI) and `src/kyota/actions.py` (the shared action layer the CLI and TUI both call).

## Operating Principles
1. Read [`../index.md`](../index.md), then [`../log.md`](../log.md), then the canonical coordination schema before any write.
2. Treat root files, `/schema/`, `/entities/`, `../entities/index.md`, `../raw/index.md`, and `../log.md` as hotspot files. No hotspot edit without an active `CLAIM`, except for appending a single structured coordination record to `../log.md`.
3. The shared action layer is the only authoritative mutation path. Prefer `../bin/kyota <command>` over hand-editing `log.md`; the CLI enforces lifecycle invariants the schema describes.
4. Ownership scopes should be bounded and explicit. If a task crosses file ownership or blows past the selected budget, stop and re-scope before continuing.
5. Prefer Draft -> Evaluate -> Improve on risky work. Evaluators return evidence and fix instructions; they do not silently rewrite the draft unless they explicitly own the improvement phase.

## Record Catalog
Each record is a single append to `../log.md` in the canonical format. The CLI produces them; avoid hand-authoring except when the CLI is unavailable.

| Record | Purpose | Typical `status` | Who clears it |
| --- | --- | --- | --- |
| `HISTORY` | Document completed ingest/maintenance work. Does not grant ownership. | `done` | terminal |
| `CLAIM` | Assert ownership of a named file scope before editing. | `active` | matching `HANDOFF`, `RELEASE`, or `RECOVER` |
| `BLOCKER` | Announce an impasse on an active claim without releasing it. | `blocked` | matching `UNBLOCK`, `HANDOFF`, `RELEASE`, or `RECOVER` |
| `UNBLOCK` | Clear a blocker while keeping the same active claim open. | `done` | terminal for the blocker, not the claim |
| `HANDOFF` | Transfer ownership to another agent; auto-clears any open blocker on the transferred scope. | `handoff` | the receiving agent's new `CLAIM` |
| `VERIFY` | Capture deterministic evidence that justifies `RELEASE`. Required for non-trivial shared changes. | `passed` | terminal |
| `RELEASE` | Close ownership after verification; the normal completion path. | `released` | terminal |
| `RECOVER` | Close an abandoned stale claim or blocker explicitly. Recovery cleanup only, not normal completion. | `recovered` | terminal |

## Lifecycle Flows

### Normal flow
```text
CLAIM (active) -> [edits] -> VERIFY (passed) -> RELEASE (released) -> HISTORY (done)
```
`HISTORY` may be appended before or after `RELEASE`; it documents the work but does not close the claim. Non-trivial shared changes should not be released without a `VERIFY` that cites deterministic evidence (lint output, test results, reflector traces, formal-gate traces).

### Blocked flow
```text
CLAIM -> BLOCKER (blocked) -> UNBLOCK (done) -> VERIFY -> RELEASE
```
`UNBLOCK` clears the blocker without transferring ownership. Use it once the impasse resolves but the same agent continues the work.

### Handoff flow
```text
agent-A: CLAIM -> [partial work] -> HANDOFF (audience=agent-B)
agent-B: CLAIM (accepts the handoff) -> VERIFY -> RELEASE
```
A `HANDOFF` auto-clears any open `BLOCKER` on the transferred scope. The receiving agent records a fresh `CLAIM` on the same files to take ownership.

### Recovery flow (abandoned work)
```text
any agent: RECOVER (recovered)   # replaces the stale CLAIM/BLOCKER on that scope
```
Use `RECOVER` only when the original owner is no longer progressing the work. Do not use it to shortcut normal completion - that is what `RELEASE` is for.

## Staleness and Recovery
1. Staleness is tracked from the most recent open-scope lifecycle activity on a claim, not from the original `CLAIM` timestamp. A long-running claim that keeps logging `BLOCKER`/`UNBLOCK`/`VERIFY` records is not stale.
2. Use `../bin/kyota doctor` or `../bin/kyota status` before choosing recovery; both surface stale scopes so you do not guess.
3. `RECOVER` is for abandoned-work cleanup only. If the original owner is still active or reachable, prefer `HANDOFF` over `RECOVER`.
4. After a `RECOVER`, the next agent re-claims the scope normally before editing; `RECOVER` closes ownership but does not grant it.

## Shared Action Layer
1. `src/kyota/actions.py` is the single authoritative mutation point. Both the CLI (`bin/kyota`) and the Textual TUI call into it, so they enforce the same invariants, ordering, and blocker lifecycle rules.
2. Prefer `../bin/kyota` or the TUI over editing `log.md` by hand. Hand edits bypass lifecycle validation and can produce the exact drift that `../bin/kyota lint` is designed to catch.
3. Treat the CLI as the fast path and the TUI as the operator view over the same actions; neither adds rules of its own.

## Pre-Write Checklist
Before writing to a hotspot file, confirm in order:
1. `../index.md` and the recent `../log.md` window have been read.
2. `BUDGET` and execution pattern (direct / explicit RCI / deterministic reflector / formal gate) are chosen.
3. `../bin/kyota status` shows no overlapping active `CLAIM` on your target scope, and no unresolved `BLOCKER` you are about to step on.
4. Your own `CLAIM` exists and exactly names the files you plan to edit.
5. You know which deterministic evidence (`lint`, `doctor`, tests, reflector output) will justify `VERIFY`.

## Common Failure Modes
- Releasing without a `VERIFY` on non-trivial shared changes. Fix: run `../bin/kyota lint` and any task-relevant tests, record the result in `VERIFY`, then `RELEASE`.
- Claiming a broader file set than you will touch. Fix: keep claims bounded; re-scope and split rather than overclaiming.
- Hand-editing `log.md` and producing malformed records. Fix: use the CLI; run `../bin/kyota lint` to catch drift.
- Using `RECOVER` to close your own in-progress work. Fix: `RELEASE` is the normal path; `RECOVER` is for abandoned scopes surfaced by `doctor`/`status`.
- Letting a `BLOCKER` sit indefinitely. Fix: `UNBLOCK` once the impasse clears, `HANDOFF` if someone else should continue, or `RECOVER` if the work is abandoned.

## Merge Hygiene
- Update registries and `../log.md` in the same unit of work when shared knowledge changes.
- Use explicit `HANDOFF` boundaries between drafting, evaluation, and improvement phases instead of concurrent edits on the same hotspot files.
- Resolve contradictions through the log and the canonical schema, not through undocumented parallel edits.
