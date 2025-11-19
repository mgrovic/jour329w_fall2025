from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from glob import glob
from string import Template
from typing import Any, Dict, List, Tuple

DEFAULT_INPUT = "Aquaculture.json"
DEFAULT_OUTPUT = None  # auto-version if not provided

ALLOWED_IMPACT = {"Economy", "Culture", "Policy"}

PROMPT_TEMPLATE = """You extract structured entities (people, places, organizations) from LOCAL NEWS stories.

Return ONLY a JSON object with exactly these keys:
- docref: copy from input if present (else null)
- people: list of 1–6 most important people AS OBJECTS:
    - name: "First Last"
    - title: concise role/position if clearly stated; "" if unknown
- geographic_focus: list of distinct geographic or physical location names
- key_institutions: list of distinct organization / agency / government body names
- environmental_focus: list of distinct environmental themes explicitly mentioned in the text
  (e.g., "Water pollution", "Habitat loss", "Erosion", "Climate change", "Overfishing",
   "Wetland destruction", "Waste management", "Air pollution", "Other")
- impact: which population is most impacted (choose any of: Economy, Culture, Policy)

Rules:
- Use short, canonical person names (no honorifics in the name).
- Titles must be concise and factual; if not present in the text, use "".
- Do not include duplicates (dedupe by name, case-insensitive).
- Only entities/themes clearly mentioned; no guessing.
- If none found for a category, return [].
- Do not include the Star Democrat as an organization (exclude “Star Democrat” / “The Star Democrat”).

Example output:
{
  "docref": "ABC-123",
  "people": [
    {"name": "Ben Cardin", "title": "U.S. Senator"},
    {"name": "Tina Cardosi", "title": ""}
  ],
  "geographic_focus": ["Chesapeake Bay", "Talbot County"],
  "key_institutions": ["Maryland Department of Natural Resources", "EPA"],
  "environmental_focus": ["Water pollution", "Habitat loss"],
  "impact": ["Economy", "Policy"]
}

Story input:
docref: $docref
title: $title
byline: $byline
content: $content

Return ONLY the JSON object.
"""

def build_prompt(story: Dict[str, Any]) -> str:
    tmpl = Template(PROMPT_TEMPLATE)
    return tmpl.safe_substitute(
        docref=story.get("docref", story.get("id", "")) or "",
        title=(story.get("title") or "").strip(),
        byline=(story.get("byline") or story.get("author") or "").strip(),
        content=(story.get("content") or story.get("summary") or story.get("body") or "").strip(),
    )

def call_llm(prompt: str, model: str, use_uv: bool = False, timeout: int = 120) -> str:
    if not model:
        raise RuntimeError("Model is required (--model).")
    cmd = (["uv", "run", "llm"] if use_uv else ["llm"]) + ["-m", model]
    proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "llm call failed")
    return (proc.stdout or "").strip() or (proc.stderr or "").strip()

def extract_json_block(text: str) -> str | None:
    m = re.search(r"\{[\s\S]*\}", text)
    return m.group(0) if m else None

def _dedup_lower_preserve(items: List[str]) -> List[str]:
    out: List[str] = []
    seen = set()
    for s in items:
        k = s.lower()
        if k not in seen:
            seen.add(k)
            out.append(s)
    return out

def clean_list(values: Any) -> List[str]:
    out: List[str] = []
    if isinstance(values, list):
        for v in values:
            if isinstance(v, str):
                s = v.strip()
                if not s:
                    continue
                low = s.lower()
                if low in ("star democrat", "the star democrat"):
                    continue
                out.append(s)
    return _dedup_lower_preserve(out)

def clean_impact(values: Any) -> List[str]:
    # Normalize to allowed: Economy, Culture, Policy
    if isinstance(values, str):
        cand = [values]
    elif isinstance(values, list):
        cand = [v for v in values if isinstance(v, str)]
    else:
        cand = []
    out: List[str] = []
    seen = set()
    for v in cand:
        s = v.strip()
        if not s:
            continue
        match = next((opt for opt in ALLOWED_IMPACT if opt.lower() == s.lower()), None)
        if match and match not in seen:
            seen.add(match)
            out.append(match)
    return out

def _norm_person(name: str) -> str:
    # remove leading titles inside names if model put them there
    name = name.strip()
    name = re.sub(r"^(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|Sen\.|Rep\.|Gov\.|Mayor|Comptroller|Secretary)\s+", "", name, flags=re.I)
    return name.strip()

