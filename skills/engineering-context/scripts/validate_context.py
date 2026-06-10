#!/usr/bin/env python3
"""
Deterministic validation checks for workspace instruction files.

Usage:
    python validate_context.py <project-root>
    python validate_context.py <project-root> --format json

Checks:
    - File size thresholds (150-line root, 200-line subdirectory)
    - Broken file/path references within instruction files
    - Stale date references (>30 days old)
    - Duplicate headings across instruction files
    - Missing permission boundaries
    - Positional burial of critical directives
    - Tone overtriggering patterns
    - Gitignore hygiene for local-only files
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Instruction file patterns to scan
INSTRUCTION_PATTERNS = [
    "AGENTS.md", "CLAUDE.md", "CLAUDE.local.md",
    ".cursorrules", "README-agent.md", "AGENTS.override.md",
    ".windsurfrules", ".clinerules", "codex.md",
    ".github/copilot-instructions.md",
]

# Directive verbs that signal a prescriptive use of critical keywords
DIRECTIVE_VERBS = re.compile(
    r"\b(do not|must not|must|never|always|ensure|require|forbid|avoid|prevent)\b",
    re.IGNORECASE,
)

# Overtriggering tone patterns (the bare all-caps token case is handled
# separately in check_tone so filenames/technical tokens can be excluded)
TONE_PATTERNS = [
    re.compile(r"!!!"),
    re.compile(r"ABSOLUTELY\s+(NEVER|DO NOT|MUST)"),
    re.compile(r"YOU MUST (NEVER|NOT|ALWAYS)"),
    re.compile(r"UNDER NO CIRCUMSTANCES"),
]

# All-caps token candidate for tone check
CAPS_TOKEN = re.compile(r"\b[A-Z]{4,}\b")

# Inline code spans — stripped before tone analysis
CODE_SPAN = re.compile(r"`[^`]*`")

# Technical all-caps tokens that are not aggressive tone
CAPS_ALLOWLIST = {
    "AGENTS", "CLAUDE", "SKILL", "README", "CHECKPOINT", "PATH",
    "JSON", "YAML", "HTML", "HTTP", "HTTPS", "TODO", "EPIC", "FEAT",
}

# Permission-related keywords
PERMISSION_KEYWORDS = ["always", "ask first", "ask-first", "never", "approval", "permission"]

# Files that should be gitignored (local-only)
LOCAL_ONLY_FILES = {"CLAUDE.local.md", "AGENTS.override.md"}

# Files that should be committed (shared)
SHARED_FILES = {"AGENTS.md", "CLAUDE.md", ".cursorrules"}


class Finding:
    def __init__(self, file, line, tag, severity, message):
        self.file = file
        self.line = line
        self.tag = tag
        self.severity = severity
        self.message = message

    def __str__(self):
        loc = f"{self.file}:{self.line}" if self.line else self.file
        return f"[{self.severity.upper()}] {self.tag} — {loc}: {self.message}"

    def to_dict(self):
        return {
            "file": self.file, "line": self.line,
            "tag": self.tag, "severity": self.severity,
            "message": self.message,
        }


def find_instruction_files(root):
    """Find all instruction files in the project."""
    found = []
    root = Path(root)
    skip_dirs = {".git", ".svn", ".hg", "node_modules", "__pycache__", "worktrees"}

    def keep_dir(parent, d):
        if d in skip_dirs and not (d == "worktrees" and parent.name != ".claude"):
            return False
        # A `.git` *file* (not directory) marks a worktree checkout — skip it
        # to avoid double-counting nested checkouts.
        git_marker = parent / d / ".git"
        if git_marker.is_file():
            return False
        return True

    for dirpath, dirnames, filenames in os.walk(root):
        dirpath = Path(dirpath)
        dirnames[:] = [d for d in dirnames if keep_dir(dirpath, d)]
        for pattern in INSTRUCTION_PATTERNS:
            filepath = dirpath / pattern
            if filepath.exists():
                found.append(filepath)
    return sorted(set(found))


def is_root_file(filepath, root):
    """Check if instruction file is at project root (always-loaded)."""
    return filepath.parent.resolve() == root.resolve()


def check_file_size(filepath, lines, root):
    """Check file size thresholds, adjusted for root vs subdirectory."""
    findings = []
    n = len(lines)
    at_root = is_root_file(filepath, root)
    if at_root:
        if n > 200:
            findings.append(Finding(
                str(filepath), None, "bloat", "high",
                f"Root file is {n} lines (limit: 200). Split into root + subdirectory files."
            ))
        elif n > 150:
            findings.append(Finding(
                str(filepath), None, "bloat", "medium",
                f"Root file is {n} lines (target: <150). Consider trimming."
            ))
    else:
        if n > 300:
            findings.append(Finding(
                str(filepath), None, "bloat", "high",
                f"Subdirectory file is {n} lines (limit: 300). Split further."
            ))
        elif n > 200:
            findings.append(Finding(
                str(filepath), None, "bloat", "medium",
                f"Subdirectory file is {n} lines (target: <200). Consider trimming."
            ))
    return findings


def check_broken_references(filepath, lines, root):
    """Check for file/path references that don't exist."""
    findings = []
    ref_patterns = [
        re.compile(r"\[.*?\]\(([^)]+)\)"),
        re.compile(r"`((?:\.\.?/)?[\w./-]+\.(?:md|py|sh|ts|js|json|yaml|yml))`"),
    ]
    for i, line in enumerate(lines, 1):
        for pat in ref_patterns:
            for match in pat.finditer(line):
                ref = match.group(1)
                if ref.startswith(("http://", "https://", "#")):
                    continue
                ref_path = (filepath.parent / ref).resolve()
                if not ref_path.exists():
                    findings.append(Finding(
                        str(filepath), i, "context_rot", "high",
                        f"Broken reference: {ref}"
                    ))
    return findings


