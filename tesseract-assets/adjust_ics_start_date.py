#!/usr/bin/env python3
"""
Adjust the start date of an .ics calendar by shifting all VEVENT DTSTART/DTEND
timestamps by a computed delta so the earliest event starts on --new-start.

Usage:
  python3 adjust_ics_start_date.py --input "Tesseract Labs.ics" --output "Tesseract Labs.shifted.ics" --new-start 2025-11-17

Behavior:
- Finds the earliest DTSTART among VEVENTs.
- Computes days_delta = (new_start_date - earliest_date).days
- Adds that many days to all DTSTART and DTEND values (preserves time-of-day and 'Z' marker).
- Preserves other ICS content (UID, DESCRIPTION, SUMMARY, VALARM, etc).
- Writes shifted calendar to output file.

Notes:
- The script shifts by whole days. If you need to shift by hours/minutes instead,
  use --shift-hours / --shift-minutes.
- This script only modifies DTSTART and DTEND tokens (and OPTIONALLY DTSTAMP if --update-dtstamp is set).
- Backup your original ICS before running.
"""
from __future__ import annotations
import argparse
import re
from datetime import datetime, timedelta, date

DT_RE = re.compile(r'^(DTSTART(?:;TZID=[^:]+)?|DTEND(?:;TZID=[^:]+)?|DTSTAMP)(:(\d{8}(?:T\d{6})?Z?))\s*$', flags=re.M)

def parse_dt_token(tok: str) -> datetime:
    # tok examples: 20251103T153000Z  or 20251103T153000 or 20251103
    if tok.endswith('Z'):
        if 'T' in tok:
            return datetime.strptime(tok, "%Y%m%dT%H%M%SZ")
        else:
            return datetime.strptime(tok, "%Y%m%dZ")
    if 'T' in tok:
        return datetime.strptime(tok, "%Y%m%dT%H%M%S")
    return datetime.strptime(tok, "%Y%m%d")

def format_dt_token(dt: datetime, original_tok: str) -> str:
    if original_tok.endswith('Z'):
        if 'T' in original_tok:
            return dt.strftime("%Y%m%dT%H%M%SZ")
        else:
            return dt.strftime("%Y%m%dZ")
    if 'T' in original_tok:
        return dt.strftime("%Y%m%dT%H%M%S")
    return dt.strftime("%Y%m%d")

def find_earliest_dt(ics_text: str) -> datetime | None:
    dts = []
    for m in DT_RE.finditer(ics_text):
        key = m.group(1)
        tok = m.group(3)
        # Only consider DTSTART (and DTSTART with TZID). Also ignore DTSTAMP here.
        if key.startswith("DTSTART"):
            try:
                dts.append(parse_dt_token(tok))
            except Exception:
                pass
    return min(dts) if dts else None

def shift_ics(ics_text: str, delta: timedelta, update_dtstamp: bool=False) -> str:
    # Replace each matching DT line with shifted date
    def repl(m):
        key = m.group(1)   # e.g., DTSTART or DTSTART;TZID=Asia/Kolkata
        tok = m.group(3)   # the date token string
        try:
            dt = parse_dt_token(tok)
        except Exception:
            # if parse fails, return original segment unchanged
            return m.group(0)
        new_dt = dt + delta
        new_tok = format_dt_token(new_dt, tok)
        return f"{key}:{new_tok}"
    new_text = DT_RE.sub(repl, ics_text)
    if update_dtstamp:
        # Optionally update any DTSTAMPs to now in UTC (Z)
        nowz = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        new_text = re.sub(r'^(DTSTAMP:)(\d{8}T\d{6}Z)\s*$', f"DTSTAMP:{nowz}", new_text, flags=re.M)
    return new_text

def main():
    p = argparse.ArgumentParser(description="Shift all DTSTART/DTEND in an ICS so earliest event starts on a chosen date.")
    p.add_argument("--input", "-i", required=True, help="Input .ics file")
    p.add_argument("--output", "-o", required=True, help="Output .ics file")
    p.add_argument("--new-start", required=True, help="Desired new earliest start date (YYYY-MM-DD)")
    p.add_argument("--update-dtstamp", action="store_true", help="Also update DTSTAMP lines to now (UTC)")
    p.add_argument("--shift-hours", type=int, default=0, help="Also add additional hours to shift")
    p.add_argument("--shift-minutes", type=int, default=0, help="Also add additional minutes to shift")
    args = p.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        ics = f.read()

    earliest = find_earliest_dt(ics)
    if earliest is None:
        print("No DTSTART found in input ICS. Nothing to do.")
        return

    # Determine delta in days between earliest.date() and new start date
    new_start_date = datetime.strptime(args.new_start, "%Y-%m-%d").date()
    earliest_date = earliest.date()
    days_delta = (new_start_date - earliest_date).days
    delta = timedelta(days=days_delta, hours=args.shift_hours, minutes=args.shift_minutes)

    print(f"Earliest DTSTART found: {earliest.isoformat()} (date {earliest_date.isoformat()})")
    print(f"Desired new start date: {new_start_date.isoformat()} -> shifting by {days_delta} days (+{args.shift_hours} hours, +{args.shift_minutes} minutes)")

    shifted = shift_ics(ics, delta, update_dtstamp=args.update_dtstamp)
    with open(args.output, "w", encoding="utf-8", newline="\n") as f:
        f.write(shifted)

    print(f"Wrote shifted ICS to {args.output}")

if __name__ == "__main__":
    main()