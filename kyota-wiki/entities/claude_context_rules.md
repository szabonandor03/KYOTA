# Claude Context Rules

## Status
- Source class: Official Anthropic documentation
- Retrieved: 2026-04-17
- Latest dated source located during initialization: Anthropic system prompt release notes updated April 16, 2026

## Sources
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role)
- [System prompts release notes](https://platform.claude.com/docs/en/release-notes/system-prompts)

## Canonical Rules
1. Treat context as a curated working memory, not a bucket to fill. Anthropic explicitly notes that recall and accuracy degrade as token count grows, so more context is not automatically better.
2. For long-running conversations and agentic workflows, Anthropic recommends server-side compaction as the primary context-management strategy. Use context editing only for more specialized cleanup such as clearing tool results or thinking blocks.
3. Starting with Claude Sonnet 3.7, requests that exceed the model's context window fail with a validation error instead of silently truncating. Token counting should be used before large requests.
4. Extended thinking tokens count toward the current turn's limit and billing, but previous thinking blocks are automatically stripped from future context calculations by the Claude API.
5. In tool-use flows, thinking blocks must be preserved through the corresponding tool-result turn. Modifying them can break reasoning continuity and cause API errors.
6. Claude Opus 4.7, Claude Opus 4.6, and Claude Sonnet 4.6 have a 1M-token context window. Claude Sonnet 4.5 and Sonnet 4 use a 200k-token context window.
7. Claude 4.5+ models expose context awareness: the model is informed about its token budget and remaining capacity, which improves long-running and multi-window execution.
8. For large inputs around 20k+ tokens, Anthropic recommends placing longform material near the top, putting the query near the end, wrapping documents and metadata in XML tags, and asking Claude to ground answers in quoted evidence before synthesis.
9. Stable role and behavior instructions belong in the API `system` prompt. Anthropic's published claude.ai and mobile-app system prompts are informative but explicitly do not apply to the Claude API.

## KYOTA Implications
- Inference: Entity pages should prioritize compressed, high-signal summaries over maximal transcript capture, because Anthropic's context guidance favors curation over accumulation.
- Inference: Multi-agent or long-horizon runs should persist state to files or git checkpoints so fresh context windows can recover quickly instead of dragging full conversational history forward.
- Inference: When a KYOTA agent works with large source corpora, it should request quote extraction or evidence highlighting before final synthesis to reduce context noise and improve traceability.

## Evidence Notes
- The context windows guide states that long-running workflows should prefer compaction and warns that context rot appears as token counts grow.
- The prompting guide recommends role-setting in the `system` prompt and gives explicit long-context prompt layout guidance for large documents.
- The latest dated system-prompt page found during initialization was updated on April 16, 2026 for Claude Opus 4.7, and it clarifies that those app-level prompts are separate from the API.
