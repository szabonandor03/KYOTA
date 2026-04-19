# Progressive Disclosure UI

## Source Basis
- Derived from `../raw/UX_HCI_Research_Report.md`
- Primary upstream concepts: progressive disclosure, layered skill loading, adaptive questioning, and chat keyhole mitigation

## Purpose
Define how KYOTA should minimize user cognitive load while preserving full backend traceability for agent work.

## User-Facing Rules
1. Default to high-level summaries, not raw logs.
2. Hide verbose agent-to-agent traces, raw JSON payloads, long command output, and intermediate deliberation unless the user explicitly requests them.
3. Surface only the minimum information the user needs to make the next decision or understand the result.
4. When detail is necessary, reveal it progressively: summary first, specifics second, raw artifacts last.

## Backend Retention Rules
1. Store durable execution history in backend files such as `NOW.md`, entity pages, and git commit messages — not in the main user-facing response.
2. Preserve machine-oriented detail in auditable files, structured notes, or dedicated logs so specialists can recover context without overwhelming the user.
3. Do not paste raw tool payloads into shared user summaries when a concise explanation would preserve the meaning.

## Layered Loading Model
1. Start from metadata: read `index.md` before loading entity bodies or raw sources.
2. Load details on demand: open only the entities required for the current task.
3. Load deep resources only when execution, verification, or source validation actually requires them.

## Adaptive Questioning
1. Interrupt the user only when an answer materially changes the outcome.
2. Stop asking once the task is sufficiently specified to proceed safely.
3. Prefer making a documented reasonable assumption over presenting the user with a form-like interrogation.

## Response Shape
- Summary: what changed, what matters, what needs attention.
- Optional detail: verification notes, affected files, or key constraints.
- Raw evidence: only on request or when failure analysis requires it.
