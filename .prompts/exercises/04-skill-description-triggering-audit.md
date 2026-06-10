# Exercise 4: Skill-description triggering audit

Usage: paste into a fresh agent session with `~/.agents` as the workspace root.
Sequencing: independent of the other exercises. If `AGENTS.md` exists at the repo root, follow its conventions for where to save the audit artifacts.

## Goal

Audit and tune the six frontmatter `description` fields in `skills/*/SKILL.md` for triggering precision and recall, validated against a written probe set. The description is the routing prompt that decides whether a skill activates at all: a skill that never fires is worth zero, and one that fires on everything pollutes sessions.

## Required skills

- `skills/engineering-prompts/SKILL.md`, run as a prompt audit (mode 4). Treat each description as a prompt whose target "model" is the host's skill router, and apply the anti-pattern library — in particular the guidance against aggressive trigger language on recent Claude models.
- The skill-creator skill (Claude plugin cache, `example-skills/.../skill-creator/SKILL.md`) for its description-optimization guidance and any description length limits, if reachable.

## Method requirements

- Build the probe set before touching any description. Per skill: 4-6 positive messages (should trigger) and 3-4 hard negatives (plausible but should not trigger). Add shared collision probes — messages that two descriptions could both claim. Cover at least these known collision surfaces:
  - defining-specifications vs ticket-workflow: spec-first vs decompose-first requests ("plan out this feature for me").
  - engineering-context vs engineering-prompts: both claim context-engineering territory — the prompts skill carries a CONTEXT_ENGINEERING reference while the context skill owns instruction-file auditing.
  - hamza-voice breadth: "draft an email/message" currently triggers regardless of stakes — test trivial transactional messages as hard negatives.
  - session-retrospective vs engineering-context: post-session improvement vs instruction-file audit.
- Evaluate every probe against the current descriptions and record a verdict matrix: probe by skill, trigger yes/no, with the deciding phrase from the description.
- Rewrite only descriptions with demonstrated precision or recall failures. Preserve trigger phrases that match how the user actually asks. Respect any host length limits found in the skill-creator guidance. Use plain imperative phrasing — no stacked emphasis.
- Where two skills legitimately border each other, encode the disambiguation in both descriptions, the way defining-specifications already carves out ticket decomposition.
- Re-run the same probe matrix against the rewritten descriptions.

## Deliverables

- The probe set and both verdict matrices (before and after), saved as a single audit report file in the location AGENTS.md prescribes, or alongside the skills if no convention exists.
- Edited `description` frontmatter only — no skill-body edits.
- Report: per-skill diagnosis naming the offending phrase for each failure, changes made, and residual collisions accepted by design with rationale.

## Definition of done

- Every description change traces to a specific failed probe; no speculative rewording.
- The after-matrix shows no lost positive triggers for engineering-context, engineering-prompts, ticket-workflow, or defining-specifications.
- At least one collision or hard-negative failure is resolved overall, or the report explains why the current boundaries are already optimal.
- Frontmatter remains valid YAML in every edited file.
- Changes committed, one commit per skill or one for the full audit; nothing pushed.
