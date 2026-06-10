# Specification: defining-specifications skill v1.3

Status: Approved (2026-06-10, Hamza via orchestrator proxy at the Phase A checkpoint)
Date: 2026-06-10
Owner/Requester: Hamza Amjad
Primary Consumers: AI coding agents executing this change via ticket-workflow; human reviewer at checkpoints
Source Context: see Source References

## For Implementing Agents

- Authoritative sections: Requirements, Nonfunctional Requirements, Non-Goals, Decisions, Acceptance Criteria. Implementation Slices are advisory sizing hints; the epic decomposition governs.
- Open Questions are blockers to surface, not guess. Q-001 and Q-002 were resolved at the Phase A checkpoint (DEC-003, DEC-004).
- Assumptions are unconfirmed; if one fails during implementation, stop and report rather than improvising.
- All file paths are relative to the repo root (`~/.agents`). The only files the epic may modify or create: `skills/defining-specifications/SKILL.md`, `skills/defining-specifications/evals/evals.json`, a new fixture under `skills/defining-specifications/evals/fixtures/`, plus ticket-workflow runtime artifacts (`.tickets/`, `.prompts/orchestration/`). The Q-001 repo-policy changes (`.gitignore`, `AGENTS.md` layout, decision memo) were committed on main before epic creation per DEC-003/DEC-004.

## Summary

Ship v1.3 of the `defining-specifications` skill, resolving the five gaps surfaced by the iteration-3 benchmark: an orphan `DEC-###` ID convention with no template section, a `Status` field whose `Approved` and `Blocked` values have no entry/exit rules, undefined Simple/Medium/Large tiers behind the Clarify question budgets, no inline worked example, and a confounded eval (eval-1) whose subject already embodies the conventions under test.

All five are small, local edits to one skill plus its eval set. The change keeps the template structure stable, stays within the 300-line budget for `SKILL.md`, and bumps the skill version to 1.3.

## Problem Statement

Iteration-3 benchmarking (`skills/defining-specifications-workspace/iteration-3/benchmark.md`) shows v1.2 reliably produces its conventions when loaded, but the with-skill runs themselves surfaced internal inconsistencies: the skill names artifacts it never defines (`DEC-###`, two `Status` values, three size tiers) and shows no end-to-end example of its own template. Separately, eval-1 cannot discriminate skill value because its subject material is the skill itself: a baseline agent mirrors EARS/GWT/handoff conventions straight from the input, so the eval passes with or without the skill (10/10 both arms).

Undefined conventions are worse than missing ones: an agent following the skill must either invent semantics (divergent behavior across runs) or silently skip the convention (dead weight in the trigger surface).

## Goals

- G-001: Every ID convention and field value named in `SKILL.md` has a defined home and defined semantics.
- G-002: An agent reading only `SKILL.md` can see one condensed, correct instance of the template's load-bearing conventions (EARS, GWT traceability, Decisions).
- G-003: The eval set discriminates skill value on all three evals; no eval's subject embodies the conventions under test.
- G-004: The v1.3 file remains within repo size budgets and existing structure, so downstream hosts (Cursor, Claude Code, Codex) see an incremental revision, not a rewrite.

## Non-Goals

- NG-001: No edits to any other skill in this exercise; friction findings about other skills go to the Phase D friction log.
- NG-002: No restructuring, reordering, or rewording of existing `SKILL.md` sections beyond what REQ-001..REQ-010 require. The workflow steps, template section order (except the one insertion in REQ-001), and reference files' existing content stay as-is.
- NG-003: No change to the frontmatter `description` (load-bearing trigger surface per `AGENTS.md`); only `metadata.version` changes.
- NG-004: No iteration-4 benchmark run inside this exercise. The repo's eval loop expects revised skills to be benchmarked before being trusted; that run is an explicit follow-up after v1.3 ships. (Tension logged as friction.)
- NG-005: No modifications to `references/requirements-and-acceptance-criteria.md` or `references/spec-type-profiles.md`.
- NG-006: The eval harness itself is out of scope; eval changes are limited to `evals/evals.json` and the new fixture file.

## Users And Stakeholders

