import argparse, json, os, subprocess, shlex, time
from typing import List

DEFAULT_INPUT = "stardem_sample.json"
DEFAULT_OUTPUT = "stardem_topics_classified.json"
DEFAULT_MODEL = "groq/meta-llama/llama-4-scout-17b-16e-instruct"

DEFAULT_TOPICS = [
   "Local Government and Policy",
   "Crime and Law Enforcement",
   "Education and Schools",
   "Religion, Culture & Family",
   "Community",
   "Food and Agriculture",
   "Sports and Recreation",
   "National News",
   "Business and Economy",
   "Development",
   "History",
   "Environment and Bay Sustainability",
   "Other",
]


def load_topics(topics_file: str | None) -> List[str]:
    if not topics_file:
        return DEFAULT_TOPICS
    with open(topics_file, "r", encoding="utf-8") as f:
        text = f.read().strip()
    # support JSON list or newline-separated text
    try:
        maybe = json.loads(text)
        if isinstance(maybe, list) and all(isinstance(x, str) for x in maybe):
            return maybe
    except Exception:
        pass
    return [line.strip() for line in text.splitlines() if line.strip()]

def prompt_option1(story: dict) -> str:
    title = (story.get("title") or "").strip()
    content = (story.get("content") or story.get("summary") or story.get("body") or "").strip()
    return f"""
Analyze this news story and assign it a single topic category.
Choose a 1–2 word broad topic that best represents what this story is about.
Use consistent topic names; if unclear, pick 'Other'.

Title: {title}
Content: {content}

Return only the topic name as a single string.
""".strip()

def prompt_option2(story: dict, topic_list: List[str]) -> str:
    title = (story.get("title") or "").strip()
    content = (story.get("content") or story.get("summary") or story.get("body") or "").strip()
    return f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {title}
Content: {content}

Return only the topic name from the list above.
""".strip()

def call_llm(prompt: str, model: str, use_uv: bool, timeout: int = 60) -> str:
    quoted = shlex.quote(prompt)
    runner = "uv run llm" if use_uv else "llm"
    # no --max-tokens, no --temperature
    cmd = f"echo {quoted} | {runner} -m {shlex.quote(model)}"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "llm call failed")
    return (proc.stdout or "").strip() or (proc.stderr or "").strip()


def normalize_choice(raw: str) -> str:
    for line in (raw or "").splitlines():
        s = line.strip()
        if s:
            return s
    return (raw or "").strip()

def map_to_list(choice: str, topic_list: List[str]) -> str:
    if not choice:
        return "Other"
    if choice in topic_list:
        return choice
    for t in topic_list:
        if choice.lower() == t.lower():
            return t
    for t in topic_list:
        if t.lower() in choice.lower() or choice.lower() in t.lower():
            return t
    return "Other"

def run_classification(mode: str, stories: list[dict], model: str, use_uv: bool, topic_list: List[str], sleep_s: float):
    total = len(stories)
    print(f"Classifying {total} stories with mode={mode}, model={model}")
    for i, story in enumerate(stories, start=1):
        if story.get("topic"):
            print(f"[{i}/{total}] Skip (already has topic): {story.get('title','')[:70]}")
            continue
        if mode == "llm":
            prompt = prompt_option1(story)
        else:
            prompt = prompt_option2(story, topic_list)

        raw = ""
        for attempt in range(3):
            try:
                raw = call_llm(prompt, model, use_uv, timeout=60)
                break
            except Exception as e:
                print(f"[{i}/{total}] LLM error (attempt {attempt+1}): {e}")
                time.sleep(2 + attempt * 2)
        choice = normalize_choice(raw)
        topic = map_to_list(choice, topic_list) if mode == "list" else (choice or "Other")
        # In option1, still normalize to 'Other' if empty
        if mode == "llm" and topic not in topic_list:
            # best-effort map to default list to keep results tidy
            topic = map_to_list(topic, topic_list)
        story["topic"] = topic
        print(f"[{i}/{total}] Topic: {topic} — {story.get('title','')[:80]}")
        time.sleep(sleep_s)
    return stories

def main():
    ap = argparse.ArgumentParser(description="Classify Star-Democrat stories into topics using the `llm` CLI (Groq).")
    ap.add_argument("--input", "-i", default=DEFAULT_INPUT)
    ap.add_argument("--output", "-o", default=DEFAULT_OUTPUT)
    ap.add_argument("--model", "-m", default=os.environ.get("STARD_MODEL", DEFAULT_MODEL))
    ap.add_argument("--use-uv", action="store_true", help="Use `uv run llm`")
    ap.add_argument("--mode", choices=["llm", "list"], default="list", help="llm = LLM invents topics; list = pick from your list")
    ap.add_argument("--topics-file", help="Path to a JSON list or newline-separated file of topics (Option 2).")
    ap.add_argument("--sleep", type=float, default=0.5)
    args = ap.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"Input not found: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        stories = json.load(f)
    if not isinstance(stories, list):
        raise SystemExit("Input JSON must be a list of story objects.")

    topic_list = load_topics(args.topics_file)
    updated = run_classification(args.mode, stories, args.model, args.use_uv, topic_list, args.sleep)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
    print(f"Saved classified stories to {args.output}")

if __name__ == "__main__":
    main()