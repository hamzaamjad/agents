# SPEC-agent-memory-context-summary-2026-06-05

## Summary

Define a lightweight agent memory/context summary convention for the `.agents` workspace so future coding agents can quickly understand durable project decisions without reading every prior chat transcript.

The convention should add one small, agent-readable durable memory surface and a clear update protocol. It should complement, not replace, existing skills such as `engineering-context`, `session-retrospective`, and `ticket-workflow`.

## Existing Workspace Context

Read-only inspection found:

- No root `AGENTS.md`, `CLAUDE.md`, or `README` in `/Users/hamzaamjad/.agents`.
- `skills/engineering-context/SKILL.md` treats instruction files as production interfaces and prefers a canonical `AGENTS.md` plus thin overlays.
- `skills/engineering-context/references/context-design-patterns.md` defines dynamic loading tiers: always-loaded core, on-demand modules, and session-scoped context.
- `skills/engineering-context/references/agents-md-spec.md` warns against bloated always-loaded context and requires no session-scoped progress logs in `AGENTS.md`.
- `skills/session-retrospective/SKILL.md` treats `AGENTS.md`/`CLAUDE.md` as first-class memory after explicit user approval, and allows `.context/` for durable domain or workspace context.
- `skills/ticket-workflow/SKILL.md` defines tickets as structured execution artifacts; this memory convention should not create or depend on tickets.

## Clarifications, Assumptions, And Recorded Questions

Because this evaluation task forbids stopping to ask the user, the following assumptions drive the spec:

- Assumption A1: The memory convention should be file-based and repository-local, not an external database, vector store, or chat transcript index.
- Assumption A2: The first implementation may create `.context/agent-memory.md` because the retrospective skill already names `.context/` as the place for durable workspace context.
- Assumption A3: If root `AGENTS.md` and `CLAUDE.md` are later introduced, they should stay lean and point to `.context/agent-memory.md` rather than duplicating its entries.
- Assumption A4: "Durable project decisions" means decisions expected to affect future work across sessions: canonical workflow choices, permission boundaries, architecture conventions, accepted tradeoffs, and recurring user preferences.
- Assumption A5: Completed task logs, transient TODOs, and "what I tried this session" notes are not durable memory unless they change how future agents should operate.

Recorded questions for the implementing agent or user:

- Q1: Should the initial memory file be created immediately, or only after the first session produces a durable decision worth recording?
- Q2: Should `AGENTS.md` and `CLAUDE.md` both be created as thin pointers if neither exists, or should the workspace start with only `.context/agent-memory.md`?
- Q3: Should memory entries cite parent chat transcripts when available, or should citations prefer local specs, tickets, and docs only?
- Q4: Who is allowed to mark a memory entry obsolete: any agent after inspection, or only the user?

## Scope

This specification covers:

- A durable memory file convention for the `.agents` workspace.
- The minimum structure future agents can scan quickly.
- Rules for what belongs in durable memory versus tickets, specs, session notes, and chat transcripts.
- Update and verification requirements for future implementation.

## Non-Goals

This specification does not cover:

- Creating tickets or decomposing work into tickets.
- Implementing the memory convention in this evaluation pass.
- Rewriting existing skills or broad documentation.
- Building automated transcript mining, embeddings, search, or external storage.
- Capturing every historical decision already present in past chats.
- Replacing existing skill instructions.

## Proposed Convention

Future implementation should create a single durable memory file:

`/.context/agent-memory.md`

If root instruction files are added later, they should include only a short pointer such as:

`Read when: onboarding to this workspace or checking durable project decisions -> .context/agent-memory.md`

The memory file should be short enough to read at the start of a session, but not automatically loaded into every context unless the host supports lightweight pointers. Target length is under 100 lines, with a hard review threshold at 150 lines.

## Memory File Structure

`/.context/agent-memory.md` should use stable headings:

1. `# Agent Memory`
2. `## Purpose`
3. `## Durable Decisions`
4. `## Workspace Conventions`
5. `## User Preferences`
6. `## Open Questions`
7. `## Maintenance Rules`

Each durable decision should use a stable ID:

`MEM-YYYYMMDD-NNN`

Example entry shape:

```markdown
### MEM-20260605-001: Keep durable memory separate from tickets

- Decision: Store cross-session workspace context in `.context/agent-memory.md`, not in `.tickets/`.
- Rationale: Tickets are execution artifacts; durable memory should remain lightweight and task-independent.
- Applies when: Future agents need workspace-level decisions before planning or editing.
- Source: `skills/ticket-workflow/SKILL.md`, `skills/session-retrospective/SKILL.md`
- Status: active
```

Valid status values are `active`, `superseded`, and `needs-review`.

## Requirements

### MEM-REQ-001: Define One Canonical Durable Memory File

The convention must define `.context/agent-memory.md` as the canonical place for durable cross-session workspace decisions.

Rationale: The workspace currently has no root instruction file, and the retrospective skill already identifies `.context/` as appropriate for durable context.

### MEM-REQ-002: Keep Always-Loaded Instructions Lean

If `AGENTS.md`, `CLAUDE.md`, or another always-loaded instruction file is introduced, it must point to `.context/agent-memory.md` instead of copying memory entries.

Rationale: Existing `engineering-context` guidance warns that bloated always-loaded context reduces task success and increases cost.

### MEM-REQ-003: Separate Durable Memory From Session State

