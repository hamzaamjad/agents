# AGENTS.md Validation

Validate and structure AGENTS.md files using these standard sections and checks.

## Critical Warning

Empirical evidence (ETH Zurich, Feb 2026, 438-task benchmark across Claude Code and GPT models) shows that **poorly curated AGENTS.md files reduce task success by ~3% while increasing inference costs by >20%**. Even human-written files provide only ~4% marginal gains. Include a line only if removing it would cause the agent to make mistakes. Default toward deletion.

## Standard Sections

### 1. Project Overview (required)
One sentence: what this project is, tech stack, key architectural decisions.

### 2. Key Commands (required)
Enumerated commands the agent needs: install, dev server, build, test, lint.
One default per task — avoid listing multiple equivalent options.

### 3. Project Structure (required)
Directory map with one-line descriptions. Pointers to key entry points.

### 4. Code Style (often unnecessary)
Prefer enforcing style via linters, formatters, and type checkers rather than documenting it here. Modern LLMs learn style from existing code without explicit guidance. Include only non-obvious conventions that tooling cannot enforce.

### 5. Architecture Patterns (recommended)
Non-obvious patterns with mechanism descriptions. Explain *why* the pattern exists, not just *what* it is.

### 6. Testing Rules (recommended)
Test framework, naming conventions, coverage expectations, where tests live.

### 7. Permission Boundaries (recommended)

Three tiers:

**Always** — agent may do unconditionally:
- Run linting before commits
- Write human-authored commit messages
- Run tests

**Ask first** — requires explicit human approval:
- Database schema modifications
- Dependency additions/upgrades
- CI/CD pipeline changes
- API contract changes

**Never** — hard boundaries:
- Commit secrets or credentials
- Force push to main/protected branches
- Modify auth/security code without review
- Delete production data or resources

## Validation Checklist

- [ ] File exists at project root as `AGENTS.md`
- [ ] Project overview is present and under 3 sentences
- [ ] At least install and test commands are documented
- [ ] Project structure section maps all top-level directories
- [ ] Code style section is absent, minimal, or only covers conventions linters cannot enforce
- [ ] Permission boundaries are defined (even if minimal)
- [ ] File is under 200 lines (split to subdirectory files if over)
- [ ] Critical rules are in the first 30 lines
- [ ] No tool-specific content (that belongs in CLAUDE.md/.cursorrules)
- [ ] No session-scoped content (progress logs, TODO status)

## When To Split

Split AGENTS.md into modular files when:
- File exceeds 200 lines
- Project is a monorepo with distinct subdirectories
- Different subsystems have conflicting conventions

Pattern:
```
AGENTS.md              (root: shared standards, pointers)
src/api/AGENTS.md      (API-specific patterns)
src/frontend/AGENTS.md (frontend-specific patterns)
```

Subdirectory files narrow scope. They never broaden or contradict root rules.

