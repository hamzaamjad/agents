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
