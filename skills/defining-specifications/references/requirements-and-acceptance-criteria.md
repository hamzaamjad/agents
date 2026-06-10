# Requirements And Acceptance Criteria

Read this when writing the `Requirements` and `Acceptance Criteria` sections of a spec. The goal is requirements an implementing agent can turn into code and tests without guessing, and acceptance criteria a grader can check without interpretation.

## Why this matters

A spec's requirements are a contract. Vague requirements ("handle errors", "make it fast") force the downstream agent to invent behavior, which is where hallucinated logic and silent scope creep come from. Two lightweight conventions remove most of that ambiguity: EARS for the requirement sentence, and Given/When/Then for the check that proves it.

## EARS: a default shape for functional requirements

EARS (Easy Approach to Requirements Syntax) constrains a requirement into a predictable clause order: optional preconditions, optional trigger, the system name, then `shall` plus the response. The keywords (`While`, `When`, `If/Then`, `Where`) tell both a human and an agent exactly what kind of behavior this is. Use `shall` for normative requirements so they are not mistaken for commentary.

Pick the pattern that matches the behavior:

| Pattern | When to use | Template |
|---------|-------------|----------|
| Ubiquitous | Always-on behavior, no trigger | `The <system> shall <response>.` |
| State-driven | Active while a state holds | `While <precondition>, the <system> shall <response>.` |
| Event-driven | Response to a trigger/event | `When <trigger>, the <system> shall <response>.` |
| Optional-feature | Behavior only when a feature is present | `Where <feature is included>, the <system> shall <response>.` |
| Unwanted-behavior | Handling errors / undesired input | `If <trigger>, then the <system> shall <response>.` |
| Complex | Combine the above | `While <precondition>, when <trigger>, the <system> shall <response>.` |

Keep the existing `REQ-###` (and `NFR-###`) IDs. EARS describes the sentence shape; the ID makes it referenceable. Example: `REQ-007: When a dependency reference cannot be resolved within the current epic, the validator shall emit an error-severity diagnostic naming the unresolved ID.`

### When NOT to force EARS

EARS is the default, not a straitjacket. Reach for a clearer form when a single sentence would distort the requirement:

- More than ~3 preconditions, or deeply nested conditions -> use a decision table or a small truth table.
- Quantitative relationships or formulas -> state the formula or thresholds directly (this is common for NFRs).
- Structured data shapes (schemas, payloads, config keys) -> use a JSON/YAML block or a table.

When you move logic into a table or block, keep a short EARS sentence that references it (e.g. `The validator shall classify diagnostics by severity per the table in "Diagnostic Model".`).

## Acceptance criteria: Given/When/Then, mapped to requirements

Write acceptance criteria as Given/When/Then (GWT) scenarios. GWT forces a concrete context, a concrete action, and an *observable* outcome, which is exactly what a test or a grader needs. Each criterion keeps its `AC-###` ID and names the requirement(s) it verifies, so traceability runs `REQ -> AC -> TEST`.

```markdown
- AC-001 (verifies REQ-007):
  - Given an epic containing TASK-001 with `dependencies: [FEAT-999]` and no FEAT-999 in that epic,
  - When the validator runs,
  - Then it exits non-zero and prints one error naming `FEAT-999` as unresolved.
```

Guidelines:

- Outcomes must be observable: a file written, an exit code, a value returned, a visible state, a logged event. Avoid "the user is happy" or "it works correctly".
- Cover the unwanted-behavior path, not just the happy path. If a requirement uses `If/Then`, it should have a matching negative-case AC.
- Prefer one assertion per criterion. If a scenario needs three Thens, it is probably three criteria.
- For UI/visual work, a screenshot diff or a described end state is an acceptable observable outcome.

## Traceability

For any non-trivial spec, every `REQ-###` should be reachable from at least one `AC-###`, and acceptance criteria should map to entries in `Testing And Verification` (`TEST-###`). A requirement with no acceptance criterion is either untestable (rewrite it) or out of scope (move it to Non-Goals). This mapping is what lets a downstream agent know when it is actually done. The same rule applies to `NFR-###`: every NFR needs at least one AC, or an explicit waiver recorded in the spec ("verified by inspection" plus a one-line rationale).

## Worked contrast (good vs weak)

**Requirement**

- Weak: `The system should handle invalid tickets gracefully.`
- Strong: `If a ticket file has missing or malformed YAML frontmatter, then the validator shall report a TV-FM-001 error with the file path and skip graph rules for that file.`

**Acceptance criterion**

- Weak: `Invalid tickets are detected.`
- Strong: `AC-003 (verifies REQ-002): Given a ticket file whose frontmatter is not valid YAML, When the validator runs, Then it emits exactly one TV-FM-001 error referencing that path and the process exits with code 1.`

**Non-goal**

- Weak: `We won't do everything.`
- Strong: `NG-002: The validator does not mutate, repair, or reformat ticket files; it is read-only.`

A good non-goal names a specific tempting behavior and excludes it. These are high-leverage guardrails because they stop an eager implementing agent from expanding scope.
