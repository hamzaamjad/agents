# Notes and Questions

## Inspection Notes

- No `.tickets/` directory was present in the workspace during inspection.
- Ticket templates found in local workspace context define ticket types: `epic`, `feature`, `bug`, `chore`, `refactor`, and `task`.
- Template frontmatter uses statuses `to-do`, `in-progress`, `blocked`, and `done`.
- Template frontmatter uses priorities `critical`, `high`, `medium`, and `low`.
- Completed tickets are expected to include a `## Outcome` section.
- The specification assumes validation should be read-only and should not create tickets, implementation code, or auto-fixes.

## Assumptions

- `.tickets/` is the canonical ticket root even though it was not present at inspection time.
- `task` tickets must have a non-empty `parent` that resolves to an epic.
- Non-task tickets may have an empty `parent` unless the workspace later decides all active work must belong to an epic.
- `dependencies` should always be a YAML list, even when empty.
- Current-state validation is sufficient for the first version; historical transition validation can come later if git history is needed.
- Archived tickets should be excluded by default and validated only when explicitly requested.

## Clarifying Questions

1. Should `parent` be required for `feature`, `bug`, `chore`, and `refactor` tickets, or only for `task` tickets?
2. What are the canonical active ticket directory layouts, especially for standalone tickets versus epic-owned tickets?
3. Should `agent_created` be required for every ticket type?
4. Should archived tickets always be `done`, or can archived records include cancelled, superseded, or otherwise terminal non-done states?
5. Should `blocked` require structured frontmatter for the blocker, or is a body section enough?
6. Should dependency references be globally unique ticket IDs only, or should same-epic short references and cross-epic path references be supported?
7. Should unknown frontmatter fields be warnings by default, errors in strict mode, or always errors?
