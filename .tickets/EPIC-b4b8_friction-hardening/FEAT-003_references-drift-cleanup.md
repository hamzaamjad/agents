---
id: FEAT-003
title: "ticket-workflow references: drift and portability cleanup"
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

# ticket-workflow references: drift and portability cleanup

## Context

Five friction entries target the skill's `references/` files rather than SKILL.md:
FRIC-001, 010, 011, 014 (template half), and 016 in `.prompts/exercises/02-friction-log.md`.
These run parallel to FEAT-001/002 — different files, no merge conflict surface.

## Requirements

- [ ] FRIC-010: `references/templates.md` epic template no longer mentions INDEX.md (HTML comment and merge-order line N) — SKILL.md's closure protocol has no INDEX.md step; the two must not drift.
- [ ] FRIC-011: the epic template's acceptance criterion "PR from epic branch to main created and ready for review" gains "(or local merge per repo policy)".
- [ ] FRIC-016: `references/outcome-schema.md` origin-repo references (search: "implementation_plan", "r4-archive-knowledge-retrieval", "from the point FEAT-003 lands") are replaced with self-contained wording per the bundling rule in AGENTS.md.
- [ ] FRIC-001: `references/orchestration-template.md` preamble comment gains a re-run hygiene clause: a re-run that finds leftover artifacts from an interrupted prior run adopts-and-verifies them or deletes-and-rewrites — never silently mixes the two.
- [ ] FRIC-014: in the same template, M2 (post-merge checks) is reordered after worktree cleanup or scoped so repo-wide scans ignore `.claude/worktrees/` — nested checkouts currently poison tree-scanning sanity commands.
- [ ] Gate tiering (user decision 2026-06-10, cost control for long test suites): the template documents that gates fall into cost tiers — inspection gates (A, C-G) always run per ticket; Gate B/H4's `<SANITY_COMMANDS>` is the scoped tier (the ticket's own Verification block plus tests touching its Gate D allowlist paths, never the full suite by default); the full battery runs at integration boundaries only (`<POST_MERGE_CHECKS>` after the last content ticket merges, and at the epic-to-main merge). Tickets with complexity >= 6 or cross-cutting paths may opt into the broader suite at their own merge. Add the same tiering rule in one short paragraph to `references/orchestrator-review-protocol.md` so the two files do not drift.

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

- [ ] `rg -c 'INDEX' skills/ticket-workflow/references/templates.md` returns no matches (exit 1).
- [ ] The epic template AC line contains "local merge".
- [ ] `rg -c 'implementation_plan|r4-archive' skills/ticket-workflow/references/outcome-schema.md` returns no matches (exit 1).
- [ ] The orchestration template preamble contains the re-run hygiene clause (the adopt-and-verify wording).
- [ ] M-step ordering or scoping reflects the FRIC-014 fix in the template text.
- [ ] Both the template and the review protocol name the three gate cost tiers (per-ticket inspection, scoped sanity, integration-boundary full battery) with matching semantics.

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
