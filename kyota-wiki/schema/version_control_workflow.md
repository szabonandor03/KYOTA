# KYOTA Version Control Workflow

This document records the git workflow the repository has actually been using and turns it into the default operating contract. Local history informed it; future work should follow it unless a later decision replaces it.

## Purpose

KYOTA is a single-operator, serial-agent workspace. Version control is not the center of the system, but it is the boundary for:

- integrating finished work into `main`
- keeping parallel agent experiments isolated when needed
- preserving durable history so `NOW.md` can stay small and current

The repo does not use an in-repo claim or mailbox layer anymore. If work needs isolation, use git.

## Default Contract

For any non-trivial repo change, the default path is:

`clean start from main -> short-lived branch -> focused local verification -> PR -> readable main history -> delete branch`

That is the baseline. Deviations should be rare and intentional.

## Observed Baseline

The local history shows a consistent pattern:

- work is usually done on short-lived agent branches such as `claude/zen-northcutt-fabd13`
- branch commits are narrow and task-specific
- `main` acts as the integration branch
- branch work is typically landed through a PR
- the most recent PRs usually land as a single commit on `main` with the same subject plus `(#PR)` suffix
- earlier PRs sometimes landed as explicit merge commits
- when a branch drifts behind `main`, it is sometimes synced explicitly with a merge commit such as `Merge origin/main, keep ...`
- merged work does not always have its local branch cleaned up afterward; this should improve

Representative commits from local history:

- `0900fd4` -> `15921e1`: branch change landed to `main` as PR `#1`
- `3d073b9` -> `e775b1d`: branch commit landed to `main` as a single PR commit `(#7)`
- `cb2346d` -> `d79e556`: same pattern for PR `#6`
- `a860a92`, `f090f5c`: explicit branch sync merges from `origin/main`

## Start Conditions

Before creating or continuing a branch:

1. Check `git status --short`.
2. If the worktree is dirty, decide whether those changes belong to the task you are about to do.
3. Do not sweep unrelated operator changes into your branch just because they are already present.
4. Start from current `main` unless you are deliberately continuing an existing open branch or PR.

In this repo, branch isolation is the coordination mechanism. Do not recreate the old claim and release workflow inside Markdown.

## Branch Lifecycle

1. Start from current `main`.
2. Create a short-lived branch for one bounded task.
3. Keep the branch focused. If the scope splits, split the branch.
4. Verify locally to the level the change warrants.
5. Commit with a direct, scope-first subject.
6. Open a PR to `main`.
7. Land the PR using the merge mode that leaves `main` clearest.
8. Delete the branch once merged, locally and remotely.

The branch is the working container, not the backlog. A stale local branch is not a roadmap.

## Branch Naming

Observed branch names are agent-scoped and ephemeral:

- `claude/<session-codename>`
- `codex/<session-codename>`

Equivalent names are fine as long as they stay short-lived and clearly disposable. The important rule is that the branch names describe execution context, not long-term product lanes.

## Scope Rules

- One branch should correspond to one reviewable unit.
- One PR should have one clear reason to exist.
- If a task mixes unrelated wiki guidance, site changes, and media housekeeping, split it unless the pieces are inseparable.
- If you discover adjacent cleanup while working, either leave it out or put it in a clearly separate commit that still belongs to the same branch purpose.

## Commit Style

Prefer concrete commit subjects in one of these forms:

- `<scope>: <specific change>`
- `<imperative change>; <second clause if needed>`

Examples from history:

- `fidesz-sapka: bigger video and photo grid items`
- `fidesz-sapka: update track release dates`
- `Rip out kyota CLI + TUI dashboard + log.md ledger; replace with NOW.md`
- `Add task contract template + first FS-003 task contract`

Rules:

- keep the subject specific enough that `git log --oneline` is useful by itself
- prefer one topic per commit
- avoid vague subjects like `fix stuff`, `update docs`, or `changes`
- commit only the files that belong to the task you actually completed
- run the appropriate local check before committing when the change has an executable surface

Verification is proportional:

