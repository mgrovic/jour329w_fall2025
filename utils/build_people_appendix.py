#!/usr/bin/env python3
import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Optional

try:
    import requests  # for optional LLM calls
except Exception:
    requests = None

# Simple acronym/alias mapping to normalize organizations found in titles
ORG_ALIASES = {
    "CBF": "Chesapeake Bay Foundation",
    "MDE": "Maryland Department of the Environment",
    "DNR": "Maryland Department of Natural Resources",
    "BDC": "Bainbridge Development Corporation",
}


def load_json_array(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            # some files may be a dict with a top-level array under a key
            for v in data.values():
                if isinstance(v, list):
                    return v
            return []
        except json.JSONDecodeError:
            # allow for JSON with trailing commas or comments by a naive cleanup
            text = f.read()
            text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
            text = re.sub(r",\s*([}\]])", r"\1", text)
            try:
                data = json.loads(text)
                return data if isinstance(data, list) else []
            except Exception:
                return []


def normalize_org(title: str | None) -> str | None:
    if not title:
        return None
    # Try to detect acronyms in the title
    for alias, proper in ORG_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", title):
            return proper
    return None


def collect_people(json_paths, people_csv_path: Path):
    people_map = defaultdict(lambda: {"name": None, "position": None, "organization": None, "sources": set()})

    # From JSONs
    for p in json_paths:
        articles = load_json_array(p)
        for art in articles:
            # derive organizations list for context
            orgs = []
            for key in ("key_institutions", "organizations"):
                v = art.get(key)
                if isinstance(v, list):
                    orgs.extend([str(x).strip() for x in v if x])
            if not isinstance(art.get("people"), list):
                continue
            for person in art.get("people", []):
                name = (person or {}).get("name") or (person or {}).get("Name")
                position = (person or {}).get("title") or (person or {}).get("Title")
                if not name:
                    continue
                rec = people_map[name]
                rec["name"] = name
                # Keep the most descriptive position (longest string)
                if position and (not rec["position"] or len(position) > len(rec["position"])):
                    rec["position"] = position
                # Try to set organization from title alias
                org_from_title = normalize_org(position)
                if org_from_title and not rec["organization"]:
                    rec["organization"] = org_from_title
                # If we still don't have org, and there is exactly one org in article, use it
                if not rec["organization"] and len(orgs) == 1:
                    rec["organization"] = orgs[0]
                # Record source docref
                docref = art.get("docref") or art.get("article_id")
                if docref:
                    rec["sources"].add(str(docref))

    # From CSV (optional enrichment)
    if people_csv_path.exists():
        with people_csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("name") or row.get("Name") or row.get("person") or row.get("Person") or "").strip()
                if not name:
                    continue
                position = (row.get("position") or row.get("Position") or row.get("title") or row.get("Title") or "").strip()
                organization = (row.get("organization") or row.get("Organization") or row.get("org") or row.get("Org") or "").strip()
                rec = people_map[name]
                rec["name"] = name
                if position and (not rec["position"] or len(position) > len(rec["position"])):
                    rec["position"] = position
                if organization:
                    rec["organization"] = organization
                # Optionally, accept a source column
                source = (row.get("source") or row.get("Source") or "").strip()
                if source:
                    rec["sources"].add(source)

    # Convert sources to sorted strings
    for rec in people_map.values():
        rec["sources"] = ", ".join(sorted(rec["sources"]))

    return list(people_map.values())


def write_csv(rows, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "position", "organization", "sources"])
        writer.writeheader()
        for r in sorted(rows, key=lambda x: (x["name"] or "")):
            writer.writerow(r)


