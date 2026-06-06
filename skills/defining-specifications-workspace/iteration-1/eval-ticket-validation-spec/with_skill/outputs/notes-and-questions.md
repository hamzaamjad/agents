# Notes and Clarifying Questions

## Context Inspected

- Active skill: `skills/defining-specifications/SKILL.md`
- Ticket workflow: `skills/ticket-workflow/SKILL.md`
- Ticket templates: `skills/ticket-workflow/references/templates.md`
- Outcome schema: `skills/ticket-workflow/references/outcome-schema.md`
- Complexity rubric: `skills/ticket-workflow/references/complexity-scoring.md`
- Workspace ignore rules: `.gitignore`

No `.tickets/` directory was present in the inspected workspace, so the specification is based on canonical workflow documentation rather than concrete ticket examples.

## Assumptions Recorded

- Absence of `.tickets/` should be a successful no-op.
- Standalone bare dependencies resolve within `.tickets/_standalone/`.
- Active tickets should not depend on archived tickets unless a future policy explicitly allows it.
- Archive validation is opt-in via `--include-archive`.
- Missing closure tickets should start as warnings to avoid breaking older ticket sets.
- `TASK` tickets are not allowed as standalone tickets.

## Clarifying Questions

- Should the validator hard-require the full template frontmatter for each ticket type, or only the minimal fields called out in the workflow creation step?
- Should `parent` references allow both epic IDs and ticket IDs, or should one form be canonical?
- Should active tickets ever be allowed to depend on archived tickets?
- Should archive validation failures fail CI, or only report advisory diagnostics?
- Which implementation home is preferred: standalone Python script, shell utility, skill helper, or another command surface?
- Should body quality rules such as ticket length and acceptance-criteria count be errors, warnings, or strict-mode-only errors?
