# Specification: Improve the `defining-specifications` Skill

Status: Draft for review  
Date: 2026-06-05  
Artifact under review: `skills/defining-specifications/SKILL.md`  
Primary consumers: AI coding agents  
Secondary consumers: human reviewers, maintainers, and project owners

## Summary

Improve the `defining-specifications` skill from a brief conversation guide into a precise operating protocol for creating spec-driven development artifacts. The improved skill should help AI coding agents gather context, clarify ambiguity, produce implementation-ready specifications, and preserve a reviewable trail of assumptions, decisions, requirements, and acceptance criteria.

The skill should remain human-readable, but its structure should be optimized for agents that need to convert rough ideas into scoped, verifiable engineering work.

## Current Seed Assessment

The current seed establishes the broad intent: guide a user from an idea or feature request into a saved specification. It also correctly emphasizes read-only context gathering, user refinement, workspace review, and writing the final specification to a file.

However, it is not yet specific enough to reliably produce strong spec-driven development artifacts:

- The frontmatter appears malformed because the `description` string is opened but not clearly closed before `metadata`.
- The trigger is broad and may fire for casual mentions of specifications, reviews, or ideas without distinguishing when a full specification workflow is appropriate.
- The workflow says to refine through conversation, but does not define what to ask, how many questions to ask, what to do when the user cannot answer, or how to proceed in no-interaction contexts.
- The expected output structure is underspecified. Agents are told to create a specification, but not what sections, identifiers, traceability, acceptance criteria, or implementation planning detail the artifact should contain.
- The skill mentions workspace context, UX review, databases, question tools, and todo tools, but does not define boundaries, priority order, or failure modes for those tools.
- The file-writing constraints are useful but ambiguous when multiple spec files are allowed.
- There is no quality gate for determining whether a generated spec is ready for implementation, ready for human review, or still blocked by unresolved questions.

## Goals

1. Make the skill deterministic enough for AI coding agents to follow consistently across repositories and task types.
2. Produce specifications that are directly useful for implementation planning, ticket decomposition, test design, and review.
3. Keep specifications readable by humans while adding stable structure that agents can parse and update.
4. Preserve clear distinctions between facts from source context, user decisions, agent assumptions, open questions, and recommendations.
5. Encourage bounded clarification instead of endless interviewing.
6. Preserve safe workspace behavior: read broadly when needed, write only the requested specification artifacts, and avoid implementation edits.
7. Support both interactive use and evaluation or automation contexts where the agent must proceed without asking the user live questions.

## Non-Goals

1. The skill should not implement the feature described by the specification.
2. The skill should not replace a ticket workflow, project management system, or architecture review process, though it may produce implementation slices that can become tickets.
3. The skill should not prescribe a single software architecture, technology stack, or documentation style for all projects.
4. The skill should not force a large formal document for tiny changes where a short spec is sufficient.
5. The skill should not invent product or technical decisions without marking them as assumptions or recommendations.

## Target Users and Use Cases

### AI Coding Agents

Agents use the skill to create a reliable bridge between ambiguous user intent and implementation-ready engineering work. They need stable headings, explicit identifiers, source references, and testable acceptance criteria.

### Human Reviewers

Humans use the resulting spec to quickly verify scope, product intent, tradeoffs, risks, and whether the implementation plan matches their expectations.

### Common Use Cases

- Turning a rough feature idea into a development specification.
- Reviewing and strengthening an existing specification.
- Converting bug reports or product feedback into scoped remediation specs.
- Defining refactors, migrations, or architecture changes before implementation.
- Preparing agent-readable context for future coding sessions.

## Improved Skill Behavior

### 1. Invocation Criteria

The improved skill should activate when the user explicitly asks to create, draft, refine, audit, review, or improve a specification, spec, product requirements document, implementation plan, design document, or similar planning artifact.

It may also activate when the user presents a sufficiently ambiguous feature idea and asks for help defining it before implementation.

It should not activate for simple direct edits, ordinary code review, debugging, or implementation tasks unless the user asks for a spec first.

### 2. Intake Protocol

At the start, the agent should identify:

- The requested artifact type: new spec, spec review, implementation spec, product spec, migration spec, bug remediation spec, or architecture spec.
- The intended audience: coding agent, human reviewer, product stakeholder, or mixed.
- The expected output location and filename, if specified.
- Whether the user wants an interactive interview or wants the agent to proceed with recorded assumptions.
- Known constraints: deadlines, compatibility needs, systems affected, security or privacy requirements, and non-goals.

The agent should restate the understood goal briefly before deep exploration when useful.

### 3. Context Gathering Protocol

The improved skill should instruct agents to gather enough context to make the specification grounded but not exhaustive.

Required context sources:

- All user-provided notes, attachments, linked files, or pasted requirements.
- Existing specifications or documentation directly referenced by the user.
- Relevant repository files, including code, tests, schemas, APIs, configuration, and architecture docs.

