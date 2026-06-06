# Specification: Defining Specifications Skill Improvement

Status: Ready for Review
Date: 2026-06-05
Owner/Requester: Hamza Amjad
Primary Consumers: AI coding agents, human reviewers
Source Context:
- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`

## Summary

Improve the `defining-specifications` skill so agents produce more consistently implementation-ready specifications for spec-driven development. The skill already provides a strong mission, workflow, default template, agent-friendly ID conventions, and write boundaries. The next improvement should make the skill more deterministic in how agents choose the right spec shape, distinguish evidence from assumptions, handle non-interactive runs, and self-review artifacts before saving them.

The improved skill should continue to optimize for AI coding agents as the primary consumers while keeping the output easy for humans to review. The target outcome is not a broader documentation framework. It is a sharper instruction set that helps future agents write focused specs that can be handed to another coding agent without reconstructing the original conversation.

## Problem Statement

The current skill has a comprehensive default template and good operating principles, but it leaves several high-impact decisions to agent judgment:

- How to tailor the template to different spec types without producing bloated or under-specified artifacts.
- How much context to inspect before drafting, especially when source material is sparse or ambiguous.
- How to make non-interactive runs deterministic when clarification would normally be required.
- How to write requirements, acceptance criteria, and verification steps at the right level for downstream coding agents.
- How to self-audit the finished spec beyond checking that common sections exist.

These gaps can lead to specs that are structurally complete but not reliably actionable: too much boilerplate, ambiguous assumptions, missing evidence, vague acceptance criteria, or implementation slices that drift into ticket decomposition.

## Goals

- G-001: Add a clear output contract that defines what every generated spec must enable a downstream coding agent to do.
- G-002: Add spec-type profiles so agents can choose a focused structure for product, technical, bug remediation, migration, UX, review, and agent-handoff specs.
- G-003: Strengthen guidance for context gathering, evidence recording, and source references.
- G-004: Make non-interactive clarification behavior deterministic by requiring recorded questions, assumptions, and risk impact instead of blocking.
- G-005: Improve requirement, verification, and acceptance-criteria guidance so completion is objectively checkable.
- G-006: Add a lightweight quality rubric that agents apply before finalizing generated artifacts.

## Non-Goals

- NG-001: Do not rewrite the skill into a long handbook or generic product-management process.
- NG-002: Do not require every spec to include every template section.
- NG-003: Do not introduce ticket creation, implementation planning, branch management, commits, or code edits into this skill.
- NG-004: Do not optimize primarily for human narrative polish at the expense of downstream agent executability.
- NG-005: Do not add dependencies on external tools, schemas, or automation beyond normal file reading and writing.

## Users And Stakeholders

- AI coding agents invoking the skill: Need stable structure, explicit boundaries, concrete requirements, and enough context to implement without guessing.
- Human reviewers: Need fast confirmation of intent, scope, decisions, risks, and unresolved questions.
- Skill maintainer: Needs concise, durable guidance that remains easy to audit and update.
- Evaluation harness: Needs deterministic behavior when live clarification is disallowed.

## Current State

The current `SKILL.md` defines:

- A mission centered on focused, durable specs for downstream agent work.
- Operating principles that emphasize source-of-truth behavior, constructive criticism, focused scope, evidence, explicit assumptions, and checkable acceptance criteria.
- A five-step workflow: intake, context review, clarify, outline and confirm, write the spec.
- A default spec template with sections for summary, goals, current state, requirements, verification, risks, questions, assumptions, and acceptance criteria.
- Agent-friendly stable ID conventions.
- A quality checklist and write boundaries that prohibit implementation edits and unrelated artifacts.

Observed improvement opportunities:

- The default template is comprehensive, but the skill does not define profiles for when sections are required, optional, condensed, or omitted.
- The skill tells agents to gather proportional context, but does not define a minimum evidence set or when to stop exploring.
- The skill says to record questions and assumptions when clarification is unavailable, but does not require impact, default decision, or confidence metadata.
- The skill asks for concrete acceptance criteria, but does not provide examples or a standard pattern for writing requirement-to-test traceability.
- The skill mentions implementation slices, but the boundary between a lightweight slice and a downstream ticket can be clearer.
- The quality checklist verifies presence of important content, but does not force a final readiness judgment for agent handoff.

## Proposed Behavior

The skill should be revised to add five focused instruction blocks while preserving its existing mission and write boundaries.

### 1. Output Contract

Add a short "Output Contract" near the top of the skill. It should state that every generated spec must let a downstream coding agent answer:

- What problem is being solved and why now?
- What is in scope and explicitly out of scope?
- What source context was inspected?
- What decisions are confirmed versus assumed?
- What behavior must change?
- How will completion be verified?
- What risks, compatibility concerns, or operational constraints matter?
- What files, modules, systems, or interfaces are likely involved when known?

### 2. Spec-Type Profiles

Add a "Spec Type Profiles" section after intake or before the default template. The profiles should help agents tailor the artifact without inventing a new structure each time.

Recommended profiles:

- New feature/product spec: emphasize user/stakeholder needs, goals, non-goals, proposed behavior, edge cases, acceptance criteria, rollout, and verification.
- Technical design/RFC: emphasize current architecture, proposed technical behavior, alternatives considered, data/API contracts, migration, compatibility, risks, and verification.
- Bug remediation spec: emphasize observed behavior, expected behavior, reproduction evidence, suspected scope, non-regression requirements, tests, and rollback risk.
- Migration/refactor spec: emphasize invariants, compatibility, phased rollout, data/schema impact, observability, rollback, and acceptance criteria.
- UX/workflow spec: emphasize journeys, states, copy, accessibility, empty/error/loading states, screenshots or visual references when available, and manual verification.
- Existing spec review/refinement: emphasize findings, proposed changes, unresolved decisions, and a clean revised spec or patch plan, without silently overwriting user decisions.
- Agent handoff spec: emphasize source context, hard constraints, implementation boundaries, likely files, verification commands, and no-go areas.

Each profile should name sections that are required, commonly useful, and usually omit-worthy. This preserves focus while keeping the default template available.

### 3. Evidence And Context Guidance

Strengthen context review with a minimum evidence heuristic:

- Read all user-provided input files in full unless they are too large, binary, generated, or irrelevant.
- Inspect adjacent documentation or code only when it changes requirements, constraints, acceptance criteria, or verification.
- Record every source that materially shaped the spec in `Source Context` or `Source References`.
- Stop context gathering when additional reading is unlikely to change scope, requirements, risks, or verification.
- If key evidence is unavailable, record the gap as an open question or assumption with impact.

### 4. Non-Interactive Clarification Protocol

When the environment forbids live questions, the skill should require agents to proceed using a standard pattern:

- Add open questions with why each answer matters.
- Add assumptions with confidence level and invalidation condition.
- Choose conservative defaults that minimize irreversible design decisions.
- Put high-impact unresolved questions in both `Open Questions` and `Risks And Mitigations`.
- Save a short companion notes/questions file when the user explicitly requested it or when unresolved questions are material.

### 5. Agent-Ready Quality Rubric

Replace or supplement the current checklist with a brief rubric. Before finalizing, the agent should rate the spec as ready only when:

- Grounded: source context is named and important claims are traceable to inputs or assumptions.
- Scoped: goals and non-goals prevent reasonable downstream scope creep.
- Actionable: requirements describe observable behavior rather than intent.
- Verifiable: testing and acceptance criteria can be checked by commands, inspection, or manual review.
- Bounded: the spec does not create tickets, implement code, or require unrelated rewrites.
- Reviewable: a human can scan the summary, scope, risks, questions, and acceptance criteria quickly.

If a dimension is weak, the agent should either improve the artifact or mark the weakness in notes before saving.

## Requirements

- REQ-001: The skill must preserve its current mission: producing focused specification artifacts, not implementation changes or ticket decomposition.
- REQ-002: The skill must define an output contract for downstream AI coding agents.
- REQ-003: The skill must include spec-type profiles with guidance for selecting required, optional, and omittable sections.
- REQ-004: The skill must define deterministic behavior for non-interactive runs, including recorded questions and assumptions.
- REQ-005: The skill must require assumptions to include confidence and invalidation criteria when they materially affect the spec.
- REQ-006: The skill must require open questions to state why the answer matters.
- REQ-007: The skill must strengthen source-context guidance so agents record the inputs that materially shaped the spec.
- REQ-008: The skill must clarify that implementation slices are lightweight sequencing hints, not full tickets or task breakdowns.
- REQ-009: The skill must add requirement-writing guidance that favors observable behavior and discourages vague improvement language.
- REQ-010: The skill must add acceptance-criteria guidance that ties completion to inspectable behavior, tests, commands, or manual checks.
- REQ-011: The skill must add or update a final quality rubric for agent-readiness and human reviewability.
- REQ-012: The skill must keep instructions concise enough to remain usable as an active agent skill.

## Nonfunctional Requirements

- NFR-001: Maintainability: The revised skill should be organized into clear sections and avoid duplicating the same rule in multiple places.
- NFR-002: Determinism: Evaluation and non-interactive runs should not block on clarification when the prompt instructs the agent to proceed.
- NFR-003: Compatibility: Existing users who expect the current default template should still receive specs with the same core sections unless a profile justifies a focused variant.
- NFR-004: Human readability: The skill should remain easy to scan, with concise bullets and minimal tables.
- NFR-005: Agent usability: The skill should use imperative, testable instructions that are easy for coding agents to follow.

## Data, API, Or Contract Changes

No runtime data, API, or persistence contract changes are required. The only intended implementation target is the skill instruction file:

- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`

