# Specification: Ticket Validation Capability

Status: Ready for Review
Date: 2026-06-05
Owner/Requester: Hamza Amjad
Primary Consumers: AI coding agents, human reviewers
Source Context:
- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/templates.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/outcome-schema.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/complexity-scoring.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/orchestrator-review-protocol.md`

## Summary

Add a validation capability for `.tickets/` markdown files in this `.agents` workspace. The validator should inspect ticket frontmatter and markdown structure against the ticket workflow contract, catch invalid statuses and broken dependency references, and flag lifecycle inconsistencies before agents execute, orchestrate, or archive tickets.

The first version should be a read-only checker. It should produce clear diagnostics that identify the file, ticket ID when available, severity, rule ID, and a short fix hint. It must not create tickets, mutate frontmatter, archive epics, run implementation verification commands, or make workflow decisions for agents.

## Problem Statement

The ticket workflow relies on agents reading and trusting `.tickets/` markdown files. Invalid frontmatter, drift from template fields, unresolved dependencies, or inconsistent lifecycle state can cause agents to start blocked work, mark tickets done incorrectly, miss closure obligations, or corrupt archive history. A deterministic validator is needed as an early quality gate for ticket authoring and orchestration.

## Goals

- G-001: Validate required ticket frontmatter keys and value shapes for epic, feature, bug, chore, refactor, and task tickets.
- G-002: Enforce allowed ticket status values and type/id/path consistency.
- G-003: Resolve `dependencies` and `parent` references using the workspace's documented scoping rules.
- G-004: Detect lifecycle consistency issues involving blocked work, done tickets, epic closure, archive state, and outcome records.
- G-005: Return actionable diagnostics suitable for humans, AI agents, and CI-style checks.
- G-006: Keep the validator read-only and scoped to `.tickets/` markdown files.

## Non-Goals

- NG-001: Do not create, update, decompose, archive, or close tickets.
- NG-002: Do not implement ticket execution, orchestration, worktree setup, PR creation, or merge logic.
- NG-003: Do not run ticket `## Verification` commands or inspect implementation diffs.
- NG-004: Do not validate every subjective quality rule in ticket prose, such as whether requirements are well-written.
- NG-005: Do not introduce persistent infrastructure, external services, semantic search, or database storage for validation.
- NG-006: Do not treat archived tickets as mutable or auto-repair historical files.

## Users And Stakeholders

- Ticket-authoring agents: Need immediate feedback when generated tickets violate the workflow contract.
- Ticket-executing agents: Need confidence that dependencies, status, scope, and closure metadata are trustworthy before starting work.
- Orchestrator agents: Need a deterministic preflight gate before assigning sub-tickets and closing epics.
- Human reviewers: Need concise diagnostics that explain what is invalid and where to inspect.

## Current State

The workspace has a `ticket-workflow` skill that defines the ticket system, but no active `.tickets/` directory was present during this context review. The documented directory layout is:

- `.tickets/_standalone/` for standalone tickets.
- `.tickets/EPIC-<hex>_<slug>/` for active epics.
- `.tickets/EPIC-<hex>_<slug>/_epic.md` for the epic ticket.
- `.tickets/EPIC-<hex>_<slug>/TYPE-NNN_*.md` for sub-tickets.
- `.tickets/_archive/EPIC-<hex>_<slug>/` for completed epics, which are read-only historical context.

The workflow defines ticket prefixes `FEAT`, `BUG`, `REFAC`, `CHORE`, `TASK`, and `EPIC`; status values `to-do`, `in-progress`, `done`, and `blocked`; and dependency resolution where bare IDs resolve only within the current epic while cross-epic dependencies use `EPIC-<hex>/TYPE-NNN`.

Ticket templates define frontmatter fields for each ticket type, and the execution protocol adds lifecycle requirements: dependencies must be `done` before execution, `complexity` is required for `TASK` tickets and for tickets with `parent:` or multi-file scope, done tickets must append an `## Outcome` section, and closure tickets mark all sub-tickets and the epic done before archiving.

## Proposed Behavior

Provide a read-only ticket validator that can be run against the workspace root or an explicit `.tickets/` path. The validator should discover ticket markdown files, parse YAML frontmatter and markdown headings, build an in-memory index of ticket IDs and locations, and evaluate deterministic rules.

When `.tickets/` is absent, the validator should exit successfully with an informational diagnostic rather than failing the workspace. When `.tickets/` exists, malformed ticket files, broken references, and lifecycle contradictions should produce diagnostics. The validator should distinguish between errors that make ticket execution unsafe and warnings that indicate template drift or review risk.

