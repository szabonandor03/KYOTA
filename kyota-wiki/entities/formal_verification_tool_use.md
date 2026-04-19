# Formal Verification for LLM Tool-Use

**Date:** 2026-04-17
**Source URIs:**
- AI Safety & Formal Methods 2025/2026 literature (Applying Z3 SMT Solvers to LLM Tool Chains)

## Technical Core
By 2025, deploying autonomous agents in high-stakes environments requires bridging the gap between probabilistic text generation and deterministic execution. "Formal Verification for Tool-Use" achieves this by pairing LLMs with Satisfiability Modulo Theories (SMT) solvers, primarily Z3.
Instead of relying on an LLM to self-regulate, the architecture intercepts the LLM's proposed tool arguments. The system translates the arguments and the known system invariants (e.g., `user_role != 'guest' AND resource_id > 10`) into an SMT formula. The Z3 solver evaluates the formula. If the result is `SAT` (satisfiable), the tool executes. If `UNSAT`, the deterministic failure trace is returned to the LLM to trigger a correction loop. This entirely decouples safety guarantees from the LLM's token probabilities.

## Actionable Prompt Fragments

```text
[SYSTEM: FORMAL_VERIFICATION_GATE]
You are generating arguments for the `[TOOL_NAME]` function.
A Static Analysis layer (Z3 SMT Solver) sits between you and the execution engine.
Your arguments MUST satisfy the following invariant formulas:
- INVARIANT_1: `{args.x} >= 0`
- INVARIANT_2: `validate_permission({args.role}) == TRUE`
If you generate arguments that violate these constraints, the execution will be blocked, and you will receive a deterministic `UNSAT` trace. Provide mathematically sound parameters.
```
