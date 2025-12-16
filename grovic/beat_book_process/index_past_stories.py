#!/usr/bin/env python3
"""
Build a Past Stories Index from a JSON summaries file.

Usage:
  python index_past_stories.py --input ../../data/story_summaries.json --output past_stories_index.md
"""
import argparse, json
from pathlib import Path
from typing import Any, Dict, List


def load(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def mk_line(item: Dict[str, Any]) -> str:
    title = (item.get("title") or item.get("headline") or "").strip()
    date = (item.get("date") or item.get("pub_date") or "").strip()
    summary = (item.get("summary") or item.get("dek") or "").strip()
    docref = (item.get("id") or item.get("docref") or "").strip()
    place = (item.get("place") or item.get("river") or item.get("county") or "").strip()
    parts = []
    if date:
        parts.append(date)
    if place:
        parts.append(place)
    meta = " | ".join(parts)
    meta = f" ({meta})" if meta else ""
    cite = f" (docref: {docref})" if docref else ""
    summary = summary[:180] + ("…" if len(summary) > 180 else "")
    return f"- {title}{meta}{cite} — {summary}".strip()


def main():
    ap = argparse.ArgumentParser(description="Generate past stories index from summaries JSON.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="past_stories_index.md")
    args = ap.parse_args()

    items = load(Path(args.input))
    lines = ["# Past Stories Index\n"]
    for it in items[:300]:
        lines.append(mk_line(it))
    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote index → {args.output} ({len(items)} items, truncated)")

if __name__ == "__main__":
    main()
