#!/usr/bin/env python3
"""
Fix Tesseract.ics by sorting VEVENTs by DTSTART and inserting a 30-minute
DISPLAY VALARM for each event that does not already contain a VALARM.

Usage:
  python3 fix_tesseract_ics.py Tesseract.ics > Tesseract.fixed.ics
  # or write to file:
  python3 fix_tesseract_ics.py Tesseract.ics Tesseract.fixed.ics

Behavior:
- Preserves everything outside VEVENT blocks (headers, VTIMEZONE, etc.).
- Parses each VEVENT, extracts DTSTART (handles date and datetime with or
  without trailing 'Z' and DTSTART with TZID=...).
- If a VEVENT already contains a BEGIN:VALARM block, it is left unchanged.
- If a VEVENT has no VALARM, a DISPLAY alarm with TRIGGER:-PT30M is inserted
  immediately before END:VEVENT.
- VEVENTs are sorted by the parsed DTSTART ascending.
- Writes a full, valid VCALENDAR to stdout or to the output file if provided.

Notes:
- This script is conservative: it does not attempt to normalize timezones,
  it simply parses the DTSTART token for ordering.
- Make a backup of your original ICS before overwriting.
"""
import sys
import re
from datetime import datetime

VALARM_BLOCK = (
    "BEGIN:VALARM\n"
    "ACTION:DISPLAY\n"
    "DESCRIPTION:Reminder\n"
    "TRIGGER:-PT30M\n"
    "END:VALARM\n"
)

DTSTART_RE = re.compile(r'(^DTSTART(?:;[^:]*)?:)(\d{8}(?:T\d{6}Z?)?)', re.M | re.I)
VEVENT_RE = re.compile(r'BEGIN:VEVENT(.*?)END:VEVENT', re.S | re.I)

def parse_dt(dt_token):
    """Parse the DTSTART datetime token (string like 20251103 or 20251103T210000 or ...Z)."""
    s = dt_token
    try:
        if len(s) == 8:
            return datetime.strptime(s, "%Y%m%d")
        if s.endswith('Z'):
            return datetime.strptime(s, "%Y%m%dT%H%M%SZ")
        return datetime.strptime(s, "%Y%m%dT%H%M%S")
    except Exception:
        # fallback: try to extract date part
        m = re.match(r'(\d{8})', s)
        if m:
            try:
                return datetime.strptime(m.group(1), "%Y%m%d")
            except Exception:
                pass
    # Last-resort: return epoch so it sorts first
    return datetime(1970,1,1)

def ensure_valarm_in_vevent(block):
    """Return block with VALARM inserted if none present (preserve existing trailing newlines)."""
    if re.search(r'BEGIN:VALARM', block, re.I):
        return block  # already has an alarm
    # Insert VALARM just before the END:VEVENT (we're operating on the inner content)
    # The block currently represents the inner content matched by VEVENT_RE (between BEGIN:VEVENT and END:VEVENT).
    # We'll append VALARM before the closing END:VEVENT which will be added later by the wrapper.
    # But because VEVENT_RE captures inner content without BEGIN/END, we return inner + VALARM.
    # Note: the outer assembly will place BEGIN:VEVENT + content + END:VEVENT.
    # Ensure there's exactly one trailing newline before VALARM for readability.
    content = block.rstrip() + "\n\n" + VALARM_BLOCK
    return content

def main():
    if not (2 <= len(sys.argv) <= 3):
        print("Usage: python3 fix_tesseract_ics.py input.ics [output.ics]", file=sys.stderr)
        sys.exit(2)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) == 3 else None

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split header (everything up to first BEGIN:VEVENT), then collect VEVENTs, then tail (after last END:VEVENT).
    first_event = re.search(r'BEGIN:VEVENT', text, re.I)
    if not first_event:
        print("No VEVENT blocks found in input.", file=sys.stderr)
        sys.exit(1)

    header = text[:first_event.start()]
    # Find all VEVENT blocks (including their inner content)
    vevent_matches = list(VEVENT_RE.finditer(text))
    vevents = []
    for m in vevent_matches:
        inner = m.group(1)  # content between BEGIN:VEVENT and END:VEVENT
        full_block = "BEGIN:VEVENT" + inner + "END:VEVENT"
        # For sorting, find DTSTART inside the inner content
        dt_match = DTSTART_RE.search(inner)
        if dt_match:
            dt_token = dt_match.group(2)
            dt_parsed = parse_dt(dt_token)
        else:
            dt_parsed = datetime(1970,1,1)
        # Ensure VALARM present in inner content (we will re-add BEGIN/END around it later)
        inner_with_alarm = ensure_valarm_in_vevent(inner)
        vevents.append((dt_parsed, inner_with_alarm))

    # Sort by datetime
    vevents.sort(key=lambda t: t[0])

    # Build output
    # Preserve the very last END:VCALENDAR if present in original; otherwise append it.
    tail_search = re.search(r'END:VCALENDAR\s*$', text, re.I)
    tail = "\nEND:VCALENDAR\n" if tail_search else "\nEND:VCALENDAR\n"

    out_lines = []
    out_lines.append(header.rstrip() + "\n")  # keep header formatting
    for dt_parsed, inner in vevents:
        out_lines.append("BEGIN:VEVENT")
        out_lines.append(inner.rstrip())
        out_lines.append("END:VEVENT\n")
    out_lines.append(tail)

    out_text = "\n".join(out_lines).replace("\r\n", "\n")

    if output_path:
        with open(output_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(out_text)
        print(f"Wrote fixed ICS with {len(vevents)} events to {output_path}")
    else:
        # print to stdout
        sys.stdout.write(out_text)

if __name__ == "__main__":
    main()