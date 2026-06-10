---
id: FEAT-004
title: CLI entry point, CI workflow, test wiring
type: feature
epic: EPIC-001
status: todo
owner: unassigned
depends_on: [FEAT-001, FEAT-002, FEAT-003]
blocks: []
files:
  - linkcheck/cli.py
  - linkcheck/__main__.py
  - linkcheck.py
  - tests/test_cli.py
  - .github/workflows/linkcheck.yml
  - .gitignore
  - README.md
created: 2026-06-10
---

# FEAT-004: CLI entry point, CI workflow, test wiring

## Summary

Wire extraction → checking → reporting into a CLI with meaningful exit
codes, make both `python -m linkcheck` and the root `linkcheck.py` shim
work, add an end-to-end test, and add the CI workflow that runs the whole
suite plus a network-free smoke run.

## Interface (binding, from EPIC-001)

```python
# linkcheck/cli.py
def main(argv: list[str] | None = None, *, transport=None) -> int: ...
```

`transport` is passed through to `linkcheck.check.check_urls` so the
integration test can run without network access.

## Requirements

- Arguments:
  - positional `paths` (one or more): markdown files, or directories
    expanded via `find_markdown_files`
  - `--report PATH` (default `linkcheck-report.md`)
  - `--timeout FLOAT` (default 10.0), `--retries INT` (default 2),
    `--user-agent STR`
  - `--no-fail-on-broken`: exit 0 even when broken links are found
- Environment overrides, applied only when the flag is not given:
  `LINKCHECK_TIMEOUT`, `LINKCHECK_USER_AGENT`.
- Behavior: extract links from all inputs, check unique URLs, write the
  report to `--report`, print a one-line summary to stdout.
- Exit codes: `0` all links ok or no links found; `1` broken links found
  (suppressed by `--no-fail-on-broken`); `2` usage error or unreadable path.
- `linkcheck/__main__.py` delegates to `cli.main()`; the root `linkcheck.py`
  stub body is replaced by a thin shim calling `linkcheck.cli.main()` so both
  invocations behave identically.
- `tests/test_cli.py`: build a temp directory of markdown files, run
  `main()` with a fake transport, assert exit codes (0, 1, and 2 paths),
  the stdout summary, and the written report content.
- CI workflow `.github/workflows/linkcheck.yml`:
  - triggers: `push` and `pull_request`
  - steps: checkout, set up Python 3.x,
    `python -m unittest discover -s tests -v`,
    then smoke run `python -m linkcheck README.md --report /tmp/report.md`
  - the smoke run must stay network-free: keep any example URLs in README
    inside code fences (the extractor ignores those)
- Add `linkcheck-report.md` to `.gitignore`.
- README: replace stub wording with real usage (flags, exit codes, CI note).

## Acceptance criteria

- [ ] `python -m unittest discover -s tests -v` passes (full suite, all tickets)
- [ ] `python -m linkcheck README.md --report /tmp/report.md` exits 0 and
      writes a report
- [ ] `python linkcheck.py README.md --report /tmp/report2.md` behaves
      identically to the module invocation
- [ ] Exit codes 0, 1, and 2 each covered by `tests/test_cli.py`
- [ ] No files modified outside this ticket's `files:` list
- [ ] Verification passes

## Verification

```
python -m unittest discover -s tests -v
python -m linkcheck README.md --report /tmp/report.md && echo "exit 0 ok"
```
