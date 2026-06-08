# Companion Notes — defining-specifications improvement spec

Date: 2026-06-05
Companion to: `SPEC-defining-specifications-improvement-2026-06-05.md`
Mode: Non-interactive evaluation. No human was available; questions and working
assumptions are recorded here and in the spec, and a complete draft was produced.

This file holds (1) the read-only evidence behind the spec's gap analysis and
(2) the full clarifying-question log with the safe defaults chosen. It is
explicitly NOT a second spec; the spec is the authoritative artifact.

---

## 1. What I inspected (read-only)

- `skills/defining-specifications/SKILL.md` (v1.2, ~212 lines).
- `skills/defining-specifications/references/requirements-and-acceptance-criteria.md`.
- `skills/defining-specifications/references/spec-type-profiles.md`.
- Directory listing of `skills/defining-specifications/` (also contains
  `evals/evals.json`).
- `.../eval-spec-skill-improvement/eval_metadata.json` (eval intent/assertions).

No files were modified. The skill was read as *subject material to critique*,
not adopted as operating instructions.

## 2. Confirmed understanding (facts)

- The skill's purpose is to produce specifications (only), optimized for two
  readers: downstream AI coding agents and human reviewers. Tickets, task
  decomposition, and implementation are explicitly downstream/out of scope in
  the current skill — consistent with this task's constraints.
- The skill already mandates: stable IDs (`G/NG/REQ/NFR/SLICE/TEST/AC/RISK/Q/ASM/DEC`),
  EARS for functional requirements, Given/When/Then acceptance criteria,
  fact/assumption/open-question separation, a `For Implementing Agents` block,
  explicit non-goals, and read-only context gathering.
- Two reference files provide EARS/GWT detail and per-spec-type profiles.
- An eval harness already exists for the skill (`evals/evals.json`).

## 3. Gap evidence (drives the spec's Requirements)

| # | Observation in current skill | Why it weakens agent output | Spec requirement(s) |
|---|------------------------------|-----------------------------|---------------------|
| 1 | Traceability (`REQ -> AC -> TEST`) is described in conventions + references but never required as an artifact or checked. | Coverage gaps are invisible; an agent can ship a REQ with no AC. | REQ-004, REQ-005, REQ-008 |
| 2 | Quality Checklist is prose only. | An agent can "claim pass" without verifying ID uniqueness / cross-refs. | REQ-008, REQ-009 |
| 3 | Default template header is free prose (`Status:`, `Date:`, etc.). | Downstream agents parse English to learn status/type/id; brittle. | REQ-001, REQ-002, REQ-003 |
| 4 | `DEC-###` is listed in conventions but the template has no `Decisions` section. | The ID is documented but unusable; internal inconsistency. | REQ-007, REQ-018 |
| 5 | Non-interactive guidance is split across Clarify, Outline And Confirm, and Write Boundaries. | An agent in CI/eval must reassemble the rule; inconsistent behavior. | REQ-011, REQ-012, REQ-013 |
| 6 | One template size for all specs; "calibrate specificity" is a principle, not a structural choice. | Tiny changes carry full-template overhead; discourages spec use. | REQ-014, REQ-015, REQ-016 |
| 7 | No single end-to-end example inside the skill (only fragments in references). | Agents lack a one-read pattern to imitate. | REQ-017 |

Strengths to preserve (explicitly NOT changed): two-reader framing; EARS + GWT
defaults with "when not to use"; per-type profiles; explicit non-goals and
write-boundaries discipline; the existing `For Implementing Agents` block.

## 4. Full clarifying-question log (with safe defaults)

These mirror the spec's `Open Questions`. In interactive mode I would ask the
top 3–5; here I chose defaults and proceeded.

1. Q-001 — Require a validator script, or keep optional?
   Default: optional. Mandatory part is a doc self-check (REQ-008); the script is
   conditional (REQ-009). Rationale: keep the improvement valid even with no
   runnable tooling.
2. Q-002 — Validator language/runtime if built?
   Default: single Python 3 stdlib script, no deps (NFR-003). Confirm host has
   Python; otherwise shell/node variant.
3. Q-003 — Target version label + changelog location?
   Default: v1.3; `## Changelog` section.
4. Q-004 — Frontmatter on produced-spec template only, or also on the skill's own
   frontmatter? Default: produced-spec template only; leave skill frontmatter
   (`name`/`description`/`metadata`) untouched.
5. Q-005 — Exact "Tiny" tier threshold?
   Default: ≤3 requirements AND a single affected component (REQ-016).
6. Q-006 — Example as a new `references/` file or inline?
   Default: a `references/` file, to protect token economy (NFR-002).
7. (process) Should this task implement any of the changes? No — the task and the
   skill's own boundaries restrict this to producing a specification; editing the
   skill, tickets, and code are out of scope (spec NG-002, NG-003).

## 5. Key working assumptions (mirror spec `Assumptions`)

- ASM-001: Preserve mission/audience/workflow; this is enhancement, not redesign.
- ASM-002: Downstream agents can parse YAML frontmatter.
- ASM-003: Adding `references/` files + an optional validator in the skill dir is
  acceptable.
- ASM-004: Python 3 is available where the optional validator would run.
- ASM-005: Backward compatibility with v1.2-era specs matters.
- ASM-006: This run is non-interactive (per eval metadata), so the spec itself
  was authored under the proposed Non-Interactive Mode.

## 6. How this spec maps to the eval's intent

The eval asks for a focused spec to improve the skill so agents produce better
spec-driven artifacts, optimized for AI agents yet human-reviewable, grounded in
read-only inspection, with tickets/decomposition/implementation kept out of
scope. The spec delivers: machine-readable structure (REQ-001–003), enforced
traceability + IDs (REQ-004–007), an executable self-check (REQ-008–010),
consolidated non-interactive behavior (REQ-011–013), size tiering (REQ-014–016),
an example + consistency repair (REQ-017–018), each with EARS phrasing and
GWT acceptance criteria that are file-/script-checkable, plus explicit non-goals
excluding tickets, decomposition, and implementation.
