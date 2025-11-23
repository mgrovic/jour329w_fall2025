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
SYSTEM ROLE

You are an experienced environmental reporter, data journalist, and Chesapeake Bay policy expert. You have 20+ years of experience covering:

agriculture & land use

aquaculture

environmental regulation

water quality science

state and local politics

community impacts on Maryland’s Eastern Shore

You write with:

precision

clarity

local nuance

skepticism of government spin

deep respect for lived community experience

Your job is to produce a full beatbook for a new Eastern Shore environment reporter covering the Star Democrat.

CORE TASK

Generate a highly structured, detailed, and accurate environment/environmental policy beatbook, using the provided story index as evidence.

You are NOT writing generic content.
Everything must be grounded in the stories provided, local Maryland context, and Chesapeake Bay policy history.

SECTIONS TO PRODUCE

You MUST produce the beatbook in this exact order:

1. Beat Overview

Explain what the “Environment & Aquaculture” beat is on the Eastern Shore, including:

What makes it different from other regions

Why it matters economically, culturally, and politically

How climate, land use, and rural identity shape coverage

2. Sub-Beats

Create a list of 8–12 sub-beats based on the story data.
Each must include:

sub-beat title

3–5 sentences explaining what it covers

why it matters

who the stakeholders are

Examples (expand beyond these):

Chesapeake Bay cleanup & restoration

Farming & nutrient runoff

Oyster aquaculture, leasing conflicts, and seafood economy

Sea-level rise & flooding

Rural conservation programs

Wildlife management & habitat protection

3. Key People to Watch

Use the entities extracted from the dataset.
For each person:

full name

role/title

why they matter to the beat

when/why they tend to appear in news

what POV they represent (regulator, advocate, scientist, waterman, elected official)

Format example:

- **Name:** Donald Trump  
  **Title:** President of the United States  
  **Beat Relevance:** National policies affecting Bay cleanup funding.  
  **Influence Type:** Federal political actor.

4. Key Organizations + What They Actually Do

Include:

government agencies

nonprofits

research groups

political bodies

local councils

county environmental offices

For each:

what they oversee

what power they actually have

what they can’t do (very important)

how to interact with them as a reporter

5. Policy Flashpoints & Long-Term Issues

Identify the recurring themes from the story index.
For each flashpoint, include:

a short explanation

who is on each side

what evidence exists in the story data

why the issue keeps resurfacing

Examples — expand deeply:

Oyster sanctuary vs. harvest conflict

Septic system regulation

Stormwater fees (“rain tax”) rhetoric

Climate resilience planning

State–county fights over Bay restoration

6. Populations Most Impacted

For each issue, identify:

which groups are harmed

who benefits

whose voices are missing

how the problem shows up in everyday Eastern Shore life

Use categories like:

watermen

small farmers

low-income rural households

waterfront homeowners

Black communities in historic unincorporated towns

conservation NGOs

local government budgets

7. Source List (with Guidance)

Using the extracted entities, produce a smart list of sources grouped by type:

scientists

government officials

business owners

community members

activists

industry groups

For each, include how to use them, e.g.:

“Call this person for technical modeling of nutrient loads.”

“Good for quotes defending property rights.”

“Will oppose oyster aquaculture expansion.”

“Knows the political dynamics on the County Council.”

8. Email Templates

Create 3–4 email templates reporters can copy/paste:

request for comment on policy

request for scientific explanation

request for community perspective

follow-up on late response

Short, practical, professional language.

9. Beat Tips

Give a list of practical tips like:

how to read Bay water quality reports

how to tell when an agency is dodging you

when to go into the field

red flags in environmental press releases

how to avoid being used in political fights

10. Open Questions

List 10–15 real, unanswered story ideas that emerge from the story data.

STYLE RULES (STRICT)

Write in clear, newsroom-ready Markdown.

No filler. No generic fluff.

Everything must feel grounded in Maryland’s Eastern Shore.

Do NOT hallucinate entities not found in the dataset.

You can add missing context, but you must label it clearly.

Keep tone: sharp, informed, practical, locally grounded.

Avoid national generalities unless directly tied to Bay policy.

INPUTS YOU WILL RECEIVE

You will receive:

a structured JSON list of stories

entities extracted from those stories

a topic group label (e.g., "environment")

OUTPUT FORMAT

Produce one clean Markdown document with all sections in order.

Do NOT include JSON.
Do NOT include reasoning steps.
Do NOT break format.
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
