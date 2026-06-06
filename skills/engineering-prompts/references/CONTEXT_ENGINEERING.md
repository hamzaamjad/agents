# Context Engineering

## Contents
- [Why context engineering is separate from prompt engineering](#why-context-engineering-is-separate-from-prompt-engineering)
- [Failure modes in long context](#failure-modes-in-long-context)
- [Context budgets and positioning](#context-budgets-and-positioning)
- [Loading strategies: upfront, just-in-time, hybrid](#loading-strategies-upfront-just-in-time-hybrid)
- [Compaction for long-horizon work](#compaction-for-long-horizon-work)
- [External memory systems](#external-memory-systems)
- [Automated prompt compression](#automated-prompt-compression)
- [Tool-definition token budget](#tool-definition-token-budget)
- [RAG vs long context: decision guide](#rag-vs-long-context-decision-guide)
- [Mitigation tactics summary](#mitigation-tactics-summary)

## Why context engineering is separate from prompt engineering
Prompt engineering manages *what to say* to the model. Context engineering manages *what tokens occupy the window* at inference time -- system instructions, tools, tool output, message history, retrieved documents, persisted memory, and everything else the model sees. Anthropic published *Effective context engineering for AI agents* in 2025 framing this as a distinct concern (anthropic.com/engineering/effective-context-engineering-for-ai-agents); the framing has become a community standard even if "discipline" is stronger language than the primary source uses.

The core insight: as context windows grow larger, the limiting constraint shifts from *finding the right words* to *managing the entire information state available to the model*. A well-written prompt buried in 100K tokens of irrelevant history will underperform a terse prompt in a well-curated 10K-token context.

## Failure modes in long context

### Lost in the middle (Liu et al. 2023)
Models preferentially attend to information at the beginning and end of long contexts; performance drops when critical information sits in the middle. Foundational finding from *Lost in the Middle: How Language Models Use Long Contexts* (arxiv 2307.03172), tested on multi-document QA and key-value retrieval across contexts up to 32K tokens.

**Status in 2025-2026**: partially mitigated in newer models (GPT-5, Gemini 2.5), but not fully. Treat "start or end" as a design preference, not a guarantee.

### Length-driven degradation independent of position
A more fundamental problem has emerged in 2025 research (*Context Length Alone Hurts LLM Performance Despite Perfect Retrieval*, Du et al., arxiv 2510.05381): performance degrades as context length grows *even when relevant information is placed exactly where the model needs it and retrieval is perfect*. Experiments across five LLMs on math, QA, and coding reported 13.9%-85% accuracy drops as input length increased within claimed supported ranges. The failure mode is not "the model can't locate the fact"; it is "the model can locate the fact but fails to reason over it effectively when surrounded by many tokens."

**Implication**: extending context window capacity provides diminishing returns past a task-dependent threshold.

### Shallow long-context adaptation: the cliff
Research on Qwen2.5-7B (arxiv 2601.15300, *Intelligence Degradation in Long-Context LLMs*) identified a critical threshold at 40-50% of the model's maximum context length where F1 scores dropped abruptly from 0.55-0.56 to 0.30 -- a 45.5% degradation over a narrow 10% range of context length. This "cliff" pattern suggests (at least in the tested model) that models may maintain performance through most of their supported range and then degrade sharply.

**Scope caveat**: this specific finding is from a single 7B open-source model. Frontier commercial models (GPT-5, Claude Opus 4.6, Gemini 2.5 Pro) were not tested in that study, and their cliff behavior -- if any -- may occur at different thresholds or not at all. Treat this as "cliff-like degradation is a known phenomenon and worth testing for on your specific target model," not as a universal rule.

### Context rot (Anthropic, 2025)
Anthropic's term for the observed phenomenon that LLMs "lose focus or experience confusion at a certain point" as context accumulates. Acknowledged in their context engineering guide and driven by needle-in-haystack style benchmarking showing accuracy decay with length.

## Context budgets and positioning

### The 60-70% working ceiling
A community heuristic -- not in Anthropic's primary guide as a hard rule -- is to work within roughly 60-70% of a model's claimed maximum context length, leaving headroom before length-driven degradation starts biting. The exact ceiling depends on the task and model: some workloads degrade earlier, some tolerate more. Use this as a starting point for experiments, not a universal constant.

### Positioning priority
- **Highest priority**: place critical instructions and success criteria at the start or end of the context.
- **High priority**: put reference documents before the query for Gemini 2.5.
- **Avoid middle**: deprioritize irrelevant material into the middle of the context, or remove it entirely.

### Recency bias in multi-turn
In multi-turn agents, anecdotal and benchmark evidence suggests models can over-weight recent inputs relative to earlier turns. For agents needing sustained coherence, **state reconstruction** at each turn (explicitly rewrite the current state into the prompt instead of appending turns) has been shown to help: state-update prompting (arxiv 2509.17766) reported ~10% Word F1 improvement and 1.5+ Info Score gains on 10-turn dialogues vs history concatenation.

## Loading strategies: upfront, just-in-time, hybrid
Anthropic's context engineering guide identifies three strategies with different tradeoffs.

- **Upfront**: preload all potentially relevant data. Best for static contexts where the same information is needed every call. Burns tokens on unused material; cannot scale to large corpora.
- **Just-in-time**: keep lightweight identifiers in context (file paths, query strings, URLs); fetch data dynamically via tools only when needed. Best for large, dynamic corpora. Used by Claude Code for database analysis. Adds latency per tool call.
- **Hybrid**: preload the most frequently needed data; fetch the rest on demand. Works well for mixed workloads like legal research or finance where some material is always relevant and the rest is task-specific.

Decision rule: if the same 10% of data is accessed 90% of the time, hybrid wins. If access is uniform across a large corpus, just-in-time is better. If the corpus is small and always relevant, upfront is simplest.

## Compaction for long-horizon work
Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitializing a new context window with the summary. Used in Claude Code to preserve continuity without hitting window limits.

**What to keep in the compaction summary**:
- Architectural and design decisions with rationale
- Open questions and unresolved bugs
- Implementation state (what's done, what's in progress, what's next)
- Relevant file paths and artifact identifiers
- Any user-provided constraints or preferences

**What to drop**:
- Redundant tool output (raw file contents that are no longer relevant)
- Search results that were used once and discarded
- Chat pleasantries and acknowledgments
- Intermediate reasoning that has been superseded

**Trigger points**: compact around the working ceiling (~70% of context window is common), or after any long tool operation that produced a large volume of ephemeral output.

**Empirical support**: **ACON** (*Optimizing Context Compression for Long-horizon LLM Agents*, arxiv 2510.00615) demonstrated systematic compression reducing peak tokens by 26-54% while maintaining task performance, and reporting up to 46% performance improvement on smaller-model agents by mitigating long-context distraction.

## External memory systems
When compaction is not enough -- e.g., for agents that span sessions or accumulate knowledge over weeks -- use an external memory system rather than trying to keep everything in-context.

**Options and reference implementations**:
- **Claude memory tool** (Anthropic Developer Platform) -- file-based store agents can read, write, and consult across sessions.
- **MemGPT / Letta** (UC Berkeley, arxiv 2310.08560) -- OS-inspired two-tier memory: **main context** (prompt tokens, analogous to RAM) and **external context** (disk-like storage, further split into archival storage for searchable facts and recall storage for conversation history). The model uses tools to page data between tiers explicitly. Letta is the productized successor.
- **LangMem** (LangGraph) -- episodic, semantic, and procedural memory integrated into LangGraph.
- **Zep** (arxiv 2501.13956) -- temporal knowledge graphs that store fact-validity windows rather than timestamped snapshots. Reported improvements over baselines on memory benchmarks; consult the paper for current numbers against specific comparison systems.

**Selection heuristic**: use a memory system when (a) the task spans sessions, (b) accumulated knowledge must be queryable, or (c) the conversation routinely exceeds the context window even with compaction.

## Automated prompt compression
When the context compressor mode is not sufficient and the input is long enough to justify a tool-based approach, automated compression can reduce token counts without manual distillation.

**LLMLingua family** (Microsoft Research) -- use a small model to identify and drop low-information tokens from the prompt before the main model sees it. Variants:
- **LLMLingua** (arxiv 2310.05736) -- coarse-to-fine compression with budget controller.
- **LongLLMLingua** -- targets long-context scenarios with question-aware compression.
- **LLMLingua-2** (arxiv 2403.12968) -- task-agnostic compression using a smaller distilled classifier.

Reported compression ratios of up to 20x on some tasks with minimal performance degradation. Useful as a drop-in preprocessing step for long documents going into a RAG or long-context prompt, especially when token cost dominates latency.

**Caveat**: LLMLingua compresses aggressively and can damage prompts where every token matters (precise instructions, delimiter-sensitive structures). Don't apply it blindly to system prompts or anything inside `<untrusted>` blocks where attacker-relevant context might be dropped.

## Tool-definition token budget
Every tool definition the model sees consumes context. In large tool-using agents this adds up fast. Guidance from Anthropic's multi-agent research system (2025):

- **Scope tool sets tightly per subagent.** Give each subagent only the tools it needs for its subtask.
- **Use dynamic tool loading** for large tool collections -- load tools on demand via a search or discovery mechanism (e.g., MCP tool search) rather than preloading them all.
- **Prefer specialized subagents** with small tool sets over a generalist agent with everything available.

## RAG vs long context: decision guide
Long context windows raise the question of when to use retrieval at all. Evidence from 2024-2026:

- **In the Agri-Query case study** (arxiv 2508.18093, single-domain: an agricultural manual in three languages), hybrid RAG (keyword + semantic) outperformed direct long-context prompting from nine long-context LLMs on needle-in-haystack-with-unanswerable variants. This is one data point on one corpus, not proof that hybrid RAG universally wins.
- **RAG inference cost is lower** in general -- only relevant chunks are sent to the LLM. Long-context inference for large prompts can be materially more expensive per call (exact numbers vary by provider and pricing; do the math for your model).
- **Long context wins** for reasoning-intensive work on static, self-contained knowledge bases -- policy chatbots, document summarization, single-paper analysis.
- **RAG wins** for dynamic, high-volume ecosystems with frequently-changing source data.
- **Hybrid approaches** (RAG for retrieval, long context for reasoning over retrieved material) are often the strongest option.

Decision rule: start with RAG if the corpus changes, is large, or cost matters. Move to long context if reasoning must span the entire document and the document fits comfortably under the working ceiling.

## Mitigation tactics summary
Fast reference for what a prompt engineer can do about long-context problems:

1. **Budget conservatively.** Start at ~60-70% of max as a working ceiling; measure on your task.
2. **Position critical content at start or end.** Never bury constraints in the middle of a long context.
3. **Compact proactively** before hitting the window limit, not after.
4. **Use state reconstruction** in multi-turn dialogues instead of concatenating history.
5. **Use RAG or hybrid** when the corpus is large or dynamic.
6. **Scope tool definitions tightly** per subagent.
7. **Test against longer-than-typical inputs** during development -- don't assume the happy path length.
8. **Measure confidence calibration**, not just accuracy -- models often become conservative under long-context stress rather than confidently wrong.
9. **Consider automated compression** (LLMLingua family) for preprocessing long documents before they enter the main prompt, when every token counts.
