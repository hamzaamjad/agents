---
id: FEAT-002
title: HTTP status checker with retries
type: feature
epic: EPIC-001
status: todo
owner: unassigned
depends_on: []
blocks: [FEAT-003, FEAT-004]
files:
  - linkcheck/__init__.py
  - linkcheck/check.py
  - tests/test_check.py
created: 2026-06-10
---

# FEAT-002: HTTP status checker with retries

## Summary

Create `linkcheck/check.py`: check a URL's HTTP status with bounded retries
and exponential backoff, returning `CheckResult` records. The network layer
is an injectable `transport` callable so unit tests never touch the network.
No CLI, no printing.

## Interface (binding, from EPIC-001)

```python
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
```

## Requirements

- `transport` is a callable `(url: str, timeout: float, user_agent: str) -> int`
  that returns the final HTTP status after following redirects, or raises
  `OSError` on network failure. When `transport=None`, use the default
  urllib-based transport.
- Default transport: `urllib.request`, HEAD request first, falling back to
  GET when HEAD returns 405 or 501; follows redirects; sends `user_agent`;
  an `HTTPError` code is a valid status result, not an exception.
- Classification: `ok` is true for final status 200-399; 4xx and 5xx are
  not ok; when all attempts raise, `status=None`, `ok=False`, and `error`
  holds a short description of the last failure.
- Retry policy: retry on network errors (`OSError`) and on 5xx statuses;
  never retry 4xx. `retries` is the number of additional attempts after the
  first (default 2, so at most 3 attempts). Sleep `backoff * 2**i` seconds
  before retry `i` (0-based) using the injectable `sleep`.
- `check_urls`: deduplicates while preserving first-seen order; returns
  `dict[str, CheckResult]` keyed by URL.
- Standard library only (`urllib`, `time`, `dataclasses`).
- Create `linkcheck/__init__.py` as an empty file if it does not exist yet;
  never put code in it.

## Acceptance criteria

- [ ] Unit tests in `tests/test_check.py` (stdlib `unittest`, fake transport
      and fake sleep) cover: success on first try (attempts=1); 404 returns
      immediately with no retry; 503 then 200 succeeds with attempts=2;
      persistent network error exhausts retries (attempts=3, ok=False,
      status=None, error set); backoff sequence received by the fake sleep
      is `[0.5, 1.0]` for defaults; `check_urls` dedup and ordering
- [ ] No real network access anywhere in the tests
- [ ] No files modified outside this ticket's `files:` list
- [ ] Verification passes

## Verification

```
python -m unittest tests.test_check -v
```
