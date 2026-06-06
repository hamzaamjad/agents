# Notes And Questions

## Scope Notes

- This task was completed without reading `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`.
- No tickets, source files, implementation code, or broad documentation files were edited.
- Outputs were written only under the assigned `without_skill/outputs/` directory.

## Read-Only Sources Inspected

- `skills/engineering-context/SKILL.md`
- `skills/engineering-context/references/agents-md-spec.md`
- `skills/engineering-context/references/context-design-patterns.md`
- `skills/engineering-context/references/priority-resolution.md`
- `skills/engineering-context/references/rubric.md`
- `skills/session-retrospective/SKILL.md`
- `skills/ticket-workflow/SKILL.md`
- `skills/ticket-workflow/references/outcome-schema.md`
- `skills/ticket-workflow/references/templates.md`
- `skills/engineering-prompts/references/CONTEXT_ENGINEERING.md`

## Working Assumptions

- A lightweight convention should live in `.context/agent-memory.md`, not in an always-loaded root instruction file.
- Memory should be advisory and lower precedence than explicit user instructions, active tickets, source code, tests, and root instruction files.
- Existing ticket `## Outcome` blocks should remain the primary retrieval surface for completed ticket work.
- The initial convention should be manual and markdown-only; automation can be considered later if the file proves useful.
- The workspace currently lacks root `AGENTS.md`, `CLAUDE.md`, `README.md`, and `.context/` docs, so the spec avoids assuming those files already exist.

## Clarifying Questions For A Future Implementer

- Should future memory seeding mine parent chat transcripts, or should it only use accepted specs, tickets, and existing workspace docs?
- Should a memory update require explicit user approval every time, or is a completed/accepted artifact enough evidence?
- If a root `AGENTS.md` is later created, should it include a one-line pointer to `.context/agent-memory.md`?
- Should the memory file have a scheduled review cadence, or should pruning happen only during retrospectives and instruction cleanup?
- Should there be separate user-preference memory, or should this convention remain limited to project/workspace decisions?
