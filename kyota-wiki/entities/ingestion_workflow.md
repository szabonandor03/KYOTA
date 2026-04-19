# Ingestion Workflow

## Purpose
Concrete walkthrough for turning a new research source into durable KYOTA knowledge. Operationalizes [`../schema/maintenance_protocol.md`](../schema/maintenance_protocol.md) and [`../schema/research_protocol.md`](../schema/research_protocol.md) so ingestion takes minutes, not a re-read of every schema.

## Canonical Authority
- Source-of-truth rules: [`../schema/research_protocol.md`](../schema/research_protocol.md).
- Ingest/query/lint rules: [`../schema/maintenance_protocol.md`](../schema/maintenance_protocol.md).
- Memory-operation semantics (`ADD`/`UPDATE`/`DELETE`/`NOOP`): [`./hierarchical_memory_rules.md`](./hierarchical_memory_rules.md).
- This page is operational; if it disagrees with a schema, the schema wins and this page gets an `UPDATE`.

## When to Ingest vs Skip
Ingest when the source:
1. Introduces a capability, rule, or pattern KYOTA does not already encode (`ADD`).
2. Refines or supersedes a claim already in `/entities/` (`UPDATE`).
3. Invalidates or retires a claim currently in active guidance (`DELETE`).

Skip (`NOOP`) when the source:
- Restates guidance that is already captured with equal or better precision.
- Contains only editorial/marketing framing around an already-ingested technical point.
- Is published before 2024 and conflicts with [`../schema/research_protocol.md`](../schema/research_protocol.md)'s recency rule, unless it is the primary source for a concept still referenced by newer work.

When in doubt, prefer `NOOP` over speculative ingestion. Record the decision in the `HISTORY` record so future agents do not re-evaluate the same source.

## Operation Decision Rule
| Situation | Operation | Minimal artifacts |
| --- | --- | --- |
| New fact, pattern, or rule not yet in `/entities/` | `ADD` | new raw file + new entity + both registry updates + `HISTORY` |
| Same concept refined by a newer source | `UPDATE` | new raw file + edited entity (preserve prior claim with caveat) + registry touch-up if summary changes + `HISTORY` |
| Claim is now invalid or duplicated | `DELETE` | edited entity (remove the claim, keep audit trail in `log.md`) + `HISTORY`. Do not erase the source in `/raw/` |
| Source offers no net new guidance | `NOOP` | `HISTORY` record only, noting the skip reason |

## Provenance Standards
Every `/entities/` page synthesized from research must carry:
- A `## Source Basis` or `## Sources` block naming the raw file in `/raw/` and, when available, the upstream paper/doc and retrieval date.
- A clear distinction between sourced claims and agent inference. Use an `## Evidence Notes` or `## KYOTA Implications` section for the latter so readers can tell them apart.
- Publication/retrieval date when it materially affects recency judgments.
- An explicit note for any conflict between sources: name the conflict, show the resolution rule, do not smooth it over.

Never paste a whole raw source into an entity. Distill atomic claims per [`./hierarchical_memory_rules.md`](./hierarchical_memory_rules.md) so later agents can revise one fact without rewriting the page.

## Pre-Ingest Checklist
1. `kyota status` shows no overlapping active `CLAIM` on the entity or registry files you will touch.
2. `kyota lint` is currently clean (you should not absorb pre-existing drift into your slice).
3. You have read [`../schema/research_protocol.md`](../schema/research_protocol.md) for any source not already inside `/raw/`.
4. You have decided the operation (`ADD` / `UPDATE` / `DELETE` / `NOOP`) before starting the write.
5. Your `CLAIM` scope matches: for `ADD`, typically the new raw file, the new entity, and both registry files; for `UPDATE`, the affected entity and the registry only if the one-liner changes.

## Worked Example: `ADD` a New Capability
Scenario: a 2026 paper introduces a pattern KYOTA does not yet encode - call it "Contrastive Tool Self-Check" (CTSC). You obtained a clean copy of the paper's relevant summary and saved it locally.

1. **Claim the exact file set.**
   ```bash
   kyota claim --agent <id> \
     --files kyota-wiki/raw/contrastive_tool_self_check_raw.md \
             kyota-wiki/entities/contrastive_tool_self_check.md \
             kyota-wiki/raw/index.md \
             kyota-wiki/entities/index.md \
     --note "ADD: ingest contrastive tool self-check pattern from 2026 paper."
   ```

2. **Write the raw file** under `kyota-wiki/raw/contrastive_tool_self_check_raw.md`. Preserve the source verbatim: quotes, section structure, citations. Do not rewrite prose to fit KYOTA style; `/raw/` is immutable episodic memory.