Conditional context sources:

- Browser or UI inspection when the spec affects user-facing flows, visual behavior, or interaction design.
- Database, analytics, or operational data only when the user has provided access and the request depends on that data.
- External documentation only when library, framework, platform, or API behavior materially affects the spec.

The agent should keep a concise source inventory in the resulting spec. Source references should use stable paths, document names, URLs, or tool-provided identifiers. When evidence is weak or inferred, the spec should say so.

### 4. Clarifying Question Protocol

The improved skill should avoid both extremes: producing a speculative spec without checking critical unknowns, and blocking progress with too many questions.

Recommended behavior:

- Ask only high-leverage questions that materially change scope, architecture, UX, data model, rollout, or acceptance criteria.
- Group questions by theme when there are several.
- Prefer 3 to 7 questions in an initial clarification pass.
- If the user asks the agent to proceed, or if the environment does not allow live clarification, record assumptions and continue.
- Mark unresolved issues as `Open Question` entries with IDs.

Blocking questions should be reserved for cases where proceeding would create a misleading or unsafe artifact.

### 5. Specification Output Structure

The improved skill should define a default markdown template with stable headings. Agents may omit irrelevant sections for small specs, but should preserve the core structure.

Recommended default template:

```markdown
# Specification: <Title>

Status: Draft | Ready for Review | Approved
Date: <YYYY-MM-DD>
Owner/Requester: <Name if known>
Primary Consumers: AI coding agents, humans, or both
Source Context: <brief list or link to appendix>

## Executive Summary
<One to three paragraphs describing the desired outcome and why it matters.>

## Problem Statement
<Current pain, opportunity, or failure mode.>

## Goals
- G-001: <Goal>

## Non-Goals
- NG-001: <Explicitly excluded scope>

## Users and Stakeholders
- <User or stakeholder>: <Need or concern>

## Current State
<Relevant system behavior, files, flows, data, constraints, or prior decisions.>

## Proposed Behavior
<Target behavior from product and system perspectives.>

## Requirements
- REQ-001: <Testable functional requirement>

## Nonfunctional Requirements
- NFR-001: <Performance, reliability, privacy, accessibility, security, or maintainability requirement>

## UX and Workflow
<User journeys, states, edge cases, empty states, errors, accessibility notes, and copy requirements if applicable.>

## Data, API, and Contract Changes
<Models, schemas, endpoints, events, migrations, backwards compatibility, and integration contracts.>

## Technical Approach
<Affected components, architecture, sequencing, dependencies, and alternatives considered.>

## Implementation Slices
- SLICE-001: <Small reviewable unit of work with expected files or modules>

## Testing and Verification
- TEST-001: <Unit, integration, e2e, manual, migration, or observability check>

## Rollout and Operations
<Migration, feature flags, monitoring, rollback, support, and documentation needs.>

## Risks and Mitigations
- RISK-001: <Risk> / Mitigation: <Mitigation>

## Open Questions
- Q-001: <Question and why it matters>

## Assumptions
- ASM-001: <Assumption and confidence level>

## Acceptance Criteria
- AC-001: <Observable condition that indicates the work satisfies the spec>

## Source References
- <Path, URL, transcript, issue, or artifact>
```

### Agent-Friendly Requirements

The improved skill should require stable identifiers for goals, non-goals, requirements, assumptions, open questions, risks, tests, and acceptance criteria when the spec is more than a short one-page artifact.

Recommended prefixes:

- `G-###` for goals.
- `NG-###` for non-goals.
- `REQ-###` for functional requirements.
- `NFR-###` for nonfunctional requirements.
- `SLICE-###` for implementation slices.
- `TEST-###` for verification tasks.
- `AC-###` for acceptance criteria.
- `RISK-###` for risks.
- `Q-###` for open questions.
- `ASM-###` for assumptions.
- `DEC-###` for explicit decisions.

These identifiers make the document easier for future agents to reference, update, test against, and decompose into tickets.

### Human Review Requirements

The spec should avoid opaque agent-only formatting. Each section should contain readable prose or concise bullets. Tables may be used when they improve clarity, but the skill should not require large tables for every spec.

The top of the spec should make review status obvious: draft, ready for review, approved, or blocked.

## Quality Gate

Before finalizing a specification, the agent should check that:

1. The problem, goals, and non-goals are clear.
2. Requirements are testable and do not silently include unresolved assumptions.
3. Acceptance criteria map back to the stated goals and requirements.
4. Major edge cases, error states, and compatibility concerns are addressed or explicitly deferred.
5. The implementation slices are small enough for reviewable coding work.
6. Testing guidance covers the highest-risk behavior.
7. Open questions are separated from assumptions and decisions.
8. The source context is listed so reviewers can audit the basis of the spec.
9. The spec does not modify or depend on unrelated implementation details outside the requested scope.
10. The output file is saved in the requested location, or in a documented default location if none was provided.

