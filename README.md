# Tesseract Study — FastAPI + Algorithms

This repository tracks a 6‑month study plan (FastAPI, Python fundamentals, LeetCode).

## 📁 Repository Structure

```
tesseract-study/
├── app/                    # Main FastAPI application
│   ├── __init__.py
│   ├── main.py            # App entry point
│   ├── algorithms.py      # LeetCode implementations
│   └── schemas.py         # Pydantic models
├── tests/                 # Test suite
├── issues/                # LeetCode problem tracking
├── tesseract-assets/      # Scripts, calendars, notes, templates
│   ├── *.ics             # Calendar files
│   ├── *.py              # Utility scripts
│   ├── *.sh              # Shell scripts
│   └── README.md         # Asset documentation
├── projects/              # Example FastAPI/mini projects
│   └── README.md         # Project guidelines
├── docs/                  # ADRs, one-pagers, study notes
│   ├── adr/              # Architecture Decision Records
│   ├── one-pagers/       # Technical deep-dives
│   ├── notes/            # Weekly notes & retrospectives
│   └── README.md         # Documentation guide
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
└── README.md             # This file
```

## Local Development Setup

### Prerequisites
- **Python 3.9+** (Python 3.10+ recommended)
- **pip & virtualenv** 
- **Docker & docker-compose** (for containerized deployment)
- **Git & GitHub CLI (gh)** (for version control and issue management)

### Initial Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```
   
   This includes:
   - `pytest` - Testing framework
   - `black` - Code formatter
   - `flake8` - Linter
   - `mypy` - Static type checker
   - `pytest-cov` - Code coverage
   - `ipython` - Enhanced Python shell
   - `pre-commit` - Git hooks for quality checks

3. **Run the FastAPI application:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Development Workflow

**Code Quality Tools:**
```bash
# Format code with black
black .

# Check code style with flake8
flake8 app/ tests/

# Type check with mypy
mypy app/

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

**Testing:**
```bash
pytest                    # Run all tests
pytest tests/test_two_sum.py  # Run specific test file
pytest -v                 # Verbose output
```

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

## Shift start dates
How to use for your two calendars

1. Back up your originals (just in case).
2. Run for Tesseract Labs:
Command: python3 adjust_ics_start_date.py --input "Tesseract Labs_42f4e74c....ics" --output "Tesseract Labs_shifted.ics" --new-start 2025-11-17
3. Run for Tesseract Podcasts:
Command: python3 adjust_ics_start_date.py --input "Tesseract Podcasts_c71209....ics" --output "Tesseract Podcasts_shifted.ics" --new-start 2025-11-18
