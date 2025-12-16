#!/usr/bin/env python3
import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import llm

# Heuristic location signals
MD_TERMS = {
    "maryland","md ","umces","university of maryland","umd","mde","dnr","d.nr", "d.n.r",
    "horn point","easton","talbot","st. michaels","oxford","trappe","dorchester","caroline",
    "kent county","queen anne","queen anne's","chesapeake","bay","eastern shore","shore rivers","shorerivers",
    "annapolis","baltimore","wye","choptank","tred avon","miles river","chester river","harris creek",
}
DE_TERMS = {
    "delaware","dnrec","de ","dover","sussex county","new castle","kent county de","lewes","rehoboth","bethany","delmarva",
}
VA_TERMS = {
    "virginia","va ","vims","vmrc","virginia marine resources commission","norfolk","hampton","newport news","richmond",
    "james river","york river","rappahannock","tangier","accomack","northampton va",
}
REGIONAL_TERMS = {
    "chesapeake bay","cbf","chesapeake bay foundation","bay program","watershed",
}

# Terms suggesting not a person
NON_PERSON_TERMS = {
    "foundation","college","creekwatchers","association","coalition","inc","llc","corp","company",
    "conditions","availability","population","committee","department","agency","institute",
}

# Basic “looks like a name” check
NAME_TOKEN_RE = re.compile(r"^[A-Z][a-z'\.-]*$")

def looks_like_person_name(name: str) -> bool:
    n = name.strip()
    if not n or len(n) > 80:
        return False
    if any(ch.isdigit() for ch in n):
        return False
    # Filter obvious org/phrases
    low = n.lower()
    if any(t in low for t in NON_PERSON_TERMS):
        return False
    # Accept common suffixes
    suffix_ok = {"jr.", "sr.", "iii", "ii"}
    parts = [p for p in re.split(r"\s+", n) if p]
    if len(parts) < 2 or len(parts) > 6:
        return False
    good = 0
    for p in parts:
        pl = p.lower()
        if pl in suffix_ok:
            good += 1
            continue
        # Allow initials like "J." or "A."
        if re.fullmatch(r"[A-Z]\.", p):
            good += 1
            continue
        if NAME_TOKEN_RE.match(p):
            good += 1
    return good >= max(2, len(parts) - 2)

def normalize(s: str) -> str:
    return (s or "").strip()

def is_relevant_heuristic(name: str, title: str) -> Optional[bool]:
    txt = f"{name} {title}".lower()
    # If any MD/DE/VA term present, relevant
    if any(t in txt for t in MD_TERMS | DE_TERMS | VA_TERMS | REGIONAL_TERMS):
        return True
    # If mentions generic US/Great Lakes without Chesapeake context, likely not
    if any(x in txt for x in ["great lakes","wisconsin","milwaukee","appalachian state","polish","copernicus"]):
        return False
    # Unsure
    return None

LLM_SYSTEM = """Decide if this person (name + title) is relevant to Maryland, Delaware, or Virginia environmental/aquaculture reporting.
Rules:
- Relevant if they work in/for MD/DE/VA agencies, universities, counties, towns, rivers, or Bay-wide regional orgs (e.g., Chesapeake Bay Foundation, Bay Program).
- Relevant if their title implies Eastern Shore/Chesapeake focus even without explicit state (e.g., Horn Point, UMCES, ShoreRivers).
- Not relevant if clearly tied to other regions with no Bay tie (e.g., Great Lakes, Wisconsin) unless Chesapeake is also mentioned.
Return exactly YES or NO."""

def get_model(model_name: Optional[str]):
    if model_name:
        try:
            return llm.get_model(model_name)
        except Exception:
            for p in ("groq","openai","anthropic","ollama"):
                try:
                    return llm.get_model(f"{p}/{model_name}")
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

