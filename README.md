# Tesseract Study — FastAPI + Algorithms

This repository tracks a 6‑month study plan (FastAPI, Python fundamentals, LeetCode) and contains:
- A FastAPI starter app in `app/`
- LeetCode solutions in `problems/` organized by topic and date
- Tests in `tests/` run by GitHub Actions CI
- Study plan and weekly retrospectives in `STUDY_PLAN.md` and `docs/`
- Calendar file `TESSERACT.ics` (optional) you can import into Google Calendar

How to run locally
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. uvicorn app.main:app --reload --port 8000

Testing
- pytest

## Populating Issues from Calendar

This project includes a unified script to create GitHub issues from the `Tesseract.ics` calendar file with intelligent labels and phase milestones in one command:

### Quick Start
```bash
# Preview (dry-run)
python3 create_and_organize_issues.py bshridhar tesseract-study Tesseract.ics --phases 3 --assignee bshridhar --dry-run

# Create for real
python3 create_and_organize_issues.py bshridhar tesseract-study Tesseract.ics --phases 3 --assignee bshridhar
```

### What This Script Does

**create_and_organize_issues.py** - One command to do it all:
- Parses all events from `Tesseract.ics`
- Creates one GitHub issue per calendar event with format: `[YYYY-MM-DD] Event Summary`
- Intelligently assigns 1-3 labels per issue based on content:
  - `fastapi` - for FastAPI/Pydantic implementation tasks
  - `leetcode` - for algorithm problems  
  - `type:study` - for general study sessions
- Distributes issues across Phase 1, 2, 3 based on date ranges
- Sets assignee on all issues
- Includes retry logic for transient API failures (HTTP 502, 503)
- Skips issues that already exist (idempotent)
- Shows clear progress with ✓ and ✗ indicators

**delete_all_issues.sh** (optional)
- Closes all issues in the repository
- Use when starting fresh: `./delete_all_issues.sh bshridhar tesseract-study`

### Requirements
- GitHub CLI (`gh`) installed and authenticated (`gh auth login`)
- Python 3.x with standard libraries
- Write access to the repository

## Workflow
- Issues are auto-created from calendar events
- Create a branch `feat/<short>` when you start working
- Open PR, link the issue, and request review
- Merge once CI passes and close the issue
