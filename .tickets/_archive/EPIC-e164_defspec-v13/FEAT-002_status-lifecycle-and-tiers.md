---
id: FEAT-002
title: "Status lifecycle and clarify-tier definitions"
type: feature
status: done
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: [FEAT-001]
tags: [skills, defining-specifications]
agent_created: false
complexity: 3            # rubric: files 2(.20) deps 4(.15) testing 3(.15) risk 2(.15) new/mod 2(.10) crosscut 1(.10) api 1(.05) db 1(.10) = 2.20 → 3
---

# Status lifecycle and clarify-tier definitions

## Context

Implements REQ-003..REQ-006 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`. v1.2's template offers `Status: Draft | Ready for Review | Approved | Blocked` but only defines the Draft-to-Ready-for-Review transition (Self-Review, line 98); `Approved` and `Blocked` have no entry or exit rules. The Clarify step keys question budgets (3/5/7) to Simple/Medium/Large specs without defining the tiers anywhere in the skill or its references. Phase A of this very epic hit the lifecycle gap: an approved-at-checkpoint spec had no defined status to move to.

Depends on FEAT-001 because both edit `SKILL.md` (serialized to avoid same-file merge conflicts) and the lifecycle text may reference recording resolutions as `DEC-###` entries.

## Requirements

- [x] REQ-003: Define entry and exit criteria for each `Status` value (`Draft`, `Ready for Review`, `Approved`, `Blocked`), colocated with the existing Self-Review status gate; the current Draft-to-Ready-for-Review rule's meaning is preserved.
- [x] REQ-004: If a spec is marked `Blocked`, the status line or an adjacent note must name the blocking `Q-###` or external dependency.
- [x] REQ-005: `Approved` requires approver and date recorded; material post-approval edits revert the spec to `Draft` or `Ready for Review` with a changelog entry.
- [x] REQ-006: Define Simple, Medium, and Large tiers using observable scope signals (e.g. components/files touched, contract/data/schema changes, rollout or migration needs, residual ambiguity after intake), keeping the existing 3/5/7 question budgets unchanged.

## File path hints

- `skills/defining-specifications/SKILL.md` — modify (workflow step 3 Clarify vicinity; workflow step 6 Self-Review vicinity or a small adjacent subsection)

## Constraints

- Do NOT change the 3/5/7 question budgets or reword unrelated workflow text (spec NG-002).
- Do NOT change frontmatter `name`/`description` or bump `version` (CHORE-001 owns the bump).
- Do NOT edit `references/` files (spec NG-005).
- Must keep each new or modified section under ~40 lines; moderate phrasing.

## Acceptance criteria

- [x] AC-003: each of the four statuses has at least one entry criterion and one exit criterion; `Blocked` requires naming its blocker; `Approved` requires approver-and-date plus the re-approval rule for material edits.
- [x] AC-004: Simple, Medium, and Large are each defined by observable scope signals, and the literal budgets "up to 3", "up to 5", "up to 7" remain.
- [x] `wc -l skills/defining-specifications/SKILL.md` ≤ 300.
- [x] `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high, 0 medium, ≤ 6 low.

## Verification

```bash
# AC-003: all four statuses have lifecycle rules near the Self-Review gate
rg -n -A 2 'Draft|Ready for Review|Approved|Blocked' skills/defining-specifications/SKILL.md | rg -i 'entry|exit|until|move|revert|when' | head -20
rg -n -i 'blocked.*(Q-|blocker|dependency)' skills/defining-specifications/SKILL.md
rg -n -i 'approved.*(approver|date)|approver.*date' skills/defining-specifications/SKILL.md
# AC-004: tiers defined, budgets unchanged
rg -n -i 'simple.*:|medium.*:|large' skills/defining-specifications/SKILL.md | head -10
rg -n 'up to 3|up to 5|up to 7' skills/defining-specifications/SKILL.md
# Budgets and hygiene
wc -l skills/defining-specifications/SKILL.md
python3 skills/engineering-context/scripts/validate_context.py .
```

## Notes

Spec sections: REQ-003..006, AC-003/AC-004, Technical Context placement guidance. The rg checks above are heuristics — the executing agent must confirm AC-003/AC-004 by reading the modified sections, then record evidence in the verification log.

## Verification log (2026-06-10)

- Lifecycle block read-confirmed: all four statuses carry explicit entry and exit rules (SKILL.md:100-105); Draft→Ready-for-Review meaning preserved (gate sentence untouched above it)
- `rg -i 'blocked.*(Q-|blocker|dependency)'` → SKILL.md:105; `rg -i 'approved.*approver'` → SKILL.md:104
- Tiers read-confirmed at SKILL.md:66-68, defined by scope signals; literal budgets "up to 3/5/7" intact
- `wc -l` → 221 (≤ 300); Self-Review section 12 lines (< 40)
- `validate_context.py` → 0 high, 0 medium, 6 low (baseline)
- Actual tool rounds: 5 batched rounds (7 repo-acting tool calls) vs complexity 3 — in line

## Outcome

**Summary:** Defined the previously dangling spec `Status` lifecycle — all four values (`Draft`, `Ready for Review`, `Approved`, `Blocked`) now have explicit entry and exit rules colocated with the Self-Review gate, including the approver-and-date requirement and the material-edit reversion rule. Defined the Simple/Medium/Large clarify tiers by observable scope signals inline in the existing budget bullets, leaving the 3/5/7 budgets untouched. One file, +7 net lines (214 → 221).

**Key decisions:**
- Lifecycle expressed as per-status entry/exit bullets, not a transition diagram — greppable and renders anywhere.
- Tier definitions inlined as parentheticals in the existing bullets — avoids a new section and keeps the budget literals stable for downstream greps.
- `Blocked` exits to "the status it interrupted" rather than always `Draft` — avoids penalizing approved specs blocked late.

**Constraints & invariants discovered (keep):**
- The Draft→Ready-for-Review gate sentence is load-bearing for v1.2 compatibility; lifecycle text extends it without rewording it.
- Budget literals "up to 3/5/7" are verification anchors; do not rephrase.

**Implementation notes (high signal only):**
- Touch points: `skills/defining-specifications/SKILL.md` (workflow steps 3 and 6)
- Pattern: define-where-referenced — semantics live adjacent to first use

**Verification:**
- `rg -i 'blocked.*(Q-|blocker|dependency)'` → :105; `rg -i 'approved.*approver'` → :104
- `rg 'up to 3|up to 5|up to 7'` → :66-68; `wc -l` → 221; validator → baseline

**Risk / regression surface:**
- FEAT-003's example must keep its Status line consistent with these rules (dependency encoded).

**Retrieval tags:** defining-specifications, status lifecycle, Draft, Ready for Review, Approved, Blocked, clarify tiers, Simple Medium Large, question budget, v1.3
