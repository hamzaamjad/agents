# Complexity Scoring Rubric

This is the rubric consumed by Step 3 of `SKILL.md` ("Assess complexity").
Populate the `complexity` frontmatter field (integer 1–10) by scoring each
of the eight factors below on a 1–10 sub-scale, then taking the weighted
average. The weights are fixed and sum to 100%. Do **not** retune the
weights per-ticket — keep the math simple so the rubric stays usable
during Step 3 without running a script.

Sub-score bands apply uniformly to every factor:

- **1–3** — trivial / isolated / well-understood.
- **4–6** — moderate / localized-but-nontrivial.
- **7–8** — hard / cross-cutting / high-coordination.
- **9–10** — systemic / high-risk / unknown-unknowns dominate.

## Files affected (20%)

- **1–3:** one file, or one file plus a trivial config / docs edit.
- **4–6:** 2–3 real files in one module.
- **7–8:** 4–5 real files, or 2–3 files spanning modules.
- **9–10:** 6+ real files, or any pervasive cross-module change.

"Real files" excludes docs-only, generated, or lockfile-style changes
(e.g. `CHANGELOG.md`, `package-lock.json`). A one-line comment touch is
not a "real file" in the sense meant here.

## Dependency count (15%)

- **1–3:** no in-repo `dependencies:` on other tickets; no new external
  packages.
- **4–6:** one or two in-repo dependencies; or one new third-party
  dependency with a well-documented API.
- **7–8:** three or more in-repo dependencies, or a new dependency with
  thin documentation.
- **9–10:** fan-in across many modules, or a new dependency that requires
  non-trivial auth / configuration surface.

## Testing complexity (15%)

- **1–3:** unit test in one file covers the change.
- **4–6:** multiple unit tests, or one integration test with an existing
  harness.
- **7–8:** new integration test harness, flaky-test surface, or
  significant mock/stub scaffolding.
- **9–10:** end-to-end / cross-service testing; test environment itself
  must be built or significantly extended.

## Risk level (15%)

- **1–3:** cosmetic, documentation, dev-tooling; no production blast
  radius.
- **4–6:** internal refactor with clear invariants; rollback is trivial.
- **7–8:** touches behavior on a hot path, or a rarely-exercised code
  path whose regressions would be silent.
- **9–10:** auth, authorization, billing, data-integrity, irreversible
  migrations, security surfaces.

## New vs modify (10%)

- **1–3:** modifying existing code in place, matching the local style.
- **4–6:** adding a small new module alongside existing ones.
- **7–8:** introducing a new subsystem, new public API, or new
  architectural seam.
- **9–10:** green-field service or a framework change that other code
  must then be adapted to.

## Cross-cutting concerns (10%)

- **1–3:** change stays inside one concern / one layer.
- **4–6:** touches two layers (e.g. service + test) with a clean
  interface.
- **7–8:** spans three or more layers, or couples two previously
  independent subsystems.
- **9–10:** invasive cross-cutting change (logging, auth, I/O shape)
  that forces edits in many unrelated call sites.

## External API integration (5%)

- **1–3:** no external API; or a single call to a well-known, stable API
  with no auth change.
- **4–6:** new call to an existing third-party with known contract.
- **7–8:** webhook / OAuth / multi-step integration with a new vendor.
- **9–10:** integration that requires vendor-side configuration changes
  or custom retry / idempotency handling.

## Database changes (10%)

- **1–3:** no DB change; or a backward-compatible read-only query
  addition.
- **4–6:** additive schema change (new nullable column, new index) with
  no data migration.
- **7–8:** schema change that requires a write-path migration, or a
  change to an index on a large table.
- **9–10:** irreversible migration, cross-table invariants, or any
  change that cannot be rolled back by reverting the code alone.

## Worked example

Ticket: "Add request-scoped cache to the report endpoint."

| Factor                     | Weight | Sub-score | Weighted |
|----------------------------|-------:|-----------|---------:|
| Files affected             | 0.20   | 4         | 0.80     |
| Dependency count           | 0.15   | 3         | 0.45     |
| Testing complexity         | 0.15   | 5         | 0.75     |
| Risk level                 | 0.15   | 6         | 0.90     |
| New vs modify              | 0.10   | 5         | 0.50     |
| Cross-cutting concerns     | 0.10   | 4         | 0.40     |
| External API integration   | 0.05   | 1         | 0.05     |
| Database changes           | 0.10   | 1         | 0.10     |
| **Total**                  |        |           | **3.95** |

Rounded up, `complexity: 4`. Under Tier B defaults (`SKILL.md` Step 3),
this sits below the decomposition threshold (≥ 8 or ≥ 5 real files).
Under Tier A, it also sits below the threshold (≥ 6 or ≥ 3 real files),
but the 4 files sub-score means the "≥ 3 real files" trigger fires for
Tier A — so a Haiku-class agent would decompose; a frontier agent would
not.

---

This rubric is consumed by `SKILL.md` → "Execution Protocol" → Step 3
("Assess complexity"). The calibration loop lives in Step 6 ("Verify"),
which records the realized tool-round count next to the predicted
complexity so future tuning is empirical rather than speculative.
