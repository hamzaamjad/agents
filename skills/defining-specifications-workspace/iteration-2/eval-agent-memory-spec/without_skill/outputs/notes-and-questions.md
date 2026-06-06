# Notes and Questions

Date: 2026-06-05
Task: Baseline evaluation for an agent memory/context summary convention

## Read-Only Context Inspected

- `skills/engineering-context/SKILL.md`
- `skills/engineering-context/references/agents-md-spec.md`
- `skills/engineering-context/references/context-design-patterns.md`
- `skills/engineering-context/references/priority-resolution.md`
- `skills/engineering-context/references/rubric.md`
- `skills/ticket-workflow/SKILL.md`
- `skills/ticket-workflow/references/outcome-schema.md`
- `skills/session-retrospective/SKILL.md`
- `.gitignore`

The prohibited `skills/defining-specifications/SKILL.md` file was not read or used.

## Observations

- No root `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.context/`, or `.tickets/` directory was present during inspection.
- Existing guidance consistently warns against bloated always-loaded context and session-scoped content in persistent instruction files.
- The ticket workflow already has a dense `## Outcome` pattern for archived ticket retrieval; the proposed memory convention borrows the same high-signal style without requiring tickets.
- `.gitignore` excludes `.tickets/`, `.prompts/`, and `.claude/worktrees/`, but does not currently exclude `.context/`.

## Assumptions

- The desired convention should be committed workspace context unless the user later decides `.context/` is local-only.
- A single `.context/agent-memory.md` file is enough for the initial convention.
- Agent memory should be curated and replace stale entries, not append every session summary.
- Current files remain authoritative over memory when they conflict.
- Root instruction-file pointers are useful later, but creating root instruction files is outside this task.

## Clarifying Questions Not Asked

- Should `.context/agent-memory.md` be tracked in git, ignored, or split into tracked and local variants?
- Should future session-retrospective work be allowed to write memory entries automatically after user approval?
- What threshold should promote a ticket `## Outcome` decision into agent memory?
- Should transcript references be allowed in durable memory, and if so, what exact link format should be canonical?
