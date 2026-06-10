---
id: FEAT-002
title: Add per-column summary statistics
type: feature
status: to-do
priority: medium
created: 2026-06-08
updated: 2026-06-08
parent:
dependencies: [FEAT-001]
tags: [csv, stats]
agent_created: false
complexity:
---

# Add per-column summary statistics

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
