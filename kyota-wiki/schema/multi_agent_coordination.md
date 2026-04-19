# KYOTA Multi-Agent Coordination

## Authority
This file is the canonical coordination contract. If any router, entity page, or summary conflicts with it, this file wins.

## Required Startup
1. Read `../index.md`.
2. Read `../log.md` for recent `HISTORY` records and any active coordination records.
3. Set `BUDGET` to `tight`, `standard`, or `large`.
4. `SELECT` only the files needed for the current task before writing.

## Verification Roles
1. When correctness matters, separate Drafting, Evaluation, and Improvement responsibilities, even if one agent performs more than one phase serially.
2. Evaluation work should prefer deterministic evidence from tests, compilers, linters, searches, or formal solvers over intuition-only review.
3. Evaluation agents return evidence and fix instructions; they must not silently rewrite the draft unless they explicitly own the improvement phase.
4. High-stakes tool use should pass proposed arguments through a formal invariant gate before execution when one is available.

## Isolation Rules
1. Use Git worktrees by default; use branch-isolated execution only when worktrees are unavailable.
2. Parallel agents must not share one mutable working directory.
3. Root files, `/schema/`, `/entities/`, `../entities/index.md`, `../raw/index.md`, and `../log.md` are hotspot files.
4. No hotspot file may be edited without an active `CLAIM`, except for appending a single structured coordination record to `../log.md`.

## Claim Lifecycle
1. Append a `CLAIM` before editing any hotspot or shared file. The claim must name the exact files or file group it covers.
2. If an active overlapping `CLAIM` already exists, stop and wait for `HANDOFF` or `RELEASE`.
3. Use `BLOCKER` to announce an impasse without releasing ownership.
4. Use `UNBLOCK` to clear a blocker while keeping the same active claim.
5. Use `HANDOFF` to transfer ownership, `VERIFY` to record checks for non-trivial work, and `RELEASE` to close ownership.
6. If a claim or blocker becomes stale and the original owner is no longer progressing it, use `RECOVER` to close that abandoned scope explicitly.
7. Non-trivial shared changes should not be released without a `VERIFY` record, and that record should cite deterministic evidence when available.
8. `HISTORY` records document ingest and maintenance but do not grant ownership.
9. The newest unreleased `CLAIM` governs a file scope until a matching `HANDOFF`, `RELEASE`, or `RECOVER` appears.
10. The newest unresolved `BLOCKER` remains active until a matching `UNBLOCK`, `HANDOFF`, `RELEASE`, or `RECOVER` appears.
11. Staleness is tracked from the most recent open-scope lifecycle activity, not just from the original claim timestamp.

## Canonical Log Format
```text
timestamp=<ISO8601> | type=<HISTORY|CLAIM|BLOCKER|UNBLOCK|HANDOFF|VERIFY|RELEASE|RECOVER> | agent=<agent-id> | worktree_or_branch=<name> | files_owned=<comma-separated paths or -> | status=<active|blocked|handoff|passed|released|recovered|done> | audience=<all|agent-id> | note=<free text>
```

## Tooling
- Use `../bin/kyota history` for append-only `HISTORY` records whenever the tool is available.
- Use `../bin/kyota` to create `CLAIM`, `BLOCKER`, `UNBLOCK`, `HANDOFF`, `VERIFY`, `RELEASE`, and `RECOVER` records whenever the tool is available.
- Prefer `../bin/kyota status` over manual log scanning when checking active ownership or unresolved blockers.
- Use `../bin/kyota doctor` or `../bin/kyota status` to surface stale work before choosing recovery.
- Use `../bin/kyota lint` to catch overlapping active claims, malformed records, invalid blocker lifecycles, registry drift, and router drift before shared maintenance work.
- Use `VERIFY` records to capture reflector output, formal-gate traces, test results, or other deterministic evidence that justified release.

## Merge Hygiene
- Keep ownership scopes bounded and explicit.
- Update registries and `../log.md` in the same unit of work when shared knowledge changes.
- Use explicit `HANDOFF` boundaries between drafting, evaluation, and improvement phases instead of concurrent edits on the same hotspot files.
- Resolve contradictions through the log and canonical schema, not through undocumented parallel edits.
