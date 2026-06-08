---
title: Ticket Validation Capability for the `.agents` Workspace
spec_id: SPEC-ticket-validation
status: draft
version: 0.1
author: AI agent (baseline, no specialized skill)
date: 2026-06-05
reviewers: [unassigned]
related: [.tickets/ workflow convention]
---

# Ticket Validation Capability

## 1. Summary

Add a **ticket validation capability** to the `.agents` workspace that statically
inspects the markdown files in `.tickets/` and reports structural and semantic
problems before they cause downstream workflow failures. The validator checks
four families of rules:

1. **Required frontmatter** — every ticket has the mandatory metadata keys, with
   correct types and formats.
2. **Allowed status values** — the `status` field is one of a known, closed set.
3. **Dependency references** — `dependencies` (and similar links) point at real,
   non-self, non-cyclic tickets.
4. **Lifecycle consistency** — status and dependency state are mutually
   consistent (e.g., a closed ticket should not depend on an open one).

The capability is a read-only checker. It does not mutate tickets, create
tickets, or change workflow state. It is intended to run on demand by an agent or
human, and to be wired into pre-commit / CI later (out of scope for v1 build).

> Scope note: This is a *specification only*. No implementation code, tickets,
> branches, or commits are produced by this document.

## 2. Background & Motivation

The `.agents` workspace uses a `.tickets/` directory (confirmed as a tracked
convention in `.gitignore`, where `.tickets/` is listed as a per-workspace agent
workflow artifact) to coordinate multi-step work. Tickets are markdown files with
YAML frontmatter that encode metadata such as id, status, and dependencies.

Because tickets are hand- and agent-edited markdown, they drift:

- A ticket references a dependency ID that was renamed or never existed.
- A status is misspelled (`in progress` vs `in-progress`) and breaks filters.
- A ticket is marked `done` while a ticket it depends on is still `todo`.
- Two tickets share the same `id`, or a filename and its `id` disagree.
- Required fields (owner, created date) are missing.

These defects are cheap to introduce and expensive to debug mid-workflow. A fast,
deterministic validator gives a single authoritative answer to "are my tickets
well-formed and internally consistent?" and a machine-readable report that other
tooling can consume.

## 3. Goals

- **G1.** Detect structurally invalid tickets (missing/mistyped frontmatter,
  malformed YAML, unparseable files).
- **G2.** Enforce a closed vocabulary for `status` (and `type`/`priority` if
  defined).
- **G3.** Enforce dependency referential integrity: every referenced ticket
  exists, no self-dependencies, no dependency cycles, no duplicate IDs.
- **G4.** Detect lifecycle inconsistencies between a ticket's status and the
  status of its dependencies / children.
- **G5.** Produce both a human-readable report and a machine-readable (JSON)
  report, with stable rule IDs and clear severities (error vs warning).
- **G6.** Be deterministic, read-only, and fast enough to run on every
  invocation of the ticket workflow.

## 4. Non-Goals

- **N1.** Auto-fixing or rewriting tickets (a future `--fix` mode is explicitly
  out of scope for v1).
- **N2.** Creating, closing, archiving, or transitioning tickets.
- **N3.** Enforcing prose/content quality of ticket bodies (only frontmatter and
  cross-ticket structure are validated; body checks are optional warnings at
  most).
- **N4.** Defining the full ticket *workflow* (statuses, transitions) — this spec
  consumes the existing workflow's vocabulary; it does not redesign it.
- **N5.** Networked checks (e.g., resolving external issue trackers).
- **N6.** A GUI. The first interface is a CLI / callable function.

## 5. Assumptions

These assumptions are made because the canonical ticket schema lives in workspace
skill files that were intentionally **not read** for this baseline draft. Each
assumption is a candidate clarifying question (see companion notes file) and must
be confirmed before implementation. The validator's schema **must be
configuration-driven** so that confirmed values can be set without code changes.

- **A1.** Tickets live in `.tickets/` as one markdown file per ticket
  (e.g., `.tickets/TICK-0007.md`), possibly with subfolders (e.g., per-epic or an
  `archive/` subfolder).
