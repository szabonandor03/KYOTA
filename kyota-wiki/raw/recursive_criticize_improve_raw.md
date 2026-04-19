# Raw Search Summary: Recursive Criticize and Improve (2025-2026)

### Core Concepts of RCI
*   **Mechanism:** An LLM generates an initial response, identifies flaws (criticism phase), and generates an improved version (improvement phase). This is highly recursive.
*   **Approaches:**
    *   **Explicit RCI:** Explicitly prompted to generate critique before improving.
    *   **Implicit RCI:** Prompted to directly update or revise without outputting the critique as a distinct message.

### Context in 2025 AI Agent Architectures
*   **Reflective Architectures:** Aligns with industry shift to "inference-time scaling" and internal critics. RCI acts as a self-healing mechanism.
*   **Integration:** Often combined with CoT and ReAct to vet logic and action execution.
*   **Agentic Frameworks:** Explicit prompt chaining (Prompt A to generate -> Prompt B to critique -> Prompt C to fix) has become canonical over relying on one monolithic prompt.
