#!/usr/bin/env python3
"""
Assign labels selectively to issues in a repo based on heuristics and milestones based on date.

Usage:
  python3 assign_labels_milestones.py <owner> <repo> [--phases N] [--assignee USER] [--dry-run]

Examples:
  python3 assign_labels_milestones.py bshridhar tesseract-study --phases 3 --assignee bshridhar --dry-run

Description:
  - Intelligently assigns ONE label per issue based on content:
    * "fastapi" when title/body contains: fastapi, pydantic, endpoint, path/query, route, uvicorn
    * "leetcode" when title/body contains: leetcode.com, leetcode, "Problem:"
    * "type:study" when title contains "Study Session", "Weekend Deep" or general study keywords
  - Assigns issues to Phase milestones based on date in title [YYYY-MM-DD]
  - Sets assignee if provided
  - Idempotent: only modifies what needs changing

Requirements:
  - GitHub CLI (gh) installed and authenticated
  - Permission to edit issues in the repository
"""
import argparse
import subprocess
import json
import re
import sys
from datetime import datetime
from math import ceil

DATE_RE = re.compile(r"^\s*\[(\d{4}-\d{2}-\d{2})\]\s*(.*)$")

# Label heuristics
KEYWORDS_FASTAPI = [r"\bfastapi\b", r"\bpydantic\b", r"\bendpoint\b", r"\bpath.query\b", r"\broute\b", r"\buvicorn\b", r"\bTestClient\b"]
KEYWORDS_LEETCODE = [r"leetcode\.com", r"\bleetcode\b", r"\bProblem:", r"https://leetcode\.com/problems", r"\bTwo Sum\b", r"\bAnagram\b", r"\bDuplicate\b", r"\bIntersection\b", r"\bMove Zeroes\b"]
KEYWORDS_STUDY = [r"\bStudy Session\b", r"\bWeekend Deep\b", r"LeetCode \+ FastAPI"]

def run(cmd):
    """Run a shell command and return (code, stdout, stderr)."""
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

def matches_any(text, patterns):
    """Check if text matches any of the regex patterns."""
    if not text:
        return False
    for p in patterns:
        try:
            if re.search(p, text, flags=re.I):
                return True
        except re.error:
            if p.lower() in text.lower():
                return True
    return False

def determine_labels(title, body):
    """
    Determine which labels should be assigned based on content.
    Returns set of label names.
    Can return multiple labels if issue covers multiple topics.
    """
    text = (title or "") + "\n" + (body or "")
    labels = set()
    
    # Check for fastapi
    if matches_any(text, KEYWORDS_FASTAPI):
        labels.add("fastapi")
    
    # Check for leetcode
    if matches_any(text, KEYWORDS_LEETCODE):
        labels.add("leetcode")
    
    # Check for study session
    if matches_any(text, KEYWORDS_STUDY):
        labels.add("type:study")
    
    # If no specific labels matched, default to type:study for study sessions
    if not labels:
        labels.add("type:study")
    
    return labels

def ensure_labels(owner, repo, dry_run=False):
    """Ensure required labels exist in the repo."""
    print("Ensuring labels exist...")
    required = ["fastapi", "leetcode", "type:study"]
    
    code, out, err = run(["gh", "api", f"repos/{owner}/{repo}/labels", "--jq", ".[].name"])
    existing = set()
    if code == 0:
        existing.update([l.strip() for l in out.splitlines() if l.strip()])
    
    for label in required:
        if label in existing:
            print(f"  label exists: {label}")
            continue
        if dry_run:
            print(f"  [DRY-RUN] would create label: {label}")
            continue
        
        color = "0e8a16" if label in ("fastapi", "leetcode") else "ffd966"
        desc = f"Auto-created label '{label}'"
        print(f"  creating label: {label}")
        code, out, err = run(["gh", "label", "create", label, "--color", color, "--description", desc, "--repo", f"{owner}/{repo}"])
        if code != 0:
            print(f"    ERROR creating label {label}: {err}")

def ensure_milestones(owner, repo, phases, dry_run=False):
    """Ensure Phase milestones exist; return dict mapping phase index -> title."""
    print("Ensuring milestones exist...")
    code, out, err = run(["gh", "api", f"repos/{owner}/{repo}/milestones", "--jq", ".[].title"])
    existing = set()
    if code == 0:
        existing.update([l.strip() for l in out.splitlines() if l.strip()])
    
    milestone_map = {}
    for i in range(1, phases + 1):
        title = f"Phase {i}"
        milestone_map[i] = title
        if title in existing:
            print(f"  milestone exists: {title}")
            continue
        if dry_run:
            print(f"  [DRY-RUN] would create milestone: {title}")
            continue
        print(f"  creating milestone: {title}")
        code, out, err = run(["gh", "api", "-X", "POST", f"repos/{owner}/{repo}/milestones", "-f", f"title={title}", "-f", f"description=Auto-created {title}"])
        if code != 0:
            print(f"    ERROR creating milestone {title}: {err}")
    return milestone_map

