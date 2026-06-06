# Ticket Validation Specification

## Summary

Add a read-only ticket validation capability for this `.agents` workspace that inspects markdown files under `.tickets/` and reports structural, reference, and lifecycle issues before agents execute or archive work.

The validator should parse each ticket as markdown with YAML frontmatter, validate the frontmatter against the workspace ticket conventions, verify dependency and parent references, and check lifecycle consistency across active and archived tickets. It should not create, modify, move, or archive tickets.

## Read-Only Context Inspected

- No `.tickets/**/*.md` files were present in the current workspace scan, so this specification is based on documented conventions rather than a live ticket corpus.
- `skills/ticket-workflow/references/templates.md` defines ticket templates for `feature`, `bug`, `chore`, `refactor`, `task`, and `epic`.
- `skills/ticket-workflow/references/complexity-scoring.md` defines `complexity` as an integer from 1 to 10.
- `skills/ticket-workflow/references/outcome-schema.md` requires tickets marked `done` to carry a structured `## Outcome` section.
- `skills/ticket-workflow/references/orchestrator-review-protocol.md` references dependency-aware merge behavior and terminal review states such as `BLOCKED_DEPENDENCY`, but those are review outcomes rather than ticket frontmatter statuses.

## Clarifications And Assumptions

### Questions To Confirm

- Q1. What is the canonical frontmatter status allowlist? The templates show `to-do`; lifecycle docs mention `done` and `blocked`. This spec assumes `to-do`, `in-progress`, `blocked`, and `done`.
- Q2. Should archived tickets remain under `.tickets/_archive/`, and should active validation include or exclude archived tickets by default?
- Q3. Are ticket IDs globally unique across active and archived tickets, or only unique within active tickets?
- Q4. Should `priority` and `tags` be required for `task` tickets, even though the current task template omits them?
- Q5. Is `complexity` optional for all non-task tickets or should the validator warn when it is missing?
- Q6. Should status transitions be validated from version-control history, or should lifecycle validation only check the current file state?
- Q7. Are bare dependency IDs allowed only in `task` tickets with a parent epic, or in all child tickets under an epic?
- Q8. Should dependency references be allowed to point to archived tickets?

### Working Assumptions

- A1. The first implementation validates current file state only and does not inspect git history.
- A2. Markdown tickets may exist under `.tickets/` and `.tickets/_archive/`; default validation scans both, with an option to scan active tickets only.
- A3. Ticket IDs are globally unique across the scanned set.
- A4. `dependencies` is always a YAML list. Empty dependencies must be represented as `[]`, not an empty string.
- A5. `created` and `updated` are ISO calendar dates in `YYYY-MM-DD` format, and `updated` must not be earlier than `created`.
- A6. Review outcome states such as `MERGED`, `NEEDS_FIX`, and `BLOCKED_DEPENDENCY` are not valid frontmatter `status` values.

## Goals

- G1. Catch malformed ticket markdown before an agent starts execution.
- G2. Make ticket graph problems visible, including missing dependencies, duplicate IDs, and cycles.
- G3. Keep lifecycle checks deterministic and file-based so they can run in CI, hooks, or manual agent workflows.
- G4. Produce concise diagnostics that identify the file, ticket ID if available, severity, rule ID, and remediation hint.

## Non-Goals

- NG1. Do not implement ticket creation, ticket migration, archiving, or status mutation.
- NG2. Do not infer missing fields from headings or body text.
- NG3. Do not validate implementation diffs, changed file allowlists, or verification command results.
- NG4. Do not require network access, external services, or persistent infrastructure.
- NG5. Do not replace human judgment for ambiguous lifecycle decisions; report warnings where the convention is not yet canonical.

## Ticket Model

### Ticket Types

The validator should recognize these frontmatter `type` values:

- `feature`
- `bug`
- `chore`
- `refactor`
- `task`
- `epic`

### Status Values

The validator should recognize these frontmatter `status` values unless the workspace later defines a different canonical list:

