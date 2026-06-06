# Specification: Improve `defining-specifications` Skill

Status: Draft for review  
Date: 2026-06-05  
Source skill: `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`  
Primary consumers: AI coding agents  
Secondary consumers: human reviewers, maintainers, and users collaborating with agents

## 1. Summary

Improve the `defining-specifications` skill so AI coding agents can reliably produce high-quality, spec-driven development artifacts from rough requests, existing code context, and bounded clarification. The revised skill should preserve the current seed's collaborative intent, but make the workflow concrete enough for agents to execute consistently: inspect context, identify uncertainty, ask or record clarifying questions, draft a reviewable specification, and save it to the correct location without making unrelated changes.

The improved skill should optimize for agents that need operational guidance under varied constraints. It should tell the agent what to read, what questions to ask, how to proceed when answers are unavailable, how to structure the final specification, and what quality bar the output must meet.

## 2. Current State

The seed skill currently defines a broad "Specification Creator" mode with these strengths:

- It frames specification work as collaborative refinement rather than one-shot writing.
- It instructs the agent to read user-provided inputs and relevant workspace context.
- It establishes a default behavior of saving specification files under `./docs/specs/`.
- It allows critical pushback and encourages holistic specifications.

However, the current seed is too underspecified for repeatable agent behavior:

- The YAML frontmatter appears malformed because the `description` string is opened but not closed before `metadata`.
- The skill does not define a concrete spec template, quality rubric, or acceptance criteria.
- It assumes live back-and-forth with the user, but does not say how to proceed in evaluation, batch, or no-response contexts.
- It does not distinguish between discovery questions, assumptions, requirements, non-goals, risks, and implementation details.
- It says to use a todo list and question asking tool if present, but does not define when or how.
- It grants broad context review guidance, but does not set guardrails for read-only exploration, browser usage, or write boundaries beyond the generated spec file.
- It leaves naming, multi-file output, and artifact reviewability somewhat ambiguous.

## 3. Goals

1. Make the skill directly executable by AI coding agents without relying on hidden judgment.
2. Produce specifications that are useful for implementation, review, testing, and future agent handoff.
3. Preserve human reviewability through clear headings, decisions, assumptions, and traceable requirements.
4. Support both interactive and non-interactive workflows.
5. Keep the skill compact enough to be loaded as operational guidance, while moving reusable detail into a clear output template.
6. Prevent accidental edits outside generated specification artifacts.

## 4. Non-Goals

- Do not turn the skill into a full project management system.
- Do not require agents to create tickets, epics, branches, PRs, or implementation code.
- Do not mandate a single product-development methodology such as PRD, RFC, or design doc for all cases.
- Do not require browser or database exploration unless relevant to the requested specification.
- Do not optimize primarily for polished marketing prose; the artifact should be practical for engineering execution.

## 5. Target Users and Use Cases

### 5.1 AI Coding Agent Creating a Spec From a Rough Request

The agent receives a feature idea, bug fix proposal, refactor request, product change, or architecture direction. It should inspect relevant inputs, ask the highest-value clarifying questions if allowed, record assumptions when answers are unavailable, and produce a saved specification.

### 5.2 AI Coding Agent Reviewing an Existing Spec

The agent receives an existing spec and should identify missing requirements, unclear scope, risky assumptions, test gaps, and implementation ambiguity before producing a revised or companion specification.

### 5.3 Human Reviewer Consuming the Spec

A human should be able to scan the artifact and understand the problem, proposed behavior, scope boundaries, open questions, risks, acceptance criteria, and implementation-readiness without reading the entire chat.

### 5.4 Future Agent Implementing the Spec

A later coding agent should be able to use the specification as a work contract. The spec should contain enough detail to guide implementation choices, tests, and verification without needing to reconstruct context from chat history.

## 6. Required Skill Behavior

### 6.1 Activation

The skill should activate when the user asks to:

- Draft, define, improve, review, or formalize a specification.
- Turn an idea, feature request, rough notes, issue, ticket, design discussion, or product change into a spec.
- Create implementation-ready requirements for a coding agent.
- Evaluate or improve a specification-writing process.

### 6.2 Initial Context Intake

The agent must read all directly provided inputs before drafting. Depending on the task, this may include:

