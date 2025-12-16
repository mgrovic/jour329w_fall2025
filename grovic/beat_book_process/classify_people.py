#!/usr/bin/env python3
import argparse
import csv
import json
import random
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import llm

CATEGORIES = [
    "Government Officials",
    "Advocates",
    "Scientists/Academics",
    "Watermen/Farmers",
    "Media/Journalists",
    "Business/Industry",
    "Other",
]

SYSTEM_INSTRUCTIONS = """You are classifying people by their titles/roles into beat-relevant categories.

Categories:
- Government Officials (elected officials, appointed officials, agency staff, council/commissioners, state/federal/local)
- Advocates (nonprofits, environmental groups, riverkeepers, association leaders, activists)
- Scientists/Academics (researchers, professors, lab directors, institute staff)
- Watermen/Farmers (commercial fishermen, oyster growers, aquaculture operators, farmers)
- Media/Journalists (reporters, editors)
- Business/Industry (company executives, plant managers, developers)
- Other (if none fit)

Return ONLY the category string from the list above. Prefer the most specific category.
"""

def get_model(model_name: Optional[str]):
    if model_name:
        try:
            return llm.get_model(model_name)
        except Exception:
            for prefix in ("groq", "openai", "anthropic", "ollama"):
                try:
                    return llm.get_model(f"{prefix}/{model_name}")
                except Exception:
                    pass
            raise
    return llm.get_model()

def _resp_text(resp) -> str:
    if hasattr(resp, "text"):
        t = resp.text
        if callable(t):
            try:
                return t()
            except Exception:
                return ""
        return t
    return str(resp)

def read_people_csv(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if not path.exists():
        print(f"Warning: file not found: {path}", file=sys.stderr)
        return rows
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            name = (r.get("name") or "").strip()
            title = (r.get("title") or "").strip()
            if name and title:  # keep only with title
                rows.append({"name": name, "title": title})
    return rows

def dedupe(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    out = []
    for r in rows:
        key = (r["name"].lower(), r["title"].lower())
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out

# Quick heuristic to reduce LLM calls
def heuristic_category(title: str) -> Optional[str]:
    t = title.lower()
    gov_hits = ["council", "commissioner", "delegate", "senator", "mayor", "governor", "secretary", "department", "agency", "planner", "mde", "dnr", "army corps", "epa"]
    advocate_hits = ["riverkeeper", "shore rivers", "advocate", "activist", "association", "coalition", "nonprofit", "conservancy", "audubon", "chesapeake bay foundation"]
    sci_hits = ["professor", "research", "scientist", "lab", "institute", "university", "marine", "ecology"]
    water_hits = ["waterman", "oyster", "aquaculture", "grower", "farmer", "fishery", "harvester", "seafood", "boat captain"]
    media_hits = ["reporter", "journalist", "editor"]
    biz_hits = ["ceo", "manager", "director", "developer", "company", "llc", "inc", "operations", "plant"]

    if any(k in t for k in gov_hits):
        return "Government Officials"
    if any(k in t for k in advocate_hits):
        return "Advocates"
    if any(k in t for k in sci_hits):
        return "Scientists/Academics"
    if any(k in t for k in water_hits):
        return "Watermen/Farmers"
    if any(k in t for k in media_hits):
        return "Media/Journalists"
    if any(k in t for k in biz_hits):
        return "Business/Industry"
    return None

def load_cache(path: Path) -> Dict[str, str]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_cache(path: Path, cache: Dict[str, str]) -> None:
    try:
        path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"Warning: failed to write cache: {e}", file=sys.stderr)

def cache_key(name: str, title: str) -> str:
    return f"{name.strip().lower()}|||{title.strip().lower()}"

def classify_llm(model, name: str, title: str, max_retries: int = 5, base_delay: float = 1.0, jitter: float = 0.5) -> str:
    prompt = f"""{SYSTEM_INSTRUCTIONS}

Classify the person into ONE category from the list.

Name: {name}
Title: {title}

Return only the exact category string."""
    for attempt in range(1, max_retries + 1):
        try:
            resp = model.prompt(prompt)
            cat = _resp_text(resp).strip()
            if cat not in CATEGORIES:
                cat = "Other"
            return cat
        except Exception as e:
            if attempt == max_retries:
                print(f"LLM classify failed after {attempt} attempts for {name} – using 'Other'. Error: {e}", file=sys.stderr)
                return "Other"
            sleep_s = base_delay * (2 ** (attempt - 1)) + random.uniform(0, jitter)
            print(f"LLM error (attempt {attempt}): {e}. Retrying in {sleep_s:.1f}s...", file=sys.stderr)
            time.sleep(sleep_s)
    return "Other"

def write_csv(path: Path, rows: List[Dict[str, str]]):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "title", "category"])
        w.writeheader()
        w.writerows(rows)

