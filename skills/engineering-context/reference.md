# Engineering Context Reference

Detailed rubric for deep context audits.

## Failure Patterns

### 1) Bloat and Verbosity

- Instruction files exceed practical size and attention budget.
- Explanations repeat what code or linters already enforce.
- Large static reference material is embedded instead of linked.

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

## Document Roles

- `AGENTS.md`: canonical cross-tool project conventions.
- `CLAUDE.md`: thin tool-specific overlay or pointer.
- `docs/INDEX.md`: pointer map only.
- `docs/ROADMAP.md`: forward-looking initiatives and intake.
- `docs/archive/*`: historical completion detail.

## Portability Guidance

- Keep shared conventions in `AGENTS.md`.
- Keep tool-specific behavior in tool-specific files only.
- Prefer pointers over duplicate prose across tools.

## Practical Thresholds

- Keep always-loaded instruction files lean.
- Prefer one clear default command over many equivalent options.
- Keep references one level deep to avoid partial-loading misses.

## Extended Verification Checklist

- [ ] No contradictory guidance across instruction files.
- [ ] No completed-work tracking in active roadmap docs.
- [ ] No status/changelog narrative in `docs/INDEX.md`.
- [ ] No broken file references in instruction docs.
- [ ] No leftover temporary override files (for example `AGENTS.override.md`).
- [ ] `CLAUDE.md` remains a pointer/thin overlay, not a second AGENTS clone.
- [ ] High-risk instructions are placed in obvious top-level sections.
