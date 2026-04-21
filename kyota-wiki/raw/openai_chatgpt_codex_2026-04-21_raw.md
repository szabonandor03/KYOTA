# OpenAI ChatGPT + Codex Snapshot (Official Sources)

Retrieved: 2026-04-21

## Source URLs

- https://chatgpt.com/pricing/
- https://help.openai.com/en/articles/9793128-what-is-chatgpt-pro
- https://developers.openai.com/api/docs/models/gpt-5.4-pro
- https://developers.openai.com/api/docs/models/gpt-5.2-codex

## Scope

This note captures the official OpenAI product facts that matter for KYOTA workflow design: ChatGPT plan capabilities, current Pro-tier structure, and the OpenAI surfaces most likely to affect model routing or recurring work.

## ChatGPT Pricing Snapshot

Official pricing page facts relevant to KYOTA on 2026-04-21:

- `Plus` includes advanced reasoning models, expanded deep research and agent mode, expanded memory and context, projects, tasks, custom GPTs, and expanded Codex usage.
- `Pro` includes everything in `Plus` plus `5x or 20x more usage`, `GPT-5.4 Pro`, `maximum Codex tasks`, `maximum deep research and agent mode`, `maximum memory and context`, and expanded projects, tasks, and custom GPTs.
- `Business` includes apps that bring internal tools and data into ChatGPT, shared projects, workspace GPTs, and access to Codex across documents, tools, and codebases.
- `Enterprise` adds a larger context window and enterprise controls.

Feature-comparison facts relevant to memory and recurring work:

- `Tasks` are available on `Plus`, `Pro`, `Business`, and `Enterprise`.
- `Projects` are available across plans, but that does not make them canonical for KYOTA.
- `Memory with past chats` is marked `Expanded` on `Plus` and `Pro`, and `Coming soon` on `Business` and `Enterprise`.
- `Apps connecting to internal tools` are present on `Plus`, `Pro`, `Business`, and `Enterprise`.
- `Company knowledge` appears only on `Business` and `Enterprise`.
- `Developer mode (beta)` appears on `Plus`, `Pro`, `Business`, and `Enterprise`.

## Pro Tier Snapshot

Official help-center facts relevant to subscription planning on 2026-04-21:

- OpenAI currently documents two `Pro` tiers: `$100` and `$200`.
- Both Pro tiers include the same core capabilities.
- The main difference is usage allowance: `$100` is documented as `5x` higher usage than `Plus`; `$200` is documented as `20x` higher usage than `Plus`.
- OpenAI explicitly calls out higher Codex allowances on Pro, with temporary promotional multipliers noted in the help article.
- The help article positions Pro as the plan for users who rely on advanced tools such as `Codex` and `Deep Research` for real projects throughout the week.

## API / Developer Snapshot

Official developer-doc facts relevant to future KYOTA API adoption:

- `GPT-5.4 Pro` is documented as available in the `Responses API` only.
- OpenAI says `GPT-5.4 Pro` is intended for harder, more precise work, may take several minutes on some requests, and should use `background mode` to avoid timeouts.
- `GPT-5.4 Pro` is documented with a `1,050,000` token context window.
- `GPT-5.2-Codex` is documented as an upgraded model optimized for long-horizon, agentic coding tasks in Codex or similar environments.
- `GPT-5.2-Codex` is documented with a `400,000` token context window and supports configurable reasoning effort.

## Raw Implications (Not Yet Distilled)

- ChatGPT individual paid plans now expose enough workflow features that KYOTA needs an explicit rule for what is canonical and what is only an execution surface.
- Current OpenAI guidance suggests separating three layers: repo memory, ChatGPT execution containers, and future API-driven agent surfaces.
- Vendor facts in this note should be re-checked before reuse because OpenAI pricing, tier names, and feature allocations are volatile.
