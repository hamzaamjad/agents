# Exercise 2 friction log — Phase D deliverable (final)

Every point of pipeline friction observed while shipping defining-specifications
v1.3 through the workspace's own toolchain (spec → epic → execution → retro).
Each entry carries a concrete improvement candidate with a file and section
target. Maintained live during the exercise; finalized 2026-06-10 at Phase D.
Priority candidates, by observed cost: FRIC-017, FRIC-018, FRIC-014, FRIC-013,
FRIC-009 (see the session retrospective for ranking rationale).

## Phase A

- FRIC-001: Pre-existing uncommitted spec for this exact deliverable found in
  `docs/specs/` at Phase A start (leftover from an interrupted prior run; not in any
  commit). Neither the exercise brief nor the orchestration protocol defines how a
  re-run should treat leftover artifacts. The defining-specifications skill's
  update-in-place rule (Workflow step 5) happened to cover it — adopted, re-verified
  every claim, repaired one defect. Candidate fix: orchestration/exercise-brief
  template gains a "re-run hygiene" clause (adopt-and-verify vs delete-and-rewrite);
  target `skills/ticket-workflow/references/orchestration-template.md` (preamble) or
  the exercise-brief conventions.

- FRIC-002: Backlog item 2 (undefined Status lifecycle) bit during this very phase:
  a spec that is complete and being presented at a human checkpoint, with one
  decision-critical open question, has no correct status under v1.2 — line 98 forces
  `Draft` until questions are "resolved or explicitly accepted", though the artifact
  is literally ready for review. Kept `Draft` with a parenthetical. Validates
  REQ-003; no extra fix needed beyond the spec's own scope. Target:
  `skills/defining-specifications/SKILL.md` § Self-Review (fixed by v1.3 REQ-003).

- FRIC-003: Traceability rule ambiguity: the references file requires every
  `REQ-###` to be reachable from an `AC-###` but is silent on whether `NFR-###`
  needs the same; the prior draft left NFR-004 unmapped and the Quality Checklist
  didn't catch it. Candidate fix: one sentence in
  `skills/defining-specifications/references/requirements-and-acceptance-criteria.md`
  § Traceability stating whether/which NFRs require AC coverage.

- FRIC-004: `validate_context.py` has no baseline mechanism: 6 pre-existing LOW
  findings on AGENTS.md mean every downstream gate must hand-carry "no NEW findings
  beyond the 6 known LOWs" (spec NFR-003, TEST-005). Candidate fix: either remediate
  the 6 LOWs in `AGENTS.md` or add a baseline/suppression option to
  `skills/engineering-context/scripts/validate_context.py`.

- FRIC-005: Eval harness path convention conflicts with the repo portability rule:
  `evals/evals.json` eval-1 `files` uses an absolute home path
  (`/Users/hamzaamjad/...`), while AGENTS.md forbids absolute home paths in skill
  content. Captured in spec (Technical Context, ASM-001, NFR-004). Candidate fix:
  document the harness's path-resolution contract wherever the eval loop is defined,
  or make the harness resolve repo-relative paths; target: eval-loop docs /
  `skills/defining-specifications/evals/evals.json` consumers.

- FRIC-006: `docs/specs/` is absent from the AGENTS.md directory layout (only
  `docs/audits/` and `docs/decisions/` are listed), so the skill's default output
  location exists outside the documented repo map. Candidate fix: one layout line in
  `AGENTS.md` § Directory layout (bundle with the Q-001 edit if option A is chosen).

- FRIC-007 (observation, no deviation): the gitignore conflict the brief flags is
  real and verified — `.gitignore` lines 42-44 ignore `.tickets/` and `.prompts/`,
  while ticket-workflow epic-creation step 7 requires committing tickets + the
  orchestration prompt, and closure steps 2-3 run `git mv`/`git rm` on those paths
  (fail on untracked files). Resolution is Q-001 at the Phase A checkpoint; the
  decision memo (if option A) is the improvement artifact. Target: `.gitignore` +
  `AGENTS.md` layout lines + `docs/decisions/` memo.
  [Resolved 2026-06-10: DEC-003, broadened option A; memo
  `docs/decisions/2026-06-10-version-tickets-and-prompts.md` shipped on main.]

## Phase B

- FRIC-008: Sub-ticket numbering scheme is ambiguous: SKILL.md § Directory Structure
  says "sequential numbering within epic", but the ID-assignment command dedupes
  per prefix (`awk -F- '!seen[$1]++'`), implying independent per-prefix sequences.
  Chose per-prefix (FEAT-001..004 + CHORE-001) per the command's semantics; a
  continuous reading would yield CHORE-005. Candidate fix: one sentence in
  `skills/ticket-workflow/SKILL.md` § Naming stating numbering is per type prefix
  within the scope.

- FRIC-009: The exercise's 5-sub-ticket cap collides with the protocol's mandatory
  closure ticket: the spec's five implementation slices + closure = 6 natural
  tickets. Folded SLICE-005 (version bump + final sweep) into the closure CHORE —
  defensible (the sweep must run after all content tickets, exactly when closure
  runs) but it makes the closure ticket carry content work in a separate commit
  before the closure commit. Candidate fix: `skills/ticket-workflow/SKILL.md`
  § Epic Closure Ticket states whether closure may carry small finalization tasks;
  orchestration/exercise briefs state whether the closure ticket counts toward
  decomposition caps.

- FRIC-010: Drift between `skills/ticket-workflow/references/templates.md` and
  SKILL.md: the epic template's merge-order comment says the closure ticket
  "updates INDEX.md", but SKILL.md's closure protocol (steps 1-5) has no INDEX.md
  step and no INDEX.md exists in this repo. Followed SKILL.md. Candidate fix:
  remove the INDEX.md mention from the templates.md comment, or add the step to
  the closure protocol — the two must not drift.

