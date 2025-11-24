#!/usr/bin/env python3
"""
Convert the commute_podcasts_curated.csv (the CSV I provided) into a Google Calendar CSV.

Usage:
  python3 convert_to_google_csv.py commute_podcasts_curated.csv google_import.csv

This writes:
  google_import.csv with columns: Subject, Start Date, Start Time, End Date, End Time, All Day Event, Description, Location, Private
"""
import csv
import sys
from datetime import datetime

if len(sys.argv) != 3:
    print("Usage: python3 convert_to_google_csv.py input.csv output.csv")
    sys.exit(1)

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, newline='', encoding='utf-8') as fin, open(outfile, 'w', newline='', encoding='utf-8') as fout:
    reader = csv.DictReader(fin)
    fieldnames = ["Subject","Start Date","Start Time","End Date","End Time","All Day Event","Description","Location","Private"]
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    for r in reader:
        date = r.get("Date", "")
        start = r.get("StartTime", "")
        end = r.get("EndTime", "")
        # Compose a helpful description
        desc_parts = []
        if r.get("SourceSummary"):
            desc_parts.append("Topic: " + r["SourceSummary"])
        if r.get("SourceDescription"):
            desc_parts.append(r["SourceDescription"])
        if r.get("SuggestedEpisode"):
            desc_parts.append("Suggested: " + r["SuggestedEpisode"])
        if r.get("SpotifySearchURL"):
            desc_parts.append("Spotify: " + r["SpotifySearchURL"])
        description = "\n\n".join(desc_parts)
        row = {
            "Subject": r.get("Title","Podcast"),
            "Start Date": date,
            "Start Time": start,
            "End Date": date,
            "End Time": end,
            "All Day Event": "False",
            "Description": description,
            "Location": "",
            "Private": "False"
        }
        writer.writerow(row)
print("Wrote", outfile)