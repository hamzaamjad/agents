---
name: engineering-context
description: >-
  Audits and remediates workspace instruction quality for agentic coding.
  Trigger when: (1) context cleanup, context rot, or documentation hygiene,
  (2) canonical instruction source maintenance (AGENTS.md, CLAUDE.md,
  .cursorrules, or host-specific equivalents), (3) contradiction,
  duplication, or staleness remediation across instruction files,
  (4) instruction file quality review or scoring, (5) setting up or
  auditing AGENTS.md or CLAUDE.md structure, (6) context window
  optimization or instruction prioritization, (7) permission boundary
  or security guardrail review in agent instruction files.
---

# Context Engineering

Treat instruction files as production interfaces: each edit should reduce model mistakes in future sessions.

## Principles

- **Hierarchy first**: Define precedence across instruction sources before editing. See [references/priority-resolution.md](references/priority-resolution.md).
- **Single source of truth**: Shared conventions live in one canonical source; other files point, not fork.
- **Positive directives**: Prefer "do X" over "do not do Y."
- **Grounding before generation**: Prefer evidence-linked edits over freeform policy synthesis.

## Workflow

### Scope selection (before starting)

Determine the audit scope:
- **(A) Single-file review**: skip Steps 1 and 6. Run the script on the target file, diagnose, fix, verify, report.
- **(B) Targeted fix**: skip Steps 1 and 6. Go directly to diagnose/fix/verify on the identified problem.
- **(C) Full workspace audit**: run all steps.
- **(D) No instruction files exist**: skip to scaffolding — propose an initial `AGENTS.md` using [references/agents-md-spec.md](references/agents-md-spec.md). Ask the user which sections are relevant before generating.

### Reference loading map

| Step | File | Condition |
|---|---|---|
| 1 | `references/priority-resolution.md` | Only when multiple instruction sources exist |
| 2 | `references/rubric.md` | Always — failure patterns and thresholds |
| 3 | `references/context-design-patterns.md` | Always — positional optimization, tiers |
| As needed | `references/agents-md-spec.md` | When auditing or creating AGENTS.md |

### Steps

1. **Inventory canonical context** (full audit only)
   - Run `scripts/validate_context.py <project-root>` to seed initial findings.
   - Read the highest-priority instruction sources (e.g., `AGENTS.md`, `CLAUDE.md`, system prompt files, or equivalent).
   - Read pointer/index docs and planning docs if they exist.
   - Discover rule/override surfaces (rules directories, host config files, override docs).
   - Map each file's purpose in one line before editing.
   - For monorepos: read root files first, then scan subdirectory files only in areas relevant to the user's concern. List discovered files and confirm scope with the user before loading all.
   - If multiple instruction sources coexist, read [references/priority-resolution.md](references/priority-resolution.md) and establish precedence.

2. **Diagnose with explicit tags**
   - Read [references/rubric.md](references/rubric.md) for the detailed failure-pattern rubric and refactoring patterns.
   - Tag each issue with one or more: `contradiction`, `context_rot`, `bloat`, `redundancy`, `mixed_concerns`, `missing_guardrail`, `positional_burial`, `missing_permissions`, `tone_overtrigger`, `missing_checkpoint`, `missing_decomposition`, `security_gap`.
   - Record impact: `high` (can cause wrong behavior), `medium` (causes ambiguity), `low` (style/noise).
   - Prioritize `contradiction`, `security_gap`, and `high` impact items first.

3. **Design the minimal fix**
   - Read [references/context-design-patterns.md](references/context-design-patterns.md) for positional optimization, dynamic loading tiers, and format guidance.
   - Prefer deletion or pointer replacement over rewriting large blocks.
   - Replace duplicated policy text with explicit pointers to canonical sources (for example: `Read when:` directives or equivalent conventions).
   - Keep durable rules in canonical sources; keep host-specific overlays as thin pointers.
   - Apply positional optimization: move critical rules (security, permissions, breaking-change warnings) to the first 20% of each file. Place supporting detail after. Avoid burying high-impact instructions in middle sections.
   - If unsure whether content is historical or active, move it to an archive note instead of deleting.

4. **Apply remediation**
   - Edit only files tied to diagnosed findings.
   - Keep instructions specific, measurable, and operational (who does what, when, where).
   - Add examples only for behaviors that repeatedly fail.
   - For projects handling data, APIs, or user input: verify instruction files include security constraints (input validation, auth rules, secret management, dependency security). Tag missing constraints as `security_gap` with `high` impact.

5. **Verify against acceptance checks**
   - Re-read all edited files.
   - Confirm all local file/path references exist.
   - Confirm index/pointer docs are pointer-first (not status/changelog narrative).
   - Confirm planning docs are forward-looking (completed detail archived).
   - Confirm no rule is duplicated across canonical sources unless intentionally mirrored.
   - Confirm constraint ordering: complex behavioral constraints (architecture, edge cases, security) before simple formatting/style rules.
   - Confirm instruction tone uses moderate, clear phrasing — no ALL CAPS directives or aggressive emphasis patterns (see references/rubric.md § Tone Overtriggering).

6. **Report**
   - **Scan mode** (no edits applied): Findings + Recommendations. Omit Applied Changes and Residual Risk.
   - **Audit mode** (edits applied): Findings, Applied Changes, Residual Risk, Next Pass.
   - If the audit surfaced a systemic workflow issue (not just a file issue), note one process improvement in the Next Pass section.

## Editing Rules

- Edit only files tied to diagnosed findings.
- Archive uncertain removals rather than deleting when history may matter.
- Preserve active in-progress temporal files.
- Confirm with the user before ambiguous removals.

## Quality Gate

Before considering the pass complete, all must be true:

- No contradiction between canonical instruction sources and host/runtime-specific overlays.
- Index/pointer docs contain pointers, not status/changelog narrative.
- Planning docs are forward-looking; completed detail is archived.
- No duplicated instruction exists across top-priority canonical sources.
- Critical instructions are positioned in the first 20% of each file, not buried in middle sections.
- Security-relevant projects include explicit security constraints in instruction files.
- Permission boundaries (always/ask-first/never) are defined for agent-facing instruction files.
- Instruction files under quantitative thresholds (see [references/rubric.md](references/rubric.md) § Practical Thresholds).
- At least one acceptance check verifies each high-impact fix.

## References

- [references/rubric.md](references/rubric.md) — failure patterns, refactoring patterns, thresholds. Read during Step 2 (Diagnose).
- [references/priority-resolution.md](references/priority-resolution.md) — precedence rules, conflict matrix. Read during Step 1 when multiple instruction sources exist.
- [references/agents-md-spec.md](references/agents-md-spec.md) — AGENTS.md structure and validation. Read when auditing or creating AGENTS.md files.
- [references/context-design-patterns.md](references/context-design-patterns.md) — positional optimization, dynamic loading tiers, format guidance. Read during Step 3 (Design).
