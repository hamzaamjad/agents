---
name: defining-specifications
description: "Create, review, or refine focused software specifications for spec-driven development. Use this skill whenever the user asks to draft a spec, define an idea, formalize rough notes, write product requirements, create an implementation-ready design/RFC, review an existing spec, or prepare an agent handoff before coding. Especially use when the primary consumer of the artifact is an AI coding agent. Do not use for direct implementation, ordinary code review, or ticket decomposition unless the user asks for a specification first."
metadata:
  author: "Hamza Amjad"
  version: "1.2"
---

# Specification Creator

## Mission

Create focused, durable specification documents that convert rough ideas, feature requests, bug reports, refactors, migrations, UX changes, or existing draft specs into agent-consumable engineering artifacts.

Optimize for two readers:

- Future AI coding agents that need stable structure, explicit constraints, source context, and verifiable acceptance criteria.
- Human reviewers who need to quickly confirm intent, scope, risks, and unresolved decisions.

This skill produces specifications only. Tickets, task decomposition, implementation plans, and code changes are downstream artifacts unless the user explicitly asks to include lightweight implementation slices inside the spec.

## Operating Principles

- Treat the spec as the source of truth for downstream agent work. It should stand alone without requiring the next agent to reconstruct the chat.
- Be constructively critical. Surface ambiguity, contradictions, missing constraints, and risky assumptions before writing final artifacts.
- Keep the artifact focused. Prefer one coherent spec over a broad documentation rewrite. If multiple focused specs are justified, ask before creating them.
- Ground the spec in evidence. Read user-provided inputs in full and inspect relevant workspace context read-only. Never present an inference as a fact: cite the file, doc, or command behind any claim, and label unverified API names, dependency versions, or system behavior as assumptions rather than requirements. Avoid "typically the system does X" unless you can point to the evidence.
- Separate facts, decisions, assumptions, and open questions. Future agents need to know which parts are confirmed and which are inferred, and which questions are still blocking.
- Calibrate specificity. Specify *what* and *why* (behavior, constraints, acceptance), and defer *how* (implementation choices) to the downstream agent unless a constraint forces a choice. Over-specifying invented implementation detail is as harmful as under-specifying behavior; apply YAGNI and KISS to each requirement.
- Make completion objectively checkable. Write functional requirements in EARS form and acceptance criteria as Given/When/Then by default (see `references/requirements-and-acceptance-criteria.md`), concrete enough for tests, commands, file inspection, or manual review.

## Workflow

### 1. Intake

Read the user's request and all directly attached or referenced inputs before drafting. Identify:

- The artifact type: new spec, spec review, product requirements, implementation-ready design, RFC, bug remediation spec, migration spec, UX spec, or agent handoff.
- The system, feature, behavior, or document being specified.
- The intended audience and primary consumer.
- Any requested output path, filename, status, format, or review process.
- Constraints, non-goals, deadlines, compatibility requirements, security/privacy concerns, and affected users.

Use your to-do list tool when present for non-trivial spec work.

### 2. Context Review

Gather enough context to make the spec grounded, but keep exploration proportional.

Read-only sources to consider:

- User notes, attachments, linked files, existing specs, tickets, issues, READMEs, rules, ADRs, and design docs.
- Relevant code, tests, schemas, API contracts, configuration, logs, data models, and module boundaries.
- Existing UX/UI through browser or visual tools when the request affects user-facing flows, interaction design, visual states, accessibility, or copy.
- Database, analytics, or operational data only when the user has provided access and the spec depends on it.
- Current external docs when library, framework, platform, SDK, or API behavior materially affects the specification.

Record important sources in the spec. Do not perform writes outside the generated spec artifacts.

### 3. Clarify

Ask focused questions before writing when interaction is allowed and the answers would materially change scope, architecture, UX, data contracts, rollout, or acceptance criteria.

Use your question asking tool when present. Prefer:

