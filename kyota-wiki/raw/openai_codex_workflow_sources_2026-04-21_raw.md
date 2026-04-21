# OpenAI Codex Workflow Sources

Retrieved: 2026-04-21

## Source URLs

- https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/use-cases/reusable-codex-skills
- https://developers.openai.com/codex/use-cases/proactive-teammate
- https://developers.openai.com/codex/use-cases/codebase-onboarding

## Scope

This note captures the official OpenAI guidance that most directly changes how KYOTA should use Codex in day-to-day repo work: prompting posture, reusable skills, persistent project instructions, long-running teammate threads, and large-codebase onboarding.

## Codex Prompting Guide

Official cookbook facts checked on 2026-04-21:

- OpenAI positions Codex as its recommended agentic coding model.
- The guide recommends `medium` reasoning effort as the default interactive balance and `high` or `xhigh` for the hardest long-running work.
- OpenAI explicitly calls out first-class compaction support as part of the Codex workflow for long multi-hour reasoning.
- The guide says the best reference implementation is the open-source Codex CLI agent.
- OpenAI recommends migrating prompts toward the Codex baseline by keeping the autonomy, persistence, codebase exploration, tool use, and frontend-quality snippets that matter most.
- OpenAI also recommends removing unnecessary prompting for upfront plans, preambles, or excessive rollout-status chatter because those patterns can cause Codex to wrap up too early.

## Agent Skills

Official docs facts checked on 2026-04-21:

- Skills are the authoring format for reusable workflows in Codex.
- A skill packages instructions, resources, and optional scripts.
- Skills use progressive disclosure: Codex starts with metadata and loads the full `SKILL.md` only when it chooses to use the skill.
- Skills are available across the CLI, IDE extension, and Codex app.
- OpenAI explicitly frames skills as the right place to preserve repeatable workflows instead of repeatedly pasting long instructions.

## AGENTS.md

Official docs facts checked on 2026-04-21:

- Codex reads `AGENTS.md` files before doing any work.
- Discovery is layered: global guidance in `~/.codex`, then project root, then nested directories down to the current working directory.
- Files closer to the current directory override broader files because they are appended later in the chain.
- Codex stops adding instruction files after the configured byte limit, which defaults to `32 KiB`.
- OpenAI recommends using global defaults for broad working agreements and repository-local files for project-specific expectations.

## Use Case: Save Workflows as Skills

Official use-case facts checked on 2026-04-21:

- OpenAI frames this as turning a working Codex thread, review rule set, test command sequence, release checklist, or repo-specific example into a skill Codex can keep on hand.
- The page explicitly recommends a reusable skill instead of pasting a long prompt into every thread.
- The example workflow starts from one working example plus supporting sources, scripts, commands, and the shape of the desired final output.

## Use Case: Set Up a Teammate

Official use-case facts checked on 2026-04-21:

- OpenAI frames this as giving Codex a durable view of your work so it can notice what changed.
- The use case combines connected tools, one persistent thread that learns what matters, and an automation that checks the same sources again later.
- The core pattern is not “remember everything forever”; it is “teach one thread what matters, then revisit the same sources with automations.”
- The examples focus on Slack, Gmail, calendar, Notion, code, and notes as context surfaces that help Codex escalate the items that deserve your judgment.

## Use Case: Understand Large Codebases

Official use-case facts checked on 2026-04-21:

- OpenAI frames large-codebase onboarding as tracing request flows, identifying module ownership, finding where validation happens, and ending with the next files to read before editing.
- The use case explicitly prefers concrete maps and risky spots over vague summaries of the repository.
- The recommended pattern is to scope the system area, ask Codex to trace the request flow, call out ownership and validation points, then ask for the next files that matter.

## Raw Implications (Not Yet Distilled)

- OpenAI’s Codex guidance strongly supports a “small standing core + progressive disclosure” memory model rather than huge default prompts.
- Skills and layered instruction files are the official place to store repeatable workflow memory.
- Codex’s smoothest workflow is less about giving it more text and more about giving it better durable structures: `AGENTS.md`, skills, teammate threads, automations, and concrete onboarding prompts.
