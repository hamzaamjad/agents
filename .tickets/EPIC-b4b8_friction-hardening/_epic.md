---
id: EPIC-b4b8
title: "Fold the v1.3 dogfood friction log back into the toolchain"
type: epic
status: to-do
priority: high
branch: epic/b4b8/friction-hardening
created: 2026-06-10
updated: 2026-06-10
tags: [friction-log, dogfood, skill-maintenance]
complexity:
---

# Fold the v1.3 dogfood friction log back into the toolchain

## Context

Shipping defining-specifications v1.3 through the workspace's own pipeline (EPIC-e164,
archived) produced a 19-entry friction log: `.prompts/exercises/02-friction-log.md`.
The ticket-workflow benchmark (`evals/ticket-workflow/iteration-1/benchmark.md`) and the
instruction-layer audit (`docs/audits/2026-06-10-instruction-layer-audit.md`, Next pass #5)
added three more fold-backs. This epic converts every open candidate fix into shipped edits.

Already resolved, do not re-fix: FRIC-002 (v1.3 REQ-003), FRIC-007 (DEC-003 memo),
FRIC-006 (AGENTS.md `docs/specs/` layout line, commit 0b36496).

Out of scope: eval iteration-2 redesign (benchmark "next-iteration changes"), the
codex-skills consolidation memo, relocating `skills/defining-specifications-workspace/`.

## Sub-tickets

| ID       | Title                                                       | Status |
|----------|-------------------------------------------------------------|--------|
| FEAT-001 | ticket-workflow SKILL.md: closure and integration fixes     | to-do  |
| FEAT-002 | ticket-workflow SKILL.md: creation and execution guidance   | to-do  |
| FEAT-003 | ticket-workflow references: drift and portability cleanup   | to-do  |
| FEAT-004 | validate_context.py: tone false-positives, worktree skip, skill-reference scan | to-do  |
| FEAT-005 | Cross-skill one-line clarifications (defspec, retro, eval contract) | to-do  |
| CHORE-001| Epic closure: mark done, archive, cleanup                   | to-do  |

## Merge order

1. FEAT-001 (SKILL.md edits; serialized first — FEAT-002 edits the same file)
2. FEAT-002 (depends on FEAT-001 landing to avoid same-file merge conflicts)
3. FEAT-003 (references/ only — may run in a parallel worktree with FEAT-001/002)
4. FEAT-004 (validator script only — parallel-capable)
5. FEAT-005 (three small files in other skills + AGENTS.md — parallel-capable)
6. CHORE-001 — Epic closure (always last: archives epic, deletes orchestration prompt)

## Acceptance criteria

- [ ] All sub-tickets are `done`
- [ ] `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high, 0 medium, 0 low on the epic branch (FEAT-004 removes the documented false-positive class)
- [ ] Epic archived and orchestration prompt deleted (by closure ticket)
- [ ] Integrated to main per repo policy: local `git merge --no-ff` from the primary clone (no pushable-remote PR required)
- [ ] Every open friction entry (FRIC-001, 003, 004, 005, 008..019) maps to a shipped edit or a recorded descope rationale in a ticket Outcome block

## Notes

Created 2026-06-10 in worktree `.claude/worktrees/epic-b4b8`; the creation worktree is
removed after ticket files merge to main, and the branch `epic/b4b8/friction-hardening`
stays alive as the integration target. Re-add a worktree at orchestration start:
`git worktree add .claude/worktrees/epic-b4b8 epic/b4b8/friction-hardening`.
Archive search (`scripts/archive-search.sh`) returned no matches for this pitch.
