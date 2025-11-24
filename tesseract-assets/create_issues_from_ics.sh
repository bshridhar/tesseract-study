#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <owner> <repo>"
  echo "Example: $0 bshridhar tesseract-study"
  exit 1
fi

OWNER="$1"
REPO="$2"
ICS_FILE="Tesseract.ics"
LABEL="enhancement"
ASSIGNEE="bshridhar"
MILESTONE_TITLE="Phase 1"

# Check GH CLI
if ! command -v gh >/dev/null 2>&1; then
  echo "gh (GitHub CLI) not found. Install it and run 'gh auth login' before proceeding."
  exit 1
fi

if [ ! -f "$ICS_FILE" ]; then
  echo "File $ICS_FILE not found in current directory. Place your Tesseract.ics here."
  exit 1
fi

# Create milestone if not exists
echo "Ensuring milestone '$MILESTONE_TITLE' exists..."
MILESTONE_ID=$(gh api "repos/${OWNER}/${REPO}/milestones" --jq ".[] | select(.title==\"${MILESTONE_TITLE}\") | .number" 2>/dev/null || true)
if [ -z "$MILESTONE_ID" ]; then
  echo "Milestone not found. Creating milestone '${MILESTONE_TITLE}'..."
  gh api -X POST "repos/${OWNER}/${REPO}/milestones" -f title="${MILESTONE_TITLE}" -f description="Phase 1: initial study schedule (automatically created)"
  MILESTONE_ID=$(gh api "repos/${OWNER}/${REPO}/milestones" --jq ".[] | select(.title==\"${MILESTONE_TITLE}\") | .number")
  echo "Created milestone #${MILESTONE_ID}"
else
  echo "Found milestone #${MILESTONE_ID}"
fi

# Run the python parser/creator
python3 create_issues_from_ics.py "$OWNER" "$REPO" "$ICS_FILE" "$LABEL" "$ASSIGNEE" "$MILESTONE_TITLE"
