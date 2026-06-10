---
id: FEAT-002
title: "Status lifecycle and clarify-tier definitions"
type: feature
status: to-do
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: [FEAT-001]
tags: [skills, defining-specifications]
agent_created: false
complexity:              # populate at execution Step 3 per references/complexity-scoring.md
---

# Status lifecycle and clarify-tier definitions

## Context

Implements REQ-003..REQ-006 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`. v1.2's template offers `Status: Draft | Ready for Review | Approved | Blocked` but only defines the Draft-to-Ready-for-Review transition (Self-Review, line 98); `Approved` and `Blocked` have no entry or exit rules. The Clarify step keys question budgets (3/5/7) to Simple/Medium/Large specs without defining the tiers anywhere in the skill or its references. Phase A of this very epic hit the lifecycle gap: an approved-at-checkpoint spec had no defined status to move to.

Depends on FEAT-001 because both edit `SKILL.md` (serialized to avoid same-file merge conflicts) and the lifecycle text may reference recording resolutions as `DEC-###` entries.

## Requirements

- [ ] REQ-003: Define entry and exit criteria for each `Status` value (`Draft`, `Ready for Review`, `Approved`, `Blocked`), colocated with the existing Self-Review status gate; the current Draft-to-Ready-for-Review rule's meaning is preserved.
- [ ] REQ-004: If a spec is marked `Blocked`, the status line or an adjacent note must name the blocking `Q-###` or external dependency.
- [ ] REQ-005: `Approved` requires approver and date recorded; material post-approval edits revert the spec to `Draft` or `Ready for Review` with a changelog entry.
- [ ] REQ-006: Define Simple, Medium, and Large tiers using observable scope signals (e.g. components/files touched, contract/data/schema changes, rollout or migration needs, residual ambiguity after intake), keeping the existing 3/5/7 question budgets unchanged.

## File path hints

- `skills/defining-specifications/SKILL.md` — modify (workflow step 3 Clarify vicinity; workflow step 6 Self-Review vicinity or a small adjacent subsection)

## Constraints

- Do NOT change the 3/5/7 question budgets or reword unrelated workflow text (spec NG-002).
- Do NOT change frontmatter `name`/`description` or bump `version` (CHORE-001 owns the bump).
- Do NOT edit `references/` files (spec NG-005).
- Must keep each new or modified section under ~40 lines; moderate phrasing.

## Acceptance criteria

- [ ] AC-003: each of the four statuses has at least one entry criterion and one exit criterion; `Blocked` requires naming its blocker; `Approved` requires approver-and-date plus the re-approval rule for material edits.
- [ ] AC-004: Simple, Medium, and Large are each defined by observable scope signals, and the literal budgets "up to 3", "up to 5", "up to 7" remain.
- [ ] `wc -l skills/defining-specifications/SKILL.md` ≤ 300.
- [ ] `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high, 0 medium, ≤ 6 low.

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
