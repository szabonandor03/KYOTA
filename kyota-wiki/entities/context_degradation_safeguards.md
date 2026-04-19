# Context Degradation Safeguards

## Source Basis
- Derived from `../raw/LLM_OS_Research_Report.md`
- Primary upstream concepts: Anthropic context-engineering failure modes, BEAVER hierarchical compression, and long-context degradation research

## Purpose
Prevent KYOTA agents from degrading reasoning quality as tasks accumulate files, logs, tool outputs, and competing instructions.

## Failure-Mode Rules
1. Guard against context poisoning. Unverified facts, speculative summaries, and model-generated guesses must not be inserted into shared entities as if they were settled knowledge.
2. Guard against context distraction. Load only the files and excerpts needed for the immediate task instead of dumping broad tool output or entire directories into the active context.
3. Guard against context confusion. Do not present overlapping tools, similar documents, or redundant entity pages unless the distinction matters to the task at hand.
4. Guard against context clash. When two sources disagree, name the conflict and resolve it deliberately rather than leaving contradictory guidance side by side without explanation.

## Tool-Output Discipline
1. Tool outputs must be token-efficient. Prefer targeted `rg`, `sed`, or focused test output over whole-file dumps and verbose command transcripts.
2. Summarize large outputs before reusing them. The workspace should carry forward the minimum evidence needed to act, not every intermediate byte.
3. Never paste irrelevant stack traces, logs, or build output into entity pages.
4. When compressing long material, preserve sentence and section boundaries. Do not splice partial sentences into the working context, because fragmented context degrades retrieval and synthesis.

## Context Assembly Rules
1. Put durable constraints near the beginning of a working context and the active question or decision near the end. Do not bury critical instructions in the middle of a long prompt.
2. Prefer just-in-time retrieval over preloading documents "just in case."
3. If a source is large, select at the page, section, or heading level before drilling down to sentence-level evidence.
4. Use quarantine for suspect information: keep it out of shared rules until it has been verified against the source of truth.

## Escalation Triggers
- If the active context starts carrying contradictory facts, repeated summaries of the same material, or large irrelevant tool output, stop and rebuild the context from `index.md`.
- If a task requires too many documents at once, split it into smaller sub-tasks with separate retrieval passes rather than forcing everything through one overloaded window.
