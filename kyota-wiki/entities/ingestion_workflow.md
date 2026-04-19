# Ingestion Workflow

## Purpose
Concrete walkthrough for turning a new research source into durable KYOTA knowledge so ingestion takes minutes, not a re-read of every schema.

## Canonical Authority
- Source-of-truth rules: [`../schema/research_protocol.md`](../schema/research_protocol.md).
- Memory-operation semantics (`ADD`/`UPDATE`/`DELETE`/`NOOP`): [`./hierarchical_memory_rules.md`](./hierarchical_memory_rules.md).
- This page is operational; if it disagrees with a schema, the schema wins.

## When to Ingest vs Skip
Ingest when the source:
1. Introduces a capability, rule, or pattern KYOTA does not already encode (`ADD`).
2. Refines or supersedes a claim already in `/entities/` (`UPDATE`).
3. Invalidates or retires a claim currently in active guidance (`DELETE`).

Skip (`NOOP`) when the source:
- Restates guidance already captured with equal or better precision.
- Contains only editorial/marketing framing around an already-ingested technical point.
- Is published before 2024 and conflicts with [`../schema/research_protocol.md`](../schema/research_protocol.md)'s recency rule, unless it is the primary source for a concept still referenced by newer work.

When in doubt, prefer `NOOP` over speculative ingestion. Note the decision in `NOW.md` under **Recent decisions** so future agents do not re-evaluate the same source.

## Operation Decision Rule
| Situation | Operation | Minimal artifacts |
| --- | --- | --- |
| New fact, pattern, or rule not yet in `/entities/` | `ADD` | new raw file + new entity + both registry updates |
| Same concept refined by a newer source | `UPDATE` | new raw file + edited entity (preserve prior claim with caveat) + registry touch-up if summary changes |
| Claim is now invalid or duplicated | `DELETE` | edited entity (remove the claim). Do not erase the source in `/raw/` |
| Source offers no net new guidance | `NOOP` | `NOW.md` decision line noting the skip reason |

## Provenance Standards
Every `/entities/` page synthesized from research must carry:
- A `## Source Basis` or `## Sources` block naming the raw file in `/raw/` and, when available, the upstream paper/doc and retrieval date.
- A clear distinction between sourced claims and agent inference. Use an `## Evidence Notes` or `## KYOTA Implications` section for the latter so readers can tell them apart.
- Publication/retrieval date when it materially affects recency judgments.
- An explicit note for any conflict between sources: name the conflict, show the resolution rule, do not smooth it over.

Never paste a whole raw source into an entity. Distill atomic claims per [`./hierarchical_memory_rules.md`](./hierarchical_memory_rules.md) so later agents can revise one fact without rewriting the page.

## Pre-Ingest Checklist
1. Registries (`entities/index.md`, `raw/index.md`) are currently clean — on-disk files match one-for-one.
2. You have read [`../schema/research_protocol.md`](../schema/research_protocol.md) for any source not already inside `/raw/`.
3. You have decided the operation (`ADD` / `UPDATE` / `DELETE` / `NOOP`) before starting the write.

## Worked Example: `ADD` a New Capability
Scenario: a 2026 paper introduces a pattern KYOTA does not yet encode — call it "Contrastive Tool Self-Check" (CTSC).

1. **Write the raw file** under `kyota-wiki/raw/contrastive_tool_self_check_raw.md`. Preserve the source verbatim: quotes, section structure, citations. Do not rewrite prose to fit KYOTA style; `/raw/` is immutable episodic memory.

2. **Create the entity** at `kyota-wiki/entities/contrastive_tool_self_check.md` with this skeleton:
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

3. **Register both files** in the same unit of work:
   - Append a one-line entry to `kyota-wiki/raw/index.md`.
   - Append a one-line entry to `kyota-wiki/entities/index.md` in alphabetical order.

4. **Distill reusable prompt fragments** into [`../schema/kyota_agent_schemas.md`](../schema/kyota_agent_schemas.md) only if the fragment belongs to the reusable module library. If it is a one-off, leave it in the entity.

5. **Deterministic check.** Confirm every new `/raw/` file is linked from `raw/index.md` and every new `/entities/` page is linked from `entities/index.md`. Mention this in the reply as VERIFY evidence.

## Worked Example: `UPDATE` an Existing Entity
Scenario: a newer paper refines a claim in an existing entity without replacing the whole page.

1. Add the new source at the top of the `## Source Basis` block; keep older references so the provenance chain stays visible.
2. In the body, keep the prior claim but mark its scope: "Up to <earlier source>, X. As of <newer source>, Y supersedes X for <condition>." Do not silently overwrite.
3. If the change materially shifts the entity summary, touch the `entities/index.md` one-liner.

## Worked Example: `NOOP`
Scenario: a blog post restates prior guidance with no new evidence.

1. No edits to `/raw/` or `/entities/`.
2. Add a single line to `NOW.md` **Recent decisions** naming the source and the reason the skip was appropriate (for example, "NOOP: 2026 blog post restates already-captured guidance from `claude_context_rules.md`; no net new guidance.").
3. Future agents can now reject the same source without re-reading it.

## Common Pitfalls
- **Registry drift.** New on-disk file without a registry line, or registry line without a file. Reconcile before claiming done.
- **Paraphrasing `/raw/`.** The raw file is episodic memory; preserve source language and structure. Paraphrase only in the derived entity.
- **Silent `UPDATE`.** Overwriting a prior claim without preserving the supersession trail destroys audit history.
- **Premature schema promotion.** Do not add a prompt fragment to `../schema/kyota_agent_schemas.md` unless it is genuinely reusable across tasks; one-off fragments belong on the entity page.
- **Skipping provenance dates.** Recency is a first-class decision factor in [`../schema/research_protocol.md`](../schema/research_protocol.md); undated entities force later agents to re-verify.

## Post-Ingest Invariants
After any ingestion the following must all hold:
- Every new `/raw/` file is linked from `raw/index.md`, and every new `/entities/` page is linked from `entities/index.md`.
- No normative rule is duplicated between `/schema/` and `/entities/` without an explicit canonical pointer.

## Cross-References
- Memory-operation semantics: [`./hierarchical_memory_rules.md`](./hierarchical_memory_rules.md).
- Context-degradation safeguards for summarization discipline: [`./context_degradation_safeguards.md`](./context_degradation_safeguards.md).
- Specialist startup and VERIFY evidence standards: [`./specialist_playbook.md`](./specialist_playbook.md).
