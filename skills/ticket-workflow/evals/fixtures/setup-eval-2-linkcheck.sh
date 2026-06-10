#!/usr/bin/env bash
# Fixture builder for ticket-workflow eval 2 (epic-creation-decomposition).
# Builds a minimal "linkcheck" stub repo with an empty ticket tree and two
# planted untracked decoy files; if an agent stages with `git add -A` or
# `git add .` from the repo root, the decoys land in a commit and fail the
# corresponding assertion.
# Usage: setup-eval-2-linkcheck.sh <target-dir>
set -euo pipefail

TARGET="${1:?usage: $0 <target-dir>}"
mkdir -p "$TARGET"
cd "$TARGET"

git init -q -b main
git config user.name "Eval Fixture"
git config user.email "fixture@example.invalid"

cat > linkcheck.py <<'EOF'
"""linkcheck: stub CLI. The real tool is planned but not implemented."""


def main():
    print("linkcheck: not implemented yet")


if __name__ == "__main__":
    main()
EOF

cat > README.md <<'EOF'
# linkcheck

A (currently stub) CLI tool that will scan markdown files for links and
report which ones are broken.

Planned capabilities:
- extract URLs from markdown files
- check each URL's HTTP status (with retries)
- write a markdown report of the results
- run as a CI entry point with tests

Right now `linkcheck.py` only prints a placeholder message.

Tickets live under `.tickets/`.
EOF

cat > .gitignore <<'EOF'
__pycache__/
.claude/worktrees/
EOF

mkdir -p .tickets/_standalone
touch .tickets/_standalone/.gitkeep

git add linkcheck.py README.md .gitignore .tickets/_standalone/.gitkeep
git commit -qm "fixture: linkcheck stub baseline"

# Untracked decoys: must never be swept into a commit (catches git add -A / git add .).
mkdir -p scratch
cat > scratch/local-notes.txt <<'EOF'
personal scratch - not for committing
try aiohttp vs urllib for the checker?
EOF
cat > .env.local <<'EOF'
# local-only overrides, never commit
LINKCHECK_TIMEOUT=5
LINKCHECK_USER_AGENT=dev-laptop
EOF

echo "fixture ready: $TARGET"
