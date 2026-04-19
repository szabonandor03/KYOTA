# KYOTA Research Protocol

## Purpose
This document defines what qualifies as valid source-of-truth material for the KYOTA knowledge base and how agents must acquire it.

## Source-of-Truth Rules
1. Prefer primary sources over summaries, commentary, or derivative blog posts.
2. Preserve raw source artifacts in `/raw/` whenever possible so later agents can audit the original material.
3. Synthesize source material into `/entities/` only after the source has been read directly.
4. Record every ingestion or synthesis action in `../log.md` immediately after the change is made.

## Primary Targets
- Official documentation from model vendors is the default target for best-practice guidance.
- Approved examples include Anthropic documentation such as the Prompt Engineering Interactive Tutorial and OpenAI official materials such as the OpenAI Cookbooks.
- For architectural patterns, target recent peer-reviewed or primary-source technical materials covering LLM OS concepts, multi-agent patterns such as AutoGen, and context-window degradation studies.

## Recency Bias
- Discard prompt-engineering or context-handling advice published before 2024.
- Do not preserve legacy formatting tricks merely because they were once common.
- When multiple valid sources exist, prefer the most recent one that still comes from an official vendor or a primary academic source.

## Search Protocol
- For vendor guidance, prefer direct searches scoped to official domains such as `site:anthropic.com` or `site:openai.com`.
- For academic concepts, search arXiv first using queries such as `Retrieval Augmented Generation`, `Agentic Workspaces`, or `Multi-Agent Coordination`.
- Use recent publication dates as a filter whenever the search tooling supports recency.
- Reject low-signal aggregator content when a primary source is available.

## Human Fallback
- If a target source is blocked by a paywall, CAPTCHA, login wall, or heavy client-side rendering that prevents clean reading, stop the ingestion flow.
- Inform the user that the source could not be accessed safely.
- Request that the user download the raw text or PDF and place it in `/raw/` for controlled ingestion.

## Evidence Handling
- Each entity synthesized from research should name the source, note its publication or retrieval date when known, and distinguish sourced claims from agent inference.
- If the source contains ambiguous or conflicting guidance, capture the conflict explicitly instead of smoothing it over.
