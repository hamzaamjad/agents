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
complexity:
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
