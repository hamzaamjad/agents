# Diagnostic Rubric

Use this rubric to classify and remediate instruction file issues.

## Failure Patterns

### 1) Bloat and Verbosity

- Instruction files exceed practical size and attention budget.
- Explanations repeat what code or linters already enforce.
- Large static reference material is embedded instead of linked.
- **Counterproductive context**: empirical evidence (ETH Zurich, Feb 2026, 438-task benchmark) shows that poorly curated AGENTS.md files *reduce* task success by ~3% while inflating inference costs by >20%. Human-written files provide only ~4% marginal gains at ~19% cost overhead. Benefits materialize only with ruthlessly curated, project-specific content focused on non-derivable information. Apply Anthropic's diagnostic: **"Would removing this line cause the agent to make mistakes?"** If no, delete it.

### 2) Context Rot

- **Temporal rot**: stale dates, completed milestones shown as active.
- **Structural rot**: paths/symbols no longer exist.
- **Semantic rot**: old behavior descriptions now misleading.

### 3) Contradictions

- `AGENTS.md` and `CLAUDE.md` disagree on process or constraints.
- Tool-specific files duplicate shared conventions and drift over time.

### 4) Mixed Concerns

- Persistent docs contain progress logs/TODO status.
- "What the system is" and "how to run this task" are mixed in one file.

### 5) Redundancy

- Same rule appears in multiple files with slight wording differences.

### 6) Security Gaps

- Project handles user input, APIs, or data but instruction files include no security constraints.
- No input validation rules specified for user-facing endpoints.
- No secret management policy (e.g., "never commit .env files", "use environment variables").
- No dependency security expectations (e.g., "run audit before adding packages").
- Auth/authz rules absent for projects with authentication flows.

### 7) Missing Permission Boundaries

- Agent-facing instruction files lack always/ask-first/never permission tiers.
- No explicit boundary on destructive operations (force push, schema drops, file deletion).
- No approval gates for high-risk changes (dependency upgrades, CI/CD modifications).

### 8) Positional Burial

- Critical rules (security, permissions, breaking changes) buried in middle sections of long files.
- High-impact instructions nested inside low-priority subsections.
- "Must" / "never" constraints placed after optional style guidance.

### 9) Tone Overtriggering

- Aggressive capitalization ("YOU MUST NEVER", "ABSOLUTELY DO NOT") — causes model overtriggering.
- Excessive negation chains ("do not ever under any circumstances") — prefer clear positive directives.
- Triple emphasis or exclamation marks — moderate phrasing produces better instruction following.

### 10) Agentic Workflow Gaps

- **Missing checkpoints**: Instruction files describe multi-step workflows without "pause and validate" gates. Agents loop or proceed past errors without human review.
- **Missing decomposition**: Complex tasks described as single instructions ("Build a REST API") without intermediate steps. Agents perform better when instruction files break tasks into ordered stages.
- **Missing rollback guidance**: No instructions for what to do when an agentic step fails (revert? retry? escalate?). Agents may silently produce broken state.
- **Missing iteration markers**: No version or progress tracking in instruction files used across multi-turn sessions. Agents lose track of what was already attempted.

## Refactoring Patterns

### Extract and Point

Move long topic blocks to dedicated docs, then replace with:

`Read when: <trigger> -> docs/<topic>.md`

### Prune Completed Work

Remove completed items from active roadmaps. Keep history in archive docs.

### Resolve Contradictions

1. Confirm canonical source (usually `AGENTS.md`).
2. Update canonical file.
3. Remove or rewrite conflicting copies.

### Consolidate Redundancy

Keep shared rules in one canonical file and replace copies with references.

### Separate Temporal From Persistent

Move progress/changelog text out of persistent references.

## Practical Thresholds

| Metric | Target | Rationale |
|---|---|---|
| Lean target | <60 lines | HumanLayer and Anthropic's own examples (~20-60 lines); tightest practical files |
| Practical max (always-loaded) | <150 lines | Practitioner consensus across Anthropic, HumanLayer, Globant; context degrades with length |
| Split threshold | >200 lines | GitHub analysis of 2500+ repositories (2025) — modular files outperform monolithic |
| Single section length | <40 lines | Longer sections should use a `Read when:` split to a reference file |
| Freshness | Flag dates >30 days old | Unless marked with an explicit "still valid" annotation |
| Command variants | 1 default per task | Prefer one clear default command over many equivalent options |
| Reference depth | 1 level recommended, 5 max | Claude Code supports up to 5-hop `@path` imports; deeper chains risk partial-load misses |
| Prose-to-directive ratio | Prefer imperative directives | Flag files where explanatory prose dominates actionable instructions |

### Freshness Heuristics

- Dates in instruction files (deadlines, "as of" markers) older than 30 days: tag `context_rot` / `medium`.
- Completed milestones still listed as active: tag `context_rot` / `high`.
- File paths or symbol names referenced in instructions that no longer exist: tag `context_rot` / `high`.
- Dependency versions pinned in instructions that differ from lockfile: tag `context_rot` / `medium`.