## Requirements

- REQ-001: The validator must discover ticket files only under `.tickets/`, including `_standalone`, active epic directories, and `_archive`, and must ignore non-markdown files.
- REQ-002: The validator must parse frontmatter as structured YAML and fail a ticket file if frontmatter is missing, malformed, or not a mapping.
- REQ-003: The validator must require `id`, `title`, `type`, and `status` for every ticket file.
- REQ-004: The validator must require template-defined frontmatter keys by ticket type, reporting missing optional-template fields as warnings when they are not execution-critical.
- REQ-005: The validator must enforce allowed `type` values: `feature`, `bug`, `refactor`, `chore`, `task`, and `epic`.
- REQ-006: The validator must enforce allowed `status` values: `to-do`, `in-progress`, `done`, and `blocked`.
- REQ-007: The validator must enforce ID prefix to type consistency: `FEAT` maps to `feature`, `BUG` maps to `bug`, `REFAC` maps to `refactor`, `CHORE` maps to `chore`, `TASK` maps to `task`, and `EPIC` maps to `epic`.
- REQ-008: The validator must enforce path to ID consistency for active epic directories, archived epic directories, `_epic.md`, sub-ticket files, and standalone ticket files.
- REQ-009: The validator must require `TASK` tickets to have non-empty `parent`, `dependencies`, `agent_created`, and `complexity` fields matching the task template contract.
- REQ-010: The validator must require epic tickets to have `branch`, `priority`, `created`, `updated`, `tags`, and `agent_created` fields, with `branch` matching `epic/<hex>/<slug>` for active epics when present.
- REQ-011: The validator must validate `dependencies` as an array of ticket references. Empty arrays are valid.
- REQ-012: The validator must resolve bare dependency IDs within the current epic only, and must not search other epics globally when a bare ID is missing.
- REQ-013: The validator must resolve cross-epic dependency IDs in the form `EPIC-<hex>/TYPE-NNN` against indexed tickets.
- REQ-014: The validator must flag dependencies that reference missing tickets, duplicate dependencies, self-dependencies, or references with invalid syntax.
- REQ-015: The validator must validate `parent` references when present, including requiring `TASK` parents to resolve to an indexed ticket or epic according to the same scoped-reference rules.
- REQ-016: The validator must flag `in-progress` or `done` tickets whose dependencies are not all `done`.
- REQ-017: The validator must flag archived tickets whose status is not `done`.
- REQ-018: The validator must flag active epic directories whose epic status is `done` while the directory has not been moved under `_archive`, unless an explicit transitional validation mode is enabled.
- REQ-019: The validator must require every ticket with `status: done` to contain an `## Outcome` section.
- REQ-020: The validator must validate the `## Outcome` section for the seven required subsections in the canonical order from `references/outcome-schema.md`.
- REQ-021: The validator must flag done tickets with unchecked items remaining under `## Acceptance criteria`.
- REQ-022: The validator must flag epics whose `## Sub-tickets` or `## Merge order` references sub-ticket IDs that do not exist in the same epic directory.
- REQ-023: The validator must flag epics that do not define a final closure `CHORE` ticket in merge order.
- REQ-024: The validator must require an epic to be `done` only when all sub-tickets in that epic are `done`.
- REQ-025: The validator must report diagnostics with stable rule IDs, severity, file path, line number when available, ticket ID when available, message, and suggested fix.
- REQ-026: The validator must return a non-zero process status when one or more error-severity diagnostics are present, and zero when only warnings or informational diagnostics are present.
- REQ-027: The validator must support validating archived tickets without modifying them or treating history as auto-fixable.

## Frontmatter Contract

The validator should treat these key sets as the initial contract:

- Epic tickets require: `id`, `title`, `type`, `status`, `priority`, `branch`, `created`, `updated`, `tags`, `agent_created`, `complexity`.
- Feature, bug, chore, and refactor tickets require: `id`, `title`, `type`, `status`, `priority`, `created`, `updated`, `parent`, `dependencies`, `tags`, `agent_created`, `complexity`.
- Task tickets require: `id`, `title`, `type`, `status`, `parent`, `dependencies`, `agent_created`, `complexity`.

`complexity` may be blank for epic, feature, bug, chore, and refactor tickets unless the ticket has a non-empty `parent` value or the validator can determine from file path hints that more than one real file is affected. `complexity` must be an integer from 1 to 10 when populated and is always required for `TASK` tickets.