- **A2.** Each ticket begins with a YAML frontmatter block delimited by `---`.
- **A3.** Assumed frontmatter schema (to be confirmed):
  - `id` (string, required, unique, matches a pattern like `^[A-Z]+-\d+$`)
  - `title` (string, required, non-empty)
  - `status` (string enum, required)
  - `type` (string enum, optional; e.g., `epic` | `ticket` | `task`)
  - `priority` (string enum, optional; e.g., `P0`..`P3` or `low`/`med`/`high`)
  - `dependencies` (list of ticket IDs, optional, default `[]`)
  - `epic` / `parent` (ticket ID, optional)
  - `owner` / `assignee` (string, optional)
  - `created` (date `YYYY-MM-DD`, required)
  - `updated` (date `YYYY-MM-DD`, optional)
- **A4.** Assumed allowed `status` set (to be confirmed):
  `backlog`, `todo`, `in-progress`, `blocked`, `in-review`, `done`, `cancelled`.
  Terminal statuses: `done`, `cancelled`.
- **A5.** Dependencies are referenced by `id` (not filename/path).
- **A6.** Implementation language/stack is Python (inferred from `.gitignore`
  entries for `ruff`, `mypy`, `pytest`, `.venv`), so the validator should be a
  small Python module + console entry point with no heavy dependencies (stdlib +
  a YAML parser).
- **A7.** Archived/cancelled tickets remain on disk and must still parse, but may
  be exempt from some lifecycle checks (configurable).

## 6. Definitions / Glossary

- **Ticket file** — a markdown file under `.tickets/` with YAML frontmatter.
- **Frontmatter** — the leading YAML block (`---` ... `---`).
- **Ticket ID** — the value of `id`; the canonical reference key.
- **Dependency** — a ticket this ticket needs completed first (it "depends on").
- **Terminal status** — a status from which no further work is expected
  (`done`, `cancelled`).
- **Finding** — a single rule violation, with rule ID, severity, file, and
  message.
- **Error** — a finding that makes the ticket set invalid (non-zero exit).
- **Warning** — a finding that is suspicious but non-fatal (zero exit unless
  `--strict`).

## 7. Interface & Behavior

### 7.1 Invocation

A single command/function, e.g.:

```
agents-tickets validate [PATH] [--json] [--strict] [--config FILE]
                        [--include-archive] [--quiet]
```

- `PATH` — directory to scan; default `.tickets/`.
- `--json` — emit machine-readable JSON instead of (or in addition to) text.
- `--strict` — treat warnings as errors (non-zero exit on any finding).
- `--config FILE` — path to schema/vocabulary config (statuses, required fields,
  ID pattern). Default: a checked-in config or sensible built-in defaults.
- `--include-archive` — include archived tickets in lifecycle checks.
- `--quiet` — suppress success output; only print findings.

The capability should also be importable as a function returning a structured
result, so other tooling/agents can call it without parsing stdout.

### 7.2 Processing pipeline

1. **Discover** ticket files: glob `*.md` under `PATH` (recursive),
   respecting archive inclusion rules. Non-`.md` files are ignored.
2. **Parse** each file: split frontmatter from body; parse YAML. A file with no
   frontmatter or invalid YAML produces a parse-level error and is skipped for
   semantic checks.
3. **Build an index**: map `id -> ticket` (detecting duplicates).
4. **Per-ticket checks**: required fields, types/formats, status enum, etc.
5. **Cross-ticket checks**: dependency existence, cycles, lifecycle consistency.
6. **Report**: aggregate findings, sort deterministically (by file, then rule
   ID), print, and set exit code.

### 7.3 Exit codes

- `0` — no errors (warnings allowed unless `--strict`).
- `1` — one or more errors (or warnings under `--strict`).
- `2` — tool/usage error (bad path, unreadable config, internal failure).

### 7.4 Output

**Human-readable (default):** grouped by file, each finding as
`SEVERITY [RULE-ID] file:loc — message`, ending with a summary line
(`N errors, M warnings across K tickets`).

**JSON (`--json`):** stable schema, e.g.:

