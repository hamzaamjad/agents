---
name: engineering-context
description: >-
  Audits and remediates workspace instruction quality for agentic coding.
  Trigger when: (1) context cleanup, context rot, or documentation hygiene,
  (2) canonical instruction source maintenance (AGENTS.md, CLAUDE.md,
  .cursorrules, README-agent.md, or host-specific equivalents),
  (3) contradiction, duplication, or staleness remediation across instruction
  files, (4) "agent is confused" / "too much context" / "workspace is noisy",
  (5) instruction file review or quality scoring, (6) setting up or auditing
  AGENTS.md or CLAUDE.md structure, (7) context window optimization or
  instruction prioritization, (8) permission boundary or security guardrail
  review in agent instruction files.
---

# Context Engineering

Treat instruction files as production interfaces: each edit should reduce model mistakes in future sessions.

## Principles

- **Clarity over cleverness**: Write explicit, directly actionable instructions.
- **Instruction hierarchy is explicit**: Define precedence and conflict handling across instruction sources before editing.
- **Structure matters**: Separate role/rules/examples/context with clear headings and tags where useful.
- **Positive directives**: Prefer "do X" to long lists of "do not do Y."
- **Few-shot for tricky behaviors**: Add compact examples for repeated failure modes.
- **Single source of truth**: Shared conventions live in one canonical source (or a clearly ordered canonical set); other files should point, not fork.
- **Grounding before generation**: Prefer evidence-linked or retrieval-backed edits over freeform policy synthesis.
- **Forward-only planning**: Planning docs stay future-focused; completed detail moves to history/archive.
- **Evaluate changes**: Use concrete acceptance checks after edits, not intuition alone.

## Workflow

Run this sequence:

1. **Inventory canonical context**
   - Read the highest-priority instruction sources (e.g., `AGENTS.md`, `CLAUDE.md`, `README-agent.md`, system prompt files, or equivalent).
   - Read pointer/index docs and planning docs (e.g., `docs/INDEX.md`, `docs/ROADMAP.md`) if they exist.
   - Discover rule/override surfaces (e.g., rules directories, host config files, override docs, or policy sidecars).
   - Map each file's purpose in one line before editing.
   - If multiple instruction sources coexist, read [references/priority-resolution.md](references/priority-resolution.md) and establish precedence before proceeding.

2. **Diagnose with explicit tags**
   - Read [reference.md](reference.md) for the detailed failure-pattern rubric and refactoring patterns.
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
   - Confirm constraint ordering within each file: complex behavioral constraints (architecture, edge cases, security) before simple formatting/style rules. Models follow hard-to-easy ordering better (arxiv:2502.17204).
   - Confirm instruction tone uses moderate, clear phrasing — no ALL CAPS directives or aggressive emphasis patterns (see reference.md § Tone Overtriggering).

6. **Run a micro-retrospective (from session-retrospective)**
   - Capture at least one friction point from this pass.
   - State one transferable prompting/workflow improvement for future sessions.
   - Propose at most two concrete workspace improvements with file targets.

7. **Report in strict order**
   - Findings (severity-sorted, with file references)
   - Applied changes
   - Residual risks
   - Optional next pass (narrow, high-leverage only)

## Editing Rules

- Do not make opportunistic rewrites outside identified findings.
- Archive uncertain removals instead of deleting when history may matter.
- If active in-progress temporal files exist, do not prune them blindly.
- If a requested removal is ambiguous, ask before destructive cleanup.

## Quality Gate

Before considering the pass complete, all must be true:

- No contradiction between canonical instruction sources and host/runtime-specific overlays.
- Index/pointer docs contain pointers, not status/changelog narrative.
- Planning docs are forward-looking; completed detail is archived.
- No duplicated instruction exists across top-priority canonical sources.
- Critical instructions are positioned in the first 20% of each file, not buried in middle sections.
- Security-relevant projects include explicit security constraints in instruction files.
- Permission boundaries (always/ask-first/never) are defined for agent-facing instruction files.
- Instruction files under quantitative thresholds (see [reference.md](reference.md) § Practical Thresholds).
- At least one acceptance check verifies each high-impact fix.
- Output includes one retrospective friction point and one concrete prevention action.

## Output Contract

Return results in this order:

1. **Findings**: severity-sorted with file references.
2. **Applied changes**: concise list of edits.
3. **Residual risk**: what remains and why.
4. **Optional next pass**: narrow recommendations only.

## Automated Validation

Run `scripts/validate_context.py <project-root>` for deterministic checks before manual review. Covers: file size thresholds, broken references, stale dates, duplicate headings, missing permissions, positional burial, tone patterns. Use output to seed Step 2 (Diagnose) findings.

## Anti-Patterns To Reject

- Large instruction dumps copied across multiple files
- Persistent docs containing week-by-week status logs
- Vague policy like "follow best practices" without examples or checks
- Conflicting precedence rules across canonical sources, overlays, and skill files
- Cleanup passes with no verification step

## References

- [reference.md](reference.md) — failure-pattern rubric, refactoring patterns, document roles, verification checklist. Read during Step 2 (Diagnose).
- [references/priority-resolution.md](references/priority-resolution.md) — precedence rules and conflict matrix for multi-source instruction files. Read during Step 1 when multiple instruction sources exist.
- [references/agents-md-spec.md](references/agents-md-spec.md) — AGENTS.md standard structure and validation. Read when auditing or creating AGENTS.md files.
- [references/context-design-patterns.md](references/context-design-patterns.md) — dynamic loading tiers, positional optimization, format guidance. Read during Step 3 (Design).