3. **Create the entity** at `kyota-wiki/entities/contrastive_tool_self_check.md` with this skeleton:
   ```markdown
   # Contrastive Tool Self-Check

   **Date:** <retrieval date>
   **Source URIs:**
   - <primary source>

   ## Technical Core
   <atomic claims, one per bullet where possible>

   ## Actionable Prompt Fragments
   ```text
   [SYSTEM: CTSC_EVALUATOR]
   <reusable prompt block>
   ```

   ## KYOTA Implications
   - Inference: <how this should shape specialist behavior>
   ```

4. **Register both files** in the same unit of work:
   - Append a one-line entry to `kyota-wiki/raw/index.md`.
   - Append a one-line entry to `kyota-wiki/entities/index.md` in alphabetical order.

5. **Distill reusable prompt fragments** into [`../schema/kyota_agent_schemas.md`](../schema/kyota_agent_schemas.md) only if the fragment belongs to the reusable module library. If it is a one-off, leave it in the entity and note the choice in the `HISTORY` record.

6. **Run deterministic checks:**
   ```bash
   kyota lint && kyota doctor
   ```
   Both must pass. Fix registry drift immediately - a new on-disk file without a registry line will trip the lint.

7. **Record VERIFY, RELEASE, HISTORY:**
   ```bash
   kyota verify  --agent <id> --files <same set> --note "kyota lint and kyota doctor passed; entity + raw registered; no prompt-library changes needed."
   kyota release --agent <id> --files <same set> --note "Released CTSC ingestion after VERIFY."
   kyota history --agent <id> --files <same set> --note "ADD: ingested contrastive tool self-check pattern; new raw, new entity, registry updates; schema/kyota_agent_schemas.md unchanged (one-off fragment)."
   ```

## Worked Example: `UPDATE` an Existing Entity
Scenario: a newer paper refines a claim in an existing entity without replacing the whole page.

1. `CLAIM` only the entity being edited (and `entities/index.md` only if the one-line summary changes).
2. Add the new source at the top of the `## Source Basis` block; keep older references so the provenance chain stays visible.
3. In the body, keep the prior claim but mark its scope: "Up to <earlier source>, X. As of <newer source>, Y supersedes X for <condition>." Do not silently overwrite.
4. If the change materially shifts the entity summary, touch the `entities/index.md` one-liner in the same `CLAIM`.
5. `kyota lint` + `kyota doctor`, then `VERIFY` / `RELEASE` / `HISTORY` naming the operation as `UPDATE`.

## Worked Example: `NOOP`
Scenario: a blog post restates prior guidance with no new evidence.

1. No claim is needed.
2. Append a single `HISTORY` record through `kyota history` naming the source and the reason the skip was appropriate (for example, "NOOP: 2026 blog post restates already-captured guidance from claude_context_rules.md; no net new guidance.").
3. Future agents can now reject the same source without re-reading it.

## Common Pitfalls
- **Registry drift.** New on-disk file without a registry line, or registry line without a file. `kyota lint` catches it; fix before `VERIFY`.
- **Over-broad claims.** Do not `CLAIM` the whole `/entities/` directory when only one file changes.
- **Paraphrasing `/raw/`.** The raw file is episodic memory; preserve source language and structure. Paraphrase only in the derived entity.
- **Silent `UPDATE`.** Overwriting a prior claim without preserving the supersession trail breaks `log.md` as audit history.
- **Premature schema promotion.** Do not add a prompt fragment to `../schema/kyota_agent_schemas.md` unless it is genuinely reusable across tasks; one-off fragments belong on the entity page.
- **Forgetting `HISTORY` on `NOOP`.** Without it, the next agent re-investigates the same dead-end source.
- **Skipping provenance dates.** Recency is a first-class decision factor in [`../schema/research_protocol.md`](../schema/research_protocol.md); undated entities force later agents to re-verify.

## Post-Ingest Invariants
After any ingestion the following must all hold:
- `kyota lint` passes.
- `kyota doctor` reports healthy.
- Every new `/raw/` file is linked from `raw/index.md`, and every new `/entities/` page is linked from `entities/index.md`.
- The ingesting agent's `CLAIM` is released, with a `VERIFY` that cites deterministic evidence and a `HISTORY` that names the operation (`ADD`/`UPDATE`/`DELETE`/`NOOP`).
- No normative rule is duplicated between `/schema/` and `/entities/` without an explicit canonical pointer.

## Cross-References
- Memory-operation semantics: [`./hierarchical_memory_rules.md`](./hierarchical_memory_rules.md).
- Lifecycle records and the shared action layer: [`./multi_agent_coordination.md`](./multi_agent_coordination.md).
- Operator startup, CLI cheatsheet, and VERIFY evidence standards: [`./specialist_playbook.md`](./specialist_playbook.md).
- Context-degradation safeguards for summarization discipline: [`./context_degradation_safeguards.md`](./context_degradation_safeguards.md).
