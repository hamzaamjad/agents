# Specification: Improve the `defining-specifications` Skill for Agent-Consumable Spec Output

Status: Ready for Review
Date: 2026-06-05
Owner/Requester: Hamza Amjad (skill author)
Primary Consumers: AI coding agents (implementing agent that will edit the skill), human reviewers
Source Context:
- `skills/defining-specifications/SKILL.md` (v1.2) — mission, workflow, default template, conventions, quality checklist, write boundaries
- `skills/defining-specifications/references/requirements-and-acceptance-criteria.md` — EARS + Given/When/Then guidance
- `skills/defining-specifications/references/spec-type-profiles.md` — six per-type profile deltas
- `skills/defining-specifications/evals/evals.json` — existing eval harness for the skill
- Companion: `notes-questions.md` (clarifying questions, assumptions, grounded defects D1–D8)

## For Implementing Agents

This spec is itself an **agent-handoff / skill spec**: the system being specified is the
`defining-specifications` skill (its `SKILL.md` plus files under `references/`), not application code.

- **Authoritative sections:** `Requirements`, `Nonfunctional Requirements`, `Non-Goals`, and
  `Acceptance Criteria`. Implement to those. `Proposed Behavior` and `Technical Context` are supporting
  detail; `Summary`/`Current State` are orientation.
- **Assumptions (`ASM-###`) are unconfirmed.** They were chosen to unblock a non-interactive draft. If
  one is false, stop and reconcile before implementing the affected requirement.
- **Open Questions (`Q-###`) are blockers, not decisions.** Surface them to the requester; do not guess
  an answer and bake it into the skill.
- **Constraints that override defaults:** This spec changes a *skill that writes specs*. Do not break the
  existing EARS/Given-When-Then methodology or the established ID conventions (`REQ-###`, `AC-###`, …).
  All changes must be backward-compatible with specs already produced by v1.2.
