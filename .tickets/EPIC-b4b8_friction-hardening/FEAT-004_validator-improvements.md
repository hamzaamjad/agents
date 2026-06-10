---
id: FEAT-004
title: "validate_context.py: tone false-positives, worktree skip, skill-reference scan"
type: feature
status: to-do
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: []
tags: [friction-log, audit-next-pass]
agent_created: false
complexity:
---

# validate_context.py: tone false-positives, worktree skip, skill-reference scan

## Context

Three systemic gaps in `skills/engineering-context/scripts/validate_context.py`:

1. FRIC-004: the `[A-Z]{4,}` tone heuristic flags canonical filenames and tokens
   (AGENTS.md, SKILL.md, CLAUDE.md, PATH, JSON, YAML, CHECKPOINT) as "aggressive tone" —
   currently 10 false-positive LOWs on this repo's AGENTS.md, forcing every downstream
   gate to hand-carry a known-findings baseline.
2. FRIC-014: repo scans descend into `.claude/worktrees/`, double-counting nested
   checkouts (observed: 0/9/12 with a worktree present vs 0/0/6 baseline).
3. Audit next-pass #5 (`docs/audits/2026-06-10-instruction-layer-audit.md`): the script
   scans only AGENTS.md-class files, so dangling relative references inside
   `skills/*/SKILL.md` — the failure class behind audit findings 1-3 — are invisible.
   The audit's AC5 link sweep is the prototype.

## Requirements

- [ ] Tone heuristic ignores all-caps tokens that are filenames, code spans (backticked), or a small allowlist of technical tokens; genuine all-caps directives ("NEVER do X") still fire.
- [ ] Directory walk skips `.claude/worktrees/` (and any path containing a nested `.git` file marker, which is how worktree checkouts present).
- [ ] New check: for every `skills/*/SKILL.md` and `skills/*/references/*.md`, each relative markdown link and each backticked relative path that looks like an intra-repo file reference must resolve from the containing file's directory; unresolved references report as MEDIUM `dangling_reference`.
- [ ] The new check tolerates placeholders (paths containing `<`, `*`, or `{`) without flagging them.

## File path hints

- `skills/engineering-context/scripts/validate_context.py` — modify

## Constraints

- Do NOT change the output format (severity tags, summary line) — downstream verification commands parse it.
- Do NOT add third-party dependencies; stdlib only.
- Do NOT weaken existing checks; this ticket only removes false positives and adds detection.

## Acceptance criteria

- [ ] `python3 skills/engineering-context/scripts/validate_context.py .` on this repo reports 0 high, 0 medium, 0 low (run after FEAT-001..003 land or explain residuals in the Outcome block).
- [ ] A temp fixture with a SKILL.md linking `references/missing.md` yields a MEDIUM `dangling_reference` finding.
- [ ] A temp fixture containing `.claude/worktrees/<x>/AGENTS.md` with planted issues yields no findings from under that path.
- [ ] A planted `NEVER use this` directive in a fixture AGENTS.md still fires the tone check.

## Verification

```bash
python3 skills/engineering-context/scripts/validate_context.py . | tail -1
# fixture checks: build under mktemp -d, run script against fixture root, assert findings
# (dry-run the exact fixture commands while authoring the implementation; record them in the log)
```

## Notes

Severity choice (MEDIUM for dangling references) mirrors the audit's classification of
findings 1-3. Keep the heuristic changes small and documented inline — this script is
itself instruction-adjacent content.
