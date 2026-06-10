---
id: TASK-001
title: "Fix four dangling skill references surfaced by the FEAT-004 scanner"
type: task
status: to-do
parent: EPIC-b4b8
dependencies: [FEAT-003, FEAT-004]
agent_created: true
complexity: 2
created: 2026-06-10
updated: 2026-06-10
---

# Fix four dangling skill references surfaced by the FEAT-004 scanner

## Goal

Bring the epic branch to `0 high, 0 medium, 0 low` on the validator by resolving the four `dangling_reference` MEDIUM findings FEAT-004's new scan exposed (corrective sub-ticket per orchestrator review of FEAT-004).

## File path hints

- `skills/engineering-context/references/context-design-patterns.md` — modify lines 51-52: the two example entries `references/testing.md` and `references/security.md` are hypothetical illustrations, not real files; rewrite them as placeholder paths (e.g. `references/<topic>.md` style) so the meaning survives but the scanner's placeholder tolerance applies.
- `skills/ticket-workflow/references/orchestrator-review-protocol.md` — modify line 108: `references/templates.md` is written skill-root-relative but the file sits in the same directory; change to `templates.md` (keep the § Task pointer).
- `skills/ticket-workflow/references/outcome-schema.md` — modify line 86: `scripts/archive-search.sh` does not resolve from `references/`; change to `../scripts/archive-search.sh`.

## Constraints

- Do NOT touch files outside the three hints above.
- Do NOT weaken the validator or add allowlist entries — fix the references themselves.
- Preserve each sentence's meaning; minimal rewording only.

## Acceptance criteria

- [ ] `python3 skills/engineering-context/scripts/validate_context.py .` reports `0 high, 0 medium, 0 low`.
- [ ] Each rewritten reference still conveys its original example or pointer intent.

## Verification

```bash
python3 skills/engineering-context/scripts/validate_context.py . | tail -1
```

## Notes

Findings originate from the FEAT-004 Outcome block and the orchestrator's post-merge battery run on the epic branch (commit 784d931).
