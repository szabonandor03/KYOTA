# KYOTA Project Bootstrap

This repo is wiki-first. Canonical state lives in `kyota-wiki/`, not in chat memory.

## Default Startup

When starting cold in this repo:

1. Read `kyota-wiki/index.md`.
2. Read `kyota-wiki/NOW.md`.
3. If the task is a concrete `fidesz-sapka-site/` edit, follow `kyota-wiki/schema/fidesz_sapka_single_prompt_workflow.md`.
4. Otherwise, read `kyota-wiki/CODEX.md`.
5. Create a compact context-selection record:
   - goal
   - exclusions
   - budget
   - selected context
   - omitted context
   - execution pattern
   - verify method
6. Load only the files needed for the task.

## Repo Rules

- Prefer `tight` or `standard` context unless the task clearly requires more.
- Do not preload broad wiki context, raw sources, or frontier source files by default.
- For non-trivial tasks, make omitted context explicit.
- Follow `kyota-wiki/schema/version_control_workflow.md` for lasting repo changes.
- If ingesting new sources, follow `kyota-wiki/schema/research_protocol.md`.
- `Superpowers` is optional and should only shape execution if the active runtime actually exposes it.

## FIDESZ SAPKA

For work inside `fidesz-sapka-site/`:

- Read `fidesz-sapka-site/AGENTS.md` if present.
- Read `fidesz-sapka-site/CLAUDE.md` before touching styles or markup.
- Preserve the archive / leaked-Drive posture.

## Updating State

- Update `kyota-wiki/NOW.md` in place when active guidance changes materially.
- Keep the file small enough for cheap cold starts.