- Simple spec: up to 3 questions.
- Medium spec: up to 5 questions.
- Large or ambiguous spec: up to 7 questions grouped by theme.

Do not ask questions that can be answered by reading available context. If the user asks you to proceed, or the environment does not allow live clarification, write the questions and your working assumptions into the spec and continue.

### 4. Outline And Confirm

Before writing final files, share a short outline for confirmation when the user has not already approved a structure. Include:

- Proposed spec title and output path.
- Major sections.
- Key scope boundaries.
- Any assumptions that would materially affect the final artifact.

If the user explicitly asked you to proceed without another checkpoint, or the task is running in an evaluation/non-interactive context, include the outline or assumptions in the output instead of blocking.

### 5. Write The Spec

Unless the user requests otherwise:

- Save specs under `./docs/specs/`.
- Use filename format `SPEC-{{short-kebab-description}}-{{YYYY-MM-DD}}.md`.
- Create the output directory if it does not exist.
- Write only the spec file and, when useful, one companion notes/questions file.
- Start from the default template, then apply the matching spec-type profile from `references/spec-type-profiles.md` (feature, bug, refactor, migration, UX, or agent handoff).
- Write functional requirements in EARS form and acceptance criteria as Given/When/Then, mapping each criterion back to the requirement IDs it verifies. See `references/requirements-and-acceptance-criteria.md` for templates, when not to use EARS, and worked examples.

If modifying an existing spec, prefer updating it in place: preserve its filename and structure, add a short changelog/date entry, and avoid spawning a near-duplicate spec. Do not silently replace user-authored decisions; mark proposed changes clearly or ask first.

### 6. Self-Review Before Handoff

Before presenting the spec, run the Quality Checklist below as a gate. Keep `Status: Draft` until the checklist passes and decision-critical open questions are resolved or explicitly accepted; only then move to `Ready for Review`. Unresolved blocking questions stay visible in `Open Questions` — never resolve them by guessing. When a blocking question is resolved during review, record the resolution as a `DEC-###` entry in `Decisions` and mark the `Q-###` item resolved with a pointer to that entry, rather than deleting the question.

## Default Spec Template

Use this structure by default. Omit sections only when clearly irrelevant, but preserve the core substance: scope, requirements, assumptions, risks, verification, and acceptance criteria.

```markdown
# Specification: <Title>

Status: Draft | Ready for Review | Approved | Blocked
Date: <YYYY-MM-DD>
Owner/Requester: <Name if known>
Primary Consumers: AI coding agents, human reviewers
Source Context: <brief list of key files, docs, URLs, or artifacts>

## For Implementing Agents
<Short orientation for the downstream agent: which sections are authoritative (Requirements, Acceptance Criteria, Non-Goals), that Assumptions are unconfirmed and Open Questions are blockers to surface rather than guess, and any constraints that override defaults.>

## Summary
<One to three paragraphs describing the desired outcome and why it matters.>

## Problem Statement
<Current pain, opportunity, failure mode, or decision to formalize.>

## Goals
- G-001: <Goal>

## Non-Goals
- NG-001: <Explicitly excluded scope>

## Users And Stakeholders
- <User or stakeholder>: <Need or concern>

## Current State
<Relevant system behavior, files, flows, data, constraints, or prior decisions.>

## Proposed Behavior
<Target behavior from product and system perspectives.>

## Requirements
- REQ-001: <Testable functional requirement in EARS form, e.g. "When <trigger>, the <system> shall <response>." See references for patterns.>

## Nonfunctional Requirements
- NFR-001: <Performance, reliability, privacy, accessibility, security, maintainability, or operability requirement>

## UX, Workflow, Or Interaction Notes
<User journeys, states, edge cases, empty states, errors, accessibility notes, and copy requirements if applicable.>

## Data, API, Or Contract Changes
<Models, schemas, endpoints, events, migrations, backwards compatibility, and integration contracts if applicable.>

## Technical Context
<Affected components, constraints, integration points, alternatives considered, and implementation guidance that belongs in the spec.>

## Implementation Slices
- SLICE-001: <Optional small reviewable unit of work. Keep this lightweight; detailed tickets are downstream.>

## Testing And Verification
- TEST-001: <Unit, integration, e2e, manual, migration, observability, or file-inspection check>

## Rollout, Migration, And Operations
<Feature flags, migrations, monitoring, rollback, support, and docs needs if applicable.>

## Risks And Mitigations
- RISK-001: <Risk> / Mitigation: <Mitigation>

## Decisions
- DEC-001: <decision> — Rationale: <why>. Alternatives considered: <list>. Date: <YYYY-MM-DD>.

## Open Questions
- Q-001: <Question and why it matters>

## Assumptions
- ASM-001: <Assumption, confidence level, and what would invalidate it>

## Acceptance Criteria
- AC-001 (verifies REQ-001): Given <context>, When <action>, Then <observable outcome>.

## Source References
- <Path, URL, issue, ticket, transcript reference, or artifact>
```

