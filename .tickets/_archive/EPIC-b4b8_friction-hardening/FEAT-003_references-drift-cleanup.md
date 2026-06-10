---
id: FEAT-003
title: "ticket-workflow references: drift and portability cleanup"
type: feature
status: done
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: []
tags: [friction-log]
agent_created: false
complexity: 4
---

# ticket-workflow references: drift and portability cleanup

## Context

Five friction entries target the skill's `references/` files rather than SKILL.md:
FRIC-001, 010, 011, 014 (template half), and 016 in `.prompts/exercises/02-friction-log.md`.
These run parallel to FEAT-001/002 — different files, no merge conflict surface.

## Requirements

- [x] FRIC-010: `references/templates.md` epic template no longer mentions INDEX.md (HTML comment and merge-order line N) — SKILL.md's closure protocol has no INDEX.md step; the two must not drift.
- [x] FRIC-011: the epic template's acceptance criterion "PR from epic branch to main created and ready for review" gains "(or local merge per repo policy)".
- [x] FRIC-016: `references/outcome-schema.md` origin-repo references (search: "implementation_plan", "r4-archive-knowledge-retrieval", "from the point FEAT-003 lands") are replaced with self-contained wording per the bundling rule in AGENTS.md.
- [x] FRIC-001: `references/orchestration-template.md` preamble comment gains a re-run hygiene clause: a re-run that finds leftover artifacts from an interrupted prior run adopts-and-verifies them or deletes-and-rewrites — never silently mixes the two.
- [x] FRIC-014: in the same template, M2 (post-merge checks) is reordered after worktree cleanup or scoped so repo-wide scans ignore `.claude/worktrees/` — nested checkouts currently poison tree-scanning sanity commands.
- [x] Gate tiering (user decision 2026-06-10, cost control for long test suites): the template documents that gates fall into cost tiers — inspection gates (A, C-G) always run per ticket; Gate B/H4's `<SANITY_COMMANDS>` is the scoped tier (the ticket's own Verification block plus tests touching its Gate D allowlist paths, never the full suite by default); the full battery runs at integration boundaries only (`<POST_MERGE_CHECKS>` after the last content ticket merges, and at the epic-to-main merge). Tickets with complexity >= 6 or cross-cutting paths may opt into the broader suite at their own merge. Add the same tiering rule in one short paragraph to `references/orchestrator-review-protocol.md` so the two files do not drift.

## File path hints

- `skills/ticket-workflow/references/templates.md` — modify (epic template only)
- `skills/ticket-workflow/references/outcome-schema.md` — modify (provenance wording only)
- `skills/ticket-workflow/references/orchestration-template.md` — modify (preamble + B/M-steps + gate tiering)
- `skills/ticket-workflow/references/orchestrator-review-protocol.md` — modify (gate-tiering paragraph only)

## Constraints

- Do NOT edit SKILL.md or any file outside the four named reference files.
- Do NOT change template placeholder names (`<EPIC_BRANCH>`, `<MAX_FIX_CYCLES>`, ...) — per-epic instances depend on them.
- Edits to `orchestrator-review-protocol.md` are limited to the gate-tiering paragraph; keep it and the template consistent — the two must not drift.

## Acceptance criteria

- [x] `rg -c 'INDEX' skills/ticket-workflow/references/templates.md` returns no matches (exit 1).
- [x] The epic template AC line contains "local merge".
- [x] `rg -c 'implementation_plan|r4-archive' skills/ticket-workflow/references/outcome-schema.md` returns no matches (exit 1).
- [x] The orchestration template preamble contains the re-run hygiene clause (the adopt-and-verify wording).
- [x] M-step ordering or scoping reflects the FRIC-014 fix in the template text.
- [x] Both the template and the review protocol name the three gate cost tiers (per-ticket inspection, scoped sanity, integration-boundary full battery) with matching semantics.

## Verification

```bash
# "adopt" discriminates (absent today); a bare "re-run" grep would not — Gate B
# already says "re-run once".
rg -n 'INDEX' skills/ticket-workflow/references/templates.md; test $? -eq 1
rg -n 'local merge' skills/ticket-workflow/references/templates.md
rg -n 'implementation_plan|r4-archive' skills/ticket-workflow/references/outcome-schema.md; test $? -eq 1
rg -n -i 'adopt' skills/ticket-workflow/references/orchestration-template.md
rg -n -i 'tier' skills/ticket-workflow/references/orchestration-template.md skills/ticket-workflow/references/orchestrator-review-protocol.md
python3 skills/engineering-context/scripts/validate_context.py . | tail -1
```

## Notes

EPIC-e164 instantiated its orchestration prompt with the M2/M4 hazard live: the first
post-merge sanity scan reported 9 phantom mediums until the nested worktree was removed.

## Outcome

**Summary:** Cleaned drift and origin-repo provenance out of four ticket-workflow reference files. The epic template no longer mentions INDEX.md and allows local merge; outcome-schema.md is self-contained; the orchestration template gains a re-run hygiene clause, a fixed M-step ordering, and a three-tier gate cost model mirrored in the review protocol. Resolved FRIC-001, 010, 011, 014 (template half), and 016 in 13 tool rounds.

**Key decisions:**
- Removed INDEX.md from templates.md rather than adding the step to SKILL.md — SKILL.md was the followed source of truth and no INDEX.md exists.
- FRIC-014 fixed by reordering (cleanup before post-merge checks) plus a scoping fallback excluding `.claude/worktrees/` — covers both orderings an orchestrator may need.

**Constraints & invariants discovered (keep):**
- Template placeholder names (`<EPIC_BRANCH>`, `<SANITY_COMMANDS>`, ...) are load-bearing; per-epic instances depend on them.
- Gate-tiering semantics in orchestration-template.md and orchestrator-review-protocol.md must stay identical — the two must not drift.

**Implementation notes (high signal only):**
- Touch points: `skills/ticket-workflow/references/{templates,outcome-schema,orchestration-template,orchestrator-review-protocol}.md`
- Pattern: paired-document sync (template block + protocol paragraph carrying the same tier rule)

**Verification:**
- `rg -n 'INDEX' .../templates.md; test $? -eq 1` → exit 0 (no matches)
- `rg -n -i 'tier' .../orchestration-template.md .../orchestrator-review-protocol.md` → hits in both files
- `python3 skills/engineering-context/scripts/validate_context.py . | tail -1` → `Summary: 0 high, 0 medium, 10 low` (all LOWs pre-existing AGENTS.md tone findings; no sibling-worktree noise)

**Risk / regression surface:**
- Per-epic orchestration prompts instantiated from the old template won't carry the tiering block; only future instances inherit it.

**Retrieval tags:** FRIC-001, FRIC-010, FRIC-011, FRIC-014, FRIC-016, gate cost tiers, SANITY_COMMANDS, POST_MERGE_CHECKS, re-run hygiene, INDEX.md, local merge, bundling rule
