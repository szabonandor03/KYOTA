# Intent Routing Architecture

## Source Basis
- Derived from `../raw/UX_HCI_Research_Report.md`
- Primary upstream concepts: intent-based orchestration, unified entry-point routing, and staged tool invocation
- Operationally extended by `./autonomous_verification_loops.md`, `./jit_tool_loading.md`, `./recursive_criticize_improve.md`, and `./formal_verification_tool_use.md`

## Purpose
Define how KYOTA should transform user intent into bounded specialist work without exposing routing complexity to the user or binding tasks to a specific model name.

## Canonical Flow
1. Intent Understanding: infer the user's real objective, requested deliverable, and risk level.
2. Risk and Invariant Extraction: identify whether the task needs explicit constraints, deterministic verification, or formal tool gating.
3. Task Decomposition: split the objective into bounded work units with explicit file or knowledge ownership.
4. Context Assembly: select only the files, prompt fragments, invariants, and tool schemas needed for the immediate execution tick.
5. Drafting: produce the initial plan, answer, patch, or proposed tool call.
6. Critique or Reflection: use explicit RCI for rigid constraints and deterministic reflector loops when external verification is available.
7. Formal Tool Gate: validate proposed tool arguments against invariants before execution when failure cost is non-trivial.
8. Execution and Recovery: execute approved actions, feed tool output back into refinement when checks fail, and unload tool schemas at terminal state.
9. Completion Review: verify whether the result solved the original intent and whether follow-up routing is needed.

## Routing Rules
1. The Orchestrator must route by intent and risk, not by whichever tool looks convenient first.
2. A task should be split only when the subtasks have clean boundaries and materially reduce risk, latency, or context load.
3. Use explicit RCI when critique quality matters or the task has rigid invariants that should be checked before revision.
4. Separate drafting from evaluation when deterministic verification materially reduces risk.
5. Do not spawn multiple specialists onto the same hotspot file unless the work is explicitly serialized.
6. If decomposition would create more coordination overhead than execution savings, keep the task with one specialist.

## Interchangeable Specialist Assignment
- Route to any available specialist agent that can honor the current claims, selected budget, and required file scope.
- Agent identity must not change startup sequence, state recovery, or coordination requirements.
- Use multiple specialists only when file scopes or outputs can be separated cleanly.
- When more than one specialist is involved, the Orchestrator should define handoff order explicitly. Keep handoff notes inside `NOW.md` so the next agent can pick up cold. For concurrent multi-agent work (rare), use git branches + PRs rather than an in-repo coordination ledger.
- Prefer the specialist with the smallest additional context load or the existing claim on the relevant files.

## Tool Discipline
1. Use the smallest viable toolset for each subtask and load it just in time.
2. Keep tool schemas and invariants ephemeral; unload them after the current execution tick reaches a terminal state.
3. Keep evidence collection separate from final synthesis when possible.
4. Place formal invariants between proposed tool arguments and execution when the task is high stakes.
5. Reflection must compare the output against the original intent and deterministic feedback, not only against local task completion.

## Failure Policy
- If a specialist notices intent drift, hidden dependency, or ambiguous ownership, it must stop broadening scope and return a routing summary for the Orchestrator.
- If critique, reflector, or formal-gate output reports a defect, reroute into a bounded improvement cycle instead of improvising a new task.
