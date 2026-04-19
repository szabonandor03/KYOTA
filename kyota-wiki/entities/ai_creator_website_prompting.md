# AI Site-Build Prompt Discipline (2024–2026)

**Date:** 2026-04-18
**Source URIs:**
- `../raw/creator_websites_and_ai_tools_raw.md` (Sections 5 and 6)

## Purpose

How to prompt AI tools (third-party site-builders or AI coding agents) to produce *designed* output rather than generic SaaS-template defaults. Captures the constraint-first prompting model, the two distinct flows (third-party builder vs. AI coding agent), the AI-build anti-patterns to refuse, and the mitigations that hold a design system steady across iterations.

For the design canon the prompts must serve, see [`creator_web_design_canon.md`](./creator_web_design_canon.md). For tool selection, see [`ai_creator_website_tools_and_stack.md`](./ai_creator_website_tools_and_stack.md). For broader execution-pattern selection (RCI, deterministic reflector, etc.), see [`execution_patterns.md`](./execution_patterns.md).

## Technical Core

### The Constraint-First Prompting Model

The single most important shift in 2024–2026 prompting practice is moving from **"describe how it should look"** to **"describe the constraints that bound the look."** The agent (or builder) is given the *grammar* of allowed moves, not the *aesthetic adjective* to interpret.

Constraint axes to specify explicitly in any creator-site prompt:

1. **Typography stack — name the fonts and the configuration.**
   Don't say "use a clean monospace." Say: "Use IBM Plex Mono. Base size 14px, tracked at -0.02em, line-height 1.1. Headings at 32px and 80px only — no other sizes allowed."

2. **Grid structure — name the columns and the rules.**
   Don't say "use a Swiss grid." Say: "Strict 12-column grid. All content starts at column 2 and ends at column 11. 1px black borders between modules. No element may break the grid."

3. **Motion vocabulary — define the physics, not the feel.**
   Don't say "make it feel premium." Say: "No ease-in or ease-out. All hover state changes are instant. The only allowed transition is `color` and `background-color`, both at 0ms duration."

4. **Color discipline — name the palette and forbid drift.**
   Don't say "monochrome." Say: "#000 and #FFF only. No grays, no opacity-based tints. The only deviation allowed is one identity color (#7C3AED for FS purple), used only on the catalog ID badges."

5. **Reference URLs — provide the exact sites to emulate.**
   "Emulate the archival structure of canaryyellow.com but the typographic weight of paulmacgregor.com." Reference URLs let the model anchor on a real artifact rather than its training-data average.

6. **Tonal posture — name what the copy is and is not.**
   "Deadpan. Hungarian. No exclamation points, no 'OUT NOW,' no marketing voice. If a section is empty, write 'pending' or '—', not 'Coming Soon!'."

### Flow A — Prompting Third-Party AI Site-Builders

For Framer, Lovable, v0, Bolt, Webflow AI, Wix Studio AI, the prompt structure is:

1. **Constraint preamble.** State the six axes above before describing any feature.
2. **Layout structure.** Name the page or section in spatial / structural terms (e.g., "a 4-column grid of artifacts," not "a portfolio gallery"). Avoid SaaS section names ("hero," "features," "testimonials") — they trigger template-shape lock-in.
3. **Content inventory.** Provide actual content (real titles, dates, IDs) or stub placeholders that match the site's posture. Lorem ipsum drags the agent toward generic.
4. **Iteration discipline.** After the first generation, never accept the first output. Reject and re-prompt with a *more specific* constraint (e.g., "the borders are too thick — reduce to exactly 1px and remove the drop shadow"). Three-pass refinement is the floor.

### Flow B — Prompting AI Coding Agents (Claude Code, Cursor, Aider)

For agent-authored code in an OSS stack, the prompt structure is:

1. **Establish load-bearing walls in repository config.** Before any feature work, write the design system into source-of-truth config files: `tailwind.config.mjs` (palette, fonts, spacing scale, `rounded-none`, no extras), `CLAUDE.md` or `AGENTS.md` (the design invariants the agent cannot violate), `src/styles/globals.css` (font imports, base reset). Future prompts reference these files instead of restating constraints.

2. **Constrain the component library up front.**
   "You are limited to the components in `src/components/ui/`. Do not invent new Tailwind class combinations. If a layout requires a primitive that does not exist, add it to that directory and document its API in a comment block. Never inline a one-off style."

3. **Provide reference URLs and screenshots.**
   Drop a URL into the prompt and ask the agent to fetch and consider it (via WebFetch or Playwright MCP). Screenshot review beats verbal description for aesthetic conformance.

