# Benchmark Summary: defining-specifications iteration 3

## Result

- `with_skill`: 30/30 assertions passed, mean pass rate 100%.
- `without_skill`: 23/30 assertions passed, mean pass rate 76.7%.
- Delta: +23.3 percentage points for the revised skill (v1.2).
- Timing/token metrics were unavailable from subagent completion notifications, so this benchmark compares output quality only.

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 77% ± 21% | +0.23 |

## What changed this iteration

Iteration 3 tests v1.2 of the skill, which added EARS-by-default functional requirements, Given/When/Then acceptance criteria with `REQ -> AC -> TEST` traceability, a `For Implementing Agents` handoff block, specificity calibration, anti-hallucination grounding rules, a self-review status gate, and two `references/` files (EARS/GWT detail and spec-type profiles). Three discriminating assertions were added to the eval set to test these capabilities directly.

## Per-eval findings

- **eval-0 ticket-validation**: with_skill 10/10, without_skill 6/10 (+0.4). The baseline avoided the ticket-workflow skill and invented a status vocabulary that contradicts the real lifecycle, and used no EARS/GWT/handoff structure.
- **eval-1 spec-skill-improvement**: with_skill 10/10, without_skill 10/10 (+0.0). Confounded — the baseline reads `SKILL.md` v1.2 as its subject material and naturally mirrors EARS, GWT traceability, and the handoff block. This eval does not discriminate the skill's value.
- **eval-2 agent-memory**: with_skill 10/10, without_skill 7/10 (+0.3). The baseline was well-grounded and well-scoped but used no EARS, no GWT traceability, and no handoff block, and prematurely marked the spec `Ready for Review` despite open questions.

## Conclusions

- The new conventions (EARS, GWT traceability, handoff block) are reliably produced when the skill is loaded and are reliably absent from a strong baseline on clean tasks — they are exactly what the skill now buys.
- On the two clean evals (0 and 2), the skill delta is +0.4 and +0.3; the headline +0.23 average is dragged down by the confounded eval-1.
- The new grounding/calibration guidance did not regress any previously passing behavior; with_skill remained at 100%.

## Suggested next steps

- Replace eval-1's subject with an artifact that does not already embody the conventions, or drop it as a value discriminator (keep it only as a regression check).
- Consider a future v1.3 addressing gaps the with-skill runs themselves surfaced: the orphan `DEC-###` ID convention (no template section), an undefined `Status` lifecycle (`Approved`/`Blocked` never defined), undefined Simple/Medium/Large size tiers, and the absence of one inline worked example.