def clean_people(values: Any) -> List[Dict[str, str]]:
    """
    Normalize people to a list of objects [{name, title}], deduped by name, max 6.
    Accepts:
      - ["Full Name", "Full Name; Title", "Full Name - Title", ...]
      - [{"name": "...", "title": "..."}, {"person": "...", "role": "..."}, ...]
    """
    out: List[Dict[str, str]] = []
    seen = set()

    def split_inline(s: str) -> Tuple[str, str]:
        s = s.strip()
        for sep in [";", " — ", " – ", " - ", " | ", ", "]:
            if sep in s:
                a, b = s.split(sep, 1)
                return _norm_person(a), b.strip()
        return _norm_person(s), ""

    def pick(v: Any) -> Tuple[str, str]:
        if isinstance(v, str):
            return split_inline(v)
        if isinstance(v, dict):
            name = ""
            title = ""
            for k in ("name", "person", "full_name", "label"):
                val = v.get(k)
                if isinstance(val, str) and val.strip():
                    name = _norm_person(val)
                    break
            for k in ("title", "role", "position", "job", "office"):
                val = v.get(k)
                if isinstance(val, str) and val.strip():
                    title = val.strip()
                    break
            return name, title
        return "", ""

    if isinstance(values, list):
        for v in values:
            name, title = pick(v)
            if not name:
                continue
            low = name.lower()
            if low in ("star democrat", "the star democrat"):
                continue
            if low in seen:
                continue
            seen.add(low)
            out.append({"name": name, "title": title or ""})
            if len(out) >= 6:
                break

    return out

def _get_any(obj: Dict[str, Any], keys: List[str], default):
    for k in keys:
        if k in obj:
            return obj.get(k)
    lower_map = {str(k).lower(): k for k in obj.keys()}
    for k in keys:
        kk = lower_map.get(k.lower())
        if kk is not None:
            return obj.get(kk)
    return default

def coerce_entities(obj: Dict[str, Any]) -> Dict[str, Any]:
    # Tolerant key collection
    docref = _get_any(obj, ["docref", "id", "doc_ref"], None)
    ppl = _get_any(obj, ["people", "persons", "people_names"], [])
    places = _get_any(obj, ["geographic_focus", "places", "locations", "location"], [])
    orgs = _get_any(obj, ["key_institutions", "organizations", "orgs"], [])
    envs = _get_any(obj, ["environmental_focus", "environmental_issues", "environment"], [])
    impacts = _get_any(obj, ["impact", "impacts"], [])

    return {
        "docref": docref,
        "people": clean_people(ppl),
        "geographic_focus": clean_list(places),
        "key_institutions": clean_list(orgs),
        "environmental_focus": clean_list(envs),
        "impact": clean_impact(impacts),
    }

# Fallback name/title extraction from text if LLM omits people
# Pattern 1: "Name is/was <title>"
_IS_TITLE_RE = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+){0,2})\s+(?:is|was|serves as|served as)\s+([^.\n,]{3,100})",
    flags=re.I,
)

# Pattern 2: "<Title> Name" (e.g., "Comptroller Brooke Lierman")
_PRE_TITLE_RE = re.compile(
    r"\b((?:U\.S\.\s+)?(?:Sen\.|Senator|Rep\.|Representative|Del\.|Delegate|Gov\.|Governor|Mayor|Comptroller|Secretary|Director|Executive Director|President|Vice President|Chair|Chairman|CEO|CFO|COO|Founder|Owner|Professor|Associate Professor|Assistant Professor|Dean|Associate Dean|Manager|Commissioner|Council President|County Executive|Labor Secretary|Attorney General)[^,\n]{0,80})\s+([A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+){0,2})",
    flags=re.I,
)

# Pattern 3: "Name, <title>, ..." (comma title)
_POST_TITLE_RE = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+){1,2}),\s+([^,\n]{3,120})",
    flags=re.I,
)

_EXCLUDE_TOKENS = {
    # Institutions/places and common false positives
    "Star Democrat", "Maryland", "Chesapeake Bay", "City Council", "County Council",
    "United States", "Supreme Court", "EPA", "NOAA", "USDA", "DNR", "UMCES",
    # months, days
    "January","February","March","April","May","June","July","August","September","October",
    "November","December","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday",
    # misc
    "News Document", "APG National Enterprise Editor", "Staff Writer",
}

