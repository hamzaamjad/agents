# Specification: Ticket Markdown Validation Capability

Status: Draft  
Date: 2026-06-05  
Audience: future implementation agent for the `.agents` workspace

## Summary

Add a read-only ticket validation capability for `.tickets/` markdown files. The validator should parse ticket frontmatter, verify the current ticket graph, and report precise diagnostics for malformed tickets before agents use them for planning, execution, dependency checks, or archive retrieval.

The capability should not create, modify, archive, or execute tickets. It is a validation gate only.

## Problem

The workspace ticket model relies on structured markdown files whose frontmatter drives agent behavior. A malformed field, typoed status, broken dependency, or inconsistent parent/child lifecycle can cause an agent to execute work out of order, miss a blocker, mark incomplete work done, or lose useful archive context.

There is currently no explicit validator described for these invariants. The new capability should make ticket state errors visible early with actionable messages.

## Goals

- Validate all active `.tickets/**/*.md` ticket files against the expected frontmatter schema for their ticket type.
- Enforce allowed values for `type`, `status`, `priority`, boolean fields, dates, tags, and complexity.
- Build a ticket ID index and validate `parent` and `dependencies` references.
- Detect dependency cycles and lifecycle inconsistencies that can be inferred from current files.
- Require completed tickets to carry the expected completion context.
- Produce human-readable output by default and machine-readable JSON for automation.
- Exit non-zero when errors are found so the validator can be used in CI, hooks, or agent preflight checks.

## Non-Goals

- Do not create, decompose, edit, execute, archive, or close tickets.
- Do not infer missing metadata by rewriting files.
- Do not validate production implementation code referenced by tickets.
- Do not require git history to validate lifecycle transitions. This first version validates the current ticket state only.
- Do not depend on a populated `.tickets/` directory. An absent or empty ticket root should be handled gracefully.

## Workspace Context Observed

No `.tickets/` tree was present during inspection. Existing local ticket templates define these ticket types:

- `epic`
- `feature`
- `bug`
- `chore`
- `refactor`
- `task`

Template status values and lifecycle text indicate these valid statuses:

- `to-do`
- `in-progress`
- `blocked`
- `done`

Template priority values indicate these valid priorities:

- `critical`
- `high`
- `medium`
- `low`

Completed tickets are expected to include a `## Outcome` section. Archived ticket outcome blocks are intended to be dense retrieval surfaces for future agents.

## Proposed User Interface

Provide a command that can be run from the workspace root:

```bash
validate-tickets [--root .tickets] [--include-archive] [--format text|json] [--strict]
```

Default behavior:

- Validate `.tickets/**/*.md`.
- Exclude `.tickets/_archive/**` unless `--include-archive` is set.
- Print grouped diagnostics in text format.
- Exit `0` when no errors are found.
- Exit `1` when validation errors are found.
- Exit `2` for validator usage/configuration failures, such as an unreadable root path.

If `.tickets/` does not exist, print a short warning and exit `0` unless `--strict` is set.

## Ticket Discovery

The validator should:

1. Resolve the ticket root relative to the workspace root unless an absolute `--root` is provided.
2. Find markdown files beneath the ticket root.
3. Ignore non-markdown files.
4. Exclude archive paths by default.
5. Include archived tickets only when explicitly requested.

Files under archive paths should be treated as historical records. Validation may report diagnostics for them when requested, but messages should not imply they should be casually edited in place.

## Parsing Requirements

Each ticket file must:

- Start with YAML frontmatter delimited by `---`.
- Parse as a mapping/object, not a scalar or list.
- Have exactly one ticket `id`.
- Have a body after the closing frontmatter delimiter.

Use a YAML/frontmatter parser rather than ad hoc string splitting so lists, booleans, dates, and quoted strings are interpreted consistently.

## Frontmatter Schema

### Common Rules

All ticket types require:

- `id`: non-empty string.
- `title`: non-empty string.
- `type`: one of `epic`, `feature`, `bug`, `chore`, `refactor`, `task`.
- `status`: one of `to-do`, `in-progress`, `blocked`, `done`.
- `agent_created`: boolean when present.

Common optional fields:

- `tags`: list of strings.
- `complexity`: integer from `1` through `10`, unless required by ticket type.

Unknown fields should be warnings by default and errors under `--strict`.

### Type-Specific Required Fields

`epic` tickets require:

- `id`, matching `EPIC-...`
- `title`
- `type: epic`
- `status`
- `priority`
- `branch`
- `created`
- `updated`
- `tags`
- `agent_created`

`feature` tickets require:

- `id`, matching `FEAT-...`
- `title`
- `type: feature`
- `status`
- `priority`
- `created`
- `updated`
- `parent`
- `dependencies`
- `tags`
- `agent_created`

`bug` tickets require:

- `id`, matching `BUG-...`
- `title`
- `type: bug`
- `status`
- `priority`
- `created`
- `updated`
- `parent`
- `dependencies`
- `tags`
- `agent_created`

`chore` tickets require:

- `id`, matching `CHORE-...`
- `title`
- `type: chore`
- `status`
- `priority`
- `created`
- `updated`
- `parent`
- `dependencies`
- `tags`
- `agent_created`

`refactor` tickets require:

- `id`, matching `REFAC-...`
- `title`
- `type: refactor`
- `status`
- `priority`
- `created`
- `updated`
- `parent`
- `dependencies`
- `tags`
- `agent_created`

`task` tickets require:

- `id`, matching `TASK-...`
- `title`
- `type: task`
- `status`
- `parent`
- `dependencies`
- `agent_created`
- `complexity`

### Field Value Rules

