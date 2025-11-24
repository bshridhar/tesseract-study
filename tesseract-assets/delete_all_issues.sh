#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <owner> <repo>"
  echo "Example: $0 bshridhar tesseract-study"
  echo ""
  echo "WARNING: This will DELETE ALL issues in the repository!"
  exit 1
fi

OWNER="$1"
REPO="$2"

# Check GH CLI
if ! command -v gh >/dev/null 2>&1; then
  echo "gh (GitHub CLI) not found. Install it and run 'gh auth login' before proceeding."
  exit 1
fi

echo "=========================================="
echo "WARNING: This will DELETE ALL ISSUES in ${OWNER}/${REPO}"
echo "=========================================="
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirmation

if [ "$confirmation" != "yes" ]; then
  echo "Aborted."
  exit 0
fi

echo ""
echo "Fetching all issues..."

# Get all issue numbers (open and closed)
ISSUE_NUMBERS=$(gh api "repos/${OWNER}/${REPO}/issues?state=all&per_page=100" --paginate --jq '.[].number' 2>/dev/null || true)

if [ -z "$ISSUE_NUMBERS" ]; then
  echo "No issues found or error fetching issues."
  exit 0
fi

TOTAL=$(echo "$ISSUE_NUMBERS" | wc -l | tr -d ' ')
echo "Found ${TOTAL} issues to delete."
echo ""

deleted=0
failed=0

for num in $ISSUE_NUMBERS; do
  echo "Deleting issue #${num}..."
  
  # GitHub API doesn't allow deleting issues via standard endpoints
  # We'll close them and add a "DELETED" label instead
  # If you have admin access, you could use the GraphQL API to delete
  
  # Close the issue
  if gh issue close "$num" --repo "${OWNER}/${REPO}" --reason "not planned" 2>/dev/null; then
    ((deleted++))
    echo "  Closed issue #${num}"
  else
    ((failed++))
    echo "  ERROR: Failed to close issue #${num}"
  fi
done

echo ""
echo "=========================================="
echo "Summary:"
echo "  Issues closed: ${deleted}"
echo "  Failed: ${failed}"
echo "=========================================="
echo ""
echo "Note: GitHub does not allow deleting issues via API."
echo "Issues have been closed with reason 'not planned'."
echo "To permanently delete them, you must do so manually via the GitHub web interface."
