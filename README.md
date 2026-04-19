# KYOTA

KYOTA is a local-first coordination system for agent work. It keeps the real state in Markdown files inside `kyota-wiki/`, and the `kyota` command helps you work with that state safely instead of editing logs and ownership records by hand.

## What You Use It For

Use KYOTA when you want a simple way to:

- see who owns which files
- claim work before editing shared files
- record blockers, verification, and release events
- detect stale claims or blockers before they silently pile up
- recover abandoned work with an explicit audit trail
- lint the workspace so drift and broken process show up quickly

The source of truth stays in the repo. The CLI just makes it easier and safer to work with it.

## Install

From the repo root:

```bash
python3 -m pip install .
```

After that, you can run:

```bash
kyota --help
```

If you want the terminal coordination console too, install the TUI extra:

```bash
python3 -m pip install '.[tui]'
```

If you run the command outside the repo, set the workspace path first:

```bash
export KYOTA_REPO_ROOT=/path/to/KYOTA
```

If you want live local code changes without reinstalling every time, you can try:

```bash
python3 -m pip install -e .
```

If editable install fails on an older pip, upgrade pip first and rerun it.

## The Commands You Will Actually Use

- `kyota status` shows active claims and unresolved blockers, including verify/stale markers.
- `kyota claim --agent <id> --files ... --note "..."` claims shared work.
- `kyota verify --agent <id> --files ... --note "..."` records that the work was checked.
- `kyota release --agent <id> --files ... --note "..."` releases ownership after verification.
- `kyota recover --agent <id> --files ... --note "..."` recovers a stale abandoned claim and clears its blocker state.
- `kyota lint` checks the workspace for broken records, missing registry entries, and router drift.
- `kyota doctor` does a quick setup and health check, and also reports stale work that may need recovery.
- `kyota tui` remains available as an optional dashboard, but this phase does not add new TUI behavior.

## A Normal Wiki Session

1. Check the workspace:

```bash
kyota doctor
kyota status
```

2. Set your agent name for this shell:

```bash
export KYOTA_AGENT=codex
```

3. Claim the files you need:

```bash
kyota claim \
  --files kyota-wiki/index.md kyota-wiki/log.md \
  --note "Working on startup docs"

kyota verify \
  --files kyota-wiki/index.md kyota-wiki/log.md \
  --note "Checked docs, links, and lint output"

kyota release \
  --files kyota-wiki/index.md kyota-wiki/log.md \
  --note "Done with the doc update"
```

4. Do the actual Markdown editing in your normal editor.

5. If work gets stuck and `kyota doctor` or `kyota status` shows a stale claim/blocker, recover it explicitly:

```bash
kyota recover \
  --files kyota-wiki/index.md \
  --note "Recovering abandoned scope after stale blocker"
```

6. Run the safety check:

```bash
kyota lint
```

## Notes

- KYOTA expects to run from the repo root, from inside `kyota-wiki/`, or with `KYOTA_REPO_ROOT` set.
- The Markdown files remain the real system record.
- `kyota-wiki/bin/kyota` still works, but the packaged `kyota` command is now the preferred entry point.
- `RECOVER` is distinct from `RELEASE`: recover is for abandoned stale scopes, not normal completion.
- `kyota lint` stays focused on structural correctness. Use `kyota doctor` or `kyota status` to see stale work.
- `kyota tui` remains available if you want a live dashboard, but content editing still happens in your normal editor.
