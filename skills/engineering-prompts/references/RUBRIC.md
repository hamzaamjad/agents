# Prompt Review Rubric

Score each dimension from 0 to 2.

## 1. Goal clarity
- 0: vague or implied
- 1: somewhat clear but incomplete
- 2: explicit objective and deliverable

## 2. Context quality
- 0: missing key background or overloaded with irrelevant detail
- 1: mixed relevance
- 2: lean, decision-relevant context only

## 3. Constraints
- 0: missing or hidden
- 1: partial
- 2: explicit and prioritized

## 4. Output contract
- 0: unspecified
- 1: partially specified
- 2: exact artifact, sections, length, and format are clear

## 5. Completion criteria
- 0: no definition of done
- 1: soft success criteria only
- 2: explicit checks and handling for uncertainty or blockers

## 6. Consistency
- 0: contradictory or ambiguous
- 1: mostly consistent with some mixed signals
- 2: coherent and unambiguous

## 7. Reusability
- 0: too tied to one chat and not reusable
- 1: partly reusable
- 2: uses clean placeholders or filled context appropriately

## Thresholds
- **12-14**: strong
- **9-11**: usable but should be tightened
- **0-8**: rewrite before relying on it

## Fast QA questions
1. What exactly is being produced?
2. What facts or sources should the model trust?
3. What constraints are non-negotiable?
4. What should the model do if information is missing or weak?
5. What should the output look like?
6. Are any instructions fighting each other?
7. Can any paragraph be deleted without changing the result?

## Rewrite triggers
Rewrite the prompt if any of these are true:
- the deliverable is not explicit
- the output format is implied instead of stated
- “be concise” or “be detailed” is used without limits
- examples conflict with instructions
- the prompt contains multiple goals that should be split
