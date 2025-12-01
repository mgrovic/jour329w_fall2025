#!/usr/bin/env python3
"""
Revise beatbook_combined.md to emphasize residents' impact, prioritize local sources,
convert organization bullets to explanatory narrative, link docs/data/tools to story "why",
and make story ideas more narrative (what/why first, then where/how). Also de-emphasize
generic ethics content by collapsing Section 10 to geographic pitfalls and accuracy traps.

Usage:
  uv run python beatbook_reviser.py \
    -i beatbook_combined.md \
    -o beatbook_revised.md \
    -m groq/meta-llama/llama-4-maverick-17b-128e-instruct

Tips:
- Runs section-by-section to stay under Groq token limits.
- Preserves headings and docrefs. Does not invent facts; rewrites for clarity and focus.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import llm


# -------------------------
# LLM helpers
# -------------------------

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
    # datasette-llm Response.text may be a callable
    if hasattr(resp, "text"):
        t = resp.text
        if callable(t):
            try:
                return t()
            except Exception:
                return ""
        return t
    return str(resp)


# -------------------------
# Section parsing
# -------------------------

SECTION_HEADER_RE = re.compile(r"(?m)^##\s*(\d+)\)\s*(.+?)\s*$")

def split_sections(md: str) -> Tuple[List[int], Dict[int, Tuple[str, str]]]:
    """
    Return (order, mapping) where mapping[num] = (header_line, body_text)
    Keeps everything outside numbered sections as preface (num=0).
    """
    parts = []
    last_pos = 0
    order: List[int] = []
    mapping: Dict[int, Tuple[str, str]] = {}

    # Find all headers with numbers like "## 4) Source Profiles (People)"
    for m in SECTION_HEADER_RE.finditer(md):
        header_start = m.start()
        header_end = m.end()
        section_num = int(m.group(1))
        header_line = md[m.start():m.end()]

        # capture previous chunk as body of the previous header (or preface if first)
        if parts:
            prev_num, prev_header, prev_start, prev_end = parts[-1]
            body = md[prev_end:header_start]
            mapping[prev_num] = (prev_header, body)
        else:
            # anything before first section is preface
            preface = md[:header_start]
            if preface.strip():
                mapping[0] = ("__PREFACE__", preface)

        parts.append((section_num, header_line, header_start, header_end))
        order.append(section_num)
        last_pos = header_end

    # Last section body
    if parts:
        last_num, last_header, _, last_header_end = parts[-1]
        mapping[last_num] = (last_header, md[last_header_end:])
    else:
        # No numbered sections found; treat entire doc as a single body
        mapping[1] = ("## 1) Revised Beatbook", md)
        order = [1]

    return order, mapping


# -------------------------
# Prompts per section
# -------------------------

BASE_EDITOR_PROMPT = """You are revising a single section of a local-environment/aquaculture beatbook for the Easton Star Democrat.

Core editorial changes to apply now:
- Keep geography, but remove repetition; foreground how issues affect Eastern Shore residents and working communities.
- Prioritize local sources over statewide; reflect that in ordering and emphasis.
- Turn bullet-heavy organization content into short narrative paragraphs explaining why each org matters, with generic tips that apply across orgs (e.g., get on press lists, subscribe to agendas).
- Make Documents/Data/Tools explicitly connect to stories: for each key item, add a quick "Why this matters" use case.
- Rewrite Story Opportunities as short narrative pitches: lead with the WHAT and WHY; then the WHERE and HOW (people to call, docs to pull).
- De-emphasize generic "reporting 101" ethics; keep geographic pitfalls and concrete accuracy checks (permit numbers, boundaries, dates).

Rules:
- Do not invent facts; only reorganize, condense, or clarify what the source text already contains.
- Preserve story citations and docrefs exactly: [Title] (docref: news/XXXX)
- Keep section header as-is; maintain roughly similar length unless instructed otherwise.
- Short, direct sentences. Professional tone.
- If something is missing in the source text, note it in a [Gap] bullet instead of making it up.

Now revise the section below accordingly.
"""

SECTION_SPECIFIC_GUIDANCE = {
    1: """Section 1 guidance:
- Reduce repeated county/river lists; keep a concise place frame.
- Add 3–5 sentences showing resident impact (work, water bills, flooding, access).
- Keep 3–5 citations with docrefs.
""",
    2: """Section 2 guidance:
- For each core issue (water quality, fisheries, climate, industrial pollution/DAF, conservation), add a 5–8 step micro-workflow (who to call first, what doc/data to pull, a verification step).
- Tie each issue to specific communities or worker impacts.
""",
    3: """Section 3 guidance:
