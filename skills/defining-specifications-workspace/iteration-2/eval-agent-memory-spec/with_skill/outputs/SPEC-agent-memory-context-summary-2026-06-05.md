# Specification: Lightweight Agent Memory Context Summary

Status: Draft
Date: 2026-06-05
Owner/Requester: Hamza Amjad
Primary Consumers: AI coding agents, human reviewers
Source Context:
- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/context-design-patterns.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/agents-md-spec.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/priority-resolution.md`
- `/Users/hamzaamjad/.agents/skills/session-retrospective/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/outcome-schema.md`

## Summary

Add a lightweight, durable agent-memory convention to the `.agents` workspace so future coding agents can quickly recover stable project decisions without reading every past chat or transcript.

The convention should introduce a small, sourced, advisory memory index at `.context/agent-memory.md`, with optional topic files only when a decision needs more detail than the index should carry. It must preserve the workspace's existing bias toward small instruction surfaces, pointer-first context, explicit precedence, and evidence-linked workspace improvements.

This specification defines the intended behavior and acceptance criteria only. It does not create the memory files, tickets, hooks, implementation code, or broad documentation rewrites.

## Problem Statement

Durable workspace decisions currently live across skills, references, ticket outcomes, and chat history. Future agents can inspect those sources, but doing so repeatedly is expensive and easy to skip. A memory convention is needed to capture only high-signal, long-lived project context while avoiding the common failure mode where "memory" becomes an oversized progress log or a second instruction file.

The workspace already has patterns that constrain the design:

- Context engineering guidance treats bloated instruction files as harmful and recommends dynamic loading tiers.
- Session retrospective guidance allows workspace context improvements, but only when justified by session evidence.
- Ticket workflow guidance uses compact `## Outcome` blocks as retrieval surfaces for archived work.
- No root `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`, or `.context/` directory was found during this read-only evaluation pass.

## Goals

- G-001: Give future agents a fast, durable first stop for project decisions that would otherwise require transcript mining.
- G-002: Keep always-loaded instruction context small by storing memory as on-demand context, not as a large root instruction block.
- G-003: Make every memory entry evidence-linked, scoped, and easy to verify or retire.
- G-004: Define clear promotion criteria so temporary session details do not become durable memory.
- G-005: Preserve existing authority boundaries between system/user instructions, source files, active tickets, archived tickets, specs, and advisory memory.

## Non-Goals

- NG-001: Do not create the `.context/agent-memory.md` file as part of this specification task.
- NG-002: Do not create tickets, implementation code, hooks, embeddings, databases, or external memory services.
- NG-003: Do not store raw chat transcripts, chain-of-thought, private credentials, secrets, or complete session summaries.
- NG-004: Do not turn memory into a replacement for `AGENTS.md`, source code, active tickets, specs, or archived ticket outcomes.
- NG-005: Do not perform a broad documentation rewrite or canonical instruction-file cleanup as part of the memory convention itself.

## Users And Stakeholders

- Future coding agents: Need a compact map of durable project decisions and where to inspect deeper sources.
- Human maintainer: Needs memory entries to be auditable, small, and easy to prune when stale.
- Skill authors and evaluators: Need a convention that helps later changes respect existing workspace decisions without inflating skills or specs.

## Current State

The workspace contains several agent-facing skills but no current root-level canonical instruction file or context directory:

- `defining-specifications` defines how to produce focused specs with source context, assumptions, open questions, verification, and write boundaries.
- `engineering-context` defines instruction hygiene principles: hierarchy first, single source of truth, grounding before generation, and minimal context that earns its place.
- `engineering-context/references/context-design-patterns.md` defines dynamic loading tiers and warns against cumulative context degradation.
- `session-retrospective` recommends optional workspace improvements to `AGENTS.md`, `CLAUDE.md`, `.context/`, or docs after a session, but only after user approval and session-specific justification.
- `ticket-workflow` uses archived ticket `## Outcome` blocks as compact retrieval surfaces for prior work.

There is no discovered `.context/` directory, so the proposed convention should be introduced as a new future artifact rather than modifying an existing memory surface.

## Proposed Behavior

When implemented, the workspace should use `.context/agent-memory.md` as the canonical durable memory index for agents. The file should be intentionally small, sourced, and advisory. It should tell agents what durable decisions exist and where to inspect deeper context, not summarize every historical detail.

Root instruction files, if introduced later, should contain at most a short pointer to `.context/agent-memory.md` with a trigger such as: "Read when starting unfamiliar work, updating workspace conventions, or making changes that may conflict with prior durable decisions." They should not duplicate the memory contents.

Agents should update memory only at consolidation moments:

- After a session retrospective when the user approves workspace improvements.
- After a meaningful workspace convention, skill, or spec decision has landed.
- After ticket archive outcomes reveal durable constraints or invariants worth preserving.
- During an explicit context cleanup or instruction hygiene pass.

Agents should not update memory during routine implementation work unless explicitly asked to consolidate context.

## Requirements

