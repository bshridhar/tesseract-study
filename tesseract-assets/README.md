# Tesseract Assets

This directory contains utility scripts, calendar files, notes, and templates for managing the Tesseract Study project.

## Contents

### 📅 Calendar Files
- `Tesseract.ics` - Main study calendar
- `Tesseract Labs.ics` - Labs/implementation tasks calendar
- `Tesseract Podcasts.ics` - Podcast study calendar
- `*.ics` - Various shifted and processed calendar files

### 🔧 Utility Scripts

#### Issue Management
- `create_and_organize_issues.py` - Creates GitHub issues from calendar with labels and milestones
- `create_issues_from_ics.py` - Basic issue creation from ICS files
- `create_issues_from_ics.sh` - Shell script wrapper for issue creation
- `delete_all_issues.sh` - Closes all issues in repository (use with caution)
- `assign_labels_milestones.py` - Assigns labels and milestones to existing issues

#### Calendar Processing
- `adjust_ics_start_date.py` - Shifts calendar start dates
- `fix_tesseract_ics.py` - Calendar file cleanup and validation

#### Data Conversion
- `convert_to_google_csv.py` - Converts data to Google Calendar CSV format
- `google_import.csv` - Google Calendar import template
- `commute_podcasts_curated.csv` - Curated podcast list

### 📝 Documentation
- `SETUP.md` - Development environment setup guide

## Usage Examples

### Create Issues from Calendar
```bash
# Dry run (preview)
python3 tesseract-assets/create_and_organize_issues.py \
  bshridhar tesseract-study \
  tesseract-assets/Tesseract.ics \
  --phases 3 --assignee bshridhar --dry-run

# Create for real
python3 tesseract-assets/create_and_organize_issues.py \
  bshridhar tesseract-study \
  tesseract-assets/Tesseract.ics \
  --phases 3 --assignee bshridhar
```

### Shift Calendar Dates
```bash
python3 tesseract-assets/adjust_ics_start_date.py \
  --input "tesseract-assets/Tesseract Labs.ics" \
  --output "tesseract-assets/Tesseract Labs_shifted.ics" \
  --new-start 2025-11-17
```

### Delete All Issues (CAUTION)
```bash
./tesseract-assets/delete_all_issues.sh bshridhar tesseract-study
```

## Notes

- Keep calendar files and scripts organized here
- Scripts should be run from the project root directory
- Backup important calendar files before processing
