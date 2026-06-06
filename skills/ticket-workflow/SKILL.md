---
name: ticket-workflow
description: "Manage structured tickets in .tickets/. Use when: creating tickets, executing/implementing tickets, decomposing tickets into sub-tickets, updating ticket status, creating or closing epics, archiving completed epics, or verifying ticket completion. Handles the full lifecycle: template-based creation, ID assignment, dependency checking, complexity assessment, decomposition, scoped execution, verification, and archival."
---

# Ticket Workflow

## Directory Structure

```
.tickets/
  _standalone/           # Tickets without a parent epic
  _archive/              # Completed epics (read-only historical context)
    EPIC-<hex>_<slug>/
  EPIC-<hex>_<slug>/     # Active epic directories (hex = 4-char random ID)
    _epic.md             # Epic ticket
    TYPE-NNN_*.md        # Sub-tickets (sequential numbering within epic)
```

## Naming

Epic directories: `EPIC-<hex>_<slug>/` where `<hex>` is a 4-character random hex ID (e.g., `EPIC-a7f3_field-contract/`). Sub-ticket files: `TYPE-NNN_kebab-slug.md` with IDs locally scoped within their epic. Cross-epic references: `EPIC-<hex>/TYPE-NNN` (e.g., `EPIC-a7f3/FEAT-001`).

| Prefix | Type     | Use case                                    |
|--------|----------|---------------------------------------------|
| `FEAT` | feature  | New functionality                           |
| `BUG`  | bug      | Defect fix                                  |
| `REFAC`| refactor | Structural improvement, zero behavior change|
| `CHORE`| chore    | Maintenance, CI, docs, tooling              |
| `TASK` | task     | Agent-generated sub-ticket                  |
| `EPIC` | epic     | Parent ticket grouping related work         |

### Dependency ID resolution

Bare IDs in a ticket's `dependencies` frontmatter field — e.g. `FEAT-001` — resolve within the ticket's current epic (`bare IDs resolve within current epic`). Cross-epic dependencies must use the full form `EPIC-<hex>/TYPE-NNN`. An agent resolving a bare ID that has no in-epic match must fail the dependency check, not search other epics globally.

## Status Lifecycle

`to-do` --> `in-progress` --> `done`

A ticket may also be `blocked`. `in-progress` is optional -- agents may go directly from `to-do` to `done`.

## ID Assignment

### Epics

Generate a 4-character random hex ID. No filesystem scan needed -- eliminates collision risk when multiple agents create epics concurrently.

```bash
python -c "import secrets; print(f'EPIC-{secrets.token_hex(2)}')"
```

### Sub-tickets and standalone tickets

Sequential numbering within their directory scope. Find the next available number:

```bash
# Within an epic:
ls .tickets/EPIC-*_*/[A-Z]*.md | sed 's|.*/||;s|_.*||' | sort -t- -k1,1 -k2,2rn | awk -F- '!seen[$1]++' | sort

# Standalone:
ls .tickets/_standalone/[A-Z]*.md | sed 's|.*/||;s|_.*||' | sort -t- -k1,1 -k2,2rn | awk -F- '!seen[$1]++' | sort
```

## Worktree Rules

**Recovery:** If any `git worktree` step fails, stop and follow `docs/runbooks/worktree-recovery.md` § Diagnostic commands before retrying.

All epic-related work (creation, execution, orchestration, archival) MUST happen in a git worktree — never directly on the main branch. Main is the integration target; agents never modify it directly.

### Orchestrator worktree

The agent that creates an epic's tickets and orchestration prompt — or orchestrates epic execution — must work in a worktree, not on main. This prevents accidental main branch mutations when multiple epics run concurrently.

```bash
# Ticket-creator / orchestrator worktree setup
git worktree add .claude/worktrees/epic-<hex> -b epic/<hex>/<slug> main
cd .claude/worktrees/epic-<hex>
```

### Sub-ticket worktrees

Sub-ticket agents branch from the epic branch, not main. Paths and branch names are namespaced under the epic hex to prevent collisions when multiple epics run concurrently.

```bash
git worktree add .claude/worktrees/epic-<hex>/<ticket-id> -b epic-<hex>/<ticket-id>/<slug> epic/<hex>/<slug>
```

### Key constraints

