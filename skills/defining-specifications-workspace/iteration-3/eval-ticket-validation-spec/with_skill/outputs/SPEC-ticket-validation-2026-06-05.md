# Specification: `.tickets/` Ticket Validation Capability

Status: Draft
Date: 2026-06-05
Owner/Requester: Hamza Amjad (workspace owner)
Primary Consumers: AI coding agents, human reviewers
Source Context:
- `skills/ticket-workflow/SKILL.md` (directory structure, naming, status lifecycle, dependency ID resolution, required frontmatter, execution protocol)
- `skills/ticket-workflow/references/templates.md` (per-type frontmatter fields and required-vs-optional fields)
- `skills/ticket-workflow/references/outcome-schema.md` (`## Outcome` requirement for `done` tickets)
- `skills/ticket-workflow/references/complexity-scoring.md` (`complexity` field semantics)
- `skills/ticket-workflow/scripts/archive-search.sh` (existing in-repo tooling conventions: bash, `set -euo pipefail`, frontmatter/section extraction, safe-on-empty behavior)
- `.gitignore` (evidence that `.tickets/` is per-workspace and untracked)

## For Implementing Agents

This spec defines a **new validation capability** for the `.tickets/` workflow. Its primary consumer is another AI agent, so treat it as an agent handoff.

- **Authoritative sections:** `Requirements`, `Diagnostic Model`, `Non-Goals`, and `Acceptance Criteria`. Build to these.
- **`Assumptions` are unconfirmed.** They encode the most defensible reading of the ticket-workflow conventions, but each names what would invalidate it. Do not treat them as settled fact.
- **`Open Questions` are blockers, not guesses.** Several (Q-001 language, Q-003 invocation surface, Q-004 Outcome severity) materially change the build. Surface them to the requester rather than silently deciding; where this spec must proceed it states a provisional default and flags it.
- **Read-only constraint overrides defaults:** the tool, and the agent building it, must never mutate ticket files (NG-001, REQ-025, NFR-001).
- **Ground every rule in the cited convention.** Every diagnostic code in the Diagnostic Model traces to a specific line of `ticket-workflow/SKILL.md` or `templates.md`; do not invent additional rules without adding them here first.

## Summary

The `.tickets/` workflow (managed by the `ticket-workflow` skill) stores structured tickets as markdown files with YAML frontmatter, organized into epics, standalone tickets, and an archive. The conventions — required frontmatter, an allowed status enum, epic-scoped dependency resolution, and lifecycle rules like "`done` tickets carry an `## Outcome`" — are currently enforced only by agents reading the skill prose. Nothing mechanically checks that a ticket tree is internally consistent.

This spec defines a **read-only validator** that inspects every ticket markdown file under `.tickets/` and reports structured, severity-classified diagnostics for four classes of problem: (1) missing/malformed required frontmatter, (2) disallowed enum values (status, priority, type), (3) broken dependency references (unresolved bare IDs, dangling cross-epic refs, cycles), and (4) lifecycle/consistency violations (e.g., a `done` ticket whose dependency is not `done`, an archived epic with unfinished sub-tickets, a `TASK` with no parent epic). It exits non-zero when any error-severity diagnostic is found so agents and humans can use it as a gate.

The validator is a guardrail, not an author: it never creates, repairs, or reformats tickets.

## Problem Statement

Ticket conventions live in skill prose and are enforced manually. As epics multiply and agents create sub-tickets, several silent failure modes become likely:

- A `TASK` created without a `parent`, violating "TASKs only exist inside a parent epic," is not caught until an agent tries to resolve its scope.
- A `dependencies:` entry references a ticket that was renamed, archived, or never existed; the dependency check at execution time (SKILL Step 2) then fails confusingly mid-run instead of up front.
- A ticket is marked `status: done` while a ticket it depends on is still `to-do`, breaking the lifecycle invariant.
- An epic is archived (moved under `_archive/`) while a sub-ticket is still `in-progress`, so the archive — which is supposed to be completed history — is inconsistent.
- A `status` typo (`inprogress`, `todo`, `Done`) silently falls outside the lifecycle enum and breaks downstream filters.

A single mechanical check that an agent can run before orchestration, before archival, or as a pre-flight catches these cheaply.

## Goals