```json
{
  "summary": {"tickets": 12, "errors": 2, "warnings": 1, "ok": false},
  "findings": [
    {
      "rule": "TV-301",
      "severity": "error",
      "id": "TICK-0007",
      "file": ".tickets/TICK-0007.md",
      "field": "dependencies",
      "message": "Dependency 'TICK-0099' does not exist."
    }
  ]
}
```

## 8. Validation Rule Catalog

Each rule has a stable ID, a default severity, and a clear message. Severities
are defaults and **must be configurable**.

### 8.1 Parsing & file structure

| Rule | Severity | Description |
|------|----------|-------------|
| TV-001 | error | File has no YAML frontmatter block. |
| TV-002 | error | Frontmatter is not valid YAML / cannot be parsed. |
| TV-003 | error | Frontmatter is not a mapping (e.g., a list or scalar). |
| TV-004 | warning | File `*.md` under `.tickets/` looks like a ticket but lacks an `id` (possible non-ticket doc). |

### 8.2 Required frontmatter (Goal G1)

| Rule | Severity | Description |
|------|----------|-------------|
| TV-101 | error | Missing required field (`id`, `title`, `status`, `created`). One finding per missing field. |
| TV-102 | error | Field has wrong type (e.g., `dependencies` not a list, `created` not a date). |
| TV-103 | error | `id` does not match the configured ID pattern. |
| TV-104 | error | `title` is empty or whitespace-only. |
| TV-105 | warning | Unknown/unexpected frontmatter key (typo guard; configurable allow-list). |
| TV-106 | warning | `created`/`updated` not in `YYYY-MM-DD` format. |
| TV-107 | warning | Filename does not correspond to `id` (e.g., `TICK-0007.md` vs `id: TICK-0008`). |

### 8.3 Allowed status & enum fields (Goal G2)

| Rule | Severity | Description |
|------|----------|-------------|
| TV-201 | error | `status` is not in the allowed set. |
| TV-202 | warning | `type` is not in the allowed set (if `type` is defined). |
| TV-203 | warning | `priority` is not in the allowed set (if defined). |
| TV-204 | warning | `status` differs only by case/whitespace/hyphenation from a valid value (likely typo; suggest the canonical value). |

### 8.4 Dependency references (Goal G3)

| Rule | Severity | Description |
|------|----------|-------------|
| TV-301 | error | Dependency references a ticket `id` that does not exist. |
| TV-302 | error | Duplicate ticket `id` across files (ambiguous reference target). |
| TV-303 | error | Ticket lists itself as a dependency. |
| TV-304 | error | Dependency cycle detected (report the cycle path). |
| TV-305 | warning | Duplicate entries within a ticket's `dependencies` list. |
| TV-306 | error | `epic`/`parent` references a non-existent ticket `id`. |
| TV-307 | warning | `epic`/`parent` target exists but is not of `type: epic` (if `type` is used). |

### 8.5 Lifecycle consistency (Goal G4)

| Rule | Severity | Description |
|------|----------|-------------|
| TV-401 | error | A ticket in a terminal status (`done`) depends on a non-terminal ticket (open dependency closed out of order). |
| TV-402 | warning | A ticket in `in-progress`/`in-review` has a dependency that is not yet `done` (started before prerequisites complete). |
| TV-403 | warning | A ticket marked `blocked` has no incomplete dependency and no explicit blocker note (blocked-without-reason). |
| TV-404 | warning | An `epic` is `done` while it has child tickets that are not terminal. |
| TV-405 | warning | An `epic` is `done`/`cancelled` but has zero child tickets (empty epic). |
| TV-406 | warning | `updated` date is earlier than `created` date. |
| TV-407 | warning | Terminal ticket (`done`) is missing an expected completion signal (e.g., no `updated` date), if convention requires one. |

> Rule severities and the exact lifecycle invariants (especially TV-401 vs
> TV-402) depend on the workspace's actual status semantics and must be confirmed
> (see Open Questions Q3–Q5).

## 9. Edge Cases

- **Empty `.tickets/`** or directory absent → not an error; report `0 tickets`,
  exit `0` (configurable: `--require-tickets` could make absence an error).
