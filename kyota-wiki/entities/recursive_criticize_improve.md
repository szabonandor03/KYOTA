# Recursive Criticize and Improve (RCI)

**Date:** 2026-04-17
**Source URIs:**
- OpenReview & ArXiv Papers on Reflective Architectures (2025/2026)

## Technical Core
By 2025, RCI has transitioned from a specialized prompting technique to a foundational element of "inference-time scaling" in agent design. In complex domains, generating an answer in a single forward pass yields high error rates. RCI resolves this via prompt-chaining loops:
1.  **Drafting Phase:** The model produces an initial plan or answer.
2.  **Critic Phase (Explicit):** A separate contextual prompt strictly forces the model to evaluate the draft against invariant rules without modifying it.
3.  **Improvement Phase:** The generated critique modifies the draft.
Currently, strict "Explicit RCI" (where the critique is captured as an intermediate cognitive step) outperforms "Implicit RCI" for tasks involving rigid constraints.

## Actionable Prompt Fragments

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