- AI coding agents using the skill to write specs: need defined semantics for every convention the skill names.
- AI agents executing this revision via ticket-workflow: need file-inspectable acceptance criteria.
- Hamza (owner): needs the benchmark to measure real skill value, and the skill to stay portable across hosts.

## Current State

Verified against `skills/defining-specifications/SKILL.md` (v1.2, 211 lines) on 2026-06-10:

- `DEC-###` appears in the Agent-Friendly Conventions ID list (line 179) and "decisions" are named a first-class category in Operating Principles (line 28), but the default template (lines 104-175) has no Decisions section. Orphan confirmed.
- The template offers `Status: Draft | Ready for Review | Approved | Blocked` (line 107); Self-Review (line 98) defines only the Draft-to-Ready-for-Review transition. `Approved` and `Blocked` have no entry or exit rules. Confirmed.
- Clarify (lines 66-69) keys question budgets (3/5/7) to Simple/Medium/Large specs; the tiers are defined nowhere in `SKILL.md` or `references/`. Confirmed.
- No inline worked example exists. `references/requirements-and-acceptance-criteria.md` has a weak-vs-strong contrast (lines 58-75) but no end-to-end filled instance. Confirmed.
- Eval-1 (`spec-skill-improvement`, id 1) in `evals/evals.json` takes `skills/defining-specifications/SKILL.md` as its `files` subject and asserts EARS/GWT/handoff conventions in the output (assertions 8-10) — conventions the subject itself embodies. Iteration-3 measured 10/10 in both arms. Confounding confirmed.
- `evals.json` line 41 references the subject by absolute home path (`/Users/hamzaamjad/...`), in tension with the repo portability rule. Noted; see Technical Context.

## Proposed Behavior

v1.3 of `SKILL.md` defines everything it names: a `## Decisions` template section anchors `DEC-###`; a status lifecycle gives all four `Status` values entry/exit rules; the Clarify tiers are defined by observable scope signals; a condensed worked example shows the conventions in use. The eval set replaces eval-1's subject with a bundled convention-free fixture so all three evals discriminate.

## Requirements

- REQ-001: The v1.3 default spec template shall include a `## Decisions` section, inserted immediately before `## Open Questions`, with entry format `- DEC-001: <decision> — Rationale: <why>. Alternatives considered: <list>. Date: <YYYY-MM-DD>.`
- REQ-002 (scope addition beyond the 5-item backlog, surfaced by self-review): When a blocking open question is resolved during review, the skill shall direct authors to record the resolution as a `DEC-###` entry rather than silently deleting the `Q-###` item.
- REQ-003: The skill shall define entry and exit criteria for each `Status` value (`Draft`, `Ready for Review`, `Approved`, `Blocked`), colocated with the existing Self-Review status gate, preserving the current Draft-to-Ready-for-Review rule unchanged.
- REQ-004: If a spec is marked `Blocked`, then the skill shall require the status line or an adjacent note to name the blocking `Q-###` or external dependency.
- REQ-005: Where a spec is marked `Approved`, the skill shall require the approver and date to be recorded, and shall state that material post-approval edits revert the spec to `Draft` or `Ready for Review` with a changelog entry.
- REQ-006: The skill shall define the Simple, Medium, and Large tiers referenced by the Clarify question budgets using observable scope signals (such as components or files touched, contract/data/schema changes, rollout or migration needs, and residual ambiguity after intake), while keeping the existing 3/5/7 question budgets unchanged.
- REQ-007: `SKILL.md` shall contain one inline worked example, at most 40 lines including its fence, presented as a condensed filled instance of the template that demonstrates at least: two EARS requirement patterns, one Given/When/Then acceptance criterion with a `(verifies REQ-###)` mapping, one `DEC-###` entry, one `Q-###` or `ASM-###` entry, and a `Status` line consistent with REQ-003.
- REQ-008: The worked example section shall point to `references/requirements-and-acceptance-criteria.md` for full patterns rather than duplicating reference content.
- REQ-009: Eval id 1 in `evals/evals.json` shall take as its subject a new fixture file under `skills/defining-specifications/evals/fixtures/`, with its prompt rewritten to ask the agent to review and formalize that draft into a focused specification; the eval `id` value 1 shall be retained, and the eval `name` may change to match the new subject.
- REQ-010: The fixture shall be a realistic rough draft (a feature idea or informal notes document) that contains no EARS `shall` requirements, no Given/When/Then phrasing, no `For Implementing Agents` heading, and no `REQ-`/`AC-`/`DEC-` style IDs, so the conventions under test cannot leak from the subject.
- REQ-011: The frontmatter `metadata.version` shall be `"1.3"`.
- REQ-012 (scope addition, surfaced by self-review): The quality checklist item "Separates confirmed facts from assumptions and open questions" shall be extended to include decisions (facts, decisions, assumptions, open questions).

