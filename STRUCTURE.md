# Repository Structure Overview

This document provides a complete overview of the Tesseract Study repository structure.

## 📂 Directory Tree

```
tesseract-study/
│
├── .venv/                      # Virtual environment (gitignored)
├── .gitignore                  # Git ignore rules
├── README.md                   # Main project documentation
├── SETUP.md                    # Development environment setup guide
├── STRUCTURE.md                # This file - repository structure overview
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
│
├── app/                        # Main FastAPI Application
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   ├── algorithms.py          # LeetCode algorithm implementations
│   └── schemas.py             # Pydantic data models
│
├── tests/                      # Test Suite
│   ├── __init__.py
│   └── test_two_sum.py        # Example test file
│
├── issues/                     # LeetCode Problem Tracking
│   ├── README.md
│   └── 2025-11-03-two-sum.md  # Problem documentation
│
├── tesseract-assets/          # Scripts, Calendars, Notes, Templates
│   ├── README.md              # Asset documentation
│   │
│   ├── Calendar Files (.ics)
│   │   ├── Tesseract.ics
│   │   ├── Tesseract Labs.ics
│   │   ├── Tesseract Podcasts.ics
│   │   └── *_shifted.ics
│   │
│   ├── Issue Management Scripts
│   │   ├── create_and_organize_issues.py
│   │   ├── create_issues_from_ics.py
│   │   ├── create_issues_from_ics.sh
│   │   ├── delete_all_issues.sh
│   │   └── assign_labels_milestones.py
│   │
│   ├── Calendar Processing Scripts
│   │   ├── adjust_ics_start_date.py
│   │   └── fix_tesseract_ics.py
│   │
│   └── Data Conversion
│       ├── convert_to_google_csv.py
│       ├── google_import.csv
│       └── commute_podcasts_curated.csv
│
├── projects/                   # Example Projects & Mini-Apps
│   ├── README.md              # Project guidelines and templates
│   └── [future-projects]/     # Individual project directories
│
└── docs/                       # Documentation & ADRs
    ├── README.md              # Documentation guide
    │
    ├── adr/                   # Architecture Decision Records
    │   └── [future ADRs]      # e.g., adr-001-use-fastapi.md
    │
    ├── one-pagers/           # Technical Deep-Dives
    │   └── [future docs]      # e.g., fastapi-basics.md
    │
    └── notes/                # Study Notes
        ├── [weekly notes]     # e.g., week-01-fastapi-setup.md
        └── retrospectives/   # Weekly retrospectives
            └── [retros]       # e.g., 2025-11-week1.md
```

## 📝 Directory Purposes

### Core Application
- **`app/`** - Main FastAPI application with algorithms and schemas
- **`tests/`** - Unit and integration tests

### Study & Tracking
- **`issues/`** - LeetCode problem documentation and solutions
- **`tesseract-assets/`** - Utility scripts, calendars, and templates

### Learning & Projects
- **`projects/`** - Individual learning projects and FastAPI examples
- **`docs/`** - Architecture decisions, technical one-pagers, study notes

### Configuration
- Root level files for dependencies, setup, and git configuration

## 🎯 Quick Navigation

### Starting Development
1. See **SETUP.md** for environment setup
2. See **README.md** for project overview
3. See **requirements-dev.txt** for installed tools

### Working on Features
1. Check **issues/** for LeetCode problems
2. Implement in **app/algorithms.py**
3. Add tests in **tests/**

### Creating Projects
1. See **projects/README.md** for guidelines
2. Create new project directory
3. Follow project template structure

### Documentation
1. **docs/adr/** - Architectural decisions
2. **docs/one-pagers/** - Technical topics
3. **docs/notes/** - Weekly learnings

### Utilities
1. **tesseract-assets/** - All helper scripts
2. See **tesseract-assets/README.md** for usage

## 🔄 Workflow

```
1. Issue Created (from calendar or manual)
   ↓
2. Branch Created (feat/<name>)
   ↓
3. Implementation (app/, tests/)
   ↓
4. Testing (pytest, coverage)
   ↓
5. Code Quality (black, flake8, mypy)
   ↓
6. PR & Review
   ↓
7. Merge & Close Issue
   ↓
8. Documentation (docs/)
```

## 📊 File Type Distribution

| Type | Location | Purpose |
|------|----------|---------|
| Python (.py) | app/, tests/ | Application & test code |
| Markdown (.md) | docs/, root | Documentation |
| Calendar (.ics) | tesseract-assets/ | Study schedule |
| Config | Root | requirements.txt, .gitignore |
| Scripts | tesseract-assets/ | Automation utilities |

## 🚀 Getting Started Checklist

- [x] Repository structured
- [x] Virtual environment created
- [x] Dependencies installed
- [x] Documentation organized
- [ ] First project created
- [ ] ADRs documented
- [ ] Weekly notes started

---

**Last Updated:** 2025-11-20
