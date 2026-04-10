---
name: engineering-context
description: >-
  Audits and remediates workspace instruction quality for agentic coding.
  Use when reducing context bloat, resolving contradictory guidance, or
  tightening instruction reliability across canonical docs, rules, and skills.
---

# Context Engineering

Use this skill to keep instruction context high-signal, testable, and non-contradictory.
Treat instruction files as production interfaces: each edit should reduce model mistakes in future sessions.

## When To Use

Trigger this skill when the user asks for any of:

- context cleanup, context rot cleanup, or documentation hygiene
- canonical instruction source maintenance (for example: `AGENTS.md`, `CLAUDE.md`, `README-agent.md`, or host-specific equivalents)
- contradiction, duplication, or staleness remediation across instruction files
- "agent is confused" / "too much context" / "workspace is noisy"

## Provider + Research-Aligned Principles

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

2. **Diagnose with explicit tags**
   - Tag each issue with one or more: `contradiction`, `context_rot`, `bloat`, `redundancy`, `mixed_concerns`, `missing_guardrail`.
   - Record impact: `high` (can cause wrong behavior), `medium` (causes ambiguity), `low` (style/noise).
   - Prioritize `contradiction` and `high` impact items first.

3. **Design the minimal fix**
   - Prefer deletion or pointer replacement over rewriting large blocks.
   - Replace duplicated policy text with explicit pointers to canonical sources (for example: `Read when:` directives or equivalent conventions).
   - Keep durable rules in canonical sources; keep host-specific overlays as thin pointers.
   - If unsure whether content is historical or active, move it to an archive note instead of deleting.

4. **Apply remediation**
   - Edit only files tied to diagnosed findings.
   - Keep instructions specific, measurable, and operational (who does what, when, where).
   - Add examples only for behaviors that repeatedly fail.

5. **Verify against acceptance checks**
   - Re-read all edited files.
   - Confirm all local file/path references exist.
   - Confirm index/pointer docs are pointer-first (not status/changelog narrative).
   - Confirm planning docs are forward-looking (completed detail archived).
   - Confirm no rule is duplicated across canonical sources unless intentionally mirrored.

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
- Critical instructions are easy to find (top-level sections, not buried).
- At least one acceptance check verifies each high-impact fix.
- Output includes one retrospective friction point and one concrete prevention action.

## Output Contract

Return results in this order:

1. **Findings**: severity-sorted with file references.
2. **Applied changes**: concise list of edits.
3. **Residual risk**: what remains and why.
4. **Optional next pass**: narrow recommendations only.

## Anti-Patterns To Reject

- Large instruction dumps copied across multiple files
- Persistent docs containing week-by-week status logs
- Vague policy like "follow best practices" without examples or checks
- Conflicting precedence rules across canonical sources, overlays, and skill files
- Cleanup passes with no verification step

## References

Use these as operating guidance when refining this skill:

- **Model provider guidance (skills/instructions)**
  - OpenAI docs: prompt guidance + instruction hierarchy + agent reliability patterns
  - Anthropic prompt engineering guidance: system prompts, XML/tag structuring, examples, and edge-case handling
  - Cursor docs: rules/skills best practices (focused rules, canonical pointers, iterative rule growth)
- **Open standards**
  - Agent Skills open standard (`agentskills.io`) for portable skill structure
- **Academic context-engineering foundations**
  - Chain-of-Thought Prompting (Wei et al., 2022): explicit intermediate reasoning structure
  - ReAct (Yao et al., 2023): reasoning + action loops for tool-grounded behavior
  - Retrieval-Augmented Generation (Lewis et al., 2020): retrieval-backed grounding for factual reliability
  - Self-Refine (Madaan et al., 2023): iterative critique-refine loops
  - Reflexion (Shinn et al., 2023): retrospective verbal feedback and memory for error reduction
