---
id: FEAT-003
title: "Inline worked example"
type: feature
status: to-do
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: [FEAT-002]
tags: [skills, defining-specifications]
agent_created: false
complexity:              # populate at execution Step 3 per references/complexity-scoring.md
---

# Inline worked example

## Context

Implements REQ-007 and REQ-008 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`. v1.2 has a template and reference files but no end-to-end filled instance anywhere in `SKILL.md`; the nearest thing is a weak-vs-strong contrast in `references/requirements-and-acceptance-criteria.md`. Spec DEC-002: the example lives inline (≤ 40 lines), not only in `references/`.

Depends on FEAT-002 because the example's `Status` line must be consistent with the lifecycle FEAT-002 defines, and its `DEC-###` entry must follow the format FEAT-001 introduced (FEAT-001 is transitively covered via FEAT-002's dependency).

## Requirements

- [ ] REQ-007: Add one inline worked example to `SKILL.md`, at most 40 lines including its code fence, presented as a condensed filled instance of the template. It must demonstrate at least: two distinct EARS requirement patterns, one Given/When/Then acceptance criterion with a `(verifies REQ-###)` mapping, one `DEC-###` entry, one `Q-###` or `ASM-###` entry, and a `Status` line consistent with the FEAT-002 lifecycle.
- [ ] REQ-008: The worked example section points to `references/requirements-and-acceptance-criteria.md` for full patterns rather than duplicating reference content.
- [ ] Placement: immediately after the Default Spec Template section (spec Technical Context, advisory).

## File path hints

- `skills/defining-specifications/SKILL.md` — modify (insert one section after the Default Spec Template)

## Constraints

- Do NOT exceed 40 lines for the example block. If the file would exceed 300 lines, apply the spec's deterministic overflow fallback: move the full example to a new `references/worked-example.md`, keep an inline pointer plus an excerpt of at most 10 lines (spec Technical Context).
- Do NOT modify the template block itself or other sections; do not change frontmatter or `references/` (except via the overflow fallback above).
- The example must be self-consistent: its IDs cross-reference correctly (the AC verifies a REQ that exists in the example).

## Acceptance criteria

- [ ] AC-005: the example block is ≤ 40 lines including the fence, contains two distinct EARS patterns (e.g. one `When ..., the ... shall ...` and one `If ..., then the ... shall ...` or `While ...`), one GWT criterion with `(verifies REQ-`, one `DEC-` entry, one `Q-` or `ASM-` entry, and a pointer to `references/requirements-and-acceptance-criteria.md` adjacent to the block.
- [ ] The example sits after the Default Spec Template section and before Agent-Friendly Conventions.
- [ ] `wc -l skills/defining-specifications/SKILL.md` ≤ 300.
- [ ] `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high, 0 medium, ≤ 6 low.

## Verification

```bash
# AC-005: measure the example block and check required contents
python3 - <<'EOF'
import re
t = open('skills/defining-specifications/SKILL.md').read()
m = re.search(r'\n## [^\n]*[Ee]xample[^\n]*\n(.*?)(?=\n## |\Z)', t, re.S)
assert m, 'no worked example section found'
sec = m.group(1)
fence = re.search(r'```.*?```', sec, re.S)
assert fence, 'no fenced example block'
n = fence.group(0).count('\n') + 1
assert n <= 40, f'example block is {n} lines (> 40)'
assert re.search(r'When .*shall ', sec), 'event-driven EARS pattern missing'
assert re.search(r'(If .*then .*shall |While .*shall |Where .*shall )', sec), 'second EARS pattern missing'
assert '(verifies REQ-' in sec, 'GWT-to-REQ mapping missing'
assert 'DEC-' in sec, 'DEC entry missing'
assert ('Q-' in sec) or ('ASM-' in sec), 'Q/ASM entry missing'
assert 'Status:' in sec, 'Status line missing'
assert 'requirements-and-acceptance-criteria.md' in sec, 'reference pointer missing'
print(f'AC-005 ok ({n} lines)')
EOF
# Placement: example section appears after the template section
rg -n '^## ' skills/defining-specifications/SKILL.md
# Budgets and hygiene
wc -l skills/defining-specifications/SKILL.md
python3 skills/engineering-context/scripts/validate_context.py .
```

## Notes

Spec sections: REQ-007/REQ-008, DEC-002, AC-005, RISK-001 (overflow), Technical Context (placement + fallback). Keep the example's subject domain different from spec-tooling itself so it doubles as a usage illustration (a small CLI or validation feature works well).
