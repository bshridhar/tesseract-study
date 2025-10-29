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

Workflow
- Create an issue for a task (title: `[YYYY-MM-DD] <short description>`)
- Create a branch `feat/<short>` when you start
- Open PR, link the issue, and request review
- Merge once CI passes and close the issue