- User prompt or pasted notes.
- Referenced files or folders.
- Existing specs, tickets, READMEs, rules, or design docs.
- Relevant code paths when the spec depends on current implementation behavior.
- UI or browser state only when the request involves user-facing workflows where visual behavior matters.

The skill should instruct agents to keep context gathering proportional. A narrow change may only require a few files; a cross-system spec may require broader exploration.

### 6.3 Clarification Protocol

The skill should make clarification explicit:

1. Identify decision-critical unknowns.
2. Ask a small number of high-value questions when interaction is allowed.
3. Avoid asking questions that can be answered by reading provided context.
4. If the user or evaluation constraints prohibit asking, create a "Questions and Assumptions" section and proceed with stated assumptions.
5. Label assumptions by confidence and impact where useful.

Recommended question limit:

- Simple spec: up to 3 questions.
- Medium spec: up to 5 questions.
- Large or ambiguous spec: up to 7 questions, grouped by theme.

The skill should tell agents not to block forever on clarification. If answers are unavailable, the agent should produce the best useful draft with visible assumptions and open questions.

### 6.4 Specification Artifact Requirements

The final specification should include these sections unless clearly irrelevant:

1. Title and metadata
2. Summary
3. Background or current state
4. Problem statement
5. Goals
6. Non-goals
7. Users or consumers
8. Requirements
9. Proposed behavior or workflow
10. Data model, API, UI, or integration details as applicable
11. Edge cases and failure modes
12. Security, privacy, permission, or safety considerations as applicable
13. Testing and verification plan
14. Rollout, migration, or compatibility notes as applicable
15. Open questions
16. Assumptions
17. Acceptance criteria

For small specs, the agent may collapse adjacent sections, but it must preserve the substance: scope, requirements, assumptions, risks, verification, and acceptance criteria.

### 6.5 Requirements Style

Requirements should be concrete, testable, and grouped logically. The skill should prefer normative language:

- "The system must..." for required behavior.
- "The system should..." for preferred behavior.
- "The system may..." for optional behavior.
- "Out of scope..." for explicit exclusions.

Requirements should avoid vague phrases such as "make it better," "improve UX," or "handle errors" unless expanded into observable behavior.

### 6.6 Acceptance Criteria

Every spec should end with acceptance criteria that an implementer or reviewer can check. Criteria should cover:

- Artifact completeness.
- Functional behavior.
- Important non-functional requirements.
- Tests or verification steps.
- No unintended writes or scope creep when the spec is produced by an agent.

Acceptance criteria should be phrased as pass/fail statements.

### 6.7 Output Location and File Naming

Default behavior should remain:

- Save specifications under `./docs/specs/`.
- Use a filename like `SPEC-{{short-kebab-description}}-{{YYYY-MM-DD}}.md`.

If the user specifies an output directory or filename, that instruction overrides the default. The agent must create only the required output directory if it does not exist, and must not edit unrelated files.

If multiple files would be useful, the agent should ask first when interaction is allowed. If interaction is disallowed and multiple files are justified, it may create:

- One final specification file.
- One short notes/questions file containing unresolved questions, assumptions, and evaluation notes.

### 6.8 Write Boundaries

The skill should explicitly state:

- Source files, implementation code, tickets, and existing docs are read-only unless the user specifically asks to edit them.
- The agent may create or update only the generated spec artifacts.
- The agent must not "fix" implementation issues discovered during specification work.
- If existing source changes are noticed, the agent should work around them and not revert them.

### 6.9 Human Reviewability

The generated spec should be easy to review in plain Markdown:

- Use short headings and concise prose.
- Prefer bullets for requirements and acceptance criteria.
- Include enough context to stand alone outside the chat.
- Put unresolved questions and assumptions in dedicated sections.
- Avoid giant tables unless they materially improve comprehension.
- Cite relevant files with paths when source context influenced the spec.

## 7. Proposed Improved Skill Structure

The revised `SKILL.md` should use this structure:

1. Valid YAML frontmatter
   - `name`
   - concise `description`
   - `metadata` with author and version
2. Mode and mission
3. When to use
4. Operating principles
5. Workflow
   - Intake
   - Context review
   - Clarification
   - Drafting
   - Review pass
   - Save output