- G-001: Provide a single command that validates the structural and lifecycle consistency of a `.tickets/` tree and reports actionable, stable-coded diagnostics.
- G-002: Make the result usable as a gate: non-zero exit on errors so it can be invoked by an agent or a local hook.
- G-003: Ground every rule in an existing `ticket-workflow` convention, so the validator and the skill cannot drift apart silently.
- G-004: Emit machine-readable output so an AI agent can parse, prioritize, and act on diagnostics without scraping prose.
- G-005: Be safe to run anywhere, anytime — read-only, and a no-op success on a workspace with no tickets.

## Non-Goals

- NG-001: The validator does not mutate, repair, reformat, or re-sort ticket files; it is strictly read-only.
- NG-002: The validator does not create, transition, archive, or decompose tickets — those remain the `ticket-workflow` skill's responsibility.
- NG-003: The validator does not run `git`, create branches/worktrees, or verify that an epic's `branch:` actually exists in the repo (worktree/branch existence is out of scope).
- NG-004: The validator does not inspect `.prompts/orchestration/`, `docs/`, or any path outside `.tickets/`.
- NG-005: The validator does not judge prose quality (requirement wording, whether acceptance criteria are "good"); only the enumerated structural rules apply. (Optional structural lints are deferred — see Q-008.)
- NG-006: The validator does not auto-fix, rewrite, or suggest patches; it only reports.
- NG-007: The validator does not deep-validate the internal seven-subsection schema of an `## Outcome` block; it checks presence only (see Q-005).

## Users And Stakeholders

- AI coding agents (ticket creators, orchestrators, sub-ticket executors): run the validator as a pre-flight before orchestration, before archival, or after generating sub-tickets; consume machine-readable output.
- Workspace owner / human reviewer: runs it ad hoc to sanity-check a hand-edited ticket tree; reads human-readable output.
- The `ticket-workflow` skill itself: an authoritative, machine-checkable encoding of its own conventions.

## Current State

Confirmed from the cited sources:

