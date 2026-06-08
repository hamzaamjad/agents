# Specification: Lightweight Agent Memory / Context Summary Convention

- **Status:** Draft (ready for review)
- **Date:** 2026-06-05
- **Workspace:** `/Users/hamzaamjad/.agents`
- **Primary consumers:** AI coding agents working in this workspace (secondary: the human maintainer)
- **Author:** Baseline drafting pass (no specialized skill used)

---

## 1. Summary

Add a single, lightweight, durable **agent memory** file to the `.agents` workspace so future
coding agents can recover stable project decisions in one read instead of mining past chat
transcripts. The convention is one canonical Markdown file, `.context/agent-memory.md`, holding a
short, dated, append-mostly log of **durable decisions and their rationale**, plus a small set of
rules for when to read it, when to append to it, and how to keep it small.

This spec defines the convention only. It does **not** create the file, write automation, modify
existing skills, or rewrite documentation.

---

## 2. Problem & Motivation

The `.agents` workspace is a shared, version-controlled collection of agent skills
(`engineering-context`, `session-retrospective`, `ticket-workflow`, `defining-specifications`,
`engineering-prompts`, `hamza-voice`). It currently has **no** root `AGENTS.md`, `CLAUDE.md`,
`README.md`, or `.context/` directory.

As a result, the *rationale* behind durable decisions — why `.tickets/`, `.prompts/`, and
`.claude/worktrees/` are gitignored as per-workspace artifacts; why skills follow a specific
`SKILL.md` + `references/` layout; naming conventions like dated `SPEC-*.md` files; precedence
rules between skills — lives only in:

- the skill files themselves (scattered, must be inferred), and
- past chat transcripts (`agent-transcripts/*.jsonl`), which are expensive and unreliable to scan.

Future agents either re-derive these decisions (risking inconsistency) or skip the context
entirely. There is a gap between two well-defined tiers already described by the existing
`engineering-context` skill:

- **Tier 0** — canonical *rules* the agent must follow (`AGENTS.md` / `CLAUDE.md`). Kept lean.
- **Tier 2** — *session-scoped* state (plan files, git history) that should **not** persist in
  instruction files.

Durable **decisions with rationale** ("what we decided and why") fit neither tier cleanly. They
are not session-scoped, but they are also not the terse, must-follow directives that belong in a
lean `AGENTS.md`. This spec defines the missing middle tier as a small, dedicated memory file.

---

## 3. Goals & Non-Goals

### Goals

- **G1** — Give future agents a single fast first stop for durable project decisions, removing the
  need to read every past chat.
- **G2** — Define a format compact and structured enough to scan in seconds and append to safely.
- **G3** — Define clear *promotion criteria* so only durable, high-signal decisions are recorded
  (and ephemeral session detail is kept out).
- **G4** — Fit the workspace's existing conventions: lean instruction surfaces, single source of
  truth, pointer-first context, and evidence-linked changes.
- **G5** — Be verifiable by simple file inspection (path, structure, size).

### Non-Goals

- **NG1** — Do **not** create `.context/agent-memory.md` or seed it with entries as part of this spec.
- **NG2** — Do **not** build automation (hooks, scripts, CI, embeddings, search index, database).
- **NG3** — Do **not** auto-summarize or ingest chat transcripts.
- **NG4** — Do **not** rewrite or restructure existing skills or documentation.
- **NG5** — Do **not** create a second instruction file that competes with a future `AGENTS.md`.
  Memory holds *decisions + rationale*, not must-follow rules.

---

## 4. Current State (read-only findings)