6. Output template
7. Quality checklist
8. Constraints and write boundaries

The skill should be written as direct operational guidance to the agent, not as abstract advice.

## 8. Proposed Workflow Text

The improved skill should instruct agents to follow this workflow:

1. Read the user's request and all referenced inputs in full.
2. Identify the system, artifact, or behavior being specified.
3. Inspect relevant workspace context read-only when needed.
4. Create a short working plan or todo list for non-trivial specs.
5. Ask decision-critical clarifying questions if interaction is allowed.
6. If answers are unavailable, record questions and proceed with explicit assumptions.
7. Draft a specification using the required sections.
8. Run a self-review for ambiguity, missing acceptance criteria, and scope creep.
9. Save the final spec to the requested path or default specs directory.
10. Summarize the saved output and any unresolved questions.

## 9. Quality Checklist

The improved skill should require the agent to check the final artifact before saving:

- The spec can stand alone without chat history.
- Requirements are grouped and testable.
- Non-goals prevent likely scope creep.
- Open questions are separated from assumptions.
- The testing plan maps to the acceptance criteria.
- Risks and edge cases are captured for implementation planning.
- File paths and source context are cited where relevant.
- The output path follows user instructions.
- No source files or implementation code were edited.

## 10. Example Output Template

The skill should include or reference a compact template like this:

```markdown
# Specification: {{Title}}

Status: Draft
Date: {{YYYY-MM-DD}}
Owner/Requester: {{if known}}
Source context: {{links or paths}}

## Summary
{{One to three paragraphs describing the requested change and intended outcome.}}

## Current State
{{What exists today and what context was reviewed.}}

## Problem
{{The user, product, technical, or process problem this spec addresses.}}

## Goals
- {{Goal 1}}
- {{Goal 2}}

## Non-Goals
- {{Explicit exclusion 1}}
- {{Explicit exclusion 2}}

## Requirements
### {{Group A}}
- The system must {{testable behavior}}.
- The system should {{preferred behavior}}.

### {{Group B}}
- The system must {{testable behavior}}.

## Proposed Approach
{{Workflow, architecture, UX, data, or integration details appropriate to the request.}}

## Edge Cases and Risks
- {{Edge case or risk}}

## Testing and Verification
- {{Verification step}}

## Open Questions
- {{Question}}

## Assumptions
- {{Assumption}}

## Acceptance Criteria
- [ ] {{Pass/fail criterion}}
- [ ] {{Pass/fail criterion}}
```

## 11. Acceptance Criteria for the Skill Improvement

- The revised skill has valid YAML frontmatter.
- The revised skill tells agents when to activate it.
- The revised skill defines a step-by-step workflow that supports both interactive and non-interactive contexts.
- The revised skill instructs agents to record unanswered clarification questions and assumptions when they cannot ask the user.
- The revised skill includes a reusable specification template or clearly enumerated required sections.
- The revised skill includes a quality checklist for self-review before saving.
- The revised skill preserves write boundaries and read-only context exploration.
- The revised skill makes output path and filename behavior deterministic, with user-specified paths overriding defaults.
- The revised skill optimizes for AI coding agents while remaining readable by human reviewers.

## 12. Open Questions

- Should the improved skill support multiple named spec formats, such as product spec, technical spec, RFC, and implementation plan, or should it keep one flexible default template?
- Should the skill require a separate notes/questions file in non-interactive evaluation settings, or only allow one when useful?
- Should the default spec include checkboxes in acceptance criteria, or plain pass/fail bullets?
- Should "Specification Creator" remain the mode name, or should it be renamed to "Spec-Driven Development Planner" to better fit AI coding agent consumption?
- Should the skill include an example completed mini-spec, or is the blank template enough?

## 13. Assumptions

- The immediate improvement target is the skill text itself, not a generated implementation spec for a separate product feature.
- AI coding agents are the primary execution environment, so instructions should be imperative and operational.
- Human reviewability matters, but the artifact should favor clarity and testability over polished narrative.
- The existing default of saving specs under `./docs/specs/` should be preserved unless the user provides an output path.
- The current seed's collaborative posture is valuable and should be retained with clearer non-interactive fallback behavior.

