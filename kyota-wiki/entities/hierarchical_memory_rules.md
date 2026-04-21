# Hierarchical Memory Rules

## Source Basis
- Derived from `../raw/LLM_OS_Research_Report.md`
- Primary upstream concepts: MemMachine (2026), Memory-R1 (2026), and the LLM OS memory-tier model

## Purpose
Convert hierarchical-memory research into operational rules for how specialist agents store, revise, and retire knowledge inside KYOTA.

## Use When

- deciding whether new material should become durable knowledge
- updating or retiring entity guidance after source verification
- checking whether a change belongs in `/raw/`, `/entities/`, `NOW.md`, or nowhere at all

## Do Not Load When

- the task only needs current project state and does not touch durable knowledge
- the source has already been resolved into a task contract or current decision
- the work is a bounded implementation edit with no research or knowledge-base change

## Workspace Rules
1. Treat `/raw/` as immutable episodic memory. Never rewrite or summarize over the original source file.
2. Promote knowledge from `/raw/` into `/entities/` as atomic statements, preferably one sentence or one short bullet per fact, so later agents can retrieve and revise specific claims without reopening whole documents.
3. Preserve provenance for each important memory. Every entity page must identify the source file and, when relevant, the upstream paper or vendor document family.
4. Use explicit memory operations instead of silent overwrites:
   - `ADD` when a source introduces a new fact, pattern, or rule.
   - `UPDATE` when the same concept is refined or superseded by a newer source.
   - `DELETE` when a claim is invalid, duplicated, or no longer suitable for active use.
   - `NOOP` when new material does not justify a knowledge-base change.
5. Default to `NOOP` unless the new source changes behavior, policy, or execution quality. Newness alone is not enough.
6. `UPDATE` does not mean erasing history blindly. Preserve the previous claim long enough to explain what changed, why it changed, and which source justified the revision.
7. `DELETE` means removing a memory from active guidance. The audit trail lives in git history (commit messages) and optionally a one-line note in `NOW.md` **Recent decisions**. Do not destroy evidence in `/raw/`.
8. When a source contains contradictions, prefer consolidation over replacement. Convert conflicting statements into a resolved rule with explicit caveats instead of flattening them into a single unsupported claim.
9. Retrieve memory with local context, not isolated fragments. When an entity or log entry appears relevant, inspect its neighboring notes or adjacent history so the "nucleus" fact is interpreted with surrounding context.

## KYOTA Operating Pattern
- Working memory: the current task context and open files.
- Short-term memory: `NOW.md` and the few entity pages selected for the task.
- Episodic memory: immutable source files stored in `/raw/`.
- Semantic memory: distilled operating knowledge in `/entities/`.
- Profile memory: any future durable preferences or agent-specific conventions, stored explicitly rather than inferred repeatedly.

## Editing Standard
- Prefer small, targeted edits to entity files so one memory operation maps to one auditable change.
- If a new source would force broad rewrites across many entities, create the smallest necessary updates first and log the scope before continuing.
