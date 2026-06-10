---
id: EPIC-e164
title: "Ship defining-specifications v1.3"
type: epic
status: done
priority: high             # critical | high | medium | low
branch: epic/e164/defspec-v13
created: 2026-06-10
updated: 2026-06-10
tags: [skills, defining-specifications, dogfood]
agent_created: false
complexity:                # 1-10, optional
---

# Ship defining-specifications v1.3

## Context

Implements the approved spec `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md` (Status: Approved 2026-06-10). The spec is authoritative for all requirements (REQ-001..012), non-functional requirements (NFR-001..004), decisions (DEC-001..004), and acceptance criteria (AC-001..010) referenced by sub-tickets.

v1.2 of the skill names artifacts it never defines: an orphan `DEC-###` ID convention, `Approved`/`Blocked` statuses with no entry/exit rules, undefined Simple/Medium/Large clarify tiers, and it lacks any inline worked example. Separately, eval-1 in `skills/defining-specifications/evals/evals.json` is confounded — its subject is the skill itself, so baselines mirror the conventions under test (iteration-3: 10/10 both arms).

What must NOT change: frontmatter `name` and `description` (load-bearing trigger surface), existing template section order except the one Decisions insertion, the two existing `references/` files, the 3/5/7 question budgets, all other skills (spec NG-001..006). Archive search for prior related epics: no matches (fresh `.tickets/` tree; first epic in this repo).

## Sub-tickets

| ID        | Title                                                        | Status |
|-----------|--------------------------------------------------------------|--------|
| FEAT-001  | Decisions template section, Q-to-DEC rule, checklist update  | done   |
| FEAT-002  | Status lifecycle and clarify-tier definitions                | done   |
| FEAT-003  | Inline worked example                                        | done   |
| FEAT-004  | Replace confounded eval-1 with convention-free fixture       | done   |
| CHORE-001 | Version bump, final verification sweep, epic closure         | done   |

## Merge order

1. FEAT-001 (template/conventions base; first writer to `SKILL.md`)
2. FEAT-002 (lifecycle text builds on the Decisions convention; same file as FEAT-001, so sequential)
3. FEAT-003 (worked example must instantiate the Decisions format and a lifecycle-consistent Status line; same file, sequential)
4. FEAT-004 (touches only `evals/`; parallel-safe with 1-3 — may execute concurrently in its own worktree, merges in slot 4 for determinism)
5. CHORE-001 — Epic closure (always last: version bump + full verification battery, then archives epic, deletes orchestration prompt, cleans worktrees; no INDEX.md exists in this repo)

## Acceptance criteria

- [x] All sub-tickets are `done`
- [x] Sanity suite passes on epic branch: `wc -l skills/defining-specifications/SKILL.md` ≤ 300; `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high / 0 medium / ≤ 6 low; `evals.json` parses
- [x] Epic archived and orchestration prompt deleted (by closure ticket)
- [ ] Epic branch integrated to main per the merge strategy approved at the Phase B checkpoint (local merge; nothing pushed) — completes immediately after the closure merge; see main history
- [x] Spec acceptance criteria AC-001..AC-010 all verifiable against the epic branch

## Notes

- Spec: `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`
- Backlog source: `skills/defining-specifications-workspace/iteration-3/benchmark.md` ("Suggested next steps")
- Gitignore precondition resolved on main before this epic branched: `docs/decisions/2026-06-10-version-tickets-and-prompts.md` (DEC-003/DEC-004)
- Orchestration prompt: `.prompts/orchestration/epic-e164_defspec-v13.md`