If this spec is implemented later, the skill metadata version should be bumped according to the maintainer's convention.

## Technical Context

The skill currently uses frontmatter followed by markdown instruction sections. The improvement should be applied as a focused edit to the existing structure:

- Keep the frontmatter and description aligned with the skill's trigger behavior.
- Preserve the mission and operating principles unless wording changes improve precision.
- Insert the output contract and profile guidance before the default template so agents use them before drafting.
- Keep the default template but clarify that profiles tailor it.
- Update the quality checklist into, or alongside, an agent-readiness rubric.
- Avoid editing files outside the skill source if this spec is later implemented.

## Implementation Slices

- SLICE-001: Add an `Output Contract` section and update the mission/intake language to emphasize downstream agent readiness.
- SLICE-002: Add `Spec Type Profiles` with concise guidance for required, useful, and usually omitted sections by artifact type.
- SLICE-003: Revise `Context Review` and `Clarify` to include the evidence heuristic and non-interactive clarification protocol.
- SLICE-004: Add examples or rules for writing observable requirements, verification steps, and acceptance criteria.
- SLICE-005: Replace or supplement the checklist with an agent-ready quality rubric and finalization behavior.

These slices are sequencing hints only. They should not be expanded into tickets by this skill unless a later user explicitly asks.

## Testing And Verification

