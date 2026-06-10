# Skill-description triggering audit — 2026-06-10

Audit of the six frontmatter `description` fields in `skills/*/SKILL.md`, treating each description as a routing prompt whose target model is the host's skill router (engineering-prompts mode 4: prompt audit — diagnose failure modes, minimal rewrite). `skills/defining-specifications-workspace/` is eval data, not a skill, and is out of scope.

## Method

1. Built the probe set below before touching any description: per skill 4–6 positives (should trigger) and 3–4 hard negatives (plausible near-misses that should not trigger), plus shared collision probes covering the four known collision surfaces (defining-specifications↔ticket-workflow, engineering-context↔engineering-prompts, hamza-voice breadth, session-retrospective↔engineering-context).
2. Evaluated every probe against the current descriptions (before-matrix), recording the deciding phrase for every trigger or weak claim. Verdicts are static evaluation — careful reading of each description against each probe, reasoned as the host router would — not live router runs.
3. Rewrote only descriptions with demonstrated precision or recall failures; every change traces to a failed probe.
4. Re-ran the identical matrix against the rewritten descriptions (after-matrix).

Guidance applied:

- engineering-prompts anti-pattern library: *Aggressive trigger language on Claude 4.6 (scoped)* — aggressive language in tool/skill-invocation prompts ("whenever", "any request where…", unconditional quoted trigger lists) causes overtriggering on recent Claude models. Fix: plain imperative phrasing, reserve breadth for genuine scope.
- skill-creator description guidance: the description is the primary triggering mechanism and must state both what the skill does and concrete trigger contexts; metadata budget ~100 words (soft), 1024-character hard cap; hard negatives should be near-misses, not obviously-irrelevant probes. Its "make descriptions a little pushy" advice is deliberately not followed: it targets older undertriggering behavior and is superseded by the Claude 4.6 overtriggering guidance above (per the exercise brief).
- AGENTS.md: description is a load-bearing trigger surface; moderate imperative phrasing; no all-caps directives.

Verdict legend: ✓ = triggers, ~ = weak/ambiguous claim (router plausibly fires), · = no trigger. **Bold** marks verdicts that are failures. Skills: DS = defining-specifications, EC = engineering-context, EP = engineering-prompts, HV = hamza-voice, SR = session-retrospective, TW = ticket-workflow.

## Probe set

59 probes: 30 positives, 24 hard negatives, 5 shared collision probes.

### defining-specifications (5 positives, 4 hard negatives)

| ID | Probe |
|---|---|
| DS-P1 | "Draft a spec for adding rate limiting to our public API — I have rough notes in notes/rate-limit.md, turn them into something an agent can implement from." |
| DS-P2 | "Can you review docs/specs/SPEC-export-pipeline-2026-05-30.md and tell me if it's ready to hand to a coding agent?" |
| DS-P3 | "i have a rough idea for a notification digest feature. help me formalize it into product requirements before we build anything" |
| DS-P4 | "Write an RFC for migrating our session storage from Redis to Postgres — needs to be implementation-ready for review on Thursday." |
| DS-P5 | "Prepare an agent handoff doc for the search-index rebuild so a fresh session can pick it up without me re-explaining everything." |
| DS-N1 | "Implement the spec at docs/specs/SPEC-rate-limiting-2026-06-01.md — it's already approved." |
| DS-N2 | "Review this PR diff for the export pipeline, make sure the error handling is sane." |
| DS-N3 | "Break the approved payments spec down into tickets with dependencies so agents can pick them up." |
| DS-N4 | "What's the difference between an RFC and a design doc? When should a team use each?" |

### engineering-context (5 positives, 4 hard negatives)

