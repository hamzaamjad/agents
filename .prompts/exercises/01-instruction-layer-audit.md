# Exercise 1: Instruction-layer audit and ticket-workflow portability remediation

Usage: paste into a fresh agent session with `~/.agents` as the workspace root.
Sequencing: run this exercise first; exercises 2-4 assume its outputs may exist.

## Goal

Bring this workspace's instruction layer up to the standard its own skills define: every pointer resolves, the repo documents itself, and the `ticket-workflow` skill becomes self-contained and portable across deployment hosts.

## Required skill

Read and follow `skills/engineering-context/SKILL.md` as a full workspace audit (scope C), plus initial `AGENTS.md` scaffolding (scope D applies — no AGENTS.md exists yet). Load its references per the skill's loading map and run its `scripts/validate_context.py <project-root>` before and after edits.

## Evidence pack

Findings from a review on 2026-06-09. Line numbers may drift; re-locate via the quoted search strings. Re-verify each finding before editing; if one no longer reproduces, record that in the report and skip its fix.

1. Dangling failure-recovery pointer: `skills/ticket-workflow/SKILL.md` lines 67 and 185 (search: `worktree-recovery.md`) direct agents to `docs/runbooks/worktree-recovery.md`, which does not exist in this repo. The pointer fires exactly when a worktree operation has already failed.
2. Unversionable canonical template: line 129 (search: `_template.md`) links `../../../.prompts/orchestration/_template.md`. The target does not exist, and `.gitignore` ignores `.prompts/`, so the canonical orchestration template can never be committed.
3. Host-specific path: line 221 (search: `archive-search.sh`) invokes `bash .claude/skills/ticket-workflow/scripts/archive-search.sh`. `~/.claude/skills` does not exist on this machine; the script lives at `skills/ticket-workflow/scripts/archive-search.sh` here.
4. Missing self-documentation: the repo has no `AGENTS.md` or `README.md` — no authoring conventions, eval-loop docs, or deployment map.
5. Fragmented global instruction surface: `~/.codex/AGENTS.md` is an empty file; `~/.claude/CLAUDE.md` makes claims about an auto-memory system that need verification; `~/.codex/rules/default.rules` holds project-specific command allowances in global scope.
6. Unversioned second skill library: `~/.codex/skills/` holds 9 skills outside any git repo (analytics-sql, chronicle, codex-primary-runtime, data-observability, dbt-ops, playwright, playwright-interactive, screenshot, security-best-practices).
7. Namespace pollution: `skills/defining-specifications-workspace/` holds eval artifacts, not a skill, inside the directory hosts scan for skills.

## Deliverables

1. Self-contained `ticket-workflow`: bundle a worktree-recovery runbook and the orchestration prompt template into `skills/ticket-workflow/references/`, and rewrite the three broken references so they resolve relative to the skill directory on any deployment host. For the runbook: first search the user's other repositories for an existing `worktree-recovery.md`; if found, copy it in and cite its origin. If not found, reconstruct it from the sections SKILL.md cites (diagnostic commands; recovery procedures including closure-ticket partial execution with Goal A as safe default; prevention conventions including the lock-contention retry snippet) and mark it `Status: Reconstructed — review required`.
2. `AGENTS.md` at the repo root per `skills/engineering-context/references/agents-md-spec.md`, covering: what this repo is, directory layout, skill-authoring conventions (frontmatter, size budgets, references/ pattern, eval expectations), the eval-loop workflow and where its artifacts live, a deployment map of which hosts read which paths, and permission boundaries (always / ask-first / never).
3. Audit report in audit mode: Findings, Applied Changes, Residual Risk, Next Pass.
4. A decision memo — proposal only, no migration performed — on consolidating `~/.codex/skills` into this repo: recommendation, options considered, migration steps, risks.

## Boundaries

- Autonomous: edits inside `~/.agents`, including the remediation and the new AGENTS.md.
- Ask first: any write outside `~/.agents` (`~/.codex/*`, `~/.claude/*`); moving or renaming `skills/defining-specifications-workspace/`; changes to `.gitignore` policy.
- Never: deleting or rewriting skill content beyond diagnosed findings; history rewrites; pushing.
- Tone: per the engineering-context rubric, use moderate imperative phrasing in all edited instruction files — no all-caps directives.

## Definition of done

- The validation script's after-run is clean, or each remaining warning is explained in the report.
- Every relative reference in every edited file resolves from that file's own location.
- `ticket-workflow` contains no path that assumes a specific deployment root.
- AGENTS.md passes the engineering-context quality gate: critical rules in the first 20%, permission boundaries defined, within the rubric's size thresholds.
- Each fixed pointer has a named acceptance check in the report.
- Work is committed in small commits, one per finding group; nothing pushed.

## If evidence does not match

Report the discrepancy in Findings and continue with the remaining items. Do not force a pre-baked fix onto changed ground.
