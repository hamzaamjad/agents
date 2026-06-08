# Notes & Clarifying Questions — Agent Memory Convention

Companion to `SPEC-agent-memory-context-summary.md`. Captures the read-only investigation and the
clarifying questions that would normally be asked of the requester. This pass is non-interactive,
so each question carries a working assumption (mirrored in the spec's §8).

## Read-only investigation log

Inspected (read-only, no modifications outside the assigned output directory):

- Workspace root `ls` and `.gitignore`.
- Confirmed no `AGENTS.md` / `CLAUDE.md` / `.cursorrules` anywhere in the repo.
- `git check-ignore .context/agent-memory.md` → not ignored (would be committed/tracked).
- `skills/engineering-context/SKILL.md` and references `agents-md-spec.md`,
  `context-design-patterns.md` (Tier 0/1/2 model; lean-instruction + size guidance).
- `skills/session-retrospective/SKILL.md` (Phase 2 already targets `.context/`,
  `AGENTS.md`/`CLAUDE.md`; "add additions over edits", "archive before delete").

Key facts that shaped the design:

1. `.context/` is already named as a sanctioned workspace-improvement target and is **not**
   gitignored, so it is the natural shared home for durable memory.
2. The gitignore deliberately marks `.tickets/`, `.prompts/`, `.claude/worktrees/` as
   per-workspace ephemeral — memory is intentionally the opposite (shared).
3. Existing skill guidance is strongly anti-bloat: instruction files that grow unmaintained
   *reduce* task success, so the convention enforces a size cap + promotion criteria.
4. There is a real gap: durable *decisions + rationale* are neither Tier 0 (lean must-follow
   rules) nor Tier 2 (session-scoped). The memory file fills that middle tier.

## Clarifying questions (with assumptions taken)

1. **Granularity** — one file vs. `.context/memory/<topic>.md`?
   Assumption: single file now; split deferred until the cap is repeatedly hit.
2. **Sharing model** — committed vs. gitignored?
   Assumption: committed/shared (matches `.context/` status and the cross-session goal).
3. **AGENTS.md** — introduce one now to host the pointer?
   Assumption: no; out of scope. Pointer rule applies only if/when an AGENTS.md exists.
4. **Write authority** — autonomous agent appends vs. human-gated?
   Assumption: agents may append under the promotion criteria; consolidation (the only
   destructive edit) follows the existing archive/confirm posture.
5. **Filename** — `agent-memory.md` vs `MEMORY.md` vs `decisions.md`?
   Assumption: `.context/agent-memory.md`.
6. **Frontmatter** — YAML for future tooling vs. plain Markdown?
   Assumption: plain Markdown; revisit if validation tooling is later requested.
7. **Retention** — hard delete superseded entries or keep them?
   Assumption: keep with `Status: superseded by AM-XXXX`; prune only at consolidation.

## Explicitly deferred (not in this spec)

- Any automation (hooks, CI validation, search/embeddings, databases).
- Transcript ingestion / auto-summarization.
- Editing `session-retrospective` / `engineering-context` to wire in append behavior
  (the spec describes the integration points but changes no skill).
- Creating/seeding the memory file itself.
