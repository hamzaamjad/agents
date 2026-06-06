# Benchmark Summary: defining-specifications iteration 1

## Result

- `with_skill`: 20/21 assertions passed, mean pass rate 95.24%.
- `without_skill`: 21/21 assertions passed, mean pass rate 100%.
- Timing/token metrics were unavailable from the subagent completion notifications, so this benchmark compares output quality only.

## Main Finding

The current skill does not yet outperform a capable baseline agent. It gives useful direction, but it lacks enough concrete structure to reliably change behavior.

## Patterns To Preserve

- Focused specs with explicit non-goals and write boundaries.
- Read-only workspace inspection before drafting.
- Clarifying questions or recorded assumptions when interaction is unavailable.
- Concrete acceptance criteria and verification plans.
- Output files written only to the assigned spec location.

## Gaps To Fix

- Require stable IDs for goals, non-goals, requirements, acceptance criteria, assumptions, questions, and risks.
- Add a default spec template with stable headings.
- Define the clarify -> outline -> confirm -> write flow.
- Clarify that tickets/tasks are downstream artifacts and out of scope for this skill.
- Strengthen the skill description so it triggers for spec-driven planning, agent handoffs, PRDs, RFCs, design docs, and rough ideas that need formalization.
