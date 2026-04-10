# Priority Resolution Framework

Resolve conflicts between coexisting instruction sources using these rules.

## Default Precedence (highest to lowest)

1. **System prompt / runtime injection** — immutable, set by the host tool
2. **Directory-local instruction file** (e.g., `src/api/CLAUDE.md`) — most specific scope
3. **Project-root instruction file** (e.g., `CLAUDE.md`, `AGENTS.md`, `.cursorrules`)
4. **Global / user-level instruction file** (e.g., `~/.claude/CLAUDE.md`)
5. **Skill-provided instructions** — lowest priority, overridden by all above

## Resolution Rules

### Specificity wins
A rule scoped to a subdirectory overrides the same rule at project root. A rule targeting a specific file type overrides a general coding-style rule.

### Explicit override beats implicit conflict
If two files contradict and neither declares precedence, flag as `contradiction`. Do not silently pick one.

### Last-writer awareness
When the same rule appears in multiple files with different wording, the most recently edited version is likely intentional — but confirm before assuming.

## Conflict Matrix Template

When auditing, build this matrix for each dimension of concern:

| Dimension | Canonical Owner | Override Allowed? | Notes |
|---|---|---|---|
| Code style | `AGENTS.md` | Yes, in subdirectory files | Subdirectory narrows, never contradicts |
| Security constraints | `AGENTS.md` § Security | No — must be consistent | Flag any weakening as `security_gap` |
| Testing rules | `AGENTS.md` § Testing | Yes, per-directory | E.g., integration tests in `api/`, unit in `lib/` |
| Permissions | `AGENTS.md` § Permissions | No — strictest wins | Never relax a `never` tier rule in an override |
| Tool-specific behavior | Tool-specific file (e.g., `CLAUDE.md`) | N/A | Should not duplicate shared rules |
| Build / run commands | `AGENTS.md` or `README.md` | Yes, per-directory | Monorepo subdirectories may have own commands |

## Audit Checklist

- [ ] Each instruction file declares its scope (project-wide, directory, tool-specific)
- [ ] No two files at the same precedence level contradict on the same dimension
- [ ] Security and permission rules are never weakened by lower-precedence files
- [ ] Tool-specific files (CLAUDE.md, .cursorrules) contain only tool-specific behavior, not duplicated shared rules
- [ ] When a conflict is detected, the resolution is documented in the canonical source
