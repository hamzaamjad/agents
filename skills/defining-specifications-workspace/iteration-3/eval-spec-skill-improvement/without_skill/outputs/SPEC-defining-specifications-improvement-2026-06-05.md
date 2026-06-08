---
spec_id: SPEC-defining-specifications-improvement
title: Improve the defining-specifications skill for better agent-consumable specs
status: Ready for Review
version: 1.0
date: 2026-06-05
owner: Hamza Amjad
spec_type: agent-handoff / process-and-skill
primary_consumers: [AI coding agents, human reviewers]
subject_artifact: skills/defining-specifications/SKILL.md (v1.2) + references/*
related:
  - skills/defining-specifications/references/requirements-and-acceptance-criteria.md
  - skills/defining-specifications/references/spec-type-profiles.md
---

# Specification: Improve the `defining-specifications` Skill

## For Implementing Agents

This spec is the source of truth for the next round of edits to the
`defining-specifications` skill. Read this orientation first.

- **Authoritative sections** (build to these exactly): `Goals`, `Non-Goals`,
  `Requirements`, `Acceptance Criteria`, and `Testing And Verification`. If any
  other section conflicts with these, these win.
- **Scope of the change**: you are improving an existing instruction artifact
  (a Markdown skill plus its `references/` files, and you MAY add small helper
  assets such as a validator script and example files). You are NOT building a
  product feature, and you are NOT rewriting the skill from scratch.
- **`Assumptions` are unconfirmed.** They are recorded so you can proceed
  without a human, but if reality contradicts one, prefer reality and note it.
- **`Open Questions` are blockers, not guesses.** Where an `Open Question`
  governs a requirement, the requirement marks the safe default to use until the
  question is answered. Do not silently invent an answer; surface it.
- **Out of scope, always**: creating tickets, task decomposition, branches,
  commits, PRs, or implementing the validator's downstream behavior beyond what
  the acceptance criteria require. See `Non-Goals`.
- **Definition of done**: every `REQ-###` is satisfied and reachable from at
  least one passing `AC-###`; `Acceptance Criteria` are checkable by file
  inspection or a scripted check; the skill's own Quality Checklist still passes
  on the edited skill.

## Summary

The `defining-specifications` skill (v1.2) is already a mature, well-structured
instruction set: it defines a mission, operating principles, a six-step
workflow, a default template, agent-friendly ID conventions, a quality
checklist, and two reference files (EARS/GWT and per-type profiles). It is good
prose, but it under-delivers on its own central promise — making spec quality
*objectively checkable by an AI agent without a human in the loop*.

This spec proposes a focused set of improvements that turn the skill's stated
conventions into **enforceable, machine-verifiable structure**: a YAML
frontmatter contract for produced specs, an executable self-check that verifies
ID and traceability invariants, a consolidated non-interactive operating mode, a
spec-size tiering rule to cut overhead on small changes, repair of an internal
inconsistency (`DEC-###` IDs with no home), and one inline golden example. The
goal is measurably better agent output, not a documentation rewrite.

## Problem Statement

The skill tells agents to do high-value things (stable IDs, `REQ -> AC -> TEST`
traceability, separate facts from assumptions, behave well when non-interactive)
but provides no mechanism that lets an agent — or a grader — confirm those things
actually happened. Concretely, from read-only inspection of the current skill:

1. **Traceability is advisory, not enforced.** The skill states every
   non-trivial `REQ` should be reachable from an `AC`, and `AC -> TEST`
   (`SKILL.md` Agent-Friendly Conventions; `references/requirements-and-acceptance-criteria.md`
   "Traceability"), but there is no required artifact (a matrix) or check that
   proves coverage. Gaps are invisible until review.
2. **The Quality Checklist is prose only.** `SKILL.md` "Quality Checklist" is a
   human reading task. An agent can claim it passed without verifying ID
   uniqueness, monotonic numbering, or `REQ`/`AC` cross-references.
3. **Produced-spec metadata is not machine-readable.** The Default Spec Template
   header (`Status:`, `Date:`, `Owner/Requester:`, `Primary Consumers:`,
   `Source Context:`) is free prose. Downstream agents must parse English to
   learn a spec's status, type, or ID, which is brittle.
4. **Internal inconsistency: `DEC-###` has no section.** Agent-Friendly
   Conventions lists `DEC-###` as a stable ID, but the Default Spec Template has
   no `Decisions` section, so decisions have nowhere to live and the ID is
   unusable as written.
5. **Non-interactive behavior is scattered.** Guidance for "no human in the
   loop" is split across the Clarify step, the Outline And Confirm step, and
   Write Boundaries. An agent in an evaluation/CI context must reassemble the
   rule from three places, which invites inconsistent behavior (this very eval
   is such a context).
6. **One template size for all specs.** The skill ships a single, fairly large
   default template with no lightweight tier, so a one-line change and a large
   migration get the same overhead. "Calibrate specificity" is stated as a
   principle but not operationalized into a structural choice.
7. **No end-to-end example inside `SKILL.md`.** The references contain fragments,
   but there is no single short, complete spec the agent can pattern-match
   against in one read.

## Goals

- G-001: Make the skill's core quality promises (IDs, traceability, fact/assumption
  separation) **verifiable by file inspection or a scripted check**, not just by
  prose instruction.
- G-002: Make produced specs **machine-parseable** at the top (structured
  metadata) without hurting human readability.
- G-003: Give agents **one unambiguous rule** for operating non-interactively
  (evaluations, CI, batch runs) so behavior is consistent.
- G-004: **Reduce overhead** for small specs via an explicit size-tiering rule,
  while preserving rigor for large ones.
- G-005: **Repair internal inconsistencies** and add the minimum scaffolding
  (e.g., a Decisions section) so every documented convention is usable.
- G-006: Keep the skill **focused and backward-compatible**: existing specs and
  the existing ID scheme remain valid; this is an enhancement, not a rewrite.

## Non-Goals

- NG-001: This spec does NOT change the skill's mission, audience, or core
  six-step workflow shape; it refines and enforces what is already there.
- NG-002: This task produces a **specification only**. It does NOT create
  tickets, task decomposition, implementation plans, branches, commits, or PRs.
- NG-003: It does NOT edit `skills/defining-specifications/SKILL.md` or its
  references; implementation of these requirements is downstream work.
- NG-004: It does NOT introduce a heavyweight spec framework, external
  dependencies, a hosted service, or a required toolchain. Any helper script
  must be optional and run with tools already assumed present.
- NG-005: It does NOT mandate a specific programming language, CI provider, or
  repository layout for the optional validator beyond what acceptance criteria
  require.
- NG-006: It does NOT expand the skill into general documentation authoring,
  code review, or ticket validation (those are separate skills/concerns).

## Users And Stakeholders

- **Downstream AI coding agents** (primary consumer): read produced specs to
  plan and implement; need stable structure, machine-readable metadata, and
  explicit traceability so they can act without reconstructing chat context.
- **The spec-authoring agent** (the skill's runtime): needs deterministic rules
  and a self-check it can run before handoff.
- **Human reviewers**: need to confirm intent, scope, and unresolved decisions
  quickly; must not be forced to read YAML to understand the spec.
- **Skill maintainer (Hamza)**: needs changes that are backward-compatible and
  low-maintenance.
- **Evaluation/grader harness**: needs outcomes checkable by file inspection or
  scripts without interpretation.

## Current State

Grounded in read-only inspection of `skills/defining-specifications/` on
2026-06-05:

- `SKILL.md` (v1.2, ~212 lines): YAML frontmatter (`name`, `description`,
  `metadata.version`), then Mission, Operating Principles, a 6-step Workflow
  (Intake, Context Review, Clarify, Outline And Confirm, Write The Spec,
  Self-Review), a Default Spec Template (prose-header + ~20 sections), an
  Agent-Friendly Conventions list (IDs `G/NG/REQ/NFR/SLICE/TEST/AC/RISK/Q/ASM/DEC`),
  a Quality Checklist, and Write Boundaries.
- `references/requirements-and-acceptance-criteria.md`: EARS patterns table, GWT
  acceptance-criteria format, traceability narrative, good/weak contrasts.
- `references/spec-type-profiles.md`: per-type deltas (feature, bug, refactor,
  migration, UX, agent handoff).
- `evals/evals.json`: present (eval harness for the skill).

Observed strengths to preserve: clear mission/two-reader framing; EARS + GWT as
defaults with explicit "when not to use"; per-type profiles; explicit
non-goals/write-boundaries discipline; a `For Implementing Agents` block already
in the template.

Observed gaps drive the `Requirements` below (see `Problem Statement` items
1–7). Detailed evidence is in the companion file
`NOTES-clarifying-questions-and-analysis-2026-06-05.md`.

## Proposed Behavior

After these changes, an agent using the improved skill will:

1. Emit produced specs with a **YAML frontmatter** block carrying structured
   metadata, while keeping the human-readable header content available in the
   body.
2. Maintain (and, for non-trivial specs, render) a **traceability mapping** so
   `REQ -> AC -> TEST` coverage is explicit.
3. Run a **deterministic self-check** (a documented checklist procedure, and an
   optional validator script) before handoff that verifies ID and traceability
   invariants and fails loudly on violations.
4. Follow a **single consolidated non-interactive rule** when it cannot ask
   questions: record questions + assumptions in the spec and proceed to a
   complete draft, choosing documented safe defaults.
5. Choose a **spec size tier** (Tiny / Standard / Large) and use the matching
   section set, reducing overhead on small changes.
6. Have a **`Decisions` section** so `DEC-###` IDs are usable.
7. Have **one short end-to-end example** to pattern-match against.

## Requirements

Functional requirements use EARS (`shall`, with `When/If/While/Where`). The
"system" is the improved `defining-specifications` skill and its optional
validator unless stated otherwise.

### Theme A — Machine-readable produced specs

- REQ-001: The skill shall instruct authoring agents to begin each produced
  specification file with a YAML frontmatter block delimited by `---` containing
  at least: `spec_id`, `title`, `status`, `date`, `spec_type`,
  `primary_consumers`, and `source_context` (or `related`).
- REQ-002: Where the produced spec is a revision of an existing spec, the skill
  shall require a `version` field and a changelog entry, and shall instruct the
  agent to preserve the existing `spec_id`.
- REQ-003: The skill shall define the allowed `status` values as an enumerated
  set (`Draft`, `Ready for Review`, `Approved`, `Blocked`) and shall require the
  frontmatter `status` to be one of them.

### Theme B — Enforced traceability and IDs

- REQ-004: When a produced spec contains more than five `REQ-###` requirements,
  the skill shall require an explicit traceability mapping (a matrix or a
  per-`AC` reference list) that links each `REQ-###` to at least one `AC-###`.
- REQ-005: The skill shall require that every `AC-###` names the `REQ-###`
  (or `NFR-###`) it verifies, and that every non-trivial `REQ-###`/`NFR-###` is
  referenced by at least one `AC-###`.
- REQ-006: The skill shall state that IDs are unique within a spec, are never
  reused after removal, and that a removed requirement is marked deprecated
  rather than renumbered, so external references remain stable.
- REQ-007: The skill's Default Spec Template shall include a `Decisions` section
  using `DEC-###` IDs, resolving the current inconsistency where `DEC-###` is
  listed as a convention but has no section.

### Theme C — Executable self-check

- REQ-008: The skill shall provide a deterministic, ordered self-check procedure
  (a numbered checklist the agent executes) that verifies, at minimum: required
  frontmatter fields present, `status` valid, ID uniqueness, and `REQ -> AC`
  coverage.
- REQ-009: Where a validator script is included, the validator shall accept a
  spec file path and shall exit non-zero and print a diagnostic naming the
  offending ID or field for each violation of REQ-001, REQ-003, REQ-005, or
  REQ-006.
- REQ-010: If the self-check or validator reports an unresolved blocking item,
  then the skill shall require the agent to keep the spec at `status: Draft` (or
  `Blocked`) rather than `Ready for Review`.

### Theme D — Non-interactive operating mode

- REQ-011: The skill shall define a single, named "Non-Interactive Mode" rule in
  one place, and other steps (Clarify, Outline And Confirm) shall reference it
  rather than restating it.
- REQ-012: While operating in Non-Interactive Mode, the skill shall require the
  agent to (a) record clarifying questions in `Open Questions`, (b) record the
  working assumption and the safe default chosen for each, in `Assumptions`, and
  (c) proceed to a complete draft without blocking.
- REQ-013: While operating in Non-Interactive Mode, the skill shall instruct the
  agent to write all outputs only within the assigned output location and to
  treat any other path as out of bounds.

### Theme E — Spec size tiering

- REQ-014: The skill shall define at least two spec size tiers (e.g., "Tiny" and
  "Standard"/"Large") and the minimum required sections for each, so that small
  changes do not incur full-template overhead.
- REQ-015: When the change is small (the agent judges a Tiny tier), the skill
  shall still require, at minimum: frontmatter, summary/problem, scope/non-goals,
  at least one `REQ-###`, and at least one `AC-###` with traceability.
- REQ-016: The skill shall give an explicit, observable heuristic for choosing a
  tier (e.g., based on number of requirements or affected components) so the
  choice is reproducible rather than arbitrary.

### Theme F — Example and consistency

- REQ-017: The skill shall include exactly one short, complete end-to-end
  example spec (inline or in `references/`) that demonstrates frontmatter, EARS
  requirements, GWT acceptance criteria, and traceability.
- REQ-018: The skill shall remain internally consistent: every ID type listed in
  Agent-Friendly Conventions shall have a corresponding place in the Default
  Spec Template or an explicit note that it is optional.

## Nonfunctional Requirements

- NFR-001: Backward compatibility — specs produced under v1.2 conventions
  (prose header, existing IDs) shall remain valid; the new frontmatter shall be
  additive, and the validator shall not hard-fail a pre-existing spec solely for
  lacking the new frontmatter (it MAY warn).
- NFR-002: Token economy — the edited `SKILL.md` shall not grow disproportionately;
  new normative detail beyond a short rule + example should live in
  `references/` to keep the always-loaded skill body lean.
- NFR-003: Tooling minimalism — any validator shall run with tools reasonably
  assumed present (e.g., a single standard-library script) and shall require no
  network access or external service.
- NFR-004: Human readability — frontmatter shall not replace the human-facing
  header/orientation content; a reviewer shall be able to understand the spec
  without parsing YAML.
- NFR-005: Determinism — the self-check procedure shall produce the same
  pass/fail verdict for the same spec input regardless of run order.

## UX, Workflow, Or Interaction Notes

- The improved Workflow keeps its six steps; "Non-Interactive Mode" is added as a
  named, referenced rule rather than a seventh step.
- The `Write The Spec` step gains a tier-selection sub-step and a
  frontmatter-emission instruction.
- The `Self-Review Before Handoff` step is upgraded from a prose checklist to an
  ordered, executable self-check (REQ-008) plus the optional validator (REQ-009).
- No change to the skill's invocation surface (its `description` trigger) is
  required; if edited, the trigger phrasing shall remain backward-compatible.

## Data, API, Or Contract Changes

- **Spec frontmatter contract** (new): the YAML keys in REQ-001/002/003 form the
  contract downstream agents may parse. Treat unknown keys as ignorable; treat
  the listed keys as stable.
- **Validator CLI contract** (optional, if implemented): input = path to a spec
  file; output = human-readable diagnostics on stderr/stdout and an exit code
  (`0` pass, non-zero fail). No other interface is mandated (see NG-005).

## Technical Context

- Affected artifacts: `SKILL.md` (workflow, template, conventions, checklist),
  `references/requirements-and-acceptance-criteria.md` (traceability matrix
  guidance), `references/spec-type-profiles.md` (tier-aware notes), and OPTIONAL
  new assets: `references/example-spec.md` and a validator script under the skill
  directory.
- Alternatives considered:
  - *Frontmatter vs. keep prose header*: frontmatter chosen for machine parsing;
    prose orientation retained for humans (NFR-004).
  - *Mandatory validator vs. documented self-check*: self-check is mandatory
    (REQ-008) so the improvement holds even without running code; the validator
    is optional/additive (REQ-009) to avoid a hard tooling dependency (NFR-003).
  - *Tiering vs. one template*: tiering chosen to operationalize the existing
    "calibrate specificity" principle (REQ-014–016).

## Implementation Slices

Lightweight only; detailed decomposition is downstream and out of scope (NG-002).

- SLICE-001: Add frontmatter contract + `status` enum + `Decisions` section to
  the Default Spec Template (REQ-001, REQ-003, REQ-007).
- SLICE-002: Add consolidated "Non-Interactive Mode" rule and re-point existing
  steps to it (REQ-011–013).
- SLICE-003: Add spec size tiers + selection heuristic (REQ-014–016).
- SLICE-004: Upgrade Self-Review into an ordered self-check; add traceability
  matrix requirement (REQ-004, REQ-005, REQ-008, REQ-010).
- SLICE-005: Add one end-to-end example and reconcile ID/section consistency
  (REQ-017, REQ-018).
- SLICE-006 (optional): Add the validator script (REQ-009) + a tiny fixture pair.

## Testing And Verification

- TEST-001: File-inspection — open the edited `SKILL.md` and confirm the Default
  Spec Template shows a YAML frontmatter block with the REQ-001 fields and a
  `Decisions` section.
- TEST-002: File-inspection — confirm the `status` enumeration (REQ-003) appears
  and matches the four allowed values.
- TEST-003: File-inspection — confirm a single "Non-Interactive Mode" definition
  exists and that the Clarify / Outline steps reference it (REQ-011).
- TEST-004: File-inspection — confirm at least two tiers and an explicit
  selection heuristic exist (REQ-014, REQ-016).
- TEST-005: File-inspection — confirm exactly one end-to-end example spec is
  present and contains frontmatter + EARS + GWT + traceability (REQ-017).
- TEST-006: Consistency check — for each ID type in Agent-Friendly Conventions,
  confirm a template section or explicit "optional" note exists (REQ-018).
- TEST-007 (if validator built): run the validator against a conformant fixture
  (expect exit 0) and a non-conformant fixture missing a `REQ -> AC` link
  (expect non-zero with a diagnostic naming the orphan REQ) (REQ-009).
- TEST-008: Regression — run the skill's existing `evals/evals.json` (or a
  representative subset) and confirm no previously passing assertion regresses
  (NFR-001).

## Rollout, Migration, And Operations

- Roll out as an in-place edit to the skill (version bump to v1.3). No data
  migration needed; existing specs remain valid (NFR-001).
- Communicate the new frontmatter contract in the skill body so downstream
  agents adopt it on next use.
- Rollback is trivial: revert the skill file(s) to v1.2; no persistent state.

## Risks And Mitigations

- RISK-001: Over-engineering the skill into a heavy framework. / Mitigation:
  NG-004, NFR-002, NFR-003; mandatory parts are doc-only, the validator is
  optional.
- RISK-002: Frontmatter duplicates the prose header and confuses humans. /
  Mitigation: NFR-004 keeps human orientation primary; frontmatter is additive.
- RISK-003: Tiering tempts agents to under-spec by always choosing "Tiny". /
  Mitigation: REQ-015 sets a hard minimum for the Tiny tier; REQ-016 makes the
  choice an observable heuristic, not a vibe.
- RISK-004: Backward-incompatible validation breaks old specs. / Mitigation:
  NFR-001 (warn, not fail) and TEST-008 regression gate.
- RISK-005: Skill bloat increases token cost on every load. / Mitigation:
  NFR-002 pushes detail to `references/`.

## Open Questions

Unanswered; each names the safe default the implementing agent should use until
resolved (treat as blockers to surface, not to guess past).

- Q-001: Should a validator **script** be required, or remain optional? Default:
  optional (REQ-008 mandatory self-check; REQ-009 conditional). Affects scope.
- Q-002: Preferred validator language/runtime if built (Python stdlib vs. node
  vs. shell)? Default: a single Python 3 stdlib script (no deps) — confirm host
  has Python. Affects NFR-003.
- Q-003: Exact target version label for the edited skill (v1.3?) and changelog
  location (frontmatter vs. a `## Changelog` section)? Default: v1.3, changelog
  as a short `## Changelog` section.
- Q-004: Should the new frontmatter be added to the *produced spec* template
  only, or also to `SKILL.md`'s own frontmatter? Default: produced-spec template
  only; leave the skill's own frontmatter (`name`/`description`/`metadata`)
  unchanged.
- Q-005: Exact tier thresholds (what counts as "Tiny")? Default proposed in
  REQ-016: Tiny when ≤3 requirements and a single affected component.
- Q-006: Should `references/example-spec.md` be a new file (adds a file) or be
  inline in `SKILL.md` (adds tokens)? Default: a `references/` file to honor
  NFR-002.

## Assumptions

- ASM-001: The skill's mission, audience, and six-step workflow are intentional
  and should be preserved, not redesigned. Confidence: high. Invalidated if the
  maintainer wants a structural redesign.
- ASM-002: Downstream consumers are AI coding agents capable of parsing YAML
  frontmatter. Confidence: high. Invalidated if specs are consumed only by tools
  that cannot parse YAML.
- ASM-003: Adding `references/` files and an optional validator inside the skill
  directory is acceptable to the maintainer. Confidence: medium. Invalidated if
  new files are unwanted (then prefer inline, accepting token cost).
- ASM-004: A Python 3 interpreter is available in environments where the
  optional validator would run. Confidence: medium. Invalidated on hosts without
  Python (then use a shell/node variant or skip the script).
- ASM-005: Backward compatibility with existing specs matters (there may be
  specs already authored under v1.2). Confidence: medium-high.
- ASM-006: This eval run is non-interactive; therefore this spec itself was
  authored under the proposed Non-Interactive Mode (questions + assumptions
  recorded, complete draft delivered). Confidence: high (matches eval metadata).

## Acceptance Criteria

Each criterion is checkable by file inspection or a scripted check and names the
requirement(s) it verifies.

- AC-001 (verifies REQ-001, REQ-003): Given the edited `SKILL.md`, When the
  Default Spec Template is inspected, Then it shows a `---`-delimited YAML
  frontmatter block containing `spec_id`, `title`, `status`, `date`,
  `spec_type`, `primary_consumers`, and `source_context`/`related`, and the
  `status` field's allowed values are enumerated as exactly `Draft`,
  `Ready for Review`, `Approved`, `Blocked`.
- AC-002 (verifies REQ-007, REQ-018): Given the edited `SKILL.md`, When the
  template and conventions are inspected, Then a `Decisions` section using
  `DEC-###` exists, and every ID type in Agent-Friendly Conventions maps to a
  template section or an explicit "optional" note.
- AC-003 (verifies REQ-004, REQ-005): Given a produced spec with more than five
  `REQ-###`, When it is inspected, Then a traceability mapping is present and
  every `REQ-###` appears in at least one `AC-###` reference, and every `AC-###`
  names the requirement(s) it verifies.
- AC-004 (verifies REQ-006): Given a spec revision that removes a requirement,
  When the file is inspected, Then the removed ID is not reused and is marked
  deprecated rather than renumbered.
- AC-005 (verifies REQ-008, REQ-010): Given the edited `SKILL.md`, When the
  Self-Review step is inspected, Then it contains an ordered self-check covering
  frontmatter presence, `status` validity, ID uniqueness, and `REQ -> AC`
  coverage, and states that an unresolved blocking item keeps `status` at
  `Draft`/`Blocked`.
- AC-006 (verifies REQ-011, REQ-012, REQ-013): Given the edited `SKILL.md`, When
  the workflow is inspected, Then exactly one "Non-Interactive Mode" definition
  exists, the Clarify and Outline steps reference it, and it requires recording
  questions in `Open Questions`, assumptions+defaults in `Assumptions`, and
  writing only within the assigned output location.
- AC-007 (verifies REQ-014, REQ-015, REQ-016): Given the edited skill, When the
  `Write The Spec` step is inspected, Then at least two size tiers are defined,
  the Tiny tier still mandates frontmatter + summary/problem + scope/non-goals +
  ≥1 `REQ` + ≥1 traceable `AC`, and an observable tier-selection heuristic is
  stated.
- AC-008 (verifies REQ-017): Given the edited skill, When references/body are
  inspected, Then exactly one complete end-to-end example spec exists containing
  frontmatter, at least one EARS `shall` requirement, at least one GWT
  acceptance criterion, and a `REQ -> AC` link.
- AC-009 (verifies REQ-009, NFR-003): Given the optional validator is built,
  When it runs against a non-conformant fixture whose `REQ-002` has no `AC`,
  Then it exits non-zero and prints a diagnostic naming the orphaned `REQ-002`;
  and When it runs against a conformant fixture, Then it exits `0`; and the
  validator uses no network and no third-party dependencies.
- AC-010 (verifies NFR-001): Given a valid v1.2-style spec lacking the new
  frontmatter, When the validator runs, Then it does not hard-fail solely for
  the missing frontmatter (it may warn).
- AC-011 (verifies NFR-002, NFR-004): Given the edited `SKILL.md`, When compared
  to v1.2, Then human-readable orientation remains and the bulk of new normative
  detail (matrix guidance, example, tier detail) lives in `references/` rather
  than inflating the always-loaded skill body.

## Source References

- `skills/defining-specifications/SKILL.md` (v1.2) — mission, workflow, default
  template, agent-friendly conventions, quality checklist, write boundaries.
- `skills/defining-specifications/references/requirements-and-acceptance-criteria.md`
  — EARS patterns, GWT format, traceability narrative.
- `skills/defining-specifications/references/spec-type-profiles.md` — per-type
  deltas including the agent-handoff profile.
- `skills/defining-specifications/evals/evals.json` — existing eval harness
  (regression target for TEST-008).
- `.../iteration-3/eval-spec-skill-improvement/eval_metadata.json` — eval intent
  and assertions used to scope this spec.
- Companion: `NOTES-clarifying-questions-and-analysis-2026-06-05.md` (this
  directory) — detailed gap evidence and full clarifying-question log.

## Changelog

- 1.0 (2026-06-05): Initial specification. Authored non-interactively per the
  proposed Non-Interactive Mode; clarifying questions recorded in `Open Questions`
  with safe defaults.
