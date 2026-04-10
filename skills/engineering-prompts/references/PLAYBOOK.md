# Prompt Engineering Playbook

## Contents
- [The five-layer stack](#the-five-layer-stack)
- [Common prompt failures](#what-good-prompt-work-usually-fixes)
- [Pairing modes](#pairing-modes) (from scratch, rewrite, pack, audit, compressor)
- [Build order](#build-order)
- [When to add examples](#when-to-add-examples)
- [Task-specific guidance](#task-specific-guidance) (research, writing, code, agents)
- [Cross-model structural tips](#cross-model-structural-tips)
- [Reusable prompt skeleton](#reusable-prompt-skeleton)
- [Tightening tactics](#tightening-tactics)
- [Anti-pattern library](#anti-pattern-library)
- [Decision rule: prompt vs outside](#decision-rule-what-belongs-in-the-prompt-vs-outside-it)
- [Final review checklist](#final-review-checklist)

## Goal
Create prompts that capable models can execute correctly on the first try.

## The five-layer stack
Use this order unless the task clearly does not need one of the layers.

1. **Persistent preferences**
   - Stable defaults that should apply across many tasks
   - Tone, decisiveness, default depth, citation expectations, formatting preferences

2. **Task brief**
   - Goal
   - Audience
   - Known constraints
   - Inputs and source of truth
   - What success looks like

3. **Context pack**
   - Only the facts, prior decisions, or examples that materially change the answer
   - Prefer curated bullets over raw dumps
   - Separate instructions from source material with delimiters

4. **Output contract**
   - Artifact type
   - Required sections
   - Order
   - Length limits
   - Format requirements
   - Citation rules
   - Placeholder policy

5. **Definition of done**
   - What must be covered
   - How uncertainty should be handled
   - What to do if evidence is thin
   - What to mark as blocked
   - Required self-checks before finalizing

## What good prompt work usually fixes
Most weak prompts fail because of one or more of these:
- no explicit deliverable
- no source of truth
- no format contract
- no completion criteria
- contradictory instructions
- hidden constraints introduced too late
- too much irrelevant background
- length guidance that is vague instead of explicit

## Pairing modes

### 1. Prompt from scratch
Use when the user has a goal but no usable prompt.

Output:
- a finished prompt
- assumptions or placeholders
- optional note on how to adapt it

### 2. Prompt rewrite
Use when the user already has a prompt.

Process:
- identify failure modes
- preserve intent
- remove contradictions and ambiguity
- rewrite with a clearer output contract

### 3. Prompt pack
Use when the workflow needs multiple related prompts.

Typical pack:
- discovery prompt
- execution prompt
- critique or QA prompt
- finalization prompt

### 4. Prompt audit
Use when the user wants diagnosis rather than a rewrite.

Return:
- strongest failure modes
- why they matter
- revised wording for the most important fixes

### 5. Context compressor
Use when the user provides too much background.

Process:
- extract only decision-relevant facts
- move raw notes to an appendix or omit them
- rewrite into a compact context block

## Build order
When drafting, use this sequence:
1. one-sentence objective
2. audience and environment
3. constraints and non-negotiables
4. source of truth / grounding rules
5. output contract
6. completion rules
7. optional examples

## When to add examples
Add examples only when they materially improve reliability:
- strict structured output
- non-obvious tone matching
- complex transformations
- edge-case behavior

Do not add examples when they merely repeat the same instructions or risk anchoring the model to a narrow pattern.

## Task-specific guidance

### For research and synthesis
Emphasize:
- source hierarchy
- citation rules
- uncertainty handling
- breadth vs depth
- stop conditions

### For writing and editing
Emphasize:
- audience
- voice
- what must stay fixed
- what to improve
- output length and structure

### For code and analysis
Emphasize:
- environment assumptions
- correctness requirements
- inputs and outputs
- edge cases
- test or validation expectations

### For tool-using agents
Emphasize:
- when to use tools
- what must be checked before acting
- what counts as enough evidence
- when to stop and surface uncertainty
- planning and sub-task decomposition before execution
- progress tracking (TODO lists, structured state files)
- boundaries between autonomous action and user confirmation
- handling of tool errors and ambiguous tool results

### Cross-model structural tips
When building prompts that may run on different model families, keep these differences in mind:
- Claude responds best to XML tags (`<instructions>`, `<example>`, `<document>`) for separating prompt sections. Use descriptive, consistent tag names.
- OpenAI docs recommend markdown headers (`###`) and triple-quote delimiters (`"""`) to mark section boundaries. Their `developer` / `user` role split gives developer instructions higher priority.
- Google Gemini guidance emphasizes placing constraints and rules at the end of the prompt, after context and examples, for best adherence.
- Llama models benefit from combining a role declaration, explicit restrictions, and a concrete example to lock down output format -- especially for structured outputs like JSON.
- When the target model is unknown, use markdown headers with clear section labels. This is the most portable format across model families.

## Reusable prompt skeleton

```text
You are my {{ROLE}}.

Goal:
- {{GOAL}}

Audience:
- {{AUDIENCE}}

Relevant context:
- {{RELEVANT_CONTEXT}}
- {{PRIOR_DECISIONS}}

Constraints:
- {{CONSTRAINTS}}
- {{DO_NOT_CHANGE}}

Output contract:
- Return {{ARTIFACT_TYPE}}
- Sections: {{SECTIONS}}
- Length: {{LENGTH_LIMIT}}
- Format: {{FORMAT_RULES}}
- Citations: {{CITATION_RULES}}

Definition of done:
- {{DONE_CRITERIA}}
- If evidence is weak, {{UNCERTAINTY_RULE}}
- Before finalizing, check {{CHECKS}}
```

## Tightening tactics
When a prompt underperforms, try these in order:
1. make the deliverable explicit
2. add or sharpen the source of truth
3. add exact output shape and length
4. remove contradictions and duplicate instructions
5. define what to do when inputs are missing
6. add one high-value example
7. split one overloaded prompt into two smaller prompts

## Anti-pattern library
Avoid these:
- “Be insightful, strategic, concise, comprehensive, nuanced, practical, and visionary.”
- “Use the provided context” when the prompt never says which facts matter.
- “Answer in a clear format” without specifying the format.
- “Ask clarifying questions” as a default even when a best-effort draft is possible.
- “Think harder” instead of defining what needs to be checked.

## Decision rule: what belongs in the prompt vs outside it
Put something inside the prompt only if it changes execution quality.

Keep outside the prompt when it is:
- maintenance commentary
- background the model will not actually use
- duplicate wording
- examples that do not match the current task

## Final review checklist
Before shipping a prompt, verify:
- one clear objective
- one clear output contract
- one clear completion standard
- explicit handling of uncertainty
- no instruction conflicts
- no unnecessary context
