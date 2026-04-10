#!/usr/bin/env python3
"""
Deterministic validation checks for workspace instruction files.

Usage:
    python validate_context.py <project-root>
    python validate_context.py .

Checks:
    - File size thresholds (150-line always-loaded, 200-line split warning)
    - Broken file/path references within instruction files
    - Stale date references (>30 days old)
    - Duplicate headings across instruction files
    - Missing permission boundaries
    - Positional burial of critical keywords
    - Tone overtriggering patterns
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Instruction file patterns to scan
INSTRUCTION_PATTERNS = [
    "AGENTS.md", "CLAUDE.md", ".cursorrules", "README-agent.md",
    "AGENTS.override.md",
]

# Critical keywords that should appear early in files
CRITICAL_KEYWORDS = [
    "never", "must not", "forbidden", "security", "secret",
    "credential", "permission", "auth",
]

# Overtriggering tone patterns
TONE_PATTERNS = [
    r"\b[A-Z]{4,}\b",  # ALL CAPS words (4+ chars)
    r"!!!",             # Triple exclamation
    r"ABSOLUTELY\s+(NEVER|DO NOT|MUST)",
    r"YOU MUST (NEVER|NOT|ALWAYS)",
    r"UNDER NO CIRCUMSTANCES",
]

# Permission-related keywords
PERMISSION_KEYWORDS = ["always", "ask first", "ask-first", "never", "approval", "permission"]


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


def find_instruction_files(root):
    """Find all instruction files in the project."""
    found = []
    root = Path(root)
    for dirpath, _, filenames in os.walk(root):
        dirpath = Path(dirpath)
        # Skip hidden dirs except .cursorrules
        if any(p.startswith(".") and p != ".cursorrules" for p in dirpath.parts):
            if ".git" in dirpath.parts:
                continue
        for pattern in INSTRUCTION_PATTERNS:
            filepath = dirpath / pattern
            if filepath.exists():
                found.append(filepath)
        # Also pick up subdirectory AGENTS.md / CLAUDE.md
        for f in filenames:
            if f in ("AGENTS.md", "CLAUDE.md") and (dirpath / f) not in found:
                found.append(dirpath / f)
    return sorted(set(found))


def check_file_size(filepath, lines):
    """Check file size thresholds."""
    findings = []
    n = len(lines)
    if n > 200:
        findings.append(Finding(
            str(filepath), None, "bloat",
            "high",
            f"File is {n} lines (threshold: 200). Split into root + subdirectory files."
        ))
    elif n > 150:
        findings.append(Finding(
            str(filepath), None, "bloat",
            "medium",
            f"File is {n} lines (target: <150 for always-loaded). Consider trimming."
        ))
    return findings


def check_broken_references(filepath, lines, root):
    """Check for file/path references that don't exist."""
    findings = []
    # Match markdown links and backtick paths
    ref_patterns = [
        re.compile(r"\[.*?\]\(([^)]+)\)"),                     # [text](path)
        re.compile(r"`((?:\.\.?/)?[\w./-]+\.(?:md|py|sh|ts|js|json|yaml|yml))`"),  # `path.ext`
    ]
    for i, line in enumerate(lines, 1):
        for pat in ref_patterns:
            for match in pat.finditer(line):
                ref = match.group(1)
                if ref.startswith("http://") or ref.startswith("https://"):
                    continue
                ref_path = (filepath.parent / ref).resolve()
                if not ref_path.exists():
                    findings.append(Finding(
                        str(filepath), i, "context_rot",
                        "high",
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
                        str(filepath), i, "context_rot",
                        "medium",
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
                if len(heading) > 3:  # skip tiny headings
                    key = heading
                    if key not in heading_locations:
                        heading_locations[key] = []
                    heading_locations[key].append((str(filepath), i))
    for heading, locations in heading_locations.items():
        if len(locations) > 1:
            files = ", ".join(f"{f}:{l}" for f, l in locations)
            findings.append(Finding(
                locations[0][0], locations[0][1], "redundancy",
                "medium",
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
            str(filepath), None, "missing_permissions",
            "medium",
            "No permission boundaries (always/ask-first/never) found."
        ))
    return findings


def check_positional_burial(filepath, lines):
    """Check if critical keywords are buried in the middle of the file."""
    findings = []
    n = len(lines)
    if n < 20:
        return findings
    threshold_line = int(n * 0.6)
    for i, line in enumerate(lines, 1):
        if i <= threshold_line:
            continue
        lower = line.lower()
        for kw in CRITICAL_KEYWORDS:
            if kw in lower and not line.strip().startswith("#"):
                findings.append(Finding(
                    str(filepath), i, "positional_burial",
                    "medium",
                    f"Critical keyword '{kw}' at line {i}/{n} (after 60% mark). Consider moving earlier."
                ))
                break  # one finding per line
    return findings


def check_tone(filepath, lines):
    """Check for overtriggering tone patterns."""
    findings = []
    for i, line in enumerate(lines, 1):
        for pat in TONE_PATTERNS:
            if re.search(pat, line):
                findings.append(Finding(
                    str(filepath), i, "tone_overtrigger",
                    "low",
                    f"Aggressive tone detected. Moderate phrasing improves instruction following."
                ))
                break  # one finding per line
    return findings


def main():
    parser = argparse.ArgumentParser(description="Validate workspace instruction files.")
    parser.add_argument("root", help="Project root directory to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    files = find_instruction_files(root)
    if not files:
        print(f"No instruction files found in {root}")
        sys.exit(0)

    print(f"Scanning {len(files)} instruction file(s)...\n")

    all_findings = []
    all_files_lines = []

    for filepath in files:
        lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
        all_files_lines.append((filepath, lines))
        all_findings.extend(check_file_size(filepath, lines))
        all_findings.extend(check_broken_references(filepath, lines, root))
        all_findings.extend(check_stale_dates(filepath, lines))
        all_findings.extend(check_permission_boundaries(filepath, lines))
        all_findings.extend(check_positional_burial(filepath, lines))
        all_findings.extend(check_tone(filepath, lines))

    all_findings.extend(check_duplicate_headings(all_files_lines))

    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    all_findings.sort(key=lambda f: severity_order.get(f.severity, 3))

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

    sys.exit(1 if high_count > 0 else 0)


if __name__ == "__main__":
    main()