- TEST-001: Inspect the revised `SKILL.md` and confirm it still contains mission, workflow, default template, agent-friendly conventions, quality checks, and write boundaries.
- TEST-002: Confirm the revised skill includes an output contract that answers the downstream-agent readiness questions in this spec.
- TEST-003: Confirm the revised skill includes at least the seven spec-type profiles listed in `Proposed Behavior`.
- TEST-004: Run a sample non-interactive prompt mentally or with an evaluation harness and verify the agent records questions and assumptions instead of blocking.
- TEST-005: Run or review a sample generated spec and confirm each material requirement has a matching verification or acceptance criterion.
- TEST-006: Confirm the revised skill does not instruct agents to create tickets, commits, implementation code, migrations, or PRs.

## Rollout, Migration, And Operations

No runtime rollout is required. If implemented, the maintainer should:

- Update the skill file in one focused change.
- Bump the skill version if versioning is used for evaluation comparisons.
- Run existing skill evaluations, including this spec-skill-improvement task and at least one agent-handoff or bug-remediation spec task.
- Compare outputs for focus, actionability, and reduced ambiguity rather than only template completeness.

## Risks And Mitigations

- RISK-001: The skill becomes too long and agents ignore parts of it. / Mitigation: Add concise sections and remove duplicative wording where possible.
- RISK-002: Spec-type profiles cause agents to omit important sections too aggressively. / Mitigation: State that profiles tailor the default template but must preserve scope, requirements, assumptions, risks, verification, and acceptance criteria.
- RISK-003: The output contract makes specs overly implementation-prescriptive. / Mitigation: Emphasize behavior, constraints, and verification while keeping implementation slices lightweight.
- RISK-004: Non-interactive assumptions hide important ambiguity. / Mitigation: Require impact, confidence, and invalidation conditions for material assumptions.
- RISK-005: Human reviewers find agent-oriented artifacts too mechanical. / Mitigation: Keep the summary, problem, goals, risks, and acceptance criteria concise and reviewable.

## Open Questions

- Q-001: Should the improved skill include short good/bad examples for requirements and acceptance criteria? This matters because examples improve consistency but increase skill length.
- Q-002: Should the skill require a companion notes/questions file in all evaluation contexts, or only when useful/requested? This matters because notes improve auditability but can create unnecessary artifacts.
- Q-003: Should implementation of this spec bump the skill version from `1.1` to `1.2` or another version? This matters for tracking evaluation comparisons.
- Q-004: Are there existing evaluation rubrics outside this file that the skill should align with? This matters because the skill's self-review rubric should not conflict with external scoring.

## Assumptions

- ASM-001: The primary implementation target is only `skills/defining-specifications/SKILL.md`. Confidence: High. Invalidated if the maintainer wants supporting examples, tests, or docs outside the skill file.
- ASM-002: The improved skill should remain a single-file skill instruction, not a multi-file workflow package. Confidence: Medium. Invalidated if future evaluations require reusable templates or examples as separate resources.
- ASM-003: The most valuable improvement is better decision guidance, not a larger default spec template. Confidence: High. Invalidated if evaluator feedback shows missing sections are a bigger issue than overgeneralization.
- ASM-004: Backward compatibility with existing generated spec structure matters because downstream agents and humans may already expect those sections. Confidence: Medium. Invalidated if the maintainer prefers a clean redesign.

## Acceptance Criteria

- AC-001: A downstream coding agent can update `SKILL.md` from this spec without asking for additional context.
- AC-002: The updated skill tells agents how to choose a focused spec shape for at least product, technical, bug, migration, UX, review, and agent-handoff tasks.
- AC-003: The updated skill tells agents exactly what to do when clarification is useful but live questioning is disallowed.
- AC-004: The updated skill requires material assumptions and open questions to include why they matter.
- AC-005: The updated skill improves acceptance-criteria and verification guidance enough that generated specs can be checked objectively.
- AC-006: The updated skill remains explicitly bounded to spec artifacts and does not authorize implementation edits, tickets, commits, branches, migrations, or PRs.
- AC-007: A human reviewer can scan the updated skill and identify the mission, workflow, profiles, default template, quality rubric, and write boundaries.

## Source References

- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`
