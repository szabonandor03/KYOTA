# Superpowers Plugin Local Sources

Retrieved: 2026-04-21

## Source Paths

Local files checked on 2026-04-21:

- `/Users/nandi/.codex/plugins/cache/openai-curated/superpowers/b1986b3d3da5bb8a04d3cb1e69af5a29bb5c2c04/README.md`
- `/Users/nandi/.codex/plugins/cache/openai-curated/superpowers/b1986b3d3da5bb8a04d3cb1e69af5a29bb5c2c04/skills/using-superpowers/SKILL.md`
- `/Users/nandi/.codex/plugins/cache/openai-curated/superpowers/b1986b3d3da5bb8a04d3cb1e69af5a29bb5c2c04/skills/writing-plans/SKILL.md`
- `/Users/nandi/.codex/plugins/cache/openai-curated/superpowers/b1986b3d3da5bb8a04d3cb1e69af5a29bb5c2c04/skills/subagent-driven-development/SKILL.md`
- `/Users/nandi/.codex/config.toml`

## Scope

This note captures the locally installed Superpowers plugin facts that matter for KYOTA integration: what the plugin is, how its default workflow behaves, what artifact locations it expects, how it prioritizes instructions, and how its worktree / TDD / subagent routines should fit into a file-first repo.

## README Facts

Local plugin README facts checked on 2026-04-21:

- Superpowers describes itself as a complete software-development workflow for coding agents, built from composable skills plus startup instructions that force the agent to use them.
- The documented default workflow is: `brainstorming -> using-git-worktrees -> writing-plans -> subagent-driven-development or executing-plans -> test-driven-development -> requesting-code-review -> finishing-a-development-branch`.
- The README frames the system as plan-first and execution-discipline-heavy rather than as a memory layer.
- The plugin emphasizes `TDD`, `YAGNI`, `DRY`, systematic debugging, evidence over claims, and review gates.
- The README says skills should trigger automatically when relevant and that the agent should rely on those skills instead of ad hoc behavior.

## `using-superpowers` Skill Facts

Local skill facts checked on 2026-04-21:

- The skill says that if there is even a small chance a skill applies, the agent should invoke it before responding or acting.
- The priority order is explicit: user instructions first, Superpowers skills second, default system behavior last.
- The skill says process skills come before implementation skills.
- The skill positions Superpowers as a workflow override layer, not as a replacement for the user's explicit instructions.

## `writing-plans` Skill Facts

Local skill facts checked on 2026-04-21:

- The skill is for comprehensive implementation plans before touching code.
- It expects a dedicated worktree created by the earlier workflow.
- Its default save location is `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`.
- It expects extremely explicit plans with exact file paths, concrete code, concrete test commands, and very small task slices.
- The skill explicitly allows user preferences to override the default plan location.

## `subagent-driven-development` Skill Facts

Local skill facts checked on 2026-04-21:

- The core pattern is one fresh subagent per task, followed by two review passes: spec compliance first, then code quality.
- The skill prefers isolated task context to avoid controller-context pollution.
- It recommends using the least powerful model that can safely handle each task role.
- It treats `using-git-worktrees`, `writing-plans`, `requesting-code-review`, and `finishing-a-development-branch` as required workflow partners.
- It explicitly warns against starting implementation on `main` or `master` without user consent.

## Local Availability Observation

Local config and session facts checked on 2026-04-21:

- `/Users/nandi/.codex/config.toml` enables `superpowers@openai-curated`.
- The active Codex session's exposed plugin / skill surface did not list Superpowers skills, even though the plugin is installed locally.
- Local installation therefore does not guarantee active-session availability.

## Raw Implications (Not Yet Distilled)

- Superpowers is an execution-discipline surface, not a memory surface.
- Its default `docs/superpowers/...` artifact locations should not automatically become canonical state inside KYOTA.
- The strongest parts of the plugin are useful for larger implementation and debugging work, but too heavy for small direct edits, wiki curation, or ingestion decisions.
- User instructions and KYOTA repo contracts must outrank Superpowers defaults whenever they conflict.
