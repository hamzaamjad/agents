---
id: FEAT-003
title: Markdown report generator
type: feature
epic: EPIC-001
status: todo
owner: unassigned
depends_on: [FEAT-001, FEAT-002]
blocks: [FEAT-004]
files:
  - linkcheck/report.py
  - tests/test_report.py
created: 2026-06-10
---

# FEAT-003: Markdown report generator

## Summary

Create `linkcheck/report.py`: render extraction + check results into a
deterministic markdown report. Pure functions of their inputs — no network,
no clock, no CLI. Consumes `Link` from `linkcheck.extract` and `CheckResult`
from `linkcheck.check`.

## Interface (binding, from EPIC-001)

```python
def render_report(links: Sequence[Link], results: Mapping[str, CheckResult]) -> str: ...
def write_report(path: str | os.PathLike, links, results) -> None: ...
```

## Requirements

- Report structure, in order:
  - `# Link check report` heading
  - summary block: total link occurrences, unique URLs, OK count, broken
    count (a URL is broken when its `CheckResult.ok` is false)
  - `## Broken links` — table with columns URL | status/error | occurrences;
    occurrences rendered as comma-separated `source_file:line`, sorted by
    (file, line); when nothing is broken, render the line `_No broken links._`
    instead of a table
  - `## Checked URLs` — table of every unique URL with its final status
    (the integer, or the error text when status is `None`)
- Deterministic: tables sorted by URL; no timestamps, hostnames, or other
  run-dependent content; same inputs produce byte-identical output.
- Escape `|` characters in URLs and error text when rendering table cells.
- `write_report` writes UTF-8 and ends the file with a single trailing newline.
- Standard library only.

## Acceptance criteria

- [ ] Unit tests in `tests/test_report.py` (stdlib `unittest`) cover:
      a mixed report (ok + 404 + network-error URLs, one URL referenced from
      two files) compared against an expected golden string; the empty-input
      report (zero links) renders the heading, zero counts, and
      `_No broken links._`; pipe-escaping in a URL
- [ ] `render_report` calls produce identical output across two invocations
      with the same inputs (covered by a test)
- [ ] No files modified outside this ticket's `files:` list
- [ ] Verification passes

## Verification

```
python -m unittest tests.test_report -v
```
