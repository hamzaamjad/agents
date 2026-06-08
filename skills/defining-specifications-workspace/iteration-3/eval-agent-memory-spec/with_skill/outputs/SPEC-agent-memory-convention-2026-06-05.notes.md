# Companion Notes — Agent Memory / Durable-Decision Convention

Companion to `SPEC-agent-memory-convention-2026-06-05.md`. This file holds the context-review log, the clarifying questions I would have asked a human, my working assumptions, and the pre-write outline. It exists because the run is **non-interactive** (per the `defining-specifications` skill: when live clarification is not allowed, record the questions and assumptions and proceed to a complete draft).

## How I worked the skill

- Spec type: **agent handoff / process-skill spec** (primary consumer is an AI agent) composed with the **feature / new capability** profile (it adds a convention). Applied both profile deltas: led with `Source Context` + `For Implementing Agents`, made Open Questions explicit blockers, kept implementation slices lightweight, and made non-goals concrete.
- Followed the default template, EARS for requirements, Given/When/Then for acceptance criteria, and stable IDs (`REQ/NFR/AC/TEST/RISK/Q/ASM/SLICE/G/NG`).

## Context-review log (read-only)

Evidence gathered and how it shaped the spec:

- `ls /Users/hamzaamjad/.agents` → only `skills/`, `.gitignore`, `.DS_Store`, `.git`. Glob `**/{AGENTS,CLAUDE,README}.md` → **0 results**. ⇒ No canonical instruction file exists; spec must account for creating a minimal `AGENTS.md` to host the pointer.
- `.gitignore` ignores `.tickets/`, `.claude/worktrees/`, `.prompts/` but **not** `.context/`. ⇒ Raised Q-005 (commit vs ignore the log); assumed committed.
- `skills/session-retrospective/SKILL.md` → Phase 2 priority hierarchy names `AGENTS.md`/`CLAUDE.md` (Priority 1, "first-class memory"), `.context/` (Priority 2), `docs/` (Priority 3); rules: "prefer additions," "never delete without approval," "AGENTS.md and CLAUDE.md must stay identical," "ask before creating non-AGENTS files." ⇒ Reused `.context/` as the home; mirrored append-only / supersede; REQ-010 (identical pointer); Q-004 (wire retrospective to write here).
- `skills/engineering-context/SKILL.md` → single-source-of-truth, "would removing this cause mistakes?", scope-D = "propose initial AGENTS.md when none exist." ⇒ NFR-005 pointer-only; SLICE-002 minimal AGENTS.md; the "default to not recording" workflow.
- `references/context-design-patterns.md` → 3-tier model; **Tier 2 session-scoped content must NOT live in instruction files**; context-rot length lever; recency/primacy. ⇒ Positioned the log as Tier 1; REQ-006/NG-002 exclude session state; NFR-001 length cap; NFR-003 newest-first.
- `references/agents-md-spec.md` → AGENTS.md < 200 lines, critical rules in first 30, "No session-scoped content (progress logs, TODO status)." ⇒ Justified NOT putting decisions in AGENTS.md; mirrored thresholds (NFR-001).
- Runtime fact (system prompt): transcripts live at `~/.cursor/projects/Users-hamzaamjad-agents/agent-transcripts/<uuid>.jsonl`. ⇒ This is the costly "past chats" source the convention replaces.

## Clarifying questions I would have asked (and how I proceeded)

These mirror the spec's `Open Questions`; the decision-critical ones gate promotion to `Ready for Review`.

1. (Q-001, blocker) Canonical instruction file for the pointer — `AGENTS.md`, `CLAUDE.md`, or both identical? → Assumed `AGENTS.md` (engineering-context default).
2. (Q-002) Single global log vs. per-skill/per-area logs? → Assumed single global log; revisit at length cap.
3. (Q-003) Exact thresholds (~12 lines/record, ~200-line file)? → Assumed mirror `agents-md-spec.md`.
4. (Q-004, blocker) Update `session-retrospective`/`engineering-context` to point at this convention? → Marked Non-Goal (NG-006) for this spec; deferred to owner.
5. (Q-005) Commit `.context/` or git-ignore it? → Assumed committed (shared durable memory).
6. (Q-006) Who may record decisions, and when? → Assumed any agent may append; policy-changing decisions need user confirmation.

## Pre-write outline (shared here instead of blocking, per skill step 4)

- Title: Lightweight Agent Memory / Durable-Decision Convention for `.agents`.
- Output path: the assigned `.../iteration-3/eval-agent-memory-spec/with_skill/outputs/` directory; filename per skill convention `SPEC-agent-memory-convention-2026-06-05.md`.
- Major sections: Summary, Problem, Goals/Non-Goals, Users, Current State, Proposed Behavior, Requirements (EARS), NFRs, UX/Workflow, Data/Contract (record format + AGENTS.md pointer), Technical Context (tier placement + alternatives), Implementation Slices, Testing, Rollout, Risks, Open Questions, Assumptions, Acceptance Criteria, Source References.
- Scope boundaries: durable decisions only (Tier 1); not Tier 0 rules, not Tier 2 session state, not tooling, not transcript ingestion, not a docs system.
- Core design: `.context/decisions.md` append-only decision log with `DEC-###` records + one `Read when:` pointer in `AGENTS.md`; supersede-don't-delete; archive past length cap.

## Status rationale

Kept `Status: Draft`. Two decision-critical questions (Q-001 canonical file; Q-004 skill integration) genuinely affect scope and were resolved only by working assumption, not confirmation. Per the skill, the spec stays `Draft` until those are resolved or explicitly accepted by the owner; everything else is checklist-complete and ready for review on resolution.