| Observation | Source | Implication for this spec |
|---|---|---|
| No root `AGENTS.md`/`CLAUDE.md`/`README.md`/`.context/` exists | `ls` of workspace root | Memory file is a net-new artifact; no migration needed. |
| `.tickets/`, `.prompts/`, `.claude/worktrees/` are gitignored "per-workspace, not shared" | `.gitignore` | Ephemeral agent artifacts are deliberately *not* shared; memory must be the opposite — shared. |
| `.context/agent-memory.md` is **not** gitignored (would be tracked) | `git check-ignore` returns "not ignored" | Memory will be committed and shared across clones/sessions, matching G1. |
| `session-retrospective` Phase 2 already lists `.context/` as a workspace-improvement target and treats `AGENTS.md`/`CLAUDE.md` as "first-class memory" | `skills/session-retrospective/SKILL.md` | `.context/` is the natural, already-anticipated home; this spec formalizes one file there. |
| `engineering-context` defines a Tier 0/1/2 model and warns that poorly curated instruction files *reduce* task success and raise cost | `skills/engineering-context/references/{context-design-patterns,agents-md-spec}.md` | Memory must stay small and high-signal; bias toward deletion/consolidation. |

---

## 5. Proposed Convention

### 5.1 Canonical location

- **One file:** `.context/agent-memory.md` at the workspace root.
- It is **committed** (shared across sessions and clones), unlike the gitignored ephemeral
  artifacts.
- It is the single source of truth for durable decisions. If a future `AGENTS.md` is added, it
  should carry only a short **pointer** to this file, never a duplicate of its contents.

### 5.2 File structure

The file has a fixed, minimal shape:

1. A **header** stating purpose, authority, and read/append triggers (so the file is
   self-explanatory to an agent that opens it cold).
2. A **`## Decisions`** section: a reverse-chronological list of dated entries.

Proposed contract:

```markdown
# Agent Memory

Durable decisions for agents working in this workspace. Read this before starting unfamiliar
work or changing a workspace convention. Append a new entry when a durable decision is made.

Authority: advisory context, not a rule file. It never overrides explicit user instructions,
the current task spec, source code, or a future AGENTS.md. Keep it small and high-signal —
prefer superseding old entries over accumulating noise.

## Decisions

### AM-0002 — <short decision title>
- Date: 2026-06-05
- Scope: <area, e.g. ticket-workflow / repo-wide / skill authoring>
- Decision: <the durable choice in 1-2 sentences>
- Rationale: <why; the tradeoff or constraint that drove it>
- Source: <pointer: file path, ticket ID, or chat title — where to verify deeper>
- Status: active            # active | superseded by AM-XXXX

### AM-0001 — <older decision title>
- ...
```

### 5.3 Entry schema (per decision)

| Field | Required | Purpose |
|---|---|---|
| ID (`AM-NNNN`) | Yes | Stable handle for cross-reference and supersession. Monotonic, zero-padded. |
| Title | Yes | One-line scannable summary. |
| Date | Yes | When the decision was recorded (ISO `YYYY-MM-DD`). |
| Scope | Yes | What the decision applies to, so agents can skip irrelevant entries. |
| Decision | Yes | The durable choice, stated as a fact (1–2 sentences). |
| Rationale | Yes | The "why" — the constraint/tradeoff future agents must respect. |
| Source | Yes | Pointer to deeper context (file path, ticket, or chat title). May be "none". |
| Status | Yes | `active` or `superseded by AM-XXXX`. |

### 5.4 Promotion criteria — what belongs (and what does not)

Record an entry only if **all** of these hold:

- **Durable** — expected to remain true across multiple future sessions.
- **Decision or invariant** — a choice made or a constraint to respect, not a task status.
- **Non-obvious** — not already enforced by tooling, the gitignore, or plainly visible in code.
- **Cross-session value** — a future agent would otherwise re-derive it or get it wrong.

Keep **out** (these are Tier 2 / ephemeral, per `context-design-patterns.md`):

- Progress logs, TODOs, "files attempted this session", current blockers.
- Restatements of rules that belong in a lean `AGENTS.md`.
- Summaries of routine chats with no durable decision.
- Anything already enforced by linters, formatters, or the gitignore.

### 5.5 Lifecycle

- **Read trigger:** an agent reads `.context/agent-memory.md` near the start of work when the task
  is unfamiliar, touches a workspace convention, or asks for historical/"why" context.
- **Append trigger:** an agent (or the human) adds an entry when a decision meeting §5.4 is made —
  e.g., at the end of a task, or during `session-retrospective` Phase 2.
