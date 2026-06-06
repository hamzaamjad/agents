# Specification: Lightweight Agent Memory Context Summary

## Purpose

Add a lightweight, durable memory convention to this `.agents` workspace so future coding agents can quickly understand stable project decisions without reading every prior chat or transcript.

The convention should capture only high-signal, durable facts that affect future agent behavior: architecture decisions, workspace workflow invariants, known tradeoffs, and where to retrieve deeper context. It must not become a progress log, ticket replacement, or broad documentation rewrite.

## Background From Existing Workspace Patterns

Relevant existing docs establish these constraints:

- Instruction context should be small and curated. The existing context guidance repeatedly uses the diagnostic: "Would removing this line cause the agent to make mistakes?"
- Always-loaded files should contain project identity, critical constraints, and pointers, not detailed history.
- Session-scoped context belongs outside persistent instruction files.
- Ticket `## Outcome` blocks already serve as dense retrieval surfaces for completed ticket work.
- Retrospective guidance treats `AGENTS.md`, `CLAUDE.md`, and `.context/` as possible workspace improvement targets, but updates should be justified by evidence from actual sessions.

This spec therefore proposes a pointer-first memory file in `.context/`, not a large always-loaded instruction block.

## Goals

- Give agents a fast first stop for durable project memory.
- Preserve important decisions that otherwise live only in chat history.
- Keep the memory small enough that agents will actually read it.
- Make entries easy to search with plain text tools.
- Define clear promotion criteria so temporary session notes do not become durable memory.
- Complement existing ticket `## Outcome` blocks by linking to them instead of duplicating them.

## Non-Goals

- Do not create tickets as part of this convention.
- Do not implement scripts, hooks, embeddings, databases, or external memory services.
- Do not rewrite existing workspace docs broadly.
- Do not store complete chat summaries, raw transcript excerpts, or agent reasoning.
- Do not duplicate active ticket status, task progress, or TODO lists.
- Do not make memory files authoritative over source code, tickets, or explicit user instructions.

## Proposed Files

### 1. `.context/agent-memory.md`

Canonical durable memory index for future agents.

If `.context/` does not already exist, create it only when implementing this convention. The file should be manually edited by agents at natural consolidation points, such as the end of a session, after completing a meaningful workspace convention change, or after archiving ticket outcomes.

Recommended maximum size: 120 lines. If it exceeds that, split older or domain-specific detail into `.context/memory/` topic files and leave only pointers in the index.

### 2. Optional `.context/memory/<topic>.md`

Use only when one durable theme needs more detail than the index should carry.

Examples:

- `.context/memory/ticket-workflow-decisions.md`
- `.context/memory/context-engineering-decisions.md`
- `.context/memory/skill-authoring-decisions.md`

Topic files should be rare. Prefer linking to ticket outcomes, specs, or docs that already exist.

## Memory Entry Criteria

Add an item only when all of these are true:

- It is durable across future sessions, not just relevant to the current task.
- It affects future agent decisions or prevents a likely mistake.
- It is not already obvious from file names, source code, or nearby docs.
- It can be expressed in one concise entry with a source pointer.
- The user explicitly approved it, or it was established by a completed workspace artifact such as a merged ticket outcome, accepted spec, or stable instruction file.

Do not add an item when any of these are true:

- It describes in-progress task state.
- It is a preference that has only appeared once and may be situational.
- It restates generic coding-agent behavior.
- It duplicates a ticket `## Outcome` block without adding cross-cutting value.
- It may become stale quickly, such as a temporary branch name or today's blocker.

## File Format

Use this structure for `.context/agent-memory.md`:

```markdown
# Agent Memory

Purpose: Durable workspace context for future coding agents. Keep this file small, sourced, and decision-oriented.

## How To Use

- Read this after the root instruction file and before mining old chats.
- Treat source files, active tickets, and explicit user instructions as higher priority.
- Follow `Source` links for deeper context instead of expanding this file.

## Durable Decisions

### YYYY-MM-DD - <short decision title>

- Decision: <what is now considered true or preferred>
- Rationale: <why this choice was made, including rejected alternative if important>
- Applies when: <trigger condition for future agents>
- Source: `<path-or-artifact-id>`
- Tags: <5-8 searchable keywords>

## Open Questions

- <question> - Assumption until resolved: <current working assumption>. Source: `<path>`

## Review Notes

- Last reviewed: YYYY-MM-DD
- Prune entries that no longer affect agent behavior.
```

Use reverse chronological order within `Durable Decisions` so recent decisions are easy to find. Keep each entry to 5 bullets or fewer.

## Entry Types

### Durable Decision

Use for accepted project or workflow choices that should influence future agents.

Examples:

- Ticket archive retrieval should use dense `## Outcome` blocks before reading full archived tickets.
- Root instruction files should remain pointer-first and avoid session-scoped content.
- Worktree-heavy ticket workflows should avoid broad staging commands.

### Constraint Or Invariant

Use when violating the rule would likely break future work.

Examples:

- Archived tickets are read-only.
- Active ticket sources are authoritative over archived historical context.
- Memory entries must include a source pointer.

