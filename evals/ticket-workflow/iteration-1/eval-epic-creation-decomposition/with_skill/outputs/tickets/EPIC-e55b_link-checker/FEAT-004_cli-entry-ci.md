---
id: FEAT-004
title: "CLI entry point, tests wiring, CI workflow"
type: feature
status: to-do
priority: high
created: 2026-06-10
updated: 2026-06-10
parent: EPIC-e55b
dependencies: [FEAT-001, FEAT-002, FEAT-003]
tags: [linkcheck, cli, ci]
agent_created: true
complexity: 4
---

# CLI entry point, tests wiring, CI workflow

## Context

Final feature ticket for the linkcheck tool (parent: EPIC-e55b). Wires extract, check,
and report into a runnable CLI, replaces the root stub `linkcheck.py` with a proper
package entry point, and adds the CI workflow. All three prior FEAT tickets must be
`done` and merged to the epic branch first.

## Requirements

- [ ] Create `linkcheck/cli.py` with `main(argv: list[str] | None = None) -> int`
      (argparse): positional `paths` (files or directories; directories scanned
      recursively for `*.md`), options `--report PATH`, `--retries N` (default 2),
      `--timeout SECONDS` (default 5.0). Flow: discover files -> read text ->
      `extract_urls` -> `check_urls` -> print one summary line per the epic contract
      -> optionally `write_report`.
- [ ] Exit codes: 0 = all links ok (or no links found), 1 = at least one broken link,
      2 = usage/input error (e.g. a path that does not exist). Keep the check
      function injectable (parameter defaulting to `check_urls`) so CLI tests run offline.
- [ ] Create `linkcheck/__main__.py` delegating to `cli.main()` so
      `python3 -m linkcheck <paths>` works; delete the root stub `linkcheck.py`.
- [ ] Create `.github/workflows/linkcheck.yml`: on push + pull_request, single Linux
      job — checkout, set up Python 3.13, `pip install pytest`, run
      `python3 -m pytest tests/ -q`, then offline smoke `python3 -m linkcheck README.md`.
- [ ] Create `tests/test_cli.py` covering exit codes 0/1/2 and `--report` file output
      using an injected fake checker (no network); update README usage section.

## File path hints

- `linkcheck/cli.py` — create
- `linkcheck/__main__.py` — create
- `linkcheck.py` — delete (root stub replaced by `python3 -m linkcheck`)
- `.github/workflows/linkcheck.yml` — create
- `tests/test_cli.py` — create
- `README.md` — modify (usage: `python3 -m linkcheck`, exit codes; drop stub wording)

## Constraints

- Do NOT add packaging metadata (pyproject/setup.py), console-script installs, or new
  runtime dependencies — invocation is `python3 -m linkcheck` only.
- Do NOT add CI matrix builds, artifact uploads, caching, or scheduled triggers.
- Do NOT let tests or the CI smoke step hit the network (README has no external URLs;
  keep it that way in the usage section).
- Do NOT touch `scratch/` or `.env.local`.

## Acceptance criteria

- [ ] `python3 -m linkcheck README.md` exits 0 from the repo root (offline smoke).
- [ ] `python3 -m linkcheck missing-file.md` prints an error and exits 2.
- [ ] CLI test with an injected fake checker proves exit 1 on a broken link and that
      `--report` writes the rendered report to the given path.
- [ ] Root `linkcheck.py` no longer exists; `.github/workflows/linkcheck.yml` exists
      and runs pytest + the offline smoke command.
- [ ] `python3 -m pytest tests/ -q` passes (full suite, all four test modules).

## Verification

```bash
python3 -m pytest tests/ -q
python3 -m linkcheck README.md; echo "exit=$?"          # expect exit=0
python3 -m linkcheck no-such-file.md; echo "exit=$?"    # expect exit=2
test ! -f linkcheck.py && test -f .github/workflows/linkcheck.yml && echo "layout ok"
```

## Notes

Exit-code contract and data contract are pinned in `_epic.md`. The smoke step stays
offline only while README contains no external links — CI failure there is the tool
working as designed.
