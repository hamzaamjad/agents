# AGENTS.md

This repo (`~/.agents`) is the canonical, versioned library of agent skills for Hamza's machines. Plain Markdown plus a few bash/python helper scripts; no build system. Deployment hosts (Cursor, Claude Code, Codex) read skills from here directly or via symlink — see Deployment map.

## Critical rules

- Skill content must stay portable: every path inside a skill resolves relative to that skill's directory. Never reference a deployment root such as `.claude/skills/...` or an absolute home path from skill content.
- Treat `skills/*/SKILL.md` frontmatter `description` as a load-bearing trigger surface; edit it deliberately, not casually.
- Use moderate imperative phrasing in instruction files; avoid all-caps directives and aggressive emphasis.

## Permission boundaries

**Always** (no approval needed):

- Read anything in this repo; run skill scripts and the validation command below.
- Edit files in this repo when tied to a diagnosed finding or an explicitly assigned task.
- Make small, scoped commits on the current branch (one concern per commit).

**Ask first**:

- Any write outside this repo (`~/.codex/*`, `~/.claude/*`, project repos).
- Moving, renaming, or deleting a skill directory; changes to `.gitignore` policy.
- Rewriting skill content beyond what a diagnosed finding requires.

**Never**:

- Push, force-push, or rewrite history without explicit instruction.
- Commit secrets or credentials.
- Modify other workspaces' runtime artifacts (`.tickets/`, `.claude/worktrees/`) as if they were skill content.

## Key commands

- Validate the instruction layer: `python3 skills/engineering-context/scripts/validate_context.py .`
- There is no build, install, or test suite; the validation script and the skill eval loop are the quality gates.

## Environment facts

- `cursor` on PATH is the Cursor IDE launcher (symlink to `Cursor.app/.../bin/code`), not an agent. The headless agent CLI — primary command `agent`, back-compat alias `cursor-agent`, installed via `curl https://cursor.com/install -fsS | bash` — is not installed on this machine as of 2026-06-10. Re-check `which agent cursor-agent` before designing anything that shells out to it.
- Until that CLI exists here, eval arms run as host subagents, which share host context (skill descriptions are visible to both arms). Record that isolation caveat in benchmark notes, as `evals/ticket-workflow/iteration-1/benchmark.md` does.

## Directory layout

```
skills/<name>/                Skill package: SKILL.md + references/ + scripts/ (+ evals/ eval suite: evals.json + fixtures/)
skills/defining-specifications-workspace/   Eval artifacts for the defining-specifications skill (legacy location; iteration-N runs, not a skill)
evals/<skill>/                Eval workspaces: iteration-N/ benchmark artifacts — the convention for new eval workspaces
docs/audits/                  Instruction-layer audit reports (yyyy-mm-dd-<slug>.md)
docs/decisions/               Decision memos (yyyy-mm-dd-<slug>.md)
docs/specs/                   Specifications authored via defining-specifications
.prompts/                     Versioned prompts (exercise briefs, orchestration instances) — see docs/decisions/2026-06-10-version-tickets-and-prompts.md
.tickets/                     Versioned ticket-workflow tickets (active epics + _archive/)
.claude/worktrees/            Unversioned worktree checkouts — gitignored
```

## Skill-authoring conventions

- One directory per skill; the entry point is `skills/<name>/SKILL.md`, with on-demand depth in `references/` and executables in `scripts/`.
- Frontmatter: `name` (kebab-case, matches the directory) and `description` (third person, states concrete trigger conditions).
- Size budgets follow `skills/engineering-context/references/rubric.md`: keep the entry point lean (under ~150 lines preferred), keep sections under ~40 lines, and move anything longer into `references/` with a pointer.
- Link reference files relative to the skill's own directory, and cite external origins when bundling copied material.
- Skills that other repos consume at runtime (e.g. `ticket-workflow`) bundle their own runbooks and templates in `references/` rather than pointing at files in consuming repos.

## Eval loop

New or revised skills are benchmarked before being trusted:

1. Draft or revise the skill.
2. Run paired evals — the same tasks with and without the skill loaded.
3. Grade outputs (one grading.json per eval) and summarize each iteration in benchmark.md and benchmark.json.
4. Fold findings back into the skill and commit the new version.

Eval suites (the evals JSON plus fixture builders) live in `skills/<name>/evals/`; iteration artifacts go in a top-level workspace at `evals/<skill>/iteration-N/` — per-eval directories carrying eval metadata plus with_skill and without_skill runs (each with outputs and a grading file), topped by the iteration's benchmark summary pair. The `defining-specifications` workspace predates this convention and stays at `skills/defining-specifications-workspace/` until relocated; that directory holds eval data, not a skill.

## Orchestration

Conventions for sessions that run exercise briefs, epics, or evals through subagents:

- The orchestrator acts as the user's proxy by default: it makes checkpoint decisions, records each one in the produced artifact (or a `docs/decisions/` memo when policy-level), and surfaces only decisions the user explicitly reserved.
- Launch prompts are self-contained: workspace root, the exact file to read and follow, pre-decided boundaries (never push; never write outside this repo), and what the final message must report.
- Checkpoint convention: a subagent that hits a decision its brief reserves for the user stops and ends its message with a line starting `CHECKPOINT:` — decision needed, options, recommendation. The orchestrator resumes it with the decision.
- Exercise briefs live in `.prompts/exercises/`; per-epic orchestration prompts in `.prompts/orchestration/` (instances of the ticket-workflow canonical template).
- The orchestrator validates subagent claims independently between runs (git history, file existence, JSON/YAML parses, the validation script) before launching dependent work.

## Deployment map

| Host | Reads | Notes |
|---|---|---|
| Cursor | `~/.agents/skills/*/SKILL.md` | Loaded directly as user skills |
| Claude Code (per project) | `<repo>/.claude/skills/<skill>` | Symlink into this repo, e.g. `~/tickets/.claude/skills/ticket-workflow -> ~/.agents/skills/ticket-workflow` |
| Claude Code (global) | `~/.claude/CLAUDE.md` | Global memory only; no `~/.claude/skills` on this machine |
| Codex CLI | `~/.codex/skills/`, `~/.codex/AGENTS.md` | Separate unversioned library; consolidation proposal in `docs/decisions/2026-06-10-codex-skills-consolidation.md` |

## Repo documentation conventions

- Audit reports go in `docs/audits/`, decision memos in `docs/decisions/`, both named `yyyy-mm-dd-<slug>.md` and committed with the change they describe.
- Keep this file under 150 lines and free of session-scoped status; durable conventions only.
