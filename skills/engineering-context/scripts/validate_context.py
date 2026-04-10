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

# Overtriggering tone patterns
TONE_PATTERNS = [
    re.compile(r"\b[A-Z]{4,}\b"),
    re.compile(r"!!!"),
    re.compile(r"ABSOLUTELY\s+(NEVER|DO NOT|MUST)"),
    re.compile(r"YOU MUST (NEVER|NOT|ALWAYS)"),
    re.compile(r"UNDER NO CIRCUMSTANCES"),
]

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
    skip_dirs = {".git", ".svn", ".hg", "node_modules", "__pycache__"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirpath = Path(dirpath)
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
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
        for pat in TONE_PATTERNS:
            if pat.search(line):
                findings.append(Finding(
                    str(filepath), i, "tone_overtrigger", "low",
                    "Aggressive tone detected. Moderate phrasing improves instruction following."
                ))
                break
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
    if not files:
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