- **Layout** (`SKILL.md` "Directory Structure"): `.tickets/_standalone/` (no-parent tickets), `.tickets/_archive/EPIC-<hex>_<slug>/` (completed epics, read-only), and active `.tickets/EPIC-<hex>_<slug>/` containing `_epic.md` plus `TYPE-NNN_*.md` sub-tickets.
- **Naming** (`SKILL.md` "Naming"): epic dirs `EPIC-<hex>_<slug>/` with a 4-char hex; sub-ticket files `TYPE-NNN_kebab-slug.md`; cross-epic references `EPIC-<hex>/TYPE-NNN`.
- **Types** (`SKILL.md` prefix table): `FEAT`→feature, `BUG`→bug, `REFAC`→refactor, `CHORE`→chore, `TASK`→task, `EPIC`→epic.
- **Status lifecycle** (`SKILL.md` "Status Lifecycle"): `to-do → in-progress → done`, plus `blocked`; `in-progress` is optional (a ticket may go `to-do → done` directly).
- **Required frontmatter** (`SKILL.md` "Sub-tickets" step 4): `id`, `title`, `type`, `status`.
- **Per-type fields** (`templates.md`): FEAT/BUG/CHORE/REFAC carry `id,title,type,status,priority,created,updated,parent,dependencies,tags,agent_created,complexity`; `priority` enum is `critical|high|medium|low`. `TASK` requires a non-empty `parent` ("required — cannot be empty; TASKs only exist inside a parent epic") and a `complexity` ("required for TASK"), with `agent_created: true`. `EPIC` carries `branch:` (the epic's primary branch) and no `parent`.
- **Dependency resolution** (`SKILL.md` "Dependency ID resolution"): bare IDs in `dependencies` resolve **within the ticket's current epic**; cross-epic deps must use `EPIC-<hex>/TYPE-NNN`; an agent resolving a bare ID with no in-epic match "must fail the dependency check, not search other epics globally."
- **Dependency gate** (`SKILL.md` Execution Step 2): "If any dependency status != `done`, STOP." This makes "a `done` ticket may not depend on a non-`done` ticket" a derivable lifecycle invariant.
- **Outcome on done** (`outcome-schema.md`): "Every ticket marked `done` from the point FEAT-003 lands must carry an `## Outcome` section." (Note the temporal qualifier — see Q-004.)
- **`.tickets/` is git-ignored** (`.gitignore` lines: `# Agent workflow artifacts ... .tickets/`). So tickets are local/untracked; a committed-file CI gate would never see them (see Q-003 and ASM-006).
- **Tooling conventions** (`archive-search.sh`): bash with `#!/usr/bin/env bash`, `set -euo pipefail`, `awk`-based frontmatter and section extraction, and a "no `.tickets/...` dir → print friendly message, exit 0" safe-on-empty pattern.

There is currently **no** validation tooling for active or standalone tickets; `archive-search.sh` only searches archived `## Outcome` blocks.

## Proposed Behavior

A command (provisionally `validate-tickets`) walks `.tickets/`, parses each ticket's frontmatter and body, applies the rules in the Diagnostic Model, and prints a deterministic, severity-classified report. Each finding carries a stable code (`TV-*`), a severity (`error`/`warning`), the file path, and a one-line message. The process exits non-zero if any `error` was emitted, zero otherwise (including warnings-only and the empty-workspace case).

The validator distinguishes **resolution scopes**: an active epic directory and `_standalone/` are each an independent scope for bare-ID dependency resolution and for `id` uniqueness. Archived epics are validated under a lighter rule set (archive invariant + reference integrity) because they are historical and may predate the current schema (ASM-008, Q-007).

## Diagnostic Model

The validator shall classify each diagnostic per this table (referenced by the EARS requirements below). `error` fails the run; `warning` is reported but does not by itself fail.

| Code | Category | Default severity | Condition |
|------|----------|------------------|-----------|
| TV-FM-001 | Frontmatter | error | File has missing or unparseable YAML frontmatter; graph/lifecycle rules are skipped for the file. |
| TV-FM-002 | Frontmatter | error | A universal required field (`id`, `title`, `type`, `status`) is absent or empty. |
| TV-FM-003 | Frontmatter | error | A type-specific required field is absent/empty: `task` missing non-empty `parent` or missing `complexity`. |
| TV-FM-004 | Frontmatter | warning | `epic` missing or malformed `branch:` (`epic/<hex>/<slug>`); provisional severity, see Q-009. |
| TV-EN-001 | Enum | error | `status` not in `{to-do, in-progress, done, blocked}`. |
| TV-EN-002 | Enum | error | `priority` present but not in `{critical, high, medium, low}`. |
| TV-EN-003 | Enum | error | `type` not in `{feature, bug, refactor, chore, task, epic}`. |
| TV-ID-001 | Identity | error | `type` value does not match the filename `TYPE` prefix per the prefix↔type map. |
| TV-ID-002 | Identity | error | Frontmatter `id` does not match the filename's `TYPE-NNN` / `EPIC-<hex>` component. |
| TV-ID-003 | Identity | error | Duplicate `id` within a single resolution scope (one epic dir, or `_standalone/`). |
| TV-DEP-001 | Dependency | error | A bare-ID dependency has no matching ticket in the ticket's own scope (no global fallback). |
| TV-DEP-002 | Dependency | error | A cross-epic dependency `EPIC-<hex>/TYPE-NNN` names an epic or ticket that does not exist. |
| TV-DEP-003 | Dependency | error | A dependency entry is neither a valid bare ID nor a valid cross-epic reference (malformed). |
| TV-DEP-004 | Dependency | error | A dependency cycle (including self-dependency) exists in the resolved graph. |
| TV-LC-001 | Lifecycle | warning | A `status: done` ticket has no `## Outcome` section; provisional severity, see Q-004. |
| TV-LC-002 | Lifecycle | error | A `status: done` ticket depends on a ticket whose status is not `done`. |
| TV-LC-003 | Lifecycle | warning | An epic's `## Sub-tickets` table status for a sub-ticket disagrees with that sub-ticket's frontmatter `status`. |
| TV-LC-004 | Lifecycle | error | An epic under `_archive/` (or any of its sub-tickets) has a status other than `done`. |
| TV-LC-005 | Lifecycle | error | A `type: task` ticket is outside an epic directory or has an empty `parent`. |

## Requirements

Discovery and safety:

- REQ-001: The validator shall discover and inspect every `*.md` ticket file under `.tickets/`, covering `_standalone/`, active `EPIC-<hex>_<slug>/`, and `_archive/` trees.
- REQ-002: If `.tickets/` is absent or contains no `*.md` ticket files, then the validator shall report that there is nothing to validate and exit zero.

Frontmatter and schema:

- REQ-003: If a ticket file has missing or unparseable YAML frontmatter, then the validator shall emit a TV-FM-001 error naming the path and shall skip dependency-graph and lifecycle rules for that file.
- REQ-004: When a ticket's frontmatter is parsed, the validator shall verify that each universal required field (`id`, `title`, `type`, `status`) is present and non-empty, emitting one TV-FM-002 error per violation.
- REQ-005: Where a ticket's `type` is `task`, the validator shall require a non-empty `parent` and a present `complexity`, emitting TV-FM-003 for each missing field.
- REQ-006: Where a ticket's `type` is `epic`, the validator shall require a `branch` field matching `epic/<hex>/<slug>`, emitting TV-FM-004 (warning) when it is absent or malformed.

Enumerations:

- REQ-007: When a ticket declares `status`, the validator shall require it to be one of `{to-do, in-progress, done, blocked}`, emitting TV-EN-001 otherwise.
- REQ-008: When a ticket declares `priority`, the validator shall require it to be one of `{critical, high, medium, low}`, emitting TV-EN-002 otherwise.
- REQ-009: When a ticket declares `type`, the validator shall require it to be one of `{feature, bug, refactor, chore, task, epic}`, emitting TV-EN-003 otherwise.

Identity and naming:

- REQ-010: When a ticket file is inspected, the validator shall verify its `type` value corresponds to the filename `TYPE` prefix per the prefix↔type map, emitting TV-ID-001 on mismatch.
- REQ-011: When a ticket file is inspected, the validator shall verify its frontmatter `id` matches the filename's `TYPE-NNN` (or `EPIC-<hex>`) component, emitting TV-ID-002 on mismatch.
- REQ-012: The validator shall detect duplicate `id` values within a single resolution scope (one active epic directory, or `_standalone/`) and emit TV-ID-003 naming the conflicting paths. Identical numeric IDs across different epics are not a violation.

Dependencies:

- REQ-013: If a `dependencies` entry is a bare ID with no matching ticket in the ticket's own scope (its epic, or `_standalone/` for standalone tickets), then the validator shall emit a TV-DEP-001 error naming the unresolved ID, without searching other epics.
- REQ-014: If a `dependencies` entry uses the cross-epic form `EPIC-<hex>/TYPE-NNN` and the referenced epic or ticket does not exist, then the validator shall emit a TV-DEP-002 error.
- REQ-015: If a `dependencies` entry matches neither a valid bare ID nor a valid cross-epic reference, then the validator shall emit a TV-DEP-003 malformed-reference error.
- REQ-016: The validator shall detect cycles in the resolved dependency graph (including self-dependencies) and emit a TV-DEP-004 error listing the cycle members.

Lifecycle consistency:

- REQ-017: When a ticket has `status: done`, the validator shall require a `## Outcome` section to be present, emitting TV-LC-001 (warning by default) when it is absent.
- REQ-018: While a ticket has `status: done`, if any of its resolvable dependencies has a status other than `done`, then the validator shall emit a TV-LC-002 error naming the offending dependency.
- REQ-019: When an epic's `## Sub-tickets` table lists a status for a sub-ticket, the validator shall compare it to that sub-ticket's frontmatter `status` and emit TV-LC-003 (warning) on mismatch.
- REQ-020: While an epic resides under `_archive/`, the validator shall require the epic and every sub-ticket within it to have `status: done`, emitting TV-LC-004 otherwise.
- REQ-021: If a `type: task` ticket is located outside an epic directory (e.g., in `_standalone/`) or has an empty `parent`, then the validator shall emit a TV-LC-005 error.

Output, exit, and boundaries:

- REQ-022: The validator shall print each diagnostic with its stable code, severity, file path, and message, classifying severity per the Diagnostic Model.
- REQ-023: The validator shall exit non-zero when at least one `error`-severity diagnostic is emitted, and exit zero when only warnings or no diagnostics are emitted.
- REQ-024: The validator shall provide a machine-readable output mode (JSON: one object per diagnostic with at least `code`, `severity`, `path`, `message`) in addition to the default human-readable text mode.
- REQ-025: The validator shall not create, modify, delete, or reformat any ticket file or any other workspace file during a run.

## Nonfunctional Requirements

- NFR-001: Read-only. A validation run produces zero filesystem mutations under `.tickets/` or elsewhere (verifiable by comparing mtimes / `git status` before and after).
- NFR-002: Safe on empty/fresh workspaces — no `.tickets/` directory is a successful no-op, mirroring `archive-search.sh`.
- NFR-003: Deterministic output — diagnostics are emitted in a stable order (e.g., sorted by path, then code) so repeated runs and diffs are stable and agent-parseable.
- NFR-004: No heavy new dependencies — the tool shall run using utilities already implied by the workspace (POSIX shell + `awk`/ripgrep as used by `archive-search.sh`, or Python standard library only). A YAML dependency, if introduced, must be justified against Q-001.
- NFR-005: Performance — validating a tree of up to a few hundred tickets completes in well under a few seconds on a developer laptop.
- NFR-006: Each diagnostic is independently actionable and self-contained (path + code + message on its own record); the validator continues after a finding rather than aborting on the first error (except per REQ-003, where graph rules are skipped only for the unparseable file).

## Technical Context

- The existing `archive-search.sh` establishes the in-repo style: `#!/usr/bin/env bash`, `set -euo pipefail`, `awk` to extract frontmatter (between the first two `---` lines) and to extract a `##` section until the next `## ` heading, plus `nullglob`/`globstar` directory walking and a safe-on-missing-dir guard. A bash validator could reuse these extraction patterns directly (ASM-005). The workspace `.gitignore` also shows Python tooling (`.pytest_cache`, `.ruff_cache`, `.mypy_cache`), so Python stdlib is an equally viable host — this is the substance of Q-001.
- Resolution scope matters for several rules: dependency resolution (REQ-013) and `id` uniqueness (REQ-012) are scoped to a single epic dir or to `_standalone/`. The implementer should build a per-scope index of `{id → ticket}` first, then evaluate dependency and lifecycle rules against it.
- Cross-epic references (REQ-014) require a global index of `{EPIC-<hex> → {id → ticket}}` across active (and possibly archived, per Q-007) epics.
- Path note: `ticket-workflow/SKILL.md` refers to scripts under `.claude/skills/ticket-workflow/...`, but in this workspace the skill lives at `skills/ticket-workflow/...`. The validator should locate the ticket root relative to the invocation/repo root rather than hardcoding either prefix (RISK-005).

## Implementation Slices

- SLICE-001: Frontmatter parsing + universal/type-specific required-field checks + enum checks + identity checks (TV-FM-*, TV-EN-*, TV-ID-*).
- SLICE-002: Per-scope and cross-epic dependency index, reference resolution, and cycle detection (TV-DEP-*).
- SLICE-003: Lifecycle consistency rules — Outcome presence, done-deps-done, epic table sync, archive invariant, task-parent rule (TV-LC-*).
- SLICE-004: Output formatting (deterministic text + JSON), exit-code semantics, and empty-workspace handling.

(Slices are lightweight orientation only; ticket decomposition is downstream and out of scope for this spec.)

## Testing And Verification

- TEST-001 (verifies REQ-001, REQ-023): a fixture tree of fully valid tickets → no diagnostics, exit 0.
- TEST-002 (verifies REQ-002): no `.tickets/` directory → "nothing to validate", exit 0.
- TEST-003 (verifies REQ-003): a ticket whose frontmatter is not valid YAML → exactly one TV-FM-001 for that path, graph rules skipped, exit 1.
- TEST-004 (verifies REQ-004): a ticket missing `status` → TV-FM-002, exit 1.
- TEST-005 (verifies REQ-005, REQ-021): a `type: task` with empty `parent` in `_standalone/` → TV-FM-003 and TV-LC-005, exit 1.
- TEST-006 (verifies REQ-007): `status: Done` (wrong case) → TV-EN-001, exit 1.
- TEST-007 (verifies REQ-010, REQ-011): file `FEAT-001_*.md` with `type: bug` / `id: BUG-002` → TV-ID-001 and TV-ID-002.
- TEST-008 (verifies REQ-013): a bare dependency `FEAT-999` with no in-epic match → one TV-DEP-001 naming `FEAT-999`, exit 1.
- TEST-009 (verifies REQ-014): cross-epic dep `EPIC-zzzz/FEAT-001` with no such epic → TV-DEP-002.
- TEST-010 (verifies REQ-016): two tickets depending on each other → TV-DEP-004 listing both, exit 1.
- TEST-011 (verifies REQ-017): a `done` ticket with no `## Outcome` → TV-LC-001 warning; with no other findings, exit 0.
- TEST-012 (verifies REQ-018): a `done` ticket depending on a `to-do` ticket → TV-LC-002, exit 1.
- TEST-013 (verifies REQ-020): an `_archive/` epic with an `in-progress` sub-ticket → TV-LC-004, exit 1.
- TEST-014 (verifies REQ-024): JSON mode output parses as valid JSON with one record per diagnostic carrying `code`, `severity`, `path`, `message`.
- TEST-015 (verifies REQ-025, NFR-001): capture `git status` + file mtimes before and after a run → identical (no writes).
- TEST-016 (verifies NFR-003): two consecutive runs on the same tree → byte-identical output.

## Rollout, Migration, And Operations

- No data migration. The tool is additive and read-only.
- Invocation surface is an open question (Q-003). Because `.tickets/` is git-ignored, a CI gate on committed files cannot see tickets; the realistic surfaces are (a) manual/agent CLI invocation as an orchestration/archival pre-flight, and (b) an optional local pre-commit hook for contributors who track tickets locally. Default to a documented CLI command; defer hook wiring until Q-003 is resolved.
- Suggested home for the script (pending Q-002): `skills/ticket-workflow/scripts/validate-tickets.{sh,py}`, alongside `archive-search.sh`.

## Risks And Mitigations

- RISK-001: YAML edge cases (block lists, multi-line values, quoting) make naive frontmatter parsing brittle. / Mitigation: either use a real YAML parser (favors Python, Q-001) or constrain parsing to the simple flat subset the templates actually use and emit TV-FM-001 on anything outside it.
- RISK-002: Over-strict rules generate false positives and erode trust. / Mitigation: the error/warning split with conservative defaults; promote a warning to error only after the relevant open question is resolved.
- RISK-003: `.tickets/` is git-ignored, so a committed-file CI gate cannot enforce validation. / Mitigation: position as a local/agent pre-flight tool; document the limitation (Q-003).
- RISK-004: Archived tickets may predate the current schema and trip current rules. / Mitigation: apply only the archive invariant + reference-integrity rules to `_archive/`, deferring full schema strictness there (ASM-008, Q-007).
- RISK-005: Hardcoding `.claude/skills/...` vs `skills/...` paths breaks portability. / Mitigation: resolve the ticket root relative to repo/invocation root, never a hardcoded skill prefix.

## Open Questions

- Q-001: Implementation language — bash (maximal consistency with `archive-search.sh`, no YAML dependency, but harder YAML/cycle logic) vs Python (stdlib `tomllib`-style robustness, easier graph/cycle code, `.gitignore` shows Python tooling present)? Materially affects RISK-001 and NFR-004. Provisional default: bash (ASM-005).
- Q-002: Exact script path and name (`skills/ticket-workflow/scripts/validate-tickets.*`) and whether it should be referenced from `ticket-workflow/SKILL.md`.
- Q-003: Intended invocation surface — manual CLI only, agent pre-flight, and/or a local git pre-commit hook? Given `.tickets/` is git-ignored, is a CI gate even desired?
- Q-004: Severity of missing `## Outcome` on `done` tickets. The schema says "from the point FEAT-003 lands"; should pre-FEAT-003 / archived tickets be exempt, and should TV-LC-001 be an error rather than a warning for current tickets?
- Q-005: Should the validator deep-validate the `## Outcome` block's seven-subsection schema (`outcome-schema.md`), or check presence only (current scope, NG-007)?
- Q-006: Should `created`/`updated` be validated for `YYYY-MM-DD` format and `updated >= created`? Currently unspecified.
- Q-007: Should archived tickets receive full schema validation, or only the archive invariant (TV-LC-004) plus reference integrity? Provisional: lighter set (ASM-008).
- Q-008: Should the `ticket-workflow` quality rules (ticket < 200 lines, ≤ 5 acceptance criteria, `## Verification` present) be enforced as warnings, or remain out of scope (NG-005)?
- Q-009: Should a missing/malformed epic `branch:` (TV-FM-004) be an error or a warning? It is procedurally required at creation but not in the universal required-field list.

## Assumptions

- ASM-001: The enums are `status ∈ {to-do, in-progress, done, blocked}`, `priority ∈ {critical, high, medium, low}`, `type ∈ {feature, bug, refactor, chore, task, epic}`. Confidence: high (SKILL + templates). Invalidated if the skill adds/renames a value.
- ASM-002: The universal required frontmatter fields are exactly `id`, `title`, `type`, `status`. Confidence: high (SKILL "Sub-tickets" step 4). Invalidated if the skill widens the required set.
- ASM-003: A `task` requires a non-empty `parent` and a present `complexity`; other types do not require `parent`. Confidence: high (templates.md TASK block). Invalidated if TASK frontmatter changes.
- ASM-004: Bare dependency IDs resolve within the ticket's own epic; standalone tickets resolve bare IDs within `_standalone/`; cross-epic deps use `EPIC-<hex>/TYPE-NNN`. Confidence: high for epics (SKILL "Dependency ID resolution"); medium for the `_standalone/` scoping, which the skill does not state explicitly.
- ASM-005: The default implementation language is bash, mirroring `archive-search.sh` conventions. Confidence: medium — Q-001 may overturn this.
- ASM-006: The validator is a local/agent-run tool rather than a committed-file CI gate, because `.tickets/` is git-ignored. Confidence: high (`.gitignore`). Invalidated if tickets become tracked.
- ASM-007: Missing `## Outcome` on a `done` ticket is a warning pending Q-004. Confidence: medium.
- ASM-008: Archived tickets are validated under a lighter rule set (archive invariant + reference integrity), not full current-schema strictness, since they are read-only history that may predate the schema. Confidence: medium — Q-007 may overturn this.

## Acceptance Criteria

- AC-001 (verifies REQ-001, REQ-022, REQ-023):
  - Given a `.tickets/` tree where every ticket conforms to all rules,
  - When the validator runs,
  - Then it prints no `error` or `warning` diagnostics and exits 0.
- AC-002 (verifies REQ-002):
  - Given a workspace with no `.tickets/` directory,
  - When the validator runs,
  - Then it prints a "nothing to validate" message and exits 0.
- AC-003 (verifies REQ-003):
  - Given a ticket file whose frontmatter is not valid YAML,
  - When the validator runs,
  - Then it emits exactly one TV-FM-001 referencing that path, applies no dependency/lifecycle rule to that file, and exits 1.
- AC-004 (verifies REQ-004):
  - Given a ticket missing the `status` field,
  - When the validator runs,
  - Then it emits a TV-FM-002 naming `status` and the path, and exits 1.
- AC-005 (verifies REQ-007):
  - Given a ticket with `status: Done`,
  - When the validator runs,
  - Then it emits a TV-EN-001 for that ticket and exits 1.
- AC-006 (verifies REQ-010, REQ-011):
  - Given a file `FEAT-001_x.md` whose frontmatter has `type: bug` and `id: BUG-002`,
  - When the validator runs,
  - Then it emits both a TV-ID-001 (type/prefix mismatch) and a TV-ID-002 (id/filename mismatch) for that file and exits 1.
- AC-007 (verifies REQ-013):
  - Given an epic containing a ticket with `dependencies: [FEAT-999]` and no `FEAT-999` in that epic,
  - When the validator runs,
  - Then it emits exactly one TV-DEP-001 naming `FEAT-999` as unresolved, does not resolve it from another epic, and exits 1.
- AC-008 (verifies REQ-014):
  - Given a ticket with `dependencies: [EPIC-zzzz/FEAT-001]` where no epic `EPIC-zzzz` exists,
  - When the validator runs,
  - Then it emits a TV-DEP-002 for that reference and exits 1.
- AC-009 (verifies REQ-016):
  - Given two tickets in one epic that list each other in `dependencies`,
  - When the validator runs,
  - Then it emits a TV-DEP-004 naming both ticket IDs as a cycle and exits 1.
- AC-010 (verifies REQ-017):
  - Given a single ticket with `status: done` and no `## Outcome` section, and no other violations,
  - When the validator runs,
  - Then it emits one TV-LC-001 warning and exits 0 (warnings alone do not fail).
- AC-011 (verifies REQ-018):
  - Given a ticket `A` with `status: done` and `dependencies: [B]`, where `B` has `status: to-do`,
  - When the validator runs,
  - Then it emits a TV-LC-002 naming `B` and exits 1.
- AC-012 (verifies REQ-020):
  - Given an epic under `_archive/` whose `_epic.md` is `done` but one sub-ticket is `in-progress`,
  - When the validator runs,
  - Then it emits a TV-LC-004 for the non-`done` member and exits 1.
- AC-013 (verifies REQ-021):
  - Given a file `TASK-001_x.md` with `type: task` in `.tickets/_standalone/`,
  - When the validator runs,
  - Then it emits a TV-LC-005 for that file and exits 1.
- AC-014 (verifies REQ-024):
  - Given any tree that produces at least one diagnostic and the JSON output mode is selected,
  - When the validator runs,
  - Then stdout is valid JSON containing one record per diagnostic, each with `code`, `severity`, `path`, and `message`.
- AC-015 (verifies REQ-025, NFR-001):
  - Given any `.tickets/` tree,
  - When the validator runs,
  - Then no ticket file's content or mtime changes and `git status` is unchanged versus before the run.
- AC-016 (verifies NFR-003):
  - Given the same `.tickets/` tree and identical flags,
  - When the validator runs twice,
  - Then the two outputs are byte-identical.
- AC-017 (verifies REQ-005):
  - Given a `type: task` ticket inside an epic with a non-empty `parent` but no `complexity` field,
  - When the validator runs,
  - Then it emits a TV-FM-003 naming the missing `complexity` and exits 1.
- AC-018 (verifies REQ-008, REQ-009):
  - Given a ticket with `type: feat` (not an allowed type) and `priority: urgent` (not an allowed priority),
  - When the validator runs,
  - Then it emits a TV-EN-003 for the type and a TV-EN-002 for the priority and exits 1.
- AC-019 (verifies REQ-012):
  - Given one epic directory containing two files that both declare `id: FEAT-001`,
  - When the validator runs,
  - Then it emits a TV-ID-003 naming both conflicting paths and exits 1.
- AC-020 (verifies REQ-015):
  - Given a ticket whose `dependencies` contains an entry that is neither a valid bare ID nor a valid `EPIC-<hex>/TYPE-NNN` reference (e.g. `feat_1`),
  - When the validator runs,
  - Then it emits a TV-DEP-003 for that entry and exits 1.
- AC-021 (verifies REQ-019):
  - Given an epic whose `## Sub-tickets` table lists `FEAT-001` as `done` while `FEAT-001`'s frontmatter `status` is `to-do`, and no other violations,
  - When the validator runs,
  - Then it emits a TV-LC-003 warning naming `FEAT-001` and exits 0.
- AC-022 (verifies REQ-006):
  - Given an `_epic.md` with no `branch` field, and no other violations,
  - When the validator runs,
  - Then it emits a TV-FM-004 warning for that epic and exits 0.

## Source References

- `skills/ticket-workflow/SKILL.md` — Directory Structure, Naming, prefix table, Status Lifecycle, Dependency ID resolution, Sub-tickets required frontmatter, Execution Protocol Step 2, Epic Closure, Quality Rules.
- `skills/ticket-workflow/references/templates.md` — per-type frontmatter, TASK `parent`/`complexity` requirements, `priority` enum, EPIC `branch`.
- `skills/ticket-workflow/references/outcome-schema.md` — `## Outcome` requirement for `done` tickets and the FEAT-003 temporal qualifier.
- `skills/ticket-workflow/references/complexity-scoring.md` — `complexity` integer semantics.
- `skills/ticket-workflow/scripts/archive-search.sh` — bash tooling conventions, frontmatter/section extraction, safe-on-empty behavior.
- `.gitignore` — `.tickets/` is per-workspace and untracked.
- Companion notes: `NOTES-ticket-validation-2026-06-05.md` (context-inspection log and clarifying-question rationale).
