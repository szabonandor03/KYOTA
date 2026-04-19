# Autonomous Verification Loops & Heuristics

**Date:** 2026-04-17
**Source URIs:**
- arXiv 2025/2026 SurveyG & CRITIC-Style Reflector Papers

## Technical Core
The 2025/2026 paradigm for self-correcting agents shifts away from "Prompted Self-Critique" (which suffers from oscillation and degradation) toward deterministic, feedback-driven "Reflector" architectures.
Instead of relying on LLM internal rubrics, cutting-edge agents leverage external execution feedback (compilers, formal verifiers, search queries). Current frameworks feature:
1.  **Learned Gap Modules**: Structuring corrections via object definitions containing claims, verification actions, evidence, and fix prescriptions.
2.  **Execution Feedback Loops**: Iterative cycles based entirely on tool output (e.g., PerfRL, PerfCodeGen).
3.  **Deterministic Governance Frameworks**: In high-stakes environments, replacing "LLM-as-a-Judge" with physics/rule-based validation.
4.  **Hierarchical Agent Coordination**: Dedicated "Evaluation Agents" separated from "Writing Agents" to enforce a rigorous citation and logic graph.

## Actionable Prompt Fragments

```text
[SYSTEM: EVALUATION_AGENT]
You operate as the Deterministic Reflector. 
Do NOT rely on internal intuition. Your sole purpose is to execute the `[VERIFICATION_TOOL]` against the drafting agent's output.
1. Generate a `Verification Action` using the appropriate heuristic.
2. Execute the action and capture the `Execution Feedback`.
3. Construct a `Gap Module` quantifying the difference between the intended outcome and the tool output.
4. Return ONLY the structured Evidence and Fix instructions.
```