## Diagnostic Model

- `error`: A violation that can make ticket execution, dependency ordering, archive state, or orchestration unsafe.
- `warning`: Template drift, missing optional metadata, or consistency risk that should be fixed but does not necessarily block safe inspection.
- `info`: Non-problematic state, such as `.tickets/` being absent.

Each diagnostic should include:

- `rule_id`: Stable identifier, for example `TV-FM-001`.
- `severity`: `error`, `warning`, or `info`.
- `path`: Workspace-relative file path.
- `line`: Best-effort line number.
- `ticket_id`: Parsed ticket ID if available.
- `message`: One-sentence explanation.
- `hint`: Short suggested remediation.

## Nonfunctional Requirements

- NFR-001: Validation must be read-only and deterministic for the same filesystem snapshot.
- NFR-002: Validation should complete quickly for typical workspaces; target under two seconds for hundreds of ticket markdown files.
- NFR-003: Diagnostics must be stable enough for CI snapshots and agent regression tests.
- NFR-004: The implementation should use a real frontmatter/YAML parser rather than ad hoc string splitting.
- NFR-005: The validator should not require network access, authentication, external services, or repository mutation.
- NFR-006: Rule definitions should be documented near the validator so future ticket workflow changes can update validation behavior without hunting through code.

## UX, Workflow, Or Interaction Notes

Primary workflows:

- Authoring preflight: An agent creates or edits tickets, runs validation, and fixes diagnostics before handing work to another agent.
- Execution preflight: An executing agent validates the assigned ticket and dependency graph before Step 2 dependency checks.
- Orchestration preflight: An orchestrator validates an epic before assigning sub-ticket work or running closure.
- Archive audit: A human or agent validates `_archive` read-only to find historical drift without modifying archived tickets.

The default output should be concise human-readable diagnostics. A structured JSON output mode is recommended for future CI or agent consumption, but it is not required for the first implementation unless the implementing agent determines the workspace already has a suitable pattern for machine-readable command output.

## Data, API, Or Contract Changes

No persisted data model or ticket schema migration is required. The capability formalizes validation rules over existing markdown/frontmatter contracts.

If a command-line interface is added, the public contract should include:

- Input: workspace root or `.tickets/` path.
- Output: diagnostics in human-readable form, with optional structured output if implemented.
- Exit code: `0` for no errors, `1` for validation errors, and `2` for validator runtime/configuration failures.

## Technical Context

The likely implementation area is the ticket workflow tooling, because the validator enforces the contract documented by `skills/ticket-workflow/SKILL.md` and `skills/ticket-workflow/references/*.md`. The exact file path is intentionally left to the implementing agent because no existing validator or `.tickets/` command structure was found during context review.

The validator should build an index before resolving relationships:

1. Discover candidate files.
2. Parse frontmatter and classify file location.
3. Index valid-enough IDs with path, type, status, epic scope, and archive/active location.
4. Run per-file frontmatter and path rules.
5. Run graph rules for dependencies and parents.
6. Run lifecycle rules for done tickets, epics, closure tickets, and archive state.
7. Emit diagnostics and final exit status.

## Implementation Slices

- SLICE-001: Add read-only discovery, frontmatter parsing, ticket indexing, and basic diagnostics for required fields, status, type, and ID/path consistency.
- SLICE-002: Add dependency and parent reference resolution using in-epic bare ID rules and cross-epic `EPIC-<hex>/TYPE-NNN` rules.
- SLICE-003: Add lifecycle validation for dependency completion, done ticket outcomes, checked acceptance criteria, archive state, and epic closure requirements.
- SLICE-004: Add fixtures and tests covering valid tickets, malformed frontmatter, broken dependencies, lifecycle contradictions, and absent `.tickets/` behavior.

## Testing And Verification