- FRIC-011: The epic template's stock acceptance criterion "PR from epic branch to
  main created and ready for review" presumes a pushable remote; this exercise
  forbids pushing, and SKILL.md step 7 itself allows "merge to main (or PR)".
  Rewrote the AC line for EPIC-e164 to "integrated to main per the approved merge
  strategy". Candidate fix: templates.md epic AC line gains "(or local merge per
  repo policy)".

- FRIC-012: Closure step 4 (`rm -rf .claude/worktrees/epic-<hex>`) is
  context-dependent in a way the protocol doesn't acknowledge: run from a nested
  sub-ticket worktree the guard is a no-op (path doesn't exist there); run from
  the orchestrator worktree it would delete the executing agent's own checkout.
  Actual cleanup happens in the post-merge orchestrator block. Candidate fix:
  `skills/ticket-workflow/SKILL.md` § Epic Closure Ticket specifies the execution
  context for closure and reconciles step 4 with the post-merge cleanup block.

- FRIC-013: The protocol's completion path is PR-shaped ("PR from epic branch to
  main. Archive after PR merge."), and its worktree rule says never cd to the
  primary clone — but in a no-remote/no-push repo the final epic-to-main merge can
  only run where main is checked out: the primary clone. The two rules collide
  exactly at integration time. Resolution proposed at the Phase B checkpoint:
  local `git merge --no-ff` executed from the primary clone as the sanctioned
  PR-substitute. Candidate fix: `skills/ticket-workflow/SKILL.md` § Epic Branch
  Workflow documents a local-merge completion variant for repos without a
  pushable remote, including where the merge runs.

- Positive observations (no fix needed): `archive-search.sh` degrades gracefully on
  a repo with no `.tickets/` tree ("no matches", exit 0); the skill's `python -c`
  hex-ID command worked on this macOS (python3 alias present).

## Phase C

- FRIC-014: The protocol nests sub-ticket worktrees inside the orchestrator
  worktree (`.claude/worktrees/epic-<hex>/<TICKET-ID>`), so any tree-scanning
  check run from the orchestrator worktree before cleanup double-counts the
  nested checkout: `validate_context.py` reported 0/9/12 with the FEAT-001
  worktree present and the baseline 0/0/6 immediately after `git worktree
  remove`. Post-merge sanity (orchestration M2) must run after worktree cleanup
  (M4) or scope its scan. Candidate fixes: `skills/ticket-workflow/SKILL.md`
  § Worktree Rules notes the nesting hazard for tree-scanning verification;
  orchestration-template.md reorders M2/M4 or scopes sanity commands;
  `validate_context.py` skips nested git worktrees.

- FRIC-015: `git branch -d` for a merged ticket branch fails when run from the
  primary clone (main does not yet contain the epic-branch merge); it must run
  from the epic worktree whose HEAD contains the merge. SKILL.md's cleanup
  snippets don't say where to run branch deletion. Candidate fix: one line in
  `skills/ticket-workflow/SKILL.md` § Epic Closure Ticket / post-merge cleanup
  stating branch deletion runs from the epic worktree (or uses -D after
  verifying the merge commit is on the epic branch).

- FRIC-016: `references/outcome-schema.md` carries provenance from its origin
  repo that does not resolve here: "from the point FEAT-003 lands" (collides
  with this epic's own FEAT-003), `docs/implementation_plan.md` §4, and
  `docs/research/r4-archive-knowledge-retrieval.md` — none exist in this repo.
  Candidate fix: replace origin-repo references with self-contained wording
  (the bundling rule AGENTS.md already prescribes for runtime-consumed skills).

- FRIC-017: A ticket verification command authored at decomposition time was
  unpassable by construction: FEAT-003's AC-005 regex captured the example
  "section" up to the next `\n## ` — but any faithful filled template instance
  contains `## ` headings inside its fence, so the capture truncated and the
  fence assertion failed. Corrected at execution to a fence-aware parse
  asserting the same properties (annotated in the ticket; orchestrator reviewed
  the correction at Gate F). Candidate fix: `skills/ticket-workflow/SKILL.md`
  § Quality Rules adds "dry-run each verification command against a sketch of
  the expected artifact before committing the ticket"; same lesson applies to
  defining-specifications TEST-### authoring (the spec's TEST-002 had the same
  latent assumption but grep-level checks dodged it).

- FRIC-018: The closure protocol's guarded `git mv` fails on a repo's first-ever
  epic: `git mv .tickets/EPIC-... .tickets/_archive/EPIC-...` requires the
  `_archive/` parent to exist, and nothing in the protocol creates it (git
  tracks no empty directories). Error: "renaming ... failed: No such file or
  directory". Fixed with `mkdir -p .tickets/_archive` before the guarded mv;
  re-run was a clean no-op-safe sequence. Candidate fix:
  `skills/ticket-workflow/SKILL.md` § Epic Closure Ticket step 2 prepends
  `mkdir -p .tickets/_archive` to the guarded snippet.

## Phase D

- FRIC-019: The exercise brief makes the friction log a file deliverable of the
  retrospective phase, while `skills/session-retrospective/SKILL.md` § Phase 1
  states retrospective output is conversational only and nothing is written to
  disk without Phase 2 approval. Resolved without deviation by maintaining the
  log as a brief-mandated exercise artifact from Phase A onward (not a retro
  write), but the seam is real for any future brief that asks the retro skill
  itself to produce files. Candidate fix: one sentence in
  `skills/session-retrospective/SKILL.md` § Phase 1 acknowledging that an
  externally mandated session log may be referenced (not authored) by the
  retrospective.
