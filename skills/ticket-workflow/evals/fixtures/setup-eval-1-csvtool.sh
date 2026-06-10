#!/usr/bin/env bash
# Fixture builder for ticket-workflow eval 1 (ticket-execution-dependency-gate).
# Builds a minimal "csvtool" repo with three prepared tickets:
#   FEAT-001 (to-do, unassigned)            - the unmet dependency
#   FEAT-002 (to-do, depends on FEAT-001)   - assigned; must hard-stop
#   FEAT-003 (to-do, no dependencies)       - assigned; the executable path (2 files)
# Usage: setup-eval-1-csvtool.sh <target-dir>
set -euo pipefail

TARGET="${1:?usage: $0 <target-dir>}"
mkdir -p "$TARGET"
cd "$TARGET"

git init -q -b main
git config user.name "Eval Fixture"
git config user.email "fixture@example.invalid"

cat > parser.py <<'EOF'
"""csvtool: minimal CSV row parsing helpers."""

DELIM = ","


def parse_row(line):
    """Split one CSV line into stripped fields (no quoting support yet)."""
    return [field.strip() for field in line.rstrip("\n").split(DELIM)]
EOF

cat > test_parser.py <<'EOF'
import unittest

from parser import parse_row


class TestParseRow(unittest.TestCase):
    def test_basic_split(self):
        self.assertEqual(parse_row("a,b,c\n"), ["a", "b", "c"])

    def test_strips_whitespace(self):
        self.assertEqual(parse_row(" a , b ,c"), ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
EOF

cat > README.md <<'EOF'
# csvtool

Minimal CSV helpers, grown ticket by ticket.

- Run the checks: `python3 test_parser.py`
- Tickets live under `.tickets/`.
EOF

cat > .gitignore <<'EOF'
__pycache__/
EOF

mkdir -p .tickets/_standalone

cat > .tickets/_standalone/FEAT-001_csv-loader.md <<'EOF'
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
EOF

cat > .tickets/_standalone/FEAT-002_summary-stats.md <<'EOF'
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
EOF

cat > .tickets/_standalone/FEAT-003_input-validation.md <<'EOF'
---
id: FEAT-003
title: Validate row field counts
type: feature
status: to-do
priority: medium
created: 2026-06-08
updated: 2026-06-08
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
- [ ] Add `validate_row(fields, expected_count)` to `parser.py`: raises `ValueError` naming the actual and expected counts when they differ, returns the fields unchanged otherwise
- [ ] `parse_row` accepts an optional `expected_count=None` argument; when provided, the parsed fields are validated before being returned
- [ ] Add tests covering the mismatch error and the happy path

## File path hints
- `parser.py` — modify
- `test_parser.py` — modify

## Constraints
- Do NOT break existing callers: `parse_row(line)` with one argument must keep working unchanged
- Do NOT add third-party dependencies

## Acceptance criteria
- [ ] `validate_row(["a", "b"], 3)` raises `ValueError`; the message includes both counts
- [ ] `parse_row("a,b", expected_count=2)` returns `["a", "b"]`; `parse_row("a,b", expected_count=3)` raises `ValueError`
- [ ] All tests pass

## Verification
```bash
python3 test_parser.py
```
EOF

git add parser.py test_parser.py README.md .gitignore .tickets/_standalone
git commit -qm "fixture: csvtool baseline with prepared tickets"

# Untracked decoy: must never be swept into a commit (catches git add -A / git add .).
cat > perf-notes.local.md <<'EOF'
local perf scratch - not for committing
parse_row on 1M rows: 2.1s (laptop, battery)
EOF

echo "fixture ready: $TARGET"