| ID | Probe |
|---|---|
| EC-P1 | "Our AGENTS.md has gotten stale and contradicts CLAUDE.md in a few places — can you audit and clean it up?" |
| EC-P2 | "Do a context-rot pass over this repo's instruction files; the agent keeps making the same mistakes." |
| EC-P3 | "Set up an AGENTS.md for this new repo — structure it properly." |
| EC-P4 | "Score the quality of our .cursorrules and CLAUDE.md — duplication, staleness, contradictions, the works." |
| EC-P5 | "Review the permission boundaries in our agent instructions — I want explicit always/ask-first/never rules." |
| EC-N1 | "My system prompt for the support bot is 6k tokens and the model ignores half of it — compress it into a lean context block." |
| EC-N2 | "Write API documentation for the new endpoints in src/api/routes.py." |
| EC-N3 | "Clean up the dead code and unused imports across src/ — it's getting messy." |
| EC-N4 | "Why does my RAG pipeline retrieve irrelevant chunks? The context window fills up with junk." |

### engineering-prompts (6 positives, 4 hard negatives)

| ID | Probe |
|---|---|
| EP-P1 | "Write me a prompt for extracting line items from invoice PDFs with GPT-5 — needs to output strict JSON." |
| EP-P2 | "This prompt keeps producing inconsistent tone — fix why it isn't working. [prompt pasted]" |
| EP-P3 | "Design a system prompt for a customer-support triage agent on Claude." |
| EP-P4 | "Turn these messy meeting notes into a task brief I can hand to a contractor." |
| EP-P5 | "Port this Claude prompt to Gemini — it relies on XML tags and prefilling." |
| EP-P6 | "Audit this system prompt and tell me which parts are hurting performance." |
| EP-N1 | "The agent keeps ignoring our repo conventions — audit AGENTS.md and figure out why." |
| EP-N2 | "Why is my LangChain agent timing out when calling the vector store?" |
| EP-N3 | "Write a commit message for this diff." |
| EP-N4 | "Improve the wording of our app's onboarding tooltips." |

### hamza-voice (5 positives, 4 hard negatives)

Hard negatives implement the brief's required breadth surface: trivial transactional messages and non-personal product/team writing.

| ID | Probe |
|---|---|
| HV-P1 | "Draft a LinkedIn message to the hiring manager at Anthropic about the data platform role — make it sound like me." |
| HV-P2 | "Write a cover letter for this staff data engineer role using my background." |
| HV-P3 | "Polish this paragraph from my blog post on dbt testing — keep it in my voice." |
| HV-P4 | "Write a poem about coming out of a dark season — something I could perform." |
| HV-P5 | "Does this email read like me? Check it against my voice." |
| HV-N1 | "Draft an email to the building manager asking when the garage will be open this weekend." |
| HV-N2 | "Write a quick message for the team channel saying the deploy is done and the dashboard is back up." |
| HV-N3 | "Draft the release notes for v2.3 of the API." |
| HV-N4 | "Write an apology email template our support team can send when an order ships late." |

### session-retrospective (4 positives, 4 hard negatives)

| ID | Probe |
|---|---|
| SR-P1 | "That's a wrap for today — run a retro on this session." |
| SR-P2 | "Before we close out: what did we learn this session? Be honest about what went sideways." |
| SR-P3 | "session debrief please, then suggest workspace improvements" |
| SR-P4 | "We're wrapping up — capture lessons learned from this pairing session so next time goes smoother." |
| SR-N1 | "Write a retrospective doc for the Q2 incident — the postgres outage on May 14." |
| SR-N2 | "Audit AGENTS.md for staleness and contradictions." |
| SR-N3 | "Summarize this chat so I can paste it into the ticket." |
| SR-N4 | "Run our sprint retrospective — pull the Jira board and list what shipped vs slipped." |

### ticket-workflow (5 positives, 4 hard negatives)

