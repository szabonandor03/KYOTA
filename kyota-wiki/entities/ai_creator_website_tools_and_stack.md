# AI Creator-Website Tools and Stack (2024–2026)

**Date:** 2026-04-18
**Source URIs:**
- `../raw/creator_websites_and_ai_tools_raw.md` (Sections 1 and 7)

## Purpose

Decision support for choosing between (a) third-party AI website-builders and (b) authoring a site directly with an AI coding agent in an open-source code stack. Covers the 2026 tool landscape, the comparative tradeoffs, and the recommended Claude-Code-drivable stack for an archive-aesthetic creator site.

For prompt-craft once a tool or stack is chosen, see [`ai_creator_website_prompting.md`](./ai_creator_website_prompting.md). For the design canon the chosen tool must serve, see [`creator_web_design_canon.md`](./creator_web_design_canon.md). For reference sites to emulate, see [`creator_web_reference_set.md`](./creator_web_reference_set.md).

## Technical Core

### The Bifurcated 2026 Landscape

The market splits into two camps:

1. **AI-augmented legacy platforms** (Framer, Webflow, Wix Studio, Squarespace) — the AI assists layout and copy *inside* an existing visual editor. Output is hosted on the platform's infrastructure; export is limited or absent. The AI is a *stylistic assistant*.

2. **AI-native code generators** (Lovable, Bolt.new, v0, Claude Code, Cursor) — the prompt is the primary source of truth for a real codebase. Output is owned, exportable, and lives in Git. The AI is the *primary author*.

For creators with strong identity and the intent to own their site long-term, the AI-native code-generator camp is structurally better positioned. For creators who need a designed marketing site without engaging with code, Framer remains the strongest paid path.

### Tool Comparative Matrix

| Tool | Output | Free Tier | License | Self-Host | Agent-Drivable |
| --- | --- | --- | --- | --- | --- |
| Framer (AI) | Hosted proprietary | 1 project, subdomain | Proprietary | No | No |
| Webflow (AI) | Hosted proprietary | webflow.io subdomain | Proprietary | No | Partial (API/CLI) |
| Wix Studio AI | Hosted proprietary | Wix ads + subdomain | Proprietary | No | No |
| Squarespace AI | Hosted proprietary | 14-day trial only | Proprietary | No | No |
| v0 by Vercel | Exportable React | 200 credits/mo | Proprietary | No | Yes (CLI / sync) |
| Lovable | GitHub-synced React | 5 messages/day | Proprietary | No | Yes (GitHub sync) |
| Bolt.new | WebContainer / multi-framework | 150K tokens/day | Proprietary | No | Yes (browser IDE) |
| Cursor (agent) | Local codebase | 2000 completions | Proprietary | n/a | Yes (native) |
| Claude Code | Local codebase | User-licensed | Proprietary | n/a | Yes (native terminal) |
| OpenUI | Exportable code | Free | MIT (OSS) | Yes | Yes (Agent Skill) |
| Builder.io OSS | Headless components | Free | MIT (OSS) | Yes | Yes (local) |

**Free-tier limits and pricing change every quarter** — verify current values before committing to a tool. See [`../raw/creator_websites_and_ai_tools_raw.md`](../raw/creator_websites_and_ai_tools_raw.md) "Sourcing Notes" for which specific numbers above are weakly sourced.

### Three-Path Synthesis

**Path A — Best paid tool for a designer-minded creator who wants visual control and is willing to accept vendor lock-in: Framer.**
Best-in-class motion and typographic control, proprietary React framework underneath, no clean code export. Acceptable when the operator never plans to leave the platform. Not agent-drivable.

**Path B — Best free-tier path that does not sacrifice design quality: Bolt.new.**
WebContainer technology runs a real dev server in-browser, multi-framework support (Astro, Svelte, Vue, Next.js), generous daily token limits, browser IDE that an agent can help navigate. Output is real code, not a hosted-proprietary trap.

**Path C — Best path for a creator working with an AI coding agent who wants to fully own the code: Claude Code authoring directly in an open-source stack, with v0 used selectively for component scaffolding.**
Code lives in Git, deploys to a free edge target, no vendor lock-in, no monthly fee, no platform-side feature flag risk. This is the correct path when the operator already has Claude Code in the loop and intends to maintain the site over time.

