---
id: FEAT-001
title: "Decisions template section, Q-to-DEC resolution rule, checklist update"
type: feature
status: done
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: []
tags: [skills, defining-specifications]
agent_created: false
complexity: 2            # rubric: files 2(.20) deps 1(.15) testing 2(.15) risk 2(.15) new/mod 2(.10) crosscut 1(.10) api 1(.05) db 1(.10) = 1.60 → 2
---

# Decisions template section, Q-to-DEC resolution rule, checklist update

## Context

Implements REQ-001, REQ-002, REQ-012 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`. v1.2 of the skill lists `DEC-###` in its Agent-Friendly Conventions ID list (line 179) and names decisions a first-class category in Operating Principles (line 28), but the default spec template has no Decisions section — an orphan convention an agent must either invent semantics for or skip.

## Requirements

- [x] REQ-001: Insert a `## Decisions` section into the default spec template, immediately before `## Open Questions`, with entry format `- DEC-001: <decision> — Rationale: <why>. Alternatives considered: <list>. Date: <YYYY-MM-DD>.`
- [x] REQ-002: Add guidance (in workflow step 6 Self-Review or adjacent to the template) directing that when a blocking open question is resolved during review, the resolution is recorded as a `DEC-###` entry rather than the `Q-###` item being silently deleted.
- [x] REQ-012: Extend the Quality Checklist item "Separates confirmed facts from assumptions and open questions" to cover decisions (facts, decisions, assumptions, open questions).

## File path hints

- `skills/defining-specifications/SKILL.md` — modify (template block, Self-Review step or template vicinity, Quality Checklist)

## Constraints

- Do NOT reorder, reword, or remove any other template section (spec NG-002).
- Do NOT change frontmatter `name` or `description` (spec NG-003); do not bump `version` (CHORE-001 owns that).
- Do NOT edit `references/` files (spec NG-005).
- Must keep each modified section under ~40 lines and use moderate imperative phrasing (no all-caps directives).

## Acceptance criteria

- [x] AC-001: the template block contains `## Decisions` with the DEC-001 entry format, and no other `## `-level template section sits between it and `## Open Questions`.
- [x] AC-002: the Self-Review or Decisions guidance directs resolved blocking questions to be recorded as `DEC-###` entries.
- [x] AC-009: the checklist separation item lists facts, decisions, assumptions, and open questions.
- [x] `wc -l skills/defining-specifications/SKILL.md` ≤ 300.
- [x] `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high, 0 medium, ≤ 6 low.

## Verification

```bash
# AC-001: section exists, ordered immediately before Open Questions inside the template
python3 - <<'EOF'
t = open('skills/defining-specifications/SKILL.md').read()
d = t.index('\n## Decisions\n'); o = t.index('\n## Open Questions\n')
assert d < o, 'Decisions must precede Open Questions'
assert t[d:o].count('\n## ') == 1, 'Decisions must be immediately before Open Questions'
assert 'DEC-001:' in t[d:o], 'entry format with DEC-001 missing'
print('AC-001 ok')
EOF
# AC-002: Q-resolution-to-DEC guidance present
rg -n 'DEC-' skills/defining-specifications/SKILL.md | rg -iv '^\s*-\s*DEC-001' | rg -i 'resolv' || rg -n -i 'resolved.*DEC-|DEC-###.*resolv' skills/defining-specifications/SKILL.md
# AC-009: checklist separation item includes decisions
rg -n -i 'facts.*decisions.*assumptions.*open questions' skills/defining-specifications/SKILL.md
# Budgets and hygiene
wc -l skills/defining-specifications/SKILL.md
python3 skills/engineering-context/scripts/validate_context.py .
```

## Notes

Spec sections: Requirements, Decisions (DEC-001..004), Acceptance Criteria AC-001/AC-002/AC-009. FEAT-002 and FEAT-003 edit the same file afterward; keep the diff tightly scoped to the three requirement areas.

## Verification log (2026-06-10)

- AC-001 python check → `AC-001 ok` (Decisions immediately before Open Questions, DEC-001 format present)
- AC-002 rg → match at SKILL.md:98 (resolution-to-DEC rule in Self-Review)
- AC-009 rg → match at SKILL.md:199 (checklist lists facts, decisions, assumptions, open questions)
- `wc -l` → 214 (≤ 300)
- `validate_context.py` → 0 high, 0 medium, 6 low (baseline, no new findings)
- Actual tool rounds: 5 batched rounds (9 repo-acting tool calls) vs complexity 2 — in line with prediction

## Outcome

**Summary:** Added the missing `## Decisions` section to the default spec template (immediately before `## Open Questions`), de-orphaning the `DEC-###` ID convention; added a Self-Review rule that resolved blocking questions become `DEC-###` entries with the `Q-###` item pointing at them; extended the quality-checklist separation item to cover decisions. Scope: one file, three localized edits, +3 net lines (211 → 214).

**Key decisions:**
- Entry format carries Rationale, Alternatives considered, and Date inline — keeps decisions greppable one-liners, not subsections.
- Placed Decisions between Risks and Open Questions — decisions are settled context, questions remain open; adjacency mirrors the Q-to-DEC flow.

**Constraints & invariants discovered (keep):**
- No other template section may sit between `## Decisions` and `## Open Questions` (verification asserts adjacency).
- Checklist separation item must keep the order: facts, decisions, assumptions, open questions.

**Implementation notes (high signal only):**
- Touch points: `skills/defining-specifications/SKILL.md` (template block, workflow step 6, Quality Checklist)
- Pattern: convention de-orphaning — every named ID type gets a template home

**Verification:**
- AC-001 python adjacency check → `AC-001 ok`
- `rg -i 'resolved.*DEC-'` → SKILL.md:98; `rg -i 'facts.*decisions.*assumptions.*open questions'` → SKILL.md:199
- `wc -l` → 214; `validate_context.py` → 0 high / 0 medium / 6 low baseline

**Risk / regression surface:**
- FEAT-002/003 edit the same file next; adjacency assertion guards against accidental section insertion between Decisions and Open Questions.

**Retrieval tags:** defining-specifications, DEC-###, Decisions section, template, Q-to-DEC, quality checklist, SKILL.md, spec conventions, v1.3
