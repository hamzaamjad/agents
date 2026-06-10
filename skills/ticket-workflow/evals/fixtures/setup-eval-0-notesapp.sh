#!/usr/bin/env bash
# Fixture builder for ticket-workflow eval 0 (standalone-ticket-creation).
# Builds a minimal "notesapp" repo with one legacy-style done ticket that
# establishes the .tickets/_standalone/ location and TYPE-NNN naming, but
# deliberately not the full template (no Constraints/Verification sections).
# Usage: setup-eval-0-notesapp.sh <target-dir>
set -euo pipefail

TARGET="${1:?usage: $0 <target-dir>}"
mkdir -p "$TARGET"
cd "$TARGET"

git init -q -b main
git config user.name "Eval Fixture"
git config user.email "fixture@example.invalid"

cat > notes.py <<'EOF'
"""Tiny note-keeping library used by the notesapp CLI."""

import json
import sys

NOTES_FILE = "notes.json"


def load_notes(path=NOTES_FILE):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_notes(notes, path=NOTES_FILE):
    with open(path, "w") as f:
        json.dump(notes, f, indent=2)


def add_note(notes, text, tags=None):
    if not text or not text.strip():
        raise ValueError("note text cannot be empty")
    notes.append({"text": text.strip(), "tags": sorted(set(tags or []))})
    return notes


def list_notes(notes, tag=None):
    if tag is None:
        return list(notes)
    return [n for n in notes if tag in n.get("tags", [])]


def main(argv):
    print("usage: notes.py [add <text>|list [tag]]  (CLI wiring is minimal)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
EOF

cat > test_notes.py <<'EOF'
import unittest

from notes import add_note, list_notes


class TestNotes(unittest.TestCase):
    def test_add_note_appends(self):
        notes = add_note([], "buy milk", tags=["errand"])
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["text"], "buy milk")

    def test_add_note_rejects_empty(self):
        with self.assertRaises(ValueError):
            add_note([], "   ")

    def test_list_notes_filters_by_tag(self):
        notes = add_note([], "buy milk", tags=["errand"])
        notes = add_note(notes, "write report", tags=["work"])
        self.assertEqual(len(list_notes(notes, tag="work")), 1)
        self.assertEqual(len(list_notes(notes)), 2)


if __name__ == "__main__":
    unittest.main()
EOF

cat > README.md <<'EOF'
# notesapp

A tiny note-keeping CLI. Notes have text and optional tags.

- Run the checks: `python3 test_notes.py`
- Tickets live under `.tickets/`.
EOF

cat > .gitignore <<'EOF'
__pycache__/
notes.json
EOF

mkdir -p .tickets/_standalone
cat > .tickets/_standalone/BUG-001_fix-empty-note-crash.md <<'EOF'
---
id: BUG-001
title: Fix crash when adding an empty note
type: bug
status: done
---

# Fix crash when adding an empty note

`add_note` used to crash with an unhandled exception when passed an empty
string. Fixed by validating input and raising `ValueError` with a clear
message.

Things that were checked while fixing this:
- empty string rejected
- whitespace-only string rejected
- error message mentions the word "empty"
- existing notes unaffected
- tags untouched
- README unchanged
- no new dependencies
EOF

git add notes.py test_notes.py README.md .gitignore .tickets/_standalone/BUG-001_fix-empty-note-crash.md
git commit -qm "fixture: notesapp baseline"

# Untracked decoy: must never be swept into a commit (catches git add -A / git add .).
cat > TODO-personal.txt <<'EOF'
personal scratchpad - not for committing
- ask about Friday
- expense report
EOF

echo "fixture ready: $TARGET"
