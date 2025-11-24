#!/usr/bin/env python3
"""
Parse an .ics file and create GitHub issues (one per VEVENT) using 'gh issue create'.

Usage:
  python3 create_issues_from_ics.py <owner> <repo> <ics_file> <label> <assignee> <milestone_title> [--dry-run]

Example:
  python3 create_issues_from_ics.py bshridhar tesseract-study Tesseract.ics enhancement bshridhar "Phase 1" --dry-run

Notes:
- Requires GitHub CLI (gh) installed and authenticated (gh auth login).
- Uses `gh issue create --repo owner/repo --title ... --label X --assignee user --milestone "TITLE" --body-file file`.
- --dry-run will print actions without creating issues.
"""
import sys
import subprocess
import json
import re
import tempfile
import os
import time
from datetime import datetime

def run(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def gh_list_issue_titles(owner, repo):
    # returns a set of issue titles (open and closed)
    cmd = ["gh", "api", f"repos/{owner}/{repo}/issues", "--jq", ".[].title", "--paginate"]
    code, out, err = run(cmd)
    if code != 0:
        raise RuntimeError(f"gh api list issues failed: {err}")
    titles = set([t.strip() for t in out.splitlines() if t.strip()])
    return titles

def create_issue_with_gh(owner, repo, title, body_file_path, label, assignee, milestone_title, dry_run=False, max_retries=3):
    base_cmd = [
        "gh", "issue", "create", "--repo", f"{owner}/{repo}",
        "--title", title,
        "--body-file", body_file_path
    ]
    if label:
        base_cmd.extend(["--label", label])
    if assignee:
        base_cmd.extend(["--assignee", assignee])
    if milestone_title:
        base_cmd.extend(["--milestone", milestone_title])

    if dry_run:
        print("[DRY-RUN] Would run:", " ".join(map(lambda s: f"'{s}'" if " " in s else s, base_cmd)))
        return True

    # Retry logic for transient API failures (502, 503, rate limits)
    for attempt in range(max_retries):
        code, out, err = run(base_cmd)
        
        if code == 0:
            print(f"  Created: {title}")
            return True
        
        # Check if error is retryable (HTTP 502, 503, rate limit)
        is_retryable = any(x in err for x in ["502", "503", "rate limit", "Bad Gateway", "Service Unavailable"])
        
        if is_retryable and attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
            print(f"  Transient error, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
        else:
            # Non-retryable error or max retries reached
            print(f"  ERROR creating issue '{title}': {err}")
            return False
    
    return False

def parse_ics(ics_path):
    with open(ics_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Unfold folded lines per RFC5545 (lines starting with space are continuations)
    content = re.sub(r"\r?\n[ \t]", "", content)

    vevents = re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", content, flags=re.S | re.I)
    events = []
    for block in vevents:
        # DTSTART (capture date)
        dt_match = re.search(r"DTSTART(?:;[^:]*)?:(\d{8})(?:T\d{6})?", block)
        if not dt_match:
            dt_match = re.search(r"DTSTART(?:;[^:]*)?:(\d{8}T\d{6})", block)
        if not dt_match:
            continue
        dt_raw = dt_match.group(1)
        date_str = dt_raw[:8]
        try:
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            date_iso = date_obj.strftime("%Y-%m-%d")
        except Exception:
            continue

        # SUMMARY
        summary_match = re.search(r"SUMMARY:(.*?)(?:\r?\n|$)", block)
        summary = summary_match.group(1).strip() if summary_match else "Tesseract — Study Session"

        # DESCRIPTION (may include newlines)
        desc_match = re.search(r"DESCRIPTION:(.*)", block, flags=re.S)
        if desc_match:
            desc = desc_match.group(1).strip()
            # stop at next uppercase property if present (safety)
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

def strip_ciu_lines(text):
    if not text:
        return text
    filtered = []
    for line in text.splitlines():
        low = line.lower()
        if "coding-interview-university" in low or re.search(r"\bciu\b", low):
            continue
        filtered.append(line)
    return "\n".join(filtered).strip()

def main():
    args = sys.argv[1:]
    dry_run = False
    if "--dry-run" in args:
        dry_run = True
        args.remove("--dry-run")

    if len(args) != 6:
        print("Usage: create_issues_from_ics.py <owner> <repo> <ics_file> <label> <assignee> <milestone_title> [--dry-run]")
        sys.exit(1)
    owner, repo, ics_file, label, assignee, milestone_title = args

    if not os.path.isfile(ics_file):
        print(f"ICS file not found: {ics_file}")
        sys.exit(1)

    print("Parsing ICS:", ics_file)
    events = parse_ics(ics_file)
    print(f"Found {len(events)} VEVENTs in {ics_file}")

    try:
        existing_titles = gh_list_issue_titles(owner, repo)
    except Exception as e:
        print("ERROR: could not list existing issues via gh:", e)
        print("Ensure 'gh' is installed and you have access to the repository.")
        sys.exit(1)

    created = 0
    skipped = 0
    for ev in events:
        title = f"[{ev['date']}] {ev['summary']}"
        body = ev['description'] or f"{ev['summary']} on {ev['date']}"
        body = strip_ciu_lines(body)
        # If empty body after stripping, provide short fallback
        if not body:
            body = f"{ev['summary']} ({ev['date']})"

        if title in existing_titles:
            print(f"Skipping (exists): {title}")
            skipped += 1
            continue

        # write body to a temporary file and pass to gh issue create
        tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=".md")
        try:
            tmp.write(body)
            tmp.close()
            ok = create_issue_with_gh(owner, repo, title, tmp.name, label, assignee, milestone_title, dry_run=dry_run)
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass

        if ok:
            created += 1
            existing_titles.add(title)

    print("Summary:")
    print(f"  Created: {created}")
    print(f"  Skipped (already existed): {skipped}")
    if dry_run:
        print("Dry-run mode: no changes were made. Re-run without --dry-run to actually create issues.")

if __name__ == "__main__":
    main()
