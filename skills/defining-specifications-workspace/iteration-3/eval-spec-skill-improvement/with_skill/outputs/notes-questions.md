# Notes, Clarifying Questions, and Working Assumptions

Companion to `SPEC-defining-specifications-skill-improvement-2026-06-05.md`.

This run is **non-interactive** (evaluation context), so per the skill's Clarify step I record
clarifying questions and working assumptions here and in the spec, then proceed to a complete draft
instead of blocking. None of these questions were resolved by a human; the spec's `Open Questions`
are treated as blockers for the downstream implementing agent, not as resolved decisions.

## What I inspected (read-only)

- `skills/defining-specifications/SKILL.md` (v1.2) — full read.
- `skills/defining-specifications/references/requirements-and-acceptance-criteria.md` — full read.
- `skills/defining-specifications/references/spec-type-profiles.md` — full read.
- Directory listing of `skills/defining-specifications/` (also contains `evals/evals.json`).

No files were modified. The skill itself was not edited.

## Clarifying questions (would change scope / acceptance if answered)

1. **Scope of the rewrite** — Should improvements be strictly *additive* (new sections/reference
   files + small consistency fixes), or is a structural reorganization of `SKILL.md` in scope?
   Assumption: additive + targeted consistency fixes only (see ASM-001).
2. **New reference files** — Is it acceptable to add a worked end-to-end example spec as a new file
   under `references/`, or must everything stay inside `SKILL.md`? Assumption: new reference files
   are allowed and preferred to keep `SKILL.md` lean (ASM-002).
3. **Token/length budget** — Is there a target maximum length for `SKILL.md` (it is loaded into the
   agent context on every trigger)? Assumption: keep `SKILL.md` roughly its current size by pushing
   long content into `references/` (ASM-003).
4. **Methodology stability** — Are EARS + Given/When/Then locked in, or open to alternatives? Assumption:
   locked in; this spec strengthens their *application*, not the methodology (ASM-004).
5. **Self-review automation** — Is a scripted/machine-checkable self-review (e.g., a checklist the agent
   must emit, or a linter) desired, or is the prose checklist sufficient? Assumption: a structured,
   inspectable self-review is desired but a code/tooling deliverable is out of scope (ASM-005, NG-005).
6. **Versioning** — Should the improvement bump `metadata.version` (1.2 -> 1.3) and follow a changelog
   convention? Assumption: yes, bump to 1.3 and note changes (ASM-006).

## Working assumptions (carried into the spec)

- The audience optimization target is unchanged: AI coding agents as primary consumers, humans as reviewers.
- The skill's mission, operating principles, EARS/GWT conventions, and write boundaries are sound and
  should be preserved; this is a refinement, not a redesign.
- The improvement is implemented by a downstream agent editing the skill files; this spec does not edit them.

## Grounded defects / opportunities found in the current skill

These observations are derived directly from reading the current files and motivate the requirements:

- **D1 (inconsistency):** `Agent-Friendly Conventions` lists a `DEC-###` ID (SKILL.md line ~179), but the
  Default Spec Template has no `Decisions` section that would use it.
- **D2 (inconsistency):** The template's `Status` enum includes `Approved` and `Blocked` (line ~107), but
  the workflow only defines the `Draft -> Ready for Review` transition (line ~98); `Approved`/`Blocked`
  are never defined.
- **D3 (scattered guidance):** Non-interactive / autonomous behavior is described in three separate places
  (Clarify step line ~70, Outline step line ~81, and indirectly elsewhere) with no single canonical rule.
- **D4 (undefined terms):** The Clarify step keys question budgets to "Simple / Medium / Large" specs
  (lines ~66-68) but never defines those tiers.
- **D5 (no worked example):** `references/` contains only methodology snippets; there is no full,
  end-to-end example spec demonstrating the template + a profile + EARS + GWT + traceability together.
- **D6 (un-enforced traceability):** Traceability `REQ -> AC -> TEST` is described (line ~181 and the
  references) but there is no recommended at-a-glance traceability artifact for larger specs.
- **D7 (prose-only gate):** The Quality Checklist is a prose gate (lines ~188-203) with no structured,
  inspectable self-review output an agent (or grader) can verify mechanically.
- **D8 (output-path precedence):** The default save location `./docs/specs/` (line ~87) and "any requested
  output path" (line ~41) coexist without an explicit precedence rule when an assigned path is given.

## Decisions taken to keep the spec focused (YAGNI/KISS)

- Excluded building any tooling, linter, or CI to enforce the checklist (kept as instructions only).
- Excluded changing the trigger `description` or skill `name`.
- Excluded adding new spec *types* beyond the existing six profiles.
