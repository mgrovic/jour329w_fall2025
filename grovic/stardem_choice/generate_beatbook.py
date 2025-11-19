from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
from collections import Counter
from typing import Any, Dict, List


DEFAULT_INPUTS = [
    "stories_with_entities_v11.json",
    "stories_with_entities_v12.json",
]
DEFAULT_OUTPUT = "beatbook_star_dem_environment.md"
DEFAULT_MODEL = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"

AQUA_KEYWORDS = [
    "aquaculture","mariculture","oyster","oysters","clam","clams","mussel","mussels",
    "shellfish","hatchery","fish farm","fish farming","aquafarm","seaweed","kelp",
    "lease","aquaculture lease","aquaculture permit","aquaculture operation","aquaculture facility",
]

def load_json(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected list in {path}")
    return data

def _people_names_from_story(s: Dict[str, Any]) -> List[str]:
    """
    Normalize story['people'] which may be:
      - list[str] of names, or
      - list[dict{name, title?...}]
    Returns a de-duplicated list of names (case-insensitive, order-preserving).
    """
    items = s.get("people") or s.get("metadata_people") or []
    names: List[str] = []
    if isinstance(items, list):
        for p in items:
            if isinstance(p, dict):
                n = p.get("name")
                if isinstance(n, str) and n.strip():
                    names.append(n.strip())
            elif isinstance(p, str) and p.strip():
                names.append(p.strip())
    seen = set()
    out: List[str] = []
    for n in names:
        k = n.lower()
        if k not in seen:
            seen.add(k)
            out.append(n)
    return out

def _str_list(values: Any) -> List[str]:
    out: List[str] = []
    if isinstance(values, list):
        for v in values:
            if isinstance(v, str) and v.strip():
                out.append(v.strip())
    return out

def aggregate_entities(stories: List[Dict[str, Any]], top_n: int = 25) -> Dict[str, List[str]]:
    people = Counter()
    places = Counter()
    orgs = Counter()
    env_focus = Counter()
    impacts = Counter()

    for s in stories:
        for name in _people_names_from_story(s):
            people[name] += 1
        for g in _str_list(s.get("geographic_focus") or s.get("places") or s.get("metadata_geographic_focus") or []):
            places[g] += 1
        for o in _str_list(s.get("key_institutions") or s.get("organizations") or s.get("metadata_key_institutions") or []):
            orgs[o] += 1
        for e in _str_list(s.get("environmental_focus") or s.get("environmental_issues") or []):
            env_focus[e] += 1
        for im in _str_list(s.get("impact") or s.get("impacts") or []):
            impacts[im] += 1

    return {
        "top_people": [name for name, _ in people.most_common(top_n)],
        "top_places": [name for name, _ in places.most_common(top_n)],
        "top_organizations": [name for name, _ in orgs.most_common(top_n)],
        "top_env_focus": [name for name, _ in env_focus.most_common(top_n)],
        "top_impacts": [name for name, _ in impacts.most_common(top_n)],
    }

def story_line(s: Dict[str, Any]) -> str:
    title = (s.get("title") or "").replace("\n", " ").strip()
    docref = s.get("docref") or s.get("id") or ""
    people = ", ".join(_people_names_from_story(s)[:3])
    orgs = ", ".join((_str_list(s.get("key_institutions") or s.get("organizations")) or [])[:3])
    places = ", ".join((_str_list(s.get("geographic_focus") or s.get("places")) or [])[:3])
    envs = ", ".join((_str_list(s.get("environmental_focus")) or [])[:3])
    return f"- {title} (docref: {docref}) | People: {people} | Orgs: {orgs} | Places: {places} | Env: {envs}"

def build_story_index(stories: List[Dict[str, Any]], max_lines: int = 80) -> str:
    lines = [story_line(s) for s in stories[:max_lines]]
    return "\n".join(lines)

def relates_to_aquaculture(story: Dict[str, Any]) -> bool:
    parts: List[str] = []
    for k in ("title", "content", "summary", "body", "deck", "subtitle"):
        v = story.get(k)
        if isinstance(v, str):
            parts.append(v)
    tags = story.get("tags")
    if isinstance(tags, list):
        parts += [t for t in tags if isinstance(t, str)]
    text = " ".join(parts).lower()
    return any(kw in text for kw in AQUA_KEYWORDS)

def build_prompt(
    entities: Dict[str, List[str]],
    story_index: str,
    aquaculture_index: str,
) -> str:
    # In-depth onboarding + execution guide, with strong structural constraints.
    return f"""
You are creating an in-depth onboarding beat book for a brand-new reporter at the Easton Star Democrat (Maryland).
Beat: covering the environment on the Eastern Shore, with a dedicated Aquaculture focus. Write a single cohesive Markdown document.

Audience: a new reporter who knows journalism basics but needs concrete, local guidance. Use short, direct sentences. Neutral, official tone. Avoid flowery language. Prefer specifics to generalities. Include brief checklists where helpful.

MANDATORY sections and constraints (do not skip any):
## 1) Purpose and Local Context
- Explain why environment coverage matters for the Star Democrat and the Eastern Shore economy and communities.
- Summarize what recent coverage suggests about priorities on this beat.
- Cite examples with [Story Title] (docref: ABC-123).

## 2) Background Briefing (Core Issues)
- Water quality, development/land use, fisheries, climate impacts, habitat restoration, pollution control.
- Explain how these appear in Star Democrat stories. Include 5–8 inline citations to the story index.
- Note unresolved items (lawsuits, policy debates). Add caveats that status may have changed.

## 3) Aquaculture Deep Dive
- What aquaculture looks like here (oyster, clam, mussel, seaweed; hatcheries; leases).
- Regulatory map: Maryland Department of Natural Resources (leasing and fisheries), Maryland Department of the Environment (permits/discharges), U.S. Army Corps (permits), local planning/zoning boards, NOAA (science/policy context). Keep concise and factual.
- Common friction points: siting, navigation, habitat, water quality, working waterfront conflicts.
- What to watch next: trends, technology, financing, legal challenges. Cite specific stories and docrefs from the aquaculture subset.
- Provide a 6–10 point checklist for covering a new aquaculture proposal.

## 4) Source Profiles (people)
- Profile 6–10 key people. For each: who they are, why they matter, what they can reliably speak to, best way to approach.
- Mix local watermen/farmers, county/state officials, scientists, advocates, and industry reps.
- Use names consistently with the entity lists. Include brief, practical notes.

## 5) Organization Overviews (institutions)
- Summarize 8–12 agencies/groups (e.g., DNR, MDE, EPA, ShoreRivers, CBF, UMCES, county councils/boards, planning/zoning).
- What they do, why they matter, how to find documents/data, how to get comment, typical turnaround times.

## 6) Documents, Data, and Tools
- What to pull for environment and aquaculture stories: permits, leases, inspection records, enforcement actions, environmental impact reviews, meeting packets, grant notices.
- Data sources: Bay water quality datasets, SAV mapping, NOAA/USGS datasets, county open data, agricultural stats.
- Include a short FOIA/PRA playbook (what to request, sample language, expected timelines, appeal pointers).
- List 5–8 specific datasets and how they’re used in typical stories.

## 7) Story Opportunities (with integrated reporting tips)
- Provide 12–16 concrete story ideas centered on Easton/Eastern Shore. Split across short-turn, enterprise, and accountability angles.
- For each idea: aim, what to obtain (docs/data/sources/locations), who to call first, verification steps, common pitfalls.
- Avoid rehashing already-heavy coverage; point to under-covered angles. Weigh recent coverage more.

## 8) Field Reporting and Safety
- Where to go (piers, shorelines, farms, meetings), what to bring, weather/tide checks, access etiquette on working waterfronts.
- Short checklist for field days.

## 9) Beat Cadence and Calendar
- What recurs on this beat (meetings, seasons: planting/harvest, crab/oyster cycles, legislative sessions, budget timelines).
- A monthly cadence plan for a new reporter.

## 10) Ethics, Legal, and Accuracy Checks
- Conflict-of-interest cautions, scientific uncertainty, legal sensitivities (ongoing litigation, contested permits).
- How to write caveats on unresolved matters.

## 11) Contact List
- Group contacts (people and orgs). Provide titles/roles where clear from coverage. Keep it concise and useful.

## 12) Citations and Further Reading
- Provide a compact list of cited stories in the document with their docrefs.

STYLE AND LENGTH:
- Aim for 2,000–2,800 words. Use H2/H3/H4 headings. Use bullet lists sparingly for checklists and steps.
- Use exact names for people, places, and organizations. Be concrete.

GROUND TRUTH (use to guide names and emphasis):
- Top people: {entities['top_people']}
- Top places: {entities['top_places']}
- Top organizations: {entities['top_organizations']}
- Top environmental focuses: {entities['top_env_focus']}
- Top impact categories: {entities['top_impacts']}

ATTACHED STORY INDEX (sample lines with docrefs):
{story_index}

AQUACULTURE SUBSET (sample lines with docrefs):
{aquaculture_index}
""".strip()

def call_llm(prompt: str, model: str, use_uv: bool = False, timeout: int = 240) -> str:
    cmd = ["llm", "-m", model, prompt]
    if use_uv:
        cmd = ["uv", "run"] + cmd

    print(f"Running LLM: {' '.join(shlex.quote(c) for c in cmd)}")
    res = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
        timeout=timeout,
    )
    return res.stdout.strip()