def ask_llm_relevance(model, name: str, title: str, retries: int = 4, base_delay: float = 0.7) -> bool:
    prompt = f"""{LLM_SYSTEM}

Name: {name}
Title: {title}

Answer YES or NO."""
    for i in range(retries):
        try:
            resp = model.prompt(prompt)
            ans = _resp_text(resp).strip().upper()
            return ans.startswith("Y")
        except Exception as e:
            if i == retries - 1:
                print(f"LLM relevance failed for {name}: {e} (default NO)", file=sys.stderr)
                return False
            time.sleep(base_delay * (2 ** i))
    return False

def read_category_csv(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if not path.exists():
        return rows
    # Strip leading '//' comment lines before csv reader
    lines = path.read_text(encoding="utf-8").splitlines()
    clean = [ln for ln in lines if not ln.strip().startswith("//")]
    if not clean:
        return rows
    reader = csv.DictReader(clean)
    for r in reader:
        name = normalize(r.get("name"))
        title = normalize(r.get("title"))
        category = normalize(r.get("category"))
        if not name or not title:
            continue
        if not looks_like_person_name(name):
            continue
        rows.append({"name": name, "title": title, "category": category})
    return rows

def dedupe(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    out = []
    for r in rows:
        key = (r["name"].lower(), r["title"].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out

def main():
    ap = argparse.ArgumentParser(description="Combine people (excluding media_journalists) and keep only MD/DE/VA relevant.")
    ap.add_argument("--dir", default="people_categories", help="Directory containing category CSVs")
    ap.add_argument("-o", "--output", default="people_md_de_va.csv", help="Output CSV path")
    ap.add_argument("--exclude", default="media_journalists.csv", help="Filename to exclude")
    ap.add_argument("--use-llm", action="store_true", help="Use LLM to refine MD/DE/VA relevance when heuristic is unsure")
    ap.add_argument("-m", "--model", default="groq/meta-llama/llama-4-maverick-17b-128e-instruct", help="Model id for LLM relevance")
    ap.add_argument("--cache", default="relevance_cache.json", help="Cache file for LLM relevance decisions")
    ap.add_argument("--sleep", type=float, default=0.0, help="Sleep seconds between LLM calls")
    args = ap.parse_args()

    cat_dir = Path(args.dir)
    if not cat_dir.exists():
        print(f"Directory not found: {cat_dir}", file=sys.stderr)
        sys.exit(1)

    files = sorted([p for p in cat_dir.glob("*.csv") if p.name != args.exclude])
    if not files:
        print("No CSVs found.", file=sys.stderr)
        sys.exit(1)

    all_rows: List[Dict[str, str]] = []
    for f in files:
        all_rows.extend(read_category_csv(f))
    all_rows = dedupe(all_rows)

    # Load cache
    cache_path = Path(args.cache)
    cache: Dict[str, bool] = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    model = None
    if args.use_llm:
        model = get_model(args.model)
        print(f"Using model: {getattr(model, 'model_id', args.model)}", file=sys.stderr)

    kept: List[Dict[str, str]] = []
    for r in all_rows:
        name, title = r["name"], r["title"]
        h = is_relevant_heuristic(name, title)
        if h is True:
            kept.append(r)
            continue
        if h is False and not args.use_llm:
            continue
        key = f"{name}|||{title}"
        if args.use_llm:
            if key in cache:
                ok = bool(cache[key])
            else:
                ok = ask_llm_relevance(model, name, title)
                cache[key] = ok
                try:
                    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
                except Exception:
                    pass
            if args.sleep:
                time.sleep(args.sleep)
            if ok:
                kept.append(r)
        else:
            # Heuristic unsure and no LLM -> skip
            continue

    # Write output
    out_path = Path(args.output)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "title", "category"])
        w.writeheader()
        w.writerows(kept)

    print(f"Scanned files: {len(files)}", file=sys.stderr)
    print(f"Input rows (post-parse, deduped): {len(all_rows)}", file=sys.stderr)
    print(f"Kept MD/DE/VA relevant: {len(kept)}", file=sys.stderr)
    print(f"Wrote → {out_path}", file=sys.stderr)

if __name__ == "__main__":
    main()