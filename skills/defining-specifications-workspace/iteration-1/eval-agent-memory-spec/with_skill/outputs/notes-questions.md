# Notes And Questions

## Read-Only Sources Inspected

- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/priority-resolution.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/context-design-patterns.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/agents-md-spec.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/rubric.md`
- `/Users/hamzaamjad/.agents/skills/session-retrospective/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/defining-specifications-workspace/iteration-1/eval-agent-memory-spec/eval_metadata.json`

## Observations

- No root `AGENTS.md`, `CLAUDE.md`, or `README` was found under `/Users/hamzaamjad/.agents` during inspection.
- Existing `engineering-context` guidance strongly favors a lean canonical instruction surface with pointers to on-demand context.
- Existing `session-retrospective` guidance already treats `.context/` as a suitable home for durable domain or workspace context, after user approval.
- Existing `ticket-workflow` guidance is execution-oriented and should remain separate from memory/context summary conventions.

## Questions To Resolve Later

- Should `.context/agent-memory.md` be created even before there are durable decisions to record?
- If root instruction files are introduced, should this workspace maintain both `AGENTS.md` and `CLAUDE.md`, or only portable `AGENTS.md`?
- Should concise transcript links be allowed in the `Source` field, or should memory entries only cite local files/specs/tickets?
- Should users be the only authority allowed to delete obsolete memory entries, with agents limited to marking `needs-review` or proposing `superseded`?

## Assumptions Used

- The desired output is a focused specification, not implementation.
- The memory convention should avoid automatic transcript mining.
- Durable memory entries should be sparse, auditable, and stable enough for downstream agents to reference by ID.
- Future agents should be able to verify the convention with file inspection and simple shell checks.
