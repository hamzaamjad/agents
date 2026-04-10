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

## Execution Protocol

Follow in exact order when assigned a ticket.

### Step 1: Read

Read the full ticket file. Understand requirements, constraints, acceptance criteria, and verification commands.

### Step 2: Check dependencies

Inspect `dependencies` in frontmatter. If any dependency status != `done`, STOP and report the blocker.

### Step 3: Assess complexity

If 4+ files or 5+ acceptance criteria, decompose into sub-tickets (Step 4). Otherwise skip to Step 5.

### Step 4: Decompose

Create `TASK-NNN` files with `parent:` set, `dependencies:` for execution order, `agent_created: true`, each targeting 1-2 files and <=3 acceptance criteria. Use templates from [references/templates.md](references/templates.md). Update the parent ticket with a sub-tickets tracking table and set status to `in-progress`.

### Step 5: Execute

- Read all files referenced in file path hints before making changes.
- Implement requirements within constraints -- no features beyond scope.

### Step 6: Verify

Run every command in the ticket's `## Verification` section. All must pass.

### Step 7: Mark done

On the branch, before merge:

1. Set `status: done` and update `updated` date in frontmatter.
2. Create a **dedicated commit**: `{TICKET-ID}: mark ticket as done` (separate from implementation work).
3. Do NOT update parent epic status -- managed by the orchestration agent.

## Epic Closure Ticket

Every epic MUST include a final closure ticket (typically the last `CHORE` in merge order) that performs all cleanup. This ticket runs on the epic branch before the PR to main, so main receives a clean state.

The closure ticket must:

1. **Mark all sub-tickets and epic as `done`** — set `status: done` and update `updated` dates.
2. **Archive the epic folder** — `git mv .tickets/EPIC-<hex>_<slug> .tickets/_archive/EPIC-<hex>_<slug>`.
3. **Delete the orchestration prompt** — `git rm .prompts/orchestration/epic-<hex>_*.md`.
4. **Update `docs/INDEX.md`** — remove this epic's entries from "Active Initiative Artifacts" if present. This must be idempotent: if another epic's closure already merged and removed the entries, do not fail. Do not add to "Completed Initiative Artifacts" (the archive itself is the record).
5. **Clean up worktree artifacts** — `rm -rf .claude/worktrees/epic-<hex>` (if the directory exists in the tree).
6. **Commit** — single commit: `{EPIC-ID}: archive epic and clean up orchestration artifacts`.

After the epic's PR is merged to main, the orchestrator cleans up only its own worktrees — never other epics':

```bash
# Remove only this epic's worktrees and branches
git worktree list | grep '.claude/worktrees/epic-<hex>' | awk '{print $1}' | xargs -I{} git worktree remove {} --force
git branch -d epic/<hex>/<slug>
git branch --list 'epic-<hex>/*' | xargs git branch -d 2>/dev/null
```

Archived tickets are read-only. Do not modify files under `_archive/`. Active sources are authoritative when conflicts arise.

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