| ID | Probe |
|---|---|
| TW-P1 | "Create a ticket for the CSV export bug — empty files crash the parser." |
| TW-P2 | "Execute FEAT-002 in .tickets/_standalone/ — check its dependencies first." |
| TW-P3 | "Decompose EPIC-a7f3/FEAT-003 into sub-tickets, it's too big for one pass." |
| TW-P4 | "Close out the auth epic — archive it and clean up the orchestration prompt." |
| TW-P5 | "Mark BUG-004 done and update its status — verification passed." |
| TW-N1 | "Write a spec for the export feature before we cut any tickets." |
| TW-N2 | "What's the status of the Jira ticket PROJ-1432?" |
| TW-N3 | "File a GitHub issue for the flaky CI job on the release workflow." |
| TW-N4 | "Help me prioritize my backlog for next sprint — what should come first?" |

### Shared collision probes

| ID | Surface | Probe | Desired routing |
|---|---|---|---|
| C1 | DS↔TW (spec-first vs decompose-first) | "Plan out the notification-digest feature for me — what should we build first?" | DS (shaping an undefined idea precedes tickets; TW only when tickets/epics are in play) |
| C2 | DS↔TW (decompose-first) | "Break the approved payments work into tickets agents can execute independently." | TW only (DS carves out decomposition) |
| C3a | EC↔EP (instruction files) | "Our CLAUDE.md and rules files have ballooned — the agent's context window is mostly stale instructions. Trim it." | EC only |
| C3b | EC↔EP (runtime context package) | "My agent's system prompt plus retrieved docs blow past the context budget every run — compress this context package into something lean." | EP only (context-compressor) |
| C4 | SR↔EC (post-session vs standalone audit) | "This session went badly — figure out what to change in our AGENTS.md so next session goes better." | SR (session-grounded improvement; EC for standalone audits) |

## Before-matrix (current descriptions)

### defining-specifications probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| DS-P1 | ✓ | · | · | · | · | · | DS: "draft a spec", "formalize rough notes" | pass |
| DS-P2 | ✓ | · | · | · | · | · | DS: "review an existing spec" | pass |
| DS-P3 | ✓ | · | · | · | · | · | DS: "define an idea", "write product requirements" | pass |
| DS-P4 | ✓ | · | · | · | · | · | DS: "implementation-ready design/RFC" | pass |
| DS-P5 | ✓ | · | · | · | · | · | DS: "prepare an agent handoff before coding" | pass |
| DS-N1 | · | · | · | · | · | · | DS declines: "Do not use for direct implementation" | pass |
| DS-N2 | · | · | · | · | · | · | DS declines: "ordinary code review" | pass |
| DS-N3 | · | · | · | · | · | ✓ | DS declines ("ticket decomposition"); TW: "creating tickets", "dependency checking" | pass |
| DS-N4 | · | · | · | · | · | · | informational question; no artifact request matches | pass |

### engineering-context probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| EC-P1 | · | ✓ | **~** | · | · | · | EC: "(2) canonical instruction source maintenance (AGENTS.md, CLAUDE.md…)", "(3) contradiction"; EP weak-claims via "auditing… system instructions" | pass w/ collision |
| EC-P2 | · | ✓ | · | · | · | · | EC: "(1) … context rot" | pass |
| EC-P3 | · | ✓ | · | · | · | · | EC: "(5) setting up or auditing AGENTS.md … structure" | pass |
| EC-P4 | · | ✓ | **~** | · | · | · | EC: "(4) instruction file quality review or scoring"; EP weak-claims via "auditing… system instructions" | pass w/ collision |
| EC-P5 | · | ✓ | · | · | · | · | EC: "(7) permission boundary … review" | pass |
| EC-N1 | · | **~** | ✓ | · | · | · | EC misfires via "(6) context window optimization" (unqualified); EP correctly claims via "compressing … system instructions", context-compressor | **FAIL (EC)** |
| EC-N2 | · | · | · | · | · | · | "documentation hygiene" is remediation, not authoring; subject anchor holds | pass |
| EC-N3 | · | · | · | · | · | · | code cleanup ≠ "workspace instruction quality" | pass |
| EC-N4 | · | **~** | · | · | · | · | EC misfires via "(6) context window optimization" (unqualified — RAG retrieval is not instruction files) | **FAIL (EC)** |

