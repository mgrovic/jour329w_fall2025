#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import csv

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_people.py INPUT.json OUTPUT.csv", file=sys.stderr)
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not in_path.exists():
        print(f"Input not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(in_path.read_text(encoding="utf-8"))

    rows = []
    for item in data:
        people = item.get("people", [])
        for p in people:
            name = p.get("name", "").strip()
            title = p.get("title", "").strip()
            if name:
                rows.append({"name": name, "title": title})

    # de-duplicate
    unique = {}
    for r in rows:
        key = (r["name"], r["title"])
        if key not in unique:
            unique[key] = r
    rows = list(unique.values())

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "title"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows → {out_path}")

if __name__ == "__main__":
    main()