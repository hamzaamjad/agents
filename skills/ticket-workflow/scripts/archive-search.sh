#!/usr/bin/env bash
# archive-search.sh — Lane A retrieval over .tickets/_archive/
#
# Lexical search (ripgrep) across archived tickets' YAML frontmatter and
# `## Outcome` blocks. Prints matching paths plus the Outcome snippet
# only — never the full ticket body.
#
# Lane B (`--semantic`) is not yet available; see
# `.claude/skills/ticket-workflow/references/outcome-schema.md` for the
# ship trigger (archive size ≥ ~2,000 Outcome chunks, or two logged
# Lane A runs that return ≥ 5 irrelevant matches).

set -euo pipefail

ARCHIVE_DIR=".tickets/_archive"

usage() {
  cat <<'USAGE'
Usage: archive-search.sh [flags] <query>

Lexical search over archived tickets' `## Outcome` blocks and YAML
frontmatter. Prints matching file paths and their Outcome snippets.

Arguments:
  <query>                 Substring to match (ripgrep -F semantics against
                          frontmatter + Outcome block). Required unless
                          only frontmatter filter flags are given, in
                          which case every archived ticket is a candidate.

Flags:
  --type <value>          Post-filter on frontmatter `type:` line
                          (e.g. feature, bug, refactor, chore, epic).
  --complexity <n>        Post-filter on frontmatter `complexity:` line;
                          matches exact integer.
  --tags <csv>            Post-filter on frontmatter `tags:` list; any of
                          the comma-separated tokens must appear.
  --semantic              Lane B; not yet available. Reserved for
                          future semantic search. See
                          references/outcome-schema.md for the ship
                          trigger. Invoking this flag exits non-zero
                          with a pointer to the schema doc.
  --help, -h              Show this help and exit 0.

Behavior:
  - Empty or missing `.tickets/_archive/`: prints `no matches` and
    exits 0 (safe on fresh workspaces).
  - Zero matches: prints `no matches` and exits 0.
  - Output per match: the file path, a blank line, then the ticket's
    `## Outcome` block (delimited by the next `^## ` heading or EOF).
    The full ticket body is never printed.

Examples:
  archive-search.sh cache
  archive-search.sh --type feature --tags retrieval,archive 'outcome schema'
  archive-search.sh --complexity 6 worktree
USAGE
}

query=""
filter_type=""
filter_complexity=""
filter_tags=""

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --semantic)
      echo "error: --semantic (Lane B) is not yet available." >&2
      echo "See .claude/skills/ticket-workflow/references/outcome-schema.md for the ship trigger." >&2
      exit 2
      ;;
    --type)
      filter_type="${2:-}"
      shift 2
      ;;
    --complexity)
      filter_complexity="${2:-}"
      shift 2
      ;;
    --tags)
      filter_tags="${2:-}"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "error: unknown flag: $1" >&2
      echo "run with --help for usage." >&2
      exit 2
      ;;
    *)
      if [ -z "$query" ]; then
        query="$1"
      else
        query="$query $1"
      fi
      shift
      ;;
  esac
done

if [ ! -d "$ARCHIVE_DIR" ]; then
  echo "no matches"
  exit 0
fi

shopt -s nullglob globstar

# Collect candidate archived ticket files.
candidates=()
while IFS= read -r -d '' f; do
  candidates+=("$f")
done < <(find "$ARCHIVE_DIR" -type f -name '*.md' -print0)

if [ "${#candidates[@]}" -eq 0 ]; then
  echo "no matches"
  exit 0
fi

extract_frontmatter() {
  awk '
    BEGIN { inside=0; started=0 }
    /^---[[:space:]]*$/ {
      if (!started) { started=1; inside=1; next }
      if (inside)   { inside=0; exit }
    }
    inside { print }
  ' "$1"
}

extract_outcome() {
  awk '
    /^## Outcome[[:space:]]*$/ { flag=1; print; next }
    /^## / && flag { exit }
    flag { print }
  ' "$1"
}

frontmatter_matches_filters() {
  local fm="$1"

  if [ -n "$filter_type" ]; then
    echo "$fm" | grep -qE "^type:[[:space:]]*${filter_type}[[:space:]]*$" || return 1
  fi

  if [ -n "$filter_complexity" ]; then
    echo "$fm" | grep -qE "^complexity:[[:space:]]*${filter_complexity}[[:space:]]*$" || return 1
  fi

  if [ -n "$filter_tags" ]; then
    local tags_line
    tags_line=$(echo "$fm" | awk '/^tags:/{print; exit}')
    [ -n "$tags_line" ] || return 1
    local any=0
    local IFS=','
    for t in $filter_tags; do
      t="${t## }"; t="${t%% }"
      [ -n "$t" ] || continue
      if echo "$tags_line" | grep -qE "(\[|,| )${t}(\]|,| |$)"; then
        any=1
        break
      fi
    done
    [ "$any" = "1" ] || return 1
  fi

  return 0
}

matches=()
for f in "${candidates[@]}"; do
  fm=$(extract_frontmatter "$f")
  outcome=$(extract_outcome "$f")

  if ! frontmatter_matches_filters "$fm"; then
    continue
  fi

  if [ -n "$query" ]; then
    haystack="${fm}"$'\n'"${outcome}"
    if ! printf '%s' "$haystack" | grep -qF -- "$query"; then
      continue
    fi
  fi

  matches+=("$f")
done

if [ "${#matches[@]}" -eq 0 ]; then
  echo "no matches"
  exit 0
fi

for f in "${matches[@]}"; do
  echo "$f"
  echo
  outcome=$(extract_outcome "$f")
  if [ -n "$outcome" ]; then
    echo "$outcome"
  else
    echo "(no ## Outcome block)"
  fi
  echo
  echo "---"
done