### engineering-prompts probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| EP-P1 | · | · | ✓ | · | · | · | EP: "write me a prompt" | pass |
| EP-P2 | · | · | ✓ | · | · | · | EP: "fix why my prompt isn't working" | pass |
| EP-P3 | · | · | ✓ | · | · | · | EP: "design a system prompt" | pass |
| EP-P4 | · | · | ✓ | **~** | · | · | EP: "turn these notes into a brief", "task briefs"; HV weak-claims via "memos, or any written communication" | pass w/ collision |
| EP-P5 | · | · | ✓ | · | · | · | EP: "port this prompt to another model" | pass |
| EP-P6 | · | · | ✓ | · | · | · | EP: "audit this prompt"; EC's items stay file-anchored | pass |
| EP-N1 | · | ✓ | **~** | · | · | · | EC correctly claims "(2)/(4)"; EP misfires via "auditing … system instructions, and context packages" — AGENTS.md *is* system instructions on a plain reading | **FAIL (EP)** |
| EP-N2 | · | · | · | · | · | · | runtime/infra failure, not prompt craft | pass |
| EP-N3 | · | · | · | · | · | · | no quoted trigger matches | pass |
| EP-N4 | · | · | · | · | · | · | UX copy, not prompts for LLMs; not Hamza-personal | pass |

### hamza-voice probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| HV-P1 | · | · | · | ✓ | · | · | HV: "LinkedIn messages", "make this sound like me" | pass |
| HV-P2 | · | · | · | ✓ | · | · | HV: "cover letters" | pass |
| HV-P3 | · | · | · | ✓ | · | · | HV: "blog posts", "write this in my voice" | pass |
| HV-P4 | · | · | · | ✓ | · | · | HV: "poetry, spoken word", "write a poem" | pass |
| HV-P5 | · | · | · | ✓ | · | · | HV: "reviewing or editing text to check if it matches Hamza's voice" | pass |
| HV-N1 | · | · | · | **✓** | · | · | HV misfires: unconditional quoted trigger "draft an email" + "any written communication" — trivial logistics, voice adds nothing | **FAIL (HV)** |
| HV-N2 | · | · | · | **✓** | · | · | HV misfires: "draft a message", "Slack messages", "any written communication" — trivial status note | **FAIL (HV)** |
| HV-N3 | · | · | · | **~** | · | · | HV weak-claims via "or any written communication" — release notes are product writing, not Hamza's personal voice | **FAIL (HV)** |
| HV-N4 | · | · | · | **✓** | · | · | HV misfires: "draft an email" / "emails" — a shared support template does not represent Hamza personally | **FAIL (HV)** |

### session-retrospective probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| SR-P1 | · | · | · | · | ✓ | · | SR: quoted "retro" + wrap-up signal | pass |
| SR-P2 | · | · | · | · | ✓ | · | SR: "what did we learn" | pass |
| SR-P3 | · | · | · | · | ✓ | · | SR: "session debrief" | pass |
| SR-P4 | · | · | · | · | ✓ | · | SR: "wrapping up a working session and wants to capture lessons learned" | pass |
| SR-N1 | · | · | · | · | **✓** | · | SR misfires: bare quoted "retrospective" — an incident postmortem is not the current session; in-context-memory framing loses to the unconditional quote list | **FAIL (SR)** |
| SR-N2 | · | ✓ | ~ | · | · | · | EC correctly claims; SR stays silent (no session language); EP weak-claim as in EP-N1 | pass |
| SR-N3 | · | · | · | · | · | · | summary ≠ retrospective; no trigger phrase | pass |
| SR-N4 | · | · | · | · | **✓** | · | SR misfires: bare quoted "retrospective"/"retro" — sprint/team retro on a Jira board, not this session | **FAIL (SR)** |

