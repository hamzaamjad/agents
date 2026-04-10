# AGENTS.md Standard Structure and Validation

AGENTS.md is a portable, tool-agnostic instruction file for AI coding agents. Donated to the Agentic AI Foundation (Dec 2025) by OpenAI and Anthropic. Functions as "a README for agents."

## Standard Sections

### 1. Project Overview (required)
One sentence: what this project is, tech stack, key architectural decisions.

### 2. Key Commands (required)
Enumerated commands the agent needs: install, dev server, build, test, lint.
One default per task — avoid listing multiple equivalent options.

### 3. Project Structure (required)
Directory map with one-line descriptions. Pointers to key entry points.

### 4. Code Style (recommended)
Representative code snippets over abstract rules. Let agents infer patterns from examples.

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
- [ ] Code style uses examples, not just prose descriptions
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

## Multi-Agent Considerations

When a project uses multiple specialized agents (planner, coder, reviewer, tester):

- Define agent boundaries: which agent owns which task type
- Specify handoff protocols: what artifacts pass between agents
- Scope context per agent role: planners see architecture, coders see implementation, reviewers see diffs
- Document which instruction files each agent role should read
