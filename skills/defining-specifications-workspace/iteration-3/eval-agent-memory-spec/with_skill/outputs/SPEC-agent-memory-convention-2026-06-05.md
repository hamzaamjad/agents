# Specification: Lightweight Agent Memory / Durable-Decision Convention for the `.agents` Workspace

Status: Draft
Date: 2026-06-05
Owner/Requester: Hamza Amjad (workspace owner)
Primary Consumers: AI coding agents, human reviewers
Source Context:
- `skills/session-retrospective/SKILL.md` (Phase 2 priority hierarchy: `AGENTS.md`/`CLAUDE.md` = Priority 1 "first-class memory"; `.context/` = Priority 2; `docs/` = Priority 3; section headers `## User Preferences`, `## Workspace Conventions`, `## Project Facts`; "prefer additions, never delete without approval").
- `skills/engineering-context/SKILL.md` + `references/context-design-patterns.md` (3-tier loading model; Tier 2 session-scoped state must stay ephemeral, not in instruction files; context-rot length discipline) + `references/agents-md-spec.md` (AGENTS.md < 200 lines, critical rules in first 30 lines, "No session-scoped content (progress logs, TODO status)").
- `skills/defining-specifications/SKILL.md` (agent-friendly conventions: stable IDs including `DEC-###`).
- Workspace inspection: `.agents` is a git repo containing only `skills/` and `.gitignore`; no `AGENTS.md`, `CLAUDE.md`, `README.md`, or `.context/` exists today (verified by `ls` and a `**/{AGENTS,CLAUDE,README}.md` glob returning 0 results).
- Cursor runtime fact: past chat transcripts live outside the repo at `~/.cursor/projects/Users-hamzaamjad-agents/agent-transcripts/` as `<uuid>.jsonl` files. These are the "past chats" this convention lets agents avoid re-reading.

## For Implementing Agents