### ticket-workflow probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| TW-P1 | · | · | · | · | · | ✓ | TW: "creating tickets" | pass |
| TW-P2 | · | · | · | · | · | ✓ | TW: "executing/implementing tickets", "dependency checking" | pass |
| TW-P3 | · | · | · | · | · | ✓ | TW: "decomposing tickets into sub-tickets"; DS declines via carve-out | pass |
| TW-P4 | · | · | · | · | · | ✓ | TW: "closing epics, archiving completed epics" | pass |
| TW-P5 | · | · | · | · | · | ✓ | TW: "updating ticket status", "verifying ticket completion" | pass |
| TW-N1 | ✓ | · | · | · | · | · | DS correctly claims "draft a spec"; TW's verbs all presuppose tickets — request defers them | pass |
| TW-N2 | · | · | · | · | · | · | "in .tickets/" scope anchor excludes Jira | pass |
| TW-N3 | · | · | · | · | · | · | GitHub issues ≠ `.tickets/` | pass |
| TW-N4 | · | · | · | · | · | · | prioritization is no lifecycle operation | pass |

### Collision probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| C1 | **~** | · | · | · | · | **~** | DS weak-claims "define an idea"; TW weak-claims "creating tickets… decomposition" ("what should we build first" reads as sequencing). Neither description encodes which stage precedes — router coin-flip | **FAIL (ambiguous)** |
| C2 | · | · | · | · | · | ✓ | TW: "creating tickets"/"decomposing"; DS declines via "ticket decomposition" carve-out — the existing one-sided disambiguation works on this side | pass |
| C3a | · | ✓ | **~** | · | · | · | EC correctly claims "(1)/(3)/(6)"; EP weak-claims via "compressing … system instructions" | **FAIL (EP)** |
| C3b | · | **~** | ✓ | · | · | · | EP correctly claims "compressing … context packages"; EC misfires via "(6) context window optimization" (unqualified) | **FAIL (EC)** |
| C4 | · | **✓** | · | · | **✓** | · | SR claims "workspace improvements (AGENTS.md…)" + session signal; EC claims "(2) canonical instruction source maintenance". Both fire with equal strength; neither encodes the session-grounded vs standalone split | **FAIL (double-claim)** |

## Per-skill diagnosis

| Skill | Verdict | Failed probes | Offending phrase(s) |
|---|---|---|---|
| defining-specifications | **Leave alone** | none on DS's side (C1 ambiguity is resolved from the TW side; DS's claim on C1 is the desired winner) | — |
| engineering-context | **Rewrite (precision + collision)** | EC-N1, EC-N4, C3b | "(6) context window optimization or instruction prioritization" — unqualified by instruction files, it claims runtime prompt compression and RAG context complaints. Secondary: "(1) context cleanup" lacks the instruction-file anchor that items (2)–(5)/(7) have. No boundary toward engineering-prompts or session-retrospective |
| engineering-prompts | **Rewrite (collision)** | EP-N1, C3a (+ weak-claims on EC-P1/EC-P4) | "auditing … prompts, system instructions, and context packages" — on a plain reading, AGENTS.md/CLAUDE.md *are* system instructions, so the phrase claims workspace instruction-file audits that belong to engineering-context. No carve-out |
| hamza-voice | **Rewrite (precision)** | HV-N1, HV-N2, HV-N3, HV-N4 (+ weak-claim on EP-P4) | "Trigger whenever the user says … 'draft an email,' 'draft a message,' …" — unconditional quoted triggers fire on any email/message regardless of stakes; "or any written communication" / "memos, or any written communication" extends the claim to release notes, shared templates, and contractor briefs. Classic aggressive-breadth trigger language ("whenever … any …") per the anti-pattern library |
| session-retrospective | **Rewrite (precision)** | SR-N1, SR-N4 | quoted bare "retrospective", "retro", "debrief" — fire on incident postmortems and sprint/team retrospectives that the skill cannot serve (it only reads the current session from in-context memory). C4 double-claim: "applies workspace improvements (AGENTS.md…)" with no session-vs-standalone tiebreak |
| ticket-workflow | **Rewrite (collision)** | C1 | All lifecycle verbs presuppose tickets, but nothing tells the router that shaping/planning an undefined idea precedes ticket creation — "creating tickets" + "decomposition" weak-claim planning-stage requests. Mirror disambiguation missing (DS already carves out decomposition; TW does not carve out the spec stage) |