- `to-do`
- `in-progress`
- `blocked`
- `done`

Unknown statuses are errors. Known review outcome states such as `MERGED`, `NEEDS_FIX`, `REASSIGNED`, `ESCALATED`, `RESTARTED`, and `BLOCKED_DEPENDENCY` must be rejected as ticket statuses.

### ID Formats

- `EPIC-XXXX`, where `XXXX` is a short stable identifier. Existing examples suggest a hex-like suffix, but validation should initially accept uppercase letters, lowercase letters, and digits after `EPIC-`.
- `FEAT-XXX`, `BUG-XXX`, `CHORE-XXX`, `REFAC-XXX`, and `TASK-XXX`, where `XXX` is one or more digits or a stable placeholder-compatible identifier.
- The ID prefix must match the ticket `type`.

## Requirements

### Frontmatter Parsing

- REQ-FM-001. The validator must scan markdown files under `.tickets/` recursively, excluding non-markdown files.
- REQ-FM-002. The validator must parse YAML frontmatter delimited by leading `---` markers.
- REQ-FM-003. A markdown file without parseable frontmatter must produce an error.
- REQ-FM-004. Frontmatter parse failures must report the file path and YAML parser error.
- REQ-FM-005. Body validation must not run for a file whose frontmatter cannot be parsed.

### Required Fields

- REQ-FLD-001. Every ticket must include `id`, `title`, `type`, `status`, `dependencies`, and `agent_created`.
- REQ-FLD-002. `feature`, `bug`, `chore`, `refactor`, and `epic` tickets must include `created`, `updated`, `priority`, and `tags`.
- REQ-FLD-003. `feature`, `bug`, `chore`, and `refactor` tickets may include `parent`; if present and non-empty, it must resolve to an existing `epic`.
- REQ-FLD-004. `feature`, `bug`, `chore`, `refactor`, and `epic` tickets may include `complexity`; when present, it must be an integer from 1 to 10.
- REQ-FLD-005. `task` tickets must include a non-empty `parent` that resolves to an existing `epic`.
- REQ-FLD-006. `task` tickets must include `complexity` as an integer from 1 to 10.
- REQ-FLD-007. `epic` tickets must include a non-empty `branch`.
- REQ-FLD-008. Empty required string fields must produce errors, except `title` may be temporarily empty only if the workspace chooses to permit template drafts.
- REQ-FLD-009. Unknown frontmatter fields should produce warnings, not errors, unless a strict mode is enabled.

### Field Value Validation

- REQ-VAL-001. `type` must be one of the recognized ticket types.
- REQ-VAL-002. `status` must be one of the allowed ticket status values.
- REQ-VAL-003. `priority`, when required or present, must be one of `critical`, `high`, `medium`, or `low`.
- REQ-VAL-004. `created` and `updated` must be valid `YYYY-MM-DD` dates.
- REQ-VAL-005. `updated` must be greater than or equal to `created`.
- REQ-VAL-006. `dependencies` must be a list of ticket reference strings.
- REQ-VAL-007. `tags` must be a list of strings.
- REQ-VAL-008. `agent_created` must be a boolean.
- REQ-VAL-009. `complexity`, when present, must be an integer from 1 to 10.
- REQ-VAL-010. The frontmatter `id` prefix must match the declared `type`.

### Dependency Reference Validation

- REQ-DEP-001. The validator must build an index of all scanned ticket IDs before validating references.
- REQ-DEP-002. Duplicate ticket IDs across the scanned set must produce errors listing every file that declares the duplicate.
- REQ-DEP-003. Every dependency reference must resolve to exactly one scanned ticket, unless unresolved external references are explicitly allowed by configuration.
- REQ-DEP-004. Cross-epic dependency syntax must support `EPIC-<id>/<TICKET-ID>` and resolve both the epic and child ticket.
- REQ-DEP-005. Bare dependency IDs in `task` tickets must resolve within the current parent epic first.
- REQ-DEP-006. A dependency reference that resolves to the ticket itself must produce an error.
- REQ-DEP-007. The dependency graph must be checked for cycles. Any cycle must produce an error listing the cycle path.
- REQ-DEP-008. A ticket with `status: done` must not depend on a ticket whose status is `to-do`, `in-progress`, or `blocked`.
- REQ-DEP-009. A ticket with `status: blocked` should have at least one unresolved or incomplete dependency, or an explicit body note explaining the blocker; otherwise produce a warning.

