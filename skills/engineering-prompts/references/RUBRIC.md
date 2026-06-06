# Prompt Review Rubric

Score each dimension from 0 to 2. The rubric has **8 core dimensions** that apply to every prompt and **4 conditional gates** that apply only when triggered.

## Scope and limits of this rubric
This rubric measures **prompt craft** -- whether the prompt is well-specified and aligned to its target model. It does **not** measure task merit ("should this task be done at all?"), legal or regulatory compliance, or downstream impact. A prompt can score 16/16 on this rubric and still be a bad thing to ship if the underlying task is harmful, illegal, or pointless. Rubric scores are necessary but not sufficient for shipping.

## Core dimensions (always scored; max 16)

### 1. Goal clarity
- 0: vague or implied
- 1: somewhat clear but incomplete
- 2: explicit objective and deliverable

### 2. Context quality
- 0: missing key background or overloaded with irrelevant detail
- 1: mixed relevance
- 2: lean, decision-relevant context only

### 3. Constraints
- 0: missing or hidden
- 1: partial
- 2: explicit and prioritized (with numbers, not adjectives)

### 4. Output contract
- 0: unspecified
- 1: partially specified
- 2: exact artifact, sections, length, and format are clear

### 5. Completion criteria
- 0: no definition of done
- 1: soft success criteria only
- 2: explicit checks for completeness, uncertainty handling, and blocker handling

### 6. Internal coherence
- 0: contradictory instructions or ambiguous phrasing
- 1: mostly consistent with some mixed signals
- 2: coherent and unambiguous; no instructions fighting each other

### 7. Reusability
- 0: too tied to one chat; not reusable if reusability was requested
- 1: partly reusable
- 2: uses clean placeholders or filled context appropriately for the intended lifetime

### 8. Model-class alignment
- 0: the prompt's structure contradicts the target model class (e.g., chain-of-thought prefacing and rigid step-by-step for a reasoning model; or vague goals with no steps for an instruction-following model)
- 1: mostly aligned but contains at least one element that the target class handles poorly
- 2: structure, tone, and scaffolding match the target model class; no anti-patterns for that class; target-specific gotchas are avoided
- **Why this dimension exists**: the reasoning-vs-instruction-following split is the most consequential structural decision in 2025-2026 prompt engineering. Without this dimension, a CoT-prefaced prompt targeted at a reasoning model can score 14/14 on the older 7-dimension rubric while being actively wrong for the target.

## Conditional gates (scored only if triggered; each gate must pass at its threshold)

### G1. Groundedness -- trigger: the prompt involves factual claims, research, or citations
- 0: no source of truth specified; hallucination risk unmanaged
- 1: source hierarchy mentioned but citation rules or uncertainty handling are vague
- 2: explicit source hierarchy, citation rules, and uncertainty handling ("label weak evidence; surface contradictions")
- **Gate passes at 2.** Grounded in Anthropic's guidance on grounded generation and long-context faithfulness research.

### G2. Safety and injection resistance -- trigger: the prompt ingests untrusted content (user text, tool output, scraped data, retrieved documents)
- 0: untrusted content is not isolated; no instruction hierarchy
- 1: delimiter isolation present but trust rules are vague
- 2: explicit trust boundaries, delimiter isolation, instruction hierarchy (developer > user > tool output), a rule that untrusted content cannot override system directives, **and** the prompt uses an empirically stronger defense (spotlighting, Structured Outputs with strict schema, or paraphrase pre-pass) when the attack surface is broad (public users, scraped web, high-stakes pipelines)
- **Gate passes at 2.** Grounded in OWASP LLM01:Prompt Injection, Wallace et al. 2024 (*The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*, arxiv 2404.13208), and Microsoft spotlighting research (arxiv 2403.14720).
- **Important caveat**: passing this gate reduces but does not eliminate injection risk. Empirical attack-success-rate benchmarks (Becker, AgentDojo, PromptArmor) show that even well-constructed instruction-hierarchy + delimiter defenses leave significant residual attack surface on frontier models. For high-stakes deployments, pair the prompt defense with runtime guardrails (allow-list tool scoping, output validation, rate limiting). See [TRUST_BOUNDARIES.md](TRUST_BOUNDARIES.md).

