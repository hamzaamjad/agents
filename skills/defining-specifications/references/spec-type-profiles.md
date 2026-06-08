# Spec Type Profiles

Read this after intake, once you know what kind of spec you are writing. Each profile is a *delta* on the default template in `SKILL.md`: which sections to emphasize, add, or drop. Start from the default template, then apply the matching profile. When a request spans types (e.g. a feature that needs a migration), compose the relevant profiles.

The default template already covers most of what any spec needs. Do not duplicate it here; only adjust.

## Feature / new capability

The default template is tuned for this case. Emphasis:

- `Users And Stakeholders` and `Proposed Behavior` carry the weight; write requirements as user-observable behavior.
- Make `Non-Goals` explicit early; new features attract scope creep.
- `Acceptance Criteria` should include at least one negative-case scenario per error-handling requirement.

## Bug remediation

The highest-value addition for bugs is separating three behaviors so the implementing agent fixes the defect without disturbing anything else. Replace `Proposed Behavior` with:

- **Current behavior**: what happens today, including the trigger and the incorrect result. Cite the reproduction.
- **Expected behavior**: what should happen instead.
- **Unchanged behavior**: adjacent behavior that must stay identical. This is the regression guardrail — name the flows the agent must not touch.

Also add:

- `Reproduction`: minimal steps or a failing input/command.
- `Root Cause (hypothesis)`: mark clearly as a hypothesis unless confirmed from code; do not present a guess as fact.
- Acceptance criteria should include a regression check asserting the `Unchanged behavior` still holds.

## Refactor / restructure

Zero behavior change is the defining constraint. Adjust:

- State the invariant up front: external behavior and public contracts are unchanged.
- `Non-Goals`: no behavior changes, no new features, no dependency upgrades unless named.
- Replace functional `Acceptance Criteria` with **characterization checks**: existing tests still pass; public API/signatures unchanged; before/after structure described.
- `Technical Context`: describe the current structure and the target structure (module boundaries, names, call graph).

## Migration / data or platform change

Migrations fail on edge cases and cutover, so make those explicit. Add:

- `Source -> Target`: what is moving and the mapping between old and new (a table is good here).
- `Migration Strategy`: backfill, dual-write/dual-read, cutover, and **rollback** plan. State idempotency and re-run safety.
- `Verification`: counts and reconciliation (row counts match, checksums, spot checks), not just "it ran".
- `Backwards Compatibility`: what keeps working during and after; deprecation window.
- Acceptance criteria should assert reversibility (or an explicit accepted point of no return) and data integrity.

## UX / interaction change

Specify the full state space, not just the success screen. Add or emphasize in `UX, Workflow, Or Interaction Notes`:

- All states: default, loading, empty, error, partial, success.
- Accessibility: keyboard, focus order, contrast, screen-reader labels.
- Copy: exact strings for labels, errors, and empty states (downstream agents should not invent product copy).
- Responsive/breakpoint behavior and any instrumentation/analytics events.
- Acceptance criteria can use described end states or screenshot diffs as observable outcomes.

## Agent handoff / process or skill spec

For specs whose primary consumer is another AI agent (including specs about prompts, skills, or workflows), tighten the handoff:

- Lead with `Source Context` and a `For Implementing Agents` block (see the default template) so the agent knows which sections are authoritative and how to treat assumptions and open questions.
- Be explicit that unresolved `Open Questions` are blockers: the implementing agent should surface them, not guess an answer.
- Acceptance criteria should be checkable by file inspection or scripted checks, since there may be no human in the loop.
- Keep implementation slices lightweight; this skill produces the spec, not the ticket breakdown.
