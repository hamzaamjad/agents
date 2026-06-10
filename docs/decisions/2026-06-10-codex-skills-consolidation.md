# Decision memo: consolidate ~/.codex/skills into ~/.agents

- Date: 2026-06-10
- Status: Proposal — no migration performed
- Decision owner: Hamza
- Origin: finding 6 of the 2026-06-10 instruction-layer audit (`../audits/2026-06-10-instruction-layer-audit.md`)

## Problem

`~/.codex/skills/` holds a second skill library outside any git repo: no versioning, no review trail, no eval loop, and conventions that drift from the canonical library in `~/.agents/skills/`. A machine failure or accidental deletion loses these skills entirely.

Inventory (verified 2026-06-10):

| Skill | Provenance | Notes |
|---|---|---|
| analytics-sql | Hand-authored | SKILL.md + references/ — matches ~/.agents conventions |
| data-observability | Hand-authored | Same shape |
| dbt-ops | Hand-authored | Same shape |
| chronicle | Vendor/host-coupled | Depends on Codex chronicle daemon and screen-history assets |
| playwright | Vendor-imported | LICENSE.txt/NOTICE.txt, agents/ + assets/ + scripts/ |
| playwright-interactive | Vendor-imported | Same shape |
| screenshot | Vendor-imported | OS-level capture scripts |
| security-best-practices | Vendor-imported | LICENSE.txt, agents/ + references/ |
| codex-primary-runtime | Empty directory | No SKILL.md, no contents — delete candidate |

No name collisions with the seven skills already in `~/.agents/skills/`. Cursor already discovers skills from both locations; Codex CLI reads only `~/.codex/skills/`.

## Recommendation

Adopt Option A: move the three hand-authored skills (analytics-sql, data-observability, dbt-ops) into `~/.agents/skills/` and symlink them back into `~/.codex/skills/`, after a one-skill pilot proves Codex follows symlinks. Leave the four vendor-imported skills and chronicle in place, tracked by a manifest committed to this repo. Remove the empty codex-primary-runtime directory.

Rationale: the hand-authored skills are indistinguishable in shape from this repo's skills and gain versioning, review, and the eval loop. Vendor-imported skills are upstream artifacts — vendoring them into the canonical library would mix maintained content with third-party snapshots and complicate upstream refreshes; a manifest (name, version/source, license) gives recoverability without ownership confusion.

## Options considered

- **A (recommended): selective move + symlink back.** Single canonical versioned home for owned skills; both hosts keep discovery. Cost: one pilot verification; ongoing symlink awareness.
- **B: move everything, including vendor imports.** Maximal consolidation, but imports lose a clean upgrade path and their licenses/assets bloat this repo.
- **C: git-init ~/.codex/skills as its own repo.** Versioning without moving, but creates a second canonical source with separate conventions — exactly the fragmentation this audit is remediating.
- **D: status quo + backup.** Zero effort; leaves drift and single-copy risk unaddressed.

## Migration steps (for Option A, when approved)

1. Pilot: move `analytics-sql` to `~/.agents/skills/analytics-sql`, commit, then `ln -s ~/.agents/skills/analytics-sql ~/.codex/skills/analytics-sql`. Confirm Codex CLI still lists and triggers the skill.
2. If the pilot fails (Codex does not follow symlinks), stop and fall back to evaluating Option C; do not maintain two writable copies.
3. Repeat for `data-observability` and `dbt-ops`, one commit per skill.
4. Audit each migrated SKILL.md for host-specific paths (the same failure class as audit finding 3) and fix to skill-relative references.
5. Add `docs/decisions/` follow-up note or a manifest file recording the vendor-imported skills left in `~/.codex/skills/` (name, source, license file present yes/no).
6. Delete the empty `codex-primary-runtime/` directory.
7. Update the deployment map in `AGENTS.md` (drop the "separate unversioned library" caveat for migrated skills).
8. Re-run a description-triggering audit across both hosts to confirm no duplicate or lost triggers.

## Risks

- **Symlink discovery unsupported by Codex.** Mitigated by the pilot in step 1; fallback is Option C, not copy-sync (two writable copies guarantee drift).
- **Duplicate discovery in Cursor.** Cursor scans both roots; after symlinking, the same skill may appear twice. Verify Cursor de-duplicates by resolved path; if not, exclude one root in Cursor settings.
- **Hidden host coupling inside migrated skills.** dbt-ops/analytics-sql may reference machine-specific paths; step 4 exists for this.
- **Vendor refresh confusion.** Manifest (step 5) is the guard: it records which directories are upstream snapshots and where they came from.
- **Loss of file timestamps.** Acceptable; none of these files carry git history today.

## Effort

Roughly 1–2 hours including the pilot and trigger re-verification.