### G3. Robustness -- trigger: the prompt will be reused across many inputs or across model updates
- 0: performance depends on a single phrasing; no diversity in examples; no regression plan
- 1: some reformulation testing mentioned but incomplete
- 2: prompt has been or will be tested against semantically equivalent reformulations; few-shot examples (if present) use diverse formats; a regression test set is defined
- **Gate passes at 2.** Grounded in Brittlebench (arxiv 2603.13285: up to 12% degradation from semantics-preserving perturbations; single perturbations alter model rankings in up to 63% of cases). Note: Mixture of Formats (MOF, arxiv 2025.naacl-srw.51) is a supporting tactic but was evaluated on Llama-2-13B, Llama-3-70B, and Falcon-11B -- its applicability to frontier commercial models is not directly validated.

### G4. Privacy and data protection -- trigger: the prompt ingests, generates, or reasons over personal data (names, identifiers, contact info, biographical details, health data, financial data)
- 0: personal data flows through the prompt with no scoping, minimization, or handling guidance
- 1: some scoping mentioned but purpose limitation, retention, or special-category handling is absent
- 2: the prompt explicitly bounds what personal data is in scope, minimizes what must be extracted, handles ambiguity about special-category data (GDPR Article 9, HIPAA PHI categories, etc.), and the user has been told that prompt engineering alone does not make the pipeline compliant
- **Gate passes at 2.** This gate is a prompting-craft gate, not a legal compliance check. A passing score means the *prompt* is well-shaped for privacy-aware use; it does not mean the deployed system is compliant. Legal review is always separate.

## Thresholds

| Core score | Status | Action |
|---|---|---|
| 14-16 | **Strong** | Ship if all triggered conditional gates pass |
| 10-13 | **Usable** | Tighten weak dimensions before relying on it |
| 0-9 | **Weak** | Rewrite before using |

Additionally: **any triggered conditional gate that scores below its pass threshold is a blocker**, regardless of core score. A prompt scoring 16/16 but failing G2 or G4 must be revised.

## Fast QA questions
1. What exactly is being produced?
2. What facts or sources should the model trust?
3. What constraints are non-negotiable?
4. What should the model do if information is missing or weak?
5. What should the output look like?
6. Are any instructions fighting each other?
7. Can any paragraph be deleted without changing the result?
8. Does this prompt ingest untrusted content? If so, are trust boundaries explicit and is there a stronger-than-delimiter defense for high-stakes targets?
9. Will this prompt be reused? If so, has it been tested against reformulations?
10. Is the target model reasoning-first? If so, is the prompt free of CoT prefacing, persona fluff, and rigid step-by-step scaffolds?
11. Does the prompt touch personal data? If so, is scope minimized and is the user aware that this prompt does not constitute legal compliance?

## Rewrite triggers
Rewrite the prompt if any of these are true:
- the deliverable is not explicit
- the output format is implied instead of stated
- "be concise" or "be detailed" is used without numbers
- examples conflict with instructions
- the prompt contains multiple distinct goals that should be split
- the target is a reasoning-first model and the prompt prescribes intermediate reasoning steps
- untrusted content is referenced without delimiter isolation
- a conditional gate is triggered and fails

## Self-judging caveat
If you use Claude (or any LLM) to score a prompt against this rubric, the scorer is an LLM-as-judge and carries its own biases: position bias (tends to favor first option in pairwise comparisons), verbosity bias (prefers longer responses even when less accurate), and self-preference bias (favors outputs from its own model family). For high-stakes scoring, either (a) randomize position and average multiple runs, (b) use a different model family as judge than the one being scored, or (c) calibrate the judge against human ratings on a held-out set.