- **Supersede, don't delete:** when a decision changes, add a new entry and set the old entry's
  Status to `superseded by AM-XXXX`. Delete an entry only if it was recorded in error.
- **Consolidate when large:** if the file exceeds the size budget (§5.6), prune superseded/stale
  entries or merge related ones. This consolidation is the only sanctioned destructive edit.

### 5.6 Size & quality budget

- Soft cap: **~150 lines** (aligns with the Tier 0 "always-loadable" budget in
  `context-design-patterns.md`). Crossing it triggers consolidation, not a second file.
- Every entry must independently pass the diagnostic: *"Would removing this cause a future agent to
  make a mistake?"* If no, it does not belong.

### 5.7 Relationship to existing skills (advisory, not changed by this spec)

- **`session-retrospective`** — Phase 2 already writes durable insights to `.context/`. Its
  natural integration point is to append qualifying entries here. (No edit made in this spec.)
- **`engineering-context`** — treats this file as a context source to audit for bloat/staleness,
  applying its lean-instruction principles. It must not duplicate `AGENTS.md` rules here.
- **`ticket-workflow`** — when an archived ticket surfaces a durable constraint, that constraint
  may be promoted into a memory entry (with the ticket ID as Source).

---

## 6. Acceptance Criteria

A future implementation of this convention is correct when:

- **AC1** — `.context/agent-memory.md` exists at the workspace root and is tracked by git (not
  gitignored).
- **AC2** — The file contains the header (purpose + authority + read/append triggers) and a single
  `## Decisions` section.
- **AC3** — Every decision entry includes all required schema fields from §5.3, in the defined order.
- **AC4** — Entry IDs are unique, zero-padded, and monotonic; entries are reverse-chronological.
- **AC5** — No entry contains session-scoped content as defined in §5.4 (no progress logs, TODOs,
  or blockers).
- **AC6** — File length is at or under the ~150-line soft cap, or a consolidation note explains the
  overage.
- **AC7** — If a root `AGENTS.md`/`CLAUDE.md` exists, it contains a short pointer to this file and
  does **not** duplicate its contents.
- **AC8** — These criteria are checkable by file inspection or a trivial script (no runtime
  behavior to test).

---

## 7. Out of Scope

- Creating or seeding the memory file (this spec defines the convention only).
- Editing any existing skill, including `session-retrospective` or `engineering-context`.
- Automation: hooks, CI checks, validators, embeddings/semantic search, databases.
- Transcript ingestion or auto-summarization.
- A root `AGENTS.md`/`CLAUDE.md` (referenced as a future pointer host, but not in scope here).

---

## 8. Open Questions & Working Assumptions

Because this pass is non-interactive, the following questions are recorded with the assumption
taken to allow a complete draft. See the companion notes file for the fuller log.

| # | Open question | Assumption taken |
|---|---|---|
| Q1 | Single file vs. a `.context/memory/` directory of topic files? | **Single file.** Start minimal; add topic files only if the cap is repeatedly exceeded (deferred, not in this spec). |
| Q2 | Should memory be committed/shared or per-workspace gitignored? | **Committed/shared.** `.context/` is not gitignored and the goal is cross-session/clone sharing. |
| Q3 | Should this spec also introduce a root `AGENTS.md` to host the pointer? | **No.** Keep scope focused; AGENTS.md is a separate, future decision. The pointer rule (AC7) applies *if/when* one exists. |
| Q4 | Who owns appends — agents autonomously, or only on human approval? | **Agents may append** under §5.4 criteria; destructive consolidation follows the existing skills' "archive/confirm before deleting" posture. |
| Q5 | Exact filename: `agent-memory.md` vs `MEMORY.md` vs `decisions.md`? | **`.context/agent-memory.md`** — descriptive, matches the `.context/` tier already named by `session-retrospective`. |
| Q6 | Do entries need machine-readable frontmatter (YAML) for future tooling? | **No (plain Markdown).** Keeps it lightweight; revisit only if validation tooling is later requested. |
