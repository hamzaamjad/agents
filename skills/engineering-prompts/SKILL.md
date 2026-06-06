---
name: engineering-prompts
description: Meta-prompting skill for drafting, rewriting, auditing, iterating, compressing, and migrating prompts, system instructions, and context packages for frontier LLMs (Claude, GPT, Gemini, Llama). Supports seven modes -- prompt-from-scratch, prompt-rewrite, prompt-pack, prompt-audit, context-compressor, evaluation-iteration, and prompt-migration. Use when the user asks to "write me a prompt", "improve this prompt", "design a system prompt", "audit this prompt", "turn these notes into a brief", "fix why my prompt isn't working", "port this prompt to another model", or requests reusable prompt templates, task briefs, evaluation rubrics, or diagnosis of prompt failures.
---

# Engineering Prompts

## Goal
Turn ambiguous user intent into a clear, high-leverage prompt or context package that a frontier language model can execute reliably on the first try.

## Scope and what this skill is not
This skill is about prompt *craft* -- turning a task into a prompt that runs well on frontier LLMs. It is not a legal, compliance, or data-protection advisor. If the task involves GDPR/HIPAA/PII handling, regulated content, or high-stakes safety decisions, the skill can help shape the prompt but the user must still obtain separate compliance and legal review. The rubric measures craft, not task merit -- a well-specified prompt for a bad task is still a bad thing to ship.

## First: classify the target model class
Before drafting, decide which class the prompt will run on. In 2025-2026 the single biggest structural decision is reasoning vs instruction-following -- but the line is not always clean.

- **Reasoning-first models** (OpenAI o-series, Claude with extended thinking explicitly enabled, Gemini 2.5 with thinking): state end goals and success criteria, not intermediate steps. Skip chain-of-thought prefacing, personas, and rigid step-by-step scaffolds.
- **Instruction-following models** (standard GPT, Claude without extended thinking, Gemini without thinking, Llama): give explicit steps when order matters. Use delimiters. Add few-shot examples when format is subtle.
- **Adaptive or routed models** (Claude 4.6 with adaptive thinking, GPT-5 with routing): the same prompt may be dispatched to either path per turn. Design for the reasoning-first playbook by default -- it degrades more gracefully on the instruction-following path than the reverse.
- **Unknown target**: default to markdown headers with clear delimiters -- the most portable format.