### Open-Source Framework Landscape

| Framework | License | Momentum | Agent-Drivability | Best For |
| --- | --- | --- | --- | --- |
| Astro | MIT | High | High | Content-heavy archive sites; zero JS by default. |
| Next.js (current major: 16 as of 2026-04) | MIT | Extreme | Medium | Complex full-stack apps with high interactivity. |
| SvelteKit | MIT | Growing | High | Tiny bundles, smooth interactions, simple syntax. |
| Eleventy (11ty) | MIT | Niche | High | Zero-JS, markdown-first, extremely simple structure. |

**Astro is the primary recommendation for archive-aesthetic creator sites.** Its static-first model produces the fastest possible sites, its directory structure and Content Collections are simple for an LLM agent to navigate, and its zero-JS-by-default posture aligns with code-brutalist design discipline. Next.js is preferred only when the project genuinely needs full-stack interactivity that Astro cannot deliver.

### Open-Source UI / Design-System Layer

- **shadcn/ui** — not a library; a CLI that copies component source into the project. Gold standard for "escaping the generic look" because the operator owns every line.
- **Tailwind CSS** — the substrate everything else assumes. Default carefully — Tailwind without discipline produces the "Tailwind default" look the design canon explicitly rejects.
- **daisyUI** — Tailwind plugin with semantic class names (`.btn-primary`). Reduces Tailwind verbosity that confuses model context.
- **Aceternity UI / Magic UI** — high-wow motion components. **Use sparingly or not at all** for archive-aesthetic projects; they re-introduce the SaaS look the canon rejects.

### Open-Source Headless CMS Layer

- **Keystatic** — file-based; no database. Stores content as Markdoc/JSON in the Git repo. **Best fit for Claude Code workflows** because the agent edits the files directly without an API call.
- **Payload** — TypeScript-native, MIT-licensed, self-hostable. The report claims Payload is "now backed by Figma" — verify on payloadcms.com before relying on this.
- **Sanity** — generous free tier; powerful Content Lake; GROQ query language has a learning curve for agents.
- **Decap CMS, TinaCMS** — alternatives in the file-based / Git-based CMS space; less covered in the source report.

### Open-Source Motion Layer

