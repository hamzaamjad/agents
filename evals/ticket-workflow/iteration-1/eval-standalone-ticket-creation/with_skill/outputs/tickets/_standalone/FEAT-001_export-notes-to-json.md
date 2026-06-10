---
id: FEAT-001
title: "Export notes to JSON from the CLI with optional tag filter"
type: feature
status: to-do
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent:
dependencies: []
tags: [cli, export, json]
agent_created: true
complexity: 3
---

# Export notes to JSON from the CLI with optional tag filter

## Context
Team request: "Users want to export their notes to JSON from the CLI — and
filtering the export by tag would be nice too."

Notes already persist as JSON in `notes.json` (`load_notes`/`save_notes` in
`notes.py`), but there is no user-facing way to get them out: `main()` is a
stub that only prints usage. `list_notes(notes, tag=...)` already implements
exact-match tag filtering, so the export filter should reuse it. Printing the
export to stdout lets users redirect to any file (e.g.
`python3 notes.py export > backup.json`).

## Requirements
- [ ] Wire an `export` subcommand into `main()` in `notes.py`: `python3 notes.py export` prints all saved notes as a JSON array to stdout and exits 0
- [ ] Support an optional tag filter, `python3 notes.py export --tag <tag>`, that exports only notes whose `tags` list contains `<tag>` (reuse `list_notes`)
- [ ] When `notes.json` is missing, print `[]` and exit 0 (matches `load_notes` returning `[]`)
- [ ] Add unit tests to `test_notes.py` covering unfiltered export, tag-filtered export, and the empty store
- [ ] Document the `export` command in `README.md`

## File path hints
- `notes.py` — modify: add export logic and `export` subcommand wiring (incl. `--tag` parsing) in `main()`
- `test_notes.py` — modify: add export tests
- `README.md` — modify: document the export command

## Constraints
- Do NOT change the on-disk `notes.json` schema or the signatures/behavior of `load_notes`, `save_notes`, `add_note`, `list_notes`
- Do NOT build out other subcommands (`add`/`list` CLI wiring stays out of scope)
- Do NOT add third-party dependencies — stdlib only (`json`, `argparse`/manual parsing)
- Do NOT duplicate filter logic — tag filtering must go through `list_notes`

## Acceptance criteria
- [ ] `python3 notes.py export` prints a JSON array containing every note in `notes.json` to stdout and exits 0
- [ ] `python3 notes.py export --tag errand` prints only notes whose `tags` include `errand`
- [ ] With no `notes.json` present, `python3 notes.py export` prints `[]` and exits 0
- [ ] Export output parses cleanly with `python3 -m json.tool`
- [ ] All existing tests in `test_notes.py` continue to pass

## Verification
```bash
# Existing suite plus new export tests
python3 test_notes.py

# Manual end-to-end check (notes.json is gitignored)
echo '[{"text": "buy milk", "tags": ["errand"]}, {"text": "write report", "tags": ["work"]}]' > notes.json
python3 notes.py export | python3 -m json.tool
python3 notes.py export --tag work | python3 -m json.tool

# Empty-store behavior
rm notes.json
python3 notes.py export   # expect: []
```

## Notes
Tag filtering is an exact string match against a note's `tags` list, mirroring
`list_notes` semantics. See `BUG-001` for the input-validation precedent on
`add_note`; export has no comparable validation needs beyond the missing-file
case.