- **Verification is by file inspection.** Every acceptance criterion below is checkable by reading the
  edited skill files (and, where noted, by running the skill's evals). There may be no human in the loop.

## Summary

The `defining-specifications` skill (v1.2) is already strong: clear mission, a default template, EARS +
Given/When/Then conventions, per-type profiles, and a quality checklist. Read-only inspection surfaced a
small number of **concrete, self-contained gaps** that reduce how reliably an AI agent can apply it:
internal inconsistencies (an ID convention with no matching template section; status values with no
defined lifecycle), guidance for non-interactive/autonomous runs that is scattered across three places,
undefined size tiers, the absence of a worked end-to-end example, no recommended traceability artifact,
and a prose-only quality gate that is hard to self-verify mechanically.

This spec defines a **focused, additive refinement** (target version 1.3) that closes those gaps so the
skill produces more consistent, traceable, self-verifiable specs — optimized for AI coding agents as the
primary consumer while staying easy for humans to review. It deliberately preserves the skill's existing
methodology, structure, and write boundaries; it is a refinement, not a redesign.

## Problem Statement

When a downstream agent uses the current skill, several avoidable failure modes remain:

1. **Inconsistent guidance erodes trust.** The conventions list a `DEC-###` ID that has no home in the
   template (D1), and the `Status` enum advertises `Approved`/`Blocked` states the workflow never defines
   (D2). An agent following the skill literally cannot satisfy both halves.
2. **Autonomous behavior is under-specified.** Non-interactive handling lives in three separate spots
   (D3); an agent running in an eval/CI/headless context must reconstruct the rule from fragments.
3. **Key terms are undefined.** Question budgets are keyed to "Simple/Medium/Large" specs that are never
   defined (D4), so the budget is effectively a guess.
4. **No exemplar.** `references/` has methodology snippets but no full example spec (D5); agents learn the
   target shape far faster from one worked example than from rules alone.
5. **Traceability is asserted but not made tangible.** `REQ -> AC -> TEST` is described (D6) but there is
   no compact artifact a grader or agent can scan to confirm coverage.
6. **The quality gate is prose-only.** The checklist (D7) is not expressed as inspectable pass/fail
   evidence, so self-review quality varies and graders cannot easily confirm it ran.

## Goals

- G-001: Eliminate the internal inconsistencies in `SKILL.md` so every advertised convention and status
  value is fully defined and usable.
- G-002: Make autonomous / non-interactive operation a single, canonical, unambiguous rule.
- G-003: Improve agent learnability by providing a worked, end-to-end example spec.
- G-004: Make traceability and the quality gate concretely verifiable (by the producing agent and by a
  grader) via file inspection.
- G-005: Keep `SKILL.md` lean and backward-compatible; push long content into `references/`.

## Non-Goals

- NG-001: Do not redesign the skill's methodology. EARS for requirements and Given/When/Then for
  acceptance criteria remain the defaults and are out of scope for change.
- NG-002: Do not rename the skill, change its `name`, or materially rewrite the trigger `description`
  beyond what a new reference file requires.
- NG-003: Do not add new spec *types* beyond the existing six profiles (feature, bug, refactor,
  migration, UX, agent handoff).
- NG-004: Do not produce tickets, task decomposition, implementation plans, branches, commits, or PRs.
  This spec defines *what to change in the skill*; it does not perform or schedule the change.
- NG-005: Do not build tooling, linters, scripts, or CI to enforce the quality checklist. Enforcement
  stays as skill *instructions* the agent self-applies, not as new code.
- NG-006: Do not modify the skill files as part of producing this spec; this spec is read-only with
  respect to the skill.
- NG-007: Do not break specs already authored under v1.2; all changes are additive or clarifying.

## Users And Stakeholders

- Implementing AI agent (primary consumer of this spec): needs unambiguous, self-consistent instructions
  to edit `SKILL.md` and `references/` correctly.
- Downstream spec-writing agent (primary consumer of the *improved skill*): needs a consistent template,
  a worked example, and a clear autonomous-mode rule.
- Human reviewer / skill author: needs to confirm the refinement preserves intent and is reviewable.
- Eval grader (`evals/evals.json`): needs file-inspectable evidence that the skill's gate and traceability
  conventions were followed.

## Current State

From read-only inspection of v1.2 (paths above):

- `SKILL.md` defines Mission, Operating Principles, a 6-step Workflow (Intake, Context Review, Clarify,
  Outline And Confirm, Write The Spec, Self-Review Before Handoff), a Default Spec Template, Agent-Friendly
  Conventions, a Quality Checklist, and Write Boundaries.
- The Default Spec Template includes a `For Implementing Agents` block and sections through
  `Source References`, but has **no `Decisions` section**, while Agent-Friendly Conventions lists a
  `DEC-###` ID (D1).
- The template's `Status:` line offers `Draft | Ready for Review | Approved | Blocked`; the Self-Review
  step only defines `Draft -> Ready for Review` (D2).
- The Clarify step sets question budgets for "Simple" (≤3), "Medium" (≤5), and "Large or ambiguous" (≤7)
  specs without defining the tiers (D4).
- Non-interactive handling appears in the Clarify step, the Outline And Confirm step, and is implied in
  Write Boundaries (D3).
- `references/` contains exactly two files (methodology + profiles); there is no full example spec (D5).
- Traceability `REQ -> AC -> TEST` is described in conventions and the methodology reference, with no
  recommended traceability-matrix artifact (D6).
- The Quality Checklist is a prose bullet list used as a "gate" (D7).

## Proposed Behavior

The improved skill (v1.3) behaves as today, plus:

- It is internally consistent: every ID convention has a template home, and every `Status` value has a
  defined meaning and transition rule.
- It contains one canonical "Autonomous / Non-Interactive Mode" rule that all steps reference.
- It defines the spec size tiers used for question budgeting.
- It ships a worked end-to-end example spec in `references/` that agents can pattern-match against.
- It recommends a lightweight traceability artifact for non-trivial specs and a structured, inspectable
  self-review the producing agent emits.
- `SKILL.md` stays close to its current length; new long-form content lives under `references/`.

## Requirements

Functional requirements use EARS. "The skill" = the `defining-specifications` skill as defined by
`SKILL.md` and its `references/`. "Produced spec" = a spec authored by an agent following the skill.

- REQ-001: The skill shall define a `Decisions` (`DEC-###`) element consistent with the `DEC-###`
  convention — either by adding a `## Decisions` section to the Default Spec Template or by removing the
  `DEC-###` convention — such that no advertised ID lacks a defined location. (Resolves D1.)
- REQ-002: The skill shall define the lifecycle for every value in the `Status` enum
  (`Draft`, `Ready for Review`, `Approved`, `Blocked`), stating the entry condition and allowed
  transitions for each, or shall reduce the enum to only the values it defines. (Resolves D2.)
- REQ-003: The skill shall contain a single canonical subsection (e.g. "Autonomous / Non-Interactive
  Mode") that states the rule: when live clarification is unavailable, the agent records clarifying
  questions and working assumptions in the spec (and/or one companion notes file), proceeds to a complete
  draft, and treats unresolved `Open Questions` as blockers rather than guessing. (Resolves D3.)
- REQ-004: Where the Clarify step references "Simple", "Medium", and "Large" specs, the skill shall define
  each tier with at least one observable criterion (e.g. by requirement count, files touched, or
  architectural/data-contract impact) so the question budget is determinable without guesswork.
  (Resolves D4.)
- REQ-005: When live clarification is unavailable, the skill shall instruct the agent to skip the
  blocking confirmation in "Outline And Confirm" and instead embed the outline and material assumptions in
  the output. (Reinforces REQ-003; resolves the D3 fragment in the Outline step.)
- REQ-006: The skill shall include a worked, end-to-end example specification as a reference file (e.g.
  `references/example-spec.md`) that applies the Default Spec Template and at least one spec-type profile,
  and demonstrates EARS requirements, Given/When/Then acceptance criteria, and `REQ -> AC` traceability.
  (Resolves D5.)
- REQ-007: The skill's "Write The Spec" guidance shall reference the example file by relative path so a
  downstream agent is pointed to it. (Makes REQ-006 discoverable.)
- REQ-008: For specs above the "Simple" tier, the skill shall recommend a lightweight traceability
  artifact (a `Traceability` matrix/table or an equivalent inline mapping) that links each `REQ-###` to the
  `AC-###` and `TEST-###` that verify it. (Resolves D6.)
- REQ-009: The skill shall express the Quality Checklist as a structured self-review the producing agent
  can emit and a grader can inspect — each item phrased as a verifiable pass/fail statement with space for
  evidence (e.g. a file path, section name, or ID), without introducing any executable tooling.
  (Resolves D7; bounded by NG-005.)
- REQ-010: When an explicit output path is provided by the user or the run context (e.g. an assigned eval
  directory), the skill shall instruct the agent to honor that path and shall state that it takes
  precedence over the default `./docs/specs/` location. (Resolves D8.)
- REQ-011: The skill shall preserve all existing ID conventions and section names that v1.2 specs rely on;
  where a section is added, it shall be additive so that v1.2-format specs remain valid. (Enforces NG-007.)
- REQ-012: Where the skill's metadata records a version, the skill shall update it (1.2 -> 1.3) and the
  change set shall include a short human-readable note of what changed. (Supports reviewability.)

## Nonfunctional Requirements

- NFR-001 (context economy): The edited `SKILL.md` shall not grow disproportionately; net additions to
  `SKILL.md` should stay small (target: under ~25 added lines), with substantive new content placed in
  `references/`. Rationale: `SKILL.md` is loaded into agent context on every trigger.
- NFR-002 (consistency): After the change, no convention, ID, or status value referenced anywhere in
  `SKILL.md` shall lack a definition or a template location.
- NFR-003 (backward compatibility): A spec authored under v1.2 shall still satisfy the v1.3 Quality
  Checklist without modification (additions are opt-in for new specs).
- NFR-004 (reviewability): All changes shall be expressed in Markdown and be reviewable by a human in a
  normal diff, with no generated, binary, or machine-only artifacts.

## UX, Workflow, Or Interaction Notes

Not applicable in the visual sense. The relevant "interaction" is the agent ↔ skill reading experience:
the canonical Autonomous Mode rule (REQ-003) and the example file (REQ-006) should be reachable from the
Workflow section with one relative-path hop, mirroring how the skill already points to its two existing
reference files.

## Data, API, Or Contract Changes

No code, schema, or API changes. The "contract" affected is the **document contract** of a produced spec
(its sections and ID conventions). Changes must be additive per REQ-011 / NFR-003. If REQ-002 reduces the
`Status` enum rather than defining all values, that is a contract narrowing and must be called out in the
change note (REQ-012).

## Technical Context

- Affected files: `skills/defining-specifications/SKILL.md` and one or more new/edited files under
  `skills/defining-specifications/references/`.
- The existing `references/` pattern (a `SKILL.md` section referencing a focused `.md`) is the model for
  REQ-006/REQ-007/REQ-008.
- Alternatives considered:
  - *Inline the example in `SKILL.md`* — rejected; violates NFR-001 (context economy).
  - *Build a linter/CI to enforce the checklist* — rejected; NG-005 (out of scope, adds maintenance).
  - *Keep `DEC-###` without a section* — rejected; fails NFR-002. REQ-001 allows either adding the section
    or removing the convention so the implementing agent can pick the lighter-weight fix.
- The existing `evals/evals.json` can be extended later to assert the new conventions, but doing so is not
  required by this spec (NG-005 keeps tooling out of scope).

## Implementation Slices

Lightweight only; detailed tickets are downstream (NG-004).

- SLICE-001: Consistency fixes in `SKILL.md` (REQ-001, REQ-002, REQ-011, REQ-012).
- SLICE-002: Canonical Autonomous Mode subsection + size-tier definitions, with Workflow steps referencing
  them (REQ-003, REQ-004, REQ-005, REQ-010).
- SLICE-003: Worked example reference file + traceability artifact guidance + structured self-review
  (REQ-006, REQ-007, REQ-008, REQ-009).

## Testing And Verification

- TEST-001: Inspect `SKILL.md` to confirm the `DEC-###` convention and its template location agree
  (verifies REQ-001).
- TEST-002: Inspect `SKILL.md` to confirm each `Status` value has a defined entry condition/transition, or
  that the enum was narrowed to defined values only (verifies REQ-002).
- TEST-003: Inspect `SKILL.md` for a single canonical Autonomous / Non-Interactive Mode subsection and
  confirm the Clarify and Outline steps reference it rather than restating divergent rules
  (verifies REQ-003, REQ-005).
- TEST-004: Inspect `SKILL.md` to confirm Simple/Medium/Large tiers each have at least one observable
  criterion (verifies REQ-004).
- TEST-005: Confirm a worked example spec file exists under `references/`, that it instantiates the
  template + ≥1 profile, and contains ≥1 EARS `REQ`, ≥1 Given/When/Then `AC` naming a `REQ`, and a
  traceability link (verifies REQ-006, REQ-008).
- TEST-006: Grep `SKILL.md` for a relative-path reference to the example file (verifies REQ-007).
- TEST-007: Inspect `SKILL.md` to confirm the Quality Checklist is expressed as pass/fail items with an
  evidence slot and that no executable tooling was added (verifies REQ-009, NG-005).
- TEST-008: Inspect `SKILL.md` to confirm explicit/assigned output paths are stated to override the
  `./docs/specs/` default (verifies REQ-010).
- TEST-009: Take a representative v1.2-format spec and confirm it still passes the v1.3 checklist
  unmodified (verifies REQ-011, NFR-003).
- TEST-010: Diff `SKILL.md` to confirm net additions stay within the NFR-001 budget and the version note
  is present (verifies NFR-001, REQ-012).
- TEST-011: Confirm all edited/added artifacts are Markdown and human-diff-reviewable (verifies NFR-004).

## Rollout, Migration, And Operations

- No runtime rollout. "Deploy" = merge the edited skill files. Bump `metadata.version` 1.2 -> 1.3
  (REQ-012).
- No migration of existing specs is required (NFR-003); new conventions are opt-in for new specs.
- Rollback = revert the skill file changes; there is no data or state to unwind.

## Risks And Mitigations

- RISK-001: Scope creep into a full skill rewrite. / Mitigation: NG-001..NG-003, NG-007 and the additive
  constraint REQ-011 bound the change to targeted refinements.
- RISK-002: `SKILL.md` bloat reduces context efficiency. / Mitigation: NFR-001 budget + REQ-006 places
  long content in `references/`.
- RISK-003: Over-formalizing the self-review reintroduces tooling. / Mitigation: NG-005 + REQ-009 keep it
  instruction-only (no scripts/linters).
- RISK-004: Narrowing the `Status` enum (REQ-002 option B) silently breaks specs using `Approved`/
  `Blocked`. / Mitigation: prefer defining the values; if narrowing, REQ-012 requires an explicit note and
  NFR-003 must still hold.

## Open Questions

Treat as blockers; do not guess (see `For Implementing Agents`).

- Q-001: For REQ-002, should `Approved`/`Blocked` be fully defined (lifecycle) or removed to a smaller
  enum? Preferred default if unanswered: define them (lower compatibility risk). (Relates to RISK-004.)
- Q-002: For REQ-001, is the author's intent to *add* a `Decisions` section to the template, or to *drop*
  the `DEC-###` convention? Either satisfies REQ-001; the choice affects template length (NFR-001).
- Q-003: Is there a hard length budget for `SKILL.md` beyond the NFR-001 target of ~25 added lines?
- Q-004: Should the new example reference file model a specific spec type (the agent-handoff profile is the
  most on-brand for an agent-first skill), or be type-agnostic?
- Q-005: Should `evals/evals.json` be extended to assert the new conventions now, or is that deferred?
  (Currently deferred per NG-005.)

## Assumptions

- ASM-001 (high confidence): Improvements should be additive plus targeted consistency fixes, not a
  structural rewrite. Invalidated if the author wants a reorganization.
- ASM-002 (high confidence): Adding new files under `references/` is acceptable. Invalidated if everything
  must remain in `SKILL.md`.
- ASM-003 (medium confidence): Keeping `SKILL.md` near its current length is desired for context economy.
  Invalidated by an explicit instruction that a larger `SKILL.md` is fine.
- ASM-004 (high confidence): EARS + Given/When/Then are locked in. Invalidated only by an explicit
  methodology change request.
- ASM-005 (medium confidence): A structured-but-tooling-free self-review is wanted. Invalidated if the
  author actually wants an automated linter/CI check.
- ASM-006 (medium confidence): A version bump to 1.3 with a change note is appropriate. Invalidated by a
  different versioning convention.

## Acceptance Criteria

Each criterion is checkable by inspecting the edited skill files (file inspection / grep), per the
agent-handoff profile.

- AC-001 (verifies REQ-001):
  - Given the updated `SKILL.md`,
  - When its Agent-Friendly Conventions and Default Spec Template are inspected,
  - Then either a `## Decisions` (`DEC-###`) section exists in the template, or the `DEC-###` convention is
    absent — and no ID is advertised without a template home.
- AC-002 (verifies REQ-002):
  - Given the updated `SKILL.md`,
  - When the `Status` enum and workflow are inspected,
  - Then every status value present in the template has a defined entry condition and transition rule (or
    the enum lists only defined values), with no undefined status remaining.
- AC-003 (verifies REQ-003):
  - Given the updated `SKILL.md`,
  - When searching for non-interactive guidance,
  - Then exactly one canonical subsection states the record-questions-and-assumptions-then-proceed rule and
    that unresolved Open Questions are blockers, and other steps reference it instead of restating it.
- AC-004 (verifies REQ-004):
  - Given the updated `SKILL.md`,
  - When the Clarify step's tiers are inspected,
  - Then Simple, Medium, and Large each have at least one observable, non-circular criterion.
- AC-005 (verifies REQ-005):
  - Given an agent running with live clarification unavailable,
  - When it reaches "Outline And Confirm",
  - Then the skill instructs it to embed the outline/assumptions in the output rather than block on
    confirmation.
- AC-006 (verifies REQ-006):
  - Given the `references/` directory after the change,
  - When listing it,
  - Then a worked example spec file exists that instantiates the Default Spec Template, applies ≥1 profile,
    and contains ≥1 EARS `REQ-###`, ≥1 Given/When/Then `AC-###` that names a `REQ-###`, and a
    traceability link.
- AC-007 (verifies REQ-007):
  - Given the updated `SKILL.md`,
  - When grepping for the example filename,
  - Then `SKILL.md` references the example file by relative path from the Workflow/Write step.
- AC-008 (verifies REQ-008):
  - Given the updated skill,
  - When the guidance for non-Simple specs is inspected,
  - Then it recommends a `Traceability` matrix or equivalent mapping linking `REQ -> AC -> TEST`.
- AC-009 (verifies REQ-009, NG-005):
  - Given the updated `SKILL.md`,
  - When the Quality Checklist is inspected,
  - Then each item is a verifiable pass/fail statement with an evidence slot, and no script, linter, or CI
    file was introduced.
- AC-010 (verifies REQ-010):
  - Given the updated `SKILL.md`,
  - When the output-path guidance is inspected,
  - Then it states that an explicit user-provided or run-assigned path overrides the default
    `./docs/specs/` location.
- AC-011 (verifies REQ-011, NFR-003):
  - Given a spec authored under v1.2,
  - When evaluated against the v1.3 Quality Checklist,
  - Then it passes without modification (changes are additive/opt-in).
- AC-012 (verifies REQ-012, NFR-001):
  - Given the change set,
  - When the diff and metadata are inspected,
  - Then `metadata.version` reads `1.3`, a short change note is present, and net additions to `SKILL.md`
    stay within the NFR-001 budget.
- AC-013 (verifies NG-004, NG-006):
  - Given the change set that implements this spec,
  - When it is inspected,
  - Then it modifies only the skill's `SKILL.md` and `references/` (plus optional metadata), and creates no
    tickets, branches, commits, PRs, or implementation/test code as part of satisfying the spec.

## Traceability

| Requirement | Acceptance Criteria | Verification |
|-------------|--------------------|--------------|
| REQ-001 | AC-001 | TEST-001 |
| REQ-002 | AC-002 | TEST-002 |
| REQ-003 | AC-003 | TEST-003 |
| REQ-004 | AC-004 | TEST-004 |
| REQ-005 | AC-005 | TEST-003 |
| REQ-006 | AC-006 | TEST-005 |
| REQ-007 | AC-007 | TEST-006 |
| REQ-008 | AC-008 | TEST-005 |
| REQ-009 | AC-009 | TEST-007 |
| REQ-010 | AC-010 | TEST-008 |
| REQ-011 | AC-011 | TEST-009 |
| REQ-012 | AC-012 | TEST-010 |
| NFR-001 | AC-012 | TEST-010 |
| NFR-003 | AC-011 | TEST-009 |
| NFR-004 | — | TEST-011 |
| NG-004 / NG-006 | AC-013 | (change-set inspection) |

## Source References

- `skills/defining-specifications/SKILL.md` (v1.2)
- `skills/defining-specifications/references/requirements-and-acceptance-criteria.md`
- `skills/defining-specifications/references/spec-type-profiles.md`
- `skills/defining-specifications/evals/evals.json`
- Companion notes: `./notes-questions.md` (questions, assumptions, grounded defects D1–D8)