### Parent And Epic Consistency

- REQ-EPC-001. Every non-empty `parent` must resolve to an existing `epic` ticket.
- REQ-EPC-002. Every `task` ticket must have a parent epic.
- REQ-EPC-003. An `epic` ticket must not declare a `parent`.
- REQ-EPC-004. If an epic has a `## Sub-tickets` table, every listed ticket ID must resolve to a scanned ticket whose `parent` points to that epic.
- REQ-EPC-005. If an epic has a `## Sub-tickets` table, the table status for each child must match the child ticket frontmatter status.
- REQ-EPC-006. If an epic has a `## Merge order` section, every listed ticket ID must resolve to a scanned child ticket.
- REQ-EPC-007. If a closure chore convention is present in merge order, the closure chore must be last; until this convention is confirmed, report violations as warnings.
- REQ-EPC-008. An epic with `status: done` must have all listed or discovered child tickets marked `done`.

### Lifecycle Consistency

- REQ-LFC-001. A ticket with `status: done` must include a `## Outcome` section.
- REQ-LFC-002. A `## Outcome` section on a `done` ticket must contain the seven expected subsections in order: `Summary`, `Key decisions`, `Constraints & invariants discovered (keep)`, `Implementation notes (high signal only)`, `Verification`, `Risk / regression surface`, and `Retrieval tags`.
- REQ-LFC-003. A ticket with `status: done` must have at least one verification command or explicit verification note in its body.
- REQ-LFC-004. A ticket that is not `done` may include `## Outcome`, but this should produce a warning because outcome content is intended for completed work.
- REQ-LFC-005. A ticket marked `done` must not contain unchecked acceptance criteria unless the unchecked item is explicitly marked not applicable.
- REQ-LFC-006. A ticket marked `to-do` should not have completed verification logs or outcome content; report as warning.
- REQ-LFC-007. A ticket marked `blocked` should include a blocker explanation in `## Notes`, `## Outcome`, or a dedicated blocker section; missing explanation is a warning.
- REQ-LFC-008. Lifecycle checks must distinguish errors that make the ticket unsafe to execute from warnings that indicate convention drift.

### Body Section Validation

- REQ-BDY-001. The validator must verify that each ticket body contains the major sections required by its type template.
- REQ-BDY-002. All executable ticket types must include `## Acceptance criteria`.
- REQ-BDY-003. All non-epic executable ticket types must include `## Verification`.
- REQ-BDY-004. `feature`, `bug`, `chore`, `refactor`, and `task` tickets must include `## Constraints`.
- REQ-BDY-005. `epic` tickets must include `## Sub-tickets`, `## Merge order`, and `## Acceptance criteria`.
- REQ-BDY-006. Missing body sections should be errors for non-draft tickets and warnings for template drafts, if draft mode is later defined.

### Reporting And Exit Behavior

- REQ-RPT-001. The validator must emit diagnostics with `severity`, `rule_id`, `file`, `ticket_id`, `message`, and `hint`.
- REQ-RPT-002. The validator must produce a summary count by severity and rule group.
- REQ-RPT-003. The validator must exit non-zero when any error is found.
- REQ-RPT-004. The validator must exit zero when only warnings are found, unless strict mode is enabled.
- REQ-RPT-005. Output should support a human-readable format and a machine-readable JSON format.
- REQ-RPT-006. Diagnostics should be stable enough for CI snapshots and agent follow-up prompts.