def _fallback_people_with_titles(text: str, byline: str = "") -> List[Dict[str, str]]:
    candidates: List[Tuple[str, str]] = []

    # Byline can contain author; we generally skip author as entity
    # but we also try to harvest any inline titles in body first.
    for m in _IS_TITLE_RE.finditer(text):
        name = _norm_person(m.group(1))
        title = m.group(2).strip()
        if len(name.split()) >= 2:
            candidates.append((name, title))

    for m in _PRE_TITLE_RE.finditer(text):
        title = m.group(1).strip()
        name = _norm_person(m.group(2))
        if len(name.split()) >= 2:
            candidates.append((name, title))

    for m in _POST_TITLE_RE.finditer(text):
        name = _norm_person(m.group(1))
        title = m.group(2).strip()
        # Avoid capturing trailing clauses that clearly aren't concise titles
        if len(name.split()) >= 2 and len(title.split()) <= 16:
            candidates.append((name, title))

    # Simple capitalized name fallback if still empty
    if not candidates:
        simple_name_re = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+){1,2})\b")
        for m in simple_name_re.finditer(text):
            name = m.group(1)
            if name in _EXCLUDE_TOKENS or " " not in name:
                continue
            candidates.append((name, ""))

    # Deduplicate, filter, cap to 6
    out: List[Dict[str, str]] = []
    seen = set()
    for name, title in candidates:
        if not name or name in _EXCLUDE_TOKENS:
            continue
        low = name.lower()
        if low in ("star democrat", "the star democrat"):
            continue
        if low in seen:
            continue
        seen.add(low)
        out.append({"name": name, "title": title})
        if len(out) >= 6:
            break
    return out

def process_story(story: Dict[str, Any], model: str, use_uv: bool) -> Dict[str, Any]:
    prompt = build_prompt(story)
    raw = ""
    for attempt in range(3):
        try:
            raw = call_llm(prompt, model, use_uv=use_uv, timeout=120)
            break
        except Exception:
            if attempt == 2:
                raw = ""
            else:
                time.sleep(2 + attempt * 2)

    base = {
        "docref": story.get("docref", story.get("id", None)),
        "people": [],
        "geographic_focus": [],
        "key_institutions": [],
        "environmental_focus": [],
        "impact": [],
    }

    # Build text blobs for fallback
    byline = (story.get("byline") or story.get("author") or "").strip()
    content_text = " ".join([
        (story.get("title") or ""),
        (story.get("content") or story.get("summary") or story.get("body") or ""),
    ])

    if not raw:
        ppl_fb = _fallback_people_with_titles(content_text, byline)
        return {**story, **base, "people": ppl_fb}

    block = extract_json_block(raw) or raw
    try:
        parsed = json.loads(block)
        ents = coerce_entities(parsed)
        # If LLM omitted people, try fallback extraction from story text
        if not ents.get("people"):
            ppl_fb = _fallback_people_with_titles(content_text, byline)
            ents["people"] = ppl_fb
        return {**story, **ents}
    except Exception:
        ppl_fb = _fallback_people_with_titles(content_text, byline)
        return {**story, **base, "people": ppl_fb}

def next_versioned_output(base: str = "stories_with_entities", ext: str = ".json", directory: str = ".") -> str:
    existing = sorted(glob(os.path.join(directory, f"{base}_v*.json")))
    if not existing:
        return os.path.join(directory, f"{base}_v1{ext}")
    max_v = 0
    for path in existing:
        m = re.search(r"_v(\d+)\.json$", os.path.basename(path))
        if m:
            max_v = max(max_v, int(m.group(1)))
    return os.path.join(directory, f"{base}_v{max_v + 1}{ext}")

def main():
    ap = argparse.ArgumentParser(description="Extract entities (people, geographic_focus, key_institutions, environmental_focus, impact) via llm CLI.")
    ap.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Input JSON list of stories.")
    ap.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Output JSON (auto-version if omitted).")
    ap.add_argument("--model", "-m", required=True, help="Model (required; no default).")
    ap.add_argument("--use-uv", action="store_true", help="Use `uv run llm` wrapper.")
    ap.add_argument("--sleep", type=float, default=0.4, help="Delay between calls.")
    ap.add_argument("--limit", type=int, default=0, help="Limit number of stories (0 = all).")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"Input not found: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        stories = json.load(f)
    if not isinstance(stories, list):
        raise SystemExit("Input JSON must be a list of story objects.")

    if args.limit > 0:
        stories = stories[:args.limit]
        print(f"Limiting to {len(stories)} stories")

    total = len(stories)
    print(f"Extracting entities for {total} stories using model: {args.model}")

    out: List[Dict[str, Any]] = []
    for idx, story in enumerate(stories, start=1):
        merged = process_story(story, args.model, args.use_uv)
        out.append(merged)
        title_preview = (story.get("title") or "").replace("\n", " ")[:80]
        ppl_count = len(merged.get("people", []))
        print(
            f"[{idx}/{total}] {title_preview} -> "
            f"P:{ppl_count} "
            f"G:{len(merged.get('geographic_focus', []))} "
            f"I:{len(merged.get('key_institutions', []))} "
            f"E:{len(merged.get('environmental_focus', []))} "
            f"Imp:{len(merged.get('impact', []))}"
        )
        time.sleep(args.sleep)

    output_path = args.output or next_versioned_output()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Saved entities to {output_path}")

if __name__ == "__main__":
    main()