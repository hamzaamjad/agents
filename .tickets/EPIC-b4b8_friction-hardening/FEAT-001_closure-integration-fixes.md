---
id: FEAT-001
title: "ticket-workflow SKILL.md: closure and integration protocol fixes"
type: feature
status: done
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: []
tags: [friction-log]
agent_created: false
complexity: 3
---

# ticket-workflow SKILL.md: closure and integration protocol fixes

## Context

EPIC-e164 execution hit five closure/integration defects, all logged in
`.prompts/exercises/02-friction-log.md` (FRIC-009, 012, 013, 015, 018). Each fix below
lands in `skills/ticket-workflow/SKILL.md` and must preserve the section's existing
moderate tone and structure.

## Requirements

- [ ] FRIC-018: closure step 2's guarded `git mv` snippet gains `mkdir -p .tickets/_archive` as its first line — a repo's first-ever epic archive currently fails ("No such file or directory").
- [ ] FRIC-013: § Epic Branch Workflow documents the completion variant for repos without a pushable remote: local `git merge --no-ff <epic-branch>` run from the primary clone is the sanctioned PR substitute, and names it as the one exception to "never cd to the primary clone".
- [ ] FRIC-009: § Epic Closure Ticket states whether the closure ticket may carry small finalization work (version bumps, sweeps) in a separate commit before the closure commit, and that the closure ticket does not count toward decomposition caps imposed by briefs.
- [ ] FRIC-012: closure step 4 names its execution context — the guard is a no-op from nested sub-ticket worktrees; authoritative worktree cleanup happens in the post-merge orchestrator block.
- [ ] FRIC-015: the post-merge cleanup block states where branch deletion runs: from the epic worktree (whose HEAD contains the merge), or use `git branch -D` only after verifying the merge commit is on the epic branch.

## File path hints

- `skills/ticket-workflow/SKILL.md` — modify §§ Epic Branch Workflow, Epic Closure Ticket, post-merge cleanup block

## Constraints

- Do NOT edit any file other than `skills/ticket-workflow/SKILL.md`.
- Do NOT restructure sections or renumber steps beyond the listed additions.
- Keep SKILL.md at or under 270 lines (currently 241); move overflow to `references/` only if a requirement cannot fit.
- Use moderate imperative phrasing; no all-caps directives in new text.

## Acceptance criteria

- [ ] `rg -c 'mkdir -p \.tickets/_archive' skills/ticket-workflow/SKILL.md` returns at least 1, and the line sits inside the closure step 2 snippet.
- [ ] § Epic Branch Workflow contains a local-merge completion variant naming both `--no-ff` and where the merge runs.
- [ ] §§ Epic Closure Ticket covers FRIC-009 and FRIC-012 rules in prose adjacent to the steps they amend.
- [ ] The post-merge cleanup block names the execution location for branch deletion.
- [ ] `wc -l skills/ticket-workflow/SKILL.md` reports 270 or fewer lines.

## Verification

```bash
rg -n 'mkdir -p \.tickets/_archive' skills/ticket-workflow/SKILL.md
rg -n -i 'no-ff' skills/ticket-workflow/SKILL.md
rg -n -i 'primary clone' skills/ticket-workflow/SKILL.md
wc -l skills/ticket-workflow/SKILL.md | awk '{exit ($1>270)}'
python3 skills/engineering-context/scripts/validate_context.py . | tail -1
```

## Notes

Friction sources: `.prompts/exercises/02-friction-log.md` §§ Phase B-C. EPIC-e164's
closure ticket worked around FRIC-018 with the same `mkdir -p` — this ticket makes the
workaround canonical.

## Outcome

**Summary:** Hardened the ticket-workflow closure and integration protocol in `skills/ticket-workflow/SKILL.md`, resolving five friction-log defects (FRIC-009, 012, 013, 015, 018) from EPIC-e164. The file gained 7 lines (241 → 247, under the 270 cap) with no section restructuring or step renumbering.

**Key decisions:**
- Documented the local `git merge --no-ff` from the primary clone as the sanctioned PR substitute — named explicitly as the one exception to "never cd to the primary clone".
- Kept closure step 4 as best-effort and pointed to the post-merge orchestrator block as authoritative — avoids renumbering or deleting the step.

**Constraints & invariants discovered (keep):**
- `git mv` into `.tickets/_archive/` requires the parent directory to exist; always `mkdir -p` first.
- `git branch -d` only succeeds where HEAD reaches the merge commit; run from the epic worktree or verify before `-D`.

**Implementation notes (high signal only):**
- Touch points: `skills/ticket-workflow/SKILL.md` §§ Epic Branch Workflow, Epic Closure Ticket, post-merge cleanup block
- Pattern: prose amendments adjacent to the steps they qualify; one-line snippet prepend
- Actual tool-round count: 7 meaningful rounds (vs complexity 3)

**Verification:**
- `rg -n 'mkdir -p \.tickets/_archive' skills/ticket-workflow/SKILL.md` → line 199, inside closure step 2 snippet
- `wc -l skills/ticket-workflow/SKILL.md | awk '{exit ($1>270)}'` → exit 0 (247 lines)
- `python3 skills/engineering-context/scripts/validate_context.py . | tail -1` → 0 high, 0 medium, 10 low

**Risk / regression surface:**
- New prose must not drift from `references/orchestration-template.md` cleanup ordering; the post-merge block is now the named authority for worktree cleanup.

**Retrieval tags:** ticket-workflow, closure, archive, mkdir -p .tickets/_archive, git merge --no-ff, primary clone exception, git branch -d, worktree cleanup, FRIC-009, FRIC-018
