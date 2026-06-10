---
id: CHORE-001
title: "Version bump, final verification sweep, epic closure"
type: chore
status: done
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: [FEAT-003, FEAT-004]
tags: [skills, defining-specifications, closure]
agent_created: false
complexity: 3            # rubric: files 3(.20) deps 4(.15) testing 3(.15) risk 3(.15) new/mod 2(.10) crosscut 4(.10) api 1(.05) db 1(.10) = 2.85 → 3
---

# Version bump, final verification sweep, epic closure

## Description

Final ticket, two halves. Finalization (spec SLICE-005): bump the skill version to 1.3 and run the spec's full verification battery on the finished file set. Closure (ticket-workflow "Epic Closure Ticket"): mark everything done, archive the epic folder, delete the orchestration prompt, clean worktree artifacts. Runs on the epic branch before integration to main, so main receives a clean state. Every step must be safe to re-run (guarded operations).

Implements REQ-011, NFR-001..003, AC-008, AC-010 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md`, then the closure protocol from `skills/ticket-workflow/SKILL.md`. The 5-ticket cap folded finalization into closure; keep the two halves in separate commits as described below. No INDEX.md exists in this repo (the templates.md mention does not apply; SKILL.md closure steps govern).

## Tasks

- [x] Set frontmatter `metadata.version` to `"1.3"` in `skills/defining-specifications/SKILL.md`; verify `name` and `description` are byte-identical to v1.2 (commit `19b1989`).
- [x] Run the full battery (spec TEST-001..006) and record results in this ticket's verification log.
- [x] Commit the bump: `EPIC-e164 CHORE-001: bump defining-specifications to v1.3`.
- [x] Mark all sub-tickets and `_epic.md` as `status: done` with `updated` dates (FEAT tickets should already be done via their own mark-done commits; this is the guard pass).
- [x] Archive: `[ -d .tickets/_archive/EPIC-e164_defspec-v13 ] || git mv .tickets/EPIC-e164_defspec-v13 .tickets/_archive/EPIC-e164_defspec-v13`
- [x] Delete orchestration prompt: `[ -f .prompts/orchestration/epic-e164_defspec-v13.md ] && git rm .prompts/orchestration/epic-e164_defspec-v13.md || true`
- [x] Clean worktree artifacts: `[ -d .claude/worktrees/epic-e164 ] && rm -rf .claude/worktrees/epic-e164 || true` — only sub-ticket worktrees under it that are already merged; the orchestrator's own checkout is removed after final integration per SKILL.md post-merge cleanup.
- [x] Single closure commit: `EPIC-e164: archive epic and clean up orchestration artifacts` (includes this ticket's own Outcome block and done status, per the closure protocol's single-commit rule).

## File path hints

- `skills/defining-specifications/SKILL.md` — modify (frontmatter `version` only)
- `.tickets/EPIC-e164_defspec-v13/` — status updates, then `git mv` to `.tickets/_archive/`
- `.prompts/orchestration/epic-e164_defspec-v13.md` — `git rm`

## Constraints

- Do NOT change any content line of `SKILL.md` other than the frontmatter `version` value.
- Do NOT modify files under `.tickets/_archive/` other than the incoming move itself.
- Do NOT touch other epics' worktrees or branches (none exist today; rule stands).

## Acceptance criteria

- [x] AC-008: frontmatter shows `version: "1.3"`; `name` and `description` byte-identical to v1.2.
- [x] AC-010: full battery passes — `wc -l` ≤ 300; every new/modified section under ~40 lines; validator reports 0 high / 0 medium / ≤ 6 low; `evals.json` parses with eval-1 pointing at an existing fixture.
- [x] All six ticket files (epic + 5 subs) show `status: done`.
- [x] Epic directory exists only under `.tickets/_archive/`; orchestration prompt deleted; closure commit message matches the prescribed format.

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

## Verification log (2026-06-10)

- AC-008: `version: "1.3"` at SKILL.md:6; `diff` of frontmatter lines 2-3 vs commit 19b1989 → `name+description identical`
- AC-010 battery: `wc -l` → 246 (TEST-001); composite structural check → `TEST-002 composite ok (example 20 lines)`; validator → 0 high / 0 medium / 6 low (TEST-005); eval-1 files → fixture path, `fixture exists` (TEST-004); purity verified at FEAT-004 (TEST-003); version grep (TEST-006)
- Bump commit f211930 (dedicated, before closure commit)
- Closure: all 6 ticket files `status: done`; epic dir moved via guarded `git mv`; orchestration prompt removed via guarded `git rm`; worktree-cleanup guard confirmed no-op from this worktree (nested checkout path absent here — actual orchestrator-worktree removal happens post-integration per SKILL.md)
- Actual tool rounds: 6 batched rounds (9 repo-acting tool calls) vs complexity 3 — in line

## Outcome

**Summary:** Finalized and closed EPIC-e164: bumped `defining-specifications` to v1.3 (trigger surface byte-identical to v1.2), ran the spec's full verification battery green (246/300 lines, structural checks, validator baseline, eval wiring), marked all six tickets done, archived the epic folder to `.tickets/_archive/`, and deleted the orchestration prompt. Main receives a clean state via the epic branch merge that follows this commit.

**Key decisions:**
- Finalization (version bump + battery) folded into the closure CHORE under the 5-ticket cap — kept in a dedicated commit (f211930) so content and cleanup stay separable.
- Epic AC "integrated to main" left annotated rather than pre-checked — integration happens after closure by design.

**Constraints & invariants discovered (keep):**
- Closure's worktree-cleanup step is a guarded no-op when run from a nested sub-ticket worktree; orchestrator removes its own checkout only after final integration.
- Battery greps must scope to sections now that the worked example contains REQ/DEC/Q tokens.

**Implementation notes (high signal only):**
- Touch points: SKILL.md frontmatter; all `.tickets/EPIC-e164_defspec-v13/` files; `.prompts/orchestration/epic-e164_defspec-v13.md`
- Pattern: idempotent closure — every step guarded for safe re-run

**Verification:**
- AC-008 diff vs 19b1989 → identical; battery → all green (see log above)
- post-mv: `rg -l 'status: done' .tickets/_archive/EPIC-e164_defspec-v13/ | wc -l` → 6; active dir and prompt absent

**Risk / regression surface:**
- Archive is read-only from here; future edits to archived tickets are protocol violations.

**Retrieval tags:** EPIC-e164, closure, archive, v1.3 bump, verification battery, guarded git mv, orchestration prompt deletion, defining-specifications