- Authoritative sections: **Requirements**, **Non-Goals**, **Acceptance Criteria**. Build to those.
- **Assumptions** (ASM-###) are unconfirmed inferences, not facts. Do not harden an assumption into behavior without checking it against the live workspace.
- **Open Questions** (Q-###) are blockers, not decisions. Surface them to the human; do not silently guess an answer. Q-001 and Q-004 are decision-critical and gate promotion of this spec from `Draft` to `Ready for Review`.
- This spec defines a **convention** (files + rules + a record template), not a tool. Do not build validation scripts, daemons, or transcript-ingestion automation as part of the core (see Non-Goals).
- Overriding constraint: this convention must not bloat or duplicate the canonical instruction source. It is durable *decision memory*, deliberately separate from always-loaded rules (Tier 0) and from ephemeral session state (Tier 2).

## Summary

Future agents working in `.agents` currently have no durable place to learn *why* the workspace is shaped the way it is. Decisions (naming conventions, where skills live, scope boundaries, tooling choices, things deliberately rejected) are made inside individual chats and then lost, because the transcripts live outside the repo and re-reading them is expensive and unreliable.

This spec defines a **lightweight, durable agent-memory convention**: a single append-only decision log at `.context/decisions.md`, plus a one-line on-demand pointer from the workspace's canonical instruction file. Each entry is a compact, stable-ID decision record (what was decided, why, status). The convention is intentionally narrow — it captures *durable decisions*, not session progress, not always-loaded rules, and not a general documentation system — so it slots cleanly between the existing Tier 0 (instruction sources) and Tier 2 (ephemeral session notes) layers already described by the `engineering-context` and `session-retrospective` skills.

The outcome: a future agent can read one short, scannable file and understand the durable decisions behind this workspace in seconds, without reconstructing context from chat history.

## Problem Statement

- Durable decisions made in chat are not persisted anywhere an agent reliably reads on start. They live only in transcripts at `~/.cursor/projects/Users-hamzaamjad-agents/agent-transcripts/`, which are outside the repo, numerous, and costly to scan.
- There is no canonical instruction file in the repo yet (`AGENTS.md`/`CLAUDE.md` do not exist), so even agents that *want* a starting point have none.
- The two skills that touch "memory" assume targets that are not yet established: `session-retrospective` writes improvements to `AGENTS.md`/`CLAUDE.md`/`.context/`, and `engineering-context` curates `AGENTS.md`. Without an agreed convention, each agent invents its own structure, producing drift, duplication, and `context_rot` — the exact failure modes `engineering-context` exists to prevent.
- Naively dumping decisions into `AGENTS.md` would violate the `agents-md-spec.md` rule "No session-scoped content" and the < 200-line / first-30-lines discipline, degrading task success (per the cited ETH benchmark on poorly curated AGENTS.md files).

The opportunity is a minimal, agreed convention that gives durable decisions a home without polluting the always-loaded instruction layer.

## Goals

- G-001: Give future agents one canonical, low-cost place to learn the workspace's durable decisions and their rationale.
- G-002: Keep the convention lightweight and scannable enough that reading it is always cheaper than reconstructing context from chat transcripts.
- G-003: Integrate cleanly with the existing tier model and the two memory-adjacent skills (`engineering-context`, `session-retrospective`) without duplicating or contradicting them.
- G-004: Preserve decision history (supersede rather than overwrite) so an agent can see not just the current decision but what it replaced and why.

## Non-Goals

- NG-001: This convention does **not** add or modify always-loaded rules. It does not move, restructure, or expand the role of `AGENTS.md`/`CLAUDE.md` beyond adding a single pointer line.
- NG-002: This convention does **not** store session-scoped or ephemeral content — no progress logs, TODO/in-flight task status, "files attempted this session," or per-run scratch notes. That remains Tier 2 (plan files, git history), per `context-design-patterns.md`.
- NG-003: This convention does **not** build automated tooling: no validator script, linter, git hook, or CI check is in scope for the core. (Optional future automation is captured as an open question, not a requirement.)
- NG-004: This convention does **not** auto-ingest, parse, or summarize the chat transcripts under `agent-transcripts/`. Decision capture is a deliberate human/agent authoring act, not a scraping pipeline.
- NG-005: This is **not** a general documentation system, wiki, knowledge base, or heavyweight ADR process. One compact log is the deliverable; do not introduce per-decision files, front-matter schemas, or a `docs/` build.
- NG-006: This spec does **not** itself edit the `session-retrospective` or `engineering-context` skill files. Whether to add thin pointers to them is deferred (Q-004).
- NG-007: The decision log does **not** capture secrets, credentials, tokens, or private data of any kind.

## Users And Stakeholders

- Future AI coding agents (primary): need a single, stable, machine-scannable file with predictable structure and IDs so they can orient before acting.
- Hamza (workspace owner / human reviewer): needs to audit what decisions were recorded and trust that history is preserved, not silently overwritten.
- The `session-retrospective` skill (Phase 2): a natural *writer* of decision records at end-of-session; needs an agreed target and format.
- The `engineering-context` skill: a natural *auditor* of this convention; needs the convention to respect single-source-of-truth and length discipline so it does not flag the result as `bloat`/`redundancy`/`context_rot`.

## Current State

- `.agents/` contains `skills/` and `.gitignore` only. `.gitignore` excludes per-workspace artifacts (`.tickets/`, `.claude/worktrees/`, `.prompts/`) but says nothing about `.context/`.
- No `AGENTS.md`, `CLAUDE.md`, `README.md`, or `.context/` directory exists (verified by inspection).
- `engineering-context` Scope option (D) already prescribes the response when no instruction files exist: "propose an initial `AGENTS.md`." So creating a minimal `AGENTS.md` to host the pointer is consistent with existing guidance.
- `session-retrospective` already treats `.context/` as Priority-2 memory and `AGENTS.md`/`CLAUDE.md` as Priority-1 memory, and requires they "stay identical to each other in content," with a posture of "prefer additions; never delete without approval."
- `context-design-patterns.md` defines the tier model this convention must fit into:
  - Tier 0 — always-loaded core (`AGENTS.md`/`CLAUDE.md`/`.cursorrules`): identity, critical rules, pointers.
  - Tier 1 — on-demand modules loaded via `@path` import or a `Read when:` directive.
  - Tier 2 — session-scoped state (plan files, session notes, git history) that must **not** live in instruction files.
- The durable decision log defined here is **Tier 1**: durable and authoritative, but loaded on demand rather than always.

## Proposed Behavior

A future agent starting work in `.agents`:

1. Reads the canonical instruction file (`AGENTS.md`), which contains a single pointer: a `Read when:` directive sending it to `.context/decisions.md` when it needs the rationale behind durable choices.
2. Opens `.context/decisions.md` and reads a short, newest-first list of decision records, each ~5–10 lines, with a stable `DEC-###` ID, date, status, the decision, and the rationale.
3. Understands the durable decisions of the workspace without opening any chat transcript.

When an agent (or the `session-retrospective` skill) records a new durable decision, it **appends** a new record. When a decision is reversed or replaced, the prior record is marked `Superseded` and linked to its replacement; it is never edited away or deleted. When the active log grows past the length threshold, superseded/obsolete records are moved to an archive file rather than deleted.

## Requirements

- REQ-001: The convention shall designate exactly one canonical location for durable decision records: `.context/decisions.md` at the workspace root.
- REQ-002: Each decision record shall include, at minimum, a stable ID in the form `DEC-###`, an ISO date (`YYYY-MM-DD`), a `Status`, a one-line decision statement, and a rationale. (See "Decision Record Format" under Data/Contract Changes for the exact shape.)
- REQ-003: `DEC-###` IDs shall be unique within the active log and its archive, monotonically assigned, and never reused — even after a record is superseded or archived.
- REQ-004: When a new durable decision is recorded, the agent shall append a new record and shall not edit or delete existing records (append-only).
- REQ-005: When a decision is reversed or replaced, the agent shall set the prior record's `Status` to `Superseded`, add `Superseded-by: DEC-###` to it, and add `Supersedes: DEC-###` to the new record, preserving the original text.
- REQ-006: The decision log shall exclude session-scoped/ephemeral content; if a candidate entry describes in-flight task state, progress, or per-session scratch work, then it shall not be recorded as a decision.
- REQ-007: The workspace canonical instruction file (`AGENTS.md`) shall contain exactly one pointer to `.context/decisions.md` using a `Read when:` trigger, and shall not duplicate any decision content inline.
- REQ-008: Where the active log exceeds the length threshold (NFR-001), records with `Status: Superseded` or `Status: Obsolete` shall be moved to `.context/decisions-archive.md` rather than deleted, preserving their IDs and text.
- REQ-009: The convention shall be documented in a short header block at the top of `.context/decisions.md` (purpose, one record template, the append-only/supersede rule, and the exclusion rule from REQ-006) so the file is self-describing to an agent that opens it cold.
- REQ-010: If `AGENTS.md` and `CLAUDE.md` both exist, then the pointer (REQ-007) shall appear identically in both, consistent with `session-retrospective`'s "must stay identical" rule.

## Nonfunctional Requirements

- NFR-001: Length discipline (anti–context-rot). Each decision record shall be ≤ ~12 lines. The active `.context/decisions.md` shall target ≤ ~200 lines (mirroring the `agents-md-spec.md` AGENTS.md threshold); exceeding it triggers archival per REQ-008.
- NFR-002: Portability. Records shall be plain Markdown with no required front-matter or tooling, readable by any agent and compatible with both Claude Code `@path` imports and the portable `Read when:` directive (per `context-design-patterns.md`).
- NFR-003: Scannability. The active log shall be ordered newest-first so the most recent durable decisions are seen first (recency-bias aware).
- NFR-004: Safety. No record shall contain secrets, credentials, tokens, or private personal data (consistent with `.gitignore`'s secret-exclusion intent).
- NFR-005: Single source of truth. Decision rationale shall live only in the decision log; other files (including `AGENTS.md`) point to it and do not fork its content (per `engineering-context` principle).

## UX, Workflow, Or Interaction Notes

Authoring workflow (for the agent or `session-retrospective` Phase 2):

- Default to **not** recording. Record a decision only when it is durable and would otherwise force a future agent to re-derive it from chats. Test: "Would a future agent make a worse choice without this line?" — mirrors the `engineering-context` "would removing this cause mistakes?" diagnostic.
- To record: append a new record with the next `DEC-###`, today's date, `Status: Accepted`, a one-line decision, and a rationale; optionally `Area`, `Supersedes`, and `Source`.
- To reverse: follow REQ-005 (mark old `Superseded`, cross-link).
- Reading workflow: an agent only reads `.context/decisions.md` when the AGENTS.md `Read when:` trigger fires (e.g., "when you need the rationale behind a durable workspace choice"), keeping it Tier-1 on-demand rather than always-loaded.

## Data, API, Or Contract Changes

### Decision Record Format (the contract)

The downstream agent shall use this record shape (a Markdown subsection per decision). Field set is fixed; ordering is fixed; optional fields may be omitted.

```markdown
### DEC-007: Skills live under top-level `skills/`, one directory per skill
- Date: 2026-06-05
- Status: Accepted        <!-- Accepted | Superseded | Obsolete -->
- Area: workspace-structure   <!-- optional, free-text tag -->
- Decision: Each skill is a self-contained directory under `skills/` with a `SKILL.md` entry point.
- Rationale: Keeps skills independently discoverable and avoids a monolithic instruction file.
- Supersedes: —           <!-- optional: DEC-### -->
- Superseded-by: —        <!-- optional: DEC-### -->
- Source: chat 2026-06-05 / commit abc1234   <!-- optional pointer; not a transcript dump -->
```

### File header block (top of `.context/decisions.md`)

A short self-describing preamble (satisfies REQ-009): one paragraph on purpose, the record template above, and the three rules (append-only; supersede-don't-delete; no session-scoped content). Target ≤ ~25 lines so it does not crowd the records.

### `AGENTS.md` pointer (the only inline change to Tier 0)

A single directive, e.g.:

```markdown
## Durable Decisions
Read when: you need the rationale behind a durable workspace choice (structure, naming, tooling, scope, or a deliberate rejection) → `.context/decisions.md`.
```

## Technical Context

- This convention is a **Tier-1 on-demand module** in the `context-design-patterns.md` model. It is intentionally *not* Tier 0 (always-loaded), because durable decisions are needed situationally, and *not* Tier 2 (ephemeral session state), because they are durable.
- Placement decision boundary — the single sharpest line this spec draws: a **decision** ("we chose X over Y because Z") is durable and belongs in the log; **session state** ("currently editing file F, blocked on B") is ephemeral and is explicitly excluded (REQ-006, NG-002).
- Alternatives considered:
  - *Put decisions directly in `AGENTS.md`*: rejected — violates the < 200-line / "no session-scoped content" discipline and risks `bloat`/`context_rot` that `engineering-context` would flag.
  - *One file per decision (classic ADR)*: rejected as too heavy for a personal skills workspace; conflicts with the "lightweight" goal (NG-005).
  - *Free-form notes in `.context/`*: rejected — no stable IDs or status means agents cannot reliably reference or supersede entries.
- Consistency check: `.context/` is already named as Priority-2 memory by `session-retrospective`, so this reuses an established location rather than inventing one.
- `.gitignore` currently does not mention `.context/`; the decision log is intended to be **committed** (it is shared, durable memory), so no `.gitignore` change is required. (Confirm under Q-005.)

## Implementation Slices

- SLICE-001: Create `.context/decisions.md` with the header block (REQ-009), the record template, and one or two seed records capturing already-true durable decisions (e.g., "skills live under `skills/`", "this is a personal skills library committed to git").
- SLICE-002: Add the single `Read when:` pointer to the workspace canonical instruction file. If no `AGENTS.md` exists, create a minimal `AGENTS.md` (per `engineering-context` scope-D guidance) whose initial content includes the pointer; keep `CLAUDE.md` identical if it is created (REQ-010).
- SLICE-003 (optional, lightweight): Add `.context/decisions-archive.md` only once archival is first needed (REQ-008); do not pre-create an empty archive.

## Testing And Verification

- TEST-001 (verifies REQ-001, REQ-007): File-inspection — `.context/decisions.md` exists, and `AGENTS.md` contains exactly one reference to that path.
- TEST-002 (verifies REQ-002, REQ-009): Inspection — the header block and at least one record contain all required fields (`DEC-###`, `Date`, `Status`, `Decision`, `Rationale`).
- TEST-003 (verifies REQ-003): Scripted/grep check — every `DEC-###` ID across the active log and archive is unique.
- TEST-004 (verifies REQ-005): Inspection — a superseded record has `Status: Superseded` and a `Superseded-by:` link, and its replacement has a matching `Supersedes:` back-link; original text is intact.
- TEST-005 (verifies REQ-006, NG-002): Inspection — no record contains progress/TODO/in-flight-session language (e.g., "currently", "next I will", "in progress").
- TEST-006 (verifies NFR-001): Inspection — active log ≤ ~200 lines and no single record exceeds ~12 lines; if over, superseded records are present in `.context/decisions-archive.md`.
- TEST-007 (verifies NFR-005, REQ-007): Inspection — `AGENTS.md` contains a pointer but no inline copy of any decision's rationale text.
- TEST-008 (verifies NFR-004): Scripted check — no record matches common secret patterns (API keys, tokens, private keys).

## Rollout, Migration, And Operations

- Rollout is a single additive change set (create `.context/decisions.md`, add one pointer line). No migration of existing data is required because no prior memory artifact exists.
- Operationally, the log is maintained by agents during normal work and especially by `session-retrospective` Phase 2 (with the user's approval, per that skill's "ask before creating non-AGENTS files" rule — Q-004 covers whether to wire this in explicitly).
- Rollback is trivial: deleting `.context/` and the single pointer line fully reverts the convention with no side effects.

## Risks And Mitigations

- RISK-001: The log drifts back into session-scoped noise, recreating `context_rot`. / Mitigation: REQ-006, TEST-005, and the "default to not recording" workflow guard against it; `engineering-context` can audit it.
- RISK-002: Decision content gets duplicated into `AGENTS.md`, breaking single-source-of-truth. / Mitigation: REQ-007/NFR-005 + TEST-007 enforce pointer-only.
- RISK-003: Unbounded growth makes the log as expensive to read as the transcripts it replaces. / Mitigation: NFR-001 length cap + REQ-008 archival.
- RISK-004: Overlap/contradiction with `session-retrospective`'s and `engineering-context`'s memory guidance. / Mitigation: this convention reuses their established targets (`.context/`, `AGENTS.md`) and tier model rather than inventing new ones; Q-004 tracks whether to add explicit cross-pointers.
- RISK-005: Two writers (manual agents + session-retrospective) cause ID collisions. / Mitigation: REQ-003 (never reuse) + TEST-003 (uniqueness check); newest-first append makes the next free ID obvious.

## Open Questions

- Q-001 (decision-critical, gates Ready-for-Review): Should the canonical instruction file hosting the pointer be `AGENTS.md`, `CLAUDE.md`, or both kept identical? None exist today; `engineering-context` defaults to `AGENTS.md`, `session-retrospective` writes both and requires they match. Working assumption: `AGENTS.md` (ASM-001).
- Q-002: Single global `.context/decisions.md`, or per-area logs (e.g., one per skill) given the skills-library structure? Working assumption: single global log (ASM-004); revisit only if it exceeds the length cap by area.
- Q-003: Exact thresholds — record max lines (~12) and active-log cap (~200). Are these the right numbers, or should they track AGENTS.md's limits exactly? Working assumption: mirror `agents-md-spec.md` (ASM-005).
- Q-004 (decision-critical, gates Ready-for-Review): Should the `session-retrospective` and `engineering-context` skills be updated to point at this convention (so retrospective writes here and the auditor knows to check it)? This spec marks such edits a Non-Goal (NG-006) pending the owner's call.
- Q-005: Should `.context/` be committed (treated as shared durable memory) or git-ignored like `.tickets/`/`.prompts/`? Working assumption: committed (ASM-006), since the value is cross-session/cross-agent durability.
- Q-006: Who is authorized to record decisions — any agent mid-session, only at retrospective time, or only with explicit user approval? Working assumption: any agent may append, but durable decisions that change workspace policy should be confirmed with the user (ASM-007).

## Assumptions

- ASM-001: `AGENTS.md` is the intended canonical instruction source (per `engineering-context` scope-D default), even though none exists yet. Confidence: medium. Invalidated if the owner prefers `CLAUDE.md`/`.cursorrules` as primary (resolve Q-001).
- ASM-002: `.context/` is the correct home for this memory, since `session-retrospective` already names it Priority-2 memory. Confidence: medium-high. Invalidated if the owner wants memory at repo root or under `docs/`.
- ASM-003: "Durable project decisions" means decisions about conventions, structure, tooling, scope, and deliberate rejections — not transient task state. Confidence: high (directly from the task framing). 
- ASM-004: A single global decision log is sufficient for a personal skills library; per-area logs are unnecessary now. Confidence: medium (resolve Q-002).
- ASM-005: Mirroring `agents-md-spec.md` length limits (~200-line file, critical brevity per record) is the right anti–context-rot target. Confidence: medium-high.
- ASM-006: The decision log should be committed to git as shared durable memory rather than git-ignored. Confidence: medium (resolve Q-005).
- ASM-007: Any agent may append a record, but workspace-policy-changing decisions warrant user confirmation. Confidence: medium (resolve Q-006).
- ASM-008: This run is a non-interactive evaluation, so clarifying questions are recorded here (and in the companion notes file) and the draft proceeds to completion rather than blocking. Confidence: high (from task constraints).

## Acceptance Criteria

- AC-001 (verifies REQ-001, REQ-007): Given the convention is implemented, When an agent inspects the workspace, Then `.context/decisions.md` exists and `AGENTS.md` contains exactly one `Read when:` pointer to it.
- AC-002 (verifies REQ-002, REQ-009): Given `.context/decisions.md`, When inspected, Then it opens with a self-describing header block (purpose + template + rules) and every record contains `DEC-###`, `Date`, `Status`, `Decision`, and `Rationale`.
- AC-003 (verifies REQ-003): Given the active log and any archive, When all `DEC-###` IDs are collected, Then every ID is unique with no reuse.
- AC-004 (verifies REQ-004): Given an existing record, When a new decision is added, Then the prior record's text is unchanged and a new appended record holds the new content (verifiable via git diff: additions only to prior records' region).
- AC-005 (verifies REQ-005): Given a decision is reversed, When the log is inspected, Then the old record shows `Status: Superseded` + `Superseded-by: DEC-###` and the new record shows `Supersedes: DEC-###`, with the old record's original Decision/Rationale text preserved.
- AC-006 (verifies REQ-006, NG-002): Given a candidate entry describing in-flight session state, When recording is attempted, Then it is not written to the log (and no existing record contains progress/TODO/"currently"/"in progress" language).
- AC-007 (verifies REQ-008, NFR-001): Given the active log exceeds ~200 lines, When archival runs, Then superseded/obsolete records appear in `.context/decisions-archive.md` with IDs and text intact and are removed from the active log; and the active log is back under the cap.
- AC-008 (verifies NFR-005, REQ-007): Given `AGENTS.md`, When inspected, Then it contains the pointer but no inline duplication of any record's rationale text.
- AC-009 (verifies NFR-002): Given `.context/decisions.md`, When opened by any agent, Then it is plain Markdown requiring no front-matter or tooling to parse, and the pointer works both as a `Read when:` directive and as a Claude Code `@`-style path reference.
- AC-010 (verifies NFR-004): Given any record, When scanned for secret patterns, Then no API keys, tokens, private keys, or credentials are present.

## Source References

- `skills/session-retrospective/SKILL.md` (Phase 2 priority hierarchy and rules)
- `skills/engineering-context/SKILL.md` (principles, scope-D scaffolding)
- `skills/engineering-context/references/context-design-patterns.md` (3-tier model; context rot; positional optimization)
- `skills/engineering-context/references/agents-md-spec.md` (AGENTS.md structure, length thresholds, "no session-scoped content")
- `skills/defining-specifications/SKILL.md` and `references/{requirements-and-acceptance-criteria,spec-type-profiles}.md` (this spec's structure, EARS/GWT, agent-handoff + feature profiles)
- Workspace inspection: `ls /Users/hamzaamjad/.agents`; glob `**/{AGENTS,CLAUDE,README}.md` → 0 results; `/Users/hamzaamjad/.agents/.gitignore`
- Runtime fact: chat transcripts at `~/.cursor/projects/Users-hamzaamjad-agents/agent-transcripts/<uuid>.jsonl`
- Companion notes: `SPEC-agent-memory-convention-2026-06-05.notes.md` (context-review log, full clarifying-question set, outline)
