#!/usr/bin/env python3
"""
Unified script to create GitHub issues from .ics file with intelligent labels and phase milestones.

Usage:
  python3 create_and_organize_issues.py <owner> <repo> <ics_file> --phases <N> [--assignee USER] [--dry-run]

Example:
  python3 create_and_organize_issues.py bshridhar tesseract-study Tesseract.ics --phases 3 --assignee bshridhar --dry-run

Features:
- Creates one issue per calendar event
- Intelligently assigns 1-3 labels based on content (fastapi, leetcode, type:study)
- Distributes issues across Phase 1..N based on dates
- Sets assignee on all issues
- Includes retry logic for transient API failures
- Skips issues that already exist
"""
import sys
import subprocess
import re
import tempfile
import os
import time
import argparse
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
    """Determine which labels should be assigned based on content."""
    text = (title or "") + "\n" + (body or "")
    labels = set()
    
    if matches_any(text, KEYWORDS_FASTAPI):
        labels.add("fastapi")
    if matches_any(text, KEYWORDS_LEETCODE):
        labels.add("leetcode")
    if matches_any(text, KEYWORDS_STUDY):
        labels.add("type:study")
    
    # Default to type:study if no specific labels matched
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
            print(f"  ✓ {label}")
            continue
        if dry_run:
            print(f"  [DRY-RUN] would create label: {label}")
            continue
        
        color = "0e8a16" if label in ("fastapi", "leetcode") else "ffd966"
        desc = f"Auto-created label '{label}'"
        print(f"  Creating: {label}")
        code, out, err = run(["gh", "label", "create", label, "--color", color, "--description", desc, "--repo", f"{owner}/{repo}"])
        if code != 0:
            print(f"    ERROR: {err}")

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
            print(f"  ✓ {title}")
            continue
        if dry_run:
            print(f"  [DRY-RUN] would create milestone: {title}")
            continue
        print(f"  Creating: {title}")
        code, out, err = run(["gh", "api", "-X", "POST", f"repos/{owner}/{repo}/milestones", "-f", f"title={title}", "-f", f"description=Auto-created {title}"])
        if code != 0:
            print(f"    ERROR: {err}")
    return milestone_map

def gh_list_issue_titles(owner, repo):
    """Return set of existing issue titles."""
    cmd = ["gh", "api", f"repos/{owner}/{repo}/issues", "--jq", ".[].title", "--paginate"]
    code, out, err = run(cmd)
    if code != 0:
        raise RuntimeError(f"Failed to list issues: {err}")
    return set([t.strip() for t in out.splitlines() if t.strip()])

def parse_date_from_title(title):
    """Extract date from title like: [2025-11-03] ..."""
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

def create_issue(owner, repo, title, body, labels, assignee, milestone, dry_run=False, max_retries=3):
    """Create a GitHub issue with retry logic."""
    # Write body to temp file
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=".md")
    try:
        tmp.write(body)
        tmp.close()
        
        cmd = ["gh", "issue", "create", "--repo", f"{owner}/{repo}", "--title", title, "--body-file", tmp.name]
        for label in labels:
            cmd.extend(["--label", label])
        if assignee:
            cmd.extend(["--assignee", assignee])
        if milestone:
            cmd.extend(["--milestone", milestone])
        
        if dry_run:
            print(f"[DRY-RUN] Would create: {title}")
            print(f"  Labels: {', '.join(labels)}")
            print(f"  Milestone: {milestone}")
            return True
        
        # Retry logic
        for attempt in range(max_retries):
            code, out, err = run(cmd)
            
            if code == 0:
                print(f"✓ Created: {title}")
                print(f"  Labels: {', '.join(labels)} | Milestone: {milestone}")
                return True
            
            is_retryable = any(x in err for x in ["502", "503", "rate limit", "Bad Gateway", "Service Unavailable"])
            
            if is_retryable and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"  Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"✗ ERROR: {title}")
                print(f"  {err}")
                return False
        
        return False
    finally:
        try:
            os.unlink(tmp.name)
        except Exception:
            pass

