---
id: FEAT-005
title: "Cross-skill one-line clarifications: defspec traceability, retro external logs, eval path contract"
type: feature
status: to-do
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: []
tags: [friction-log]
agent_created: false
complexity:
---

# Cross-skill one-line clarifications

## Context

Three friction entries each need roughly one sentence in a different file: FRIC-003,
FRIC-019, and FRIC-005 in `.prompts/exercises/02-friction-log.md`. Grouped because each
is too small to stand alone and none shares a file with the other sub-tickets.

## Requirements

- [ ] FRIC-003: `skills/defining-specifications/references/requirements-and-acceptance-criteria.md` § Traceability states the NFR rule: every `NFR-###` needs AC coverage or an explicit waiver recorded in the spec ("verified by inspection" with rationale). EPIC-e164's spec left NFR-004 unmapped and nothing caught it.
- [ ] FRIC-019: `skills/session-retrospective/SKILL.md` § Phase 1 acknowledges that an externally mandated session log (for example, a brief-required friction log) may be referenced by the retrospective without violating the conversational-only rule — the retro references it, never authors it in Phase 1.
- [ ] FRIC-005: `AGENTS.md` § Eval loop states the harness path contract: `files` entries in `skills/*/evals/evals.json` are repo-root-relative; absolute home paths violate the portability rule.

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

- [ ] The traceability reference names the NFR coverage-or-waiver rule.
- [ ] The retro skill names the externally-mandated-log carve-out in Phase 1.
- [ ] AGENTS.md § Eval loop names repo-root-relative `files` resolution.
- [ ] All three skills' frontmatter remains byte-identical (body/section edits only; `git diff` confirms no frontmatter lines change).
- [ ] `python3 skills/engineering-context/scripts/validate_context.py .` reports no new findings versus the pre-ticket run on the epic branch.

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
