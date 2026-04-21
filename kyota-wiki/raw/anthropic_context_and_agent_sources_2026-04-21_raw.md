# Anthropic Context And Agent Sources

Retrieved: 2026-04-21

## Source URLs

- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://claude.com/blog/building-agents-with-the-claude-agent-sdk
- https://www.anthropic.com/engineering/managed-agents

## Scope

This note captures the Anthropic engineering guidance that most directly informs Codex-side memory and workflow design inside KYOTA: context engineering, agent loops, subagents, compaction, and the separation of durable state from the active context window.

## Effective Context Engineering For AI Agents

Official Anthropic facts checked on 2026-04-21:

- Anthropic describes context as critical but finite, and frames context engineering as optimizing token utility rather than simply increasing token volume.
- The post explicitly distinguishes prompt engineering from context engineering: prompts are only one part of the overall context state.
- Anthropic recommends curating a minimal viable toolset because overlapping or ambiguous tools create unreliable behavior.
- The post recommends a small number of diverse, canonical examples instead of stuffing a prompt with exhaustive edge-case rules.
- Anthropic highlights just-in-time context retrieval and agentic search as a strong alternative to broad preloading.

## Building Agents With The Claude Agent SDK

Official Anthropic facts checked on 2026-04-21:

- Anthropic’s core design principle is to give the agent a computer so it can work like a human operator: search files, edit files, run commands, and iterate.
- The article frames a useful agent loop as `gather context -> take action -> verify work -> repeat`.
- Anthropic recommends starting with agentic search over the file system and only adding semantic search if speed or variability truly requires it.
- The post says subagents are useful both for parallelization and for context isolation because they keep most of their context out of the orchestrator’s window.
- Anthropic calls compaction a first-class tool for long-running agent work as context approaches the model limit.

## Scaling Managed Agents

Official Anthropic facts checked on 2026-04-21:

- Anthropic frames long-running agent design around stable interfaces that can outlast a particular harness implementation.
- The article separates the “brain” from the “hands” and the “session.”
- The session is an append-only event log outside the immediate context window, making durable recoverable state a separate concern from the active inference context.
- Anthropic explicitly says the harness can transform fetched events before reinserting them into context, which keeps durable storage and context engineering separate.
- The post argues that many-brains and many-hands systems work better when the interfaces stay stable and each component can fail independently.

## Raw Implications (Not Yet Distilled)

- Anthropic’s current engineering guidance strongly reinforces KYOTA’s existing file-first, just-in-time retrieval approach.
- The most relevant new additions for Codex-side use are the explicit `gather -> act -> verify -> repeat` loop, stronger support for subagents as context-isolation tools, and the separation between durable session state and the active context window.