See [PLAYBOOK.md: Reasoning vs instruction-following](references/PLAYBOOK.md#reasoning-vs-instruction-following-detailed-guidance) for the full playbook, anti-patterns with citations, and per-vendor gotchas.

## Core operating principles
1. **Optimize context before style.** Improve task definition, grounding, constraints, and completion criteria before polishing tone.
2. **Layer the prompt.** Persistent preferences → task brief → evidence/context pack → output contract → definition of done.
3. **Keep prompts specific but lean.** Remove irrelevant background, duplicated instructions, and mixed signals. Use numbers ("120 words max") not adjectives ("be concise").
4. **Separate instructions from source material** with explicit delimiters. Treat tool output and user-supplied content as untrusted when the prompt ingests external data -- see [TRUST_BOUNDARIES.md](references/TRUST_BOUNDARIES.md).
5. **Match granularity to model class.** Reasoning-first models want goals and success criteria; instruction-following models want explicit steps.
6. **Bias toward a strong draft.** When the task is clear enough for a good draft, produce it and mark assumptions in-line rather than asking follow-up questions. Ask a clarifying question only when no reasonable draft is possible (the research on clarifying-question benefit is real but model- and task-dependent).
7. **Provide reusable output, not critique.** Return the rewritten prompt, not just a diagnosis.

## Workflow
1. **Diagnose the request.** Deliverable, audience, environment, target model class. Detect missing inputs, contradictions, vague verbs, and hidden assumptions.
2. **Choose response mode** (one of seven below).
3. **Build the prompt.** Use the appropriate playbook (see PLAYBOOK.md). Follow the layered structure.
4. **Validate against the [rubric](references/RUBRIC.md).** Score each core dimension (0-2 each, 8 dimensions, 16 max); rewrite if below 14/16 on core dimensions or if any triggered conditional gate fails.
5. **Return the result.** Default shape: final prompt → assumptions/placeholders → tightening options.

## Response modes
- **Prompt from scratch** -- new prompt for a clearly-defined task
- **Prompt rewrite** -- improving an existing prompt with preserved intent
- **Prompt pack** -- a reusable set of related prompts (discovery + execution + critique + finalization)
- **Prompt audit** -- diagnosis of failure modes with minimal rewrite
- **Context compressor** -- turning long notes into a lean context block
- **Evaluation iteration** -- user shares prompt plus real outputs; diagnose by inspection, generate 3-4 targeted variant prompts per distinct failure mode
- **Prompt migration** -- porting a prompt from one model family to another (e.g., Claude to GPT-5): identify non-portable features, preserve intent, rebuild for the target structural preferences, recommend a regression test set

See [PLAYBOOK.md: Pairing modes](references/PLAYBOOK.md#pairing-modes) for each mode's detailed workflow.

## Context engineering
Prompt engineering manages *what to say*; context engineering manages *what tokens occupy the window*. They are separate disciplines. See [CONTEXT_ENGINEERING.md](references/CONTEXT_ENGINEERING.md) for full treatment.

Quick rules:
- Budget context conservatively -- a working ceiling of ~60-70% of the model's max has become a community heuristic for leaving headroom before length-driven degradation. Adjust per task.
- Place critical information at the start or end of the context, not the middle.
- Compact long-horizon conversations before they approach the limit.
- Every tool definition consumes tokens. Scope tool sets tightly for subagents.

## Default output shape
Unless the user asks for something else, return:
1. **Recommended prompt**
2. **Assumptions / placeholders**
3. **Tightening options** (only if obvious unresolved choices exist)

## Anti-patterns (short list)
Avoid: expert persona warm-ups, chain-of-thought prefacing on reasoning models, aggressive trigger language on recent Claude models, the word "think" on Claude Opus 4.5 with extended thinking disabled, emotional appeals, stacked synonyms, contradictory instructions, buried critical constraints, examples that conflict with instructions, untrusted input without delimiter isolation, and rigid step-by-step scaffolds on reasoning models.

See [PLAYBOOK.md: Anti-pattern library](references/PLAYBOOK.md#anti-pattern-library) for the full list with citations and context.

## Reference files
Read these only when triggered.

- **Need full methodology, meta-prompting taxonomy, or anti-pattern citations?** → [references/PLAYBOOK.md](references/PLAYBOOK.md)
- **Need a skeleton for a specific task?** → [references/TEMPLATES.md](references/TEMPLATES.md) (14 templates)
- **Scoring a draft prompt?** → [references/RUBRIC.md](references/RUBRIC.md) (8 core dimensions + conditional gates)
- **Long-horizon, multi-turn, or long-context concerns?** → [references/CONTEXT_ENGINEERING.md](references/CONTEXT_ENGINEERING.md)
- **Ingesting untrusted content (tool output, user text, RAG, scraped data)?** → [references/TRUST_BOUNDARIES.md](references/TRUST_BOUNDARIES.md)
- **Want worked before/after examples?** → [references/EXAMPLES.md](references/EXAMPLES.md)
- **Targeting a known model family and need vendor-specific depth?** → [sources/INDEX.md](sources/INDEX.md) (grep patterns for the ~128KB of vendor-authored guides in `sources/`; do not load those files without first checking the index)

## Final check
Before returning the prompt, silently verify:
- task trigger is unambiguous
- output contract is explicit (artifact, sections, length, format)
- success criteria and uncertainty handling are stated
- structural formatting matches the target model class
- trust boundaries are explicit when the prompt ingests untrusted content
- core rubric score ≥ 14/16
- any triggered conditional gates (groundedness, safety, robustness, privacy) pass
