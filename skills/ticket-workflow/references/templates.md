# Ticket Templates

Read the matching template for the ticket type being created. Copy the full template, then replace all placeholders.

## Feature

`````markdown
---
id: FEAT-XXX
title: ""
type: feature
status: to-do
priority: medium         # critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
parent:                  # parent ticket ID (e.g., EPIC-a7f3)
dependencies: []         # ticket IDs that must complete first
tags: []
agent_created: false
complexity:              # 1-10, optional — helps agents decide whether to decompose
---

# [Title]

## Context
[Why does this feature exist? What problem does it solve? Link to parent epic
or initiative if applicable.]

## Requirements
- [ ] [Concrete, verifiable requirement]
- [ ] [One requirement per checkbox]
- [ ] [Each should map to a testable outcome]

## File path hints
- `path/to/file.py` — [what to do: create | modify | delete]

## Constraints
- Do NOT [specific thing to avoid]
- Must [specific invariant to maintain]

## Acceptance criteria
- [ ] [Observable outcome with concrete values]
- [ ] [Keep to 5 or fewer — decompose if more are needed]

## Verification
```bash
# Commands the agent should run to self-check
pytest tests/path/to/test_file.py -v
```

## Notes
[Optional: links to docs, architecture decisions, related discussions.]
`````

## Bug

`````markdown
---
id: BUG-XXX
title: ""
type: bug
status: to-do
priority: medium         # critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
parent:                  # parent ticket ID if applicable
dependencies: []
tags: []
agent_created: false
complexity:              # 1-10, optional
---

# [Title]

## Description
[What is broken? What is the user-visible impact?]

## Steps to reproduce
1. [Exact step]
2. [Exact step]
3. [Observe the defect]

## Expected behavior
[What should happen.]

## Actual behavior
[What happens instead.]

## File path hints
- `path/to/file.py` — [suspected location of the defect]

## Root cause hypothesis
[Optional but valuable: your best guess at why this happens.
Agents use this to narrow their search.]

## Constraints
- Do NOT [specific thing to avoid]
- Fix must [specific invariant to maintain]

## Acceptance criteria
- [ ] [The defect no longer occurs under the reproduction steps]
- [ ] [Regression test exists]
- [ ] [Existing tests continue to pass]

## Verification
```bash
# Commands to confirm the fix
pytest tests/path/to/test_file.py -v
```

## Notes
[Optional: logs, screenshots, related issues.]
`````

## Chore

`````markdown
---
id: CHORE-XXX
title: ""
type: chore
status: to-do
priority: medium         # critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
parent:                  # parent ticket ID if applicable
dependencies: []
tags: []
agent_created: false
complexity:              # 1-10, optional
---

# [Title]

## Description
[What needs to be done and why. Chores are maintenance tasks that don't
change user-facing behavior: dependency updates, CI config, documentation,
tooling, etc.]

## Tasks
- [ ] [Concrete action item]
- [ ] [One task per checkbox]

## File path hints
- `path/to/file` — [what to do]

## Constraints
- Do NOT [specific thing to avoid]

## Acceptance criteria
- [ ] [Verifiable outcome]
- [ ] [Existing tests continue to pass]

## Verification
```bash
# Commands to confirm completion
```

## Notes
[Optional: links, context.]
`````

## Refactor

`````markdown
---
id: REFAC-XXX
title: ""
type: refactor
status: to-do
priority: medium         # critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
parent:                  # parent ticket ID if applicable
dependencies: []
tags: []
agent_created: false
complexity:              # 1-10, optional
---

# [Title]

## Motivation
[Why is this refactor needed? What pain does the current code cause?
Be specific — "tech debt" alone is not sufficient.]

## Scope
Files with the code to refactor:
- `path/to/file.py` (lines NN-MM) — [what's wrong]

## Target structure
- Create `path/to/new_module.py` — [purpose]
- Modify `path/to/existing.py` — [what changes]

## Acceptance criteria
- [ ] Zero behavior change — all existing tests pass unchanged
- [ ] [Structural goal achieved]
- [ ] Linter and type checker pass with no new warnings

## Constraints
- Pure refactor — NO feature changes, NO API contract changes
- Do NOT rename any existing public functions or endpoints
- Do NOT change return types or response shapes

## Verification
```bash
# Full test suite must pass unchanged
pytest tests/ -v --tb=short
ruff check path/to/new_module.py
```

## Notes
[Optional: links to design docs, prior discussions.]
`````

## Epic

`````markdown
---
id: EPIC-XXXX
title: ""
type: epic
status: to-do
priority: high             # critical | high | medium | low
branch:                    # epic/<hex>/<slug> — the epic's primary branch
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
agent_created: false
complexity:                # 1-10, optional
---

# [Title]

## Context

[Why does this epic exist? What problem does it solve? Link to any analysis
documents in `.notes/` or prior epics. Summarize what must NOT change and
what this epic specifically addresses.]

## Sub-tickets

| ID       | Title         | Status |
|----------|---------------|--------|
| FEAT-XXX | [description] | to-do  |
| CHORE-XXX| [description] | to-do  |

<!-- Add one row per sub-ticket. Update Status as work progresses. -->

## Merge order

<!-- List sub-tickets in the order they should be merged to the epic branch.
     Note which can execute in parallel worktrees vs. must merge sequentially.
     The closure CHORE ticket must ALWAYS be last — it archives the epic,
     deletes the orchestration prompt, and updates INDEX.md.
     See SKILL.md "Epic Closure Ticket" for the full spec.
-->

1. [TICKET-ID] ([rationale — why this merges first])
2. [TICKET-ID] ([rationale — dependency or conflict note])
N. CHORE-NNN — Epic closure (always last: archives epic, deletes orchestration prompt, updates INDEX.md)

## Acceptance criteria

- [ ] All sub-tickets are `done`
- [ ] Full test suite passes on epic branch
- [ ] Epic archived and orchestration prompt deleted (by closure ticket)
- [ ] PR from epic branch to main created and ready for review
- [ ] [Epic-specific verifiable outcome]

## Notes

[Optional: links to analysis sources, architecture decisions, prior epics,
or context that informed this epic's scope.]
`````
