#!/usr/bin/env python3
"""
Scaffold a reporter-friendly beat book Markdown with practical sections.
Optionally use a small JSON input of stories to suggest sub-beats and stakeholders.

Usage:
  python scaffold_beat_book.py --input sample_stories.json --output beatbook_scaffold.md
  python scaffold_beat_book.py --output beatbook_scaffold.md

Inputs: list of story dicts with keys like title, content/summary/body, people[{name,title}], tags.
Outputs: Markdown with core sections and TODO prompts.
"""
import argparse, json, sys
from pathlib import Path
from collections import Counter
from typing import Any, Dict, List

SECTION_ORDER = [
    "Beat Overview",
    "Sub-Beats",
    "People & Orgs to Watch",
    "Documents & Data",
    "Reporting Routines",
    "Tips",
    "Open Questions",
    "Future Stories",
    "Past Stories",
]

AQUA_KEYWORDS = [
    "aquaculture","oyster","oysters","lease","shellfish","waterman","harbor","mariculture"
]


def load_stories(path: Path) -> List[Dict[str, Any]]:
    if not path or not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def extract_people(stories: List[Dict[str, Any]]) -> List[str]:
    names: List[str] = []
    for s in stories:
        items = s.get("people") or []
        if isinstance(items, list):
            for p in items:
                if isinstance(p, dict):
                    n = (p.get("name") or "").strip()
                    if n:
                        names.append(n)
                elif isinstance(p, str) and p.strip():
                    names.append(p.strip())
    out, seen = [], set()
    for n in names:
        k = n.lower()
        if k not in seen:
            seen.add(k)
            out.append(n)
    return out


def extract_places_tags(stories: List[Dict[str, Any]]) -> List[str]:
    vals: List[str] = []
    for s in stories:
        tags = s.get("tags")
        if isinstance(tags, list):
            for t in tags:
                if isinstance(t, str) and t.strip():
                    vals.append(t.strip())
        for k in ("title","content","summary","body","deck","subtitle"):
            v = s.get(k)
            if isinstance(v, str):
                text = v.lower()
                if any(kw in text for kw in AQUA_KEYWORDS):
                    vals.append("aquaculture")
    # simple dedupe
    out, seen = [], set()
    for v in vals:
        k = v.lower()
        if k not in seen:
            seen.add(k)
            out.append(v)
    return out


def suggest_subbeats(stories: List[Dict[str, Any]]) -> List[str]:
    # naive frequency from tags/keywords
    tags = extract_places_tags(stories)
    counts = Counter(t.lower() for t in tags)
    base = [
        "Aquaculture leasing conflicts",
        "Septic systems & stormwater",
        "Bay cleanup funding & enforcement",
        "Rural land use & development",
        "Flooding & climate resilience",
    ]
    extras = [t.title() for t, c in counts.most_common() if c >= 2 and t not in {"aquaculture"}]
    return (base + extras)[:12]


def scaffold_md(stories: List[Dict[str, Any]]) -> str:
    people = extract_people(stories)[:20]
    subbeats = suggest_subbeats(stories)
    lines: List[str] = []

    lines.append("# Beat Book (Scaffold)\n")
    lines.append("## Beat Overview\n")
    lines.append("Describe the beat in plain language. Where it happens (rivers/towns/counties), why it matters locally, and how geography/jurisdiction shapes coverage.\n")

    lines.append("\n## Sub-Beats\n")
    if subbeats:
        for sb in subbeats:
            lines.append(f"- {sb}: why here, who’s involved, key places, recent examples.")
    else:
        lines.append("- List 8–12 sub‑beats with places, stakeholders, and examples.")

    lines.append("\n## People & Orgs to Watch\n")
    if people:
        for n in people:
            lines.append(f"- {n} — role, influence, geography, when to call, contact notes.")
    else:
        lines.append("- Add 15–25 recurring names/orgs with notes on power and geography.")

    lines.append("\n## Documents & Data\n")
    lines.append("- Aquaculture leases; water quality reports; county planning; enforcement actions — where to get, how to read, red flags, local examples.\n")

    lines.append("\n## Reporting Routines\n")
    lines.append("- Checklists for council agendas, permitting, field visits; who to call first/second; verification steps.\n")

    lines.append("\n## Tips\n")
    lines.append("- How to avoid spin; read water quality; spot jurisdiction overreach; when to go into the field.\n")

    lines.append("\n## Open Questions\n")
    lines.append("- 10–15 real story ideas tied to specific places, with a first document/source to pull.\n")

    lines.append("\n## Future Stories\n")
    lines.append("- Pitch queue, calendar/triggers, pre‑reporting checklist, risk/verification notes.\n")

    lines.append("\n## Past Stories\n")
    lines.append("- Coverage index, stakeholder follow‑ups, lessons learned, open threads.\n")

    return "\n".join(lines).strip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Generate a practical beat book scaffold.")
    ap.add_argument("--input", help="Optional JSON list of stories")
    ap.add_argument("--output", default="beatbook_scaffold.md", help="Output Markdown path")
    args = ap.parse_args()

    stories: List[Dict[str, Any]] = []
    if args.input:
        stories = load_stories(Path(args.input))
    out = scaffold_md(stories)
    Path(args.output).write_text(out, encoding="utf-8")
    print(f"Wrote scaffold → {args.output}")

if __name__ == "__main__":
    main()