- **Never `cd` to the primary clone.** An agent's working directory is its worktree. All `git` and `gh` commands run from there.
- **`gh pr create` inherits the branch from `cwd`.** Running it from the worktree automatically targets the correct branch — no checkout needed.
- **Never use `git add -A` or `git add .`** in a worktree-heavy repo. Stage specific files by name.
- **Serialize `git worktree add` calls per repo.** On `.git/config.lock` contention, retry with jitter — see `worktree-recovery.md` § Prevention conventions for the exact snippet.
- Standalone ticket creation (writing a markdown file to `_standalone/`) is exempt — it may happen on main.

## Creating Tickets

### Epics

1. Generate hex ID: `python -c "import secrets; print(secrets.token_hex(2))"` (e.g., `a7f3`).
2. Create a worktree for the epic: `git worktree add .claude/worktrees/epic-<hex> -b epic/<hex>/<slug> main`.
3. Working from the worktree, create directory: `.tickets/EPIC-<hex>_<slug>/`.
4. Read the epic template from [references/templates.md](references/templates.md).
5. Create `_epic.md` with the generated ID and `branch: epic/<hex>/<slug>` in frontmatter.
6. Create all sub-tickets and the orchestration prompt (`.prompts/orchestration/epic-<hex>_*.md`) in the same worktree.
7. Commit and merge to main (or PR) before orchestration begins.

### Sub-tickets

1. Determine target: `.tickets/EPIC-<hex>_<slug>/` or `.tickets/_standalone/`.
2. Run the sub-ticket ID assignment command to find the next number.
3. Read the matching template from [references/templates.md](references/templates.md).
4. Create `TYPE-NNN_kebab-slug.md`. Required frontmatter: `id`, `title`, `type`, `status`.

## Epic Branch Workflow

Each epic develops on its own branch, isolating it from other concurrent epics.

- **Epic branch**: `epic/<hex>/<slug>` -- created from main when the epic starts.
- **Sub-ticket worktrees**: branch from the epic branch, not main.
- **Sub-ticket merges**: go into the epic branch, not main.
- **Completion**: PR from epic branch to main. Archive after PR merge.

This prevents cross-epic conflicts on shared files. Conflicts between epics surface at PR review time, not during agent execution.

## Orchestrator Review Protocol

The orchestrator is the first automated quality gate between a sub-agent's finished ticket and the epic branch. The canonical 12-gate review checklist, the four escalation actions, the `MAX_FIX_CYCLES = 2` retry budget, and the six terminal outcome states live in [references/orchestrator-review-protocol.md](references/orchestrator-review-protocol.md). The executable form of the same protocol — the orchestration prompt with all placeholders — lives at [.prompts/orchestration/_template.md](../../../.prompts/orchestration/_template.md); per-epic briefs in `.prompts/orchestration/epic-<hex>_*.md` are instances of that template.

- Outcome states: `MERGED / NEEDS_FIX / REASSIGNED / ESCALATED / RESTARTED / BLOCKED_DEPENDENCY`.

The file `.prompts/orchestration/_template.md` is underscore-prefixed so it is **not** matched by the closure ticket's `epic-<hex>_*.md` glob; do not change that glob.

## Execution Protocol

Follow in exact order when assigned a ticket.

### Step 1: Read

Read the full ticket file. Understand requirements, constraints, acceptance criteria, and verification commands.

### Step 2: Check dependencies

Inspect `dependencies` in frontmatter. If any dependency status != `done`, STOP and report the blocker.

### Step 3: Assess complexity

Populate `complexity` (integer 1–10) in the ticket's frontmatter using the rubric in [references/complexity-scoring.md](references/complexity-scoring.md). Required whenever the ticket has a `parent:` set or affects more than one file; optional elsewhere.

Decompose (proceed to Step 4) if **either** trigger fires:

- **(i)** The model-tier file threshold is exceeded. *Tier B (frontier, current default): decompose at complexity ≥ 8, ≥ 5 real files, or any high-risk cross-cutting / data / integration change. Tier A (Haiku-class): decompose at complexity ≥ 6, ≥ 3 real files.*
- **(ii)** Execution stalls past ~25 meaningful tool rounds without convergence — abort and decompose. "Meaningful" means tool calls that act on the repo (read, edit, run verification, git); re-reading the current ticket or listing terminals does not count.

Both tiers are listed side-by-side deliberately: the workspace defaults to Tier B, but a running agent must be able to see Tier A's lower bar when it is executing under a Haiku-class model.

### Step 4: Decompose

Create `TASK-NNN` files with `parent:` set, `dependencies:` for execution order, `agent_created: true`, each targeting 1-2 files and <=3 acceptance criteria. Use templates from [references/templates.md](references/templates.md). Update the parent ticket with a sub-tickets tracking table and set status to `in-progress`.

