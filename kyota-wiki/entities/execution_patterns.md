# Execution Patterns

## Purpose
Help an agent pick the smallest fitting execution loop for a task - direct execution, explicit RCI, deterministic reflector, or formal verification gate - and compose them when one alone is not enough. This page is the operational selector over the prompt modules in [`../schema/kyota_agent_schemas.md`](../schema/kyota_agent_schemas.md).

## Canonical Authority
- Prompt fragments and module contracts: [`../schema/kyota_agent_schemas.md`](../schema/kyota_agent_schemas.md) (normative).
- Underlying entities:
  - [`./recursive_criticize_improve.md`](./recursive_criticize_improve.md)
  - [`./autonomous_verification_loops.md`](./autonomous_verification_loops.md)
  - [`./formal_verification_tool_use.md`](./formal_verification_tool_use.md)
  - [`./jit_tool_loading.md`](./jit_tool_loading.md)
- This page is operational: it decides *when and how* to apply those modules; it does not redefine them.

## The Four Patterns at a Glance
| Pattern | One-line purpose | External verifier? | Core module |
| --- | --- | --- | --- |
| Direct execution | Produce the output in one pass and move on. | No | none |
| Explicit RCI | Force a separate critique step before refinement when rigid constraints exist. | No | `explicit_rci_chain` |
| Deterministic reflector | Let a compiler, test, linter, or search grade the draft and drive correction. | Yes | `deterministic_reflector` |
| Formal verification gate | Check proposed tool arguments against invariant formulas before execution. | Yes | `formal_verification_gate` |

## Selection Decision Tree
Walk this top-down; the first matching row wins. Everything above "direct execution" is a reason to escalate.

1. **Does the task propose a tool call whose failure is costly or irreversible** (file deletion, external API write, money movement, privileged action)? -> **Formal verification gate**. Pair with explicit invariant formulas and a `UNSAT` correction path.
2. **Can an external tool produce deterministic evidence about the draft** (compiler, `pytest`, `kyota lint`, search hit count, type checker, formal solver)? -> **Deterministic reflector**. Use the tool output as the correction signal, not free-form self-critique.
3. **Does the task have rigid invariants, formatting constraints, or policy rules that a single pass tends to violate** (router parity, schema shape, lifecycle rules, style contracts)? -> **Explicit RCI**. Keep the critique phase separate from the refinement phase.
4. **Otherwise** -> **Direct execution**. Do not manufacture loops for tasks that do not need them.

If more than one trigger applies, see "Composition Recipes" below instead of collapsing them into a single pass.

## Task-to-Pattern Mapping
Concrete mappings for the kinds of work this workspace sees:

| Task | Pattern | Why |
| --- | --- | --- |
| One-line entity registry update | Direct execution | Low risk; `kyota lint` afterward is cheap validation, not a loop. |
| New entity page synthesizing a raw source | Explicit RCI (critique against provenance + memory-operation rules), then direct merge | Rigid structure (Source Basis, provenance, atomic claims). |
| Code edit where `pytest` exists | Deterministic reflector with `pytest` as verifier | External tool produces deterministic pass/fail. |
| Schema / contract change to the coordination layer | Deterministic reflector with `kyota lint` + a disposable probe cycle | Lifecycle invariants are testable. |
| Proposed `kyota recover` on a stale scope | Formal verification gate (agent identity, stale-marker presence, scope exactness) | Irreversible cleanup of someone else's claim. |
| Orchestrator routing decision | Direct execution | One-shot decision; no invariant verifier exists. |
| Distillation of a large raw source into multiple entity pages | Explicit RCI per entity, then deterministic reflector on `kyota lint` | Rigid shape + external structural check. |

When a task is not on the table, fall back to the decision tree.

## Evidence the Pattern Produces for VERIFY
The `VERIFY` record should cite the evidence the chosen pattern actually generates. What counts:

| Pattern | Acceptable `VERIFY` evidence |
| --- | --- |
| Direct execution | Post-hoc checks such as `kyota lint`, `kyota doctor`, a targeted test, or a router parity diff - cited explicitly in the note. |
| Explicit RCI | Either `CRITIQUE_CLEAN` from the critique step or a summarized flaw list plus the refinement that resolved it, paired with a post-refinement structural check. |
| Deterministic reflector | The verifier's output summary: pass/fail, counts, failing test names, lint errors cleared. Paste the signal, not the command noise. |
| Formal verification gate | The `SAT` decision on the invariant formulas with the formulas themselves, or the `UNSAT` trace and the revised arguments that satisfied the gate. |

