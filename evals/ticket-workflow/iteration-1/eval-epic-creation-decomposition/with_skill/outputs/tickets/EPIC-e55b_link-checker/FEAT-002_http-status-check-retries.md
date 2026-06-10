---
id: FEAT-002
title: "HTTP status checker with retries"
type: feature
status: to-do
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e55b
dependencies: []
tags: [linkcheck, http]
agent_created: true
complexity: 4
---

# HTTP status checker with retries

## Context

Second feature ticket for the linkcheck tool (parent: EPIC-e55b). Takes URLs (plain
strings — not `Link` objects; this ticket is independent of FEAT-001 and may execute
in parallel with it) and determines whether each is reachable. Defines the
`CheckResult` contract consumed by FEAT-003 (report) and FEAT-004 (CLI).

## Requirements

- [ ] Create package marker `linkcheck/__init__.py` (if absent) with exactly this content:
      `"""linkcheck: markdown link checker."""` plus a trailing newline. Nothing else.
- [ ] Create `linkcheck/check.py` defining the dataclass `CheckResult` with fields
      `url: str`, `ok: bool`, `status: int | None`, `attempts: int`, `error: str | None`.
- [ ] Implement `check_url(url, *, retries=2, timeout=5.0, ...) -> CheckResult` using
      stdlib `urllib.request` (GET): 2xx/3xx => ok; 4xx => broken, NO retry (deterministic);
      5xx and network errors (URLError/timeout/OSError) => retry up to `retries` extra
      attempts with exponential backoff, then broken.
- [ ] Make HTTP fetching and sleeping injectable (parameters with production defaults,
      e.g. a fetch callable and `sleep=time.sleep`) so tests run offline and without
      real delays; record the actual attempt count in `CheckResult.attempts`.
- [ ] Implement `check_urls(urls, *, retries=2, timeout=5.0) -> dict[str, CheckResult]`
      that deduplicates URLs (each distinct URL fetched once).

## File path hints

- `linkcheck/__init__.py` — create if absent (exact one-line content above)
- `linkcheck/check.py` — create
- `tests/test_check.py` — create (fake fetch/sleep; no sockets)

## Constraints

- Do NOT add third-party HTTP libraries (no requests/aiohttp/httpx) — stdlib `urllib` only.
- Do NOT add HEAD-request optimization, caching, or concurrency — out of scope.
- Do NOT perform real network I/O or real sleeps in tests.
- Do NOT touch files outside the hints above (plus this ticket file for status updates).
- Must preserve `CheckResult` field names exactly — downstream tickets import them.

## Acceptance criteria

- [ ] 2xx => `ok=True`; 4xx => `ok=False` with `attempts == 1` (no retry); 5xx/network
      error => retried, `ok=False` with `attempts == retries + 1` when all attempts fail.
- [ ] A URL that fails once with a 5xx then succeeds returns `ok=True, attempts == 2`,
      and the injected sleep was called with a positive backoff delay.
- [ ] `check_urls` fetches each distinct URL exactly once and keys results by URL.
- [ ] `python3 -m pytest tests/test_check.py -q` passes offline with no real sleeping.

## Verification

```bash
python3 -c "from linkcheck.check import CheckResult, check_url, check_urls; print('import ok')"
python3 -m pytest tests/test_check.py -q
```

## Notes

`scratch/local-notes.txt` floated aiohttp — rejected: epic constraint is stdlib-only.
Redirects: urllib follows them by default; the final status is what gets recorded.
