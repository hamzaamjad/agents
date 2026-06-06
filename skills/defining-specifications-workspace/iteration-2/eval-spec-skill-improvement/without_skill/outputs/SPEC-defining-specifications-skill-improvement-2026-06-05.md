# Specification: Improve Defining Specifications Skill

Status: Ready for Review
Date: 2026-06-05
Owner/Requester: Hamza Amjad
Primary Consumers: AI coding agents, human reviewers
Source Context:
- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`

## Summary

Improve the `defining-specifications` skill so it more reliably produces implementation-ready, agent-consumable software specifications from rough requests, existing notes, code context, or draft specs. The revised skill should preserve its current focus on specification artifacts while giving agents sharper guidance on spec depth, evidence collection, structure selection, ambiguity handling, and final quality gates.

The main outcome is not a broader or longer skill. It is a more operational skill that helps a future AI coding agent write specs that reduce downstream guessing: clear scope, stable IDs, explicit constraints, traceable source context, objective acceptance criteria, and a compact record of decisions, assumptions, and open questions.

## Problem Statement

The current seed already defines a solid mission, workflow, default template, stable ID conventions, quality checklist, and write boundaries. However, it can still allow inconsistent outputs because it does not strongly distinguish between different kinds of specs, does not define minimum viable context for downstream implementation, and leaves important decisions to the agent's judgment without concrete heuristics.

For AI coding agents, underspecified specs create predictable failure modes: scope creep, invented requirements, missing edge cases, vague acceptance criteria, weak verification steps, and confusion between confirmed facts and assumptions. The improved skill should make the best behavior easier and more repeatable without forcing every request into a heavy one-size-fits-all document.

## Goals

- G-001: Make specs more actionable for downstream AI coding agents by strengthening requirements around source grounding, scope boundaries, explicit assumptions, and verification.
- G-002: Preserve human reviewability through concise structure, readable prose, and clear separation of facts, decisions, risks, and unresolved questions.
- G-003: Add guidance for selecting spec depth and shape based on request complexity instead of always using the full default template.
- G-004: Improve ambiguity handling in non-interactive or evaluation contexts by requiring recorded assumptions and clarifying questions without blocking progress.
- G-005: Define concrete quality gates that an agent can apply before saving or returning a final spec.
- G-006: Keep the skill scoped to specification work and prevent drift into ticket creation, implementation planning, or code edits unless explicitly requested.

## Non-Goals

- NG-001: Do not rewrite the skill into a ticketing, project management, or implementation execution skill.
- NG-002: Do not require every spec to include every possible template section when a smaller focused artifact would be clearer.
- NG-003: Do not prescribe repository-specific paths beyond the existing default conventions and user-provided output locations.
- NG-004: Do not optimize for product-only PRDs at the expense of implementation-ready engineering specs.
- NG-005: Do not add external tool dependencies or require live user clarification in contexts where the user explicitly asked the agent to proceed.

## Users And Stakeholders

- AI coding agents: Need stable, complete enough instructions to plan, implement, test, and verify without reconstructing prior context.
- Human reviewers: Need to quickly validate scope, intent, assumptions, risks, and whether the proposed work is ready to hand off.
- Skill maintainer: Needs the skill to stay concise, reusable, and compatible with different repositories and agent environments.
- Requester/product owner: Needs unresolved decisions and tradeoffs surfaced clearly before implementation begins.

## Current State

The current `SKILL.md` includes:

- A clear mission to create focused, durable specs for spec-driven development.
- Two target audiences: future AI coding agents and human reviewers.
- Operating principles covering source-of-truth behavior, critical ambiguity handling, focus, evidence, and checkable completion.
- A five-step workflow: intake, context review, clarify, outline and confirm, write the spec.
- A broad default spec template with stable IDs, requirements, testing, risks, assumptions, and acceptance criteria.
- Agent-friendly conventions and a quality checklist.
- Write boundaries preventing source edits, tickets, commits, implementation code, and broad docs changes.

Important gaps:

- The skill does not define spec profiles for small, medium, large, bug, migration, UX, or agent-handoff cases.
- The skill says to inspect relevant context but does not define what source evidence must be recorded for downstream agents.
- The skill includes a template but does not define how to prune or adapt it without losing essential substance.
- Acceptance criteria guidance is present but not detailed enough to prevent vague or subjective criteria.
- The skill does not explicitly require traceability from goals to requirements to verification.
- The skill has limited guidance for reviewing or refining an existing spec versus drafting a new one.
- The skill does not include examples of good versus weak requirement phrasing.

## Proposed Behavior

Revise the skill so agents follow a profile-driven specification workflow:

1. Classify the request by artifact type and complexity.
2. Gather proportional source context and record what was inspected.
3. Choose an appropriate spec profile and section set.
4. Resolve or record ambiguity depending on whether interaction is allowed.
5. Draft a spec with stable IDs, source-grounded facts, scoped requirements, objective verification, and explicit non-goals.
6. Run a final quality gate before saving or returning the artifact.

The skill should encourage compact specs for simple changes and more complete specs for cross-system, user-facing, data, security, migration, or high-risk work. It should make the resulting document easy for a coding agent to execute from, while still allowing a human reviewer to scan it quickly.

## Requirements

- REQ-001: The revised skill must add a "Spec Profile Selection" section that helps agents choose between at least these profiles: lightweight change spec, implementation-ready feature spec, bug remediation spec, migration/refactor spec, UX/workflow spec, and existing spec review/refinement.
- REQ-002: Each profile must define required sections, optional sections, and when to escalate to a fuller spec.
- REQ-003: The revised skill must define a minimum context record for every spec: user request, directly referenced artifacts, inspected files or docs, relevant constraints, and any unavailable context that shaped assumptions.
- REQ-004: The revised skill must instruct agents to distinguish confirmed facts, inferred assumptions, user decisions, and open questions using explicit labels or sections.
- REQ-005: The revised skill must strengthen acceptance criteria guidance so criteria are observable, binary or reviewable, tied to requirements where practical, and avoid subjective wording.
- REQ-006: The revised skill must require verification guidance that names concrete checks, such as tests, commands, file inspection, browser/manual review, migration validation, or documentation review, without inventing commands unsupported by context.
- REQ-007: The revised skill must include guidance for traceability between goals, requirements, testing, and acceptance criteria for medium or larger specs.
- REQ-008: The revised skill must add a non-interactive mode rule: when clarification is disallowed, agents must proceed with documented questions, assumptions, and confidence levels instead of blocking.
- REQ-009: The revised skill must clarify how to handle existing draft specs: preserve confirmed user decisions, mark proposed changes, call out contradictions, and avoid silently replacing intent.
- REQ-010: The revised skill must keep implementation slices lightweight and explicitly separate them from detailed tickets or task decomposition.
- REQ-011: The revised skill must include examples of weak versus strong requirements, acceptance criteria, and assumptions.
- REQ-012: The revised skill must include final artifact naming and output-path behavior that respects explicit user paths over defaults.
- REQ-013: The revised skill must preserve write boundaries: no source edits, tickets, branches, commits, PRs, migrations, tests, or implementation code unless separately requested.
- REQ-014: The revised skill must avoid requiring large tables; tables may be allowed only when they improve scanability or traceability.
- REQ-015: The revised skill must tell agents to scale investigation to risk and avoid broad codebase exploration when the request is narrow.

## Nonfunctional Requirements

- NFR-001: The revised skill should remain concise enough for agents to read quickly; target a focused operational guide rather than a comprehensive writing manual.
- NFR-002: The revised skill should be model-agnostic and tool-agnostic, avoiding references that assume one host environment unless already present in the workspace.
- NFR-003: The revised skill should optimize for reliability under context pressure by prioritizing durable sections and stable IDs over long prose.
- NFR-004: The revised skill should be safe in dirty worktrees by reinforcing read-only source inspection and output-only writes.
- NFR-005: The revised skill should support both interactive user sessions and automated evaluation runs.

## Suggested Skill Structure

The improved `SKILL.md` should retain the existing frontmatter and top-level mission, then reorganize the body around operational decisions:

- Mission and output boundaries.
- Operating principles.
- Workflow.
- Spec profile selection.
- Context and evidence requirements.
- Clarification and non-interactive behavior.
- Default template with pruning guidance.
- Agent-friendly writing rules.
- Examples of strong and weak spec language.
- Final quality gate.
- Write boundaries.

The current default template can stay, but it should be framed as a base template rather than a mandatory full document. The skill should explicitly say which sections are core for nearly every spec: summary, problem/current state, goals, non-goals, requirements, verification, open questions or assumptions, acceptance criteria, and source references.

## Detailed Guidance To Add

### Spec Profiles

Add compact guidance like:

- Lightweight change spec: for narrow, low-risk changes; requires summary, scope, requirements, verification, acceptance criteria, assumptions/questions, and sources.
- Feature or system spec: for new behavior or cross-module changes; requires the full core template plus stakeholders, current/proposed behavior, risks, and rollout when relevant.
- Bug remediation spec: requires observed behavior, expected behavior, reproduction or evidence, suspected affected areas, requirements, regression tests, risks, and acceptance criteria.
- Migration or refactor spec: requires compatibility constraints, rollout/migration plan, invariants to preserve, verification strategy, risks, and rollback or recovery notes when relevant.
- UX/workflow spec: requires user journeys, states, empty/error/loading cases, accessibility and copy constraints, manual/browser verification, and acceptance criteria.
- Existing spec review/refinement: requires findings, proposed edits, preserved decisions, contradictions, open questions, and revised spec or patch plan depending on user request.

### Context Record

Require agents to include a concise source context section that answers:

- What files, docs, tickets, transcripts, or URLs were inspected?
- Which facts came from those sources?
- What context was unavailable or intentionally not inspected?
- What assumptions fill the gaps?

### Acceptance Criteria Rules

Acceptance criteria should:

- Be observable through tests, commands, code review, UI review, or file inspection.
- Reference requirement IDs for medium and large specs when practical.
- Avoid subjective phrases such as "better", "clean", "easy", or "robust" unless paired with observable evidence.
- Include negative or boundary cases when those are central to scope.

### Traceability

For medium and larger specs, require a lightweight traceability pattern:

- Goals explain why the work matters.
- Requirements define what must change.
- Verification defines how to check it.
- Acceptance criteria define when the work is complete.

This does not need a table unless the spec is complex enough that mapping IDs improves review.

### Final Quality Gate

Before finalizing, the agent should verify:

- The spec can stand alone for a future coding agent.
- Scope boundaries and non-goals are explicit.
- Requirements are specific and testable.
- Verification is concrete and realistic.
- Assumptions and open questions are recorded.
- Source references are present.
- Output path and write boundaries match the user request.
- The spec does not include implementation code or ticket decomposition unless requested.

## Implementation Slices

- SLICE-001: Revise the workflow text to include profile selection, source evidence, and non-interactive clarification behavior.
- SLICE-002: Add a spec profile selection section with required/optional sections and escalation triggers.
- SLICE-003: Update the default template guidance so it can be pruned safely while preserving core sections.
- SLICE-004: Add examples of weak versus strong requirements, acceptance criteria, and assumptions.
- SLICE-005: Replace or augment the existing quality checklist with a final quality gate optimized for downstream AI coding agents.

These slices are intentionally lightweight. They are not tickets and do not prescribe exact line-level edits.

## Testing And Verification

- TEST-001: Review the revised skill against this specification and confirm each requirement is addressed explicitly or intentionally rejected with rationale.
- TEST-002: Run a dry-read exercise: given a simple feature request, confirm the skill leads to a compact spec rather than an unnecessarily large document.
- TEST-003: Run a dry-read exercise: given a cross-module migration request, confirm the skill prompts for compatibility, rollout, risks, and verification.
- TEST-004: Run a dry-read exercise: given a non-interactive evaluation task, confirm the skill records questions and assumptions without blocking.
- TEST-005: Inspect the revised skill for write-boundary regressions; it must not encourage source edits or ticket creation as part of normal spec work.
- TEST-006: Confirm examples use stable IDs and demonstrate concrete, observable language.

## Rollout, Migration, And Operations

No runtime rollout is required. The change is a documentation/instruction update to a skill file. The maintainer should preserve the existing skill name and triggering intent unless a separate evaluation shows the description is misfiring.

If the revised skill changes frontmatter description or metadata, the maintainer should verify it still triggers for specification drafting, spec review/refinement, product requirements, RFCs, and AI-agent handoff requests, while not triggering for ordinary code review or ticket decomposition unless the user asks for a specification.

## Risks And Mitigations

- RISK-001: The skill becomes too long and agents ignore important guidance. / Mitigation: Keep examples compact and put decision-critical guidance before optional template details.
- RISK-002: Profile selection makes agents over-classify simple requests. / Mitigation: Include an explicit "choose the smallest profile that satisfies the risk" rule.
- RISK-003: Stronger verification guidance causes agents to invent tests or commands. / Mitigation: Require verification to be grounded in inspected context or phrased as manual/file-inspection checks when commands are unknown.
- RISK-004: The revised skill drifts into implementation planning. / Mitigation: Preserve boundaries and keep implementation slices lightweight and optional.
- RISK-005: Human readability suffers if traceability becomes too mechanical. / Mitigation: Use ID references and short bullets by default; reserve tables for complex specs only.

## Open Questions

- Q-001: Should the improved skill include a short complete example spec, or only examples of individual requirement/acceptance-criteria phrasing? This matters because full examples improve consistency but increase skill length.
- Q-002: Should the frontmatter version be incremented as part of the improvement? This matters for maintainability, but versioning policy was not provided.
- Q-003: Should the skill define a maximum recommended spec length by profile? This could help prevent overproduction, but hard limits may be brittle across tasks.
- Q-004: Should the default output path remain `./docs/specs/`, or should the skill recommend repository-specific convention discovery first? The current default is simple, but some repos may already use a different spec location.

## Assumptions

- ASM-001: The desired improvement is to revise the skill's instructions, not to create a separate downstream template library. Confidence: high. Invalidated if the maintainer wants multiple supporting files.
- ASM-002: The primary quality issue to optimize is downstream agent execution reliability. Confidence: high. Invalidated if human product review is the dominant target.
- ASM-003: The skill should remain broadly reusable across repositories and host environments. Confidence: medium. Invalidated if this workspace intends skills to be tightly Cursor-specific.
- ASM-004: The existing mission, stable ID convention, and write boundaries are worth preserving. Confidence: high. Invalidated if prior evaluations show those sections are causing failures.

## Acceptance Criteria

- AC-001: The improved skill includes spec profile selection with required sections and escalation guidance.
- AC-002: The improved skill tells agents how to record inspected source context, unavailable context, assumptions, and open questions.
- AC-003: The improved skill includes concrete rules for writing testable requirements and observable acceptance criteria.
- AC-004: The improved skill supports non-interactive runs by proceeding with documented assumptions and questions.
- AC-005: The improved skill clearly distinguishes spec writing from ticket creation, implementation planning, and source edits.
- AC-006: The improved skill remains concise and reviewable by a human maintainer.
- AC-007: A downstream AI coding agent can use a spec produced under the improved skill without relying on the original chat for scope, requirements, constraints, or verification.

## Source References

- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`
