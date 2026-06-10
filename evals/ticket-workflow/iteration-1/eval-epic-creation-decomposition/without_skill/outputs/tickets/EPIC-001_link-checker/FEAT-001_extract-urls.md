---
id: FEAT-001
title: Extract URLs from markdown files
type: feature
epic: EPIC-001
status: todo
owner: unassigned
depends_on: []
blocks: [FEAT-003, FEAT-004]
files:
  - linkcheck/__init__.py
  - linkcheck/extract.py
  - tests/test_extract.py
created: 2026-06-10
---

# FEAT-001: Extract URLs from markdown files

## Summary

Create `linkcheck/extract.py`: pure functions that find http(s) URLs in
markdown text, single files, and directory trees, returning `Link` records
(`url`, `source_file`, `line`). No network access, no CLI, no printing.

## Interface (binding, from EPIC-001)

```python
@dataclass(frozen=True)
class Link:
    url: str          # absolute http/https URL as written in the file
    source_file: str  # path the link was found in
    line: int         # 1-based line number

def extract_links(text: str, source_file: str = "<string>") -> list[Link]: ...
def extract_links_from_file(path: str | os.PathLike) -> list[Link]: ...
def find_markdown_files(root: str | os.PathLike) -> list[pathlib.Path]: ...
```

## Requirements

- Recognize, with correct 1-based line numbers:
  - inline links `[text](https://example.com)`, including optional titles
    `[t](https://example.com "title")`
  - autolinks `<https://example.com>`
  - reference definitions `[label]: https://example.com`
  - bare URLs `https://example.com` in plain text
- Only `http://` and `https://` schemes; ignore `mailto:`, relative paths,
  and in-page anchors.
- Ignore URLs inside fenced code blocks (``` ... ```) and inline code spans.
- Strip trailing punctuation `).,;:!?` from bare URLs.
- Keep every occurrence in document order; do not deduplicate (dedup happens
  at the check stage).
- `find_markdown_files`: recursive `*.md` under `root`, sorted, skipping
  dot-directories such as `.git`.
- `extract_links_from_file`: read UTF-8 with `errors="replace"`.
- Standard library only (`re`, `pathlib`, `dataclasses`).
- Create `linkcheck/__init__.py` as an empty file if it does not exist yet;
  never put code in it.

## Acceptance criteria

- [ ] Every Requirements bullet is demonstrated by a unit test in
      `tests/test_extract.py` (stdlib `unittest`)
- [ ] Edge cases covered: two links on one line; URL with query string;
      link inside emphasis (`**[t](u)**`); URL inside a code fence is
      ignored; reference definition with leading whitespace
- [ ] No files modified outside this ticket's `files:` list
- [ ] Verification passes

## Verification

```
python -m unittest tests.test_extract -v
```