- wiki-only guidance edits may only need a careful read-through
- site or code changes should run the smallest relevant build, test, or lint step
- do not claim verification you did not actually run

## Landing Policy

Preferred landing path:

- Prefer PR-based landing to `main`.
- Prefer squash merge when the branch is a single-purpose unit and the intermediate branch commits are not important to preserve on `main`.
- Allow merge commits when preserving branch structure is useful or when GitHub already has an open branch with meaningful history.

This matches the repo's actual mixed history:

- recent changes often appear on `main` as one clean commit with `(#PR)`
- older PRs include explicit `Merge pull request #...` commits

The practical rule is not "one true merge strategy." The practical rule is: keep `main` readable.

## Direct Commits To `main`

Direct commits to `main` are allowed only when all of the following are true:

- the change is tiny, self-contained, and immediately legible
- there is no already-open branch or PR for the same scope
- no concurrent agent or operator work needs isolation
- using a PR would add ceremony but not clarity

If any of those conditions fail, use a branch and PR.

## Syncing a Branch

If a working branch falls behind `main` and needs fresh changes before landing:

- fetch from `origin`
- sync from `origin/main`
- if conflicts require a judgment call, record that in the merge subject

Observed pattern:

- `Merge origin/main, keep correct release dates`
- `Merge origin/main, keep luminance halation design`

That style is worth keeping when you merge `origin/main` because it records the actual conflict-resolution decision, not just the mechanics of syncing.

Default sync rule:

- Prefer merging `origin/main` into the branch once the branch is shared or already has an open PR.
- A private unpublished branch may be rebased instead if that materially simplifies cleanup.
- Do not rewrite a shared branch casually.

## Main Branch Rules

- Treat `main` as the canonical integration line.
- Do not pile experimental or half-decided work directly onto `main`.
- Land finished, bounded slices.
- Keep history readable enough that later agents can recover what changed from `git log` without opening every diff.

Direct commits to `main` are the exception, not the default.

## Wiki-Specific Rules

- Use git history as the durable archive. Do not turn `NOW.md` back into an append-only ledger.
- When active guidance changes materially, update `kyota-wiki/NOW.md` in place and let git preserve the prior state.
- When ingesting research or changing durable guidance, the commit message should make that action legible. This matches `schema/research_protocol.md`.

## Simultaneous Work

This workspace is usually serial. For rare simultaneous work:

- each agent gets its own branch
- prefer separate git worktrees if two sessions need the repo open at the same time
- integrate through PRs, not through an in-repo coordination ledger

Branches are the coordination layer. Worktrees are the isolation primitive when parallelism is real.

## Branch Cleanup

Once work lands:

- delete the remote branch
- delete the local branch
- periodically prune stale branch references

The current repo already has leftover local and remote agent branches. That is tolerated history, not the target pattern.

## Recommended Commands

Start a task:

```bash
git status --short
git switch main
git pull --ff-only
git switch -c claude/<session-codename>
```

Finish the work:

```bash
git add <paths>
git commit -m "scope: specific change"
git push -u origin claude/<session-codename>
```

If the branch needs a sync before merge:

```bash
git fetch origin
git merge origin/main
```

After merge, clean up:

```bash
git push origin --delete claude/<session-codename>
git branch -d claude/<session-codename>
git fetch origin --prune
```

Then open a PR and land it to `main` using the merge mode that keeps `main` clearest.

## Anti-Patterns

- long-lived personal branches that become substitute timelines
- unrelated changes bundled into one PR
- committing unrelated dirty-worktree files because they happened to be present
- vague commit messages that hide what actually changed
- using wiki files as a surrogate for git coordination
- preserving every transient branch commit on `main` when a squash would be clearer
- leaving merged agent branches around indefinitely until branch lists stop meaning anything

## Bottom Line

The repo's target pattern is:

`clean main -> short-lived branch -> focused verification -> PR -> readable main history -> branch cleanup`

For rare simultaneous work, branches plus PRs are the coordination layer and worktrees are the isolation tool. For everything else, keep the git workflow simple and let the wiki carry the project state.