- REQ-001: The convention must define `.context/agent-memory.md` as the single canonical memory index for durable workspace context.
- REQ-002: The memory index must include a purpose statement that says it is advisory context for future agents, not an authoritative instruction source.
- REQ-003: Each durable memory entry must include a stable ID, title, date added or updated, scope, source pointer, decision or invariant, rationale, and "applies when" trigger.
- REQ-004: Each memory entry must be traceable to at least one source file, ticket outcome, spec, or user-approved retrospective recommendation.
- REQ-005: The convention must define promotion criteria for what belongs in memory.
- REQ-006: The convention must define exclusion criteria for session-scoped details, progress logs, raw transcript excerpts, secrets, and stale implementation notes.
- REQ-007: The convention must define precedence rules for resolving conflicts between memory and higher-authority sources.
- REQ-008: The convention must define a pruning or retirement workflow for stale, superseded, or unverifiable entries.
- REQ-009: Optional topic files under `.context/memory/` must be pointer targets, not a default dumping ground.
- REQ-010: Root instruction files must only point to memory; they must not inline or duplicate memory entries.

## Nonfunctional Requirements

- NFR-001: The memory index should target 100-150 lines and must stay under 200 lines before being pruned or split.
- NFR-002: Individual memory entries should be concise: ideally 5 bullets or fewer, excluding metadata.
- NFR-003: The convention must minimize always-loaded context and support on-demand loading.
- NFR-004: The memory file must be readable as plain Markdown without tooling.
- NFR-005: The convention must be safe for private workspaces: no secrets, credentials, raw private chat dumps, or unredacted sensitive data.
- NFR-006: The convention must be maintenance-light and manually editable; no persistent background service or generated database is required.

## UX, Workflow, Or Interaction Notes

For agents, the intended workflow is:

1. Read current task instructions and applicable workspace instructions first.
2. Read `.context/agent-memory.md` when the task is unfamiliar, touches workspace conventions, changes a durable process, or asks for historical context.
3. Follow only entries whose "applies when" trigger matches the task.
4. If a memory entry conflicts with explicit user instructions, source files, active tickets, or a current spec, follow the higher-authority source and record the conflict for cleanup.
5. At a consolidation point, propose memory updates only for durable decisions that meet promotion criteria.

For humans, memory updates should be easy to review in diffs. A reviewer should be able to answer: "Would removing this entry cause future agents to make worse decisions?"

## Data, API, Or Contract Changes

No runtime data, API, or code contracts are required.

The proposed Markdown contract for `.context/agent-memory.md` is:

```markdown
# Agent Memory

Purpose: Durable workspace context for future coding agents. Keep this file small, sourced, and decision-oriented. It is advisory and never overrides explicit user instructions, source code, active tickets, or current specifications.

Read when:
- Starting unfamiliar work in this workspace.
- Updating skills, specs, tickets, or instruction files.
- Resolving a question that may have a prior durable decision.

## Authority And Conflict Resolution

Memory is lower authority than system/runtime instructions, explicit user instructions, source files, active tickets, current specs, and canonical instruction files. If memory conflicts with those sources, follow the higher-authority source and mark the memory entry for review.

## Durable Decisions

### MEM-YYYYMMDD-01: <Short Decision Title>
- Scope: <workspace area, skill, convention, or subsystem>
- Source: <path, ticket outcome, spec, or retrospective recommendation>
- Decision: <durable decision or invariant>
- Rationale: <why this matters for future agents>
- Applies when: <trigger for reading/applying this entry>
- Status: active | superseded | needs-review

## Retrieval Pointers

- <Topic>: Read <path> when <trigger>.

## Open Memory Questions

- <Question>: <why it matters and who/what can resolve it>
```

Optional topic files may live under `.context/memory/<topic>.md` only when:

- A single theme has enough durable detail that it would push the index over the size target.
- The topic file has a clear "Read when" trigger.
- The index keeps a one-line pointer to the topic file.
- The topic file follows the same source, status, and conflict-resolution rules.

## Technical Context

The convention should align with existing workspace principles:

- Context should be tiered: root instructions stay small; memory is loaded on demand.
- Shared conventions should have one canonical home and other files should point to that home.
- Memory entries should be grounded in evidence, not freeform synthesis.
- Historical detail belongs in archived tickets, specs, transcripts, or topic files; the index should preserve only decision-level summaries and pointers.
- Archived ticket `## Outcome` blocks remain the retrieval surface for completed ticket work. Memory may point to important outcomes but should not duplicate the full outcome block.

Recommended precedence from highest to lowest for this workspace:

1. System/runtime instructions.
2. Explicit current user instructions.
3. Directory-local and project-root instruction files, if present.
4. Source files, active tickets, and current specifications.
5. Skill instructions applicable to the current task.
6. `.context/agent-memory.md`.
7. Archived tickets, transcripts, historical notes, and previous evaluation artifacts.

## Implementation Slices

