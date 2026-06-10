---
id: FEAT-003
title: "Inline worked example"
type: feature
status: done
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: [FEAT-002]
tags: [skills, defining-specifications]
agent_created: false
complexity: 3            # rubric: files 2(.20) deps 4(.15) testing 3(.15) risk 2(.15) new/mod 3(.10) crosscut 1(.10) api 1(.05) db 1(.10) = 2.30 → 3
---

# Inline worked example

## Context

Implements REQ-007 and REQ-008 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`. v1.2 has a template and reference files but no end-to-end filled instance anywhere in `SKILL.md`; the nearest thing is a weak-vs-strong contrast in `references/requirements-and-acceptance-criteria.md`. Spec DEC-002: the example lives inline (≤ 40 lines), not only in `references/`.

Depends on FEAT-002 because the example's `Status` line must be consistent with the lifecycle FEAT-002 defines, and its `DEC-###` entry must follow the format FEAT-001 introduced (FEAT-001 is transitively covered via FEAT-002's dependency).

## Requirements

- [x] REQ-007: Add one inline worked example to `SKILL.md`, at most 40 lines including its code fence, presented as a condensed filled instance of the template. It must demonstrate at least: two distinct EARS requirement patterns, one Given/When/Then acceptance criterion with a `(verifies REQ-###)` mapping, one `DEC-###` entry, one `Q-###` or `ASM-###` entry, and a `Status` line consistent with the FEAT-002 lifecycle.
- [x] REQ-008: The worked example section points to `references/requirements-and-acceptance-criteria.md` for full patterns rather than duplicating reference content.
- [x] Placement: immediately after the Default Spec Template section (spec Technical Context, advisory).

## File path hints

- `skills/defining-specifications/SKILL.md` — modify (insert one section after the Default Spec Template)

## Constraints

- Do NOT exceed 40 lines for the example block. If the file would exceed 300 lines, apply the spec's deterministic overflow fallback: move the full example to a new `references/worked-example.md`, keep an inline pointer plus an excerpt of at most 10 lines (spec Technical Context).
- Do NOT modify the template block itself or other sections; do not change frontmatter or `references/` (except via the overflow fallback above).
- The example must be self-consistent: its IDs cross-reference correctly (the AC verifies a REQ that exists in the example).

## Acceptance criteria

- [x] AC-005: the example block is ≤ 40 lines including the fence, contains two distinct EARS patterns (e.g. one `When ..., the ... shall ...` and one `If ..., then the ... shall ...` or `While ...`), one GWT criterion with `(verifies REQ-`, one `DEC-` entry, one `Q-` or `ASM-` entry, and a pointer to `references/requirements-and-acceptance-criteria.md` adjacent to the block.
- [x] The example sits after the Default Spec Template section and before Agent-Friendly Conventions.
- [x] `wc -l skills/defining-specifications/SKILL.md` ≤ 300.
- [x] `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high, 0 medium, ≤ 6 low.

## Verification

```bash
# AC-005: measure the example block and check required contents
# Corrected at execution (2026-06-10): the original section regex terminated at
# '\n## ' and so cut off at the headings INSIDE the fenced example — it could
# not pass for any faithful filled instance. Same assertions, fence-aware parse.
python3 - <<'EOF'
import re
t = open('skills/defining-specifications/SKILL.md').read()
h = re.search(r'\n## [^\n]*[Ee]xample[^\n]*\n', t)
assert h, 'no worked example section found'
rest = t[h.end():]
fence = re.search(r'```.*?\n```', rest, re.S)
assert fence, 'no fenced example block'
sec = rest[:fence.end()]                      # intro + example block
n = fence.group(0).count('\n') + 1
assert n <= 40, f'example block is {n} lines (> 40)'
assert re.search(r'When .*shall ', sec), 'event-driven EARS pattern missing'
assert re.search(r'(If .*then .*shall |While .*shall |Where .*shall )', sec), 'second EARS pattern missing'
assert '(verifies REQ-' in sec, 'GWT-to-REQ mapping missing'
assert 'DEC-' in sec, 'DEC entry missing'
assert ('Q-' in sec) or ('ASM-' in sec), 'Q/ASM entry missing'
assert 'Status:' in sec, 'Status line missing'
assert 'requirements-and-acceptance-criteria.md' in sec, 'reference pointer missing'
# placement: example section after the template section, before Agent-Friendly Conventions
assert t.index('\n## Default Spec Template\n') < h.start() < t.index('\n## Agent-Friendly Conventions\n')
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

## Verification log (2026-06-10)

- AC-005 fence-aware check → `AC-005 ok (20 lines)`: two EARS patterns (When/shall at example REQ-001, If/then/shall at REQ-002), GWT with `(verifies REQ-`, DEC-001 entry, Q-001 entry, Status line, reference pointer — all asserted
- Placement → section at line 187, between Default Spec Template (107) and Agent-Friendly Conventions (212); section spans 25 lines (< 40)
- `wc -l` → 246 (≤ 300; overflow fallback not triggered)
- `validate_context.py` → 0 high, 0 medium, 6 low (baseline)
- Deviation, corrected before execution: the ticket's original AC-005 regex terminated the section capture at `\n## ` and therefore cut off at headings inside the fenced example — unpassable for any faithful instance. Replaced with a fence-aware parse asserting the same properties plus placement; correction annotated in the Verification section above and logged as exercise friction FRIC-017.
- Actual tool rounds: 6 batched rounds (8 repo-acting tool calls) vs complexity 3 — in line

## Outcome

**Summary:** Added the skill's first inline worked example: a 20-line condensed filled instance of the template (CLI flag spec for skipping archived tickets in search), demonstrating two EARS patterns, a Given/When/Then criterion with `(verifies REQ-###)` traceability, a `DEC-###` decision with rationale/alternatives/date, a non-blocking `Q-###`, and a `Ready for Review` status line consistent with the FEAT-002 lifecycle. Placed immediately after the Default Spec Template; +25 net lines (221 → 246), overflow fallback not needed.

**Key decisions:**
- Example subject is a small CLI behavior, not spec tooling — avoids the self-reference confound that broke eval-1.
- Kept full `## `-level headings inside the fence for fidelity and fixed the verification parser instead of distorting the example to satisfy a buggy regex.

**Constraints & invariants discovered (keep):**
- Any text check that captures "the example section" must be fence-aware: filled template instances legitimately contain `## ` headings.
- Example block stays ≤ 40 lines including the fence; overflow moves it to `references/worked-example.md` with a ≤ 10-line excerpt.

**Implementation notes (high signal only):**
- Touch points: `skills/defining-specifications/SKILL.md` (new section after the template); ticket Verification section (corrected check)
- Pattern: condensed-instance illustration with pointer to full reference patterns

**Verification:**
- fence-aware AC-005 script → `AC-005 ok (20 lines)`
- `rg '^## '` → example at :187 between :107 and :212; `wc -l` → 246; validator → baseline

**Risk / regression surface:**
- Future SKILL.md greps may match the example's REQ/DEC/Q tokens; scope greps to sections when that matters (CHORE-001's battery already does).

**Retrieval tags:** defining-specifications, worked example, inline example, EARS, Given/When/Then, traceability, fence-aware regex, DEC-001, v1.3, condensed instance
