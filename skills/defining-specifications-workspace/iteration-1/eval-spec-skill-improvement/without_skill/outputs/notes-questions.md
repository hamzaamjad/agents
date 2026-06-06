# Notes and Clarifying Questions

Date: 2026-06-05  
Related spec: `SPEC-defining-specifications-skill-improvement-2026-06-05.md`

## Assumptions Used

- The improved skill should optimize first for AI coding agents that need to create implementation-ready artifacts.
- Human reviewability remains important, so the final artifact should use ordinary markdown and clear prose rather than agent-only metadata.
- The skill should support both interactive conversations and evaluation or automation contexts where the agent must proceed without live answers.
- The improved skill should not edit source code, tickets, or existing documentation while creating a specification unless the user separately asks for that.
- A good spec should make requirements, assumptions, open questions, risks, tests, and acceptance criteria easy for future agents to reference.

## Clarifying Questions Recorded

- Should the improved skill include a fully worked example specification, or only a reusable template?
- Should source references be required for every generated spec, or only when repository or external context was actually inspected?
- Should implementation slices be mandatory in every spec, or optional for high-level product specifications?
- Should the skill explicitly hand off to a ticket workflow when one exists?
- Should there be a fixed maximum number of initial clarifying questions, or just guidance to ask a bounded set of high-leverage questions?
- Should the default output location remain `docs/specs/`, or should the skill prefer a workspace-specific convention if one is discovered?

## Notable Seed Issues

- The current frontmatter appears to have an unclosed `description` string.
- The current workflow is directionally useful but underspecified for repeatable agent behavior.
- The current output guidance does not define a required spec structure, quality gate, or traceability model.
- The current constraints broadly allow context review but do not clearly prioritize sources or define when browser, database, or external documentation tools are appropriate.

