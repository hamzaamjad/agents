---
id: FEAT-005
title: "Cross-skill one-line clarifications: defspec traceability, retro external logs, eval path contract"
type: feature
status: done
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: []
tags: [friction-log]
agent_created: false
complexity: 2
---

# Cross-skill one-line clarifications

## Context

Three friction entries each need roughly one sentence in a different file: FRIC-003,
FRIC-019, and FRIC-005 in `.prompts/exercises/02-friction-log.md`. Grouped because each
is too small to stand alone and none shares a file with the other sub-tickets.

## Requirements

- [x] FRIC-003: `skills/defining-specifications/references/requirements-and-acceptance-criteria.md` § Traceability states the NFR rule: every `NFR-###` needs AC coverage or an explicit waiver recorded in the spec ("verified by inspection" with rationale). EPIC-e164's spec left NFR-004 unmapped and nothing caught it.
- [x] FRIC-019: `skills/session-retrospective/SKILL.md` § Phase 1 acknowledges that an externally mandated session log (for example, a brief-required friction log) may be referenced by the retrospective without violating the conversational-only rule — the retro references it, never authors it in Phase 1.
- [x] FRIC-005: `AGENTS.md` § Eval loop states the harness path contract: `files` entries in `skills/*/evals/evals.json` are repo-root-relative; absolute home paths violate the portability rule.

## File path hints

- `skills/defining-specifications/references/requirements-and-acceptance-criteria.md` — modify (§ Traceability)
- `skills/session-retrospective/SKILL.md` — modify (§ Phase 1)
- `AGENTS.md` — modify (§ Eval loop)

## Constraints

- Do NOT add more than two sentences per file.
- Do NOT alter the session-retrospective Phase 1/Phase 2 boundary itself — Phase 1 output stays conversational.
- Do NOT renumber or restructure any section.
- Keep AGENTS.md at or under 150 lines (its own stated cap).

## Acceptance criteria

- [x] The traceability reference names the NFR coverage-or-waiver rule.
- [x] The retro skill names the externally-mandated-log carve-out in Phase 1.
- [x] AGENTS.md § Eval loop names repo-root-relative `files` resolution.
- [x] All three skills' frontmatter remains byte-identical (body/section edits only; `git diff` confirms no frontmatter lines change).
- [x] `python3 skills/engineering-context/scripts/validate_context.py .` reports no new findings versus the pre-ticket run on the epic branch.

## Verification

```bash
rg -n -i 'waiver' skills/defining-specifications/references/requirements-and-acceptance-criteria.md
rg -n -i 'externally mandated|external.*log' skills/session-retrospective/SKILL.md
rg -n -i 'repo-root-relative|repo-relative' AGENTS.md
wc -l AGENTS.md | awk '{exit ($1>150)}'
python3 skills/engineering-context/scripts/validate_context.py . | tail -1
```

## Notes

FRIC-005's original instance (absolute home path in eval-1 `files`) was already fixed by
EPIC-e164 FEAT-004; this ticket documents the contract so the class does not recur.

## Outcome

**Summary:** Added three one-to-two-sentence clarifications resolving FRIC-003, FRIC-019, and FRIC-005 from the exercise-2 friction log: the NFR coverage-or-waiver traceability rule in the defining-specifications references, the externally-mandated-log carve-out in session-retrospective Phase 1, and the repo-root-relative `files` path contract in AGENTS.md § Eval loop. Body-only edits; no structural changes.

**Key decisions:**
- Appended each sentence to the existing paragraph rather than adding new headings — preserves section numbering and the Phase 1/Phase 2 boundary.
- Phrased the retro carve-out as "references, never authors" — keeps Phase 1 strictly conversational.

**Constraints & invariants discovered (keep):**
- Skill frontmatter must stay byte-identical when only body clarifications are needed.
- AGENTS.md stays at or under 150 lines (96 after edit).

**Implementation notes (high signal only):**
- Touch points: `skills/defining-specifications/references/requirements-and-acceptance-criteria.md` § Traceability, `skills/session-retrospective/SKILL.md` § Phase 1, `AGENTS.md` § Eval loop
- Pattern: single-sentence rule statement appended to the governing paragraph

**Verification:**
- Ticket's four `rg`/`wc` checks → all match, AGENTS.md 96 lines
- `validate_context.py .` → `Summary: 0 high, 0 medium, 10 low`, byte-identical to pre-ticket baseline

**Risk / regression surface:**
- None functional; only risk is wording drift if these sections are later restructured.

**Retrieval tags:** FRIC-003, FRIC-005, FRIC-019, NFR waiver, verified by inspection, repo-root-relative, evals.json files, externally mandated log, Phase 1 conversational, traceability

Execution telemetry: 8 tool rounds; FRIC entries resolved: FRIC-003, FRIC-005, FRIC-019.
