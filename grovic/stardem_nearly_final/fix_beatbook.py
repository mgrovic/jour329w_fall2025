#!/usr/bin/env python3
"""
Line-by-line fact-checker for the environmental beatbook.
Uses Claude Sonnet 4.5 to correct names/titles using your CSV master list.
"""

import csv
import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic, APIError, RateLimitError

load_dotenv()  # load ANTHROPIC_API_KEY if present

# -----------------------
# CONFIG
# -----------------------

CSV_PATH = Path("people_md_de_va.csv")
MD_INPUT = Path("beatbook_revised.md")
MD_OUTPUT = Path("beatbook_factchecked.md")

MODEL = "claude-sonnet-4.5"
MAX_RETRIES = 5
SLEEP_SECONDS = 2

# -----------------------
# LOAD CSV -> dict
# -----------------------

def load_people(csv_path: Path):
    people = {}
    with csv_path.open(newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or row.get("Name") or row.get("ame") or "").strip()
            title = (row.get("title") or row.get("Title") or "").strip()
            if not name:
                continue

            people[name.lower()] = {
                "name": name,
                "title": title,
            }
    return people


# -----------------------
# LLM CALL (robust w/ retries)
# -----------------------

def ask_claude(anthropic: Anthropic, prompt: str) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            msg = anthropic.messages.create(
                model=MODEL,
                max_tokens=300,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return msg.content[0].text.strip()

        except RateLimitError:
            time.sleep(SLEEP_SECONDS * (attempt + 1))
        except APIError:
            time.sleep(SLEEP_SECONDS * (attempt + 1))

    return ""


# -----------------------
# BUILD LINE-BY-LINE PROMPT
# -----------------------

def build_prompt(line: str, people_db: dict):
    return f"""
You are a strict fact-checker. You correct ONLY name/title facts using the CSV dataset below.
You DO NOT add new people. You DO NOT add new information not in the CSV.

CSV PEOPLE DATABASE (authoritative source):
{json.dumps(list(people_db.values()), indent=2)}

TASK:
Fact-check the following line from a beatbook.

1. If a person in the line appears in the CSV:
   - Correct their name casing.
   - Correct their title to exactly match the CSV.
2. If CSV contradicts the line → FIX IT.
3. If the line mentions a person NOT in the CSV → DO NOT change anything.
4. Do NOT rewrite structure. Only fix names/titles.
5. Return ONLY the corrected line (no explanations).

LINE:
\"\"\"{line}\"\"\"
"""


# -----------------------
# MAIN PROCESSOR
# -----------------------

def process_markdown(md_path: Path, people_db: dict, client: Anthropic):
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    result_lines = []

    for i, line in enumerate(lines):
        # skip empty lines for speed
        if not line.strip():
            result_lines.append(line)
            continue

        prompt = build_prompt(line, people_db)
        corrected = ask_claude(client, prompt)

        # fallback if LLM fails
        if not corrected:
            corrected = line

        result_lines.append(corrected)

        # optional: debug printing
        print(f"[{i+1}/{len(lines)}] processed")

    return "\n".join(result_lines) + "\n"


# -----------------------
# MAIN
# -----------------------

def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: ANTHROPIC_API_KEY not set.")

    client = Anthropic(api_key=api_key)

    if not CSV_PATH.exists():
        raise SystemExit(f"Missing CSV: {CSV_PATH}")
    if not MD_INPUT.exists():
        raise SystemExit(f"Missing markdown file: {MD_INPUT}")

    print("Loading CSV...")
    people_db = load_people(CSV_PATH)

    print("Fact-checking...")
    cleaned = process_markdown(MD_INPUT, people_db, client)

    print(f"Writing → {MD_OUTPUT}")
    MD_OUTPUT.write_text(cleaned, encoding="utf-8")

    print("Done ✓")


if __name__ == "__main__":
    main()
