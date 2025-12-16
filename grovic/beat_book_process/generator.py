#!/usr/bin/env python3
"""
Generate a beatbook in Markdown from news stories.

- Safe batching (optional token estimation)
- Markdown output (no JSON required)
- Single output file
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import llm

# Optional: token estimation for safe batching
try:
    import tiktoken  # type: ignore
    TOKEN_ESTIMATION_AVAILABLE = True
except ImportError:
    TOKEN_ESTIMATION_AVAILABLE = False


def get_model(model_name: str | None = None):
    """
    Return an llm model instance.
    If a provider prefix is missing (e.g., "meta-llama/..."), try common providers.
    """
    if model_name:
        try:
            return llm.get_model(model_name)
        except Exception:
            # If no provider prefix or unknown prefix, try common providers
            parts = model_name.split("/", 1)
            prefix = parts[0] if parts else ""
            known = {"groq", "openai", "anthropic", "ollama"}
            candidates: List[str] = []
            if prefix not in known:
                candidates = [f"{p}/{model_name}" for p in ("groq", "openai", "anthropic", "ollama")]
            for cand in candidates:
                try:
                    return llm.get_model(cand)
                except Exception:
                    pass
            # Re-raise if nothing matched
            raise
    # Fall back to default model configured in llm
    return llm.get_model()


def estimate_tokens(text: str, model_hint: str = "gpt-4o-mini") -> int:
    if TOKEN_ESTIMATION_AVAILABLE:
        try:
            enc = tiktoken.encoding_for_model(model_hint)
        except Exception:
            enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    # Fallback: rough word count
    return max(1, len(text.split()))


def batch_stories(
    stories: List[Dict[str, Any]],
    max_tokens_per_batch: int = 5000,
    model_hint: str = "gpt-4o-mini",
) -> List[List[Dict[str, Any]]]:
    batches: List[List[Dict[str, Any]]] = []
    current_batch: List[Dict[str, Any]] = []
    current_tokens = 0

    for story in stories:
        story_text = json.dumps(story, ensure_ascii=False)
        story_tokens = estimate_tokens(story_text, model_hint=model_hint)
        if current_batch and (current_tokens + story_tokens) > max_tokens_per_batch:
            batches.append(current_batch)
            current_batch = []
            current_tokens = 0
        current_batch.append(story)
        current_tokens += story_tokens

    if current_batch:
        batches.append(current_batch)
    return batches


def call_model(model, prompt: str) -> str:
    """Call LLM and return raw text (Markdown)."""
    resp = model.prompt(prompt)
    text = getattr(resp, "text", str(resp))
    if callable(text):
        text = text()  # call method if callable
    return str(text)


def extract_batch_markdown(
    batch: List[Dict[str, Any]],
    batch_num: int,
    total_batches: int,
    model,
    topic: str,
) -> str:
    prompt = f"""
You are creating a practical beatbook for a reporter at the Easton Star Democrat (Maryland).
Beat/topic: {topic}

Audience: a new reporter who knows journalism basics. Write concise, clear Markdown.

Task: Summarize and synthesize the following {len(batch)} stories into a single cohesive Markdown section that teaches the reporter how to work this beat. Provide:
- What matters (key people, institutions, geography, issues/themes)
- How to report it (specific documents, datasets, meetings, contacts, fieldwork tips)
- Pitfalls and verification steps
- Short execution checklists when helpful
- Use short sentences and a neutral, official tone
- Include inline references like: [Story Title] (docref: ABC-123) if present in the input

Output: Markdown only (no JSON). Use H2/H3/H4 headings.

Stories JSON:
{json.dumps(batch, ensure_ascii=False, indent=2)}
""".strip()

    print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} stories)...", file=sys.stderr)
    md = call_model(model, prompt)
    if md is None:
        return "_No content generated for this batch._"
    return md


def main():
    parser = argparse.ArgumentParser(
        description="Generate Markdown beatbook from news stories (batched)."
    )
    parser.add_argument("input_files", nargs="+", help="JSON files with news stories")
    parser.add_argument("-o", "--output", default="beatbook_output.md", help="Markdown output file")
    parser.add_argument("-m", "--model", help="LLM model to use (llm model id)")
    parser.add_argument("-t", "--topic", default="Star Democrat Environment Beat (with Aquaculture focus)",
                        help="Topic label embedded in the prompt")
    parser.add_argument("--use-token-estimation", action=argparse.BooleanOptionalAction, default=None,
                        help="Enable/disable token-estimation batching (auto if omitted)")
    parser.add_argument("--max-tokens-per-batch", type=int, default=5000,
                        help="Approx token cap per batch when using token estimation")
    parser.add_argument("-b", "--batch-size", type=int, default=20,
                        help="Fixed items per batch (used if token estimation is disabled/unavailable)")
    parser.add_argument("--model-hint", default="gpt-4o-mini",
                        help="Tokenizer hint name for tiktoken (only affects batch sizing)")
    parser.add_argument("--debug", action="store_true", help="Write individual batch outputs to debug_batch_###.md")
    args = parser.parse_args()

    # Resolve whether to use token estimation
    if args.use_token_estimation is None:
        use_token_estimation = TOKEN_ESTIMATION_AVAILABLE
    else:
        use_token_estimation = bool(args.use_token_estimation)

    # Load stories from all input files
    all_stories: List[Dict[str, Any]] = []
    for file_path in args.input_files:
        p = Path(file_path)
        if not p.exists():
            print(f"Warning: file not found: {file_path}", file=sys.stderr)
            continue
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            all_stories.extend(data)
        elif isinstance(data, dict):
            if "stories" in data and isinstance(data["stories"], list):
                all_stories.extend(data["stories"])
            elif "articles" in data and isinstance(data["articles"], list):
                all_stories.extend(data["articles"])
            else:
                all_stories.append(data)
        else:
            raise ValueError(f"Unknown JSON structure in {file_path}")

    print(f"Loaded {len(all_stories)} stories total.", file=sys.stderr)
    if not all_stories:
        print("No stories to process. Exiting.", file=sys.stderr)
        sys.exit(1)

    # Batch stories
    if use_token_estimation:
        batches = batch_stories(
            all_stories,
            max_tokens_per_batch=args.max_tokens_per_batch,
            model_hint=args.model_hint,
        )
        print(f"Auto-sized into {len(batches)} batches (token estimation).", file=sys.stderr)
    else:
        batches = [all_stories[i:i + args.batch_size] for i in range(0, len(all_stories), args.batch_size)]
        print(f"Fixed batch size: {len(batches)} batches of up to {args.batch_size}.", file=sys.stderr)

    # Initialize model
    model = get_model(args.model)
    model_id = getattr(model, "model_id", str(args.model) if args.model else "default")
    print(f"Using model: {model_id}", file=sys.stderr)

    # Process batches
    markdown_batches: List[str] = []
    total_batches = len(batches)
    for i, batch in enumerate(batches, 1):
        try:
            md = extract_batch_markdown(batch, i, total_batches, model, topic=args.topic)
            markdown_batches.append(md)
            if args.debug:
                with open(f"debug_batch_{i:03d}.md", "w", encoding="utf-8") as fdbg:
                    fdbg.write(md)
        except Exception as e:
            print(f"Warning: batch {i} failed with error: {e}", file=sys.stderr)

    # Combine all batch outputs into a single Markdown file
    header = f"# Beatbook: {args.topic}\n\n"
    body = "\n\n---\n\n".join(markdown_batches) if markdown_batches else "_No content generated._\n"
    with open(args.output, "w", encoding="utf-8") as fout:
        fout.write(header)
        fout.write(body)

    print(f"Done. Saved output → {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
