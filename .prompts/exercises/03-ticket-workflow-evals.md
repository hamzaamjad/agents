# Exercise 3: Build and run an eval suite for ticket-workflow

Usage: paste into a fresh agent session with `~/.agents` as the workspace root.
Sequencing: run after Exercise 1 — eval 3 below asserts against the orchestration template and recovery runbook that Exercise 1 bundles into the skill. If those do not exist yet, scope assertions to what the skill currently ships and flag the gap in the report.

## Goal

Extend the with/without-skill benchmark loop — already proven on `defining-specifications` (+23pp in iteration 3) — to the workspace's most operationally critical skill. Produce an eval suite that measures whether `ticket-workflow` actually changes agent behavior on ticket creation and execution, run one full benchmark iteration in both arms, and report which assertions discriminate.

## Required reading

- `skills/ticket-workflow/SKILL.md` and its references — the behavior under test.
- `skills/defining-specifications/evals/evals.json` — the eval JSON format precedent.
- `skills/defining-specifications-workspace/` — the harness layout precedent: `iteration-N/` containing per-eval directories with `eval_metadata.json`, `with_skill/` and `without_skill/` runs each holding `outputs/` and `grading.json`, plus `benchmark.json` and `benchmark.md`.
- The skill-creator skill (Claude plugin cache, `example-skills/.../skill-creator/SKILL.md`) for eval and benchmarking methodology, if reachable.
- `AGENTS.md` at the repo root, if present — authoritative for artifact locations.

## Design requirements

- 3 evals, 8-12 assertions each, in the precedent JSON schema (id, name, prompt, expected_output, assertions, files).
- Suggested coverage — adapt if a more discriminating design emerges, and say so in the report:
  1. Standalone ticket creation from a rough feature request. Assert: naming convention, required frontmatter fields, a Verification section with runnable commands, 5 or fewer acceptance criteria, a Constraints section.
  2. Ticket execution in a fixture repo containing a prepared ticket with one unmet dependency and one executable path. Assert: hard stop reported on the unmet dependency, complexity score populated, verification commands actually run, Outcome block matching `references/outcome-schema.md`, a dedicated mark-done commit.
  3. Epic creation and decomposition. Assert: hex-ID naming, work performed in a worktree rather than on main, orchestration prompt instantiated, dependency references resolve within the epic, no use of `git add -A`.
- Prefer assertions checkable by file inspection or git history (`git log`, frontmatter fields, file existence) over judge impressions. Where an LLM judge is unavoidable, record the standard bias caveats (position, verbosity, self-preference) in the grading notes.
- Each eval gets a fixture: a minimal throwaway git repo (a few files, a toy script with a runnable check), built by a setup script so runs are reproducible.

## Isolation rules

- Eval subagents run inside temporary fixture directories, never inside `~/.agents` itself.
- The with_skill arm receives the skill content; the without_skill arm receives only the task prompt. Neither arm receives the assertion list.
- Grading happens after runs complete, against the assertion list only.

## Deliverables

- `skills/ticket-workflow/evals/evals.json`.
- A workspace directory following the precedent layout, holding iteration-1 artifacts: per-eval outputs, grading.json files, benchmark.json, benchmark.md.
- benchmark.md reporting: pass rates per arm, per-eval deltas, which assertions discriminate (baseline fails, with-skill passes), which are confounded or trivially passed by both arms, and concrete next-iteration changes.

## Definition of done

- One full iteration executed in both arms across all 3 evals.
- At least 3 assertions demonstrate discrimination; if fewer, the next-iteration section explains the redesign honestly rather than padding the numbers.
- No mutations to `~/.agents` outside the new evals file and the workspace directory.
- Artifacts committed; nothing pushed.

## Budget note

This is the most expensive exercise: 6 or more subagent runs plus grading. If capacity is constrained, run evals sequentially and checkpoint with the user after the first eval has run in both arms to confirm the cost is acceptable.