def main():
    ap = argparse.ArgumentParser(description="Merge and classify people by category using Groq Maverick.")
    ap.add_argument("--csv-a", default="people12.csv", help="First people CSV with columns: name,title")
    ap.add_argument("--csv-b", default="people.csv", help="Second people CSV with columns: name,title")
    ap.add_argument("-m", "--model", default="groq/meta-llama/llama-4-maverick-17b-128e-instruct", help="LLM model id")
    ap.add_argument("-o", "--output", default="people_categorized.csv", help="Combined categorized CSV output")
    ap.add_argument("--per-category-dir", default="people_categories", help="Directory to write per-category CSVs")
    ap.add_argument("--dry-run", action="store_true", help="Show counts per category without writing files")
    ap.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between LLM calls (throttle)")
    ap.add_argument("--cache-file", default="people_classify_cache.json", help="Cache file to avoid re-classifying same entries")
    ap.add_argument("--max-retries", type=int, default=5, help="Max retries per LLM call")
    args = ap.parse_args()

    rows = read_people_csv(Path(args.csv_a)) + read_people_csv(Path(args.csv_b))
    rows = dedupe(rows)

    if not rows:
        print("No people with titles found.", file=sys.stderr)
        sys.exit(1)

    model = get_model(args.model)
    print(f"Using model: {getattr(model, 'model_id', args.model)}", file=sys.stderr)

    cache_path = Path(args.cache_file)
    cache = load_cache(cache_path)

    categorized: List[Dict[str, str]] = []
    counts = {c: 0 for c in CATEGORIES}

    for r in rows:
        print(r['name'])
        key = cache_key(r["name"], r["title"])
        if key in cache:
            cat = cache[key]
        else:
            cat = heuristic_category(r["title"]) or classify_llm(model, r["name"], r["title"], max_retries=args.max_retries)
            cache[key] = cat
            save_cache(cache_path, cache)
            if args.sleep > 0:
                time.sleep(args.sleep)
        r_out = {"name": r["name"], "title": r["title"], "category": cat}
        categorized.append(r_out)
        counts[cat] = counts.get(cat, 0) + 1

    # Report counts
    print("Counts by category:", file=sys.stderr)
    for c in CATEGORIES:
        print(f"- {c}: {counts.get(c, 0)}", file=sys.stderr)

    if args.dry_run:
        return

    # Write combined CSV
    write_csv(Path(args.output), categorized)

    # Write per-category CSVs
    out_dir = Path(args.per_category_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    by_cat: Dict[str, List[Dict[str, str]]] = {c: [] for c in CATEGORIES}
    for r in categorized:
        by_cat[r["category"]].append(r)

    for c, group in by_cat.items():
        safe = c.replace("/", "_").replace(" ", "_").lower()
        write_csv(out_dir / f"{safe}.csv", group)

    print(f"Wrote combined → {args.output}", file=sys.stderr)
    print(f"Wrote per-category CSVs → {out_dir}", file=sys.stderr)

if __name__ == "__main__":
    main()