The memory convention must exclude progress logs, transient TODOs, current blockers, implementation attempt history, and task-specific scratch notes.

Rationale: Existing context design guidance says session-scoped context belongs in plan files, session notes, or git history, not persistent instruction files.

### MEM-REQ-004: Use Stable Entry IDs

Every durable decision entry must have a stable `MEM-YYYYMMDD-NNN` ID and a short title.

Rationale: Stable IDs let future agents reference decisions without relying on fragile headings or full-text quotes.

### MEM-REQ-005: Include Decision, Rationale, Applicability, Source, And Status

Each durable decision must include:

- `Decision`
- `Rationale`
- `Applies when`
- `Source`
- `Status`

Rationale: These fields make entries auditable while staying compact.

### MEM-REQ-006: Define Entry Admission Criteria

A future agent may propose adding an entry only when the information is expected to affect more than one future session or prevent a likely repeated mistake.

Information should not be added if it can be inferred from current source files, tooling, linters, package metadata, or a focused spec.

Rationale: This follows the engineering-context diagnostic: "Would removing this line cause the agent to make mistakes?"

### MEM-REQ-007: Require Explicit Approval For Memory Updates

Agents must ask before adding, changing, superseding, or deleting durable memory entries, except when operating under a user request that explicitly asks them to update memory/context docs.

Rationale: Durable memory changes affect future agents and should not silently encode mistaken conclusions.

### MEM-REQ-008: Prefer Superseding Over Deleting

Obsolete entries should be marked `superseded` with a replacement pointer when useful. Deletion should require explicit user approval.

Rationale: This preserves decision history without forcing agents to read full chat transcripts.

### MEM-REQ-009: Keep Sources Local And Durable

Sources should prefer local specs, skills, tickets, docs, commits, or concise transcript references. Long chat transcripts must not be required reading for understanding a memory entry.

Rationale: The goal is to avoid making future agents reconstruct project decisions from past chats.

### MEM-REQ-010: Add A Maintenance Rule

The memory file must include a maintenance rule instructing agents to review entries when they touch related workflows and to mark stale entries as `needs-review` rather than silently trusting them.

Rationale: Durable memory can rot; status tagging makes uncertainty visible.

## Acceptance Criteria

### MEM-AC-001

File inspection confirms the implemented convention creates or specifies `.context/agent-memory.md` as the only canonical durable memory file.

### MEM-AC-002

If root `AGENTS.md` or `CLAUDE.md` exists after implementation, inspection confirms it contains at most a pointer to `.context/agent-memory.md` and does not duplicate durable memory entries.

### MEM-AC-003

Inspection of `.context/agent-memory.md` confirms it contains the required headings: `Purpose`, `Durable Decisions`, `Workspace Conventions`, `User Preferences`, `Open Questions`, and `Maintenance Rules`.

### MEM-AC-004

Every entry under `Durable Decisions` has a stable ID matching `MEM-[0-9]{8}-[0-9]{3}`.

### MEM-AC-005

Every durable decision entry includes `Decision`, `Rationale`, `Applies when`, `Source`, and `Status`.

### MEM-AC-006

No durable memory entry is a session progress log, active TODO list, implementation attempt diary, or broad transcript summary.

### MEM-AC-007

The memory file is under 100 lines at initial implementation. If it grows beyond 150 lines later, the maintaining agent must recommend pruning or splitting into on-demand reference files.

### MEM-AC-008

The memory file includes a maintenance rule requiring explicit user approval before agents add, edit, supersede, or delete entries unless the user directly requested memory/context updates.

### MEM-AC-009

Each entry's `Source` field points to durable local context or a concise transcript reference; no entry requires reading a full chat transcript to understand the decision.

### MEM-AC-010

The convention can be verified with read-only inspection and simple shell checks such as file existence, line count, and regex checks; it does not require application tests.

## Verification Plan

Future implementing agents should verify the convention with:

1. Inspect `.context/agent-memory.md` for required headings and fields.
2. Check line count stays below the target threshold.
3. Search root instruction files for duplicated memory entries.
4. Regex-check durable decision IDs.
5. Confirm no ticket files, source code, or broad docs were modified unless explicitly requested.

Example checks:

```bash
test -f .context/agent-memory.md
wc -l .context/agent-memory.md
rg '^### MEM-[0-9]{8}-[0-9]{3}:' .context/agent-memory.md
rg 'Read when:.*\\.context/agent-memory\\.md|agent-memory\\.md' AGENTS.md CLAUDE.md
```

## Risks

- Memory bloat: Agents may add too many observations. Mitigation: enforce admission criteria and line-count thresholds.
- False durability: Agents may encode assumptions as decisions. Mitigation: require sources, statuses, and explicit approval.
- Duplication drift: `AGENTS.md`, `CLAUDE.md`, and `.context/agent-memory.md` may repeat the same content. Mitigation: pointers only in always-loaded files.
- Context rot: Old entries may become misleading. Mitigation: use `needs-review` and `superseded` statuses.

## Implementation Notes

The smallest future implementation would:

1. Create `.context/agent-memory.md` using the structure in this spec.
2. Add zero or a few seed entries only if they describe already-confirmed durable workspace decisions.
3. Optionally create thin root instruction pointers only if the user wants root instruction files introduced.

Do not create tickets for the implementation unless the user separately asks for ticket workflow.
