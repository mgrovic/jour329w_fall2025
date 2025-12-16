#!/usr/bin/env python3
"""
Create a Future Stories Queue with structured entries.

Usage:
  python create_future_stories.py --output future_stories_queue.md --seed "Miles River lease expansion debate"
"""
import argparse
from pathlib import Path

TEMPLATE = """# Future Stories Queue

## Pitch: {title}
- Why now: {why_now}
- Place: {place}
- First calls: {first_calls}
- First documents: {first_docs}
- Risks & verification: {risks}

---
(Add more pitches following the same structure.)
"""


def main():
    ap = argparse.ArgumentParser(description="Write a structured future stories queue.")
    ap.add_argument("--output", default="future_stories_queue.md")
    ap.add_argument("--seed", default="")
    args = ap.parse_args()

    content = TEMPLATE.format(
        title=args.seed or "<Title>",
        why_now="<Trigger/meeting/date>",
        place="<River/Town/County>",
        first_calls="<List of names/roles>",
        first_docs="<Lease/agenda/report>",
        risks="<What could be wrong/missing and how to check>",
    )
    Path(args.output).write_text(content, encoding="utf-8")
    print(f"Wrote queue → {args.output}")

if __name__ == "__main__":
    main()
