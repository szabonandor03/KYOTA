# Raw Search Summary: Just-In-Time Tool Loading (2025-2026)

### Core Concepts
*   **Context Engineering:** Treating context window as a finite "attention budget".
*   **JIT Tool Loading:** Injecting tool schemas/skills only at exact moment of need to avoid context bloat.
*   **Dynamic Skill-Loading:** Hierarchical, modular skill fetching.

### Context & Architectures
*   **Model Context Protocol (MCP):** The primary standard for managing JIT loading (e.g. Claude Code).
*   **Execution Layer Architectures:** Tools masked/loaded based on task graph (Jenova, Manus, MolClaw).
*   **JitRL:** Continual learning via retrieving relevant experience dynamically (arXiv:2601.18510).
*   **Hierarchy:** L3 strategy, L2 workflow, L1 atomic operations.
