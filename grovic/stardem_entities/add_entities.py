from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from typing import Any, Dict, List

DEFAULT_INPUT = "stardem_sample.json"
DEFAULT_OUTPUT = "stories_with_entities.json"
# Use one of the required Groq models from the assignment
DEFAULT_MODEL = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"

PROMPT_TEMPLATE = """You extract entities from local news stories.

Task: Return JSON with exactly these keys:
- docref: copy from input if available (string or number; else null)
- people: list of the most important peoples names (strings)
- places: list of place names (strings)
- organizations: list of org names  (strings)

Rules:
- Use short, canonical names (e.g., "Joe Biden", not "President Joe R. Biden").
- Do not include duplicates.
- Only include entities clearly mentioned.
- If none found for a category, return an empty list.
- Determine importance by how much of the story is focued on the person, or what role they play in the story. List from 1-6 people.
- Do not include the Star Democrat as an Organization

Example output:
{{
  "docref": "ABC-123",
  "people": ["Jane Doe", "John Smith"],
  "places": ["Easton", "Talbot County"],
  "organizations": ["Talbot County Council", "Capital News Service"]
}}

Input story:
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
    """
    Call the `llm` CLI with prompt on stdin.
    No temperature or max-tokens flags (per your preference).
    """
    cmd = (["uv", "run", "llm"] if use_uv else ["llm"]) + ["-m", model]
    proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "llm call failed")
    # some llm providers may print to stderr; prefer stdout, then stderr
    return (proc.stdout or "").strip() or (proc.stderr or "").strip()


def extract_json_block(text: str) -> str | None:
    # Try to extract a single JSON object from the response
    m = re.search(r"\{[\s\S]*\}", text)
    return m.group(0) if m else None


def coerce_entities(obj: Dict[str, Any]) -> Dict[str, Any]:
    def clean_list(values: Any) -> List[str]:
        out: List[str] = []
        seen = set()
        if isinstance(values, list):
            for v in values:
                if isinstance(v, str):
                    s = v.strip()
                    key = s.lower()
                    if s and key not in seen:
                        seen.add(key)
                        out.append(s)
        return out

    return {
        "docref": obj.get("docref", None),
        "people": clean_list(obj.get("people", [])),
        "places": clean_list(obj.get("places", [])),
        "organizations": clean_list(obj.get("organizations", [])),
    }


def process_story(story: Dict[str, Any], model: str, use_uv: bool) -> Dict[str, Any]:
    prompt = build_prompt(story)
    raw = ""
    for attempt in range(3):
        try:
            raw = call_llm(prompt, model, use_uv=use_uv, timeout=120)
            break
        except Exception as e:
            if attempt == 2:
                raw = ""
            else:
                time.sleep(2 + attempt * 2)

    base = {
        "docref": story.get("docref", story.get("id", None)),
        "people": [],
        "places": [],
        "organizations": [],
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


def main():
    ap = argparse.ArgumentParser(description="Extract entities (people, places, organizations) using the llm CLI (Groq).")
    ap.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Input JSON file (list of stories).")
    ap.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Output JSON file (default: stories_with_entities.json).")
    ap.add_argument("--model", "-m", default=DEFAULT_MODEL, help="Groq model for `llm` (see assignment for allowed models).")
    ap.add_argument("--use-uv", action="store_true", help="Use `uv run llm` wrapper.")
    ap.add_argument("--sleep", type=float, default=0.4, help="Seconds to sleep between calls.")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"Input not found: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        stories = json.load(f)

    if not isinstance(stories, list):
        raise SystemExit("Input JSON must be a list of story objects.")

    total = len(stories)
    print(f"Extracting entities for {total} stories using model: {args.model}")
    out: List[Dict[str, Any]] = []

    for i, story in enumerate(stories, start=1):
        merged = process_story(story, args.model, args.use_uv)
        out.append(merged)
        title_preview = (story.get("title") or "").replace("\n", " ")[:80]
        print(
            f"[{i}/{total}] {title_preview} -> "
            f"P:{len(merged.get('people', []))} "
            f"L:{len(merged.get('places', []))} "
            f"O:{len(merged.get('organizations', []))}"
        )
        time.sleep(args.sleep)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"Saved entities to {args.output}")


if __name__ == "__main__":
    main()