def write_markdown(rows, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write("# People Appendix\n\n")
        f.write("A consolidated list of people, positions, and organizations from the provided sources.\n\n")
        for r in sorted(rows, key=lambda x: (x["name"] or "")):
            name = r["name"] or ""
            position = r["position"] or ""
            org = r["organization"] or ""
            sources = r["sources"] or ""
            line = f"- **Name:** {name} — **Position:** {position} — **Organization:** {org}"
            if sources:
                line += f" — Sources: {sources}"
            f.write(line + "\n")


def looks_like_real_name(name: str) -> bool:
    if not name:
        return False
    # Exclude clear non-person phrases
    bad_terms = [
        "county", "branch", "report", "document", "association", "service",
        "composting", "park", "board", "committee", "festival", "laboratory",
        "foundation", "conservancy", "university", "system", "department",
        "environmental", "partnership", "charter captains", "riverkeeper", "oyster",
    ]
    lower = name.lower()
    # Exclude location or preposition-led phrases
    if lower.startswith("in ") or lower.startswith("into ") or lower.startswith("at ") or lower.startswith("on "):
        return False
    # Exclude entries containing "," which often indicate place or descriptor phrases
    if "," in name:
        return False
    if any(t in lower for t in bad_terms):
        return False
    # Must contain at least a first and last token with initial caps
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    if len(parts) < 2:
        return False
    # Exclude organizations formatted as Title Case multi-word nouns ending with org-like suffixes
    org_suffixes = [
        "foundation", "environmental", "conservancy", "partnership", "university",
        "laboratory", "association", "board", "committee", "service", "system",
        "museum", "congress", "administration", "office",
    ]
    if parts and parts[-1].lower() in org_suffixes:
        return False
    # Allow middle initials and suffixes
    def cap_like(s: str) -> bool:
        return bool(re.match(r"^[A-Z][a-zA-Z'\-]+$", s)) or bool(re.match(r"^[A-Z]\.$", s))
    cap_tokens = sum(1 for p in parts if cap_like(p))
    return cap_tokens >= 2


def clean_and_dedupe(rows):
    seen = set()
    cleaned = []
    for r in rows:
        name = (r.get("name") or "").strip()
        if not looks_like_real_name(name):
            continue
        key = name.lower()
        if key in seen:
            # merge position/org if new info is longer
            for c in cleaned:
                if (c.get("name") or "").lower() == key:
                    pos = r.get("position") or ""
                    if pos and (not c.get("position") or len(pos) > len(c.get("position"))):
                        c["position"] = pos
                    org = r.get("organization") or ""
                    if org and not c.get("organization"):
                        c["organization"] = org
                    src = r.get("sources") or ""
                    if src:
                        c["sources"] = ", ".join(sorted(set((c.get("sources") or "").split(", ")) | set(src.split(", "))))
            continue
        seen.add(key)
        cleaned.append(r)
    return cleaned


def llm_generate_narrative(name: str, position: str, org: str, provider: Optional[str], model: Optional[str]) -> Optional[str]:
    """Call an external LLM provider (currently supports Groq) to create journalistic narrative.
    Requires environment variable GROQ_API_KEY when provider == 'groq'. Returns None if unavailable."""
    if not provider or not model or requests is None:
        return None
    prompt = (
        "You are a Chesapeake Bay/Eastern Shore beat writer. For the individual below, write a concise, journalistic blurb (2-3 sentences) that: "
        "1) explains what they can help with for Eastern Shore communities related to environment and aquaculture, 2) when and why to reach out to them, "
        "3) anchors specifics to Chesapeake Bay/Eastern Shore context. Avoid fluff; be specific.\n\n"
        f"Name: {name}\n"
        f"Position: {position}\n"
        f"Organization: {org}\n"
    )
    if provider == "groq":
        import os
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return None
        try:
            # Groq chat completions API
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a concise, specific journalist focused on Chesapeake Bay and Maryland Eastern Shore."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.4,
                "max_tokens": 220,
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content")
            return content.strip() if content else None
        except Exception:
            return None
    return None


def main():
    parser = argparse.ArgumentParser(description="Build a people appendix from JSON and CSV sources.")
    parser.add_argument("--json_v11", type=Path, default=Path("grovic/stardem_nearly_final/stories_with_entities_v11.json"))
    parser.add_argument("--json_v12", type=Path, default=Path("grovic/stardem_nearly_final/stories_with_entities_v12.json"))
    parser.add_argument("--people_csv", type=Path, default=Path("grovic/stardem_nearly_final/people_md_de_va.csv"))
    parser.add_argument("--out_csv", type=Path, default=Path("data/people_appendix.csv"))
    parser.add_argument("--out_md", type=Path, default=Path("grovic/stardem_nearly_final/people_appendix.md"))
    parser.add_argument("--narrative_md", type=Path, default=Path("grovic/stardem_nearly_final/people_appendix_narrative.md"))
    parser.add_argument("--use_llm", action="store_true", help="Use an external LLM to generate more journalistic narrative.")
    parser.add_argument("--llm_provider", type=str, default="groq", help="LLM provider id (e.g., groq)")
    parser.add_argument("--llm_model", type=str, default="groq/meta-llama/llama-4-maverick-17b-128e-instruct", help="LLM model id")
    args = parser.parse_args()

    # Build from sources
    rows = collect_people([args.json_v11, args.json_v12], args.people_csv)

    # Restrict to only people present in the CSV provided (name match)
    allowed_names = set()
    if args.people_csv.exists():
        with args.people_csv.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("name") or row.get("Name") or row.get("person") or row.get("Person") or "").strip()
                if name:
                    allowed_names.add(name)
    filtered_rows = [r for r in rows if r.get("name") in allowed_names]
    # Clean non-person entries and dedupe repeats
    filtered_rows = clean_and_dedupe(filtered_rows)

    write_csv(filtered_rows, args.out_csv)
    write_markdown(filtered_rows, args.out_md)

    # Create narrative appendix focusing on Eastern Shore relevance
    def narrative_for(r):
        name = r.get("name") or "This person"
        position = r.get("position") or ""
        org = r.get("organization") or ""
        # If LLM requested, try it first
        if args.use_llm:
            llm_text = llm_generate_narrative(name, position, org, args.llm_provider, args.llm_model)
            if llm_text:
                return f"- **{name}** — {position}; {org}. {llm_text}"
        # Heuristics based on org and title keywords
        pos_lower = position.lower()
        org_lower = org.lower()
        if "watermen" in org_lower or "waterman" in pos_lower:
            why = (
                "Best for harvest conditions, pricing, and season outlooks across the Bay. Reach out before regulatory changes or major weather shifts affecting crabbing/oystering to gauge impacts on local docks and markets."
            )
        elif any(k in org_lower for k in ["chesapeake bay foundation", "cbf"]):
            why = (
                "Go-to on water quality, oyster restoration, and aquaculture permitting on the Shore. Contact during permit reviews, algae events, or restoration projects for data, expert context, and advocacy positions."
            )
        elif any(k in org_lower for k in ["department of natural resources", "dnr"]):
            why = (
                "Authoritative source for seasons, size limits, and stock surveys. Engage around Blue Crab Winter Dredge results, oyster sanctuaries, and enforcement updates affecting Eastern Shore waterways."
            )
        elif any(k in org_lower for k in ["maryland department of the environment", "mde"]):
            why = (
                "Key contact for discharge permits, nutrient controls, and violations. Reach out during aquaculture proposals or storm-related pollution incidents impacting Choptank, Nanticoke, and local tributaries."
            )
        elif any(k in org_lower for k in ["seed to shuck", "hatchery", "aquaculture", "aquacon"]):
            why = (
                "Talk to them about spat-on-shell supply, restoration plantings, and market dynamics. Useful ahead of planting seasons and when new aquaculture facilities are proposed near Eastern Shore rivers."
            )
        else:
            why = (
                "Relevant to the Shore’s environmental or civic decisions. Contact when their domain intersects local waters, habitat, or seafood economy to clarify impacts and timelines."
            )
        return f"- **{name}** — {position}; {org}. Why important: {why}"

    args.narrative_md.parent.mkdir(parents=True, exist_ok=True)
    with args.narrative_md.open("w", encoding="utf-8") as nf:
        nf.write("# People Appendix (Narrative)\n\n")
        nf.write("Why these individuals matter for the Eastern Shore, based on their roles and organizations.\n\n")
        for r in sorted(filtered_rows, key=lambda x: (x["name"] or "")):
            nf.write(narrative_for(r) + "\n")

    print(f"Wrote {len(filtered_rows)} records to {args.out_csv}, {args.out_md}, and {args.narrative_md}")


if __name__ == "__main__":
    main()
