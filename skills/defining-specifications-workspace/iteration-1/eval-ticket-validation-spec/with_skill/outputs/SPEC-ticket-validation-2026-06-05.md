# Specification: Ticket Validation Capability

Date: 2026-06-05
Status: Draft
Workspace: `.agents`

## Context

The `.agents` workspace defines a structured ticket workflow in `skills/ticket-workflow/SKILL.md` and related references. Ticket artifacts live under `.tickets/`, which is currently ignored by git and was not present in the inspected workspace. This specification therefore uses the ticket workflow skill and templates as the canonical source of truth rather than observed ticket examples.

Relevant source rules:

- Ticket directories use `.tickets/_standalone/`, `.tickets/EPIC-<hex>_<slug>/`, and `.tickets/_archive/EPIC-<hex>_<slug>/`.
- Active epic directories contain `_epic.md` plus sub-ticket files named `TYPE-NNN_kebab-slug.md`.
- Valid ticket prefixes are `EPIC`, `FEAT`, `BUG`, `REFAC`, `CHORE`, and `TASK`.
- Valid lifecycle statuses are `to-do`, `in-progress`, `blocked`, and `done`.
- Bare dependency IDs resolve only in the current ticket scope; cross-epic dependencies use `EPIC-<hex>/TYPE-NNN`.
- Tickets marked `done` must carry an `## Outcome` section.

## Problem

Agents can create, decompose, execute, and archive ticket markdown files, but there is no explicit validation gate to catch malformed frontmatter, broken dependency references, invalid statuses, or lifecycle inconsistencies before another agent relies on those tickets. A lightweight validator should make ticket state machine errors visible early, with precise messages that tell agents what to fix.

## Goals

- Validate ticket markdown files under `.tickets/` without modifying them.
- Check required frontmatter fields by ticket type.
- Reject unknown ticket types, mismatched ID prefixes, and unsupported status values.
- Resolve dependency and parent references using the same scope rules documented in the ticket workflow.
- Detect lifecycle inconsistencies that can be inferred from the current ticket graph.
- Produce deterministic, agent-readable diagnostics suitable for local use and CI.
- Treat absence of `.tickets/` as a successful no-op with an informational message.

## Non-Goals

- Do not create, edit, archive, or decompose tickets.
- Do not infer historical status transitions from git history.
- Do not validate implementation code referenced by tickets.
- Do not enforce natural-language quality beyond structural sections explicitly required by this specification.
- Do not require network access or external services.

## Proposed User Experience

Expose a single validation command for agents and CI, for example:

```bash
python scripts/validate_tickets.py
```

Recommended options:

- `--root PATH`: workspace root, defaulting to the current working directory.
- `--include-archive`: include `.tickets/_archive/` in validation.
- `--format text|json`: default `text`; `json` for CI or agent tooling.
- `--strict`: promote warnings to errors.

The command exits with:

- `0` when no errors are found.
- `1` when validation errors are found.
- `2` for validator misuse, such as an invalid CLI option or unreadable root path.

## File Discovery

Default validation scope:

- Include active tickets under `.tickets/_standalone/**/*.md`.
- Include active epic tickets under `.tickets/EPIC-*_*/**/*.md`.
- Exclude `.tickets/_archive/**` unless `--include-archive` is set.

Archive validation scope:

- When `--include-archive` is set, validate `.tickets/_archive/EPIC-*_*/**/*.md` as read-only historical records.
- Archive diagnostics should not suggest moving or editing archived tickets unless the caller explicitly chose archive validation.

Discovery rules:

- Ignore non-markdown files.
- Error on markdown files under `.tickets/` that are outside a recognized ticket directory.
- Error on active epic directories missing `_epic.md`.
- Error on active epic directories whose name does not match `EPIC-<4-hex>_<slug>`.

## Frontmatter Rules

All ticket files must begin with YAML frontmatter delimited by `---` lines. The frontmatter parser must preserve scalar strings, booleans, integers, nulls, and arrays.

Common required fields for every ticket:

- `id`
- `title`
- `type`
- `status`

Allowed `type` values and required ID prefixes:

- `epic` -> `EPIC-<4-hex>`
- `feature` -> `FEAT-NNN`
- `bug` -> `BUG-NNN`
- `refactor` -> `REFAC-NNN`
- `chore` -> `CHORE-NNN`
- `task` -> `TASK-NNN`

Required fields by type:

