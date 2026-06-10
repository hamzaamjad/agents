---
id: CHORE-001
title: "Epic closure: archive EPIC-e55b and clean up orchestration artifacts"
type: chore
status: to-do
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e55b
dependencies: [FEAT-001, FEAT-002, FEAT-003, FEAT-004]
tags: [linkcheck, closure]
agent_created: true
complexity: 2
---

# Epic closure: archive EPIC-e55b and clean up orchestration artifacts

## Description

Final ticket of EPIC-e55b — always merges last. Runs on the epic branch
`epic/e55b/link-checker` before the merge to main, so main receives a clean state.
Every step is guarded so a partial re-run is a no-op, never a failure.

## Tasks

- [ ] Set `status: done` and `updated: <today>` in the frontmatter of all EPIC-e55b
      sub-tickets and `_epic.md`; sync the epic's Sub-tickets table to `done`.
- [ ] Archive the epic folder (guarded):
      `mkdir -p .tickets/_archive && { [ -d .tickets/_archive/EPIC-e55b_link-checker ] || git mv .tickets/EPIC-e55b_link-checker .tickets/_archive/EPIC-e55b_link-checker; }`
- [ ] Delete the orchestration prompt (guarded):
      `[ -f .prompts/orchestration/epic-e55b_link-checker.md ] && git rm .prompts/orchestration/epic-e55b_link-checker.md || true`
- [ ] Clean up worktree artifacts (guarded):
      `[ -d .claude/worktrees/epic-e55b ] && rm -rf .claude/worktrees/epic-e55b || true`
      (sub-ticket worktrees should already be removed by the orchestrator after each merge)
- [ ] Single commit: `EPIC-e55b: archive epic and clean up orchestration artifacts`.

## File path hints

- `.tickets/EPIC-e55b_link-checker/` — modify statuses, then `git mv` to `.tickets/_archive/`
- `.prompts/orchestration/epic-e55b_link-checker.md` — delete
- `.claude/worktrees/epic-e55b/` — remove from disk (untracked; not part of the commit)

## Constraints

- Do NOT modify any source code, tests, or CI files — metadata and cleanup only.
- Do NOT touch other epics' worktrees or anything under `.tickets/_archive/` besides
  adding this epic's folder.
- Do NOT merge to main inside this ticket — the orchestrator handles the final merge
  after this ticket lands on the epic branch.

## Acceptance criteria

- [ ] All EPIC-e55b tickets (including `_epic.md`) have `status: done` and live under
      `.tickets/_archive/EPIC-e55b_link-checker/`.
- [ ] `.prompts/orchestration/epic-e55b_link-checker.md` is deleted from the epic branch.
- [ ] `python3 -m pytest tests/ -q` still passes on the epic branch after cleanup.

## Verification

```bash
test -f .tickets/_archive/EPIC-e55b_link-checker/_epic.md && echo "archived"
test ! -e .tickets/EPIC-e55b_link-checker && echo "active dir gone"
test ! -f .prompts/orchestration/epic-e55b_link-checker.md && echo "prompt deleted"
grep -L "status: done" .tickets/_archive/EPIC-e55b_link-checker/*.md; echo "(no output above = all done)"
python3 -m pytest tests/ -q
```

## Notes

Recovery: if closure crashes partway, re-run from the top — every step checks
existence first (SKILL.md "Epic Closure Ticket"; Goal A safe default).
