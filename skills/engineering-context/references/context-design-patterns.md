# Context Design Patterns

Apply these patterns to optimize model attention and support dynamic loading in instruction files.

## Cumulative Context Degradation (Context Rot)

Length itself degrades attention quality independently of position. Research (Chroma/Morphllm 2025, Maximum Effective Context Window studies) shows all frontier models degrade as context grows — even when relevant information is isolated and the model is forced to attend only to it. Some models show catastrophic collapse at specific thresholds (e.g., F1 drops from 0.55 to 0.30 over a 10% context range).

**Implication**: the first lever for improving instruction following is *reducing total length*, not just repositioning content. Every line you keep must earn its presence.

## Positional Optimization

Within the length you keep, position matters. Models exhibit strong primacy and recency bias, with degraded attention to middle content. This is a secondary lever; reduce length first, then optimize positioning.

### Placement Rules

1. **First 20% of each file**: security constraints, permission boundaries, breaking-change warnings, "never" rules
2. **Next 30%**: core workflow steps, architectural patterns, behavioral constraints
3. **Next 30%**: style guides, formatting preferences, supporting detail
4. **Final 20%**: examples, edge cases, reference pointers

### Detection

Flag as `positional_burial` when:
- A "must" or "never" rule appears after line 60% of the file
- Security constraints appear in a subsection nested under style/formatting
- Permission boundaries are at the end of a file

## Dynamic Loading Tiers

Design instruction files as a tiered system, not a monolith. Inspired by Karpathy's framing: "the LLM is a CPU, the context window is RAM, you are the OS."

### Tier 0: Always-loaded core (~100-150 lines)
Project identity, critical constraints, pointers to deeper context.
Lives in: `CLAUDE.md`, `AGENTS.md`, `.cursorrules` (project root)

**Include**: project purpose (1-2 sentences), tech stack, critical "never" rules, security constraints, permission boundaries, pointers to on-demand modules.

**Exclude**: detailed style guides, architecture deep-dives, historical context.

### Tier 1: On-demand modules
Domain-specific rules loaded when the task matches. Lives in: subdirectory instruction files, reference docs.

**Loading mechanisms**:
- `@path/to/file.md` syntax — Claude Code officially supports recursive imports up to 5 hops (see [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)). Prefer this for Claude Code workspaces.
- `Read when: <trigger>` directive — portable across tools, readable as prose.
- Subdirectory instruction files (e.g., `api/CLAUDE.md`) — auto-loaded when working in that directory.

**Examples**:
- `api/CLAUDE.md` — API-specific patterns, loaded when working in `api/`
- `references/testing.md` — test framework rules, loaded when writing tests
- `references/security.md` — security checklist, loaded when touching auth/data flows

### Tier 2: Session-scoped context
Current task state, recent decisions, iteration progress.
Lives in: plan files, session notes, git history.

**Include**: current blockers, decisions made this session, files already attempted.

**Exclude**: this content should NOT live in instruction files — it belongs in ephemeral session artifacts.

### Design Checklist

- [ ] Always-loaded files contain only what cannot be deferred
- [ ] Each on-demand module has a clear trigger condition documented in the always-loaded file
- [ ] No session-scoped content in persistent instruction files
- [ ] Subdirectory instruction files narrow scope; they never broaden or contradict root-level rules

## Format Guidance

Use Markdown by default. Consider XML tags when instruction files exceed 150 lines with many interleaved categories (role + rules + examples + constraints), where Markdown section boundaries become ambiguous.

## Constraint Ordering

Within each instruction file, order constraints from hard to easy. Models follow complex constraints better when they appear before simple ones.

### Hard constraints (place first)
- Architectural patterns and invariants
- Security requirements
- Edge-case handling rules
- Permission boundaries

### Easy constraints (place after)
- Naming conventions
- Formatting preferences
- Comment style
- Import ordering
