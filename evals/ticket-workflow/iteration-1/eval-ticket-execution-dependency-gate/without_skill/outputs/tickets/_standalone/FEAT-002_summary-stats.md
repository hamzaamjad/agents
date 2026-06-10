---
id: FEAT-002
title: Add per-column summary statistics
type: feature
status: blocked
priority: medium
created: 2026-06-08
updated: 2026-06-10
parent:
dependencies: [FEAT-001]
tags: [csv, stats]
agent_created: false
complexity:
---

# Add per-column summary statistics

## Blocked
2026-06-10: Blocked on FEAT-001, which is still `to-do` — `load_csv` does
not exist in `parser.py` yet, and this ticket's constraints require
consuming `load_csv` from FEAT-001 rather than re-reading files. Execute
FEAT-001 first, then this ticket can proceed.

## Context
Once files can be loaded (FEAT-001), users want quick per-column stats
for numeric columns.

## Requirements
- [ ] `summarize(path)` loads the file via `load_csv` and returns `{column: {"min": x, "max": y, "mean": z}}` for numeric columns
- [ ] Non-numeric columns are skipped
- [ ] Empty data files return `{}`

## File path hints
- `parser.py` — modify
- `test_parser.py` — modify

## Constraints
- Do NOT add third-party dependencies
- Must consume `load_csv` from FEAT-001 rather than re-reading files

## Acceptance criteria
- [ ] `summarize` returns min/max/mean per numeric column
- [ ] Non-numeric columns absent from the result
- [ ] All tests pass

## Verification
```bash
python3 test_parser.py
```
