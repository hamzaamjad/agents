---
id: TASK-001
title: "Fix four dangling skill references surfaced by the FEAT-004 scanner"
type: task
status: done
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

## Outcome

**Summary:** Fixed the four dangling `dangling_reference` MEDIUM findings across three reference files: the two hypothetical example paths in engineering-context's context-design-patterns.md now use placeholder-style names, and two skill-root-relative paths in ticket-workflow references were corrected to resolve from `references/`. Validator is clean on the branch; meaning of every sentence preserved.

**Key decisions:**
- Rewrote example entries as `references/<topic>.md`-style placeholders — keeps the illustrative intent while triggering the scanner's placeholder tolerance, rather than creating stub files.
- Fixed paths at the reference site (`templates.md`, `../scripts/archive-search.sh`) — per ticket constraint, no validator changes or allowlist entries.

**Constraints & invariants discovered (keep):**
- Paths inside `references/` docs must resolve relative to that directory, not the skill root.
- Hypothetical example paths in skill docs must use placeholder syntax (`<topic>`) or they register as dangling references.

**Implementation notes (high signal only):**
- Touch points: `skills/engineering-context/references/context-design-patterns.md`, `skills/ticket-workflow/references/orchestrator-review-protocol.md`, `skills/ticket-workflow/references/outcome-schema.md`
- Pattern: fix-at-reference-site, minimal rewording

**Verification:**
- `python3 skills/engineering-context/scripts/validate_context.py .` → "All checks passed." (zero-finding output; Summary line only prints when findings exist)
- `--format json` summary → `{'high': 0, 'medium': 0, 'low': 0}`

**Risk / regression surface:**
- Future docs adding skill-root-relative paths from `references/` will reintroduce findings; the FEAT-004 scanner guards this.

**Retrieval tags:** dangling_reference, validate_context.py, context-design-patterns, orchestrator-review-protocol, outcome-schema, archive-search.sh, templates.md, placeholder paths, FEAT-004, EPIC-b4b8

Tool rounds: 11
