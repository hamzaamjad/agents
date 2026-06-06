# Vendor Guide Index

This directory contains vendor-authored prompting guides used as reference material. The guides are large (~2,150 lines total) and should only be loaded when a specific question cannot be answered from SKILL.md, PLAYBOOK.md, or the other references.

## When to consult these files
1. The target model family is known (Claude, GPT, Gemini, or Llama).
2. The question is about a structural preference or model-specific gotcha that is not covered in the main reference files.
3. You need to verify a specific claim against primary vendor guidance.

For most prompt-drafting work, the main reference files are sufficient.

## Files

### `anthropic-prompting-best-practices.md` (742 lines)
Anthropic's official guide for Claude 4.6, Opus 4.6, Sonnet 4.6, and Haiku 4.5.

**Consult when**:
- Drafting for Claude with extended thinking
- XML tag conventions questions
- Tool use and agentic patterns on Claude
- Adaptive thinking parameters
- Claude-specific gotchas (prefill removal, aggressive trigger overtriggering, "think" word sensitivity)
- Prompt caching and long-context strategies

**Grep hints**:
- `grep "extended thinking"` -- thinking configuration and adaptive thinking
- `grep "tool"` -- tool use patterns and parallel calling
- `grep "XML"` -- XML tag conventions
- `grep "prefill"` -- assistant message prefilling (note: removed in 4.6)
- `grep "system prompt"` -- system prompt best practices
- `grep "multishot"` or `grep "example"` -- few-shot example guidance

### `openai-prompt-engineering-guide.md` (605 lines)
OpenAI's guide covering GPT-4, GPT-5, and o-series reasoning models.

**Consult when**:
- Drafting for GPT-5 or o-series reasoning models
- Questions about `developer` vs `user` vs `assistant` message hierarchy
- `reasoning_effort` parameter tuning
- Structured Outputs with JSON Schema
- Tool preambles and agentic workflows
- GPT-specific delimiters (`###`, `"""`)

**Grep hints**:
- `grep -i "reasoning"` -- reasoning model guidance
- `grep "developer"` -- developer message hierarchy
- `grep "Structured Output"` -- JSON Schema and strict validation
- `grep "agent"` -- agentic workflow patterns
- `grep "eagerness"` -- controlling agentic behavior

### `google-gemini-prompting-strategies.md` (546 lines)
Google's guide for Gemini 2.5 including thinking models.

**Consult when**:
- Drafting for Gemini 2.5 (thinking or standard)
- Thinking budget configuration (low / medium / high)
- Thought signatures for multi-turn tool use
- Gemini's specific ordering preference (documents before query, constraints at end)
- Function declarations with schemas

**Grep hints**:
- `grep "thinking"` -- thinking models and budgets
- `grep "constraints"` -- where to place constraints in the prompt
- `grep "function"` -- function calling and schemas
- `grep "multi-turn"` -- multi-turn and stateless API notes

### `meta-llama-prompting-guide.md` (260 lines)
Meta's guide for Llama models.

**Consult when**:
- Drafting for Llama (open-source deployments)
- Structured JSON output on Llama specifically
- Role + rules + restrictions + example pattern

**Grep hints**:
- `grep "JSON"` -- structured output patterns
- `grep "role"` -- role and restriction patterns

## Cross-model topics
When a topic spans vendors, check these in this order:
- **Tool use**: Anthropic (primary) → OpenAI (alternatives) → Google
- **Long context**: Anthropic (context engineering is their term) → Google (for Gemini specifics) → OpenAI
- **Structured output**: OpenAI (Structured Outputs is their implementation) → Anthropic → Google → Meta
- **Reasoning models**: OpenAI (o-series native) → Anthropic (extended thinking) → Google (Gemini 2.5 thinking)
- **XML tags**: Anthropic is authoritative
- **Markdown / `###` delimiters**: OpenAI is authoritative

## Warning
These files reflect the state of vendor guidance at the time of capture. For the most current model-specific parameters, thinking budgets, API versions, and deprecations, also check the vendor's live documentation. The main reference files in this skill (SKILL.md, PLAYBOOK.md, CONTEXT_ENGINEERING.md) capture 2025-2026 findings and should be preferred when they conflict with older snapshots here.
