# Task Contract Template

A task contract is a small markdown file that lets an agent run to completion without checking in. Every non-trivial task should have one.

Live contracts go in `kyota-wiki/tasks/[name].md`. Delete or archive when the task is done.

## Why this exists

Without a contract, an agent reaches every ambiguous decision and stops to ask the operator. With a contract, the agent already knows the answer for the decisions the operator anticipated, and only escalates the ones that genuinely require judgment.

The contract is the structural fix for the "agent waits on me too often" bottleneck. It replaces conversational checkpoints with declared scope.

## When to write one

- Anything taking more than a single tool call or two
- Any task where you would otherwise expect to be asked clarifying questions mid-run
- Any task that produces a wiki update, file, or artifact
- Skip for: trivial reads, single-shot questions, throwaway exploration

## Format

```markdown
# Task: [short name]

## Scope
What this task covers. What it explicitly does not cover.
One paragraph. Be concrete.

## Done criteria
Specific, checkable conditions. The agent stops when ALL are true.
- [ ] condition 1
- [ ] condition 2
- [ ] condition 3

## Autonomy scope
Decisions the agent can make without asking the operator.
Be generous here — every item listed is one less interruption.
- decide X (default to Y if ambiguous)
- choose between A and B based on Z
- skip step N if condition

## Escalation conditions
What MUST come back to the operator before proceeding.
Keep this list short. Only genuine judgment calls.
- if doing this would touch [withheld item]
- if cost or time exceeds [bound]
- if a decision contradicts something in NOW.md

## Context budget
tight | standard | large

## Files to load
Explicit list. Do not load anything not on this list without a written reason.
- kyota-wiki/NOW.md
- kyota-wiki/entities/[specific].md
- [other paths]

## Output artifact
What gets written when done, and where.
- update NOW.md with [specific change]
- write [path] containing [shape]
- commit message format: [...]
```

## Authoring rules

1. **Done criteria must be checkable.** "Site looks good" is not a done criterion. "All three track rows render with playable audio and no console errors" is.

2. **Autonomy scope is generous by default.** If you find yourself wanting to leave a decision unspecified, decide it now in the contract. Future-you reading "ask the operator" is the bottleneck this template exists to fix.

3. **Escalation conditions are narrow.** Only list things that genuinely require operator judgment — usually because they touch a withheld item, a stated invariant, or a strategic direction. If escalation list grows past 3–4 items, the scope is wrong; split the task.

4. **Files to load is explicit.** No "and any other relevant entities." If you don't know which entities are relevant, run a quick discovery pass first and update the contract before executing.

5. **Output artifact is concrete.** "Update the wiki" is not an artifact. "Add one line to NOW.md Recent decisions section" is.

## Lifecycle

- **Authoring:** operator writes the contract, or asks a planning session (cheap context) to draft it
- **Execution:** executor session reads contract first, then loads only listed files, then runs to done criteria
- **Completion:** executor writes the output artifact, then either deletes the contract file or moves it to `tasks/done/` for audit
- **Escalation:** executor stops at the first escalation condition met, writes current state to the contract under a `## Escalated` section, and returns to operator

## Anti-patterns

- Writing the contract during execution ("I'll figure out done criteria as I go") — defeats the purpose
- Listing every entity "just in case" under Files to load — defeats the budget
- Empty Autonomy scope — guarantees mid-run interruptions
- Escalation conditions that are really just "if you hit a bug" — bugs aren't escalations, they're work
- Contracts longer than ~80 lines — scope is too big; split it
