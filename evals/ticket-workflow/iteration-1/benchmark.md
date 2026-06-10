# Benchmark Summary: ticket-workflow iteration 1

## Result

- `with_skill`: 32/32 assertions passed; per-eval mean pass rate 100%.
- `without_skill`: 15/32 assertions passed; per-eval mean pass rate 47.3% (pooled 46.9%).
- Delta: **+52.7 percentage points** for the skill (per-eval mean), the largest delta measured in this workspace's eval program to date (defining-specifications iteration 3 was +23.3pp).
- Timing/token metrics were unavailable from subagent completion notifications; this benchmark compares output quality only.

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass rate (per-eval mean) | 100% ± 0% | 47% ± 25% | +0.53 |

Per-eval:

| Eval | With | Without | Delta |
|------|------|---------|-------|
| 0 standalone-ticket-creation (10 assertions) | 10/10 | 6/10 | +0.40 |
| 1 ticket-execution-dependency-gate (11) | 11/11 | 7/11 | +0.36 |
| 2 epic-creation-decomposition (11) | 11/11 | 2/11 | +0.82 |

## Which assertions discriminate (baseline fails, with-skill passes) — 17 of 32

- **Eval 0 (4):** valid lifecycle status (`to-do` — baseline invented `open`); `## Verification` with runnable commands; ≤5 acceptance criteria; `## Constraints` section.
- **Eval 1 (4):** `complexity` populated; `## Outcome` appended; Outcome's 7 schema subsections in canonical order; dedicated mark-done commit separate from implementation.
- **Eval 2 (9):** 4-char hex epic ID; `_epic.md` entry point; `branch` frontmatter + real epic branch; ticket work on the epic branch rather than directly on main; worktree usage; `parent` frontmatter key; merge-order section; closure CHORE last in merge order; instantiated orchestration prompt under `.prompts/orchestration/`.

The pattern: the skill's measurable value is **convention conformance** — naming, lifecycle vocabulary, template sections, the Outcome retrieval surface, commit discipline, and the entire epic scaffolding protocol. None of it was reproduced by a strong baseline.

## Trivially passed by both arms — 15 of 32

Scope discipline (no implementation when asked for tickets; changes confined to hinted files), basic file placement, required frontmatter presence, honoring explicitly declared dependencies, post-hoc test passes, and commit hygiene against planted decoy files (`git add -A` bait was never taken by either arm — 0/3 fixtures). These measure baseline competence, not the skill; they stay as regression floor.

Notable single-run luck: eval 0's per-type numbering assertion (FEAT-001 next to BUG-001) passed in the baseline because it independently reasoned per-type scoping from one example. Treat as flaky until re-tested.

## Confounded or judge-dependent

- **Eval 1 dependency hard-stop (assertions 1–3) did not discriminate**: the fixture declared the dependency in frontmatter and reinforced it in ticket constraints, so a capable baseline honored it without the skill. The gate as designed measures metadata-following, not the skill's resolution rules.
- **Two judge-lite assertions (eval 1 #2, #11)** read the agent's final report (blocker reported; verification run during execution). Both passed both arms; both were anchored to artifacts where possible. Caveats (verbosity bias, self-preference, demonstrated run-report unreliability) are recorded in the grading.json files.
- **Eval 2 #7 (dependency resolution)** passed in the baseline under self-invented field names (`depends_on`/`blocks`); it was graded on reference resolution while the field-name deviation was charged to assertion 6. Defensible but worth splitting more cleanly next time.
- **Isolation confound (environment-level):** arms ran as host subagents, so the workspace AGENTS.md and skill descriptions were visible in their system context despite prompt prohibitions. Baseline outputs show zero skill vocabulary, so no material leakage occurred, but a CLI-isolated harness would remove the confound entirely.
- **Run-report unreliability:** in 4 of 6 runs the final narrative diverged from committed artifacts (phantom "Out of scope" section; claimed-but-absent `complexity: 2`; wrong filenames in both eval-2 reports). All grading was artifact-based; self-report-based grading would have mis-scored at least 3 assertions.

## Skill gaps surfaced by the with-skill runs

- **Blocked-status durability:** SKILL.md Step 2 says "STOP and report the blocker" without specifying a durable record. The *baseline* did this better (set `status: blocked` + in-ticket note + commit); the with-skill arm only reported in chat. Consider specifying: set `status: blocked` and record the blocking ID in the ticket before stopping.
- **Verification-log format:** the with-skill arm invented a reasonable `## Verification log` line (the skill mandates recording tool-round count but gives no format); its self-reported counts also drifted from the committed log. A one-line canonical format would make this auditable.

## Next-iteration changes

1. **Redesign the dependency gate to test resolution rules, not metadata-following:** unmet dependency expressed as a bare ID with no in-epic match but a tempting same-ID ticket in another epic/_archive (skill rule: fail the check, don't resolve globally), or a dependency in `in-progress` rather than `to-do`.
2. **Re-test eval 0's numbering assertion** with a stronger fixture (e.g. a second type series or archived FEAT-007) and/or 2–3 runs per cell to separate knowledge from single-run luck. n=1 per cell is this iteration's biggest statistical weakness.
3. **Add a worktree-recovery eval** asserting against `references/worktree-recovery.md` (planted stale worktree registration or orphaned `index.lock`; assert diagnose-first behavior: `--dry-run` prune, `rev-parse --git-path`, no manual `.git` surgery). The brief anticipated this; iteration 1 only exercises the orchestration template.
4. **Convert eval 1's judge-lite assertions to artifact checks** by asserting a durable blocked record (which also closes the skill gap above, once the skill specifies it).
5. **Split eval 2 assertion 8** (sub-tickets table vs merge-order section) into two assertions; the combined form needed a borderline judgment call against the baseline.
6. **Fold the two skill gaps above into SKILL.md** and re-run to confirm no regression (the eval suite now doubles as the regression harness).
