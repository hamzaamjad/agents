---
id: CHORE-001
title: "Epic closure: mark done, archive, cleanup"
type: chore
status: to-do
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: [FEAT-001, FEAT-002, FEAT-003, FEAT-004, FEAT-005]
tags: [closure]
agent_created: false
complexity:
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