- Keep WHERE aquaculture happens; add how residents/watermen are impacted.
- Add a siting conflict mini-narrative (what/why first).
- Keep the proposal checklist, but trim redundancy.
""",
    4: """Section 4 guidance:
- Reorder so LOCAL sources appear first. Mark locals with (LOCAL PRIORITY).
- For each source, include: GEOGRAPHIC COVERAGE, When to call, First questions.
- Move statewide sources after locals.
""",
    5: """Section 5 guidance:
- Convert bullets to short paragraphs explaining why each org matters to a reporter.
- Add generic recommendations applicable across orgs (press lists, agendas, meeting packets).
""",
    6: """Section 6 guidance:
- For each document/dataset/tool, add a one-line "Why this matters" tied to a story type.
- Keep retrieval paths and FOIA/PRA notes concise.
""",
    7: """Section 7 guidance:
- Rewrite each idea into a 4–6 sentence narrative pitch: WHAT/WHY first, then WHERE/HOW.
- Include who to call (locals first), key docs, and a verification step.
""",
    8: """Section 8 guidance:
- Keep location-specific cautions; add 1–2 resident-facing tips (e.g., who to notify, public access etiquette).
""",
    9: """Section 9 guidance:
- Keep cadence; add a "First 4 weeks" onboarding plan with concrete places and meetings.
""",
    10: """Section 10 guidance:
- Collapse to a concise "Geographic pitfalls and accuracy traps" list; remove generic reporting-101 items.
""",
    11: """Section 11 guidance:
- Reorder contact list: locals first, then regional/state.
- Keep fields; mark locals as (LOCAL PRIORITY).
""",
    12: """Section 12 guidance:
- Keep citations grouped; ensure docrefs preserved.
- One-line "why it matters" for each, tied to residents/communities.
""",
}

def make_section_prompt(section_num: int, source_section: str) -> str:
    spec = SECTION_SPECIFIC_GUIDANCE.get(section_num, "")
    src_trim = source_section[:12000]  # keep prompt under model limits
    return f"""{BASE_EDITOR_PROMPT}

Section-specific guidance:
{spec}

--- SOURCE SECTION START ---
{src_trim}
--- SOURCE SECTION END ---

Output the fully revised section, starting with the original header line.
"""


# -------------------------
# Transformation
# -------------------------

def transform_section(model, section_num: int, header: str, body: str) -> str:
    prompt = make_section_prompt(section_num, f"{header}\n{body}")
    resp = model.prompt(prompt)
    text = _resp_text(resp).strip()
    # Fallback: if model forgot header, reattach original header
    if not text.startswith(header.strip()):
        text = f"{header}\n\n{text}"
    return text

def revise_document(model, md_text: str) -> str:
    order, mapping = split_sections(md_text)
    pieces: List[str] = []
    # Keep preface if present
    if 0 in mapping:
        pref_header, pref_body = mapping[0]
        if pref_body.strip():
            pieces.append(pref_body)

    for num in order:
        header, body = mapping.get(num, ("", ""))
        if not header:
            continue
        print(f"Revising section {num}...", file=sys.stderr)
        revised = transform_section(model, num, header, body)
        pieces.append(revised)

    return "\n\n".join(pieces).strip() + "\n"


# -------------------------
# CLI
# -------------------------

def main():
    ap = argparse.ArgumentParser(description="Revise beatbook_combined.md to emphasize residents, local sources, narrative orgs and stories.")
    ap.add_argument("-i", "--input", required=True, help="Input Markdown file (beatbook_combined.md)")
    ap.add_argument("-o", "--output", default="beatbook_revised.md", help="Output Markdown file")
    ap.add_argument("-m", "--model", help="LLM model id (e.g., groq/meta-llama/llama-4-maverick-17b-128e-instruct)")
    ap.add_argument("--dry-run", action="store_true", help="Print planned section headers and exit")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"Input not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    text = in_path.read_text(encoding="utf-8")
    order, mapping = split_sections(text)

    if args.dry_run:
        print("Sections detected:")
        for num in ([0] if 0 in mapping else []) + order:
            header = mapping[num][0] if num in mapping else ""
            print(f"- {num}: {header.strip() if header else '(preface)'}")
        sys.exit(0)

    model = get_model(args.model)
    print(f"Using model: {getattr(model, 'model_id', args.model)}", file=sys.stderr)

    out_text = revise_document(model, text)
    out_path = Path(args.output)
    out_path.write_text(out_text, encoding="utf-8")
    print(f"Wrote revised beatbook → {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()