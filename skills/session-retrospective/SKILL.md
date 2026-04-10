---
name: session-retrospective
description: >-
  End-of-session retrospective and workspace improvement skill for AI coding agents.
  The agent reviews the current session from in-context memory, delivering an honest
  assessment of what went well, what didn't, and how the user can improve as a pair
  programmer. Then optionally applies workspace improvements (AGENTS.md, CLAUDE.md,
  .context/, docs/) to give future sessions a head start. Use when the user requests
  a "session review", "retrospective", "retro", "what did we learn", "end of session",
  "debrief", or "session debrief". Also use when the user signals they are wrapping up
  a working session and wants to capture lessons learned.
---

# Session Retrospective

Run a two-phase end-of-session review: first a conversational retrospective, then an optional workspace improvement pass. All analysis draws from in-context memory of the current session only — no transcript files, no external data.

---

## Phase 1: Retrospective

Deliver four sections conversationally. Never write retrospective output to a file.

### Section 1 — What Went Well

Identify specific wins from the session. Every point must reference an actual task, approach, prompt, or collaboration pattern that occurred.

| Requirement | Detail |
|---|---|
| Specificity | Name the task, file, or decision. "We refactored the auth middleware in one pass" not "things went smoothly." |
| Evidence | Each point must cite something that happened. No generic praise. |
| Scope | Cover both agent contributions and user contributions. |

### Section 2 — What Didn't Go Well

Honest friction points from both sides. **Minimum one item required — every session has friction.**

**Agent-side issues to look for:**
- Wrong approaches tried before finding the right one
- Wasted cycles (unnecessary file reads, redundant searches, over-engineering)
- Misunderstandings of user intent
- Poor tool choices or sequencing
- Unnecessary back-and-forth or confirmation loops

**User-side issues to look for:**
- Unclear or ambiguous instructions
- Missing context that caused rework
- Mid-task scope changes
- Under-specified requests that required guessing
- Contradictory requirements

| Requirement | Detail |
|---|---|
| Honesty | Do not soften or hedge. State what happened and what it cost (time, cycles, confusion). |
| Balance | Include at least one item from each side when both contributed friction. |
| Citation | Every item must reference a specific moment — "When I tried X and it failed because Y." |

### Section 3 — How the User Can Improve Pairing

Actionable prompting and collaboration tips derived from observed patterns. Frame as coaching from a senior pair programmer. Focus on transferable habits, not one-off task fixes.

**Good output characteristics:**
- Describes a pattern observed in the session, then generalizes it
- Explains *why* the pattern matters (fewer round-trips, less ambiguity, faster convergence)
- Gives the user a concrete thing to do differently next time
- Transferable to other sessions and other agents

**Example of strong output:**

> "When you provided the database schema upfront before asking me to write the query, I completed it in one pass with no follow-ups. Front-loading structural context like that — schemas, type definitions, file layouts — before asking for implementation would consistently cut round-trips across all your sessions."

**Example of weak output (do not produce):**

> "Try to be more specific with your requests."

This is too vague, not grounded in session evidence, and not transferable. Every tip must pass the test: *Could this advice help the user in a completely different session on a different project?*

### Section 4 — Workspace Context Improvements

Concrete recommendations for changes that would give future sessions a head start. For each recommendation, provide:

| Field | Content |
|---|---|
| Target file | Existing file path or proposed new file path |
| Change | Specific addition, edit, or restructure |
| Justification | Must pass this test: "Would this have made THIS session go better if it existed at session start?" |

Only recommend changes you can justify with session evidence. Do not pad with generic suggestions.

---

## Phase 2: Workspace Improvements

After delivering the retrospective, ask:

> "Would you like me to implement these workspace improvements?"

If the user declines or does not respond, stop. If the user agrees, apply changes following the priority hierarchy below.

### Priority Hierarchy

| Priority | Target | Posture | Guidance |
|---|---|---|---|
| 1 — update freely | `AGENTS.md` and `CLAUDE.md` at project root | First-class memory. Add without hesitation. Create if missing. | Plain bullet points under section headers (e.g., `## User Preferences`, `## Workspace Conventions`, `## Project Facts`). One bullet per insight. No narrative prose. |
| 2 — update thoughtfully | `.context/` files | Update when domain knowledge, team info, or business context is missing or outdated. | Append new information. Preserve existing structure and authorial voice. Restructure only if organization is clearly broken. |
| 3 — update conservatively | `docs/` files | Only when documentation is demonstrably wrong or a critical gap blocked work during the session. | Prefer additions over edits. Never remove content without asking. Provide strong justification. |

### Rules for All Workspace Changes

- Never delete existing content without explicit user approval
- Prefer additions over modifications — always
- `AGENTS.md` and `CLAUDE.md` must stay identical to each other in content
- If a file beyond `AGENTS.md`/`CLAUDE.md` does not exist, ask before creating it
- Each change must include a one-line rationale comment so the user can audit later

---

## Quality Gates

Self-enforce these at runtime before delivering output:

1. **Every retrospective point cites a specific moment** from the session — no filler, no generics
2. **"What didn't go well" contains at least one item** — if you cannot find friction, look harder
3. **Pairing tips describe transferable patterns**, not task-specific corrections
4. **Workspace recommendations are concrete and testable** — file path, change, justification
5. **Tone is direct, collegial, and constructive** — a respected peer, not a manager, not a cheerleader
6. **The retrospective is conversational only** — nothing is written to disk until Phase 2 begins with user approval
