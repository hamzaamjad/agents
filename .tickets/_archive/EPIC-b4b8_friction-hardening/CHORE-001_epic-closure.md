---
id: CHORE-001
title: "Epic closure: mark done, archive, cleanup"
type: chore
status: done
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: [FEAT-001, FEAT-002, FEAT-003, FEAT-004, FEAT-005]
tags: [closure]
agent_created: false
complexity: 1
---

# Epic closure: mark done, archive, cleanup

## Description

Mandatory closure ticket per SKILL.md § Epic Closure Ticket. Runs on the epic branch
after all FEAT tickets merge; carries no content work (FRIC-009 lesson from EPIC-e164).
Every step is re-run-safe: check existence before acting.

## Tasks

- [ ] Set `status: done` and `updated` date on all sub-tickets and `_epic.md`; update the epic's sub-ticket table.
- [ ] Archive: `mkdir -p .tickets/_archive` then the guarded `git mv .tickets/EPIC-b4b8_friction-hardening .tickets/_archive/EPIC-b4b8_friction-hardening`.
- [ ] Delete orchestration prompt: guarded `git rm .prompts/orchestration/epic-b4b8_*.md`.
- [ ] Clean worktree artifacts: guarded `rm -rf .claude/worktrees/epic-b4b8` (no-op from a nested worktree; authoritative cleanup is the post-merge orchestrator block).
- [ ] Single commit: `EPIC-b4b8: archive epic and clean up orchestration artifacts`.

## File path hints

- `.tickets/EPIC-b4b8_friction-hardening/` — git mv to `_archive/`
- `.prompts/orchestration/epic-b4b8_friction-hardening.md` — git rm

## Constraints

- Do NOT modify files under `.tickets/_archive/` other than the incoming move.
- Do NOT update INDEX.md — no such file exists in this repo (FRIC-010).
- Do NOT carry implementation work; closure only.

## Acceptance criteria

- [ ] All eight ticket files (`_epic.md` + 5 FEAT + TASK-001 + this CHORE) live under `.tickets/_archive/EPIC-b4b8_friction-hardening/` with frontmatter `status: done`.
- [ ] No `epic-b4b8_*.md` remains under `.prompts/orchestration/`.
- [ ] The closure commit is a single commit with the prescribed message.

## Verification

```bash
# Frontmatter-scoped status check: ticket bodies legitimately contain the literal
# "status: blocked" (FEAT-002 prose), so only the first status line per file counts.
ls .tickets/_archive/EPIC-b4b8_friction-hardening/ | wc -l | awk '{exit ($1!=8)}'
for f in .tickets/_archive/EPIC-b4b8_friction-hardening/*.md; do awk '/^status:/{print $2; exit}' "$f"; done | rg -v '^done$'; test $? -eq 1
ls .prompts/orchestration/epic-b4b8_*.md 2>/dev/null; test $? -ne 0
git log -1 --format=%s | rg -q 'EPIC-b4b8: archive epic'
```

## Notes

After the epic merges to main, the orchestrator (not this ticket) removes this epic's
worktrees and deletes branches from the epic worktree per SKILL.md post-merge cleanup.

## Outcome

> Summary: Closed EPIC-b4b8 on the epic branch: all eight tickets marked done, epic folder archived to `.tickets/_archive/`, orchestration prompt deleted. Executed directly by the orchestrator (mechanical closure, no content work, per FRIC-009 separation).

> Key decisions:
> - Archive count amended 7 → 8 before execution — corrective TASK-001 was created mid-epic by the FEAT-004 review; the stale count would have failed verification by construction (FRIC-017 dry-run rule applied).
> - Worktree-artifact rm step left as guarded no-op — closure ran from the epic worktree itself; authoritative cleanup is the post-merge orchestrator block.

> Constraints & invariants discovered (keep):
> - Closure verification commands that hard-code ticket counts must be re-checked whenever corrective sub-tickets are added mid-epic.
> - Frontmatter status checks must scope to the first `status:` line per file — ticket bodies can contain literal `status: blocked` prose.

> Implementation notes (high signal only):
> - Touch points: `.tickets/_archive/EPIC-b4b8_friction-hardening/`, `.prompts/orchestration/`
> - Pattern: guarded `mkdir -p` + `git mv` + `git rm`, single closure commit.

> Verification:
> - archive ls count = 8 → pass; per-file first `status:` all `done` → pass
> - no `epic-b4b8_*.md` under `.prompts/orchestration/` → pass

> Risk / regression surface:
> - None to runtime content; archive is read-only by convention.

> Retrieval tags: EPIC-b4b8, closure, archive, friction-hardening, TASK-001, FRIC-009, FRIC-017, orchestration prompt

Tool rounds: 6 (orchestrator-executed).
