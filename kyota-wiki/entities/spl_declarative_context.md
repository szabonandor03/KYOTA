# SPL Declarative Context

## Source Basis
- Derived from `../raw/LLM_OS_Research_Report.md`
- Primary upstream concepts: Structured Prompt Language (SPL), declarative token budgeting, and operator-guided SELECT/GENERATE separation
- Operationally extended by `./jit_tool_loading.md`, `./recursive_criticize_improve.md`, and `./autonomous_verification_loops.md`

## Purpose
Define how KYOTA agents should gather context declaratively instead of assembling prompts ad hoc, while loading execution affordances only when they are needed and only after a brief operator-intake step.

## Use When

- the task is non-trivial and needs an explicit intake, budget, and selection pass
- the session is at risk of context creep or broad browsing before the real deliverable is clear
- a later handoff needs to understand what was selected and what was left out

## Do Not Load When

- the single-prompt website workflow already defines the minimal load set
- a task contract already names the exact files and exclusions
- the task is so small that a full declarative selection pass would add more overhead than clarity

## Core Rules
1. Every non-trivial task should begin with a brief operator-intake step before context selection. Ask 1-3 short questions about goal, emphasis, and exclusions.
2. Every non-trivial task must then set an explicit context budget, even if it is only qualitative such as `tight`, `standard`, or `large`.
3. Every non-trivial task must make selected and omitted context explicit, following [`../schema/context_selection_contract.md`](../schema/context_selection_contract.md).
4. Context gathering and answer generation are separate phases. First `SELECT` the minimum evidence set. Then `GENERATE` the output, patch, or plan.
5. Treat tool schemas, prompt fragments, and invariants as selectable context artifacts, not as permanent prompt furniture.
6. JIT-load only the smallest viable tool and schema set for the current execution tick, then unload it after the task reaches a terminal state.
7. Do not generate while still browsing broadly. Unbounded reading causes context creep and weakens auditability.
8. If the selected evidence exceeds the budget, reduce scope before proceeding. Do not keep adding files and hope the model sorts it out.
9. When a task is high-stakes or complex, include a brief `EXPLAIN` note describing which sources were selected, which execution loop was chosen, and why they fit the budget.

## Required KYOTA Pattern
Use this mental execution order for complex work:

```text
GOAL      -> What outcome is required?
ASK       -> What is the operator actually thinking about, and what should be excluded?
RISK      -> Does this need direct execution, explicit RCI, a reflector, or a formal gate?
BUDGET    -> How much context can this task justify?
SELECT    -> Which index entries, entities, prompt fragments, invariants, log spans, or raw sources are required?
LOAD      -> Inject only the tool schemas needed for the current execution tick.
GENERATE  -> Produce the draft, patch, answer, or proposed tool call from the selected set only.
VERIFY    -> Critique, reflect, or formally gate before terminal execution.
EXPLAIN   -> State what was used, omitted, unloaded, or deferred when auditability matters.
```

## Selection Rules
1. `index.md` is the primary selector. Start there before opening entity pages or raw research.
2. Use operator answers to constrain the selection set before expanding beyond startup files.
3. Prefer `/entities/` over `/raw/` unless source verification or new ingestion is required.
4. Select only the modules needed from `../schema/kyota_agent_schemas.md`; do not load the whole prompt library by default.
5. Pull only the log window needed to understand recent changes instead of re-reading the entire history every time.
6. If a task spans architecture and implementation, select the architecture entities first, then the implementation files, not both folders indiscriminately.

## Budgeting Rules
- `tight` budget: one task, one or two entity pages, one prompt fragment if needed, and only the recent log entries needed for safety.
- `standard` budget: several entity pages, one execution loop, and a small number of implementation files or tool schemas.
- `large` budget: reserved for raw-source ingestion, audits, cross-entity reconciliation, or complex multi-stage verification loops. It should be justified explicitly, not chosen by habit.

## Failure Policy
- If the selected material still feels underspecified, expand the budget deliberately and record the reason.
- If the selected material becomes noisy, restart from `index.md` and rebuild the context instead of accreting more fragments.
- If stale tool schemas or unused prompt fragments accumulate, unload them and rebuild the execution tick from the selected set.
