# Task: Codex Frontier Source Program

Authored: 2026-04-21

## Purpose

Track the high-value current sources that should shape Codex use inside KYOTA without turning the wiki into a noisy feed of AI commentary.

## Use When

- reviewing new Codex, agent, or memory sources
- deciding whether a source should enter the KYOTA canon
- refreshing the monthly Codex source radar

## Do Not Load When

- a normal repo task only needs the default Codex core
- the task is consuming already-distilled guidance rather than reviewing sources
- a bounded task contract already provides the exact load set

## Admission Rules

Accept only these source classes:

- official vendor docs, cookbooks, use cases, or engineering posts
- direct personal sources from selected builders when the source is first-hand and directly readable

Reject or block these by default:

- reposts, SEO summaries, or second-hand explainers
- “top 10 AI tools” content
- screenshots of posts without stable readable text
- paywalled, login-blocked, or subscriber-only sources unless the raw text is manually provided

Every reviewed source must end as exactly one of:

- `ADD`
- `UPDATE`
- `DELETE`
- `NOOP`

Default rule:

- if the source does not clearly improve behavior, policy, or execution quality, it is `NOOP`

## Tier 1 Canon

### OpenAI Official

| Source | Why it matters | Current decision | Artifact |
| --- | --- | --- | --- |
| Codex Prompting Guide | Defines current Codex prompting posture, autonomy, compaction, and reasoning guidance | `ADD` | [`../raw/openai_codex_workflow_sources_2026-04-21_raw.md`](../raw/openai_codex_workflow_sources_2026-04-21_raw.md) |
| Agent Skills | Official reusable-workflow format with progressive disclosure | `ADD` | same raw file |
| AGENTS.md guide | Official persistent project-instruction chain | `ADD` | same raw file |
| Save workflows as skills | Direct pattern for converting a successful thread into reusable memory | `ADD` | same raw file |
| Set up a teammate | Long-running durable-thread and automation pattern | `ADD` | same raw file |
| Understand large codebases | Default onboarding and request-flow tracing pattern before edits | `ADD` | same raw file |

### Anthropic Official

| Source | Why it matters | Current decision | Artifact |
| --- | --- | --- | --- |
| Effective context engineering for AI agents | Strongest current framing for tight context and just-in-time retrieval | `ADD` | [`../raw/anthropic_context_and_agent_sources_2026-04-21_raw.md`](../raw/anthropic_context_and_agent_sources_2026-04-21_raw.md) |
| Building agents with the Claude Agent SDK | Strong gather -> act -> verify loop; “give the agent a computer” pattern | `ADD` | same raw file |
| Scaling Managed Agents | Useful separation of session, harness, and execution surfaces | `ADD` | same raw file |

### Direct Personal Sources

| Source | Why it matters | Current decision | Artifact |
| --- | --- | --- | --- |
| Karpathy `llm-wiki.md` | Strong direct argument for accumulated durable agent memory over repeated rediscovery | `ADD` | [`../raw/karpathy_llm_wiki_autoresearch_2026-04-21_raw.md`](../raw/karpathy_llm_wiki_autoresearch_2026-04-21_raw.md) |
| Karpathy `autoresearch` + `program.md` | Strong pattern for Markdown as durable agent control surface | `ADD` | same raw file |
| Simon Willison: Introducing the Codex app | Good field note on skills, automations, and Codex as a general agent harness | `ADD` | [`../raw/simon_willison_codex_notes_2026-04-21_raw.md`](../raw/simon_willison_codex_notes_2026-04-21_raw.md) |
| Simon Willison: How I think about Codex | Good operational framing of Codex as model + harness + surfaces | `ADD` | same raw file |

## Candidate Queue

Review these on the next monthly pass rather than loading them into the core now:

- Anthropic: `Harness design for long-running application development` (2026-03-24)
- Anthropic: `Claude Code auto mode: a safer way to skip permissions` (2026-03-25)
- Anthropic: `Building a C compiler with a team of parallel Claudes` (2026-02-05)
- OpenAI: `Using skills to accelerate OSS maintenance`
- OpenAI: `Building an AI-Native Engineering Team`
- Simon Willison: `Introducing GPT-5.3-Codex-Spark`

## Blocked / Manual Sources

- Geoffrey Huntley: `don’t waste your back pressure` — interesting, but currently blocked by subscriber-only access; do not ingest into active canon without a raw artifact
- ephemeral X / LinkedIn posts with no stable exportable text
- quoted fragments where the original source cannot be preserved cleanly

## Refresh Loop

Run monthly:

1. Review Tier 1 canon first for drift, supersession, or deletion.
2. Review the candidate queue and decide `ADD`, `UPDATE`, `DELETE`, or `NOOP`.
3. Preserve new sources in `/raw/` before distilling them.
4. Update `codex_memory_core.md` only when a source changes recurring Codex behavior.
5. Touch `NOW.md` only if active workflow guidance materially changed.
6. Keep this file as the watchlist; do not turn it into a dumping ground for every interesting post.

## Decisions

- 2026-04-21 - Adopted `primary + direct personal` as the Codex source canon.
- 2026-04-21 - Chose `small core + retrieval` as the default Codex memory mode.
- 2026-04-21 - Chose a monthly source radar instead of weekly churn.
- 2026-04-21 - Rejected second-hand summaries and paywalled sources from active canon.
- 2026-04-21 - Initial canon is Codex-first; do not broaden it into a general “all AI thought leaders” feed unless it changes Codex behavior in KYOTA.
- 2026-04-21 - Reviewed Simon Willison's `Codex for Open Source` and resolved it as `NOOP`; useful ecosystem news, but no new recurring Codex workflow behavior for KYOTA.
