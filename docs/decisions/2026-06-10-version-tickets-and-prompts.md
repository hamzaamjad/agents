# Decision memo: version .tickets/ and .prompts/ in this repo

- Date: 2026-06-10
- Status: Decided and applied
- Decision owner: Hamza (via orchestrator proxy at the Exercise 2 Phase A checkpoint)
- Origin: Q-001 of `../specs/SPEC-defining-specifications-v1-3-2026-06-10.md` (DEC-003)

## Problem

This repo's `.gitignore` ignored `.tickets/` and `.prompts/` as per-workspace artifacts, but the ticket-workflow protocol requires git-tracked paths: epic creation step 7 commits tickets and the orchestration prompt, and the closure ticket runs `git mv` (archive) and `git rm` (prompt deletion) — operations that fail on untracked files. Dogfooding the pipeline in this repo (defining-specifications v1.3 epic) made the conflict blocking.

## Decision

Un-ignore both `.tickets/` and all of `.prompts/`; keep `.claude/worktrees/` ignored (physical worktree checkouts, never content). This broadens the spec's draft option A, which would have kept `.prompts/exercises/` ignored: the exercise briefs are substantial authored artifacts the user wants versioned and synced at the end of the orchestration session — coherent history beats transience.

Applied changes: `.gitignore` (drop two ignore lines), `AGENTS.md` directory layout (three lines describing the new policy), this memo. The exercise briefs themselves are committed by the orchestrator at final sync, not by the in-flight exercise agent.

## Options considered

- **Narrow un-ignore** (`.tickets/` + `.prompts/orchestration/` only): keeps briefs transient; rejected because the user wants the briefs versioned.
- **Protocol variant for unversioned-tickets repos** (plain `mv`/`rm`, no ticket commits): requires editing ticket-workflow (out of scope for the running exercise) and loses the protocol's audit trail (committed tickets, Outcome blocks, archive history).

## Consequences

- Epics created in this repo follow ticket-workflow exactly as written, including commit and archive steps.
- `.tickets/_archive/` accumulates as the durable record of agent-executed work and feeds `archive-search.sh` retrieval.
- Future per-workspace prompts in this repo are tracked by default; anything genuinely transient needs an explicit new ignore rule.