def list_all_issues(owner, repo):
    """Return list of issue dicts."""
    print("Listing issues...")
    code, out, err = run(["gh", "api", f"repos/{owner}/{repo}/issues", "--paginate", "-X", "GET", "-f", "state=all"])
    if code != 0:
        print("ERROR: Could not list issues:", err)
        sys.exit(1)
    
    try:
        arr = json.loads(out)
    except Exception as e:
        print("ERROR parsing issues JSON:", e)
        sys.exit(1)
    
    issues = []
    for it in arr:
        labels = [l.get("name") for l in it.get("labels", []) if isinstance(l, dict)]
        milestone = it.get("milestone")["title"] if it.get("milestone") else None
        assignees = [a.get("login") for a in it.get("assignees", []) if isinstance(a, dict)]
        issues.append({
            "number": it.get("number"),
            "title": it.get("title", ""),
            "body": it.get("body", ""),
            "labels": labels,
            "milestone": milestone,
            "assignees": assignees
        })
    
    print(f"  Found {len(issues)} issues")
    return issues

def parse_date_from_title(title):
    """Extract date YYYY-MM-DD from title like: [2025-11-03] ..."""
    m = DATE_RE.match(title)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except Exception:
        return None

def compute_phase_for_date(d, start_date, end_date, phases):
    """Return phase index (1..phases) for date d."""
    if d < start_date:
        return 1
    if d > end_date:
        return phases
    total_days = (end_date - start_date).days + 1
    if total_days <= 0:
        return 1
    phase_len = ceil(total_days / phases)
    offset = (d - start_date).days
    idx = offset // phase_len + 1
    if idx > phases:
        idx = phases
    return idx

def edit_issue(owner, repo, number, labels_to_set, labels_to_remove, assignee, milestone_title, dry_run=False):
    """Edit issue with new labels, assignee, and milestone."""
    cmd = ["gh", "issue", "edit", str(number), "--repo", f"{owner}/{repo}"]
    
    for l in labels_to_set:
        cmd.extend(["--add-label", l])
    for l in labels_to_remove:
        cmd.extend(["--remove-label", l])
    if assignee:
        cmd.extend(["--assignee", assignee])
    if milestone_title:
        cmd.extend(["--milestone", milestone_title])
    
    if dry_run:
        print("[DRY-RUN] Would run:", " ".join(cmd))
        return True
    
    code, out, err = run(cmd)
    if code != 0:
        print(f"  ERROR editing issue #{number}: {err}")
        return False
    print(f"  Edited issue #{number}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Assign labels and Phase milestones intelligently.")
    parser.add_argument("owner", help="GitHub owner/org")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("--phases", type=int, default=3, help="Number of phases (default: 3)")
    parser.add_argument("--assignee", default="bshridhar", help="Assignee username")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    args = parser.parse_args()
    
    owner = args.owner
    repo = args.repo
    phases = args.phases
    assignee = args.assignee
    dry_run = args.dry_run
    
    # Ensure labels and milestones exist
    ensure_labels(owner, repo, dry_run=dry_run)
    milestone_map = ensure_milestones(owner, repo, phases, dry_run=dry_run)
    
    # List all issues
    issues = list_all_issues(owner, repo)
    
    # Gather dates to determine date range
    dates = []
    for it in issues:
        d = parse_date_from_title(it["title"])
        if d:
            dates.append(d)
    
    if not dates:
        print("No dated issues found. Nothing to do.")
        sys.exit(0)
    
    start_date = min(dates)
    end_date = max(dates)
    print(f"Using date range {start_date} -> {end_date} to split into {phases} phases")
    
    # Process each issue
    updated = 0
    skipped = 0
    
    for it in issues:
        num = it["number"]
        title = it["title"]
        body = it["body"]
        existing_labels = set(it["labels"])
        existing_milestone = it["milestone"]
        existing_assignees = set(it["assignees"])
        
        # Determine ALL correct labels for this issue
        correct_labels = determine_labels(title, body)
        
        # Determine phase/milestone from date
        d = parse_date_from_title(title)
        milestone_title = None
        if d:
            phase_idx = compute_phase_for_date(d, start_date, end_date, phases)
            milestone_title = milestone_map[phase_idx]
        
        # Figure out what labels to add/remove
        all_possible_labels = {"fastapi", "leetcode", "type:study"}
        labels_to_set = [l for l in correct_labels if l not in existing_labels]
        labels_to_remove = [l for l in existing_labels if l in all_possible_labels and l not in correct_labels]
        
        need_assignee = assignee and assignee not in existing_assignees
        need_milestone = milestone_title and existing_milestone != milestone_title
        
        if not labels_to_set and not labels_to_remove and not need_assignee and not need_milestone:
            skipped += 1
            continue
        
        print(f"Updating issue #{num}: {title}")
        if correct_labels:
            print(f"  correct labels: {sorted(correct_labels)}")
        if labels_to_set:
            print(f"  add labels: {labels_to_set}")
        if labels_to_remove:
            print(f"  remove labels: {labels_to_remove}")
        if need_assignee:
            print(f"  assign: {assignee}")
        if milestone_title:
            print(f"  milestone: {milestone_title}")
        
        ok = edit_issue(owner, repo, num, labels_to_set, labels_to_remove, 
                       assignee if need_assignee else None, 
                       milestone_title if need_milestone else None, 
                       dry_run=dry_run)
        if ok:
            updated += 1
    
    print("Done.")
    print(f"  Issues updated: {updated}")
    print(f"  Issues skipped: {skipped}")
    if dry_run:
        print("Dry-run: no changes were made. Re-run without --dry-run to apply changes.")

if __name__ == "__main__":
    main()