## Nonfunctional Requirements

- NFR-001: `SKILL.md` shall remain at or under 300 lines (`wc -l`).
- NFR-002: Each new or modified `SKILL.md` section shall stay under ~40 lines, per `skills/engineering-context/references/rubric.md` size budgets.
- NFR-003: No new content shall introduce absolute paths, deployment-root references, all-caps directives, or aggressive emphasis (per `AGENTS.md` critical rules); `python3 skills/engineering-context/scripts/validate_context.py .` shall report no new issues beyond the 6 pre-existing LOW findings on `AGENTS.md`.
- NFR-004 (scope addition, surfaced by self-review against the repo portability rule): The fixture path added to eval-1's `files` and prompt shall be expressed relative to the repo root, matching the path style already used inside eval prompts (see ASM-001 for the harness caveat).

## Technical Context

- Affected files: `skills/defining-specifications/SKILL.md` (211 lines today; ~89 lines of headroom against the 300 cap — additions are estimated at ~55-65 lines total), `skills/defining-specifications/evals/evals.json`, new `skills/defining-specifications/evals/fixtures/<name>.md`.
- Placement guidance (advisory): the status lifecycle extends workflow step 6 (Self-Review) or a small adjacent subsection; tier definitions live inside or adjacent to workflow step 3 (Clarify); the worked example sits immediately after the Default Spec Template section.
- Overflow fallback (deterministic): if REQ-007 and NFR-001 cannot both hold, move the full example to a new `references/worked-example.md` and keep a pointer plus an excerpt of at most 10 lines inline. The headroom estimate says this should not trigger.
- Known issue, not in scope to fix: eval-1's current `files` entry uses an absolute home path. REQ-009's new entry uses a repo-relative path (NFR-004); the harness compatibility question is captured in ASM-001 and the friction log, and reverting to an absolute path is a one-line change if ASM-001 fails.
- Fixture content is implementation detail, constrained only by REQ-010 and realism; suggested subject: rough notes for a small workspace capability unrelated to spec conventions.

## Implementation Slices

- SLICE-001: Decisions section in template + Q-to-DEC migration note + checklist extension (REQ-001, REQ-002, REQ-012).
- SLICE-002: Status lifecycle + Clarify tier definitions (REQ-003, REQ-004, REQ-005, REQ-006).
- SLICE-003: Inline worked example + reference pointer (REQ-007, REQ-008).
- SLICE-004: Eval-1 fixture + evals.json rewrite (REQ-009, REQ-010, NFR-004).
- SLICE-005: Version bump + line/tone/validation sweep across the finished file (REQ-011, NFR-001, NFR-002, NFR-003).

## Testing And Verification

- TEST-001: `wc -l skills/defining-specifications/SKILL.md` is ≤ 300.
- TEST-002: File inspection — template block contains `## Decisions` immediately before `## Open Questions`; Self-Review area defines all four statuses; Clarify tiers are defined; example block is ≤ 40 lines and contains `shall`, `Given`, `(verifies REQ-`, and `DEC-001`.
- TEST-003: Fixture purity by grep — `rg -n "shall|For Implementing Agents|REQ-[0-9]|AC-[0-9]|DEC-[0-9]" <fixture>` returns nothing, and no line matches the Given/When/Then triple.
- TEST-004: `python3 -c "import json,sys; d=json.load(open('skills/defining-specifications/evals/evals.json')); e=[x for x in d['evals'] if x['id']==1][0]; print(e['files'])"` parses and shows the fixture path; the fixture file exists at that path.
- TEST-005: `python3 skills/engineering-context/scripts/validate_context.py .` reports 0 high, 0 medium, and no new low findings.
- TEST-006: `rg -n "version" skills/defining-specifications/SKILL.md` shows `version: "1.3"` in frontmatter.

