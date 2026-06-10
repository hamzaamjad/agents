---
id: FEAT-003
title: "Markdown report generation"
type: feature
status: to-do
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e55b
dependencies: [FEAT-001, FEAT-002]
tags: [linkcheck, reporting]
agent_created: true
complexity: 3
---

# Markdown report generation

## Context

Third feature ticket for the linkcheck tool (parent: EPIC-e55b). Renders the outcome
of a link-check run as a markdown document. Consumes `Link` (FEAT-001) and
`CheckResult` (FEAT-002) — both dependencies must be `done` and merged to the epic
branch before this ticket starts.

## Requirements

- [ ] Create `linkcheck/report.py` implementing
      `render_report(items: Sequence[tuple[Link, CheckResult]]) -> str`.
- [ ] Report contains: an H1 title, a summary section with total links checked,
      OK count, and broken count, and — only when failures exist — a
      `## Broken links` table with columns File | Line | URL | Status/Error.
- [ ] When every link is ok (or `items` is empty), state that no broken links were
      found and emit no empty table.
- [ ] Output is deterministic: broken rows sorted by `(source_file, line, url)`;
      identical input always produces an identical string ending in one trailing newline.
- [ ] Implement `write_report(path, items) -> None` that writes `render_report` output
      to `path` (UTF-8, parent directory assumed to exist).

## File path hints

- `linkcheck/report.py` — create
- `tests/test_report.py` — create (build `Link`/`CheckResult` fixtures inline)

## Constraints

- Do NOT add HTML output, templating libraries, or color/emoji decoration — plain
  markdown text only.
- Do NOT recompute or re-check anything — this module formats results it is given.
- Do NOT touch files outside the hints above (plus this ticket file for status updates).
- Must import `Link` and `CheckResult` from `linkcheck.extract` / `linkcheck.check` —
  no local redefinitions.

## Acceptance criteria

- [ ] Mixed input (some broken, some ok) renders summary counts and a broken-links
      table with correct file/line/url and status (or error text when status is None).
- [ ] All-ok input renders a "no broken links" report with no table.
- [ ] Two calls with the same shuffled input produce byte-identical output (ordering
      is enforced by the sort).
- [ ] `python3 -m pytest tests/test_report.py -q` passes.

## Verification

```bash
python3 -c "from linkcheck.report import render_report, write_report; print('import ok')"
python3 -m pytest tests/test_report.py -q
```

## Notes

FEAT-004 wires `--report PATH` to `write_report`. Exit-code decisions live in the CLI,
not here.
