---
id: EPIC-e55b
title: "linkcheck: markdown link checker (extract, check, report, CI)"
type: epic
status: to-do
priority: high
branch: epic/e55b/link-checker
created: 2026-06-10
updated: 2026-06-10
tags: [linkcheck, cli, python]
agent_created: true
complexity: 6
---

# linkcheck: markdown link checker (extract, check, report, CI)

## Context

The repository contains a stub CLI (`linkcheck.py` prints a placeholder) and a README
that promises a working tool: scan markdown files for links and report which ones are
broken. This epic delivers that tool in four sub-tickets plus a closure ticket.

Target layout (final state on this epic branch):

```
linkcheck/__init__.py      docstring-only package marker (FEAT-001/FEAT-002, identical content)
linkcheck/extract.py       URL extraction from markdown        (FEAT-001)
linkcheck/check.py         HTTP status checking with retries   (FEAT-002)
linkcheck/report.py        markdown report rendering           (FEAT-003)
linkcheck/cli.py           argparse CLI, exit codes            (FEAT-004)
linkcheck/__main__.py      `python3 -m linkcheck` entry        (FEAT-004)
tests/test_*.py            one test module per feature ticket
.github/workflows/linkcheck.yml  CI: pytest + offline smoke run (FEAT-004)
```

The root stub `linkcheck.py` is deleted by FEAT-004 (replaced by the package entry
point). Until then the package `linkcheck/` shadows the stub for imports; this is a
known, transient state.

Shared data contract (pinned here so parallel agents converge):

- `linkcheck.extract.Link` dataclass: `url: str`, `source_file: str`, `line: int` (1-based).
- `linkcheck.check.CheckResult` dataclass: `url: str`, `ok: bool`, `status: int | None`,
  `attempts: int`, `error: str | None`.
- `extract_urls(text: str, source_file: str) -> list[Link]`
- `check_url(url, *, retries=2, timeout=5.0, ...) -> CheckResult`,
  `check_urls(urls, *, retries=2, timeout=5.0) -> dict[str, CheckResult]`
- `render_report(items: Sequence[tuple[Link, CheckResult]]) -> str`,
  `write_report(path, items) -> None`
- CLI exit codes: 0 = all links ok, 1 = broken links found, 2 = usage/input error.

Epic-level constraints:

- Standard library only at runtime (`urllib`, `re`, `dataclasses`, `argparse`); pytest
  is the only test dependency. Python >= 3.10 syntax allowed (environment is 3.13).
- No real network I/O in any test; HTTP fetching must be injectable/fakeable.
- Never modify or commit `scratch/` or `.env.local`; never commit `.claude/worktrees/`.
- All work happens on ticket branches off `epic/e55b/link-checker`; never on main.

Archive note: `.tickets/_archive/` does not exist yet (this is the repo's first epic),
so no prior Outcome blocks were available to mine for context.

## Sub-tickets

| ID        | Title                                          | Status |
|-----------|------------------------------------------------|--------|
| FEAT-001  | Extract URLs from markdown files               | to-do  |
| FEAT-002  | HTTP status checker with retries               | to-do  |
| FEAT-003  | Markdown report generation                     | to-do  |
| FEAT-004  | CLI entry point, tests wiring, CI workflow     | to-do  |
| CHORE-001 | Epic closure: archive epic, clean up artifacts | to-do  |

## Merge order

1. FEAT-001 (no dependencies; defines the `Link` contract. May EXECUTE in parallel with FEAT-002.)
2. FEAT-002 (no dependencies; defines the `CheckResult` contract. Parallel worktree OK; merges
   second. Both FEAT-001 and FEAT-002 create the identical one-line `linkcheck/__init__.py`,
   so the rebase at merge time is trivial.)
3. FEAT-003 (depends on FEAT-001 + FEAT-002 — consumes both dataclasses; merge sequentially after both.)
4. FEAT-004 (depends on FEAT-001..003 — wires all modules into the CLI and CI; deletes the root stub.)
5. CHORE-001 — Epic closure (always last: marks tickets done, archives the epic folder,
   deletes the orchestration prompt, cleans up worktree artifacts. See SKILL.md "Epic Closure Ticket".)

## Acceptance criteria

- [ ] All sub-tickets are `done`
- [ ] `python3 -m pytest tests/ -q` passes on the epic branch (tests exist for extract, check, report, cli)
- [ ] `python3 -m linkcheck README.md` exits 0 from the repo root on the epic branch (offline smoke; README currently has no external links)
- [ ] Epic archived to `.tickets/_archive/` and orchestration prompt deleted (by CHORE-001)
- [ ] Epic branch merged back to main (local merge — this repo has no remote, so no PR)

## Notes

- Orchestration brief: `.prompts/orchestration/epic-e55b_link-checker.md` (instance of the
  canonical orchestration template; defines per-ticket review packets).
- Sub-ticket worktrees: `.claude/worktrees/epic-e55b/<TICKET-ID>` on branches
  `epic-e55b/<TICKET-ID>/<slug>`, branched from `epic/e55b/link-checker`.
- `scratch/local-notes.txt` mentions "aiohttp vs urllib" — resolved: urllib (stdlib-only constraint).
