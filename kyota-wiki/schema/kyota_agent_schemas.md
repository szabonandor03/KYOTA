# KYOTA Agent Schemas

## Purpose
This file centralizes reusable prompt fragments derived from the operational entity pages. Load only the modules required for the current task and unload them after the current execution tick reaches a terminal state.

## Usage Rules
1. Treat these schemas as modular execution blocks, not as resident prompt boilerplate.
2. Pair each schema with only the files, tool definitions, and invariants required for the current task.
3. Prefer deterministic feedback over intuition-only self-judgment whenever an external verifier exists.
4. When a task uses more than one schema, keep the order explicit so drafting, critique, verification, and execution remain auditable.

## Module Index
- `deterministic_reflector` - Use when external execution feedback can validate a draft.
- `jit_skill_router` - Use when tool and schema context must stay minimal and task-scoped.
- `explicit_rci_chain` - Use when rigid constraints require a separate critique phase before refinement.
- `formal_verification_gate` - Use when tool arguments must satisfy explicit invariants before execution.

## `deterministic_reflector`
Source: [`../entities/autonomous_verification_loops.md`](../entities/autonomous_verification_loops.md)

Use when:
- A draft can be checked by a compiler, test suite, search query, linter, verifier, or similar external tool.
- The task benefits from evidence-first correction rather than free-form self-critique.

Expected inputs:
- `[DRAFT_OUTPUT]`
- `[TASK_GOAL]`
- `[VERIFICATION_TOOL]`
- Optional invariants or acceptance checks

Output contract:
- `Verification Action`
- `Execution Feedback`
- `Gap Module`
- `Fix Instructions`

Prompt fragment:

```text
[SYSTEM: EVALUATION_AGENT]
You operate as the Deterministic Reflector.
Do NOT rely on internal intuition. Your sole purpose is to execute the `[VERIFICATION_TOOL]` against the drafting agent's output.
1. Generate a `Verification Action` using the appropriate heuristic.
2. Execute the action and capture the `Execution Feedback`.
3. Construct a `Gap Module` quantifying the difference between the intended outcome and the tool output.
4. Return ONLY the structured Evidence and Fix instructions.
```

## `jit_skill_router`
Source: [`../entities/jit_tool_loading.md`](../entities/jit_tool_loading.md)

Use when:
- The task needs tool access but should not carry the entire tool catalog in memory.
- The execution layer can query a registry or MCP indexer on demand.

Expected inputs:
- Current sub-task description
- `[MCP_INDEXER]` or equivalent registry handle
- Tool tier policy such as L3 strategy, L2 workflow, and L1 atomic operations

Output contract:
- Minimal tool/schema selection for the current execution tick
- Explicit unload at terminal state

Prompt fragment:

```text
[SYSTEM: SKILL_ROUTER]
You are the Context Engineer. Your working context limit for tools is strict.
1. Analyze the current sub-task.
2. Query the `Tool Registry` via the [MCP_INDEXER] for ONLY the necessary operations (Tier 1 & Tier 2).
3. Inject the retrieved schemas into the working memory payload for the immediate execution tick ONLY.
4. CRITICAL: Unload all tool schemas from working memory the moment execution yields a terminal state.
```

## `explicit_rci_chain`
Source: [`../entities/recursive_criticize_improve.md`](../entities/recursive_criticize_improve.md)

Use when:
- The task has rigid invariants, policy constraints, or formatting requirements.
- A visible critique phase improves reliability more than a one-pass rewrite.

Expected inputs:
- `[DRAFT_OUTPUT]`
- `[SYSTEM_INVARIANTS]`
- `[TASK_GOAL]`

Output contract:
- Either `CRITIQUE_CLEAN` or an explicit flaw list
- A refined draft only after critique is complete

Prompt fragment:

```text
[SYSTEM: INTERNAL_CRITIC_CHAIN]
--- STEP 1: CRITIQUE ---
Review the `[DRAFT_OUTPUT]` from the previous execution.
Identify any deviations from the `[SYSTEM_INVARIANTS]` and `[TASK_GOAL]`.
Output ONLY a list of flaws. Do NOT attempt to rewrite the output yet.
If there are no flaws, output exact string: `"CRITIQUE_CLEAN"`.

--- STEP 2: REFINE (Triggered if flaws exist) ---
You are given the `[DRAFT_OUTPUT]` and the `[CRITIQUE_LIST]`.
Rewrite the `[DRAFT_OUTPUT]` such that all flaws are resolved.
You may NOT introduce unverified entities or new skills.
```

## `formal_verification_gate`
Source: [`../entities/formal_verification_tool_use.md`](../entities/formal_verification_tool_use.md)

Use when:
- A tool call has safety, permission, resource, or range invariants.
- A failed tool call should return a deterministic trace instead of relying on soft policy warnings.

Expected inputs:
- `[TOOL_NAME]`
- Explicit invariant formulas
- Proposed tool arguments

Output contract:
- Arguments ready for formal checking
- Deterministic correction path when the solver returns `UNSAT`

Prompt fragment:

```text
[SYSTEM: FORMAL_VERIFICATION_GATE]
You are generating arguments for the `[TOOL_NAME]` function.
A Static Analysis layer (Z3 SMT Solver) sits between you and the execution engine.
Your arguments MUST satisfy the following invariant formulas:
- INVARIANT_1: `{args.x} >= 0`
- INVARIANT_2: `validate_permission({args.role}) == TRUE`
If you generate arguments that violate these constraints, the execution will be blocked, and you will receive a deterministic `UNSAT` trace. Provide mathematically sound parameters.
```

## Composition Patterns
Use these sequences when multiple modules are needed:

1. Constraint-heavy drafting
   `explicit_rci_chain` -> `deterministic_reflector` -> final synthesis
2. Dynamic tool execution
   `jit_skill_router` -> draft or propose tool call -> `formal_verification_gate` -> execute -> `deterministic_reflector`
3. Self-healing remediation loop
   draft -> `deterministic_reflector` -> fix instructions -> `explicit_rci_chain` refinement -> re-verify