4. **Snapshot-driven iteration.**
   "Run the dev server, take a screenshot of `/archive`, and compare it to the screenshot at `references/canary_yellow.png`. Tell me three specific places where ours drifts from the reference, and propose the smallest possible code change for each." This is the agent-equivalent of the deterministic-reflector pattern in [`execution_patterns.md`](./execution_patterns.md).

5. **Snapshot tests as design lock.**
   For sites that need to stay visually stable across edits, add Playwright screenshot tests for the canonical pages. Future agent edits that change pixels in unintended ways fail the test. Pair each canonical page with a reference screenshot committed to the repo and a CI step that diffs against it.

### Worked Example 1 — Third-Party Builder Prompt (Lovable / v0 / Bolt)

> Create a single-page archive for a 3-person music group. Aesthetic: Technical Mono. Pure black and white only — no gray. Typography: IBM Plex Mono, base 14px, tracked tightly (-0.02em), line-height 1.1. Layout: 12-column grid; all content starts at column 2, ends at column 11. Hero is the group name in 80px bold monospace, left-aligned, occupying one row. Below the hero, a 4-column grid of "Artifacts." Each artifact is a square with a 1px solid black border and no rounded corners. Inside each square: a pixelated thumbnail (image-rendering: pixelated), a date in YYYY-MM-DD format, and a 6-digit ID number. No smooth scrolling. No fade-ins or transitions. On hover, the artifact inverts its colors instantly (background to black, text to white). On click, the artifact opens a modal styled exactly like a Mac OS Finder window — title bar with three traffic-light dots, a path breadcrumb, a file-list view of the track's metadata. All borders are 1px solid black. Never round any corner. Never add a drop shadow. Never animate.

### Worked Example 2 — AI Coding Agent Prompt (Claude Code authoring Astro)

> Scaffold a new Astro project with Tailwind CSS at `./site/`. We are building an archive-aesthetic site for a Hungarian hip-hop group called FIDESZ SAPKA. Posture: deadpan, file-system metaphor, no marketing voice. Step 1: define the design system in `tailwind.config.mjs`. Restrict the palette to `#000`, `#FFF`, and a single identity purple `#7C3AED` named `fs-purple`. Set `fontFamily.mono` to `["IBM Plex Mono", "ui-monospace", "monospace"]`. Set `borderRadius.DEFAULT` to `0`. Remove `rounded-md`, `rounded-lg`, etc. from utilities. Step 2: write `CLAUDE.md` at the project root naming the design invariants — black/white plus fs-purple only, monospace only, no rounded corners, no shadows, no transitions longer than 0ms, no `framer-motion`, no Aceternity UI. Step 3: create an `Artifact.astro` component. It renders one row in a native HTML `<table>` with columns `ID`, `FILENAME`, `DATE`, `TYPE`. Use a real `<table>`, not a `<div>` grid — accessibility and archival authenticity. Step 4: build a homepage at `src/pages/index.astro` that renders the catalog as one `<table>` of all artifacts. Step 5: install `@playwright/test`, write one snapshot test that takes a full-page screenshot of `/`, and commit the baseline. Before completing the task, run `astro build` to confirm zero errors and `playwright test` to confirm the snapshot baseline lands. Do not install `framer-motion`, `lucide-react`, or any UI library not explicitly named here. If you need a primitive that does not exist, add it to `src/components/ui/` and document its API in a comment.

## AI-Build Anti-Patterns and Mitigations