- `priority` must be one of `critical`, `high`, `medium`, or `low`.
- `created` and `updated` must be ISO dates in `YYYY-MM-DD` format.
- `updated` must not be earlier than `created`.
- `dependencies` must be a list of strings, even when empty.
- `parent` may be empty only for non-task tickets. For `task`, it must be non-empty.
- `complexity`, when present, must be an integer from `1` through `10`.
- `branch` on epics must be non-empty. If a branch naming convention is later formalized, this validator should enforce it.

## Reference Validation

The validator should build an index of ticket IDs before validating references.

Required checks:

- No duplicate `id` values across the scanned ticket set.
- Every `parent` value, when non-empty, resolves to an existing ticket ID.
- Every `task` parent resolves to an `epic`.
- Every dependency resolves to an existing ticket.
- A ticket cannot depend on itself.
- A ticket cannot list the same dependency more than once.
- The dependency graph cannot contain cycles.

Dependency references should support:

- Direct ticket IDs, such as `FEAT-001` or `TASK-003`.
- Same-epic sibling references where the reference is unambiguous.
- Cross-epic references in an explicit form such as `EPIC-xxxx/TASK-003`, if the workspace adopts that form.

If a reference syntax is ambiguous, the validator should fail with a diagnostic that names the candidate tickets and asks for an explicit reference.

## Lifecycle Consistency

The first version should validate lifecycle invariants that are knowable from current files:

- A ticket with `status: done` must include a `## Outcome` section.
- A ticket with `status: done` must not depend on tickets that are not `done`.
- A ticket with `status: in-progress` must not depend on tickets that are not `done`.
- A ticket with `status: blocked` should have at least one unresolved dependency or a visible blocker note in the body.
- An `epic` with `status: done` must have all discovered child tickets marked `done`.
- A parent epic should not be `done` while any child ticket is `to-do`, `in-progress`, or `blocked`.
- If an epic has a `## Sub-tickets` table, every listed ticket ID must resolve and the listed status must match that ticket's frontmatter status.
- If a ticket body has checked-off acceptance criteria but `status` is not `done`, report an informational warning only. Body checklist state can be partial and should not block validation.

Because `in-progress` is optional in the ticket lifecycle, the validator should not require a ticket to pass through `in-progress` before `done`.

## Diagnostics

Each diagnostic should include:

- Severity: `error`, `warning`, or `info`.
- Stable code, such as `TV001`.
- File path.
- Ticket ID when available.
- Field or body section when applicable.
- Clear message.
- Suggested fix.

Example text output:

```text
error TV012 .tickets/EPIC-a1b2/FEAT-001.md status
  Invalid status "complete"; expected one of: to-do, in-progress, blocked, done.
```

Example JSON shape:

```json
{
  "ok": false,
  "summary": { "files": 12, "errors": 2, "warnings": 1, "info": 0 },
  "diagnostics": [
    {
      "severity": "error",
      "code": "TV012",
      "path": ".tickets/EPIC-a1b2/FEAT-001.md",
      "ticket_id": "FEAT-001",
      "field": "status",
      "message": "Invalid status \"complete\".",
      "suggestion": "Use one of: to-do, in-progress, blocked, done."
    }
  ]
}
```

## Suggested Diagnostic Codes

- `TV001`: missing or invalid frontmatter.
- `TV002`: missing required field.
- `TV003`: invalid field type.
- `TV004`: invalid field value.
- `TV005`: ticket ID prefix does not match type.
- `TV006`: duplicate ticket ID.
- `TV007`: unresolved parent reference.
- `TV008`: invalid parent type.
- `TV009`: unresolved dependency reference.
- `TV010`: self-dependency.
- `TV011`: duplicate dependency.
- `TV012`: dependency cycle.
- `TV013`: lifecycle dependency violation.
- `TV014`: missing `## Outcome` for `done` ticket.
- `TV015`: epic child status mismatch.
- `TV016`: sub-ticket table mismatch.
- `TV017`: unknown field.

## Implementation Notes

- Keep validation read-only. Do not offer an auto-fix mode in the first version.
- Separate parsing, schema validation, reference indexing, graph validation, and lifecycle validation into independently testable units.
- Normalize paths in diagnostics relative to the workspace root.
- Preserve deterministic output by sorting files and diagnostics by path, ticket ID, and code.
- Treat archived tickets as opt-in validation scope.

## Test Plan

Add fixtures for:

- Missing frontmatter.
- Invalid YAML frontmatter.
- Missing required fields for each ticket type.
- Invalid status and priority values.
- Wrong ID prefix for type.
- Duplicate IDs.
- Missing parent.
- Task parent that is not an epic.
- Missing dependency.
- Self-dependency.
- Dependency cycle.
- `done` ticket without `## Outcome`.
- `done` ticket depending on unfinished ticket.
- `done` epic with unfinished child.
- Sub-ticket table status mismatch.
- Empty or absent `.tickets/` root.

Validation commands should be covered by tests for both text and JSON output, including exit codes.

## Open Questions

- Should `parent` be required for all non-epic ticket types, or only for `task`?
- Should non-task tickets be allowed to live outside an epic, and if so what directory convention identifies standalone tickets?
- Should `agent_created` be required on every ticket type, or only validated when present?
- Should archived tickets be required to have `status: done`, or can historical archive content include cancelled or superseded work?
- Should `blocked` require a structured blocker field, or is a body note sufficient?
- Should dependency references allow short same-epic IDs, or should all dependencies use globally unique ticket IDs only?
- Should unknown frontmatter fields be warnings forever, or should strict mode become the default once templates stabilize?
