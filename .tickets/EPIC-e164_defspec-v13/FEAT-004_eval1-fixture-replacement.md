---
id: FEAT-004
title: "Replace confounded eval-1 with convention-free fixture"
type: feature
status: done
priority: medium
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e164
dependencies: []
tags: [skills, defining-specifications, evals]
agent_created: false
complexity: 3            # rubric: files 4(.20) deps 1(.15) testing 3(.15) risk 3(.15) new/mod 4(.10) crosscut 1(.10) api 1(.05) db 1(.10) = 2.50 → 3
---

# Replace confounded eval-1 with convention-free fixture

## Context

Implements REQ-009, REQ-010, NFR-004 of `docs/specs/SPEC-defining-specifications-v1-3-2026-06-10.md` (DEC-001). Eval id 1 (`spec-skill-improvement`) in `skills/defining-specifications/evals/evals.json` takes `SKILL.md` itself as its subject, so a baseline agent mirrors EARS/GWT/handoff conventions straight from the input — iteration-3 measured 10/10 in both arms; the eval discriminates nothing. Replace the subject with a bundled fixture that does not embody the conventions under test.

Touches only `evals/`; parallel-safe with FEAT-001..003 (no shared files).

## Requirements

- [x] REQ-009: Rewrite eval id 1 so its subject is a new fixture under `skills/defining-specifications/evals/fixtures/`, its prompt asks the agent to review and formalize that draft into a focused specification, the `id` value 1 is retained, and the `name` is updated to match the new subject.
- [x] REQ-010: The fixture is a realistic rough draft (feature idea or informal notes) containing no EARS `shall` requirements, no Given/When/Then phrasing, no `For Implementing Agents` heading, and no `REQ-`/`AC-`/`DEC-` style IDs.
- [x] NFR-004: The fixture path in eval-1's `files` and prompt is repo-relative (matching the path style used inside eval prompts), not an absolute home path. Note spec ASM-001: harness resolution of relative paths is unconfirmed; the failure mode is loud and the revert is one line.
- [x] Keep eval-1's existing convention assertions (EARS, GWT traceability, handoff block) so the eval now discriminates: the subject no longer supplies them.

## File path hints

- `skills/defining-specifications/evals/evals.json` — modify (eval id 1 only: name, prompt, expected_output, files; keep assertions list intact unless an assertion references the old subject)
- `skills/defining-specifications/evals/fixtures/<kebab-name>.md` — create

## Constraints

- Do NOT modify evals 0 and 2 in any way (byte-identical).
- Do NOT embed spec conventions in the fixture (REQ-010 list) — this is the entire point.
- Fixture subject must not be the defining-specifications skill or spec tooling (avoid re-confounding); rough notes for a small unrelated workspace capability are ideal (spec Technical Context).
- Valid JSON after edit; preserve existing top-level structure and key order conventions.

## Acceptance criteria

- [x] AC-006: eval id 1's `files` is a repo-relative path to a fixture under `evals/fixtures/`, its prompt asks for review/formalization of that fixture, and the file exists at that path.
- [x] AC-007: the purity grep over the fixture returns no matches.
- [x] Evals 0 and 2 are unchanged (diff scoped to eval 1 + new fixture).
- [x] `evals.json` parses as valid JSON.

## Verification

```bash
# AC-006: eval 1 wiring
python3 - <<'EOF'
import json, os
d = json.load(open('skills/defining-specifications/evals/evals.json'))
e = [x for x in d['evals'] if x['id'] == 1][0]
assert e['files'], 'files empty'
p = e['files'][0]
assert not p.startswith('/'), f'path not repo-relative: {p}'
assert 'evals/fixtures/' in p, f'not under evals/fixtures/: {p}'
assert os.path.exists(p), f'fixture missing at {p}'
assert 'fixture' in ' '.join(e['files']) or True
print('AC-006 ok:', p)
EOF
# AC-007: fixture purity (run against the actual fixture path)
FIX=$(python3 -c "import json; print(json.load(open('skills/defining-specifications/evals/evals.json'))['evals'][1]['files'][0])")
rg -n -i 'shall|For Implementing Agents|REQ-[0-9]|AC-[0-9]|DEC-[0-9]' "$FIX" && echo 'PURITY FAIL' || echo 'purity ok'
rg -n 'Given' "$FIX" | rg 'When' | rg 'Then' && echo 'GWT FAIL' || echo 'gwt ok'
# Evals 0 and 2 untouched
git diff epic/e164/defspec-v13 -- skills/defining-specifications/evals/evals.json | rg '^[+-]' | rg -v 'fixture|spec-skill|"id": 1|formaliz|rough|draft' | head -20
python3 -c "import json; json.load(open('skills/defining-specifications/evals/evals.json')); print('json ok')"
```

## Notes

Spec sections: DEC-001 (replace, not demote), REQ-009/REQ-010, NFR-004, ASM-001, RISK-002, AC-006/AC-007. The diff-scope check above is a heuristic; the executing agent confirms evals 0/2 are untouched by reading the diff.

## Verification log (2026-06-10)

- AC-006 python check → `AC-006 ok: skills/defining-specifications/evals/fixtures/snippets-library-notes.md` (repo-relative, under fixtures/, exists, prompt asks formalization)
- AC-007 purity grep → `purity ok`; GWT line check → `gwt ok` (fixture contains no shall/handoff-heading/ID tokens, no Given+When+Then line)
- Diff read-confirmed: all changed lines inside eval id 1 (name, prompt, expected_output, assertion 6, files); evals 0 and 2 byte-identical
- `json ok` (parses; structure preserved)
- Actual tool rounds: 5 batched rounds (7 repo-acting tool calls) vs complexity 3 — in line

## Outcome

**Summary:** Replaced eval-1's confounded subject (the skill's own `SKILL.md`) with a bundled convention-free fixture — informal brain-dump notes for a prompt-snippets library — and rewired the eval (renamed `rough-notes-formalization`) to ask for review-and-formalization of that draft. The ten assertions, including the EARS/GWT/handoff discriminators, are retained (one regrounded from the old subject to the fixture), so the conventions under test can no longer leak from the input. `id: 1` retained; evals 0 and 2 untouched.

**Key decisions:**
- Replace rather than demote to regression-only (spec DEC-001) — keeps three value-discriminating evals.
- Fixture path written repo-relative (spec NFR-004), accepting ASM-001 harness risk: loud failure, one-line revert.
- Fixture subject is a human copy-paste snippets library — adjacent to the workspace domain yet convention-free by construction.

**Constraints & invariants discovered (keep):**
- Fixture must never contain `shall` (case-insensitive, even mid-word), template-heading names, ID-pattern tokens, or a Given+When+Then line — the purity grep is the gate.
- Evals 0 and 2 stay byte-identical through any eval-1 edit.

**Implementation notes (high signal only):**
- Touch points: `evals/evals.json` (eval id 1 only), new `evals/fixtures/snippets-library-notes.md`
- Pattern: subject/convention decoupling — eval input must not embody graded outputs

**Verification:**
- AC-006 script → ok with fixture path; purity grep → no matches; `json.load` → ok
- `git diff epic/e164/defspec-v13 -- evals.json` → changes confined to eval 1

**Risk / regression surface:**
- ASM-001: harness may not resolve repo-relative `files`; detect on next benchmark run, revert path to absolute if so.

**Retrieval tags:** evals.json, eval-1, rough-notes-formalization, fixture, snippets-library-notes, confound, purity grep, repo-relative path, NFR-004, v1.3