- `epic`: `id`, `title`, `type`, `status`, `priority`, `branch`, `created`, `updated`, `tags`, `agent_created`
- `task`: `id`, `title`, `type`, `status`, `parent`, `dependencies`, `agent_created`, `complexity`
- `feature`, `bug`, `chore`, `refactor`: `id`, `title`, `type`, `status`, `priority`, `created`, `updated`, `parent`, `dependencies`, `tags`, `agent_created`

Optional fields:

- `complexity` is optional for non-`task` tickets.
- `parent` may be empty for standalone or top-level non-task tickets, but the field must exist for non-epic, non-task tickets.

Value rules:

- `status` must be one of `to-do`, `in-progress`, `blocked`, or `done`.
- `priority`, when present, must be one of `critical`, `high`, `medium`, or `low`.
- `dependencies` must be an array. Empty dependency lists must be represented as `[]`, not an empty string.
- `tags` must be an array when present.
- `agent_created` must be boolean.
- `complexity`, when present and non-empty, must be an integer from 1 through 10.
- `created` and `updated` must use `YYYY-MM-DD`; `updated` must not be earlier than `created`.

## Path and Identity Rules

Epic identity:

- In `.tickets/EPIC-<hex>_<slug>/_epic.md`, the frontmatter `id` must equal `EPIC-<hex>`.
- The epic `branch` should equal `epic/<hex>/<slug>`. Mismatch is an error for active epics and a warning for archives.

Sub-ticket identity:

- In an epic directory, a sub-ticket filename must match `TYPE-NNN_kebab-slug.md`.
- The file prefix before `_` must equal the frontmatter `id`.
- The frontmatter `type` must match the ID prefix.

Standalone identity:

- In `.tickets/_standalone/`, filenames must match `TYPE-NNN_kebab-slug.md`.
- Standalone ticket IDs are scoped to `_standalone/`.
- `TASK` tickets are not allowed in `_standalone/` because tasks are decomposition artifacts tied to a parent.

Uniqueness:

- Epic IDs must be globally unique across active and included archived epics.
- Sub-ticket IDs must be unique within their directory scope.
- Standalone IDs must be unique within `.tickets/_standalone/`.

## Reference Resolution

The validator must build an in-memory index before checking references.

Dependency reference formats:

- Bare local ticket ID: `TYPE-NNN`
- Cross-epic ticket ID: `EPIC-<hex>/TYPE-NNN`
- Epic ID: `EPIC-<hex>`

Resolution rules:

- From a ticket inside an epic directory, bare `TYPE-NNN` dependencies resolve only within that same epic directory.
- From a standalone ticket, bare `TYPE-NNN` dependencies resolve only within `.tickets/_standalone/`.
- Cross-epic dependencies must specify `EPIC-<hex>/TYPE-NNN`; the validator must not search all epics for an unresolved bare ID.
- Dependencies on an epic may use `EPIC-<hex>` and resolve to that epic's `_epic.md`.
- References to archived tickets are allowed only when validating with `--include-archive`, unless a future policy explicitly permits active tickets to depend on archive records.

Parent reference rules:

- `TASK` tickets must have a non-empty `parent`.
- A non-empty `parent` must resolve using the same local or cross-epic reference rules as dependencies.
- A ticket must not list itself as its own parent.
- Parent references must not form cycles.

Dependency graph rules:

- A ticket must not depend on itself.
- Dependency cycles are errors.
- Duplicate entries in `dependencies` are warnings unless `--strict` is set.
- Unknown dependency references are errors.

## Lifecycle Consistency Rules

Dependency-gated statuses:

- `in-progress` or `done` tickets must not have dependencies whose resolved status is anything other than `done`.
- `blocked` tickets should have at least one unresolved or non-`done` dependency, or a visible blocking explanation in the ticket body. If neither exists, emit a warning.
- `to-do` tickets may depend on tickets in any status.

Done tickets:

- A ticket with `status: done` must contain an `## Outcome` section.
- A done ticket's `## Outcome` should include the seven canonical subsections from `references/outcome-schema.md`; missing subsections are warnings by default and errors in `--strict`.
- A done ticket must contain a `## Verification` section. Missing verification is an error.

Epic consistency:

- An active epic whose `_epic.md` is `done` should have all sub-tickets `done`; otherwise error.
- An archived epic must have `_epic.md` status `done` and every sub-ticket status `done`.
- Active epic directories should not be fully `done` unless they are awaiting archive/closure; emit a warning so an orchestrator can decide whether closure work is missing.
- Each active epic should include at least one closure `CHORE` ticket as the final merge-order item when the epic has sub-tickets. Missing closure ticket is a warning because older epics may predate this rule.

Body section consistency:

- Every non-epic ticket must include `## Acceptance criteria` and `## Verification`.
- Every ticket should include `## Constraints`, except epic tickets where constraints may live in `## Context` or `## Notes`.
- Tickets over 200 lines should emit a warning, matching the ticket workflow quality rule.
- Tickets with more than five acceptance criteria should emit a warning; `TASK` tickets with more than three acceptance criteria should emit an error.

## Diagnostic Format

Text output should be stable and grep-friendly:

```text
ERROR .tickets/EPIC-a7f3_demo/FEAT-001_example.md frontmatter.status invalid value "todo"; expected one of: to-do, in-progress, blocked, done
WARN  .tickets/EPIC-a7f3_demo/_epic.md lifecycle.closure missing closure CHORE in merge order
```

JSON output should contain:

- `severity`: `error`, `warning`, or `info`
- `path`
- `code`: stable machine-readable diagnostic code
- `message`
- `field`, when applicable
- `reference`, when applicable

Example diagnostic codes:

- `frontmatter.missing`
- `frontmatter.invalid_status`
- `identity.path_id_mismatch`
- `dependency.unresolved`
- `dependency.cycle`
- `lifecycle.dependency_not_done`
- `lifecycle.done_missing_outcome`
- `lifecycle.archive_not_done`
- `body.missing_verification`

## Acceptance Criteria

- Running the validator in a workspace with no `.tickets/` directory exits `0` and prints an informational no-op message.
- A ticket missing required frontmatter produces a file-specific error naming each missing field.
- A ticket with `status: todo` produces an error that lists the allowed status values.
- A bare dependency inside an epic resolves only within that same epic and errors if absent there.
- A cross-epic dependency in the form `EPIC-<hex>/TYPE-NNN` resolves to the matching epic directory and ticket.
- Dependency cycles are detected and reported with the cycle path.
- A `done` ticket without `## Outcome` produces an error.
- An archived epic containing a non-`done` ticket produces an error when `--include-archive` is enabled.
- Text and JSON output are deterministic across repeated runs on the same input.

## Verification Plan

Create fixture directories for validator tests rather than relying on real workspace tickets:

- Empty workspace with no `.tickets/`.
- Valid standalone ticket.
- Valid active epic with `_epic.md`, sub-tickets, local dependencies, and closure chore.
- Invalid frontmatter cases: missing fields, wrong scalar type, invalid status, invalid date.
- Invalid identity cases: filename/frontmatter mismatch, wrong ID prefix for type, bad epic directory hex.
- Invalid dependency cases: unresolved bare ID, unresolved cross-epic ID, dependency cycle, dependency not done for an in-progress ticket.
- Lifecycle cases: done without outcome, archived epic not fully done, task with too many acceptance criteria.

Recommended verification command after implementation:

```bash
python scripts/validate_tickets.py --root tests/fixtures/tickets/valid
python scripts/validate_tickets.py --root tests/fixtures/tickets/invalid
python scripts/validate_tickets.py --root tests/fixtures/tickets/archive --include-archive
```

## Open Questions and Assumptions

This specification proceeds with assumptions because the evaluation task forbids stopping for clarification.

- Assumption: `.tickets/` absence should be a valid no-op, because this workspace currently has no `.tickets/` directory.
- Assumption: standalone bare dependencies resolve within `.tickets/_standalone/`, mirroring the documented local-scope rule for epics.
- Assumption: active tickets should not depend on archived tickets by default, because archived tickets are historical and read-only.
- Assumption: missing closure tickets are warnings, not errors, to avoid breaking older or partially migrated epics.
- Question: Should `priority`, `created`, `updated`, `tags`, and `agent_created` be hard-required for all non-task tickets, or should the minimal requirement remain only `id`, `title`, `type`, and `status` as stated in the ticket creation step?
- Question: Should `parent` support only ticket IDs, only epic IDs, or both?
- Question: Should archived ticket validation be strict enough to fail CI, or should archive diagnostics remain advisory?
- Question: Should the validator live inside this workspace as a Python script, a shell command, or a reusable skill helper?