### Retrieval Pointer

Use when the memory index should tell agents where to look, not summarize everything.

Examples:

- For archived ticket decisions, search ticket `## Outcome` blocks first.
- For instruction-file quality standards, read engineering-context references before editing `AGENTS.md` or equivalents.

### Open Question

Use sparingly for unresolved but important ambiguity. Every open question needs a working assumption and a source.

## Update Workflow

Agents should update memory only at consolidation moments:

1. Identify candidate durable facts from the completed work.
2. Check whether the fact already lives in a stronger source such as a ticket outcome, instruction file, or spec.
3. If a stronger source exists, add only a short pointer or skip the entry.
4. Apply the entry criteria above.
5. Add or update one concise entry in `.context/agent-memory.md`.
6. Record unresolved clarification needs under `Open Questions` rather than blocking.
7. Before finishing, prune or revise any entry touched if it no longer passes the entry criteria.

Agents should not update memory in the middle of an implementation unless the user explicitly asks for a context consolidation pass.

## Retrieval Workflow For Future Agents

When starting a task in this workspace:

1. Read the root instruction source if present.
2. Read `.context/agent-memory.md` if it exists.
3. Follow only the memory entries whose `Applies when` trigger matches the task.
4. For completed-ticket history, search archived ticket `## Outcome` blocks before reading full tickets.
5. If memory conflicts with source files, active tickets, or explicit user instructions, treat the latter as authoritative and record the conflict for cleanup.

## Freshness And Pruning

Review `.context/agent-memory.md` during any instruction cleanup or session retrospective that recommends workspace context improvements.

Prune or revise entries when:

- A referenced path no longer exists.
- A decision has moved into a canonical instruction file or source doc.
- An entry describes completed progress rather than an enduring convention.
- The file exceeds 120 lines.
- An entry has not mattered in several sessions and no longer passes the "would removing this cause mistakes?" test.

## Precedence

Memory is advisory context, not an instruction source. Resolve conflicts in this order:

1. System/runtime instructions.
2. Explicit user request in the current session.
3. Directory-local instructions and active tickets.
4. Project-root instruction files.
5. Source code and tests as evidence of actual behavior.
6. `.context/agent-memory.md`.
7. Archived tickets, transcripts, and historical notes.

If two memory entries conflict, keep the newest only when its source clearly supersedes the older entry. Otherwise record an open question and do not silently choose.

## Relationship To Existing Ticket Outcomes

Ticket outcomes remain the best place for completed implementation detail. The memory file should not copy outcome blocks.

Use memory for cross-ticket conclusions, such as:

- "Archived `## Outcome` snippets are the retrieval surface for prior ticket work."
- "Do not modify `_archive/`; active sources are authoritative."
- "When a future task touches unfamiliar ticket-workflow behavior, search outcomes first."

If a memory entry points to an outcome, include the ticket or epic identifier and retrieval tags, not the full outcome body.

## Minimal Implementation Plan

This spec does not implement the convention. A future implementation should be limited to:

1. Create `.context/agent-memory.md` using the format above.
2. Seed it with 3-6 entries derived from stable, already-documented workspace decisions.
3. Add one short pointer from any root instruction file only if such a file already exists and is being intentionally maintained.
4. Avoid changing tickets, source code, or broad documentation during initial setup.

Suggested seed entries:

- Pointer-first context design and size limits.
- Ticket outcome blocks as archive retrieval surfaces.
- Separation of session-scoped notes from durable instruction files.
- Archived ticket directories are read-only.
- Worktree and staging boundaries for ticket workflows, if those workflows remain active.

## Acceptance Criteria

- `.context/agent-memory.md` exists and is under 120 lines at creation.
- Every memory entry includes `Decision`, `Rationale`, `Applies when`, `Source`, and `Tags`.
- No entry duplicates an entire ticket outcome, transcript, or skill section.
- At least one entry points to the ticket outcome convention instead of restating it.
- Open questions, if any, include a working assumption.
- No source code, tickets, or broad documentation are modified just to add the convention.

## Risks And Mitigations

- Risk: The memory file becomes another stale instruction surface.
  Mitigation: Treat it as advisory, require source pointers, and prune by the 120-line limit.

- Risk: Agents over-trust memory over active project state.
  Mitigation: Put precedence rules in the file and require conflict recording.

- Risk: The file grows into a transcript summary.
  Mitigation: Ban raw chat summaries and require durable decision phrasing.

- Risk: Useful implementation detail is lost.
  Mitigation: Keep implementation detail in ticket outcomes and link to it from memory only when the pattern generalizes.

## Clarifying Questions To Resolve Later

- Should `.context/agent-memory.md` be mentioned from a future root `AGENTS.md` if this workspace creates one?
- Should memory entries require explicit user approval, or is a completed/accepted workspace artifact enough?
- Should there be a scheduled review cadence, or only opportunistic pruning during retrospectives and instruction cleanup?
- Should old parent chat transcripts ever be mined to seed memory, or should seeding start only from current workspace docs and completed artifacts?
