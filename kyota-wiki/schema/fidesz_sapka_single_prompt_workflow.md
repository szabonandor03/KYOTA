# FIDESZ SAPKA Single-Prompt Website Workflow

Purpose: let the operator request routine website changes in one prompt without triggering a clarification loop.

This workflow is the fast path for work inside `fidesz-sapka-site/`.
It does not replace the general KYOTA startup contract for unrelated work.

## Default Rule

If the operator asks for a concrete website change and does not ask for planning, the agent should:

1. infer the smallest sufficient scope
2. load only the site files and wiki guidance required for that change
3. implement the change
4. run the smallest relevant verification step
5. report outcome, state changes, and only real blockers

The agent should not stop to ask follow-up questions unless an escalation condition below is met.

## Allowed One-Prompt Scope

This fast path is for:

- styling or layout changes in `fidesz-sapka-site/`
- copy edits that do not introduce new factual claims
- content reshuffling using already-present assets
- adding already-provided media to existing site sections
- small structural UI changes that preserve the current site concept
- bug fixes and polish passes

## Escalation Conditions

The agent must return to the operator before proceeding only if one of these is true:

- the request would break an invariant in `fidesz-sapka-site/CLAUDE.md`
- the request requires new facts the repo does not contain
- the request touches withheld material called out in `kyota-wiki/NOW.md`
- the request implies a strategic redesign rather than a bounded site edit
- the request cannot be completed and verified locally with the available toolchain

If none of those conditions are met, the agent should execute without additional questions.

## Default Assumptions

When the operator prompt is underspecified, default to these assumptions instead of asking:

- preserve the current Drive-leak / archive posture
- preserve the current routing and information architecture unless the prompt explicitly changes it
- preserve placeholders rather than inventing metadata
- use existing assets before introducing new ones
- if multiple reasonable UI choices exist, choose the one with the smallest diff that best fits the existing design language
- verify with `npm run build` in `fidesz-sapka-site/`

## Minimal Load Set

For normal website edits, load only:

- `kyota-wiki/NOW.md`
- `fidesz-sapka-site/CLAUDE.md`
- the specific files needed for the requested change

Load other wiki entities only when the requested change clearly depends on them.

## Operator Prompt Shape

Use prompts in this shape:

```text
Change the FIDESZ SAPKA website in one pass.
Task: [what should change]
Constraints: [optional hard constraints]
Do not ask follow-up questions unless you hit a true blocker under kyota-wiki/schema/fidesz_sapka_single_prompt_workflow.md.
```

## Example

```text
Change the FIDESZ SAPKA website in one pass.
Task: make the video rows feel less cramped on mobile and keep the Drive-leak look.
Constraints: do not touch copy, routes, or audio pages.
Do not ask follow-up questions unless you hit a true blocker under kyota-wiki/schema/fidesz_sapka_single_prompt_workflow.md.
```

## Success Condition

This workflow is working if routine site changes can be requested in a single prompt and the agent returns only:

- the implemented result
- the verification performed
- any real blocker that required escalation