- **Lenis** — smooth-scroll library; deliberate, opinionated, lightweight. Use for archive-aesthetic projects where one global motion choice is appropriate.
- **Motion** (formerly Framer Motion's open core) — micro-interactions; use sparingly per the design canon.
- **GSAP (free tier), Theatre.js, Rive** — covered in the source report but not recommended for the archive-aesthetic default.

### AI Coding Agents (Comparative)

- **Claude Code** — the recommended terminal agent. Best-in-class MCP server support (GitHub, Playwright) for tasks like screenshot review, site reconstruction, and live design iteration.
- **Aider** — fast CLI for pure code editing on existing repos. Lacks Claude Code's MCP skill ecosystem.
- **OpenHands (formerly OpenDevin)** — autonomous multi-step planning agent. Useful for unsupervised project scaffolding; less appropriate for design-sensitive iteration.
- **Cursor (agent mode)** — IDE-embedded; good for in-editor flow but less terminal-native than Claude Code.
- **Continue.dev, codex CLI** — covered in the source report; lower-priority alternatives.

### Free Deployment Surfaces

- **Cloudflare Pages** — truly free, no bandwidth limits on the free tier, native GitHub integration, edge-deployed for global speed. **Recommended deploy target for archive-aesthetic sites.**
- **Vercel free tier** — best for Next.js; bandwidth traps can surprise a viral creator.
- **GitHub Pages, Netlify free tier, Render, Fly.io** — viable alternatives with their own constraints.
- **Self-hosted via Coolify / Dokploy / CapRover** on a $5/mo VPS — the Full Sovereignty path for an operator who wants infrastructure ownership.

### The Recommended Claude-Code-Drivable Creator Stack

For an archive-aesthetic creator site (FIDESZ SAPKA's case, and the default recommendation for similar projects):

| Layer | Choice | Why |
| --- | --- | --- |
| Framework | **Astro** | Static-first speed; Content Collections map cleanly to the file-system / archive metaphor; zero JS by default supports code brutalism. |
| UI primitives | **shadcn/ui + Tailwind CSS** | Operator-owned component source; design system enforced via `tailwind.config.mjs` (custom palette, `font-mono`, `rounded-none`). |
| Motion | **Lenis** for global smooth scroll; **Motion** only for one or two named micro-interactions | Stays inside the design canon's "motion vocabulary defaults to none" rule. |
| CMS | **Keystatic** | File-based; Claude Code edits content directly in the repo; no database, no API key. |
| Deploy | **Cloudflare Pages** | Zero cost; no bandwidth ceiling; edge speed for an archive that may suddenly traffic-spike on a release. |
| Agent | **Claude Code** | Native terminal; best MCP support for screenshot-driven iterative design review (Playwright MCP). |

**Defenses:**
- 100% open-source or free-to-use across the stack. Zero recurring spend except optional custom domain (~$10/yr).
- Operator owns markdown, images, and code in Git. The site is fully sovereign.
- Claude Code can scaffold, edit content, swap images, run a dev server, take screenshots via Playwright MCP, and deploy — all from the terminal in the same repo as the KYOTA wiki.
- Identity elasticity is preserved because every component is operator-owned source code, not a vendor template.

## KYOTA Implications

### Decision Defaults

When the operator asks "what should we use to build a creator website," default to:
1. If the operator wants no code at all and accepts vendor lock-in: **Framer**.
2. If the operator wants a fast free prototype and may not maintain it: **Bolt.new**.
3. If the operator has Claude Code (this case) and intends to maintain the site: **the Recommended Stack above**.

Only deviate when the project genuinely requires full-stack interactivity Astro cannot serve (then: Next.js + the same UI / motion / CMS / deploy choices).

### KYOTA-Internal Note

This stack is consistent with KYOTA's own discipline: file-based content, version-controlled state, deterministic verification, no vendor APIs in the critical path. The same Git repo can host the wiki and the site if useful, or they can live in sibling repos.

## Evidence Notes

- Free-tier specifics (v0 200 credits/mo, Lovable 5 messages/day, Bolt 150K tokens/day, Cursor 2000 completions) are sourced to SEO aggregator blogs in the underlying GDS report. **Verify on each vendor's pricing page before committing the operator to a tool.**
- "Payload backed by Figma" is single-source. Verify on payloadcms.com.
- "OpenUI is 67% more token-efficient than JSON-based builders" is single-source quantitative; do not repeat in operator-facing copy without independent confirmation.
- "Next.js 16" is the current major as cited in the report on 2026-04-18; pin the version explicitly when scaffolding to avoid drift.
- "Cloudflare Pages has no bandwidth limits on the free tier" is repeatedly cited but verify against Cloudflare's current free-tier terms before promising the operator unlimited bandwidth — terms change.

## Actionable Prompt Fragments

```text
[SYSTEM: CREATOR_WEB_TOOL_SELECTION]
When the operator asks how to build a creator/artist website:

1. First clarify which path fits: Framer (paid, no-code, vendor-locked), Bolt.new (free, fast, throwaway-acceptable), or the Recommended Stack (Astro + shadcn/ui + Keystatic + Cloudflare Pages, agent-driven by Claude Code, fully sovereign).
2. For an operator with Claude Code already in the loop and intent to maintain the site, default to the Recommended Stack. Justify the choice, do not present it as the only option.
3. Before naming any specific free-tier limit, pricing, or feature, verify on the vendor's current pricing or docs page. The 2026-04 figures in this entity drift quickly.
4. Pin specific versions when scaffolding (Astro version, Next.js version, Tailwind major) so the agent's later iterations don't silently change the substrate.
5. Reject Aceternity UI / Magic UI / framer-motion-on-everything by default for archive-aesthetic projects — they re-introduce the SaaS look the design canon rejects. See creator_web_design_canon.md.
6. The default deploy target is Cloudflare Pages unless the project has a specific reason (Vercel-only Next.js feature, self-hosted PaaS preference) to deviate.
```