- **Non-ticket markdown** (e.g., `README.md`, templates) in `.tickets/` → ignored
  if no frontmatter / no `id`; TV-004 warning if ambiguous. Provide an
  ignore-glob config (e.g., ignore `_template.md`, `README.md`).
- **Archive subfolder** → parsed for existence (so dependencies on archived
  tickets resolve), but excluded from active lifecycle checks unless
  `--include-archive`.
- **Case sensitivity** of IDs → IDs compared case-sensitively by default; TV-204
  catches near-miss casing for statuses.
- **Large lists / many tickets** → linear-time index + DFS cycle detection;
  target sub-second for hundreds of tickets.
- **Duplicate IDs** → both files reported (TV-302); dependency resolution to a
  duplicated ID is itself an error to avoid silent wrong-target resolution.
- **Self-referential epic** (`parent == id`) → treated as TV-303-style error.
- **`dependencies: null`** vs missing → treated as empty list (no error).

## 10. Acceptance Criteria

The capability is accepted when, against a fixture set of crafted tickets:

- **AC1.** A fully valid ticket set produces `0 errors, 0 warnings` and exit `0`.
- **AC2.** Each rule TV-001…TV-407 has at least one fixture that triggers it and
  one that does not (positive/negative), and the validator's finding matches the
  expected rule ID, severity, and target file.
- **AC3.** Missing each required field independently yields a distinct TV-101
  finding naming that field.
- **AC4.** An invalid `status` yields TV-201; a near-miss (`In Progress`) yields
  TV-204 with a suggested canonical value.
- **AC5.** A dangling dependency yields TV-301; a 2-node and a 3-node cycle each
  yield TV-304 with the cycle path; a self-dependency yields TV-303.
- **AC6.** A `done` ticket depending on a `todo` ticket yields TV-401.
- **AC7.** `--json` output validates against the documented JSON schema and is
  byte-stable across runs on identical input (deterministic ordering).
- **AC8.** Exit codes follow §7.3, including `--strict` promoting warnings to
  error exit.
- **AC9.** Running on an empty/absent `.tickets/` exits `0` with a clear message.
- **AC10.** The tool is read-only: a checksum of every input file is unchanged
  after a run.
- **AC11.** All allowed values (statuses, required fields, ID pattern) are read
  from config; changing the config changes validation behavior without code
  edits.

## 11. Testing Strategy (high level)

- **Fixtures:** a `tests/fixtures/` tree with `valid/` and per-rule `invalid/`
  ticket sets; golden JSON outputs for snapshot comparison.
- **Unit tests:** parser (frontmatter extraction, malformed YAML), each rule
  check in isolation, cycle detection on hand-built graphs.
- **Integration tests:** run the CLI end-to-end against fixture dirs; assert exit
  codes and JSON.
- **Determinism test:** run twice, assert identical output.
- **Read-only test:** hash fixtures before/after (AC10).

## 12. Rollout / Future Work (out of scope for v1)

- Pre-commit hook and/or CI step that runs `validate --strict`.
- `--fix` autofix mode (normalize statuses, dedupe dependency lists).
- Integration with the ticket workflow tooling to validate on create/transition.
- Optional body checks (required sections, acceptance criteria present).
- Configurable per-status transition matrix enforcement.

## 13. Open Questions (must resolve before build)

See the companion file `notes-and-questions.md` for the full list with current
working assumptions. The highest-impact questions:

- **Q1.** What is the *authoritative* required-frontmatter schema and ID format?
- **Q2.** What is the exact allowed `status` vocabulary (and which are terminal)?
- **Q3.** Is "a `done` ticket depending on a non-`done` ticket" an error or a
  warning (TV-401 severity)?
- **Q4.** Do tickets use `epic`/`parent` hierarchy, and how is an epic's
  completion defined relative to its children (TV-404/405)?
- **Q5.** How are archived/cancelled tickets stored, and should they participate
  in dependency resolution and lifecycle checks?
- **Q6.** Preferred interface: standalone CLI, a script under the workspace, or a
  function callable by the agent workflow? Preferred language/deps?