### Step 5: Execute

- Read all files referenced in file path hints before making changes.
- Implement requirements within constraints -- no features beyond scope.

### Step 6: Verify

Run every command in the ticket's `## Verification` section. All must pass.

Record the **actual tool-round count** in the ticket's verification log alongside the `complexity` populated at Step 3. Future archive retrieval surfaces drift between predicted complexity and realized cost — this is the calibration loop that makes the Step 3 rubric empirical rather than speculative.

### Step 7: Mark done

On the branch, before merge:

1. Append an `## Outcome` section to the ticket using the schema in `references/outcome-schema.md`.
2. The Outcome append is staged in the same commit as `status: done` (the mark-done commit). The "separate from implementation work" rule refers to **production code changes**, not ticket metadata written at closure.
3. Set `status: done` and update `updated` date in frontmatter.
4. Create a **dedicated commit**: `{TICKET-ID}: mark ticket as done` (separate from implementation work — but the Outcome block rides with it per sub-step 2).
5. Do NOT update parent epic status -- managed by the orchestration agent.

## Epic Closure Ticket

**Recovery:** If closure fails mid-run, follow `docs/runbooks/worktree-recovery.md` § Recovery procedures > Closure ticket partial execution (Goal A is the safe default).

Every epic MUST include a final closure ticket (typically the last `CHORE` in merge order) that performs all cleanup. This ticket runs on the epic branch before the PR to main, so main receives a clean state.

Every step below must be safe to re-run; check existence before acting. If closure crashes partway through, the re-run must be a no-op on already-completed steps, not a failure.

The closure ticket must:

1. **Mark all sub-tickets and epic as `done`** — set `status: done` and update `updated` dates.
2. **Archive the epic folder** — guarded `git mv` so a partial re-run is a no-op:
   ```bash
   [ -d .tickets/_archive/EPIC-<hex>_<slug> ] || git mv .tickets/EPIC-<hex>_<slug> .tickets/_archive/EPIC-<hex>_<slug>
   ```
3. **Delete the orchestration prompt** — guarded `git rm`:
   ```bash
   [ -f .prompts/orchestration/epic-<hex>_*.md ] && git rm .prompts/orchestration/epic-<hex>_*.md || true
   ```
4. **Clean up worktree artifacts** — guarded `rm -rf`:
   ```bash
   [ -d .claude/worktrees/epic-<hex> ] && rm -rf .claude/worktrees/epic-<hex> || true
   ```
5. **Commit** — single commit: `{EPIC-ID}: archive epic and clean up orchestration artifacts`.

After the epic's PR is merged to main, the orchestrator cleans up only its own worktrees — never other epics':

```bash
# Remove only this epic's worktrees and branches
git worktree list | grep '.claude/worktrees/epic-<hex>' | awk '{print $1}' | xargs -I{} git worktree remove {} --force
git branch -d epic/<hex>/<slug>
git branch --list 'epic-<hex>/*' | xargs git branch -d 2>/dev/null
```

Archived tickets are read-only. Do not modify files under `_archive/`. Active sources are authoritative when conflicts arise.

## Querying past work

Before creating a new epic that touches an unfamiliar subsystem, mine the archive for prior Outcome blocks. Run `bash .claude/skills/ticket-workflow/scripts/archive-search.sh '<short epic pitch>'` (optionally scoping with `--type`, `--tags`, `--complexity`) and inject the top matches' `## Outcome` snippets into the new epic's Context section. The Outcome schema in `references/outcome-schema.md` is what makes those snippets dense enough to be useful; the script prints only the Outcome block, never the full ticket body, so the injected context stays small and high-signal.

Lane A (lexical) is sufficient until the archive crosses the scale horizon documented in `references/outcome-schema.md`; `--semantic` (Lane B) is reserved for that future trigger.

## Coding Standards

- Do not add features, refactoring, or improvements beyond ticket scope.
- Do not add error handling for scenarios that cannot happen.
- Do not create abstractions for one-time operations.
- Run verification commands before marking done.
- If file path hints reference nonexistent files, investigate before proceeding -- hints may be stale.

## Quality Rules

- Tickets under 200 lines.
- Maximum 5 acceptance criteria -- decompose if more needed.
- Every ticket must have `## Verification` with runnable commands.
- Include `## Constraints` to prevent scope creep.
- Concrete nouns, verbs, and file paths -- no vague instructions.
- Do NOT self-orchestrate decomposition -- follow the step order rigidly.
