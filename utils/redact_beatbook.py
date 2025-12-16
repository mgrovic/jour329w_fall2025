#!/usr/bin/env python3
import argparse
import os
import re
import sys
from typing import List, Optional

# --------- Lightweight sanitizers (links, emails) ---------
LINK_MD_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
WWW_RE = re.compile(r"\bwww\.[^\s)]+", re.IGNORECASE)
BARE_DOMAIN_RE = re.compile(r"\b[\w.-]+\.(?:com|org|gov|edu|net|io|co|us|uk)(?:/\S+)?", re.IGNORECASE)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
DOCREF_PAREN_RE = re.compile(r"\([^\)]*?docref:[^\)]*\)", re.IGNORECASE)
TEL_PAREN_RE = re.compile(r"\([^\)]*?tel:[^\)]*\)", re.IGNORECASE)
EXTRA_SPACES_RE = re.compile(r"[ \t]{2,}")
MULTI_BLANK_LINES_RE = re.compile(r"\n{3,}")


def strip_links_and_emails(text: str) -> str:
    # Replace markdown links [text](url) -> text
    text = LINK_MD_RE.sub(lambda m: m.group(1), text)
    # Remove docref parentheses entirely
    text = DOCREF_PAREN_RE.sub("", text)
    # Remove (tel:...) placeholders entirely
    text = TEL_PAREN_RE.sub("", text)
    # Remove bare URLs
    text = URL_RE.sub("", text)
    text = WWW_RE.sub("", text)
    # Remove bare domains (example.org, agency.gov/path)
    text = BARE_DOMAIN_RE.sub("", text)
    # Remove emails
    text = EMAIL_RE.sub("", text)
    # Clean leftover empty parentheses and double punctuation
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\s+[),.;:!?]", lambda m: m.group(0).strip(), text)
    text = re.sub(r"[,;:—-]{2,}", ",", text)
    # Collapse spaces created by removals around em dashes and commas
    text = re.sub(r"\s*—\s*", " — ", text)
    text = re.sub(r"\s*,\s*", ", ", text)
    text = EXTRA_SPACES_RE.sub(" ", text)
    text = MULTI_BLANK_LINES_RE.sub("\n\n", text)
    return text.strip() + "\n"


# --------- LLM integration (optional) ---------

def _load_openai_client(api_key_env: str):
    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:
        print("ERROR: The 'openai' package is required for --mode llm. Install with: pip install openai", file=sys.stderr)
        raise
    api_key = os.getenv(api_key_env)
    if not api_key:
        print(f"ERROR: Environment variable {api_key_env} is not set. Export your API key and retry.", file=sys.stderr)
        raise RuntimeError("Missing API key")
    client = OpenAI(api_key=api_key)
    return client


def _load_groq_client(api_key_env: str):
    try:
        from groq import Groq  # type: ignore
    except Exception as e:
        print("ERROR: The 'groq' package is required for Groq provider. Install with: pip install groq", file=sys.stderr)
        raise
    api_key = os.getenv(api_key_env)
    if not api_key:
        print(f"ERROR: Environment variable {api_key_env} is not set. Export your API key and retry.", file=sys.stderr)
        raise RuntimeError("Missing API key")
    client = Groq(api_key=api_key)
    return client


def _chunk_by_sections(text: str, max_chars: int = 12000) -> List[str]:
    # Split on level-2+ headings to keep structure where possible
    parts: List[str] = []
    current = []
    current_len = 0
    for line in text.splitlines(keepends=True):
        if line.startswith("## ") and current_len > 0 and current_len + len(line) > max_chars:
            parts.append(''.join(current))
            current = [line]
            current_len = len(line)
        else:
            current.append(line)
            current_len += len(line)
    if current:
        parts.append(''.join(current))
    # If any part still too big, fallback to rough chunking
    final: List[str] = []
    for p in parts:
        if len(p) <= max_chars:
            final.append(p)
        else:
            # split by paragraphs
            para = p.split("\n\n")
            buf, blen = [], 0
            for seg in para:
                seg2 = seg + "\n\n"
                if blen + len(seg2) > max_chars and buf:
                    final.append(''.join(buf))
                    buf, blen = [seg2], len(seg2)
                else:
                    buf.append(seg2)
                    blen += len(seg2)
            if buf:
                final.append(''.join(buf))
    return final