def parse_ics(ics_path):
    """Parse ICS file and return list of events."""
    with open(ics_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Unfold folded lines
    content = re.sub(r"\r?\n[ \t]", "", content)
    
    vevents = re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", content, flags=re.S | re.I)
    events = []
    
    for block in vevents:
        # Extract date
        dt_match = re.search(r"DTSTART(?:;[^:]*)?:(\d{8})(?:T\d{6})?", block)
        if not dt_match:
            continue
        
        date_str = dt_match.group(1)[:8]
        try:
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            date_iso = date_obj.strftime("%Y-%m-%d")
        except Exception:
            continue
        
        # Extract summary
        summary_match = re.search(r"SUMMARY:(.*?)(?:\r?\n|$)", block)
        summary = summary_match.group(1).strip() if summary_match else "Tesseract — Study Session"
        
        # Extract description
        desc_match = re.search(r"DESCRIPTION:(.*)", block, flags=re.S)
        if desc_match:
            desc = desc_match.group(1).strip()
            desc = re.split(r"\r?\n[A-Z]{1,20}:", desc, maxsplit=1)[0].strip()
            desc = re.sub(r"\r?\n", "\n", desc)
        else:
            desc = ""
        
        events.append({
            "date": date_iso,
            "summary": summary,
            "description": desc
        })
    
    return events

def main():
    parser = argparse.ArgumentParser(description="Create and organize GitHub issues from calendar")
    parser.add_argument("owner", help="GitHub owner/org")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("ics_file", help="Path to .ics calendar file")
    parser.add_argument("--phases", type=int, default=3, help="Number of phases (default: 3)")
    parser.add_argument("--assignee", default="bshridhar", help="Assignee username")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating")
    args = parser.parse_args()
    
    if not os.path.isfile(args.ics_file):
        print(f"ERROR: File not found: {args.ics_file}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"Creating Issues from {args.ics_file}")
    print(f"Repository: {args.owner}/{args.repo}")
    print(f"Phases: {args.phases} | Assignee: {args.assignee}")
    print(f"{'='*60}\n")
    
    # Ensure labels and milestones exist
    ensure_labels(args.owner, args.repo, args.dry_run)
    milestone_map = ensure_milestones(args.owner, args.repo, args.phases, args.dry_run)
    
    # Parse ICS file
    print(f"\nParsing {args.ics_file}...")
    events = parse_ics(args.ics_file)
    print(f"Found {len(events)} events\n")
    
    # Get date range for phase calculation
    dates = [datetime.strptime(ev["date"], "%Y-%m-%d").date() for ev in events]
    start_date = min(dates)
    end_date = max(dates)
    print(f"Date range: {start_date} → {end_date}")
    print(f"Dividing into {args.phases} phases\n")
    
    # Get existing issues
    try:
        existing_titles = gh_list_issue_titles(args.owner, args.repo)
    except Exception as e:
        print(f"ERROR: Could not list issues: {e}")
        sys.exit(1)
    
    # Process each event
    print("Creating issues...\n")
    created = 0
    skipped = 0
    
    for ev in events:
        title = f"[{ev['date']}] {ev['summary']}"
        body = ev['description'] or f"{ev['summary']} on {ev['date']}"
        
        if title in existing_titles:
            print(f"⊘ Skipped (exists): {title}")
            skipped += 1
            continue
        
        # Determine labels and phase
        labels = determine_labels(title, body)
        date_obj = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        phase_idx = compute_phase_for_date(date_obj, start_date, end_date, args.phases)
        milestone = milestone_map[phase_idx]
        
        # Create issue
        if create_issue(args.owner, args.repo, title, body, labels, args.assignee, milestone, args.dry_run):
            created += 1
            existing_titles.add(title)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"{'='*60}")
    
    if args.dry_run:
        print("\nDry-run mode: No changes made. Run without --dry-run to create issues.")

if __name__ == "__main__":
    main()