- SLICE-001: Create `.context/agent-memory.md` from the proposed Markdown contract, including purpose, read triggers, authority rules, and empty sections.
- SLICE-002: Add only a short pointer to memory from any future root instruction file, if such a file is introduced or updated.
- SLICE-003: During a later context cleanup pass, review existing skills and archived outcomes for a small initial set of memory entries, each with source pointers.
- SLICE-004: Add pruning guidance to the memory file if it approaches the 200-line ceiling.

These slices are implementation guidance only. This evaluation task must not create tickets or implement them.

## Testing And Verification

- TEST-001: File inspection confirms `.context/agent-memory.md` exists only after implementation, not during this specification task.
- TEST-002: File inspection confirms the memory index contains purpose, read triggers, authority rules, durable decisions, retrieval pointers, and open memory questions.
- TEST-003: Grep or manual review confirms every `MEM-*` entry includes a `Source:` pointer.
- TEST-004: Manual review confirms no raw transcript excerpts, secrets, chain-of-thought, or progress logs are present.
- TEST-005: Manual review confirms root instruction files, if present, contain only a pointer to memory and do not duplicate entries.
- TEST-006: Line-count check confirms `.context/agent-memory.md` remains under 200 lines.
- TEST-007: Conflict review confirms memory is treated as advisory and lower authority than current user instructions, source files, active tickets, current specs, and canonical instruction files.

## Rollout, Migration, And Operations

The first implementation should create only the memory index skeleton. It should not mine all historical chats.

Initial population should happen through explicit consolidation passes:

- Use session retrospectives to identify candidate workspace improvements.
- Use archived ticket `## Outcome` blocks to identify durable constraints.
- Use specs to capture confirmed decisions that future implementation agents need.
- Prefer adding one or two high-confidence entries at a time over bulk-importing history.

Maintenance should happen opportunistically during context cleanup, retrospective workspace improvements, or when an agent detects a conflict between memory and current sources. Stale entries should be marked `superseded` or `needs-review` before deletion unless the user explicitly approves removal.

## Risks And Mitigations

- RISK-001: Memory becomes another bloated instruction file. / Mitigation: Keep it on-demand, cap it at 200 lines, require source pointers, and prune entries that do not pass the "would removing this cause mistakes?" test.
- RISK-002: Memory conflicts with current source, tickets, specs, or user instructions. / Mitigation: State explicit lower-authority precedence and mark conflicts for review.
- RISK-003: Agents add transient session notes. / Mitigation: Require promotion and exclusion criteria, and limit updates to consolidation moments.
- RISK-004: Agents duplicate archived ticket outcomes or specs. / Mitigation: Store decision-level summaries and pointers, not full historical artifacts.
- RISK-005: Sensitive information is accidentally preserved. / Mitigation: Exclude secrets, credentials, raw transcripts, private data dumps, and chain-of-thought by rule.

## Open Questions

- Q-001: Should `.context/agent-memory.md` be introduced before or after a root `AGENTS.md` exists? This affects whether the first pointer lives only in memory or also in an always-loaded instruction file.
- Q-002: Should memory entries use `MEM-YYYYMMDD-##` IDs or a shorter sequential ID? Date-based IDs are easier to audit without a registry, but sequential IDs are cleaner for references.
- Q-003: Who is allowed to delete stale memory entries without explicit approval? The safest default is to mark entries `superseded` or `needs-review` unless the user asks for cleanup.
- Q-004: Should session retrospectives recommend memory updates directly, or should they continue to recommend generic workspace improvements that may include memory as one target?

## Assumptions

- ASM-001: The workspace intentionally has no current `.context/` directory; creating it later is acceptable if the implementation task explicitly asks for the convention. Confidence: medium. Invalidated if a hidden or branch-specific context directory exists outside the inspected workspace.
- ASM-002: Memory should be advisory and lower authority than instructions, source, tickets, and current specs. Confidence: high. Invalidated only by an explicit owner decision to make memory a canonical instruction source.
- ASM-003: The initial memory convention should be manual and Markdown-based, not tool-backed. Confidence: high. Invalidated if the maintainer asks for automated retrieval, embeddings, hooks, or external storage.
- ASM-004: Prior evaluation outputs are historical artifacts, not authoritative workspace decisions. Confidence: high. Invalidated if the maintainer promotes one of those outputs into canonical docs or memory.

## Acceptance Criteria

- AC-001: A downstream agent can implement the memory convention without reading past chats.
- AC-002: The spec clearly names `.context/agent-memory.md` as the canonical memory index and defines optional topic files only as overflow/pointer targets.
- AC-003: The spec separates goals, non-goals, requirements, assumptions, risks, open questions, verification steps, and acceptance criteria.
- AC-004: The proposed convention includes promotion criteria, exclusion criteria, source pointers, conflict precedence, and pruning behavior.
- AC-005: The convention preserves small always-loaded instruction files by using pointer-first on-demand loading.
- AC-006: No tickets, implementation code, root docs, or actual memory files are created by this evaluation task.

## Source References

- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/context-design-patterns.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/agents-md-spec.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/priority-resolution.md`
- `/Users/hamzaamjad/.agents/skills/session-retrospective/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/outcome-schema.md`