- TEST-001: Validate a workspace with no `.tickets/` directory and confirm the validator exits zero with an informational diagnostic.
- TEST-002: Validate a minimal valid standalone ticket and confirm no error diagnostics are emitted.
- TEST-003: Validate tickets with missing frontmatter, malformed YAML, missing `id`, missing `status`, and invalid `status` values; confirm error diagnostics include stable rule IDs and paths.
- TEST-004: Validate ID/type/path mismatches, including `FEAT-001` with `type: chore`, `_epic.md` with non-epic ID, and sub-ticket files whose filename ID differs from frontmatter.
- TEST-005: Validate bare dependency resolution inside an epic and confirm a missing in-epic bare ID fails without searching other epics.
- TEST-006: Validate cross-epic dependency references using `EPIC-<hex>/TYPE-NNN`, including missing epic and missing ticket cases.
- TEST-007: Validate `in-progress` and `done` tickets with incomplete dependencies and confirm they produce errors.
- TEST-008: Validate `status: done` tickets missing `## Outcome`, with malformed Outcome subsections, or with unchecked acceptance criteria.
- TEST-009: Validate archived epic folders with non-done tickets and active epic folders marked done but not archived.
- TEST-010: Validate epic `## Sub-tickets` and `## Merge order` references, including a missing final closure `CHORE`.

## Rollout, Migration, And Operations

No migration is required. The first rollout should be advisory for existing workspaces until fixture coverage confirms the rules align with real tickets. Once stable, the validator can become a required preflight step in ticket creation, orchestration, and closure workflows.

Archived tickets may contain historical drift. The validator should support auditing them, but the workflow's read-only archive rule means remediation should happen only through explicit human-approved follow-up, not auto-fixes.

## Risks And Mitigations

- RISK-001: The validator may over-enforce template fields that the ticket workflow currently treats as optional. Mitigation: distinguish execution-critical errors from template-completeness warnings.
- RISK-002: Markdown parsing of sections and checkboxes may be brittle. Mitigation: use conservative heading-based checks and avoid failing on ambiguous prose unless the lifecycle rule is explicit.
- RISK-003: Real archived tickets may not contain newer `## Outcome` sections. Mitigation: make archive strictness configurable or report legacy archive drift separately during first rollout.
- RISK-004: Dependency resolution can be ambiguous for standalone tickets. Mitigation: define standalone bare IDs as resolving only within `_standalone` and require cross-epic form for epic tickets outside the current scope.
- RISK-005: Future ticket workflow changes may drift from validator rules. Mitigation: keep rule IDs and schema constants close to ticket-workflow references and add tests tied to template examples.

## Open Questions

- Q-001: Should template-complete frontmatter keys such as `priority`, `created`, `updated`, `tags`, and `agent_created` be hard errors for all ticket types, or warnings except where execution depends on them?
- Q-002: Should archived tickets created before the Outcome schema requirement be grandfathered, or should archive validation always enforce current rules?
- Q-003: What command name and location should expose validation, for example a script under `skills/ticket-workflow/scripts/` versus a repo-level command?
- Q-004: Should blocked tickets require an explicit blocker reason field or markdown section, even though the current templates do not define one?
- Q-005: Should the first implementation emit JSON output, or is human-readable output sufficient until CI integration exists?
- Q-006: Should active epics marked `done` be a hard error immediately, or a warning to allow the closure ticket's brief pre-archive transition?

## Assumptions

- ASM-001: The ticket workflow skill and its references are the canonical source of truth for ticket validation. Confidence: high. Invalidated if another repo-level ticket schema exists outside the inspected files.
- ASM-002: Absence of `.tickets/` is valid for a workspace that has not created tickets yet. Confidence: medium. Invalidated if ticket validation is intended to require ticket system initialization.
- ASM-003: Frontmatter is YAML and `dependencies`/`tags` are arrays. Confidence: high. Invalidated if existing tickets use non-YAML frontmatter or scalar dependency syntax.
- ASM-004: Bare dependency IDs in `_standalone` resolve only within `_standalone`. Confidence: medium. Invalidated if standalone dependencies are expected to search all standalone and epic tickets globally.
- ASM-005: Validation should be implementable without modifying the ticket skill itself. Confidence: medium. Invalidated if the desired capability is explicitly part of the skill instructions rather than tooling.

## Acceptance Criteria

- AC-001: A downstream agent can implement the validator without needing additional clarification about required frontmatter, status values, dependency resolution, or lifecycle checks.
- AC-002: The validator's first implementation can be tested entirely with markdown fixtures and does not require existing `.tickets/` files in the workspace.
- AC-003: Broken dependency references, invalid statuses, missing required frontmatter, and done tickets without valid Outcome sections are reported as error-severity diagnostics.
- AC-004: Template drift and rollout-sensitive archive concerns can be reported without mutating ticket files.
- AC-005: The validator remains read-only and never creates tickets, source changes, commits, branches, worktrees, or implementation code.

## Source References

- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/templates.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/outcome-schema.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/complexity-scoring.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/orchestrator-review-protocol.md`
