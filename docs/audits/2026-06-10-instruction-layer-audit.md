# Instruction-layer audit — 2026-06-10

- Scope: full workspace audit (engineering-context scope C) plus initial AGENTS.md scaffolding (scope D); ticket-workflow portability remediation per the exercise brief at `.prompts/exercises/01-instruction-layer-audit.md` (unversioned).
- Method: `skills/engineering-context/SKILL.md` workflow with all four references loaded; evidence-pack findings re-verified before each edit.
- Validation: `python3 skills/engineering-context/scripts/validate_context.py .`
  - Before: `No instruction files found in /Users/hamzaamjad/.agents` (nothing to validate — itself finding 4).
  - After: 0 high, 0 medium, 6 low — exit 0. All six lows are one false-positive class, explained under Residual Risk.

## Findings

| # | Finding | Reproduced? | Tags | Impact |
|---|---|---|---|---|
| 1 | `docs/runbooks/worktree-recovery.md` pointers dangle (SKILL.md lines 67, 185) | Yes — plus a third instance at line 94 (`worktree-recovery.md` § Prevention conventions), found via the prescribed search string | `context_rot` | High — fires exactly when a worktree operation has already failed |
| 2 | Canonical orchestration template unversionable (`../../../.prompts/orchestration/_template.md`, line 129) | Yes — target absent; `.gitignore` ignores `.prompts/`; a fourth dangling instance found at `references/orchestrator-review-protocol.md` line 7 | `context_rot`, single-source violation | High |
| 3 | Host-specific invocation `bash .claude/skills/ticket-workflow/scripts/archive-search.sh` (line 221) | Yes — `~/.claude/skills` does not exist on this machine; script lives at `skills/ticket-workflow/scripts/`; two more host-specific references inside the script itself (header comment and `--semantic` error message) | `context_rot`, portability | High on non-symlink hosts |
| 4 | No `AGENTS.md` / `README.md` — repo does not document itself | Yes — validator found zero instruction files | `missing_permissions`, missing self-documentation | High |
| 5 | Fragmented global instruction surface | Yes, with nuance (below) | `redundancy`, `mixed_concerns`, `context_rot` | Medium |
| 6 | `~/.codex/skills/` unversioned second library | Yes — 9 directories, none under git; one (`codex-primary-runtime`) is empty, so 8 actual skills, not 9 | `missing_guardrail` | Medium-high (single-copy loss risk) |
| 7 | `skills/defining-specifications-workspace/` holds eval artifacts in the skills namespace | Yes — `iteration-{1,2,3}/` benchmarks and eval outputs; no SKILL.md | `mixed_concerns` | Medium |

Finding 5 detail (verified read-only; no writes outside this repo):

- `~/.codex/AGENTS.md` is 0 bytes — confirmed empty; pure noise in Codex's global scope.
- `~/.claude/CLAUDE.md` auto-memory claims are *consistent with on-disk evidence*: 6 project dirs under `~/.claude/projects/*/memory/` exist with `MEMORY.md` plus topic files matching the documented convention. The "loaded at session start" behavior is host runtime behavior and cannot be verified from disk alone; no contradiction found, so no remediation proposed beyond awareness.
- `~/.codex/rules/default.rules` confirmed to hold project-specific command allowances in global scope (dbt build, a specific Streamlit dashboard invocation referencing `scripts/visualization/demographic_dashboard.py` and `.secrets/rcc_db.env`). These belong in that project's scope; left in place (outside this repo — ask-first boundary).

## Applied changes

One commit per finding group; nothing pushed.