| Failure mode | Recognition | Mitigation |
| --- | --- | --- |
| **Scaffold-then-drift.** Agent builds a coherent first draft; each follow-up prompt introduces new spacing, color, or padding values that drift from the canon. | New PR adds `bg-gray-50`, `rounded-md`, or a font you didn't authorize. | `CLAUDE.md` / `AGENTS.md` enumerates design invariants. Prompt the agent to re-read it before any feature work. Snapshot tests catch visual drift. |
| **Template-shape lock-in.** Agent's first generation is a Navbar + Hero + 3-Column Features layout; every later prompt fits into that shape. | The site has "features," "how it works," "testimonials" sections you didn't ask for. | First prompt names the structure as "Table" or "File List," never "Hero" or "Features." Refuse and rewrite if the first scaffold uses SaaS section names. |
| **Motion-as-decoration.** Default `framer-motion` fade-ins on every element. | Page elements fade in on scroll; hover states have spring animations. | Explicit prompt: "Do not install motion libraries. Native CSS transitions only, max 0ms by default." Audit `package.json` after every scaffold. |
| **Accessibility regressions.** Agent uses `<div>` for everything; missing `aria-label`, no keyboard tab-ordering, no semantic landmarks. | `axe` / `lighthouse` accessibility score drops; tab key cycles unpredictably. | Run `@axe-core/playwright` or `lighthouse-ci` on every PR. Prompt: "Use semantic HTML (`<header>`, `<nav>`, `<main>`, `<table>`, `<button>`); a `<div>` is a last resort." |
| **Looks-fine-shipped-as-is trap.** Operator accepts the agent's first guess for typography, spacing, or hierarchy. | The site looks "fine" but every grid module is a different size. | Three-pass refinement floor: never ship the first generation. Each refinement names one specific value to change with the new value. |
| **Type-stack default.** Agent picks Inter or Roboto because they are training-data defaults. | The site has Inter even though you didn't specify a font. | Provide the exact `.woff2` or Google Font import in the first scaffold. Set `fontFamily.sans` and `fontFamily.mono` in `tailwind.config.mjs` *before* any page is built. |
| **AI-Tailwind-default look.** Pastel backgrounds, `rounded-2xl` cards, lucide icons in feature grids, gradient hero text. | The page looks like every other 2024–2025 vibe-coded landing page. | Forbid the entire register in `CLAUDE.md`: no pastels, no rounded corners, no lucide-react, no gradient text, no card layouts unless specifically requested. |
| **Stop prompting; just edit.** The agent can't get a specific value right after three tries. | Three iterations later, the spacing is still wrong. | Recognize the moment. Open the file, edit the line by hand, commit, then resume with the agent. Don't burn ten more turns on a one-line CSS fix. |

## KYOTA Implications

### Mapping to KYOTA's Existing Discipline

The constraint-first prompting model maps directly to existing KYOTA practice:
- **Load-bearing walls in `CLAUDE.md`** is the same pattern as KYOTA's own `kyota-wiki/CLAUDE.md` routing contract.
- **Snapshot tests as design lock** is the same pattern KYOTA already runs against the TUI dashboard (`tests/__snapshots__/test_tui/*.svg`).
- **Three-pass refinement floor** maps to the explicit RCI execution pattern in [`execution_patterns.md`](./execution_patterns.md).
- **Deterministic reflector for design** (run dev server → screenshot → compare → propose smallest fix) is a domain-specific instance of the deterministic-reflector pattern.

When KYOTA helps build a creator site, it inherits its own discipline: shared action layer, structured logging, snapshot-test verification, no silent drift.

### For the FIDESZ SAPKA Website Specifically

When the FS site work begins:
1. Author the design system into `tailwind.config.mjs` and a project-level `CLAUDE.md` *before* writing any page.
2. Pin Astro and Tailwind versions explicitly.
3. Include `creator_web_design_canon.md` and `creator_web_reference_set.md` as input context to every design-affecting prompt.
4. Snapshot-test the homepage before committing the first content; lock the visual baseline early.
5. Refuse motion libraries and Aceternity-style component packs from day one.

## Actionable Prompt Fragments

```text
[SYSTEM: AI_SITE_BUILD_PROMPT_DISCIPLINE]
When prompting any AI tool (third-party builder or coding agent) to generate or edit a creator/artist website:

1. Constraint-first, never aesthetic-first. Name the typography stack (specific font + size + tracking + leading), grid (columns + rules), motion vocabulary (physics, defaulting to none), color palette (exact hex codes + drift rule), reference URLs, tonal posture.
2. Write design invariants into a CLAUDE.md / AGENTS.md / project README *before* any feature work. The agent must read this file before each design-affecting edit. Snapshot tests enforce it across iterations.
3. Forbid SaaS section nouns ("hero," "features," "testimonials") in the first prompt. Use spatial/structural language: "a 4-column grid of artifacts," "a native HTML table of releases."
4. Forbid motion libraries by default. Native CSS transitions only, 0ms duration by default. Audit package.json after every scaffold; uninstall any unauthorized library.
5. Three-pass refinement floor — never ship the first generation. Each refinement names one specific value to change with the new value.
6. Use snapshot tests as design lock. For Astro/React sites, Playwright screenshot tests on canonical pages. New visual drift fails the test.
7. Provide reference URLs and screenshots, not aesthetic adjectives. The agent anchors on real artifacts better than on words like "premium" or "minimal."
8. When the agent can't land a specific value after three tries, stop prompting and edit the file by hand. Resume with the agent after.
9. Cross-reference creator_web_design_canon.md (what counts as good), creator_web_reference_set.md (what to emulate), and ai_creator_website_tools_and_stack.md (which substrate to build on). The prompt should serve all three.
```
