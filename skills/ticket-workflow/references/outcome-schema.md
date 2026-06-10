# `## Outcome` schema

Every ticket marked `done` must carry an
`## Outcome` section. The Outcome is the archived ticket's retrieval
surface: a single dense block that a future agent can grep or embed
without having to re-read the full ticket body.

Target length: **120–200 words**, plus **up to 8 short bullets** total.
"Small enough that agents don't skip it; dense enough that retrieval
loves it."

## Template

The seven bolded subsections below must appear in this exact order in
every archived ticket's `## Outcome` block:

**Summary:** <2–3 sentences: what shipped/fixed + user-visible effect + scope>

**Key decisions:**
- <decision> — <why this option; 1 clause>
- <decision> — <tradeoff / alternative rejected>

**Constraints & invariants discovered (keep):**
- <invariant/constraint phrased as a rule>
- <invariant/constraint phrased as a rule>

**Implementation notes (high signal only):**
- Touch points: <paths/modules/apis>
- Pattern: <name the pattern/mechanism used>

**Verification:**
- <command> → <expected signal>
- <command> → <expected signal>

**Risk / regression surface:** <1–2 bullets max>
- <what might break; what guards it>

**Retrieval tags:** <5–10 keywords and identifiers; include "weird strings" like error codes>

## Filled example

Plausible ticket: `type: feature`, adding a lightweight cache with
correctness constraints. Shown indented as a displayed code block so the
rendered schema above remains the single matchable source for
verification tooling.

    ## Outcome

    > Summary: Added request-scoped + short-TTL caching for `GET /reports/summary` to cut p95 latency under load. Cache is bypassed for privileged/admin views and never caches error responses.

    > Key decisions:
    > - Use explicit cache key versioning (`reports_summary:v2`) — avoids silent mismatch when response shape changes.
    > - Cache only successful (200) responses — prevents "sticky" failure modes during partial outages.

    > Constraints & invariants discovered (keep):
    > - Never cache responses that depend on user role/permissions unless the role is part of the key.
    > - Cache TTL must remain ≤60s until we have invalidation hooks from the write-path.

    > Implementation notes (high signal only):
    > - Touch points: `src/reports/summary.ts`, `src/cache/client.ts`, middleware ordering in `src/http/router.ts`
    > - Pattern: "read-through cache with safe bypass"

    > Verification:
    > - `pnpm test reports -- --filter summary` → all green
    > - `curl -H 'X-Role: admin' .../reports/summary` twice → second request must NOT be `X-Cache: HIT`
    > - `curl .../reports/summary` twice → second request returns `X-Cache: HIT`

    > Risk / regression surface:
    > - Middleware order matters: auth must run before cache key construction.

    > Retrieval tags: reports, summary, cache, TTL=60, read-through, X-Cache, admin bypass, key version v2

When drafting a real Outcome, restore the `**bold**` markers shown in
the template above — the indented/quoted rendering in this example
exists only so the verification grep (`^\*\*…:\*\*`) counts the
template's seven subsections once rather than twice.

## Scale horizon for Lane B

When `.tickets/_archive/` exceeds ~2,000 `## Outcome` chunks (≈ 200
tickets at ~10 bullets each), Lane A (plain grep over Outcome blocks)
precision will degrade; that volume is the trigger for shipping Lane B
(semantic retrieval over the same blocks). Until then, Lane A alone is
sufficient.

Lane B's eventual `--semantic` flag on `scripts/archive-search.sh` will
build an in-session embedding index (default model
`sentence-transformers/all-MiniLM-L6-v2`, overridable via
`ARCHIVE_SEARCH_MODEL`) and write nothing to disk — the
no-persistent-infrastructure constraint is binding across both lanes.