| Commit | Finding | Change |
|---|---|---|
| `f776e22` | 1 | Copied the canonical runbook from `hamzaamjad/tickets@c0296f9` (`docs/runbooks/worktree-recovery.md`) to `skills/ticket-workflow/references/worktree-recovery.md` with origin cited and two internal pointers adapted to resolve from the new location; rewrote all three SKILL.md pointers (lines 67, 94, 185) to `references/worktree-recovery.md` |
| `1954ba5` | 2 | Bundled the orchestration template from `hamzaamjad/tickets@b765bf8` as `skills/ticket-workflow/references/orchestration-template.md` (provenance + instantiation note in header); repointed SKILL.md line 129 and `orchestrator-review-protocol.md` line 7; reframed the underscore-glob note for deployments keeping a runtime copy under `.prompts/orchestration/` |
| `63cb2a7` | 3 | Rewrote the SKILL.md invocation as `bash scripts/archive-search.sh` resolved relative to the skill directory; replaced both in-script `.claude/skills/...` references with skill-relative `references/outcome-schema.md` |
| (this commit set) | 4 | Added root `AGENTS.md` (78 lines): identity, critical portability rule, permission boundaries (always/ask-first/never) in the first 30 lines, key command, directory layout, skill-authoring conventions, eval loop, deployment map, docs conventions |
| (this commit set) | 5–7 | This report; decision memo for finding 6 at `docs/decisions/2026-06-10-codex-skills-consolidation.md` (proposal only). Findings 5 and 7 documented, no files moved |

Finding 7 proposed remediation (not performed — downstream exercises reference the current path): move eval artifacts to a top-level `evals/defining-specifications/` directory so `skills/` contains only skill packages; update the AGENTS.md layout section in the same commit. Until then, AGENTS.md explicitly marks the directory as "eval data, not a skill."

### Acceptance checks (all passing)

- **AC1a** — `rg 'docs/runbooks' skills/ticket-workflow/` matches only the provenance citation inside the bundled runbook; zero matches in SKILL.md.
- **AC1b** — `references/worktree-recovery.md` exists and contains every section SKILL.md cites: § Diagnostic commands, § Recovery procedures > Closure ticket partial execution (Goal A safe default), § Prevention conventions with the lock-contention retry snippet.
- **AC2a** — `rg '\.\./\.\./\.\./\.prompts' skills/ticket-workflow/` returns nothing.
- **AC2b** — `references/orchestration-template.md` exists; its six outcome states and `MAX_FIX_CYCLES` default match SKILL.md and the review protocol.
- **AC3a** — `rg '\.claude/skills' skills/ticket-workflow/` returns nothing.
- **AC3b** — `cd skills/ticket-workflow && bash scripts/archive-search.sh --help` exits 0 (skill-relative invocation works).
- **AC4** — validator after-run: 0 high, 0 medium; AGENTS.md is 78 lines (<150 target), permission boundaries and critical rules within the first 30 lines.
- **AC5** — scripted sweep over every markdown link in all edited/created files: all resolve from each file's own location.

## Residual risk

- **Six low-severity tone warnings are false positives.** The validator's all-caps heuristic (`[A-Z]{4,}`) matches the canonical filenames AGENTS.md, SKILL.md, and CLAUDE.md in prose and the deployment-map table. The file contains no actual all-caps directives. Renaming canonical files to appease a heuristic would be wrong; left as-is.
- **Pre-existing emphasis caps inside ticket-workflow SKILL.md** ("MUST happen in a worktree", "Do NOT", "STOP") predate this audit and sit outside the diagnosed findings; the never-boundary on rewriting beyond findings left them. Lines actually edited use moderate phrasing.
- **Consuming repos that copied (rather than symlinked) the skill** would still hold the broken pointers. The one verified consumer (`~/tickets/.claude/skills/ticket-workflow`) is a symlink into this repo and picks up the fixes immediately.
- **`.prompts/` remains gitignored** while holding the exercise briefs; the gitignore policy decision is explicitly reserved for a later exercise. The canonical orchestration template no longer depends on it.
- **Findings 5–6 remediations are unexecuted proposals**; the fragmentation they describe persists until the memo is decided.

## Next pass

1. Decide and execute the codex-skills consolidation memo (pilot symlink first).
2. Relocate `skills/defining-specifications-workspace/` per the finding 7 proposal once downstream exercises stop referencing it.
3. Resolve the `.prompts/` gitignore policy (reserved decision): exercise briefs are currently unversioned working files.
4. Clean up the global surfaces from finding 5: delete or populate the empty `~/.codex/AGENTS.md`; move project-specific rules from `~/.codex/rules/default.rules` into that project's scope.
5. **Process improvement (systemic):** the validation script only scans AGENTS.md-class files, so dangling references inside `skills/*/SKILL.md` — the entire failure class behind findings 1–3 — are invisible to it. Extend `validate_context.py` (or add a small pre-commit check) to verify reference resolution across skill files too; AC5's link sweep in this audit is the prototype.