def check_stale_dates(filepath, lines):
    """Check for date references older than 30 days."""
    findings = []
    now = datetime.now()
    threshold = now - timedelta(days=30)
    date_pattern = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
    for i, line in enumerate(lines, 1):
        for match in date_pattern.finditer(line):
            try:
                d = datetime.strptime(match.group(1), "%Y-%m-%d")
                if d < threshold:
                    findings.append(Finding(
                        str(filepath), i, "context_rot", "medium",
                        f"Date {match.group(1)} is >30 days old. Verify still valid."
                    ))
            except ValueError:
                pass
    return findings


def check_duplicate_headings(all_files_lines):
    """Check for duplicate headings across instruction files."""
    findings = []
    heading_locations = {}
    for filepath, lines in all_files_lines:
        for i, line in enumerate(lines, 1):
            if line.startswith("#"):
                heading = line.strip().lstrip("#").strip().lower()
                if len(heading) > 3:
                    if heading not in heading_locations:
                        heading_locations[heading] = []
                    heading_locations[heading].append((str(filepath), i))
    for heading, locations in heading_locations.items():
        if len(locations) > 1:
            files = ", ".join(f"{f}:{l}" for f, l in locations)
            findings.append(Finding(
                locations[0][0], locations[0][1], "redundancy", "medium",
                f"Heading '{heading}' appears in {len(locations)} files: {files}"
            ))
    return findings


def check_permission_boundaries(filepath, lines):
    """Check if permission boundaries are defined."""
    findings = []
    text = "\n".join(lines).lower()
    has_permissions = any(kw in text for kw in PERMISSION_KEYWORDS)
    if not has_permissions:
        findings.append(Finding(
            str(filepath), None, "missing_permissions", "medium",
            "No permission boundaries (always/ask-first/never) found."
        ))
    return findings


def check_positional_burial(filepath, lines):
    """Check if critical directives are buried in the middle of the file."""
    findings = []
    n = len(lines)
    if n < 20:
        return findings
    threshold_line = int(n * 0.6)
    in_code_block = False
    for i, line in enumerate(lines, 1):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or i <= threshold_line:
            continue
        if line.strip().startswith("#"):
            continue
        # Only flag when a directive verb co-occurs with critical context
        if DIRECTIVE_VERBS.search(line):
            findings.append(Finding(
                str(filepath), i, "positional_burial", "medium",
                f"Directive at line {i}/{n} (after 60% mark). Consider moving earlier."
            ))
    return findings


def check_tone(filepath, lines):
    """Check for overtriggering tone patterns."""
    findings = []
    in_code_block = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Ignore inline code spans — backticked tokens are technical, not tonal.
        stripped = CODE_SPAN.sub("", line)
        hit = any(pat.search(stripped) for pat in TONE_PATTERNS)
        if not hit:
            for match in CAPS_TOKEN.finditer(stripped):
                token = match.group(0)
                if token in CAPS_ALLOWLIST:
                    continue
                # Skip all-caps tokens that are part of a filename (e.g. AGENTS.md).
                end = match.end()
                if end < len(stripped) and stripped[end] == "." and \
                        re.match(r"\.\w", stripped[end:]):
                    continue
                hit = True
                break
        if hit:
            findings.append(Finding(
                str(filepath), i, "tone_overtrigger", "low",
                "Aggressive tone detected. Moderate phrasing improves instruction following."
            ))
    return findings


