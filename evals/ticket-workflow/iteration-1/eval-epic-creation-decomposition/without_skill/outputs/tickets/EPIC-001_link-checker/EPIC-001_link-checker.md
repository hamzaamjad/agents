---
id: EPIC-001
title: "Link checker: extract, check, report, CI"
type: epic
status: todo
owner: unassigned
created: 2026-06-10
sub_tickets: [FEAT-001, FEAT-002, FEAT-003, FEAT-004]
---

# EPIC-001: Link checker — extract, check, report, CI

## Goal

Turn the `linkcheck.py` stub into a working CLI tool that scans markdown
files for links, checks each URL's HTTP status with retries, writes a
markdown report of the results, and runs as a CI entry point with tests.

## Out of scope

- Non-HTTP(S) link types (`mailto:`, `ftp:`, relative paths, in-page anchors)
- Concurrent/async checking (single-threaded is acceptable)
- Third-party dependencies (standard library only)
- Packaging/publishing (no `pyproject.toml`)

## Target architecture

All tool code lives in a new `linkcheck/` package; the root `linkcheck.py`
becomes a thin shim in FEAT-004.

| Path | Contents | Owner |
|---|---|---|
| `linkcheck/__init__.py` | empty package marker | any wave-1 ticket (must stay empty) |
| `linkcheck/extract.py` | `Link`, URL extraction from markdown | FEAT-001 |
| `linkcheck/check.py` | `CheckResult`, HTTP checks with retries | FEAT-002 |
| `linkcheck/report.py` | markdown report rendering | FEAT-003 |
| `linkcheck/cli.py`, `linkcheck/__main__.py` | arg parsing, wiring, exit codes | FEAT-004 |
| `linkcheck.py` (root) | shim delegating to `linkcheck.cli.main()` | FEAT-004 |
| `tests/test_*.py` | `unittest` suite per module | each ticket |
| `.github/workflows/linkcheck.yml` | CI: tests + CLI smoke run | FEAT-004 |

## Shared contracts (binding)

Sub-tickets implement exactly these interfaces. Changing a contract requires
updating this epic and every affected ticket first, in its own commit.

```python
# linkcheck/extract.py (FEAT-001)
@dataclass(frozen=True)
class Link:
    url: str          # absolute http/https URL as written in the file
    source_file: str  # path the link was found in
    line: int         # 1-based line number

def extract_links(text: str, source_file: str = "<string>") -> list[Link]: ...
def extract_links_from_file(path: str | os.PathLike) -> list[Link]: ...
def find_markdown_files(root: str | os.PathLike) -> list[pathlib.Path]: ...

# linkcheck/check.py (FEAT-002)
DEFAULT_USER_AGENT = "linkcheck/0.1"

@dataclass(frozen=True)
class CheckResult:
    url: str
    ok: bool            # True when the final HTTP status is 200-399
    status: int | None  # final HTTP status, None when no response was obtained
    error: str | None   # failure description when status is None
    attempts: int       # attempts actually made (1 = succeeded first try)

def check_url(url: str, *, timeout: float = 10.0, retries: int = 2,
              backoff: float = 0.5, user_agent: str = DEFAULT_USER_AGENT,
              transport=None, sleep=time.sleep) -> CheckResult: ...
def check_urls(urls: Iterable[str], *, ...same keywords...) -> dict[str, CheckResult]: ...

# linkcheck/report.py (FEAT-003)
def render_report(links: Sequence[Link], results: Mapping[str, CheckResult]) -> str: ...
def write_report(path: str | os.PathLike, links, results) -> None: ...

# linkcheck/cli.py (FEAT-004)
def main(argv: list[str] | None = None, *, transport=None) -> int: ...
```

## Constraints

- Python 3.10+, standard library only (`re`, `urllib`, `argparse`, `unittest`, ...).
- Tests never touch the network: `check.py` takes an injectable `transport`
  callable and an injectable `sleep`.
- Deterministic output: stable ordering everywhere, no timestamps in reports.

## Sub-tickets and dependencies

| ID | Title | Depends on | Wave |
|---|---|---|---|
| FEAT-001 | Extract URLs from markdown files | — | 1 |
| FEAT-002 | HTTP status checker with retries | — | 1 |
| FEAT-003 | Markdown report generator | FEAT-001, FEAT-002 | 2 |
| FEAT-004 | CLI entry point, CI workflow, test wiring | FEAT-001, FEAT-002, FEAT-003 | 3 |

```
FEAT-001 ─┬─→ FEAT-003 ──→ FEAT-004
FEAT-002 ─┘                (FEAT-001/002 are also direct inputs to FEAT-004)
```

## Orchestration rules (multi-agent)

1. Claim a ticket by setting its `status: in-progress` and `owner: <agent-id>`.
2. Start a ticket only when every ticket in its `depends_on` is `status: done`.
3. Wave 1 (FEAT-001, FEAT-002) may run in parallel: their file sets are
   disjoint, and `linkcheck/__init__.py` must stay empty so concurrent
   creation cannot conflict.
4. Touch only the files listed in your ticket's `files:` header.
5. Run your ticket's Verification commands; when green, set `status: done`
   and append a dated completion note at the bottom of the ticket.
6. One commit per ticket, message prefixed with the ticket ID.
7. Statuses: `todo` → `in-progress` → `done`, with `blocked` when a
   dependency or contract problem is found (note the reason in the ticket).

## Definition of done

- [ ] All four sub-tickets are `status: done`
- [ ] `python -m unittest discover -s tests -v` passes
- [ ] `python -m linkcheck README.md --report /tmp/linkcheck-report.md` exits 0
- [ ] CI workflow runs the test suite and a network-free CLI smoke run
- [ ] README describes real usage; stub wording removed
