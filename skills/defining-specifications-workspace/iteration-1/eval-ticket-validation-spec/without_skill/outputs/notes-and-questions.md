# Notes And Questions

## Inspection Notes

- No `.tickets/**/*.md` files were found in the workspace during the read-only scan.
- The specification relies on ticket convention documents under `skills/ticket-workflow/references/`, especially the ticket templates, complexity rubric, outcome schema, and orchestrator review protocol.
- The requested defining-specifications skill file was not read or used.
- No tickets, implementation code, source files, or workspace documentation were modified.

## Clarifying Questions

- What exact status values are canonical for ticket frontmatter?
- Should active validation include `.tickets/_archive/` by default?
- Are ticket IDs globally unique across active and archived tickets?
- Should `task` tickets require `priority` and `tags`, or should they keep the leaner current template?
- Should template placeholder IDs such as `FEAT-XXX` be valid only in draft mode?
- Should dependency references be allowed to point to archived tickets?
- Should lifecycle validation inspect git history, or only the current markdown state?

## Assumptions Used

- Status allowlist: `to-do`, `in-progress`, `blocked`, `done`.
- Review outcome labels like `MERGED` and `BLOCKED_DEPENDENCY` are not frontmatter statuses.
- The first validator release should be deterministic and file-based.
- Missing canonical decisions should become warnings or configuration options rather than aggressive hard failures.
