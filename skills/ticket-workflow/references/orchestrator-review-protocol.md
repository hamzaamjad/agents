# Orchestrator Review Protocol

The orchestrator is the first automated quality gate between a sub-agent's
finished ticket and the epic branch. This file is the canonical source of
the 12-gate review checklist, the four escalation actions, the retry
budget, and the six terminal outcome states. The orchestration prompt
template at [orchestration-template.md](orchestration-template.md) (same
directory) is the executable form of this protocol; the two must not drift.

## Review Gates

Execute the twelve gates below in order. Each gate produces an explicit
PASS or FAIL with one-line evidence. A FAIL on any gate stops review and
routes to the Escalation Actions section.

1. **Confirm the review inputs are complete and consistent (entry criteria).**
   **Check:** ticket scope + constraints ("Do NOT…") + acceptance criteria + declared file-path allowlist + verification log are all present; the sub-agent marked done; the worktree has a branch name that matches the ticket; and there is a clean commit history for the ticket's work (no half-done changes).
   **Why:** Formal inspections and modern review both rely on explicit entry/exit criteria to avoid reviewing garbage or incomplete artifacts; missing context is a leading cause of superficial review.

2. **Re-run a minimal "sanity verification" on the orchestrator machine (not just trust the log).**
   **Check:** run the fastest subset that detects environment drift (e.g., `lint + unit` or the project's "smoke" script) and ensure results match the provided verification log (same commands, same pass).
   **Why:** Worktrees isolate workspace state but not all shared repo/global assumptions (hooks, shared config), and logs can be stale or misreported; rerunning a small subset reduces "it passed over there" failures.

3. **Compute diff stats and classify review size vs. expected ticket size.**
   **Check:** count files changed and LOC changed; compare to the ticket's declared scope and typical thresholds (e.g., flag >400 LOC for "high scrutiny" and require explicit justification for "why this much change").
   **Why:** Defect-finding drops as reviewed code volume rises; practitioner data suggests effectiveness diminishes beyond ~200–400 LOC per review chunk. Use size as a *risk multiplier*, not an auto-fail.

4. **Verify "changed files" stay inside the ticket's declared file-path allowlist (side-effects gate).**
   **Check:** `changed_paths ⊆ allowlist` (with a small, explicitly allowed "exceptions list" such as generated lockfiles or shared configs if the ticket allows them). If there are out-of-scope file edits, require (a) an explicit rationale tied to acceptance criteria, and (b) a compatibility check with the epic branch.
   **Why:** This is the single most deterministic defense against "agent wandered into unrelated refactors." In multi-agent workflows, conflicts are often deferred to merge time; catching cross-area edits early prevents merge storms later.

5. **Hard-check the ticket "Constraints" section as non-negotiable policy.**
   **Check:** for each "Do NOT" rule, map to an observable test:
   *If "Do NOT change public API" → check exported symbols / routes / schemas weren't altered.*
   *If "Do NOT add dependencies" → check lockfile / manifest diff is empty.*
   *If "Do NOT touch migrations" → check migrations directory unchanged.*
   Any violation is an automatic review fail unless the ticket itself explicitly amended the constraint.
   **Why:** Constraints are effectively organizational policy boundaries. Probabilistic "guardrails" are routinely bypassed; the safest approach is deterministic policy enforcement at boundaries.

6. **Validate acceptance criteria by building a criteria-to-evidence matrix (not "tests passed").**
   **Check:** for each acceptance criterion, write one line of evidence: *which code path implements it, and which test/log demonstrates it.* If any criterion has no evidence, fail review.
   **Why:** Modern code review is as much about change understanding as defect hunting; a matrix forces intent alignment.

7. **Check "negative space": what *should* have changed but didn't (omissions gate).**
   **Check:** given scope + acceptance criteria, ask:
   *Should there be at least one new/modified test? docs? type updates? telemetry?*
   Require explicit justification when expected artifacts are missing.
   **Why:** Omissions are hard-to-find defects; a second-pass orchestrator is primarily an "omission hunter."

8. **Spot-check maintainability and code health, but don't block on nits.**
   **Check:** evaluate naming/readability, duplication, and whether the change worsens architectural boundaries. Block only on maintainability regressions that create future risk, not stylistic preferences (unless violating a standard).
   **Why:** Review should ensure code health improves over time, balancing progress with quality; avoid blocking for minor polish.

9. **Search for "implicit behavior changes" in shared or configuration surfaces.**
   **Check:** if diff touches config files, shared utilities, auth/session, data models, or build scripts, require:
   - explicit backward compatibility note
   - at least one targeted test or integration check
   - a short "blast radius" statement
   **Why:** These are high-leverage files where small diffs have wide impact; reviews often devolve into minor issues unless reviewers deliberately focus on deeper implications.

10. **Assess mergeability against the current epic branch (partial-merge risk control).**
    **Check:** rebase/merge the ticket branch onto the latest epic branch in the worktree (or a temporary integration worktree) and confirm:
    - conflicts are resolved (or none exist)
    - the minimal sanity suite still passes post-rebase
    **Why:** Git will surface conflicts when divergent commits touch the same lines; rebasing can introduce conflicts and forces explicit resolution. This step prevents "passes alone, breaks when combined."

11. **Handle partial epic failures with explicit dependency rules.**
    **Check:** only merge a passing ticket if (a) its dependencies are already merged, or (b) it is dependency-free / guarded (feature flag, non-reachable code path, or purely additive API that nothing calls yet). Otherwise, hold it to avoid integrating code that can't compile/run without the missing dependency ticket.
    **Why:** Workflow orchestrators treat tasks as dependency-ordered units; the epic should behave like a dependency graph, not a pile of independent patches.

12. **Finalize decision with a strict, logged outcome: MERGE, FIX, REASSIGN, ESCALATE, or RESTART.**
    **Check:** produce a short decision record containing: scope delta summary, constraints pass/fail, acceptance criteria mapping status, and the chosen escalation (if any).
    **Why:** Without an explicit exit record, orchestrators either auto-merge or stall. Make the outcome auditable and repeatable.

## Escalation Actions

The four canonical actions, each mapped to its failure-type rule from
R2's "Escalation pattern comparison" section. Exactly one action is
chosen per failing review.

1. **`REASSIGN_NEW_SUB_AGENT`** — from R2 "Re-assign the same ticket to a new sub-agent".
   **Best when:** the failure suggests *agent capability mismatch* or *process corruption*, not a small patch defect. Typical triggers:
   - The implementation repeatedly ignores constraints or scope (e.g., keeps editing out-of-allowlist paths after being corrected once).
   - The change is conceptually wrong (misread requirement), and fixing it would be equivalent to re-implementing.
   - The branch/worktree is chaotic (many unrelated commits, unclear intent), making targeted correction slower than redo.
   **Why this works:** The "retry with a fresh worker" pattern from durable execution systems: if the execution environment or decision path is bad, restarting can be cheaper than debugging.

2. **`CORRECTIVE_SUB_TICKET`** — from R2 "Create a corrective sub-ticket targeting the specific failure".
   **Best when:** the work is mostly correct and the failure is *localized* and *well-scoped*, such as:
   - Missing/weak tests for one acceptance criterion
   - Minor constraint-adjacent issue that can be fixed without redesign (e.g., touched one extra file that can be reverted)
   - Documentation/telemetry missing but easy to add
   - Small refactor needed for readability/maintainability
   **Why this works:** Mirrors "guardrails + feedback loop" patterns in agent frameworks: validate output, and if it fails, return precise feedback for a bounded correction.
   **Ticket shape:** the corrective sub-ticket **must** use the TASK template from `references/templates.md` § Task. Bare IDs in its `dependencies:` field resolve within the current epic.

3. **`ESCALATE_TO_PR_AGENT_WITH_FLAG`** — from R2 "Mark the ticket blocked and escalate to the downstream PR review agent with a flag".
   **Best when:** the failure is *high-stakes or ambiguous*, where a "stronger reviewer" (or a different review stage) is appropriate:
   - Design/API judgment calls not resolvable from ticket text
   - Security/privacy concerns that require deeper threat modeling
   - Cross-cutting architecture changes touching shared surfaces
   - Conflicts between constraints and acceptance criteria (spec inconsistency)
   **Why this works:** Many orchestration systems embed "human-in-the-loop" or "approval workflows" as explicit escalation nodes; the PR review agent is the next approval node in this pipeline.

4. **`RESTART_FROM_SCRATCH`** — from R2 "Revert the sub-agent's branch and restart from scratch".
   **Best when:** the change introduces *systemic risk* or *unrecoverable divergence*:
   - Major constraint violations with broad impact (e.g., altered public API when forbidden)
   - Large diff far outside scope, implying the agent "went rogue"
   - Hard-to-trust state: generated files, sweeping refactors, or unexplained dependency changes
   - Fixing would require large-scale manual patch surgery, risking new defects
   **Why this works:** The "compensation/rollback" idea from workflow engines: if a multi-step process fails in a way that threatens system integrity, you undo and restart.

## Retry Budget

`MAX_FIX_CYCLES = 2` is the default. After two failed correction cycles
on the same ticket, the orchestrator must choose `REASSIGN_NEW_SUB_AGENT`
or `RESTART_FROM_SCRATCH` — a third corrective ticket is not permitted.

Extrapolated from R2, which leaves `<MAX_FIX_CYCLES>` as a placeholder.
See `docs/implementation_plan.md` §4 for the observable signals that
would justify changing this default.

## Outcome States

The six terminal states. Every review finalizes to exactly one of these:

- `MERGED` — all gates PASS, ticket merged into the epic branch.
- `NEEDS_FIX` — localized failure, one `CORRECTIVE_SUB_TICKET` created.
- `REASSIGNED` — retry budget exhausted or conceptual mismatch; ticket re-queued for a fresh sub-agent.
- `ESCALATED` — ambiguity or high-stakes failure; ticket marked `blocked` and flagged for the downstream PR review agent.
- `RESTARTED` — systemic risk or sweeping unscoped change; sub-agent branch reverted, fresh run authored.
- `BLOCKED_DEPENDENCY` — ticket passes on its own but depends on a ticket that has not yet merged; holds until the dependency lands.
