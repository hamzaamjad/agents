---
id: FEAT-004
title: "validate_context.py: tone false-positives, worktree skip, skill-reference scan"
type: feature
status: done
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-b4b8
dependencies: []
tags: [friction-log, audit-next-pass]
agent_created: false
complexity: 5
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

- [x] Tone heuristic ignores all-caps tokens that are filenames, code spans (backticked), or a small allowlist of technical tokens; genuine all-caps directives ("NEVER do X") still fire.
- [x] Directory walk skips `.claude/worktrees/` (and any path containing a nested `.git` file marker, which is how worktree checkouts present).
- [x] New check: for every `skills/*/SKILL.md` and `skills/*/references/*.md`, each relative markdown link and each backticked relative path that looks like an intra-repo file reference must resolve from the containing file's directory; unresolved references report as MEDIUM `dangling_reference`.
- [x] The new check tolerates placeholders (paths containing `<`, `*`, or `{`) without flagging them.

## File path hints

- `skills/engineering-context/scripts/validate_context.py` — modify

## Constraints

- Do NOT change the output format (severity tags, summary line) — downstream verification commands parse it.
- Do NOT add third-party dependencies; stdlib only.
- Do NOT weaken existing checks; this ticket only removes false positives and adds detection.

## Acceptance criteria

- [x] `python3 skills/engineering-context/scripts/validate_context.py .` on this repo reports 0 high, 0 medium, 0 low (run after FEAT-001..003 land or explain residuals in the Outcome block).
- [x] A temp fixture with a SKILL.md linking `references/missing.md` yields a MEDIUM `dangling_reference` finding.
- [x] A temp fixture containing `.claude/worktrees/<x>/AGENTS.md` with planted issues yields no findings from under that path.
- [x] A planted `NEVER use this` directive in a fixture AGENTS.md still fires the tone check.

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

## Outcome

**Summary:** Reworked `validate_context.py` to eliminate tone false positives (filenames, backticked tokens, technical all-caps allowlist), skip `.claude/worktrees/` and any directory carrying a `.git` file marker, and add a MEDIUM `dangling_reference` check over `skills/*/SKILL.md` and `skills/*/references/*.md`. Output format and existing checks unchanged; repo scan now reads `0 high, 4 medium, 0 low` — the 4 mediums are genuine dangling references the new check surfaced (not fixed here; out of allowlist).

**Key decisions:**
- All-caps tone case moved out of `TONE_PATTERNS` into dedicated logic — allows filename/allowlist/code-span exclusion without touching other patterns.
- Dangling check resolves from file dir *or* repo root, and backticked tokens only count with skill-convention prefixes (`./`, `../`, `references/`, `scripts/`, `skills/`) — bare paths like `origin/main` or `src/foo.ts` are illustrative, not links.

**Constraints & invariants discovered (keep):**
- Summary line format (`Summary: N high, N medium, N low`) is parsed downstream; never change it.
- A `.git` *file* (vs directory) marks a worktree checkout; pruning on that marker generalizes beyond `.claude/worktrees/`.

**Implementation notes (high signal only):**
- Touch points: `skills/engineering-context/scripts/validate_context.py` (`CAPS_ALLOWLIST`, `keep_dir`, `check_tone`, `check_dangling_references`)
- Pattern: prune-on-walk + two-base path resolution with placeholder tolerance (`<`, `*`, `{`)

**Verification:**
- `python3 skills/engineering-context/scripts/validate_context.py .` → `Summary: 0 high, 4 medium, 0 low` (mediums = real dangling refs, listed below)
- mktemp fixture (SKILL.md → `references/missing.md`; planted worktree AGENTS.md; `NEVER use this` at root) → 1 MEDIUM dangling_reference, 1 LOW tone, zero findings from under `.claude/worktrees/`
- `.git`-file-marker fixture + `--format json` → `All checks passed.` / `{'high': 0, 'medium': 0, 'low': 0}`

**Risk / regression surface:**
- Tone allowlist could mask a genuinely aggressive line built solely from allowlisted tokens; other tone patterns still guard the worst phrasing.
- Dangling refs surfaced (report, not fixed): `engineering-context/references/context-design-patterns.md:51-52` (`references/testing.md`, `references/security.md` — example listings), `ticket-workflow/references/orchestrator-review-protocol.md:95` (`references/templates.md` — sibling ref written skill-root-relative), `ticket-workflow/references/outcome-schema.md:87` (`scripts/archive-search.sh` — consuming-repo script).

**Retrieval tags:** validate_context.py, dangling_reference, tone_overtrigger, CAPS_ALLOWLIST, worktree skip, .git file marker, FRIC-004, FRIC-014, audit next-pass #5, placeholder tolerance

Tool rounds: 11.