def main():
    ap = argparse.ArgumentParser(description="Generate a Star Democrat environment beat book (with Aquaculture deep dive).")
    ap.add_argument("--inputs", nargs="+", default=DEFAULT_INPUTS, help="Paths to entity-enriched JSON files")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="Output Markdown file")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Groq model for llm CLI")
    ap.add_argument("--use-uv", action="store_true", help="Call llm via `uv run`")
    ap.add_argument("--index-lines", type=int, default=80, help="Max story lines to include in attached index")
    ap.add_argument("--aqua-lines", type=int, default=40, help="Max aquaculture lines to include")
    args = ap.parse_args()

    # Load and merge stories
    stories: List[Dict[str, Any]] = []
    for path in args.inputs:
        print(f"Loading: {path}")
        stories.extend(load_json(path))
    if not stories:
        print("No stories loaded; aborting.", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(stories)} stories total.")

    # Aggregate
    entities = aggregate_entities(stories, top_n=25)
    print("Aggregated top entities:")
    print(f"- People: {len(entities['top_people'])}")
    print(f"- Places: {len(entities['top_places'])}")
    print(f"- Orgs: {len(entities['top_organizations'])}")
    print(f"- Env focus: {len(entities['top_env_focus'])}")
    print(f"- Impacts: {len(entities['top_impacts'])}")

    # Build indices
    story_index = build_story_index(stories, max_lines=args.index_lines)
    aqua_stories = [s for s in stories if relates_to_aquaculture(s)]
    aquaculture_index = build_story_index(aqua_stories, max_lines=args.aqua_lines)
    print(f"Built story index ({min(len(stories), args.index_lines)} lines) and aquaculture index ({min(len(aqua_stories), args.aqua_lines)} lines).")

    # Build prompt
    prompt = build_prompt(entities, story_index, aquaculture_index)
    print(f"Prompt length: {len(prompt):,} chars")

    # Call LLM
    started = time.time()
    try:
        output_md = call_llm(prompt, model=args.model, use_uv=args.use_uv, timeout=360)
    except subprocess.CalledProcessError as e:
        print("LLM error:", e.stderr, file=sys.stderr)
        sys.exit(2)
    finally:
        print(f"LLM call took {time.time() - started:.1f}s")

    # Save
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_md)
    print(f"Wrote beat book to {args.output}")

if __name__ == "__main__":
    main()