# Prompt Engineering Playbook

Full methodology, grounded in 2023-2026 academic and frontier lab research. This file complements [SKILL.md](../SKILL.md) -- the skill contains the essentials needed to act; this playbook contains the detailed reasoning, citations, and per-vendor specifics.

## Contents
- [Goal](#goal)
- [The five-layer stack](#the-five-layer-stack)
- [Meta-prompting methods taxonomy](#meta-prompting-methods-taxonomy)
- [Pairing modes](#pairing-modes)
- [Build order](#build-order)
- [When to add examples](#when-to-add-examples)
- [Task-specific guidance](#task-specific-guidance)
- [Reasoning vs instruction-following: detailed guidance](#reasoning-vs-instruction-following-detailed-guidance)
- [Cross-model structural tips](#cross-model-structural-tips)
- [Model-specific gotchas (2025-2026)](#model-specific-gotchas-2025-2026)
- [Robustness and prompt brittleness](#robustness-and-prompt-brittleness)
- [Evaluation-iteration mode](#evaluation-iteration-mode)
- [Prompt-migration mode](#prompt-migration-mode)
- [Common prompt smells](#common-prompt-smells)
- [Reusable prompt skeleton](#reusable-prompt-skeleton)
- [Tightening tactics](#tightening-tactics)
- [Anti-pattern library](#anti-pattern-library)
- [Decision rule: what belongs in the prompt vs outside it](#decision-rule-what-belongs-in-the-prompt-vs-outside-it)
- [Final review checklist](#final-review-checklist)

## Goal
Create prompts that frontier models can execute correctly on the first try, and that remain effective across realistic variations in input and model updates.

## The five-layer stack
Use this order unless the task clearly does not need one of the layers.

1. **Persistent preferences** -- stable defaults that should apply across many tasks. Tone, decisiveness, default depth, citation expectations, formatting preferences.
2. **Task brief** -- goal, audience, known constraints, inputs and source of truth, what success looks like.
3. **Context pack** -- only the facts, prior decisions, or examples that materially change the answer. Prefer curated bullets over raw dumps. Separate instructions from source material with delimiters.
4. **Output contract** -- artifact type, required sections, order, length limits, format requirements, citation rules, placeholder policy.
5. **Definition of done** -- what must be covered, how uncertainty should be handled, what to do if evidence is thin, what to mark as blocked, required self-checks before finalizing.

## Meta-prompting methods taxonomy
This skill is used predominantly for meta-prompting -- using an LLM to draft, refine, or audit prompts for other LLMs (or for itself). The academic literature distinguishes three related-but-distinct disciplines. The boundaries are blurry and some methods sit at the intersection.

### 1. Manual prompt engineering
Human-written prompts refined through trial and error. Relies on domain expertise and intuition. Outputs are brittle: minor perturbations to phrasing or formatting can cause 5-10 percentage point accuracy swings on standard benchmarks.

### 2. Prompt optimization
Algorithmic search over the space of prompts to maximize a task metric. The search is automated; the human defines the objective and the development set. LLMs are called as part of the search, but the orchestrating logic is an optimization procedure.

- **APE** -- *Large Language Models Are Human-Level Prompt Engineers* (Zhou et al., arxiv 2211.01910). Treats instruction generation as program synthesis. On 24 NLP tasks, matched or exceeded human-written instructions on 19/24. Notably discovered the prompt *"Let's work this out in a step by step way to be sure we have the right answer"* as a better zero-shot CoT prompt than the human-written "Let's think step by step."
- **OPRO** -- *Large Language Models as Optimizers* (Yang et al., Google DeepMind, arxiv 2309.03409). LLM iteratively generates new candidate prompts from a running log of prior attempts and their scores. Reported up to 8% on GSM8K and up to 50% on Big-Bench Hard over human-designed baselines.
- **EvoPrompt** (arxiv 2309.08532). Uses LLMs as evolutionary operators (mutation / crossover) over a population of candidate prompts. Up to 25% on Big-Bench Hard tasks.

### 3. Meta-prompting
Using the LLM itself as an active agent in the orchestration of prompt engineering -- structured task decomposition, recursive refinement loops, conductor-orchestrator patterns, and self-improvement. The distinguishing features are (a) the LLM *plans and critiques*, not just generates candidates, and (b) natural-language reasoning is the richer learning signal.

- **Promptbreeder** -- *Self-Referential Self-Improvement Via Prompt Evolution* (Fernando et al., DeepMind, arxiv 2309.16797). Mutation-prompts themselves evolve alongside task-prompts. 99.7% on MultiArith vs APE's 95.8%. On ETHOS hate-speech classification, evolved a prompt reaching 89% vs 80% for a simple human-designed baseline ("Determine whether a text contains hate speech").
- **PromptAgent** -- *Strategic Planning with Language Models Enables Expert-level Prompt Optimization* (Wang et al., arxiv 2310.16427). Monte Carlo Tree Search over prompt refinements with error-feedback rewards. Evaluated on 12 tasks spanning BBH, domain-specific, and general NLP tasks.
- **Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding** (Suzgun & Kalai, arxiv 2401.12954; Stanford and Microsoft Research). The **conductor-model** pattern: one LM decomposes a task into subtasks, delegates to specialist instances, and integrates outputs with verification. Reported aggregate improvement of +17.1% over standard prompting, +17.3% over expert dynamic prompting, and +15.2% over multipersona prompting, averaged across Game of 24, Checkmate-in-One, and Python Programming Puzzles. The pattern is iterative: the conductor can re-dispatch specialists with refined instructions based on their outputs. This is the pattern behind template 8 in [TEMPLATES.md](TEMPLATES.md).
- **DSPy** (Khattab et al., Stanford, dspy.ai). Treats LM prompts as modular components in a computational graph, with a signature (interface) separate from the prompt implementation. Optimizers like MIPROv2 and GEPA learn prompts or weights from training data. An informal evaluation in DSPy's own documentation reports raising ReAct on HotPotQA from 24% to 51% using MIPROv2 on 500 examples at ~$2 cost and 20 minutes (not a paper-published benchmark).
- **TextGrad** (Yuksekgonul et al., arxiv 2406.07496). Automatic "differentiation" via natural language feedback -- LLMs provide rich textual critique that acts as a gradient surrogate. GPT-4o GPQA improved from 51% to 55%; +20% on LeetCode-Hard; applied to molecule design and radiation oncology planning.
- **GEPA** -- *Reflective Prompt Evolution Can Outperform Reinforcement Learning* (arxiv 2507.19457, 2025). Reflects in natural language on trajectories, proposes updates, and combines complementary lessons from a Pareto frontier of attempts. Outperforms GRPO (reinforcement learning) by 6% on average (and up to 20% on some tasks) while using up to 35x fewer rollouts. +12% on AIME-2025 over MIPROv2.
- **ProTeGi** -- *Automatic Prompt Optimization with "Gradient Descent" and Beam Search* (Pryzant et al., arxiv 2305.03495). Error-driven critique generation; beam search over multiple candidates to avoid premature convergence. The pattern behind template 9 in [TEMPLATES.md](TEMPLATES.md).
- **Self-Refine** -- *Iterative Refinement with Self-Feedback* (Madaan et al., NeurIPS 2023, arxiv 2303.17651). Same LM generates → critiques its own output → refines, looping until a stop condition. Reported improvements of 20%+ absolute across tasks on GPT-3.5 and GPT-4. The pattern behind template 13 in [TEMPLATES.md](TEMPLATES.md).
- **Self-Discover** -- *Large Language Models Self-Compose Reasoning Structures* (Zhou et al., Google DeepMind, arxiv 2402.03620). The LM selects and composes reasoning modules into a task-specific structure before solving. Strong gains on BBH and MATH over chain-of-thought baselines. This is a structured-decomposition meta-prompting pattern -- the model generates the reasoning scaffold for itself rather than being given one.
- **Chain-of-Verification (CoVe)** -- *Reducing Hallucination in Large Language Models* (Dhuliawala et al., arxiv 2309.11495). The LM generates its answer, then generates verification questions about its own claims, answers them independently, and revises. Strong hallucination-reduction pattern; directly relevant to the groundedness conditional gate. The pattern behind template 14 in [TEMPLATES.md](TEMPLATES.md).

### Key structural patterns that appear across meta-prompting methods
- **Hierarchical decomposition**: complex problems broken into specialist subtasks (Suzgun, Self-Discover).
- **Critic loops**: model errors generate natural language feedback that guides the next refinement cycle (ProTeGi, GEPA, TextGrad, Self-Refine).
- **Beam search / Pareto frontier**: multiple candidates maintained to avoid premature convergence (ProTeGi, GEPA).
- **Mutation-prompts** (Promptbreeder): the operators that generate prompt variants are themselves evolvable.
- **Error-driven refinement**: targeted critiques for specific failure modes beat general "improve this" instructions.
- **Natural language reasoning over errors** is a richer learning signal than scalar reward -- the core insight of GEPA, TextGrad, and Self-Refine.
- **Self-generated reasoning scaffolds** (Self-Discover): the LM generates the scaffold, outperforming fixed hand-designed scaffolds.
- **Verification-before-finalization** (CoVe, Self-Refine): generate, then explicitly verify, then revise.

### Limitations to remember
- **Benchmark brittleness**. Brittlebench (arxiv 2603.13285, 2026) documents up to 12% performance degradation under semantics-preserving perturbations, and single perturbations altering model rankings in up to 63% of cases. Optimized prompts may exploit benchmark artifacts rather than improving generalizable reasoning.
- **Base model capability ceiling**. Meta-prompting extracts latent capability; it cannot create capability that is not present in the base model.
- **Cost**. DSPy optimization ~$2/run on the informal ReAct example; GEPA requires multiple trajectory samples. At scale, costs accumulate.
- **LLM-as-judge biases**. Position bias, verbosity bias, self-preference bias, reference-score bias -- see [Evaluation-iteration mode](#evaluation-iteration-mode).

## Pairing modes
The skill supports seven modes. Choose the one that matches the user's request.

### 1. Prompt from scratch
Use when the user has a goal but no usable prompt.

Output: a finished prompt, assumptions or placeholders, optional note on how to adapt it.

### 2. Prompt rewrite
Use when the user already has a prompt.

Process: identify failure modes, preserve intent, remove contradictions and ambiguity, rewrite with a clearer output contract.

### 3. Prompt pack
Use when the workflow needs multiple related prompts.

Typical pack: discovery prompt, execution prompt, critique or QA prompt, finalization prompt.

### 4. Prompt audit
Use when the user wants diagnosis rather than a rewrite.

Return: strongest failure modes, why they matter, revised wording for the most important fixes.

### 5. Context compressor
Use when the user provides too much background.

Process: extract only decision-relevant facts, move raw notes to an appendix or omit them, rewrite into a compact context block (template 6 in [TEMPLATES.md](TEMPLATES.md)). For automated compression of long documents before they reach the prompt, see LLMLingua in [CONTEXT_ENGINEERING.md](CONTEXT_ENGINEERING.md#automated-prompt-compression).

### 6. Evaluation iteration
Use when the user shares an existing prompt **plus real outputs** (the prompt is running but producing imperfect results). See [Evaluation-iteration mode](#evaluation-iteration-mode) below for details.

### 7. Prompt migration
Use when the user wants to port a prompt from one model family to another (e.g., Claude → GPT-5, GPT-4 → Claude 4.6, instruction-following → reasoning). See [Prompt-migration mode](#prompt-migration-mode) below.

## Build order
When drafting, use this sequence:
1. one-sentence objective
2. audience and environment
3. target model class (reasoning vs instruction-following, or adaptive / routed)
4. constraints and non-negotiables
5. source of truth / grounding rules
6. output contract
7. completion rules
8. trust boundary (if the prompt ingests untrusted content)
9. optional examples
10. self-verification step

## When to add examples
Add examples only when they materially improve reliability:
- strict structured output
- non-obvious tone matching
- complex transformations
- edge-case behavior

Do not add examples when they merely repeat the same instructions. On reasoning-first models, start zero-shot and add few-shot only if results are uneven -- the OpenAI reasoning best-practices doc explicitly recommends this ordering.

**For robustness**, when you do include few-shot examples for a reusable prompt, consider diversifying their formatting style. The Mixture of Formats (MOF) technique (arxiv 2025.naacl-srw.51) reduces style-induced brittleness by varying the format of few-shot examples rather than using a uniform template. **Caveat**: MOF was evaluated on Llama-2-13B, Llama-3-70B, and Falcon-11B -- its applicability to frontier commercial models is a reasonable extrapolation but not directly validated.

## Task-specific guidance

### For research and synthesis
Emphasize source hierarchy, citation rules, uncertainty handling, breadth vs depth, stop conditions, and trust boundary for any ingested sources. Consider Chain-of-Verification (template 14) when hallucination risk is material.

### For writing and editing
Emphasize audience, voice, what must stay fixed, what to improve, output length and structure.

### For code and analysis
Emphasize environment assumptions, correctness requirements, inputs and outputs, edge cases, test or validation expectations.

### For tool-using agents
Emphasize when to use tools, what must be checked before acting, what counts as enough evidence, when to stop and surface uncertainty, planning and sub-task decomposition before execution, progress tracking, boundaries between autonomous action and user confirmation, handling of tool errors, effort-scaling rules (see template 11), filesystem persistence of intermediate findings to avoid telephone-game compression, and trust boundary discipline for tool output. **Note**: when the target is a reasoning-first model, strip prescribed numbered workflows -- the model should plan internally.

## Reasoning vs instruction-following: detailed guidance
This is the most consequential structural decision in 2025-2026 prompt design, but it is not a clean binary.

### What changed between 2023 and 2025-2026
- The release of reasoning models (OpenAI o1/o3/o4-mini, Claude with extended thinking, Gemini 2.5 thinking) created a hard split in optimal prompting strategy.
- Adaptive and routed models complicate the picture: **Claude 4.6 with adaptive thinking** and **GPT-5 with routing** dynamically select a reasoning or fast path based on task complexity, so the same prompt can invoke either mode on different turns.
- OpenAI's reasoning best-practices documentation (developers.openai.com/api/docs/guides/reasoning-best-practices) deprecates chain-of-thought prompting for reasoning models: the phrasing on the current page notes that CoT "may not enhance performance and can sometimes hinder it."
- Anthropic's Claude 4.6 prompting documentation recommends adaptive thinking and discourages prescriptive step-by-step plans; the community shorthand "think thoroughly" is a common pattern but not a phrase officially endorsed in the primary docs.
- Wharton Generative AI Labs' *Playing Pretend: Expert Personas Don't Improve Factual Accuracy* (Prompting Science Report 4, December 2025, arxiv 2512.05858) tested expert persona prompting on GPQA Diamond (198 questions) and MMLU-Pro (300 questions) across 6 models (GPT-4o, GPT-4o-mini, o3-mini, o4-mini, Gemini 2.0 Flash, Gemini 2.5 Flash) with 25 trials per question. Result: expert personas do not reliably improve accuracy; domain-mismatched expert personas show marginal differences; low-knowledge personas (layperson, child, toddler) clearly reduce accuracy.

### Reasoning-first playbook
When the target is explicitly a reasoning-first model, or the target is adaptive and you want the prompt to degrade gracefully:
- **Zero-shot first.** Reasoning models often do not need few-shot examples and can perform worse with them. Add few-shot only if results are uneven.
- **No chain-of-thought prefacing.** The model reasons internally. Telling it to "think step by step" or "explain your reasoning" is at best redundant.
- **No personas.** Wharton 2025. Focus on the task, not on who is doing it. A persona is OK only when the role meaningfully constrains behavior (e.g., "You are a SQL linter that returns only corrected SQL") -- it must change what the model does, not just decorate.
- **No emotional appeals.** Evidence is mixed across studies; do not rely on them as a lifting technique.
- **Specific end goals and success criteria.** "The answer must satisfy X, Y, and Z." Let the model figure out how to get there.
- **Developer > user message priority.** On OpenAI reasoning models, put authoritative instructions in `developer` messages, not `user` messages.
- **Self-verification.** "Before finishing, verify your answer against [criteria]." This is not a reasoning scaffold -- it is a completion check. It catches errors especially on math and code.
- **Adaptive thinking**: on Claude 4.6 with adaptive thinking, rely on the model's internal decision about depth. A common community pattern is to use "think thoroughly" or similar lightweight framing, though this is not an officially sanctioned phrase in Anthropic's primary docs. Hand-written step-by-step plans tend to be counterproductive.

### Instruction-following playbook
When the target is a standard instruction-following model:
- **Explicit steps when order matters.** Numbered lists or ordered bullets.
- **Role only if it sharpens behavior.** "You are a SQL linter" is useful; "You are a world-class senior database expert" is fluff.
- **Delimiters.** XML tags for Claude; `###` and `"""` for OpenAI; labeled sections for Gemini; plain text with explicit format markers for Llama.
- **Few-shot examples (3-5)** when format is subtle, tone must match precisely, or edge-case behavior matters.
- **Numerical constraints.** "120 words max", not "be concise".
- **Verification and completion checks** as an explicit step at the end.

### Handling adaptive and routed models
- **Claude 4.6 with adaptive thinking**: the prompt is written once; the model routes per turn. Design with the reasoning-first playbook in mind (it degrades more gracefully on the instruction-following path than the reverse).
- **GPT-5 with routing**: similar principle. Avoid constructs that are actively harmful on either path -- so no CoT prefacing (harmful on the reasoning path) and no vague unstructured goals (harmful on the fast path). State specific end goals and success criteria, use clear delimiters, and trust the router.
- **When extended thinking is explicitly enabled or disabled** on Claude, the word-level gotchas matter (see model-specific gotchas below).

## Cross-model structural tips
When building prompts that may run on different model families, keep these differences in mind:

- **Claude** responds best to XML tags (`<instructions>`, `<example>`, `<document>`) for separating prompt sections. Use descriptive, consistent tag names. Claude 4.6 removed assistant message prefilling -- use Structured Outputs for format guarantees instead.
- **OpenAI** docs recommend markdown headers (`###`) and triple-quote delimiters (`"""`) to mark section boundaries. The `developer` / `user` / `assistant` priority chain gives developer instructions higher priority. Structured Outputs with a strict JSON Schema is the recommended approach for critical data extraction.
- **Google Gemini** guidance emphasizes placing constraints and rules at the **end** of the prompt, after context and examples, for best adherence. Reference documents should come before the query. Gemini 2.5 supports thinking budgets and returns thought signatures for multi-turn tool-calling work.
- **Llama** models benefit from combining a role declaration, explicit restrictions, and a concrete example to lock down output format -- especially for structured outputs like JSON.
- **When the target model is unknown**, use markdown headers with clear section labels. This is the most portable format across model families.

Empirical note: studies of XML vs markdown for prompt structuring show **no single format universally wins**. Effectiveness varies by model family and task type. Pick the format recommended by the target vendor; pick portable markdown if the target is unknown.

## Model-specific gotchas (2025-2026)
Full details per family -- consult when the target is known.

### Claude 4.6 (Anthropic)
- **Aggressive trigger language** (`CRITICAL`, `MUST`, `ALWAYS`) can cause overtriggering on system-prompt-driven tool or skill invocation. The primary Anthropic guidance is specifically about tool/skill triggering; the safest generalization is to prefer normal imperative phrasing for rules and reserve strong language for genuine hard constraints.
- **Assistant-message prefilling is removed** in Claude 4.6. Use Structured Outputs / strict schemas for format guarantees instead.
- **Word "think" is a documented sensitivity on Claude Opus 4.5** when extended thinking is disabled. The skill treats this as a probable sensitivity on Claude Opus 4.6 as well, but the specific documentation is for 4.5. When extended thinking is off, prefer "consider", "evaluate", or "reason through" instead of "think".
- **Adaptive thinking** is the recommended default in 4.6. Let the model route per turn rather than trying to toggle modes at prompt-write time.

### GPT-5 and o-series (OpenAI)
- Reasoning models: no CoT prefacing. Zero-shot first.
- `developer` > `user` > `assistant` priority chain. Put authoritative rules in `developer` messages.
- `reasoning_effort` dial (low/medium/high) controls exploration depth. Tune externally.
- **Tool preambles** (explicit upfront plans plus progress updates) improve agentic UX on long-running tool trajectories.
- **Structured Outputs** with JSON Schema for any critical extraction task.
- GPT-5 uses routing between fast and reasoning paths -- design for both.

### Gemini 2.5 (Google)
- **Constraints at the end.** Place reference documents before the query, then the query, then the constraints.
- **Configurable thinking budgets** (low / medium / high).
- **Thought signatures** returned for tool-using multi-turn work -- pass them back in subsequent calls.
- **Stateless API**: every request is independent; the model has no server-side memory of prior calls.

### Llama (Meta)
- Combine role + rules + restrictions + concrete example to lock down structured output, especially JSON.
- More sensitive to format drift than frontier commercial models -- include the schema and an example of a compliant output.

## Robustness and prompt brittleness
Prompt brittleness is a first-class production concern.

### Evidence
- **Brittlebench** (arxiv 2603.13285, 2026): semantics-preserving perturbations degrade performance up to 12%, and alter model rankings in up to 63% of cases. Performance variance decomposition reveals that such perturbations account for up to half of performance variance for a given model. (Use "up to" framing -- these are upper bounds, not flat averages.)
- **Format sensitivity** (arxiv 2025.naacl-srw.51): small changes in prompt format style lead to significant performance fluctuations on Llama-2/Llama-3/Falcon. The Mixture of Formats (MOF) technique -- diversifying the formatting of few-shot examples -- reduces style-induced brittleness on those models. Frontier commercial model applicability is inferential, not directly tested.
- **Model drift**: Chen, Zaharia, Zou 2023 (*How Is ChatGPT's Behavior Changing Over Time?*, arxiv 2307.09009) reported GPT-4 accuracy dropping from 84% to 51% between March and June 2023 on a prime number identification task with no prompt changes. This result has been contested on methodology grounds (the test set was imbalanced toward primes and the March model had a prime-predicting bias, so the "drop" partly reflects a bias flip rather than a capability loss -- see Narayanan's critique). The broader point -- that model updates can change prompt behavior without prompt changes -- remains valid and is documented across other experiments as well.

### Tactics to improve robustness
1. **Test against semantically equivalent reformulations.** Before shipping a reusable prompt, run it on 3-5 paraphrases of the same input and confirm that quality does not swing.
2. **Diversify few-shot example formats** (MOF) -- with the caveat above about model applicability.
3. **Define regression test sets.** A small set of representative inputs with expected outputs, re-run on any prompt change or model update.
4. **Version prompts semantically.** MAJOR for structural changes, MINOR for added features, PATCH for typo fixes. Log the change and why.
5. **Avoid reliance on a single triggering phrase.** If the prompt's effectiveness depends on one specific word or phrasing, it is brittle by definition.
6. **Prefer positive to negative instructions** as a weak default. The "ironic process" effect (naming a forbidden behavior can cue it) has some evidence, but recent research shows frontier models handle negative instructions better than older models did. Treat this as a tiebreaker, not a hard rule.

## Evaluation-iteration mode
This is the sixth mode. Use it when the user shares a prompt and real outputs from running it.

### Process
1. **Inspect the outputs, not just the prompt text.** The prompt might look fine; the outputs reveal what is actually going wrong.
2. **Group failures by root cause.** Distinct failure modes need distinct fixes. Common causes:
   - Task misunderstanding (the model is solving a different problem)
   - Missing context (the model lacks information it needs)
   - Format violation (output shape is wrong)
   - Factual / logical error (reasoning failure)
   - Injected instruction (untrusted content redirected the model)
   - Brittleness (a specific input phrasing broke the prompt)
3. **Generate 3-4 targeted variants.** Each variant addresses one failure mode. Do not stack all fixes into one variant; you lose the ability to diagnose what actually helped. This is the ProTeGi pattern; see template 9 in [TEMPLATES.md](TEMPLATES.md).
4. **Recommend a regression test set.** 5-10 representative inputs including at least one of each failure mode. The user should re-run the test set after accepting any variant.
5. **Flag robustness issues explicitly.** If the failures look like brittleness rather than a true logic gap, say so -- the fix may be tactics from the [Robustness section](#robustness-and-prompt-brittleness), not a deeper rewrite.

### LLM-as-judge warnings
If the user plans to evaluate variants using an LLM judge, warn them about documented biases:
- **Position bias**: judges tend to favor the first answer in pairwise comparisons. Mitigate by randomizing position or averaging over both orderings.
- **Verbosity bias**: judges tend to prefer longer responses even when they are not more accurate. Mitigate by normalizing for length or using length-controlled metrics.
- **Self-preference bias**: a judge tends to prefer outputs from its own model family. Mitigate by using a different family as judge.
- **Reference-score bias**: fixed scoring rubrics can systematically distort judgments. Mitigate by calibrating the judge against human-rated examples.

These biases are documented across multiple 2023-2025 papers including *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge* (NeurIPS 2024) and *A Survey on LLM-as-a-Judge* (arxiv 2411.15594). MT-Bench (Zheng et al. 2023) reported 80%+ agreement between calibrated LLM judges and human preferences; the calibration step is non-negotiable for high-stakes evaluation.

## Prompt-migration mode
This is the seventh mode. Use it when the user wants to port a prompt from one model family to another.

### Process
1. **Diagnose the source prompt's target-model features.** Identify elements that depend on the source model's structural preferences: XML tags, `developer` messages, prefilling, specific tool-calling formats, `reasoning_effort` dial values, thinking budgets, thought signatures.
2. **Identify non-portable features.** Claude 4.6 does not support assistant-message prefilling; GPT-5 does not use XML as its native structural element; Gemini places constraints at the end, not top; Llama needs explicit format examples where Claude does not. Make a short list of features that must be rebuilt.
3. **Preserve intent, rebuild structure.** Do not translate literally. Re-layer the prompt in the five-layer stack and re-choose delimiters, tag conventions, and message roles for the target model. Apply the appropriate reasoning-vs-instruction-following playbook.
4. **Strip source-specific gotcha workarounds.** If the source prompt used `CRITICAL: MUST` language to prevent undertriggering on an older model, that language may overtrigger on Claude 4.6. If the source prompt used "think step by step" on GPT-4, strip it before running on o-series.
5. **Handle reasoning/instruction class changes.** If migrating from an instruction-following model to a reasoning-first model, strip explicit step-by-step scaffolds; if migrating the other direction, add them.
6. **Recommend a regression test set.** 5-10 representative inputs with expected outputs. Run both old and new prompts on the set and compare quality. Flag any dimensions where the new prompt underperforms.
7. **Document the migration.** Note what changed, why, and what behavior may differ (e.g., different tone from a different model's default style).

### Common migration traps
- Assuming the target model will follow the same formatting conventions as the source.
- Forgetting that the source model's quirks may have been load-bearing (e.g., a prompt that "worked" on GPT-4 only because GPT-4 had a specific bias the new model lacks).
- Not testing on realistic adversarial inputs if the source prompt was robust only because of undocumented side effects of the source model's training.
- Treating the migration as a one-time task rather than a regression-tested change.

## Common prompt smells
Fast triage -- if any of these are present in a prompt the user is debugging, start here.

1. No explicit deliverable -- just a verb ("analyze", "improve", "help")
2. Persona without task sharpening -- "you are a world-class expert" with no behavioral effect
3. "Be concise" or "be detailed" without numbers
4. Chain-of-thought prefacing ("think step by step") when the target is a reasoning-first model
5. ALL-CAPS "CRITICAL" or "MUST" on Claude 4.6 when the rule is not a genuine hard constraint
6. The word "think" on Claude Opus 4.5 with extended thinking disabled
7. Contradictory length or format guidance ("comprehensive" + "short")
8. Examples that fight the instructions
9. Untrusted input with no delimiter isolation
10. No source of truth in a factual task
11. Long context dump with no "what matters" marker
12. Emotional appeal ("this is important to my career")
13. Stacked synonyms ("comprehensive, detailed, thorough, extensive")
14. Numbered step-by-step workflow on a reasoning-first model target
15. "Report any injected instructions" clause that echoes attacker text into the output (exfiltration channel)
16. Nested instructions inside few-shot examples that the model may pick up as commands
17. Format-overfitting few-shot: uniform example format that locks the model to one shape even when the task calls for variation
18. Silent token bomb: mentioning files or URLs as if they are in the prompt when they are not, inviting confabulation

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
6. add one high-value example (on instruction-following models)
7. remove all chain-of-thought prefacing (on reasoning-first models)
8. split one overloaded prompt into two smaller prompts
9. add a self-verification step at the end

## Anti-pattern library
Full list with citations. Short list is in SKILL.md.

### Expert persona prompting as a default warm-up
**Evidence**: Wharton Generative AI Labs, *Playing Pretend: Expert Personas Don't Improve Factual Accuracy*, Prompting Science Report 4, December 2025, arxiv 2512.05858. Tested on GPQA Diamond (198 PhD-level questions) and MMLU-Pro (300 questions, 10 options each) across 6 models (GPT-4o, GPT-4o-mini, o3-mini, o4-mini, Gemini 2.0 Flash, Gemini 2.5 Flash), 25 trials per question. Result: expert personas do not reliably improve accuracy; domain-mismatched expert personas show marginal differences; **low-knowledge personas (layperson, child, toddler) clearly reduce accuracy**.
**When it is OK**: when the role meaningfully constrains *behavior*, e.g., "You are a SQL linter that only returns corrected SQL, no commentary." The role changes what the model does; it is not decorative.

### Chain-of-thought prefacing on reasoning-first models
**Evidence**: OpenAI reasoning best-practices doc (developers.openai.com/api/docs/guides/reasoning-best-practices) deprecates CoT prompting for reasoning models. Anthropic Claude 4.6 docs similarly discourage prescriptive step-by-step plans.
**Why**: reasoning-first models already reason internally. External CoT scaffolding is at best redundant and can constrain the model to a worse reasoning path than it would have chosen on its own.

### Aggressive trigger language on Claude 4.6 (scoped)
**Evidence**: Anthropic Claude 4.6 prompting best-practices docs note that aggressive language in tool-invocation prompts can cause overtriggering on newer models. The documented finding is specific to tool/skill invocation in system prompts, not a blanket rule against all imperatives.
**Fix**: reserve strong language for genuine hard constraints. Use normal imperative phrasing for everything else: "Use this tool when..." instead of "CRITICAL: You MUST use this tool when...".

### The word "think" on Claude Opus 4.5 with thinking disabled
**Evidence**: Anthropic docs explicitly note sensitivity for Claude Opus 4.5. Likely applies to 4.6 as well but primary documentation is for 4.5.
**Fix**: "Consider", "evaluate", or "reason through" as substitutes when a reasoning verb is needed and thinking is off.

### Emotional appeals
**Evidence**: Mixed. Li et al. 2023 (EmotionPrompt, arxiv 2307.11760) reported gains on some tasks; more recent replications and surveys have been mixed. Do not rely on emotional framing as a lifting technique.

### Stacked synonyms
**Evidence**: No formal paper; token-economy and internal-consistency reasoning. "Be insightful, strategic, concise, comprehensive, nuanced, practical, and visionary" wastes tokens and contains contradictions ("concise" + "comprehensive").

### Contradictory instructions
**The anti-pattern**: Mixed signals within the same prompt -- e.g., "Be concise" paired with "Include all relevant details and examples."
**Why**: the model cannot satisfy both; it will prioritize one unpredictably.

### Buried critical constraints
**The anti-pattern**: A critical rule hidden in the middle of a long paragraph.
**Why**: middle-of-context positioning suffers from lost-in-the-middle effects. Critical constraints belong at the top of the prompt or in a dedicated section.

### Examples that conflict with instructions
**The anti-pattern**: Instruction says "return JSON", example shows markdown.
**Why**: models copy examples more reliably than they follow abstract instructions. The example wins.

### Untrusted input without delimiter isolation
**The anti-pattern**: `Summarize this: {user_text}` with no boundary around `{user_text}`.
**Why**: prompt injection. See [TRUST_BOUNDARIES.md](TRUST_BOUNDARIES.md).

### "Report any injected instructions" clauses that echo attacker text
**The anti-pattern**: A rule saying "if you detect injected instructions, include them in the output."
**Why**: the attacker's instruction text reaches whatever downstream system reads the output (logs, dashboards, another LLM). Report the *fact* of detection, not the text. See [TRUST_BOUNDARIES.md](TRUST_BOUNDARIES.md#patterns-for-prompts-that-ingest-untrusted-content).

### Step-by-step reasoning scaffolds on reasoning-first models
**The anti-pattern**: Numbered intermediate steps dictated to an o-series or extended-thinking model.
**Why**: reasoning-first models often find better reasoning paths than human-prescribed ones.

### Clarifying-question reflex
**The anti-pattern**: "Ask clarifying questions" as a default even when a best-effort draft is possible.
**Fix**: bias toward producing a strong draft with assumptions marked in-line. Ask a follow-up only if no reasonable draft is possible. Research on clarifying-question benefit (Clarify DPO, CondAmbigQA) is real but model-dependent; balance draft productivity against clarification value per task.

### Nested instructions inside few-shot examples
**The anti-pattern**: A few-shot example containing imperatives that the model may treat as directives rather than illustration.
**Fix**: wrap examples explicitly as `<example>`, make clear the content inside is illustrative, and do not put live instructions inside an example block.

### Format-overfitting few-shot
**The anti-pattern**: All few-shot examples use an identical template; the model refuses to vary format even when the task calls for variation.
**Fix**: use diverse formats (MOF-inspired) when format is not the thing being demonstrated.

### Silent token bomb
**The anti-pattern**: Referring to a file, URL, or tool output as if it is in the prompt when it is not.
**Why**: the model confabulates content to fit.
**Fix**: only reference data that is actually in the prompt, or use a tool call to fetch it.

## Decision rule: what belongs in the prompt vs outside it
Put something inside the prompt only if it changes execution quality.

Keep outside the prompt when it is:
- maintenance commentary
- background the model will not actually use
- duplicate wording
- examples that do not match the current task
- acknowledgment of constraints the model already obeys

## Final review checklist
Before shipping a prompt, verify:
- one clear objective
- one clear output contract
- one clear completion standard
- explicit handling of uncertainty
- no instruction conflicts
- no unnecessary context
- structural formatting fits the target model class
- trust boundaries are explicit if the prompt ingests untrusted content
- core rubric score ≥ 14/16 (see [RUBRIC.md](RUBRIC.md))
- any triggered conditional gates (groundedness, safety, robustness, privacy) pass
