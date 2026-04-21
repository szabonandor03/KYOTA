# Karpathy LLM Wiki And Autoresearch

Retrieved: 2026-04-21

## Source URLs

- https://gist.github.com/karpathy
- https://github.com/karpathy/autoresearch
- https://github.com/karpathy/autoresearch/blob/master/program.md

## Scope

This note captures the Karpathy patterns most relevant to KYOTA: externalized agent memory, accumulation over repeated retrieval, and Markdown instructions as durable “org code” for long-running agent loops.

## LLM Wiki

Direct-source facts checked on 2026-04-21:

- Karpathy describes `llm-wiki.md` as a pattern for building personal knowledge bases using LLMs.
- The gist is explicitly written as an idea file to be copied into an LLM agent such as Codex or Claude Code, then adapted collaboratively.
- The core critique is that ordinary RAG and uploaded-document flows rediscover knowledge from scratch on every question instead of accumulating useful memory.
- The pattern’s value proposition is compounding knowledge, not merely better one-shot retrieval.

## Autoresearch README

Direct-source facts checked on 2026-04-21:

- Karpathy frames `autoresearch` as an overnight autonomous experiment loop where the agent modifies the system, evaluates the result, keeps improvements, and discards failures.
- The README says the human is not primarily programming Python files directly; instead, the operator is programming the Markdown `program.md` files that provide context to the agents and define the research organization.
- The repo explicitly treats Markdown instructions as durable steering code for the agent loop.

## program.md

Direct-source facts checked on 2026-04-21:

- `program.md` defines the in-scope files, allowed edits, logging rules, branch naming, and the experiment loop.
- The loop is simple and explicit: inspect current state, change the editable file, commit, run the experiment, extract metrics, record results, keep wins, revert losses, and continue.
- Results are logged to a TSV outside the committed experiment history, which separates durable experiment memory from the code changes themselves.
- The file treats the Markdown program as the control surface for the agent rather than as a disposable prompt.

## Raw Implications (Not Yet Distilled)

- Karpathy’s current public patterns strongly support turning KYOTA into an externalized memory layer that accumulates working knowledge over time.
- `llm-wiki.md` and `autoresearch` both point toward the same principle: the agent should not depend on remembering everything in context if the durable Markdown control surface can hold the important structure.
