---
name: engineering-prompts
description: Drafts, critiques, and rewrites prompts, system instructions, and context packages for frontier language models. Supports five modes -- prompt from scratch, prompt rewrite, prompt pack, prompt audit, and context compression. Use when the user requests a system prompt, reusable prompt template, task brief, evaluation rubric, or diagnosis of why a prompt underperforms.
---

# Engineering Prompts

## Goal
Turn ambiguous user intent into a clear, high-leverage prompt or context package that a capable model can execute reliably, regardless of target model family.

## Core operating principles
1. Optimize context before style. Improve task definition, grounding, constraints, and completion criteria before polishing tone.
2. Prefer a layered structure:
   - Persistent preferences (stable style or voice defaults)
   - Task brief (goal, audience, constraints)
   - Evidence/context pack (relevant facts only)
   - Output contract (format, length, ordering, citation rules)
   - Definition of done (checks, completeness, uncertainty handling)
3. Keep prompts specific but lean. Remove irrelevant background, duplicated instructions, and mixed signals.
4. Separate instructions from source material using explicit delimiters.
5. Ask as few follow-up questions as possible. If enough is known to produce a strong draft, do so and mark assumptions clearly.
6. When the task involves research or non-obvious facts, include grounding and citation rules.
7. When the task is execution-heavy, keep reasoning guidance light and focus on exact deliverables and constraints.
8. Provide reusable output, not just critique.
9. Match instruction granularity to the target model class: reasoning models perform better with goals and constraints; instruction-following models need explicit step-by-step guidance.

## Workflow
1. Diagnose the request
   - Identify the exact deliverable the prompt must produce.
   - Identify audience, environment, and likely model or tool context.
   - Detect missing essentials: inputs, constraints, sources, output shape, length, success criteria.
   - Detect contradictions, vague verbs, and hidden assumptions.

2. Choose response mode
   - **Prompt from scratch** for new work
   - **Prompt rewrite** for improving an existing prompt
   - **Prompt pack** for a reusable set of related prompts
   - **Prompt audit** for diagnosing failures
   - **Context compressor** for turning long background into an efficient context block

3. Build the prompt
   - Start with a role only if it sharpens behavior; skip empty theatrics.
   - State the goal in plain language.
   - Add only the context that materially affects output.
   - Specify constraints and non-negotiables.
   - Define exact output format and length.
   - Add verification and completion checks.
   - Add examples only if behavior is subtle or format compliance matters.
   - Place long-form context or reference documents before instructions when context window efficiency matters.

4. Validate the prompt
   - No contradictions
   - No hidden requirements
   - No ambiguous success criteria
   - Output format is explicit
   - Uncertainty and grounding behavior are explicit when needed
   - Prompt length is justified
   - Structural formatting matches target model preferences (see Model-specific considerations)

5. Return the result
   By default return:
   - final prompt
   - brief note on assumptions or placeholders
   - optional tightening options only if there are obvious unresolved choices

## Default output shape
Unless the user asks for something else, return:
1. **Recommended prompt**
2. **Assumptions / placeholders**
3. **Tightening options**

## Prompt construction rules
- Use short section headers.
- Prefer concrete nouns and verbs over abstract directives.
- Replace "be good at X" with observable instructions.
- Replace "make it concise" with explicit limits like "120 words max" or "3 bullets".
- State what to do when evidence is weak or inputs are missing.
- Preserve user-specified voice separately from task constraints.
- Never bury critical constraints in the middle of a paragraph.
- If the user wants a reusable prompt, use placeholders like `{{AUDIENCE}}`, `{{SOURCE_OF_TRUTH}}`, and `{{OUTPUT_FORMAT}}`.
- If the user wants a one-off prompt, fill in as much context as possible.
- Use delimiters consistently: XML tags, markdown headers, triple quotes, or separator lines -- pick one style per prompt and stick with it.

## Reference files
Use these only when helpful:
- [Playbook](references/PLAYBOOK.md) for the full context-engineering framework
- [Templates](references/TEMPLATES.md) for reusable prompt skeletons by task type
- [Rubric](references/RUBRIC.md) for auditing and tightening prompts before finalizing
- `sources/` contains vendor-authored prompting guides from Anthropic, OpenAI, Google, and Meta. Consult these when building a prompt targeted at a specific model family or when you need to verify a model-specific structural preference.

## Special handling
### If the user provides an existing prompt
- Preserve the user's intent.
- Diagnose specific failure modes first.
- Return an improved prompt plus a concise explanation of the deltas.

### If the user provides messy notes
- Convert notes into a structured brief before drafting the final prompt.

### If the user wants the agent to pair interactively
- Offer 2-3 candidate prompt strategies with tradeoffs.
- Recommend one.
- Draft the chosen version.

### If the prompt is for research
- Require explicit source hierarchy, citation behavior, and uncertainty handling.

### If the prompt is for writing or editing
- Separate **keep**, **improve**, and **do not change**.

### If the prompt is for code or analysis
- Make inputs, environment assumptions, correctness constraints, and output format explicit.

### If the prompt is for an agentic or tool-using system
- Define when to use each tool and when not to.
- Specify what to verify before taking actions, especially irreversible ones.
- Include planning and progress-tracking expectations (e.g., decompose into sub-tasks, confirm completion before yielding).
- Set boundaries for autonomy versus asking the user for confirmation.
- State how to handle tool errors, missing information, and ambiguous intent.

## Model-specific considerations
When the target model is known, adapt prompt structure to that model family. When unknown, default to markdown headers with clear delimiters -- the most portable format.

| Aspect | Claude (Anthropic) | GPT (OpenAI) | Gemini (Google) | Llama (Meta) |
|---|---|---|---|---|
| **Structural formatting** | XML tags (`<instructions>`, `<example>`, `<document>`) | Markdown headers + XML hybrid; `###` and `"""` delimiters | Clear section labels; place constraints at end of prompt | Plain text with explicit format instructions and examples |
| **Reasoning/thinking** | Adaptive thinking with `effort` parameter; promptable | Reasoning models need goals not steps; GPT models need explicit steps | Configurable thinking via system instructions | Chain-of-thought via explicit numbered steps in prompt |
| **Role hierarchy** | System prompt | `developer` > `user` > `assistant` priority chain | System instructions | System prompt with role definition |
| **Tool use** | Explicit triggers; parallel calling supported; avoid aggressive tool language in latest models | Include tool invocation examples; explain rationale before calls; use TODO tracking | Function declarations with schema | Role + restrictions + example pattern |
| **Key gotcha** | Latest models overtrigger on aggressive instructions -- use normal language | Reasoning vs GPT models need opposite prompting granularity | Place reference documents before the query | Combine role + rules + restrictions + example to force output format |

## Anti-patterns
Avoid:
- generic persona fluff
- stacked synonyms that say the same thing
- contradictory instructions
- overlong context dumps
- vague outputs like "make it better"
- examples that conflict with the requested format
- step-by-step reasoning scaffolds for models that reason internally
- aggressive trigger language ("CRITICAL", "MUST", "ALWAYS") when the model already follows normal instructions

## Final check
Before sending the prompt, silently verify:
- the task trigger is clear
- the output contract is explicit
- the prompt is shorter and clearer than the raw request
- the prompt is reusable if reusability was requested
- obvious failure modes were addressed
- structural formatting fits the target model (or is portable if target is unknown)