## Risks And Mitigations

- RISK-001: The inline example pushes `SKILL.md` over budget. / Mitigation: deterministic overflow fallback in Technical Context.
- RISK-002: A repo-relative `files` path breaks a future eval-harness run. / Mitigation: ASM-001 recorded; the failure mode is loud (missing file) and the revert is one line.
- RISK-003: Lifecycle/tier additions drift into rewording adjacent workflow text. / Mitigation: NG-002 confines edits; reviewer diff-checks against v1.2.
- RISK-004: The unresolved gitignore conflict (Q-001) stalls Phase B. / Mitigation: decision taken at the Phase A checkpoint, before epic creation.

## Decisions

- DEC-001: Replace eval-1's subject with a bundled convention-free fixture rather than demoting eval-1 to a regression-only check. — Rationale: keeps three value-discriminating evals (better benchmark power) and broadens task-type coverage to "formalize a rough draft"; a regression-only eval would keep costing runtime while adding little signal. Alternatives considered: demote to regression-only (weaker benchmark); point at another live skill file (subject drifts as skills evolve and may partially embody conventions). Date: 2026-06-10.
- DEC-002: The worked example lives inline in `SKILL.md` (≤ 40 lines) rather than only in `references/`. — Rationale: the backlog gap is specifically the absence of an *inline* example; 89 lines of headroom make it feasible within budget. Alternatives considered: full example in `references/worked-example.md` only (kept as overflow fallback). Date: 2026-06-10.
- DEC-003 (resolves Q-001): Un-ignore both `.tickets/` and all of `.prompts/` in this repo's `.gitignore`; keep `.claude/worktrees/` ignored. Broadened from the spec's draft option A (which kept `.prompts/exercises/` ignored) because the exercise briefs are substantial authored artifacts the user wants versioned and synced at the end of the orchestration session. — Rationale: ticket-workflow's commit/`git mv`/`git rm` operations require tracked paths; coherent history beats transience. Recorded in `docs/decisions/2026-06-10-version-tickets-and-prompts.md`. Alternatives considered: narrow un-ignore (`.prompts/orchestration/` only); protocol variant for unversioned-tickets repos (out-of-scope ticket-workflow edit, weaker audit trail). Decided by: Hamza via orchestrator proxy. Date: 2026-06-10.
- DEC-004 (resolves Q-002): Commit the approved spec plus the DEC-003 policy change (`.gitignore`, `AGENTS.md` layout lines, decision memo) on main immediately after Phase A approval; create the epic from that state. — Rationale: the epic branch starts from a state already containing the spec and the unblocked gitignore, keeping the epic diff purely v1.3 implementation. Alternatives considered: first commit in the epic worktree (entangles repo policy with epic content). Decided by: Hamza via orchestrator proxy. Date: 2026-06-10.

## Open Questions

- Q-001 (resolved 2026-06-10 → DEC-003): This repo's `.gitignore` ignores `.tickets/` and `.prompts/`, but ticket-workflow requires committing tickets and the orchestration prompt at epic creation (step 7) and `git mv`/`git rm` on them at closure — operations that fail on untracked files. Options were (A) narrow un-ignore for this repo, or (B) a protocol variant for unversioned-tickets repos. Decision: A, broadened to all of `.prompts/`; see DEC-003.
- Q-002 (resolved 2026-06-10 → DEC-004): Commit timing for this spec once approved — on main before epic creation, or as the first commit in the epic worktree. Decision: on main immediately after approval; see DEC-004.

## Assumptions

- ASM-001: The eval harness resolves repo-relative `files` paths against the repo root. Confidence: low-medium (current entry is absolute; harness not run in this exercise per NG-004). Invalidated by an iteration-4 run failing to attach the fixture; remedy is a one-line revert to an absolute path.
- ASM-002: ~55-65 lines of additions fit the 89-line headroom (211 → ≤ 276 lines). Confidence: high. Invalidated only if drafting balloons; the overflow fallback then applies.
- ASM-003: No tooling parses the default template's section order programmatically; `validate_context.py` scans instruction files for hygiene, not spec-template internals. Confidence: high, based on the validator's output scope observed on 2026-06-10.

