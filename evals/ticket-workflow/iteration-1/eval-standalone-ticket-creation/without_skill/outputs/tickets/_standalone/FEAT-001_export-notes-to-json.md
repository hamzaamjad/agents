---
id: FEAT-001
title: Export notes to JSON from the CLI
type: feature
status: open
---

# Export notes to JSON from the CLI

Users want to export their notes to JSON from the CLI, and filtering the
export by tag would be nice too.

Notes are already stored as JSON (`notes.json`), so this is mostly CLI
wiring: add an `export` command alongside `add` and `list` in `main`. With
no arguments it writes all notes as JSON to stdout (users can redirect to a
file); with an optional tag argument (mirroring `list [tag]`) it exports
only notes carrying that tag, reusing the existing `list_notes` filtering.

Things to check when implementing this:
- `export` emits all notes as valid JSON in the stored shape (`text` + `tags`)
- `export <tag>` includes only notes carrying that tag
- no notes, or no notes matching the tag, exports `[]` rather than erroring
- output round-trips through `json.loads`
- usage string in `main` mentions `export`
- tests added to `test_notes.py`
- no new dependencies