def redact_with_llm(text: str, model: str, api_key_env: str, provider: str = "openai") -> str:
    # Provider routing
    actual_model = model
    if model.startswith("groq/"):
        provider = "groq"
        actual_model = model.split("/", 1)[1]

    if provider == "groq":
        client = _load_groq_client(api_key_env)
    else:
        client = _load_openai_client(api_key_env)

    system = (
        "You are a careful redaction assistant for newsroom beatbooks. "
        "Task: Remove ALL personal names (of people) AND their positions/titles wherever they appear. "
        "Also remove emails and any links/URLs; for markdown links, keep only the link text and drop the URL. "
        "Remove any '(docref: …)' parentheticals entirely. Remove '(tel: …)' placeholders. "
        "Preserve all other information, structure, and headings. "
        "When removing names/titles breaks a sentence, REWRITE minimally to preserve the useful information generically "
        "(e.g., replace with 'a local riverkeeper', 'a county official', 'an advocacy group spokesperson') but do NOT invent new facts. "
        "Favor concise, grammatical results over verbatim phrasing. "
        "After redaction, normalize punctuation, spaces, and blank lines."
    )

    chunks = _chunk_by_sections(text)
    outputs: List[str] = []

    for idx, chunk in enumerate(chunks):
        # Pre-strip links/emails to reduce token load; LLM focuses on names/titles redaction + light rewrite.
        pre = strip_links_and_emails(chunk)
        resp = client.chat.completions.create(
            model=actual_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": pre},
            ],
            temperature=0,
        )
        out = resp.choices[0].message.content or ""
        outputs.append(out)

    combined = "\n".join(outputs)
    # Final pass to normalize whitespace and punctuation
    combined = EXTRA_SPACES_RE.sub(" ", combined)
    combined = MULTI_BLANK_LINES_RE.sub("\n\n", combined).strip() + "\n"
    return combined


# --------- Regex-only mode (no names) ---------

def redact_with_regex_only(text: str) -> str:
    # Intentionally does NOT attempt to remove personal names/titles
    # (too error-prone without an LLM or NER); only removes links/emails.
    return strip_links_and_emails(text)


def main():
    parser = argparse.ArgumentParser(description="Redact names/titles and strip links/emails from a beatbook markdown file.")
    parser.add_argument("input", help="Path to input markdown file")
    parser.add_argument("-o", "--output", help="Path to output file (default: <input>.redacted.md)")
    parser.add_argument("--mode", choices=["llm", "regex"], default="llm", help="Use LLM for name/title redaction (with minimal rewrite) or regex-only (links/emails only)")
    parser.add_argument("--model", default=os.getenv("REDACT_MODEL", "gpt-4o-mini"), help="LLM model name (OpenAI or Groq). Prefix with 'groq/' to force Groq provider.")
    parser.add_argument("--provider", choices=["openai", "groq"], default=os.getenv("REDACT_PROVIDER", "openai"), help="LLM provider override (default: openai). Ignored if --model starts with groq/.")
    parser.add_argument("--api-key-env", default=os.getenv("REDACT_API_ENV", "OPENAI_API_KEY"), help="Env var name holding API key (default: OPENAI_API_KEY for OpenAI, GROQ_API_KEY for Groq)")
    args = parser.parse_args()

    in_path = args.input
    out_path = args.output or (os.path.splitext(in_path)[0] + ".redacted.md")

    if not os.path.exists(in_path):
        print(f"ERROR: Input file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        text = f.read()

    if args.mode == "llm":
        try:
            # If provider is groq but api key env is default, switch to GROQ_API_KEY unless user overrode.
            api_env = args.api_key_env
            provider = args.provider
            if args.model.startswith("groq/"):
                provider = "groq"
                if api_env == "OPENAI_API_KEY":
                    api_env = "GROQ_API_KEY"
            result = redact_with_llm(text, model=args.model, api_key_env=api_env, provider=provider)
        except Exception as e:
            print(f"ERROR during LLM redaction: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        result = redact_with_regex_only(text)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Redacted file written to: {out_path}")


if __name__ == "__main__":
    main()
