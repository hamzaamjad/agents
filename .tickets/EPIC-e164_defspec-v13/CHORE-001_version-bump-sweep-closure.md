---
id: CHORE-001
title: "Version bump, final verification sweep, epic closure"
type: chore
status: to-do
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: [FEAT-003, FEAT-004]
tags: [skills, defining-specifications, closure]
agent_created: false
complexity:              # populate at execution Step 3 per references/complexity-scoring.md
---

# Version bump, final verification sweep, epic closure

## Description

Final ticket, two halves. Finalization (spec SLICE-005): bump the skill version to 1.3 and run the spec's full verification battery on the finished file set. Closure (ticket-workflow "Epic Closure Ticket"): mark everything done, archive the epic folder, delete the orchestration prompt, clean worktree artifacts. Runs on the epic branch before integration to main, so main receives a clean state. Every step must be safe to re-run (guarded operations).

Implements REQ-011, NFR-001..003, AC-008, AC-010 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`, then the closure protocol from `skills/ticket-workflow/SKILL.md`. The 5-ticket cap folded finalization into closure; keep the two halves in separate commits as described below. No INDEX.md exists in this repo (the templates.md mention does not apply; SKILL.md closure steps govern).

## Tasks

- [ ] Set frontmatter `metadata.version` to `"1.3"` in `skills/defining-specifications/SKILL.md`; verify `name` and `description` are byte-identical to v1.2 (commit `19b1989`).
- [ ] Run the full battery (spec TEST-001..006) and record results in this ticket's verification log.
- [ ] Commit the bump: `EPIC-e164 CHORE-001: bump defining-specifications to v1.3`.
- [ ] Mark all sub-tickets and `_epic.md` as `status: done` with `updated` dates (FEAT tickets should already be done via their own mark-done commits; this is the guard pass).
- [ ] Archive: `[ -d .tickets/_archive/EPIC-e164_defspec-v13 ] || git mv .tickets/EPIC-e164_defspec-v13 .tickets/_archive/EPIC-e164_defspec-v13`
- [ ] Delete orchestration prompt: `[ -f .prompts/orchestration/epic-e164_defspec-v13.md ] && git rm .prompts/orchestration/epic-e164_defspec-v13.md || true`
- [ ] Clean worktree artifacts: `[ -d .claude/worktrees/epic-e164 ] && rm -rf .claude/worktrees/epic-e164 || true` — only sub-ticket worktrees under it that are already merged; the orchestrator's own checkout is removed after final integration per SKILL.md post-merge cleanup.
- [ ] Single closure commit: `EPIC-e164: archive epic and clean up orchestration artifacts` (includes this ticket's own Outcome block and done status, per the closure protocol's single-commit rule).

## File path hints

- `skills/defining-specifications/SKILL.md` — modify (frontmatter `version` only)
- `.tickets/EPIC-e164_defspec-v13/` — status updates, then `git mv` to `.tickets/_archive/`
- `.prompts/orchestration/epic-e164_defspec-v13.md` — `git rm`

## Constraints

- Do NOT change any content line of `SKILL.md` other than the frontmatter `version` value.
- Do NOT modify files under `.tickets/_archive/` other than the incoming move itself.
- Do NOT touch other epics' worktrees or branches (none exist today; rule stands).

## Acceptance criteria

- [ ] AC-008: frontmatter shows `version: "1.3"`; `name` and `description` byte-identical to v1.2.
- [ ] AC-010: full battery passes — `wc -l` ≤ 300; every new/modified section under ~40 lines; validator reports 0 high / 0 medium / ≤ 6 low; `evals.json` parses with eval-1 pointing at an existing fixture.
- [ ] All six ticket files (epic + 5 subs) show `status: done`.
- [ ] Epic directory exists only under `.tickets/_archive/`; orchestration prompt deleted; closure commit message matches the prescribed format.

## Verification

```bash
# AC-008: version bumped, trigger surface untouched
rg -n 'version: "1.3"' skills/defining-specifications/SKILL.md
diff <(git show 19b1989:skills/defining-specifications/SKILL.md | sed -n '2,3p') \
     <(sed -n '2,3p' skills/defining-specifications/SKILL.md) && echo 'name+description identical'
# AC-010: full battery (spec TEST-001..006)
wc -l skills/defining-specifications/SKILL.md
python3 skills/engineering-context/scripts/validate_context.py .
python3 -c "import json; d=json.load(open('skills/defining-specifications/evals/evals.json')); e=[x for x in d['evals'] if x['id']==1][0]; print(e['files'])"
FIX=$(python3 -c "import json; print(json.load(open('skills/defining-specifications/evals/evals.json'))['evals'][1]['files'][0])"); test -f "$FIX" && echo 'fixture exists'
# Closure state
rg -l 'status: done' .tickets/_archive/EPIC-e164_defspec-v13/ | wc -l   # expect 6
test ! -d .tickets/EPIC-e164_defspec-v13 && echo 'active dir gone'
test ! -f .prompts/orchestration/epic-e164_defspec-v13.md && echo 'prompt gone'
git log --oneline -3
```

## Notes

Closure recovery, if this crashes partway: `skills/ticket-workflow/references/worktree-recovery.md` § Closure ticket partial execution (Goal A default). Spec: AC-008/AC-010, NFR-001..003, REQ-011.