If the quality gate fails, the agent should either revise the spec or mark the document status as `Draft` or `Blocked` with clear reasons.

## File Output Rules

The improved skill should make output behavior explicit:

- Save one canonical specification file by default.
- Use the user's requested output directory when provided.
- If no output location is provided, save to `docs/specs/`.
- Use a predictable filename such as `SPEC-<kebab-case-description>-<YYYY-MM-DD>.md`.
- Create supplementary files only when useful, such as `notes-questions.md`, `source-inventory.md`, or split specs for large programs.
- Ask before creating multiple primary specification files in interactive contexts.
- In no-interaction contexts, create supplementary files only when they reduce ambiguity for future agents or reviewers.

The skill should retain the existing safety intent: write only the specification artifacts and do not edit implementation code, tickets, source documentation, or configuration unless the user explicitly requests that in a separate task.

## Recommended Revised Skill Outline

The improved `SKILL.md` should roughly contain:

1. Valid frontmatter with a concise trigger description.
2. A short "Purpose" section focused on converting ambiguity into implementation-ready specifications.
3. A "When to Use / When Not to Use" section.
4. A "Workflow" section covering intake, context gathering, clarification, drafting, review, and saving.
5. A "Clarifying Questions and Assumptions" section.
6. A "Default Specification Template" section.
7. A "Quality Checklist" section.
8. A "File and Workspace Constraints" section.
9. A "Output Summary" section describing what to report to the user after saving the spec.

## Acceptance Criteria for the Skill Improvement

- AC-001: The skill file has valid frontmatter that can be parsed by the host skill system.
- AC-002: The trigger description clearly targets specification creation, refinement, and review without over-triggering on unrelated implementation tasks.
- AC-003: The skill distinguishes interactive workflows from proceed-with-assumptions workflows.
- AC-004: The skill instructs agents to gather and cite relevant source context before drafting substantive specs.
- AC-005: The skill includes a reusable markdown template with stable headings and agent-friendly identifiers.
- AC-006: The skill defines how to record assumptions, open questions, decisions, risks, and acceptance criteria.
- AC-007: The skill includes a quality checklist agents can run before finalizing the output.
- AC-008: The skill preserves write boundaries and makes clear that implementation code should not be edited during spec creation.
- AC-009: The skill gives deterministic output location and naming rules while respecting user-provided paths.
- AC-010: The resulting specs are useful to both AI coding agents and human reviewers.

## Evaluation Plan

Evaluate the improved skill against a small set of representative prompts:

1. A vague feature idea with missing requirements.
2. A repository-grounded implementation request that requires reading existing code and tests.
3. A UX-affecting change that requires current-state review.
4. A migration or refactor request with compatibility and rollout concerns.
5. A no-interaction evaluation prompt where the agent must proceed with assumptions.

For each prompt, assess:

- Whether the agent gathered relevant context.
- Whether assumptions and open questions were explicit.
- Whether requirements and acceptance criteria were testable.
- Whether the implementation slices were actionable.
- Whether the artifact stayed within the requested output boundaries.
- Whether a human reviewer could quickly understand scope, risk, and next steps.

## Risks and Mitigations

- RISK-001: The improved skill may encourage overly long specs for small changes.  
  Mitigation: Allow agents to omit irrelevant sections and produce lightweight specs when scope is narrow.

- RISK-002: Agents may treat assumptions as facts.  
  Mitigation: Require explicit `Assumptions` and `Open Questions` sections, with confidence levels for important assumptions.

- RISK-003: Stable identifiers may feel heavy for human readers.  
  Mitigation: Require identifiers only for medium or large specs, and keep prose readable.

- RISK-004: Context gathering may become too broad.  
  Mitigation: Direct agents to gather enough context for confidence, not exhaustive repository knowledge.

## Assumptions

- ASM-001: "Spec-driven development artifacts" includes product specs, implementation specs, architecture specs, migration specs, and bug remediation specs.
- ASM-002: The improved skill should serve future AI coding sessions, not only the current conversation.
- ASM-003: Human reviewability matters, but deterministic agent execution is the primary optimization target.
- ASM-004: The skill should stay general across repositories and should not encode project-specific conventions beyond safe defaults.

## Open Questions

- Q-001: Should the improved skill include a fully worked example spec, or would that make the skill too long?
- Q-002: Should the skill require source references in every spec, or only when repository/filesystem context was used?
- Q-003: Should implementation slices be mandatory, or optional for product-only specs?
- Q-004: Should the skill integrate with a separate ticket workflow when one exists, or only prepare content that can later become tickets?
- Q-005: Should the skill specify a maximum number of clarification questions before drafting?

