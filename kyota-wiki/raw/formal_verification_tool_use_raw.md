# Raw Search Summary: Formal Verification for LLM Tool-Use (2025-2026)

### Core Concepts
*   **Static Analysis & SMT Solvers:** Using Satisfiability Modulo Theories (SMT) solvers like Z3 to mathematically prove that an LLM's generated tool arguments do not violate system invariants *before* the function executes.
*   **Safety Sandboxing:** Deterministic guardrails where an execution engine blocks the LLM if the formal proof of SMT constraint satisfiability yields `UNSAT`.
*   **Tool Schema Annotation:** Extending JSON/OpenAPI schema for tool calls with pre-conditions and post-conditions defined in formal logic.

### Context in 2025 AI Agent Architectures
*   The fundamental issue with probabilistic models (LLMs) is that they cannot guarantee deterministic safety. 
*   In mission-critical domains (financial, OS-level agents), developers bind Z3 theorems to tool input arguments.
*   The "Tool Executor" layer acts as the Static Analyzer, enforcing strict pre/post invariants. Constraints are compiled into the context window as explicit rules.