Intuition-only review is never sufficient for non-trivial shared work. See [`./specialist_playbook.md`](./specialist_playbook.md) for the broader VERIFY evidence standard.

## Composition Recipes
When a task triggers more than one row in the decision tree, compose instead of overloading a single loop. Recipes below reuse the naming in [`../schema/kyota_agent_schemas.md`](../schema/kyota_agent_schemas.md).

1. **Constraint-heavy drafting with an external check**
   `explicit_rci_chain` -> `deterministic_reflector` -> final merge.
   Use for: new entity pages with a `kyota lint` check afterward, schema edits that must satisfy both structural rules and lint.
2. **Dynamic tool execution**
   `jit_skill_router` -> draft or propose tool call -> `formal_verification_gate` -> execute -> `deterministic_reflector`.
   Use for: any multi-step action where the tool set should not be resident and the call itself needs an invariant check.
3. **Self-healing remediation loop**
   draft -> `deterministic_reflector` -> fix instructions -> `explicit_rci_chain` refinement -> re-verify.
   Use for: iterative code/doc fixes where the first reflector pass produces a concrete fix list.

Keep the order explicit in the `HISTORY` note so the composition remains auditable.

## Anti-Patterns
- **RCI on a one-line change.** The critique overhead exceeds the error budget. Use direct execution plus a post-hoc check.
- **Reflector without a real verifier.** If the "reflector" is just the same model re-reading its own draft, it is implicit self-critique - use explicit RCI or admit it is direct execution.
- **Formal gate on a low-risk call.** Writing invariants for a tool call that cannot lose work or money is busywork; prefer a reflector on the observable outcome instead.
- **Stacking all three loops by default.** Over-composition burns context and slows iteration. Walk the decision tree, escalate only when the trigger fires.
- **Silent critique inside drafting.** When RCI is chosen, the critique must be captured as a separate cognitive step, not folded into the rewrite prose. Explicit RCI outperforms implicit RCI on rigid constraints.
- **Treating `VERIFY` as a rubber stamp when the pattern produced no evidence.** If no deterministic signal was generated, either choose a pattern that produces one or narrow the slice until a post-hoc check applies.

## Worked Example: New Entity Page with Structural Verifier
Scenario: an agent is adding a new operational entity page that must follow the workspace's provenance structure and keep `kyota lint` clean.

1. **Select patterns.** Rigid structural constraints + external verifier -> composition recipe 1: `explicit_rci_chain` then `deterministic_reflector`.
2. **Draft** the entity page from the selected sources.
3. **Critique phase (`explicit_rci_chain` step 1).** Check the draft against: required sections, provenance rules, atomic claims, absence of duplicated normative rules. Produce either `CRITIQUE_CLEAN` or an explicit flaw list. Do not rewrite yet.
4. **Refine** only if flaws exist.
5. **Reflector phase (`deterministic_reflector`).** Run `kyota lint` and `kyota doctor`. Capture the pass/fail signal. If failing, feed the failure trace back as fix instructions and re-refine, not re-critique.
6. **Release with evidence.** The `VERIFY` note cites both the RCI outcome (`CRITIQUE_CLEAN` or the flaws resolved) and the reflector outcome (`kyota lint` clean, `kyota doctor` clean).
7. **History** names the composition used so future audits can reproduce the reasoning.

## Budget and JIT Integration
- Pattern choice happens inside the `BUDGET -> SELECT -> GENERATE` sequence from [`./spl_declarative_context.md`](./spl_declarative_context.md). Pick the pattern before you load prompt fragments or tool schemas.
- Load only the modules the chosen pattern needs; unload them when the execution tick reaches terminal state. See [`./jit_tool_loading.md`](./jit_tool_loading.md).
- If the task splits cleanly, each subtask can pick its own pattern. Do not apply a single heavy loop uniformly to a multi-part task.

## Cross-References
- Prompt fragments and module contracts: [`../schema/kyota_agent_schemas.md`](../schema/kyota_agent_schemas.md).
- Operator startup, CLI cheatsheet, and overall VERIFY evidence standards: [`./specialist_playbook.md`](./specialist_playbook.md).
- Record lifecycle, staleness, and the shared action layer: [`./multi_agent_coordination.md`](./multi_agent_coordination.md).
- Ingestion-specific loop choices and pitfalls: [`./ingestion_workflow.md`](./ingestion_workflow.md).
- Context-degradation rules that bound any composition: [`./context_degradation_safeguards.md`](./context_degradation_safeguards.md).