## Severity Guidelines

- Error: malformed frontmatter, missing required fields, invalid status, unresolved required references, duplicate IDs, dependency cycles, impossible done-with-incomplete-dependency states.
- Warning: unknown fields, missing optional sections, unconfirmed closure chore ordering, blocked tickets without enough explanation, outcome content on non-done tickets.
- Info: aggregate counts, scan roots, skipped files, and configuration defaults.

## Acceptance Criteria

- AC-001. Given a markdown ticket with no frontmatter, validation reports `REQ-FM-003` as an error and exits non-zero.
- AC-002. Given a ticket with `status: MERGED`, validation reports `REQ-VAL-002` as an error because review outcome states are not ticket statuses.
- AC-003. Given two files with the same frontmatter `id`, validation reports `REQ-DEP-002` and lists both file paths.
- AC-004. Given a ticket that depends on a missing ticket ID, validation reports `REQ-DEP-003` with the unresolved reference.
- AC-005. Given dependency edges `TASK-001 -> TASK-002 -> TASK-001`, validation reports `REQ-DEP-007` and prints the cycle path.
- AC-006. Given a `task` ticket without `parent`, validation reports `REQ-FLD-004`.
- AC-007. Given a child ticket whose `parent` points to a missing epic, validation reports `REQ-EPC-001`.
- AC-008. Given an epic sub-ticket table whose child status differs from the child file frontmatter, validation reports `REQ-EPC-005`.
- AC-009. Given a ticket with `status: done` and no `## Outcome`, validation reports `REQ-LFC-001`.
- AC-010. Given a ticket with `status: done` that depends on `status: blocked`, validation reports `REQ-DEP-008`.
- AC-011. Given a valid minimal `task` ticket with a resolved parent, valid dependencies, valid dates, and required body sections, validation exits zero.
- AC-012. Given only warnings, validation exits zero in default mode and non-zero in strict mode.

## Verification Plan

- VP-001. Add fixture-based tests for each ticket type template with a passing minimal example.
- VP-002. Add negative fixtures for malformed YAML, missing required fields, invalid enum values, duplicate IDs, unresolved dependencies, dependency cycles, and lifecycle mismatches.
- VP-003. Add table parsing fixtures for epic `## Sub-tickets` status consistency.
- VP-004. Add outcome schema fixtures for done tickets with missing, reordered, or partial `## Outcome` subsections.
- VP-005. Add CLI or script-level tests that confirm exit-code behavior for clean, warning-only, and error-containing scans.
- VP-006. Run the validator against an empty workspace and confirm it reports zero tickets scanned without error.

## Suggested Implementation Shape

This section is intentionally non-code and describes shape only.

- A parser layer reads markdown files, separates YAML frontmatter from body, and records parse diagnostics.
- A model layer normalizes tickets into typed records with source path, frontmatter values, headings, and table extracts.
- A graph layer indexes IDs, parents, dependencies, cross-epic references, and detects cycles.
- A lifecycle layer applies status-dependent rules.
- A reporter layer formats diagnostics for humans and machines.

## Open Decisions

- OD-001. Confirm the canonical status allowlist before hard-coding it.
- OD-002. Decide whether task tickets should inherit `priority` and `tags` requirements from other executable ticket types.
- OD-003. Decide whether archived tickets are part of the default scan.
- OD-004. Decide whether placeholder template IDs like `FEAT-XXX` should be accepted in draft mode or always rejected in real tickets.
- OD-005. Decide whether body section validation belongs in the first release or should follow frontmatter and graph validation.
- OD-006. Decide whether a configuration file is needed for workspace-specific overrides.

## Out Of Scope For First Release

- Git-history-based transition validation.
- Automatic fixes or formatting.
- Creation of missing tickets.
- Semantic validation of acceptance criteria quality.
- Execution of verification commands.
- Integration with PR or branch orchestration beyond producing validation diagnostics.
