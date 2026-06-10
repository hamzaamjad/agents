---
id: FEAT-001
title: "Decisions template section, Q-to-DEC resolution rule, checklist update"
type: feature
status: to-do
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: []
tags: [skills, defining-specifications]
agent_created: false
complexity:              # populate at execution Step 3 per references/complexity-scoring.md
---

# Decisions template section, Q-to-DEC resolution rule, checklist update

## Context

Implements REQ-001, REQ-002, REQ-012 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`. v1.2 of the skill lists `DEC-###` in its Agent-Friendly Conventions ID list (line 179) and names decisions a first-class category in Operating Principles (line 28), but the default spec template has no Decisions section — an orphan convention an agent must either invent semantics for or skip.

## Requirements

- [ ] REQ-001: Insert a `## Decisions` section into the default spec template, immediately before `## Open Questions`, with entry format `- DEC-001: <decision> — Rationale: <why>. Alternatives considered: <list>. Date: <YYYY-MM-DD>.`
- [ ] REQ-002: Add guidance (in workflow step 6 Self-Review or adjacent to the template) directing that when a blocking open question is resolved during review, the resolution is recorded as a `DEC-###` entry rather than the `Q-###` item being silently deleted.
- [ ] REQ-012: Extend the Quality Checklist item "Separates confirmed facts from assumptions and open questions" to cover decisions (facts, decisions, assumptions, open questions).

## File path hints

- `skills/defining-specifications/SKILL.md` — modify (template block, Self-Review step or template vicinity, Quality Checklist)

## Constraints

- Do NOT reorder, reword, or remove any other template section (spec NG-002).
- Do NOT change frontmatter `name` or `description` (spec NG-003); do not bump `version` (CHORE-001 owns that).
- Do NOT edit `references/` files (spec NG-005).
- Must keep each modified section under ~40 lines and use moderate imperative phrasing (no all-caps directives).

## Acceptance criteria

- [ ] AC-001: the template block contains `## Decisions` with the DEC-001 entry format, and no other `## `-level template section sits between it and `## Open Questions`.
- [ ] AC-002: the Self-Review or Decisions guidance directs resolved blocking questions to be recorded as `DEC-###` entries.
- [ ] AC-009: the checklist separation item lists facts, decisions, assumptions, and open questions.
- [ ] `wc -l skills/defining-specifications/SKILL.md` ≤ 300.
- [ ] `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high, 0 medium, ≤ 6 low.

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