Rewrite set: engineering-context, engineering-prompts, hamza-voice, session-retrospective, ticket-workflow. Left byte-identical: defining-specifications (v1.3 — no failed probe on its side; its existing ticket-decomposition carve-out passes C2/DS-N3/TW-P3 cleanly).

## Changes made (description frontmatter only; every change probe-traceable)

| Skill | Offending phrase removed/qualified | Replacement | Traces to |
|---|---|---|---|
| hamza-voice | unconditional "Trigger whenever the user says … 'draft an email,' 'draft a message,'"; "or any written communication" (×2); "memos" | stakes qualifier ("text that represents Hamza personally and where the wording carries weight"); "draft an email"/"draft a message" conditioned on "when the recipient or audience matters"; explicit skip list: "routine transactional notes (scheduling, status updates, logistics) and non-personal product or team writing (release notes, shared templates, documentation)" | HV-N1, HV-N2, HV-N3, HV-N4, EP-P4 |
| session-retrospective | bare quoted "retrospective", "retro", "debrief" | session-anchored quotes only ("session retro", "retro this session", "session debrief"); explicit carve-out "Not for sprint or team retrospectives, incident postmortems, or retrospective documents about events outside this session"; C4 tiebreak "grounded in session evidence" + pointer to engineering-context for standalone audits | SR-N1, SR-N4, C4 |
| engineering-context | "(1) context cleanup" (unanchored); "(6) context window optimization or instruction prioritization" (unqualified) | "(1) cleanup of agent instruction files…"; "(6) context-window budgeting or instruction prioritization for instruction files"; boundary sentence: prompts/system prompts/context packages for LLM applications → engineering-prompts; just-finished session review → session-retrospective | EC-N1, EC-N4, C3b, C4 |
| engineering-prompts | "auditing … system instructions" claiming workspace instruction files (no carve-out) | appended: "For auditing or maintaining workspace agent instruction files (AGENTS.md, CLAUDE.md, .cursorrules), use engineering-context instead." — quoted trigger list untouched | EP-N1, C3a, EC-P1, EC-P4 |
| ticket-workflow | no spec-stage carve-out (lifecycle verbs weak-claimed planning requests) | appended: "For shaping a vague feature idea into requirements before tickets exist, use defining-specifications first; this skill takes over once work is ready to become tickets." — mirrors defining-specifications' existing decomposition carve-out | C1 |
| defining-specifications | — (no failed probe; byte-identical to v1.3) | — | — |

