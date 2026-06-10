---
id: FEAT-002
title: "ticket-workflow SKILL.md: creation and execution guidance fixes"
type: feature
status: to-do
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: [FEAT-001]
tags: [friction-log, benchmark-foldback]
agent_created: false
complexity:
---

# ticket-workflow SKILL.md: creation and execution guidance fixes

## Context

Three friction entries (FRIC-008, 014, 017 in `.prompts/exercises/02-friction-log.md`)
plus two skill gaps surfaced by the iteration-1 benchmark
(`evals/ticket-workflow/iteration-1/benchmark.md`, "skill gaps to fold back") all target
`skills/ticket-workflow/SKILL.md`. Depends on FEAT-001 because both edit the same file.

## Requirements

- [ ] FRIC-008: § Naming states that sub-ticket numbering is sequential per type prefix within its scope (FEAT-001..N and CHORE-001..N coexist), matching the ID-assignment command's per-prefix dedupe semantics.
- [ ] FRIC-017: § Quality Rules adds: dry-run each verification command against a sketch of the expected artifact before committing the ticket — a command that cannot pass by construction is a ticket defect, not an execution defect.
- [ ] FRIC-014: § Worktree Rules notes that nested sub-ticket worktrees sit inside the orchestrator worktree, so tree-scanning checks run before worktree cleanup double-count them; scanning verification runs after cleanup or scopes out `.claude/worktrees/`.
- [ ] Benchmark fold-back: Execution Protocol Step 2 says how to record a blocker durably — set `status: blocked` in frontmatter and append a one-line note naming the unmet dependency — not just report it conversationally.
- [ ] Benchmark fold-back: Execution Protocol Step 6 defines the minimal verification-log format: one line per command — command, pass/fail, and the actual tool-round count recorded once at the end.

## File path hints

- `skills/ticket-workflow/SKILL.md` — modify §§ Naming, Worktree Rules, Execution Protocol Steps 2 and 6, Quality Rules

## Constraints

- Do NOT edit any file other than `skills/ticket-workflow/SKILL.md`.
- Do NOT change the status lifecycle vocabulary (`to-do`, `in-progress`, `done`, `blocked`).
- Keep SKILL.md at or under 280 lines after this ticket; prefer one-sentence additions.
- Use moderate imperative phrasing; no all-caps directives in new text.

## Acceptance criteria

- [ ] § Naming names per-prefix numbering explicitly.
- [ ] § Quality Rules contains the dry-run rule with the word "sketch" or equivalent concrete phrasing.
- [ ] § Worktree Rules mentions the nested-worktree scanning hazard.
- [ ] Step 2 instructs setting `status: blocked` with a note naming the unmet dependency; Step 6 defines the per-command log line format.
- [ ] `wc -l skills/ticket-workflow/SKILL.md` reports 280 or fewer lines.

## Verification

```bash
rg -n -i 'per.type prefix|per.prefix' skills/ticket-workflow/SKILL.md
rg -n -i 'dry.run' skills/ticket-workflow/SKILL.md
rg -n 'status: blocked' skills/ticket-workflow/SKILL.md
wc -l skills/ticket-workflow/SKILL.md | awk '{exit ($1>280)}'
python3 skills/engineering-context/scripts/validate_context.py . | tail -1
```

## Notes

The benchmark found the baseline arm recorded blockers better than the skill arm — the
skill says "STOP and report" but never says where the record lives. That gap is the
highest-value fold-back here.
