---
id: FEAT-001
title: "Extract URLs from markdown files"
type: feature
status: to-do
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e55b
dependencies: []
tags: [linkcheck, parsing]
agent_created: true
complexity: 3
---

# Extract URLs from markdown files

## Context

First of four feature tickets for the linkcheck tool (parent: EPIC-e55b). The checker
(FEAT-002) and report (FEAT-003) consume the `Link` records this module produces. This
ticket defines that contract; downstream tickets import it, so field names below are
binding. May execute in parallel with FEAT-002 (no shared code besides the identical
`__init__.py`).

## Requirements

- [ ] Create package marker `linkcheck/__init__.py` (if absent) with exactly this content:
      `"""linkcheck: markdown link checker."""` plus a trailing newline. Nothing else.
- [ ] Create `linkcheck/extract.py` defining the dataclass `Link` with fields
      `url: str`, `source_file: str`, `line: int` (1-based line number).
- [ ] Implement `extract_urls(text: str, source_file: str) -> list[Link]` that finds
      http/https URLs in: inline links `[text](url)` (with optional `"title"`),
      autolinks `<https://example.com>`, and reference definitions `[label]: url`.
- [ ] Exclude non-http(s) targets (mailto:, relative paths, `#anchors`) and anything
      inside fenced code blocks (``` or ~~~ fences).
- [ ] Keep duplicates: one `Link` per occurrence — deduplication happens in FEAT-002.

## File path hints

- `linkcheck/__init__.py` — create if absent (exact one-line content above)
- `linkcheck/extract.py` — create
- `tests/test_extract.py` — create (stdlib + pytest only)

## Constraints

- Do NOT attempt full CommonMark parsing or add a markdown dependency — targeted
  regex/line-scan over the constructs listed above is the intended scope.
- Do NOT do any file I/O in `extract.py` — it operates on text passed in; file
  discovery and reading belong to the CLI (FEAT-004).
- Do NOT touch files outside the hints above (plus this ticket file for status updates).
- Must preserve the `Link` field names exactly as specified — downstream tickets import them.

## Acceptance criteria

- [ ] `extract_urls` returns correct `(url, source_file, line)` for inline links,
      autolinks, and reference definitions in a multi-line sample document.
- [ ] mailto/relative/anchor links and URLs inside fenced code blocks are excluded.
- [ ] Duplicate URLs on different lines yield separate `Link` entries.
- [ ] `python3 -m pytest tests/test_extract.py -q` passes with no network access.

## Verification

```bash
python3 -c "from linkcheck.extract import Link, extract_urls; print('import ok')"
python3 -m pytest tests/test_extract.py -q
```

## Notes

Contract consumers: FEAT-003 reads `Link.source_file`/`Link.line` for the report;
FEAT-004 feeds file contents in. Parent epic pins the full data contract.
