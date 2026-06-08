# Notes, Clarifying Questions & Working Assumptions

Companion to `SPEC-ticket-validation-2026-06-05.md`.

This task was executed **non-interactively** and as a **baseline without any
specialized spec-writing skill**. Per the task constraints, no files under
`skills/` were read — including the workspace's own ticket-workflow conventions —
so the canonical ticket schema/vocabulary is **assumed** here and flagged for
confirmation. Everything below records what I would have asked a human/maintainer,
the assumption I proceeded with, and how the spec is built to absorb the real
answer cheaply (config-driven, not hard-coded).

## How workspace context was gathered (read-only)

- `ls` of workspace root: only `skills/`, `.git`, `.gitignore`, `.DS_Store`.
- `.tickets/` directory **does not currently exist** on disk.
- `.gitignore` review (non-skill file):
  - `.tickets/` is listed as a *per-workspace agent workflow artifact* (tracked
    convention, gitignored) → confirms `.tickets/` is the right target path.
  - Entries for `ruff`, `mypy`, `pytest`, `.venv`, `__pycache__` → workspace uses
    a **Python** toolchain → validator likely Python (assumption A6).
  - `.prompts/` and `.claude/worktrees/` are also per-workspace artifacts.
- Deliberately **not** read: anything under `skills/` (ticket-workflow templates,
  defining-specifications, etc.), and prior-iteration eval outputs (to keep this
  baseline independent).

## Clarifying questions (with working assumptions)

| # | Question | Working assumption used in spec |
|---|----------|---------------------------------|
| Q1 | Authoritative required-frontmatter keys + types? | `id`, `title`, `status`, `created` required; `dependencies`, `type`, `priority`, `epic`/`parent`, `owner`, `updated` optional (A3). |
| Q2 | Exact allowed `status` vocabulary; which are terminal? | `backlog`, `todo`, `in-progress`, `blocked`, `in-review`, `done`, `cancelled`; terminal = `done`, `cancelled` (A4). |
| Q3 | ID format / pattern? | `^[A-Z]+-\d+$` (e.g., `TICK-0007`); IDs globally unique (A3). |
| Q4 | One file per ticket? Filename ↔ id relationship? | One `.md` per ticket; filename should match `id` (warning TV-107 if not) (A1). |
| Q5 | Are dependencies referenced by `id` or by filename/path? | By `id` (A5). |
| Q6 | Lifecycle invariant strictness: is "`done` depends on non-`done`" an error or warning? | Error (TV-401); "started before prereqs done" is a warning (TV-402). |
| Q7 | Epic/parent hierarchy used? How is epic completion defined? | `epic`/`parent` optional; epic `done` with non-terminal children = warning (TV-404) (A3). |
| Q8 | How/where are archived & cancelled tickets stored? Do they participate in checks? | Possible `archive/` subfolder; parsed for dependency resolution, excluded from active lifecycle checks unless `--include-archive` (A7). |
| Q9 | Preferred interface (CLI vs callable vs hook) and dependency budget? | CLI + importable function; Python stdlib + a YAML parser; no heavy deps (A6). |
| Q10 | Should unknown frontmatter keys be an error or warning? | Warning (TV-105), configurable allow-list (typo guard). |
| Q11 | Should absence of `.tickets/` fail? | No by default; `--require-tickets` optional. |
| Q12 | Are warnings allowed to pass CI, or must everything be clean? | Warnings pass by default; `--strict` promotes to failure. |
| Q13 | Date format and timezone expectations for `created`/`updated`? | `YYYY-MM-DD`; `updated >= created` (TV-406). |
| Q14 | Are there non-ticket markdown files in `.tickets/` (templates, README)? | Yes likely; ignored via ignore-glob; ambiguous ones → TV-004 warning. |

## Key design decisions & rationale

- **Config-driven vocabulary.** Because the real schema is unknown, statuses /
  required fields / ID pattern / severities live in config. Confirming Q1–Q3 is a
  config edit, not a rewrite. This is the single most important hedge against the
  unread skill conventions.
- **Stable rule IDs (TV-xxx) + severities.** Enables machine-readable reports,
  per-rule fixtures, and selective enabling/severity overrides.
- **Errors vs warnings split.** Keeps the validator adoptable: structural defects
  fail; stylistic/lifecycle smells warn until the team opts into `--strict`.
- **Read-only, deterministic.** Required for safe use inside agent loops and for
  snapshot testing (AC7, AC10).
- **Dependency graph checks via DFS.** Existence + self-dep + cycle detection in
  linear time; cycle path reported for debuggability.

## Risks / things to revisit after Q&A

- If tickets use a different reference mechanism (e.g., relative file links rather
  than `id`), the dependency rules (TV-301…307) need re-targeting.
- If a formal status-transition matrix exists, lifecycle checks (§8.5) should be
  generated from it rather than from the ad-hoc invariants assumed here.
- If multiple tickets per file or nested ticket lists are allowed, the parser and
  index model (§7.2) change materially.
- Confirm whether epics are a `type` value, a separate directory, or a separate
  file convention — affects TV-306/307/404/405.
```
