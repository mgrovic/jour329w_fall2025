#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import requests
except Exception:
    requests = None

DEFAULT_MODEL = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"

PROMPT_TEMPLATE = (
    "You are assisting a journalist covering Maryland's Eastern Shore.\n"
    "From the provided beatbook briefing (Markdown), identify the 50 most relevant PEOPLE for reporting on environment and aquaculture.\n"
    "For each person, return: name, role/title, organization, primary location(s) (city/county/river/region), and 1-sentence relevance.\n"
    "Then sort them by location (group by county/city/river first), and within each location, sort by what they do (role/title).\n"
    "Only include real individuals (exclude organizations or places).\n"
    "Prefer Eastern Shore counties and rivers (Talbot, Dorchester, Caroline, Kent, Queen Anne's; Choptank, Tred Avon, Nanticoke, Wye, Eastern Bay).\n"
    "Return strict JSON with schema: {\"groups\": [{\"location\": string, \"people\": [{\"name\": string, \"role\": string, \"organization\": string, \"relevance\": string}]}]}\n"
)


def call_groq_llm(text: str, model: str) -> Optional[Dict[str, Any]]:
    if requests is None:
        return None
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = [
        {"role": "system", "content": "You are a precise, structured assistant returning strict JSON."},
        {"role": "user", "content": PROMPT_TEMPLATE + "\n\nBEATBOOK:\n" + text[:24000]},
    ]
    payload = {"model": model, "messages": messages, "temperature": 0.2, "max_tokens": 4000}
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        return None
    data = resp.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    # Try to parse JSON
    try:
        return json.loads(content)
    except Exception:
        # Attempt to extract JSON block
        import re
        m = re.search(r"\{[\s\S]*\}", content)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
        return None


def write_outputs(groups: List[Dict[str, Any]], out_md: Path, out_csv: Path):
    # Markdown
    out_md.parent.mkdir(parents=True, exist_ok=True)
    with out_md.open("w", encoding="utf-8") as f:
        f.write("# Top 50 People by Location (Eastern Shore)\n\n")
        for g in groups:
            loc = g.get("location") or "Unspecified"
            f.write(f"## {loc}\n")
            people = g.get("people") or []
            for p in people:
                name = p.get("name", "")
                role = p.get("role", "")
                org = p.get("organization", "")
                rel = p.get("relevance", "")
                f.write(f"- **{name}** — {role}; {org}. {rel}\n")
            f.write("\n")
    # CSV
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8") as f:
        f.write("location,name,role,organization,relevance\n")
        for g in groups:
            loc = g.get("location") or "Unspecified"
            for p in (g.get("people") or []):
                name = (p.get("name") or "").replace(",", " ")
                role = (p.get("role") or "").replace(",", " ")
                org = (p.get("organization") or "").replace(",", " ")
                rel = (p.get("relevance") or "").replace(",", " ")
                f.write(f"{loc},{name},{role},{org},{rel}\n")


def main():
    parser = argparse.ArgumentParser(description="Select top 50 relevant people from beatbook and group by location, then role.")
    parser.add_argument("--beatbook", type=Path, default=Path("grovic/stardem_nearly_final/beatbook_cleaned_redacted.md"))
    parser.add_argument("--out_md", type=Path, default=Path("grovic/stardem_nearly_final/top_people_by_location.md"))
    parser.add_argument("--out_csv", type=Path, default=Path("data/top_people_by_location.csv"))
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    args = parser.parse_args()

    if not args.beatbook.exists():
        raise FileNotFoundError(f"Beatbook not found: {args.beatbook}")
    text = args.beatbook.read_text(encoding="utf-8")

    result = call_groq_llm(text, args.model)
    groups: List[Dict[str, Any]] = []
    if result and isinstance(result, dict) and "groups" in result:
        groups = result.get("groups") or []
    else:
        # Fallback: derive from CSV `people_md_de_va.csv` if present
        csv_path = Path("grovic/stardem_nearly_final/people_md_de_va.csv")
        entries: List[Dict[str, Any]] = []
        if csv_path.exists():
            import csv
            with csv_path.open("r", encoding="utf-8") as cf:
                reader = csv.DictReader(cf)
                for row in reader:
                    name = (row.get("name") or row.get("Name") or "").strip()
                    if not name:
                        continue
                    role = (row.get("position") or row.get("role") or row.get("title") or "").strip()
                    org = (row.get("organization") or row.get("org") or "").strip()
                    # pick a location column if available
                    location = (
                        row.get("county") or row.get("County") or row.get("city") or row.get("City") or
                        row.get("river") or row.get("River") or row.get("location") or row.get("Location") or "Eastern Shore (General)"
                    ).strip()
                    relevance = "Relevant to Eastern Shore environment/aquaculture coverage."
                    entries.append({"location": location, "name": name, "role": role, "organization": org, "relevance": relevance})
        # Group by location and sort by role, limit to 50
        from collections import defaultdict
        grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for e in entries:
            grouped[e["location"]].append(e)
        # Sort locations by known priority ordering
        priority = ["Talbot County", "Dorchester County", "Caroline County", "Kent County", "Queen Anne's County",
                    "Choptank River", "Tred Avon River", "Nanticoke River", "Wye River", "Eastern Bay"]
        def loc_sort_key(loc: str):
            try:
                return priority.index(loc)
            except ValueError:
                return len(priority)
        sorted_locs = sorted(grouped.keys(), key=loc_sort_key)
        total = 0
        out_groups: List[Dict[str, Any]] = []
        for loc in sorted_locs:
            people = sorted(grouped[loc], key=lambda x: (x["role"] or ""))
            keep = []
            for p in people:
                if total >= 50:
                    break
                keep.append({"name": p["name"], "role": p["role"], "organization": p["organization"], "relevance": p["relevance"]})
                total += 1
            if keep:
                out_groups.append({"location": loc, "people": keep})
            if total >= 50:
                break
        groups = out_groups

    # Sanity trim to 50 total
    total = 0
    trimmed_groups = []
    for g in groups:
        people = g.get("people") or []
        keep = []
        for p in people:
            if total >= 50:
                break
            # Drop obvious non-persons
            name = p.get("name") or ""
            if not name or name.lower().startswith(("in ", "into ", "at ", "on ")):
                continue
            keep.append(p)
            total += 1
        if keep:
            trimmed_groups.append({"location": g.get("location"), "people": keep})
        if total >= 50:
            break

    write_outputs(trimmed_groups, args.out_md, args.out_csv)
    print(f"Wrote {total} people grouped by location to {args.out_md} and {args.out_csv}")


if __name__ == "__main__":
    main()
