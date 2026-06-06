# Notes And Questions: Ticket Validation Spec

Date: 2026-06-05

## Context Reviewed

- Used `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md` as the active specification skill.
- Reviewed `/Users/hamzaamjad/.agents/skills/ticket-workflow/SKILL.md` for directory layout, naming, dependency resolution, lifecycle, and execution protocol.
- Reviewed ticket workflow references:
  - `references/templates.md`
  - `references/outcome-schema.md`
  - `references/complexity-scoring.md`
  - `references/orchestrator-review-protocol.md`
- No active `.tickets/` directory or ticket markdown files were found in the workspace during this read-only inspection.

## Clarifying Questions Not Asked During Evaluation

- Q-001: Should missing template fields such as `priority`, `created`, `updated`, `tags`, and `agent_created` be hard validation errors, or warnings unless execution depends on them?
- Q-002: Should archived tickets be held to the newest Outcome schema, or should older archived tickets be grandfathered if they predate the schema?
- Q-003: Where should the validator live and how should it be invoked: ticket-workflow script, repo-level script, skill helper, or another convention?
- Q-004: Should blocked tickets require a structured blocker reason, even though the current templates only define `status: blocked` as an allowed status?
- Q-005: Should JSON output be required in the first implementation, or deferred until CI or automation integration needs it?
- Q-006: Should active epics marked `done` be a hard error, or a warning to allow the closure ticket's short transition before archive movement?

## Working Assumptions

- ASM-001: The ticket workflow skill and references are canonical for this spec.
- ASM-002: A missing `.tickets/` directory is acceptable and should not cause validation failure.
- ASM-003: Ticket frontmatter is YAML, and array fields such as `dependencies` and `tags` should be parsed as arrays.
- ASM-004: Standalone bare dependency IDs should resolve only within `.tickets/_standalone/`, by analogy to bare IDs resolving only within the current epic.
- ASM-005: The first validator should be read-only and fixture-testable, with no dependency on existing real tickets.
- ASM-006: Template completeness and lifecycle safety are related but distinct; rollout should allow warnings for template drift where strict enforcement could break older tickets.

## Output Files

- `SPEC-ticket-validation-2026-06-05.md`
- `notes-and-questions.md`
