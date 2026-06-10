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

## File path hints

- `skills/ticket-workflow/references/templates.md` — modify (epic template only)
- `skills/ticket-workflow/references/outcome-schema.md` — modify (provenance wording only)
- `skills/ticket-workflow/references/orchestration-template.md` — modify (preamble + M-steps)

## Constraints

- Do NOT edit SKILL.md or any file outside the three named reference files.
- Do NOT change template placeholder names (`<EPIC_BRANCH>`, `<MAX_FIX_CYCLES>`, ...) — per-epic instances depend on them.
- Keep `orchestration-template.md` consistent with `orchestrator-review-protocol.md`; if the M-step reorder requires touching the protocol file, stop and report per Step 2 rather than editing it.

## Acceptance criteria

- [ ] `rg -c 'INDEX' skills/ticket-workflow/references/templates.md` returns no matches (exit 1).
- [ ] The epic template AC line contains "local merge".
- [ ] `rg -c 'implementation_plan|r4-archive' skills/ticket-workflow/references/outcome-schema.md` returns no matches (exit 1).
- [ ] The orchestration template preamble contains the re-run hygiene clause (the adopt-and-verify wording).
- [ ] M-step ordering or scoping reflects the FRIC-014 fix in the template text.

## Verification

```bash
# "adopt" discriminates (absent today); a bare "re-run" grep would not — Gate B
# already says "re-run once".
rg -n 'INDEX' skills/ticket-workflow/references/templates.md; test $? -eq 1
rg -n 'local merge' skills/ticket-workflow/references/templates.md
rg -n 'implementation_plan|r4-archive' skills/ticket-workflow/references/outcome-schema.md; test $? -eq 1
rg -n -i 'adopt' skills/ticket-workflow/references/orchestration-template.md
python3 skills/engineering-context/scripts/validate_context.py . | tail -1
```

## Notes

EPIC-e164 instantiated its orchestration prompt with the M2/M4 hazard live: the first
post-merge sanity scan reported 9 phantom mediums until the nested worktree was removed.
