# Specification: Lightweight Agent Memory Context Summary

Status: Proposed
Date: 2026-06-05
Workspace: `.agents`
Primary future artifact: `.context/agent-memory.md`

## Background

This workspace currently has skill and workflow documentation, but no root `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.context/`, or `.tickets/` directory. Existing context guidance favors small canonical instruction files, on-demand reference docs, and dense archived summaries over full historical rereads.

Future coding agents need a lightweight way to recover durable project decisions without scanning past chats or transient session notes. The convention should preserve only decisions that would change future behavior and should avoid turning persistent context into a progress log.

## Goals

- Give agents one predictable place to find durable project memory.
- Keep memory short enough that agents actually read it.
- Separate durable decisions from session-scoped progress, TODOs, and chat transcripts.
- Preserve source traceability so a future agent can inspect the original spec, ticket, commit, or transcript only when needed.
- Make stale or superseded decisions easy to detect and replace.

## Non-Goals

- Do not implement automation, indexing, embeddings, or transcript parsing.
- Do not create tickets or rewrite existing skill documentation.
- Do not require agents to summarize every chat.
- Do not store secrets, credentials, private user data, or verbatim chat logs.
- Do not use memory as a substitute for reading current source files before editing.

## Proposed Convention

Create `.context/agent-memory.md` as a curated, human-readable memory file. If a root `AGENTS.md` or tool-specific instruction file is added later, it should contain only a pointer such as:

`Read when: task depends on prior workspace decisions -> .context/agent-memory.md`

The memory file is not always-loaded context by default. Agents should read it when a task touches workspace conventions, skills, tickets, prompts, long-lived process decisions, or when the user references prior work without supplying the relevant context.

## Entry Qualification

Add or update a memory entry only when all checks pass:

- The fact is durable across sessions, not just useful for the current task.
- The information is not obvious from current source files or filenames.
- Knowing it would prevent a plausible future agent mistake.
- It has a bounded scope, such as `skills`, `ticket workflow`, `context hygiene`, or a named subsystem.
- It has a source reference: spec path, ticket ID, commit hash, PR, or short transcript link.

Do not add entries for routine implementation details, completed checklist items, temporary blockers, speculative ideas, or broad summaries of a whole conversation.

## File Structure

Use a compact Markdown file with this shape:

```markdown
# Agent Memory

Last reviewed: YYYY-MM-DD

Purpose: Durable workspace decisions that are not obvious from the current files. Keep this file curated; do not append session logs.

## Active Decisions

### YYYY-MM-DD - <short decision title>

- Scope: <workspace area>
- Decision: <one sentence>
- Rationale: <one sentence explaining why>
- Applies when: <trigger for future agents>
- Source: <path, ticket ID, commit, PR, or transcript link>
- Revisit when: <condition, date, or "unknown">

## Superseded Decisions

Keep only brief pointers here. Move long history to a separate archive only if this section grows.

## Open Durable Questions

- <question> - why it matters; current assumption
```

Entry titles should be specific and searchable. Prefer nouns and identifiers that future agents might query, such as `AGENTS.md`, `.context`, `archive-search`, or `Outcome schema`.

## Size and Freshness Limits

- Target file length: under 120 lines.
- Maximum active entries: 12 before pruning, merging, or splitting by scope.
- Maximum entry length: 6 bullets.
- Review stale dated entries when they are older than 90 days, or sooner if referenced paths no longer exist.
- If the file exceeds 150 lines, split long historical material into `.context/agent-memory-archive.md` and keep `.context/agent-memory.md` as the active index.

## Update Workflow

When a session produces a durable decision:

1. Check whether `.context/agent-memory.md` already has an entry for the same scope.
2. Prefer updating or replacing the existing entry over appending a near-duplicate.
3. If a decision is reversed, move the old entry to `Superseded Decisions` with a pointer to the replacing entry.
4. Keep source references short and stable.
5. Confirm no secrets, private data, or raw transcript excerpts were copied.

Agents may propose memory updates at the end of a session, but should only write them when the user asked for workspace context improvements or when the active task explicitly includes memory maintenance.

## Retrieval Workflow

At task start, agents should read `.context/agent-memory.md` when any of these are true:

- The request mentions previous chats, prior decisions, workspace conventions, or context cleanup.
- The task modifies skill files, instruction files, ticket workflow files, prompt assets, or evaluation workspaces.
- The task asks for a spec or plan whose correctness depends on durable project history.
- The agent is about to create a root `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.context/`, `.tickets/`, or `.prompts/` artifact.

After reading, the agent should still inspect current source files before editing. Memory is a routing aid, not authoritative over the repository state.

## Conflict Handling

- Current source files beat memory when they conflict.
- More specific scoped instructions beat general memory entries.
- If memory conflicts with a current instruction file and the correct source is unclear, record the conflict in notes or ask the user before editing persistent instructions.
- When resolving a conflict, update memory in the same change set only if memory maintenance is in scope.

## Privacy and Safety

The memory file must never contain secrets, API keys, credentials, `.env` values, private personal data, or destructive-operation instructions. Transcript references should be short links or identifiers, not copied conversations. Sensitive rationale should be summarized at the level needed for future engineering work.

## Acceptance Criteria

- A future implementation creates `.context/agent-memory.md` using the structure above.
- The file explains when to read it and what not to store.
- At least one example entry can be added without exceeding 6 bullets.
- The convention keeps active memory below 120 lines after normal use.
- Root instruction files, if introduced later, point to memory instead of duplicating it.
- No existing source files, tickets, or skill docs need to be rewritten to adopt the convention.

## Open Questions

- Should `.context/agent-memory.md` be committed to git by default, or should some teams keep it local?
- Should future session-retrospective workflows be allowed to update this file directly after user approval?
- If both `.tickets/_archive/` and `.context/agent-memory.md` exist, which decisions deserve promotion from ticket outcomes into memory?
- Should transcript source references use stable chat links, commit hashes, or both when both are available?
