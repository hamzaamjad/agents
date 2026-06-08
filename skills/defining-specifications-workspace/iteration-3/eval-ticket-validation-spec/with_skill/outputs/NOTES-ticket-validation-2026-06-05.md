# Companion Notes — Ticket Validation Spec

Date: 2026-06-05
Companion to: `SPEC-ticket-validation-2026-06-05.md`
Purpose: Capture the read-only context-inspection trail and the clarifying questions that would normally be asked interactively. This run is non-interactive, so per the `defining-specifications` skill these are recorded here and as `Q-###` in the spec, and the spec proceeds on stated provisional defaults rather than blocking.

## Context Inspection Log (read-only)

What I read and the concrete facts each source established:

1. `skills/defining-specifications/SKILL.md` + `references/requirements-and-acceptance-criteria.md` + `references/spec-type-profiles.md` — the skill being exercised. Drove: default template, EARS requirements, Given/When/Then acceptance criteria, REQ→AC→TEST traceability, and the choice to compose the **Feature/new capability** and **Agent handoff / process or skill spec** profiles.
2. `skills/ticket-workflow/SKILL.md` — directory layout, naming, type-prefix table, status lifecycle, dependency ID resolution rule (bare IDs resolve within the current epic; no global fallback; must fail otherwise), required frontmatter (`id, title, type, status`), and the execution-time dependency gate ("if any dependency status != done, STOP").
3. `skills/ticket-workflow/references/templates.md` — per-type frontmatter fields; established that TASK `parent` is "required — cannot be empty" and TASK `complexity` is "required", the `priority` enum, and the EPIC `branch` field.
4. `skills/ticket-workflow/references/outcome-schema.md` — `done` tickets must carry `## Outcome`, with the temporal qualifier "from the point FEAT-003 lands" (source of Q-004).
5. `skills/ticket-workflow/references/complexity-scoring.md` — `complexity` is an integer 1–10; confirmed it is a field a validator could presence-check but not meaningfully range-check beyond 1–10.
6. `skills/ticket-workflow/scripts/archive-search.sh` — the only existing ticket tool. Established in-repo conventions (bash, `set -euo pipefail`, awk frontmatter/section extraction, safe-on-missing-dir → exit 0). Source of ASM-005 and several technical-context notes.
7. `.gitignore` — `.tickets/` is git-ignored as a per-workspace artifact. Critical: a committed-file CI gate cannot see tickets (drives Q-003, ASM-006, RISK-003). Also shows Python tooling caches, which is why Q-001 (bash vs Python) is genuinely open.
8. Filesystem check — `.tickets/` does not currently exist in this workspace; the validator must be safe on an empty/fresh tree (REQ-002, NFR-002), exactly like `archive-search.sh`.

No files outside the spec output directory were created, modified, or deleted.

## Clarifying Questions I Would Have Asked (and the provisional answer used)

Grouped by theme; full canonical list is in the spec's `Open Questions`.

Build/packaging:
- Language: bash or Python? → Provisional **bash** (ASM-005), because it mirrors the only existing tool and avoids a YAML dependency; flagged because Python would make cycle detection and robust YAML parsing easier (Q-001).
- Script path/name and whether to wire it into `ticket-workflow/SKILL.md`? → Provisional `skills/ticket-workflow/scripts/validate-tickets.*` (Q-002).

Invocation/enforcement:
- Manual CLI, agent pre-flight, or git hook? Is a CI gate even wanted given `.tickets/` is git-ignored? → Provisional: documented CLI + agent pre-flight; defer hooks (Q-003).

Rule severity/scope:
- Is missing `## Outcome` on a `done` ticket an error or warning, and are pre-FEAT-003/archived tickets exempt? → Provisional **warning** (TV-LC-001, ASM-007, Q-004).
- Deep-validate the `## Outcome` 7-subsection schema, or presence only? → Provisional **presence only** (NG-007, Q-005).
- Validate `created`/`updated` date format and ordering? → Provisional **out of scope** (Q-006).
- Full schema validation on archived tickets, or only the archive invariant + reference integrity? → Provisional **lighter set** (ASM-008, Q-007).
- Include `ticket-workflow` quality lints (size, ≤5 acceptance criteria, `## Verification` present) as warnings? → Provisional **out of scope** (NG-005, Q-008).
- Epic `branch:` missing/malformed — error or warning? → Provisional **warning** (TV-FM-004, Q-009).

## Spec-Type Profile Decision

Composed two profiles from `references/spec-type-profiles.md`:
- **Feature / new capability** — drove explicit early `Non-Goals`, user-observable `Proposed Behavior`, and at least one negative-case acceptance criterion per error path.
- **Agent handoff / process or skill spec** — drove the lead `Source Context` + `For Implementing Agents` block, the "Open Questions are blockers, not guesses" framing, and acceptance criteria that are checkable by scripted/file inspection (exit codes, emitted diagnostic codes, byte-identical reruns).

## Open Risk to Flag to a Human

The single highest-leverage unresolved decision is Q-003 combined with ASM-006: because `.tickets/` is git-ignored, this validator cannot function as a traditional committed-file CI gate. If the intent was "block bad tickets in CI," that assumption needs to be revisited before implementation, since it may require tracking tickets or running the check against the working tree in a non-standard CI step.
