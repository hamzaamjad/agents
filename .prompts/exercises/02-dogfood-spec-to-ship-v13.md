# Exercise 2: Dogfood the full pipeline — ship defining-specifications v1.3

Usage: paste into a fresh agent session with `~/.agents` as the workspace root.
Sequencing: run after Exercise 1 when possible. If `AGENTS.md` exists at the repo root, read it first; it is authoritative for workspace conventions.

## Goal

Ship v1.3 of the `defining-specifications` skill by running the workspace's own toolchain end to end — `defining-specifications` writes the spec, `ticket-workflow` turns it into an epic and executes it, `session-retrospective` closes the loop — while logging every point of friction in the pipeline itself. The friction log is a first-class deliverable, not a byproduct: it is the best available signal for improving these skills.

## Required skills

Read each at the phase that needs it, and follow it as written — deviations are data, so log them rather than silently adapting.

- `skills/defining-specifications/SKILL.md` (Phase A)
- `skills/ticket-workflow/SKILL.md` plus its references (Phases B-C)
- `skills/session-retrospective/SKILL.md` (Phase D)

## Input backlog

Source: `skills/defining-specifications-workspace/iteration-3/benchmark.md`, "Suggested next steps". Verify each against the current skill before specifying.

1. `DEC-###` appears in the Agent-Friendly Conventions ID list but has no corresponding section in the default template — an orphan convention.
2. The `Status` field offers `Draft | Ready for Review | Approved | Blocked` but only the Draft-to-Ready transition is defined; Approved and Blocked have no entry or exit rules.
3. The Clarify step keys question budgets to Simple/Medium/Large specs without defining the tiers.
4. The skill has no inline worked example.
5. Eval-1 (`spec-skill-improvement`) in `skills/defining-specifications/evals/evals.json` is confounded — its subject material already embodies the conventions being tested. Replace its subject or demote it to a regression-only check.

## Known friction to resolve at spec time

This repo's `.gitignore` ignores `.tickets/` and `.prompts/` as per-workspace artifacts, but the ticket-workflow protocol requires committing tickets and the orchestration prompt (epic creation step 7) and `git mv`-ing tickets to `_archive/` at closure — operations that fail on untracked files. Surface this as a blocking open question in the spec (options include un-ignoring those paths for this repo, or defining a documented protocol variant for unversioned-tickets repos). Get the user's decision at the Phase A checkpoint before creating the epic.

## Phases and checkpoints

Phase order is a process constraint: each phase consumes the previous phase's artifact, and two checkpoints need user decisions.

- Phase A — Spec. Save under `docs/specs/` per the skill's conventions. Scope: the five backlog items plus anything the skill's own self-review surfaces, with scope additions explicitly marked. Keep the spec under 300 lines. Checkpoint: present the spec summary and open questions (including the gitignore decision); wait for approval.
- Phase B — Epic. Use ticket-workflow exactly as written: worktree, hex ID, sub-tickets, orchestration prompt. Cap at 5 sub-tickets; decompose further only if the protocol's own triggers fire. Checkpoint: present the ticket tree and merge strategy; wait for approval.
- Phase C — Execute. Follow the execution protocol literally — dependency checks, complexity scoring, verification commands, Outcome blocks, dedicated mark-done commits, closure ticket, archive. Where protocol and reality conflict, stop, log the conflict, and ask rather than improvising.
- Phase D — Retro. Run session-retrospective with emphasis on pipeline friction: every place a skill instruction was ambiguous, wrong, or fought this repo's conventions. Deliver the friction log as a list of candidate fixes, each with a file and section target.

## Constraints

- v1.3 keeps `skills/defining-specifications/SKILL.md` at or under 300 lines; push detail into `references/` when the inline worked example would crowd the file.
- Bump frontmatter `version` to 1.3; keep the existing template structure stable except where the backlog requires changes.
- No edits to other skills in this exercise — friction findings go in the log, not into immediate fixes.
- Nothing pushed; merge or PR per the user's Phase B decision.

## Definition of done

- All five backlog items are resolved in v1.3 or explicitly descoped with rationale recorded in the spec.
- Eval-1 is replaced or marked regression-only, consistent with the spec's decision.
- Every executed ticket carries a complexity score, a verification log with the actual tool-round count, and an Outcome block per the schema.
- The epic is archived per the closure protocol and worktrees are cleaned up.
- The friction log contains at least one concrete improvement candidate per logged friction point, including the gitignore conflict resolution.
