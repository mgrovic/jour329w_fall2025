from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from glob import glob
from typing import Any, Dict, List

DEFAULT_INPUT = "topic_stories.json"
DEFAULT_OUTPUT = None  # auto-version if not provided

ALLOWED_IMPACT = {"Economy", "Culture", "Policy"}

PROMPT_TEMPLATE = """You extract structured entities (people, places, organizations) from LOCAL NEWS stories
all centered on the same topic/beat. Focus on entities that matter for a beat book
(long-term coverage). Prefer government officials, recurring stakeholders, key locations,
formal organization names. Skip generic roles unless uniquely identifying (e.g. "Maryland
Department of Natural Resources"). Exclude pure descriptors (e.g., "the agency", "officials").

Return ONLY a single JSON object with keys:
- docref: copy from input if present (else null)
- people: list of the most important people's names (strings)
- geographic_focus: list of place names (strings)
- key_institutions: list of org names (strings)
- environmental_focus: list of environmental themes (strings)
- impact: which population is most impacted

Rules:
- Use short, canonical names (e.g., "Joe Biden", not "President Joe R. Biden").
- Do not include duplicates.
- Only include entities clearly mentioned.
- If none found for a category, return an empty list.
- Determine importance by how much of the story is focused on the person, or what role they play in the story. List from 1–6 people.
- Do not include the Star Democrat as an organization (exclude “Star Democrat” / “The Star Democrat”).

Example:
Input snippet:
"Talbot County Council President Chuck Callahan said the Chesapeake Bay cleanup
plan needs broader support from the Maryland Department of Natural Resources."

Example output:
{{
  "people": ["Donald Trump", "Ben Cardin", "Tina Cardosi", "Andrew Barnet"],
  "geographic_focus": ["Annapolis", "Gunpowder Falls"],
  "key_institutions": ["EPA", "NOAA"],
  "environmental_focus": [
    "Water pollution",
    "Air pollution",
    "Habitat loss",
    "Erosion",
    "Climate change",
    "Waste management",
    "Deforestation",
    "Overfishing",
    "Wetland destruction",
    "Other"
  ],
  "impact": ["Economy", "Culture", "Policy"]
}}

Story input:
docref: {docref}
title: {title}
byline: {byline}
content: {content}

Return ONLY the JSON object.
"""

def build_prompt(story: Dict[str, Any]) -> str:
    return PROMPT_TEMPLATE.format(
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

def clean_list(values: Any) -> List[str]:
    out: List[str] = []
    seen = set()
    if isinstance(values, list):
        for v in values:
            if isinstance(v, str):
                s = v.strip()
                if not s:
                    continue
                low = s.lower()
                if low in ("star democrat", "the star democrat"):
                    continue
                if low not in seen:
                    seen.add(low)
                    out.append(s)
    return out

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

def coerce_entities(obj: Dict[str, Any]) -> Dict[str, Any]:
    # Map common alternative keys
    if "places" in obj and "geographic_focus" not in obj:
        obj["geographic_focus"] = obj.get("places", [])
    if "organizations" in obj and "key_institutions" not in obj:
        obj["key_institutions"] = obj.get("organizations", [])
    if "impacts" in obj and "impact" not in obj:
        obj["impact"] = obj.get("impacts", [])

    return {
        "docref": obj.get("docref", None),
        "people": clean_list(obj.get("people", []))[:6],
        "geographic_focus": clean_list(obj.get("geographic_focus", [])),
        "key_institutions": clean_list(obj.get("key_institutions", [])),
        "environmental_focus": clean_list(obj.get("environmental_focus", [])),
        "impact": clean_impact(obj.get("impact", [])),
    }

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
    if not raw:
        return {**story, **base}

    block = extract_json_block(raw) or raw
    try:
        parsed = json.loads(block)
        ents = coerce_entities(parsed)
        return {**story, **ents}
    except Exception:
        return {**story, **base}

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
        raise SystemExit("Input JSON must be a list.")

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
        print(
            f"[{idx}/{total}] {title_preview} -> "
            f"P:{len(merged.get('people', []))} "
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