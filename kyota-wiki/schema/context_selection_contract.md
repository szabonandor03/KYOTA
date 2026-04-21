# Context Selection Contract

## Purpose

Turn `ASK -> BUDGET -> SELECT -> GENERATE` into an auditable operating contract so non-trivial tasks prove what they loaded, what they skipped, and why the chosen context budget was justified.

## Use When

- the task is non-trivial and could sprawl across multiple wiki pages, code files, or tool surfaces
- the agent would otherwise browse broadly before the deliverable is clear
- the work needs a visible boundary between selected evidence and intentionally omitted context

## Do Not Load When

- the task is a one-line or one-file fix whose scope is already explicit
- [`fidesz_sapka_single_prompt_workflow.md`](./fidesz_sapka_single_prompt_workflow.md) fully covers a bounded site edit
- a task contract in `kyota-wiki/tasks/` already names the exact load set and exclusions

## Required Record

Every non-trivial task must carry a compact context-selection record before deeper loading begins. The record may stay internal during execution, but its fields are mandatory.

- `goal` - the outcome that must be achieved
- `exclusions` - what the operator does not want touched or considered
- `budget` - `tight`, `standard`, or `large`
- `selected_context` - the minimum file, entity, schema, and tool set needed for the task
- `omitted_context` - the most relevant files, folders, or knowledge classes intentionally not loaded
- `execution_pattern` - `direct execution`, `explicit RCI`, `deterministic reflector`, or `formal verification gate`
- `verify_method` - the concrete post-draft check, tool, or evidence plan

Recommended shape:

```text
GOAL: <required outcome>
EXCLUSIONS: <out-of-scope items>
BUDGET: tight | standard | large
SELECTED CONTEXT:
- <file or knowledge surface>
OMITTED CONTEXT:
- <file, folder, or knowledge class intentionally skipped>
EXECUTION PATTERN: <pattern>
VERIFY METHOD: <check or evidence source>
```

## Contract Rules

1. Declare `goal` and `exclusions` before broad context expansion.
2. Default to `tight` or `standard`. `large` requires an explicit reason tied to ingestion, cross-entity audit, contradiction resolution, or a multi-stage verification loop.
3. `selected_context` must be minimal and task-scoped. If two files say the same thing, select the more authoritative one.
4. `omitted_context` is mandatory for non-trivial tasks. The point is to make deliberate non-loading visible and repeatable.
5. Prefer `/entities/` over `/raw/` unless the task is doing source verification, contradiction resolution, or new ingestion.
6. Prefer dedicated task contracts over broad folder loading when one exists.
7. Choose the execution pattern before generation, not after the draft is already underway.
8. Declare the `verify_method` before tool execution so the task does not fall back to intuition-only completion.
9. If the selected set exceeds the budget, reduce scope or split the work. Do not keep adding files and hope the model sorts it out.

## Defaults For Knowledge Hygiene

- New research defaults to `NOOP` unless it changes behavior, policy, or execution quality.
- If a source only restates existing guidance, keep it out of active context and record the `NOOP` decision instead.
- If the task is architecture-heavy, select architecture documents first and implementation files second.
- If the task is implementation-heavy, load only the wiki rules that change implementation behavior.

## Cross-References

- Declarative assembly method: [`../entities/spl_declarative_context.md`](../entities/spl_declarative_context.md)
- Pattern selection: [`../entities/execution_patterns.md`](../entities/execution_patterns.md)
- Ingestion rules: [`../entities/ingestion_workflow.md`](../entities/ingestion_workflow.md)
- Shared cross-model handoff rules: [`./multi_model_operating_contract.md`](./multi_model_operating_contract.md)
