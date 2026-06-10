---
id: FEAT-001
title: Add CSV file loader
type: feature
status: to-do
priority: medium
created: 2026-06-08
updated: 2026-06-08
parent:
dependencies: []
tags: [csv, io]
agent_created: false
complexity:
---

# Add CSV file loader

## Context
csvtool can parse single rows but cannot read files yet. A loader is the
foundation for every downstream feature.

## Requirements
- [ ] `load_csv(path)` returns `(header, rows)` using `parse_row` per line
- [ ] Blank lines are skipped
- [ ] Missing files raise `FileNotFoundError` naturally

## File path hints
- `parser.py` — modify
- `test_parser.py` — modify

## Constraints
- Do NOT add third-party dependencies
- Must reuse `parse_row` for each line

## Acceptance criteria
- [ ] `load_csv` returns the header row separately from data rows
- [ ] Blank lines produce no data rows
- [ ] All tests pass

## Verification
```bash
python3 test_parser.py
```
