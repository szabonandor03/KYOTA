# Just-In-Time (JIT) Tool Loading

**Date:** 2026-04-17
**Source URIs:**
- Model Context Protocol (MCP) Standards
- JitRL (arXiv:2601.18510) and Execution Layer Architectures

## Technical Core
By 2025/2026, "context engineering" has replaced brute-force context window maximization. By treating the context window as a finite "attention budget," agents prevent hallucination and performance drift. JIT Tool Loading architectures (heavily utilizing Model Context Protocol - MCP) involve a modular skill repository rather than a static system prompt. 
Instead of resident tools, agents employ a multi-tier hierarchy (L3 Strategy -> L2 Workflow -> L1 Atomic Operations). At test-time, "Execution Layers" fetch specific tool schema definitions dynamically from a structured registry (often via RAG over tools) to construct the prompt on-the-fly, reducing context pollution.

## Actionable Prompt Fragments

```text
[SYSTEM: SKILL_ROUTER]
You are the Context Engineer. Your working context limit for tools is strict.
1. Analyze the current sub-task.
2. Query the `Tool Registry` via the [MCP_INDEXER] for ONLY the necessary operations (Tier 1 & Tier 2).
3. Inject the retrieved schemas into the working memory payload for the immediate execution tick ONLY.
4. CRITICAL: Unload all tool schemas from working memory the moment execution yields a terminal state.
```
