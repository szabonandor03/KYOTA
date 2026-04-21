# CODEX Routing

You are a Specialist Agent in the KYOTA workspace. Either agent (Claude or Codex) operates under the same contract: recover state from `index.md` and `NOW.md`, execute bounded tasks, minimize operator cognitive load, report concise state changes.

## Startup order
1. Read [`index.md`](./index.md).
2. Read [`NOW.md`](./NOW.md) — current state, blockers, next actions.
3. If the task is a concrete `fidesz-sapka-site/` edit, follow [`schema/fidesz_sapka_single_prompt_workflow.md`](./schema/fidesz_sapka_single_prompt_workflow.md) and do not ask follow-up questions unless that schema requires escalation.
4. Otherwise, ask the operator 1-3 short questions about what they are thinking about, the desired outcome, and anything that should be excluded.
5. Set `BUDGET`: `tight` / `standard` / `large`.
6. `SELECT` only the entity pages, prompt fragments, and raw sources the task needs.
7. Choose execution pattern: direct execution, explicit RCI, deterministic reflector, or formal-gated tool use.
8. `GENERATE` after selection is complete.

## Operating rules
- `/schema/` is the normative rules layer. `/entities/` is derived operational guidance.
- Read [`schema/research_protocol.md`](./schema/research_protocol.md) before ingesting external sources.
- Follow [`schema/fidesz_sapka_single_prompt_workflow.md`](./schema/fidesz_sapka_single_prompt_workflow.md) for bounded website edits in `fidesz-sapka-site/`.
- Follow [`schema/version_control_workflow.md`](./schema/version_control_workflow.md) for any lasting repo change; do not improvise ad hoc git process.
- Treat [`schema/kyota_agent_schemas.md`](./schema/kyota_agent_schemas.md) as a reusable prompt-fragment library; select only the modules the task needs.
- Use [`entities/index.md`](./entities/index.md) and [`raw/index.md`](./raw/index.md) for discovery; do not expand the root `index.md`.
- Do not decide the deeper load set before the operator-intake step, except for the explicit one-prompt website fast path. Otherwise ask first, then budget, then select.
- For rigid or high-risk tasks, prefer explicit `Draft → Critique → Refine` or a deterministic reflector loop over one-pass generation.
- When tool calls carry safety / permission / range invariants, require a deterministic gate before execution and use failure traces to drive correction.
- Keep user-facing output concise: `Outcome`, `State changes`, `Risks / Needed reroute`. Hide raw tool logs unless asked.

## Updating NOW.md
`NOW.md` is rewritten in place, not appended to. When current state changes materially:
- Move stale items out of **Active work** / **Blockers** when they no longer apply.
- Bump **Recent decisions** — keep roughly the last 5; drop older ones (git history preserves them if needed).
- Leave the file under ~100 lines. If it grows larger, you have context rot in the note itself — trim.

## Coordination (if it ever comes up)
This workspace is single-operator, serial-agent. There is no concurrent multi-agent coordination layer. If two agents ever need to work the same files simultaneously, use git branches + PRs, not an in-repo mailbox.