## Agent-Friendly Conventions

- Use stable IDs for anything future agents may reference: `G-###`, `NG-###`, `REQ-###`, `NFR-###`, `SLICE-###`, `TEST-###`, `AC-###`, `RISK-###`, `Q-###`, `ASM-###`, and `DEC-###`.
- Write functional requirements in EARS form (`shall`, with `While`/`When`/`If-Then`/`Where` as appropriate) so the requirement type and trigger are explicit. Fall back to tables, formulas, or JSON when a single sentence would distort the requirement. Avoid vague intent like "make it better", "improve UX", or "handle errors".
- Write acceptance criteria as Given/When/Then scenarios that name the requirement IDs they verify, so traceability runs `REQ -> AC -> TEST`. Every non-trivial requirement should be reachable from at least one acceptance criterion.
- Keep implementation slices optional and lightweight. This skill may prepare a spec for a ticketing skill, but it should not create tickets or full task decompositions.
- Include explicit non-goals. They are high-leverage guardrails for coding agents and prevent scope creep.
- Include source references whenever workspace context influences the spec.
- Use concise prose and bullets. Avoid large tables unless they materially improve clarity.
- See `references/requirements-and-acceptance-criteria.md` for EARS/GWT detail and `references/spec-type-profiles.md` for per-type structure.

## Quality Checklist

Before finalizing, verify that the spec:

- Has a clear title, status, date, primary consumers, source context, and a `For Implementing Agents` orientation block.
- States the problem, goals, non-goals, current state, and proposed behavior, applying the matching spec-type profile.
- Uses stable IDs for requirements, acceptance criteria, questions, assumptions, and risks when the spec is more than a very small artifact.
- Writes functional requirements in EARS form and acceptance criteria as Given/When/Then, with each criterion mapped to the requirement IDs it verifies.
- Separates confirmed facts from decisions, assumptions, and open questions, and presents no unverified API, version, or behavior claim as a fact.
- Calibrates specificity: behavior and constraints are specified, but implementation choices are left to the downstream agent unless a constraint forces them.
- Includes constraints and non-goals that limit downstream agent behavior.
- Contains concrete acceptance criteria and verification steps, with traceability from requirements to verification.
- Notes security, privacy, accessibility, compatibility, migration, rollout, or operational concerns when relevant.
- Is scoped enough that a downstream agent can plan or implement without guessing.
- Does not contain unrelated implementation edits, tickets, or broad documentation rewrites.
- Was written only to the approved output location.

## Write Boundaries

- Perform read-only inspection of code, docs, UX, databases, and external references unless the user explicitly asks for edits.
- Only create, update, or delete the generated spec artifacts.
- Do not create tickets, branches, commits, PRs, implementation code, migrations, tests, or broad docs while using this skill unless the user separately asks for that work.
- Do not revert or overwrite user changes discovered during context review.
- If a requested spec requires multiple files, ask first unless the user already authorized multiple outputs or the run is non-interactive.
