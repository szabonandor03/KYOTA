# Simon Willison Codex Notes

Retrieved: 2026-04-21

## Source URLs

- https://simonwillison.net/2026/Feb/2/introducing-the-codex-app/
- https://simonwillison.net/2026/Feb/22/how-i-think-about-codex/

## Scope

This note captures the direct Simon Willison observations that most help explain Codex as an operational system rather than as “just another model.”

## Introducing The Codex App

Direct-source facts checked on 2026-04-21:

- Simon highlights first-class support for Skills and Automations as the most interesting new workflow surfaces in the Codex app.
- He notes that the app stores automation state in SQLite, making durable local state inspectable rather than opaque.
- Simon’s takeaway is that Codex behaves like a general agent harness that happens to be optimized first for programming.
- He also calls out that OpenAI frames Codex as useful beyond writing code because technical and knowledge-work tasks can both be mediated through code and tool use.

## How I Think About Codex

Direct-source facts checked on 2026-04-21:

- Simon quotes Gabriel Chua’s framing of Codex as `Model + Harness + Surfaces`.
- The post treats the harness as the collection of instructions and tools that wrap the model.
- Simon also highlights the claim that Codex models are trained in the presence of the harness, meaning tool use, compaction, execution loops, and iterative verification are not purely bolted on.

## Raw Implications (Not Yet Distilled)

- Simon’s notes help explain why “use Codex smoothly” is not only a model-choice problem. It is also a harness, instruction, tooling, and surface-design problem.
- Skills, automations, and inspectable local state make more sense when Codex is treated as an operating system for repeated work rather than as a one-shot chatbot.