## Acceptance Criteria

- AC-001 (verifies REQ-001): Given v1.3 `SKILL.md`, When the template block is inspected, Then a `## Decisions` section with the `DEC-001` entry format appears immediately before `## Open Questions`.
- AC-002 (verifies REQ-002): Given the v1.3 Self-Review or Decisions guidance, When read, Then it directs resolved blocking questions to be recorded as `DEC-###` entries.
- AC-003 (verifies REQ-003, REQ-004, REQ-005): Given the v1.3 status lifecycle text, When each of the four statuses is looked up, Then each has at least one entry criterion and one exit criterion, `Blocked` requires naming its blocker, and `Approved` requires approver-and-date plus the re-approval rule for material edits.
- AC-004 (verifies REQ-006): Given the v1.3 Clarify guidance, When the tier definitions are read, Then Simple, Medium, and Large are each defined by observable scope signals and the 3/5/7 budgets are unchanged from v1.2.
- AC-005 (verifies REQ-007, REQ-008): Given v1.3 `SKILL.md`, When the worked example block is measured and read, Then it is ≤ 40 lines, contains two distinct EARS patterns, a GWT criterion with `(verifies REQ-###)`, a `DEC-###` entry, and a pointer to `references/requirements-and-acceptance-criteria.md`.
- AC-006 (verifies REQ-009, NFR-004): Given v1.3 `evals/evals.json`, When eval id 1 is read, Then its `files` entry is a repo-relative path to a fixture under `evals/fixtures/`, its prompt asks for review/formalization of that fixture, and the file exists at that path.
- AC-007 (verifies REQ-010): Given the fixture file, When TEST-003's grep runs, Then it returns no matches.
- AC-008 (verifies REQ-011): Given v1.3 frontmatter, When read, Then `metadata.version` is `"1.3"` and `name`/`description` are byte-identical to v1.2.
- AC-009 (verifies REQ-012): Given the v1.3 quality checklist, When the separation item is read, Then it lists facts, decisions, assumptions, and open questions.
- AC-010 (verifies NFR-001, NFR-002, NFR-003): Given the finished v1.3 file, When TEST-001 and TEST-005 run and each new or modified section is measured, Then the line count is ≤ 300, no such section exceeds ~40 lines, and validation reports no new findings.

## Source References

- `skills/defining-specifications/SKILL.md` (v1.2; cited lines 28, 66-69, 98, 104-175, 107, 179)
- `skills/defining-specifications/references/requirements-and-acceptance-criteria.md`; `references/spec-type-profiles.md` (agent-handoff profile applied to this spec)
- `skills/defining-specifications/evals/evals.json` (eval id 1, lines 24-43)
- `skills/defining-specifications-workspace/iteration-3/benchmark.md` (backlog source, "Suggested next steps")
- `AGENTS.md` (portability rules, size budgets, eval loop, gitignore policy boundary); `.gitignore` (lines 41-44)
- `skills/ticket-workflow/SKILL.md` (epic creation steps 6-7, closure steps 2-3 — basis for Q-001)
- `.prompts/exercises/02-dogfood-spec-to-ship-v13.md` (exercise brief; unversioned)

## Changelog

- 2026-06-10: Draft found uncommitted in workspace at Phase A start; adopted per the skill's update-in-place rule. Verification pass: all Current State claims re-verified against v1.2 sources and confirmed accurate. Repair: AC-006 extended to also verify NFR-004, which previously had no acceptance-criterion coverage (traceability gap).
- 2026-06-10 (Phase A checkpoint): Spec approved, including scope additions REQ-002/REQ-012 and DEC-001. Q-001 resolved as DEC-003 (un-ignore `.tickets/` and `.prompts/`, broadened option A); Q-002 resolved as DEC-004 (commit on main post-approval). Status moved Draft → Approved with approver and date recorded; note v1.2 defines no entry rule for `Approved` — the recording convention applied here is the one this spec's own REQ-005 introduces.