All trigger phrases that match how the user actually asks were preserved (quoted trigger lists in EP and SR-session forms; HV's "draft an email"/"draft a message" kept but stakes-conditioned; EC's seven numbered triggers kept; TW's lifecycle verbs kept). Phrasing stays plain imperative — no stacked emphasis, no "whenever … any …" breadth. Lengths after edit: EC 818, EP 804, HV 848, SR 806, TW 588, DS 531 chars — all well under the 1024-char cap; HV/SR/EP/EC sit at 99–118 words against the ~100-word soft budget, accepted as the cost of explicit boundary clauses.

## After-matrix (rewritten descriptions; Δ marks changed verdicts)

### defining-specifications probes — unchanged, all pass

| ID | DS | EC | EP | HV | SR | TW | Result |
|---|---|---|---|---|---|---|---|
| DS-P1…DS-P5 | ✓ | · | · | · | · | · | pass (5/5 positives kept) |
| DS-N1, DS-N2, DS-N4 | · | · | · | · | · | · | pass |
| DS-N3 | · | · | · | · | · | ✓ | pass (TW correctly claims decomposition) |

### engineering-context probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| EC-P1 | · | ✓ | · Δ | · | · | · | EC "(2)/(3)"; EP now defers via instruction-file carve-out | pass, collision resolved |
| EC-P2 | · | ✓ | · | · | · | · | EC "(1) cleanup of agent instruction files, context rot" | pass |
| EC-P3 | · | ✓ | · | · | · | · | EC "(5)" | pass |
| EC-P4 | · | ✓ | · Δ | · | · | · | EC "(4)"; EP carve-out names .cursorrules | pass, collision resolved |
| EC-P5 | · | ✓ | · | · | · | · | EC "(7)" | pass |
| EC-N1 | · | · Δ | ✓ | · | · | · | EC "(6)" now scoped "for instruction files" + boundary sends LLM-app prompts to EP | **resolved** |
| EC-N2 | · | · | · | · | · | · | — | pass |
| EC-N3 | · | · | · | · | · | · | — | pass |
| EC-N4 | · | · Δ | · | · | · | · | RAG context is not instruction files under the qualified "(6)" | **resolved** |

### engineering-prompts probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| EP-P1, EP-P2, EP-P3, EP-P5, EP-P6 | · | · | ✓ | · | · | · | quoted trigger list untouched ("write me a prompt", "fix why my prompt isn't working", "design a system prompt", "port this prompt to another model", "audit this prompt") | pass (no recall loss; EP-P3/P6 are LLM-application prompts, outside the named-file carve-out) |
| EP-P4 | · | · | ✓ | · Δ | · | · | EP "turn these notes into a brief"; HV's "any written communication"/"memos" removed, "non-personal … team writing" skipped | pass, collision resolved |
| EP-N1 | · | ✓ | · Δ | · | · | · | EP defers: "For auditing or maintaining workspace agent instruction files (AGENTS.md…), use engineering-context instead" | **resolved** |
| EP-N2, EP-N3, EP-N4 | · | · | · | · | · | · | — | pass |

### hamza-voice probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| HV-P1 | · | · | · | ✓ | · | · | "LinkedIn messages", "make this sound like me" | pass |
| HV-P2 | · | · | · | ✓ | · | · | "job applications, cover letters" | pass |
| HV-P3 | · | · | · | ✓ | · | · | "blog posts", "write this in my voice" | pass |
| HV-P4 | · | · | · | ✓ | · | · | "poetry, spoken word", "write a poem" | pass |
| HV-P5 | · | · | · | ✓ | · | · | "reviewing text for whether it sounds like Hamza" | pass |
| HV-N1 | · | · | · | · Δ | · | · | "routine transactional notes (scheduling, … logistics)"; email trigger now conditioned on recipient weight | **resolved** |
| HV-N2 | · | · | · | · Δ | · | · | "status updates" excluded by name | **resolved** |
| HV-N3 | · | · | · | · Δ | · | · | "release notes" excluded by name | **resolved** |
| HV-N4 | · | · | · | · Δ | · | · | "shared templates" excluded; not text representing Hamza personally | **resolved** |

### session-retrospective probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| SR-P1 | · | · | · | · | ✓ | · | "retro this session" + wrap-up signal | pass |
| SR-P2 | · | · | · | · | ✓ | · | "what did we learn" | pass |
| SR-P3 | · | · | · | · | ✓ | · | "session debrief" | pass |
| SR-P4 | · | · | · | · | ✓ | · | "signals they are wrapping up and want lessons captured" | pass |
| SR-N1 | · | · | · | · | · Δ | · | "Not for … incident postmortems, or retrospective documents about events outside this session" | **resolved** |
| SR-N2 | · | ✓ | · Δ | · | · | · | EC claims; SR defers standalone audits to engineering-context; EP weak-claim gone via carve-out | pass |
| SR-N3 | · | · | · | · | · | · | — | pass |
| SR-N4 | · | · | · | · | · Δ | · | "Not for sprint or team retrospectives" | **resolved** |

### ticket-workflow probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| TW-P1…TW-P5 | · | · | · | · | · | ✓ | lifecycle verbs untouched; new sentence defers only the shaping of vague ideas, and these are explicit ticket operations | pass (5/5 positives kept) |
| TW-N1 | ✓ | · | · | · | · | · | DS claims "draft a spec"; TW reinforced by "use defining-specifications first" | pass |
| TW-N2, TW-N3, TW-N4 | · | · | · | · | · | · | `.tickets/` anchor; no lifecycle op | pass |

### Collision probes

| ID | DS | EC | EP | HV | SR | TW | Deciding phrase | Result |
|---|---|---|---|---|---|---|---|---|
| C1 | ✓ Δ | · | · | · | · | · Δ | DS "define an idea" is now sole claimant; TW defers shaping-stage requests to defining-specifications by name | **resolved → DS** |
| C2 | · | · | · | · | · | ✓ | unchanged; DS carve-out + TW claim | pass |
| C3a | · | ✓ | · Δ | · | · | · | EC "(1)/(3)/(6)"; EP instruction-file carve-out | **resolved → EC** |
| C3b | · | · Δ | ✓ | · | · | · | EP "compressing … context packages" (context-compressor); EC boundary defers LLM-app context to EP | **resolved → EP** |
| C4 | · | · Δ | · | · | ✓ | · | SR "workspace improvements … grounded in session evidence"; EC boundary: "reviewing a just-finished working session belongs to session-retrospective" | **resolved → SR** |

## After-matrix summary

- **No lost positive triggers**: defining-specifications 5/5, engineering-context 5/5, engineering-prompts 6/6, ticket-workflow 5/5 (the four skills the definition of done names), and additionally hamza-voice 5/5 and session-retrospective 4/4.
- **All 12 failing cells from the before-matrix resolved**: HV-N1–N4, EP-P4(HV), SR-N1, SR-N4, EC-N1, EC-N4, C3b(EC), EP-N1(EP), C3a(EP), plus both ambiguity failures C1 and C4.
- Every collision probe now routes to exactly one skill: C1→DS, C2→TW, C3a→EC, C3b→EP, C4→SR.

## Residual collisions accepted by design

1. **hamza-voice on borderline-stakes messages** (e.g., "draft a Slack message to my manager about missing the deadline"): still triggers. Accepted — stakes, not length or channel, is the intended boundary; messages with relationship or career weight are exactly the skill's job. The router judges "when the recipient or audience matters."
2. **defining-specifications ↔ ticket-workflow on explicitly two-stage requests** (e.g., "spec this out, then cut tickets"): both legitimately trigger, in sequence. Accepted — the descriptions now encode precedence (spec first, tickets after), not mutual exclusion.
3. **engineering-context ↔ engineering-prompts on repo-committed product prompts** (e.g., auditing a versioned system prompt that lives in the workspace but drives an LLM application): both could claim. Accepted — the named-file anchor (AGENTS.md, CLAUDE.md, .cursorrules → engineering-context) covers the common cases; the remainder is rare and either skill produces a sane outcome.

## Validation

- Programmatic YAML check: all six frontmatter blocks parse with `yaml.safe_load`; `name` and all non-description fields byte-identical to HEAD; `defining-specifications/SKILL.md` byte-identical to HEAD in full; all descriptions under the 1024-character cap.
- `python3 skills/engineering-context/scripts/validate_context.py .`: 0 high, 0 medium; 7 pre-existing LOW tone flags, all in `AGENTS.md` (outside this audit's scope — no skill-file findings).
- Description-only edits confirmed via `git diff`: changes confined to the frontmatter `description` of five SKILL.md files; no skill-body lines touched.
