# Context Design Patterns

Patterns for designing instruction files that optimize model attention and support dynamic loading.

## Table of Contents

- Positional Optimization
- Dynamic Loading Tiers
- Format Guidance (XML vs Markdown)
- Constraint Ordering

## Positional Optimization

LLMs exhibit a U-shaped attention curve: strong primacy (beginning) and recency (end) bias, with degraded attention to middle content (Liu et al. 2023, "Lost in the Middle").

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

### Tier 1: On-demand modules (loaded via "Read when:" triggers)
Domain-specific rules loaded when the task matches.
Lives in: subdirectory instruction files, reference docs.

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

### When to use Markdown (default)
- Simple instruction files with clear section hierarchy
- Files under 100 lines
- Instructions that are primarily sequential (do this, then that)

### When to consider XML tags
- Complex instruction files with many interleaved categories (role + rules + examples + constraints)
- Files where section boundaries are ambiguous in Markdown
- Instruction files consumed by multiple different models/tools

XML tags create unambiguous boundaries that reduce model interpretation errors:

```xml
<security>
Validate all user input. Use parameterized queries.
</security>

<style>
Use camelCase for JS. Use snake_case for Python.
</style>
```

vs. Markdown where "## Security" and "## Style" rely on the model inferring boundaries.

### Recommendation
Use Markdown by default. Switch to XML tags only when Markdown headers create genuine ambiguity — usually in files >150 lines with complex conditional structure.

## Constraint Ordering

Within each instruction file, order constraints from hard to easy (arxiv:2502.17204).

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
