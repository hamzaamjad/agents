# Notes And Questions: Agent Memory Context Summary Spec

Date: 2026-06-05

## Read-Only Context Inspected

- `/Users/hamzaamjad/.agents/skills/defining-specifications/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/context-design-patterns.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/agents-md-spec.md`
- `/Users/hamzaamjad/.agents/skills/engineering-context/references/priority-resolution.md`
- `/Users/hamzaamjad/.agents/skills/session-retrospective/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/SKILL.md`
- `/Users/hamzaamjad/.agents/skills/ticket-workflow/references/outcome-schema.md`

## Workspace Observations

- No root `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`, or `.context/` directory was found during this pass.
- Existing context-engineering guidance strongly favors small always-loaded instruction files and on-demand modules.
- Existing retrospective guidance already names `.context/` as a possible workspace improvement target, but only after evidence-backed review and user approval.
- Existing ticket guidance treats archived ticket `## Outcome` blocks as compact retrieval surfaces, which the memory convention should point to rather than duplicate.
- Prior evaluation outputs surfaced in search results, but were treated as historical artifacts rather than authoritative workspace decisions.

## Clarifying Questions Not Asked Due Evaluation Constraints

- Should the first implementation create `.context/agent-memory.md` before a root `AGENTS.md` exists, or should both be introduced together?
- Should memory IDs use date-based IDs like `MEM-20260605-01` or shorter sequential IDs like `MEM-001`?
- Should agents ever delete stale memory directly, or only mark entries `superseded` / `needs-review` until a human approves cleanup?
- Should session retrospectives explicitly recommend memory entries, or only recommend workspace improvements where memory is one possible target?

## Working Assumptions

- `.context/agent-memory.md` is the right canonical home because it keeps root instructions small and matches existing dynamic-loading guidance.
- Memory should be advisory and lower authority than system/runtime instructions, explicit user instructions, source files, active tickets, current specs, and canonical instruction files.
- The first implementation should create a skeleton and add entries gradually from future consolidation passes, not bulk-import chat history.
- This evaluation task should save only the specification and notes in the assigned output directory.