def check_dangling_references(root):
    """Check skill files for relative references that do not resolve.

    Scans skills/*/SKILL.md and skills/*/references/*.md for markdown links
    and backticked relative paths. Placeholders (containing <, *, or {) are
    tolerated. A reference is dangling only if it resolves neither from the
    containing file's directory nor from the repo root (skill content may
    legitimately use repo-root-relative paths when citing other skills).
    """
    findings = []
    skill_files = sorted(
        list(root.glob("skills/*/SKILL.md")) +
        list(root.glob("skills/*/references/*.md"))
    )
    link_pat = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    # Backticked token that looks like a relative file path: has a slash or
    # a file extension, no spaces, no shell metacharacters beyond placeholders.
    path_like = re.compile(r"^(?:\.\.?/)?[\w.<>{}*-]+(?:/[\w.<>{}*-]+)*\.\w{1,5}$|"
                           r"^(?:\.\.?/)?[\w.<>{}*-]+(?:/[\w.<>{}*-]+)+/?$")
    for filepath in skill_files:
        lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
        in_code_block = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            candidates = [m.group(1) for m in link_pat.finditer(line)]
            # Backticked tokens are only treated as references when they use
            # skill-convention prefixes; bare paths like `src/foo.ts` or
            # `origin/main` are usually illustrative examples, not links.
            for m in CODE_SPAN.finditer(line):
                token = m.group(0)[1:-1]
                if token.startswith(("./", "../", "references/", "scripts/", "skills/")) \
                        and path_like.match(token):
                    candidates.append(token)
            for ref in candidates:
                ref = ref.split("#", 1)[0].strip()
                if not ref or ref.startswith(("http://", "https://", "mailto:", "/", "~")):
                    continue
                if any(c in ref for c in "<*{"):
                    continue  # placeholder path
                if not path_like.match(ref):
                    continue
                if (filepath.parent / ref).exists() or (root / ref).exists():
                    continue
                findings.append(Finding(
                    str(filepath), i, "dangling_reference", "medium",
                    f"Reference '{ref}' does not resolve from {filepath.parent} or repo root."
                ))
    return findings


def check_gitignore(root, found_files):
    """Check gitignore hygiene for instruction files."""
    findings = []
    gitignore_path = root / ".gitignore"
    gitignore_content = ""
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text(encoding="utf-8", errors="replace")
    for filepath in found_files:
        name = filepath.name
        if name in LOCAL_ONLY_FILES:
            if name not in gitignore_content:
                findings.append(Finding(
                    str(filepath), None, "security_gap", "medium",
                    f"Local-only file '{name}' may not be in .gitignore. Verify it is not committed."
                ))
        if name in SHARED_FILES:
            if name in gitignore_content:
                findings.append(Finding(
                    str(filepath), None, "missing_guardrail", "medium",
                    f"Shared file '{name}' appears to be gitignored. It should be committed."
                ))
    return findings


def main():
    parser = argparse.ArgumentParser(description="Validate workspace instruction files.")
    parser.add_argument("root", help="Project root directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    files = find_instruction_files(root)
    dangling_findings = check_dangling_references(root)
    if not files and not dangling_findings:
        if args.format == "json":
            print(json.dumps({"files": 0, "findings": []}))
        else:
            print(f"No instruction files found in {root}")
        sys.exit(0)

    all_findings = []
    all_files_lines = []

    for filepath in files:
        lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
        all_files_lines.append((filepath, lines))
        all_findings.extend(check_file_size(filepath, lines, root))
        all_findings.extend(check_broken_references(filepath, lines, root))
        all_findings.extend(check_stale_dates(filepath, lines))
        all_findings.extend(check_permission_boundaries(filepath, lines))
        all_findings.extend(check_positional_burial(filepath, lines))
        all_findings.extend(check_tone(filepath, lines))

    all_findings.extend(check_duplicate_headings(all_files_lines))
    all_findings.extend(check_gitignore(root, files))
    all_findings.extend(dangling_findings)

    severity_order = {"high": 0, "medium": 1, "low": 2}
    all_findings.sort(key=lambda f: severity_order.get(f.severity, 3))

    if args.format == "json":
        output = {
            "files": len(files),
            "findings": [f.to_dict() for f in all_findings],
            "summary": {
                "high": sum(1 for f in all_findings if f.severity == "high"),
                "medium": sum(1 for f in all_findings if f.severity == "medium"),
                "low": sum(1 for f in all_findings if f.severity == "low"),
            },
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Scanning {len(files)} instruction file(s)...\n")
        if not all_findings:
            print("All checks passed.")
            sys.exit(0)
        print(f"Found {len(all_findings)} issue(s):\n")
        for f in all_findings:
            print(f"  {f}")
        high_count = sum(1 for f in all_findings if f.severity == "high")
        med_count = sum(1 for f in all_findings if f.severity == "medium")
        low_count = sum(1 for f in all_findings if f.severity == "low")
        print(f"\nSummary: {high_count} high, {med_count} medium, {low_count} low")

    high_count = sum(1 for f in all_findings if f.severity == "high")
    sys.exit(1 if high_count > 0 else 0)


if __name__ == "__main__":
    main()
