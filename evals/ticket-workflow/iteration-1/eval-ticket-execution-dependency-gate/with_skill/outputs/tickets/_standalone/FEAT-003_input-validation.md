---
id: FEAT-003
title: Validate row field counts
type: feature
status: done
priority: medium
created: 2026-06-08
updated: 2026-06-10
parent:
dependencies: []
tags: [csv, validation]
agent_created: false
complexity: 3
---

# Validate row field counts

## Context
Malformed CSV rows (wrong number of fields) currently pass through
silently and corrupt downstream processing. Parsing should be able to
reject them early.

## Requirements
- [x] Add `validate_row(fields, expected_count)` to `parser.py`: raises `ValueError` naming the actual and expected counts when they differ, returns the fields unchanged otherwise
- [x] `parse_row` accepts an optional `expected_count=None` argument; when provided, the parsed fields are validated before being returned
- [x] Add tests covering the mismatch error and the happy path

## File path hints
- `parser.py` — modify
- `test_parser.py` — modify

## Constraints
- Do NOT break existing callers: `parse_row(line)` with one argument must keep working unchanged
- Do NOT add third-party dependencies

## Acceptance criteria
- [x] `validate_row(["a", "b"], 3)` raises `ValueError`; the message includes both counts
- [x] `parse_row("a,b", expected_count=2)` returns `["a", "b"]`; `parse_row("a,b", expected_count=3)` raises `ValueError`
- [x] All tests pass

## Verification
```bash
python3 test_parser.py
```

## Verification log
- 2026-06-10: `python3 test_parser.py` → `Ran 6 tests ... OK` (exit 0; 4 new tests covering mismatch and happy path). Predicted complexity: 3 (rubric weighted score 2.45, rounded up); actual meaningful tool rounds: ~8.

## Outcome

**Summary:** `parser.py` can now enforce an expected field count when parsing CSV rows. New `validate_row(fields, expected_count)` raises `ValueError` naming both the actual and expected counts on mismatch, and returns the fields unchanged otherwise; `parse_row(line, expected_count=...)` validates parsed fields before returning them. One-argument `parse_row(line)` behavior is unchanged, so existing callers are unaffected.

**Key decisions:**
- Validation is a standalone `validate_row` rather than inline in `parse_row` — downstream loaders (FEAT-001/FEAT-002) can validate pre-parsed field lists directly.
- `expected_count` defaults to `None` (opt-in) — preserves the one-argument contract required by the ticket's compatibility constraint.

**Constraints & invariants discovered (keep):**
- `parse_row(line)` with one argument must keep working unchanged.
- The mismatch `ValueError` message must name both the actual and the expected count.

**Implementation notes (high signal only):**
- Touch points: `parser.py` (`validate_row`, `parse_row`), `test_parser.py` (`TestParseRow`, `TestValidateRow`)
- Pattern: opt-in validation via an optional keyword argument delegating to a pure checker function.

**Verification:**
- `python3 test_parser.py` → `Ran 6 tests ... OK`; includes mismatch and happy-path coverage for both functions.

**Risk / regression surface:**
- A caller passing a second positional argument to `parse_row` now opts into validation; no such callers exist in-repo.

**Retrieval tags:** csv, csvtool, validation, parse_row, validate_row, expected_count, ValueError, field-count mismatch
