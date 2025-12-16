Star-Democrat Topic Classification 10/30/25

I chose option 2. I did this because I feel more confident in the categories that I created, just based on the background context that I have. I also think that LLMs also editorilaize a little too much for my liking. 

Local Government and Policy 
Crime 
Education
Religion and Culture - When looking at the heat map, it seems that a lot more stories then expected had to do with religon.
Food, Family & Lifestyle
Sports and Recreation 
Regional and National News 
Business and Development 
Environment and Bay Sustainability
Other

1. **Topic Distribution**: How many stories are in each topic?
Local Government and Policy - 47 
Crime - 8 
Education - 7
Religion and Culture - 9 
Food, Family and Lifestyle - 14
Sports and Recreation - 31
Regional and National News - 69
Business and Development - 9
Environment and Bay Sustainability - 4
Other - 2 

2. **Topic Consistency**: Do similar stories get the same topic?
I think for the most part, it did a good job grouping similar stories to the correct topic. I noticed that the smaller the number of stories had, the more similar the stoires are. The topic to me that seems to need the most work is 

3. **Topic Clarity**: Are the topic names clear and distinct?
I think that the topic names are pretty distinct. There may be a bit of overlap in *Religon and Culture* and *Food Family and Lifestyle* as I think Lifestyle and Culture had a bit of an overlap.

4. **Coverage Patterns**: What does the distribution tell you about Star-Democrat coverage?
It is super interesting to me that such a small local newspaper has such a strong focus on national news/stories. When looking through the National News Stories, it seems like these are all properly sorted. To make an infrence from these results, I would assume that people reading the stardem are not only expecting to get their local news from the paper, but national and world news as well. 



Results Analysis

#### Quality Assessment
- Did the LLM (or you and the LLM) do a good job with the list of topics?
I think I did an Okay job with the list of topics, although local government and national news need to be refined. 

- Are there topics that seem too broad or too narrow?
I think that Local Gov and National News were two topics that may have been too broad. The national news seemed like it did encompass all the stories in the topic, but they could have been sorted into better topics, ie national news, historical events and world news, or something along those lines. 

- Are there stories that seem mis-categorized?
yes

- Give specific examples of stories and their topics

Ravens flock; Local kids honored at NFL game - in the Local Government and Policy Tag. This could have been sorted into a lot of diff topics, but I think that local government is incorrect. 

New training center will provide cross-training, easier commute for first responders - Also in Local gov. Should have been in buisness and dev? or even expand crime to crime and law enforment

#### Topic Refinement
- What topics should be consolidated or combined?
I think my issue is not the topics needing consolidation, but neeeing more. 

- What topics are missing that would be useful?
I think that a history topic that would be very useful to cut down on the national news, add law enforcement in  

- Are there redundant or overlapping topics?
As I said earlier, I think that culture and lifestyle might have overlapped a bit, but not too much. Most of my issues lay in the topics being too broad. 

- How would you revise the topic list?
Local Government and Policy 
Crime and Law enforcment
Education and Schools
Religion, Culture & Family
Community
Food
Sports and Recreation 
National News 
History
Business and Economy 
Development 
Environment and Bay Sustainability
Other

#### Approach Evaluation
- Did your chosen approach (Option 1 or 2) work well?

Honestly, not as well as I hoped. While Option 2 gave me more control and let me rely on my own judgment, I still ran into challenges with defining categories that were specific enough. Some stories were difficult to classify because they touched on multiple themes, which made the process more subjective than I expected.


- Would the other approach have been better? Why or why not?

Maybe, but not entirely. The LLM approach  might have been faster and more consistent, but I was worried it would have oversimplified or not known local context. I think combining both approaches using the LLM for an initial draft and then refining the categories myself prob would produce the best results overall.



- What surprised you about the results?
 I was surprised by how many stories fell under Regional and National News for such a small local paper. I expected most of the content to focus on local government, community events, or small-town updates, but instead there was a heavy coverage of  broader national events . This suggests that the stardem is more of a complete news source than a local paper. 



I ran this again with an updated list (Local Government and Policy
Crime and Law Enforcement
Education and Schools
Religion, Culture & Family
Community
Food
Sports and Recreation
National News
History
Business and Economy
Development
Environment and Bay Sustainability
Other
), after learning from round one. Man I was way more impressed. Everything looked way better


Convo With Copilot
mgrovic: build me a Python script called `classify_topics.py`. I need it to read the json file 'stardem_sample.json', then, using grok, add a topic to each story using the following list: Local Government and Policy 
Crime 
Education
Religion and Culture
Food, Family & Lifestyle
Sports and Recreation 
Regional and National News 
Business and Development 
Environment and Bay Sustainability
Other. 

GitHub Copilot: ````python
import json
import subprocess
import shlex
import time
import os
import sys
from collections import Counter

# Config
INPUT = "stardem_sample.json"
OUTPUT = "stardem_topics_classified.json"
MODEL = os.environ.get("STARDem_MODEL", "groq/meta-llama/llama-4-scout-17b-16e-instruct")
USE_UV = os.environ.get("USE_UV", "") != ""  # set USE_UV=1 to call via `uv run llm ...`
MAX_PROMPT_CHARS = 18_000  # keep prompts reasonable

TOPICS = [
    "Local Government and Policy",
    "Crime",
    "Education",
    "Religion and Culture",
    "Food, Family & Lifestyle",
    "Sports and Recreation",
    "Regional and National News",
    "Business and Development",
    "Environment and Bay Sustainability",
    "Other",
]

def build_prompt(story, topics):
    title = story.get("title", "") or ""
    content = story.get("content", "") or story.get("body", "") or ""
    # truncate content so prompt isn't huge
    if len(content) > MAX_PROMPT_CHARS:
        content = content[:MAX_PROMPT_CHARS] + "\n\n[TRUNCATED]"
    prompt = f"""Assign this news story to EXACTLY ONE topic from the following list (choose the single best match). Return only the topic name exactly as one of the options below (no punctuation, no extra text).

Topics:
{', '.join(topics)}

Title:
{title}

Content:
{content}
"""
    return prompt

def run_llm(prompt, model):
    """
    Try calling the `llm` CLI. Try a couple of common invocation patterns.
    Returns the raw output string or raises RuntimeError.
    """
    # try direct llm complete --model MODEL (reads stdin)
    cmds = []
    if USE_UV:
        # uv run llm complete --model MODEL
        cmds.append(["uv", "run", "llm", "complete", "--model", model])
        cmds.append(["uv", "run", "llm", "--model", model])
    else:
        cmds.append(["llm", "complete", "--model", model])
        cmds.append(["llm", "--model", model])
        # some llm CLIs accept: llm text "<prompt>" --model MODEL
        cmds.append(["llm", "text", "--model", model])

    last_err = None
    for cmd in cmds:
        try:
            proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=120)
            out = (proc.stdout or "").strip()
            err = (proc.stderr or "").strip()
            if proc.returncode == 0 and out:
                return out
            # sometimes llm prints result to stderr
            if proc.returncode == 0 and err:
                return err
            last_err = (cmd, proc.returncode, out, err)
        except FileNotFoundError as e:
            last_err = ("notfound", str(e))
        except subprocess.TimeoutExpired as e:
            last_err = ("timeout", str(e))
    raise RuntimeError(f"llm CLI failed; last error: {last_err}")

# Fallback heuristic if LLM not available or returns bad output
KEYWORD_MAP = {
    "Local Government": ["county", "council", "commission", "mayor", "county commissioners", "board of supervisors", "budget", "zoning"],
    "Crime": ["shooting", "arrest", "charged", "charged with", "police", "crime", "robbery", "homicide", "assault"],
    "Education": ["school", "superintendent", "students", "teacher", "board of education", "graduation", "curriculum"],
    "Religion and Culture": ["church", "faith", "religion", "worship", "parish", "cultural", "festival"],
    "Food, Family & Lifestyle": ["restaurant", "food", "family", "recipe", "lifestyle", "wedding"],
    "Sports and Recreation": ["game", "match", "coach", "season", "tournament", "athlete", "sports"],
    "Regional and National News": ["federal", "national", "governor", "statewide", "congress", "senate", "supreme court"],
    "Business and Development": ["company", "business", "development", "project", "real estate", "economic", "employer"],
    "Environment and Bay Sustainability": ["bay", "environment", "water quality", "pollution", "conservation", "shoreline", "habitat"],
}

def heuristic_topic(story):
    text = (story.get("title","") + " " + story.get("content","") + " " + " ".join(story.get("tags",[]

mgrovic: Saves the results to a new JSON file called `stardem_topics_classified.json` 

GitHub Copilot: 

mgrovic: - Use the `llm` command-line tool with an appropriate Groq model (e.g., `groq/meta-llama/llama-4-scout-17b-16e-instruct` or `groq-kimi-k2` or `groq/meta-llama/llama-4-maverick-17b-128e-instruct`)
- Process each story and add a `topic` field
- Save the enhanced stories to `stardem_topics_classified.json`
- Print progress as it processes stories

**Tip**: Have the script use subprocess to call the `llm` command. You should provide this document (`stardem_topics.md`) as a reference.

GitHub Copilot: ````python
# ...existing code...
"""
classify_topics.py

Reads 'stardem_sample.json', classifies each story into one topic using the `llm` CLI (Groq models),
and writes results to 'stardem_topics_classified.json'.

Usage:
  python classify_topics.py \
    --input /path/to/stardem_sample.json \
    --output /path/to/stardem_topics_classified.json \
    --model groq/meta-llama/llama-4-scout-17b-16e-instruct

If your environment requires the `uv` wrapper, set environment variable USE_UV=1
or pass --use-uv on the command line.
"""
import json
import subprocess
import argparse
import shlex
import time
import os
from typing import List

TOPIC_LIST: List[str] = [
    "Local Government and Policy",
    "Crime",
    "Education",
    "Religion and Culture",
    "Food, Family & Lifestyle",
    "Sports and Recreation",
    "Regional and National News",
    "Business and Development",
    "Environment and Bay Sustainability",
    "Other",
]

DEFAULT_MODEL = "groq/meta-llama/llama-4-scout-17b-16e-instruct"
DEFAULT_INPUT = "stardem_sample.json"
DEFAULT_OUTPUT = "stardem_topics_classified.json"


def build_prompt(story: dict, topic_list: List[str]) -> str:
    title = story.get("title", "") or ""
    content = story.get("content", "") or story.get("summary", "") or ""
    # keep prompt short but clear
    prompt = f"""
You are a topic classifier. Choose exactly ONE topic from the following list (match exactly):

{', '.join(topic_list)}

Title:
{title}

Content:
{content}

Return ONLY the topic name (exactly as it appears in the list above) and nothing else.
"""
    return prompt.strip()


def call_llm(prompt: str, model: str, llm_cmd: str, timeout: int = 30) -> str:
    """
    Calls the CLI 'llm' (or uv run llm) and returns the raw output string.
    This uses a shell pipeline: echo 'prompt' | <llm_cmd> -m <model> --temperature 0 --max-tokens 16
    """
    safe_prompt = shlex.quote(prompt)
    # prefer `llm -m MODEL` syntax; adjust if your llm uses different flags
    cmd = f"echo {safe_prompt} | {llm_cmd} -m {shlex.quote(model)} --temperature 0 --max-tokens 16"
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"llm CLI error: {proc.stderr.strip()}")
        return proc.stdout.strip()
    except Exception as exc:
        raise


def normalize_choice(text: str) -> str:
    if not text:
        return ""
    # pick first non-empty line, strip whitespace
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return text.strip()


def choose_topic_from_output(raw: str, topic_list: List[str]) -> str:
    choice = normalize_choice(raw)
    # exact match preferred (case-sensitive)
    if choice in topic_list:
        return choice
    # try case-insensitive match
    for t in topic_list:
        if choice.lower() == t.lower():
            return t
    # try partial matches
    for t in topic_list:
        if t.lower() in choice.lower() or choice.lower() in t.lower():
            return t
    return "Other"


def main():
    parser = argparse.ArgumentParser(description="Classify Star-Democrat stories into topics using llm CLI.")
    parser.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Input JSON file (list of stories).")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Output JSON file to write classified stories.")
    parser.add_argument("--model", "-m", default=os.environ.get("STARD_MODEL", DEFAULT_MODEL), help="LLM model name to pass to llm.")
    parser.add_argument("--use-uv", action="store_true", default=(os.environ.get("USE_UV") == "1"), help="If set use 'uv run llm' instead of 'llm'.")
    parser.add_argument("--start", type=int, default=0, help="Start index (for batching/retry).")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of stories to process (0 = all).")
    parser.add_argument("--sleep", type=float, default=0.5, help="Seconds to sleep between calls (rate control).")
    args = parser.parse_args()

    llm_cmd = "llm"
    if args.use_uv:
        llm_cmd = "uv run llm"

    # Load stories
    with open(args.input, "r", encoding="utf-8") as f:
        stories = json.load(f)

    if not isinstance(stories, list):
        raise SystemExit("Input JSON must be an array of story objects.")

    total = len(stories)
    end_index = total if args.limit <= 0 else min(total, args.start + args.limit)

    print(f"Classifying stories {args.start}..{end_index - 1} (total {total}) using model {args.model}")
    for i in range(args.start, end_index):
        story = stories[i]
        # skip if already has topic
        if "topic" in story and story["topic"]:
            print(f"[{i+1}/{total}] Skipping (already has topic): {story.get('title','')[:60]}")
            continue

        prompt = build_prompt(story, TOPIC_LIST)
        # try calling llm with retries
        raw_output = ""
        for attempt in range(3):
            try:
                raw_output = call_llm(prompt, args.model, llm_cmd, timeout=60)
                break
            except Exception as e:
                print(f"[{i+1}/{total}] llm call failed (attempt {attempt+1}): {e}")
                time.sleep(2 + attempt * 2)
        if not raw_output:
            print(f"[{i+1}/{total}] Failed to get response, assigning 'Other'")
            story["topic"] = "Other"
        else:
            topic = choose_topic_from_output(raw_output, TOPIC_LIST)
            story["topic"] = topic
            print(f"[{i+1}/{total}] Assigned topic: {topic} -- {story.get('title','')[:80]}")

        # small delay to avoid throttling
        time.sleep(args.sleep)

    # Save results
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

    print(f"Saved classified stories to {args.output}")


if __name__ == "__main__":
    main()
# ...existing code...
````

mgrovic: please do this for me

GitHub Copilot: ````python
# ...existing code...
"""
Classify Star-Democrat stories into topics using the `llm` CLI (Groq models).

Creates 'stardem_topics_classified.json' with a new 'topic' field for each story.

Usage:
  cd /workspaces/jour329w_fall2025/grovic/stardem_topics
  python classify_topics.py --input stardem_sample.json --output stardem_topics_classified.json

Options:
  --model     LLM model to pass to `llm` (default: groq/meta-llama/llama-4-scout-17b-16e-instruct)
  --use-uv    Use 'uv run llm' instead of 'llm' (for devcontainer setups)
  --start     Start index (for batching)
  --limit     Max stories to process (0 = all)
  --sleep     Seconds to sleep between calls (rate control)
"""
from __future__ import annotations
import argparse
import json
import os
import shlex
import subprocess
import time
from typing import List

TOPIC_LIST: List[str] = [
    "Local Government and Policy",
    "Crime",
    "Education",
    "Religion and Culture",
    "Food, Family & Lifestyle",
    "Sports and Recreation",
    "Regional and National News",
    "Business and Development",
    "Environment and Bay Sustainability",
    "Other",
]

DEFAULT_MODEL = "groq/meta-llama/llama-4-scout-17b-16e-instruct"
DEFAULT_INPUT = "stardem_sample.json"
DEFAULT_OUTPUT = "stardem_topics_classified.json"


def build_prompt(story: dict, topic_list: List[str]) -> str:
    title = (story.get("title") or "").strip()
    content = (story.get("content") or story.get("summary") or "").strip()
    prompt = (
        "You are a topic classifier. Choose exactly ONE topic from the following list (match exactly):\n\n"
        + "\n".join(f"- {t}" for t in topic_list)
        + "\n\n"
        f"Title:\n{title}\n\nContent:\n{content}\n\n"
        "Return EXACTLY ONE topic name from the list above and nothing else."
    )
    return prompt


def call_llm_cli(prompt: str, model: str, llm_cmd: str, timeout: int = 60) -> str:
    # Quote prompt safely for shell
    quoted = shlex.quote(prompt)
    # Build command: echo 'prompt' | llm -m MODEL --temperature 0 --max-tokens 32
    cmd = f"echo {quoted} | {llm_cmd} -m {shlex.quote(model)} --temperature 0 --max-tokens 32"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"llm CLI error: {proc.stderr.strip()}")
    return proc.stdout.strip()


def normalize_choice(raw: str) -> str:
    if not raw:
        return ""
    # take first non-empty line
    for line in raw.splitlines():
        s = line.strip()
        if s:
            return s
    return raw.strip()


def pick_topic(raw: str, topic_list: List[str]) -> str:
    choice = normalize_choice(raw)
    if not choice:
        return "Other"
    # exact match (case-sensitive)
    if choice in topic_list:
        return choice
    # case-insensitive match
    for t in topic_list:
        if choice.lower() == t.lower():
            return t
    # partial match heuristics
    for t in topic_list:
        if t.lower() in choice.lower() or choice.lower() in t.lower():
            return t
    return "Other"


def classify_stories(
    stories: List[dict],
    model: str,
    llm_cmd: str,
    start: int = 0,
    limit: int = 0,
    sleep_s: float = 0.5,
) -> List[dict]:
    total = len(stories)
    end = total if limit <= 0 else min(total, start + limit)
    print(f"Processing stories {start}..{end-1} (total {total}) with model {model}")
    for i in range(start, end):
        story = stories[i]
        title = story.get("title", "")[:80]
        if story.get("topic"):
            print(f"[{i+1}/{total}] Skipping (already has topic): {title}")
            continue
        prompt = build_prompt(story, TOPIC_LIST)
        raw = ""
        for attempt in range(3):
            try:
                raw = call_llm_cli(prompt, model, llm_cmd, timeout=60)
                break
            except Exception as e:
                print(f"[{i+1}/{total}] llm call failed (attempt {attempt+1}): {e}")
                time.sleep(2 + attempt * 2)
        if not raw:
            story["topic"] = "Other"
            print(f"[{i+1}/{total}] Assigned fallback topic: Other -- {title}")
        else:
            topic = pick_topic(raw, TOPIC_LIST)
            story["topic"] = topic
            print(f"[{i+1}/{total}] Assigned topic: {topic} -- {title}")
        time.sleep(sleep_s)
    return stories


def main():
    p = argparse.ArgumentParser(description="Classify Star-Democrat stories into topics using llm CLI.")
    p.add_argument("--input", "-i", default=os.environ.get("INPUT_FILE", DEFAULT_INPUT))
    p.add_argument("--output", "-o", default=os.environ.get("OUTPUT_FILE", DEFAULT_OUTPUT))
    p.add_argument("--model", "-m", default=os.environ.get("STARD_MODEL", DEFAULT_MODEL))
    p.add_argument("--use-uv", action="store_true", help="Use 'uv run llm' wrapper")
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--sleep", type=float, default=0.5)
    args = p.parse_args()

    llm_cmd = "uv run llm" if args.use_uv else "llm"

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        raise SystemExit(1)

    with open(args.input, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        print("Input JSON must be a list of story objects.")
        raise SystemExit(1)

    classified = classify_stories(data, args.model, llm_cmd, start=args.start, limit=args.limit, sleep_s=args.sleep)

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(classified, fh, indent=2, ensure_ascii=False)

    print(f"Saved classified stories to {args.output}")


if __name__ == "__main__":
    main()
# ...existing code...
````

mgrovic: can u create this file for me?

GitHub Copilot: ````python
"""
classify_topics.py

Reads a Star-Democrat JSON file (list of story objects), uses the `llm` CLI (Groq models)
to assign exactly one topic from a fixed list to each story, and writes the enhanced
stories to `stardem_topics_classified.json`.

Usage:
  cd /workspaces/jour329w_fall2025/grovic/stardem_topics
  python classify_topics.py \
    --input stardem_sample.json \
    --output stardem_topics_classified.json \
    --model groq/meta-llama/llama-4-scout-17b-16e-instruct \
    [--use-uv] [--start 0] [--limit 0] [--sleep 0.5]

If your environment requires the `uv` wrapper, pass --use-uv or set USE_UV=1.
"""
from __future__ import annotations
import argparse
import json
import os
import shlex
import subprocess
import time
from typing import List

TOPICS: List[str] = [
    "Local Government and Policy",
    "Crime",
    "Education",
    "Religion and Culture",
    "Food, Family & Lifestyle",
    "Sports and Recreation",
    "Regional and National News",
    "Business and Development",
    "Environment and Bay Sustainability",
    "Other",
]

DEFAULT_MODEL = "groq/meta-llama/llama-4-scout-17b-16e-instruct"
DEFAULT_INPUT = "stardem_sample.json"
DEFAULT_OUTPUT = "stardem_topics_classified.json"


def build_prompt(story: dict, topics: List[str]) -> str:
    title = (story.get("title") or "").strip()
    content = (story.get("content") or story.get("summary") or story.get("body") or "").strip()
    prompt = (
        "You are a topic classifier. Choose EXACTLY ONE topic from the list below.\n\n"
        "Topics:\n"
        + "\n".join(f"- {t}" for t in topics)
        + "\n\n"
        "Instructions: Read the Title and Content. RETURN ONLY THE TOPIC NAME (exactly as it appears above) and nothing else.\n\n"
        f"Title:\n{title}\n\nContent:\n{content}\n"
    )
    # keep prompt reasonably short; if content very long, truncate
    MAX = 16000
    if len(prompt) > MAX:
        # trim content portion
        cut = MAX - 2000
        if cut < 0:
            cut = MAX
        truncated_content = content[:cut] + "\n\n[TRUNCATED]"
        prompt = prompt.split("Content:\n")[0] + "Content:\n" + truncated_content + "\n"
    return prompt


def call_llm(prompt: str, model: str, use_uv: bool = False, timeout: int = 60) -> str:
    """
    Attempt several plausible llm CLI invocations. Pass prompt via stdin.
    Returns raw text output (stdout or stderr) on success; raises RuntimeError on failure.
    """
    prefixes = (["uv", "run"] if use_uv else [])  # if use_uv, prefix with uv run
    candidates = [
        prefixes + ["llm", "complete", "--model", model],
        prefixes + ["llm", "--model", model],
        prefixes + ["llm", "text", "--model", model],
    ]
    last_err = None
    for cmd in candidates:
        try:
            proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout)
            out = (proc.stdout or "").strip()
            err = (proc.stderr or "").strip()
            if proc.returncode == 0 and out:
                return out
            if proc.returncode == 0 and err:
                return err
            last_err = (cmd, proc.returncode, out, err)
        except FileNotFoundError as e:
            last_err = (cmd, "notfound", str(e))
        except subprocess.TimeoutExpired as e:
            last_err = (cmd, "timeout", str(e))
    raise RuntimeError(f"llm CLI failed; last error: {last_err}")


def normalize_response(raw: str) -> str:
    if not raw:
        return ""
    # use first non-empty line
    for line in raw.splitlines():
        s = line.strip()
        if s:
            return s
    return raw.strip()


def pick_topic_from_response(raw: str, topics: List[str]) -> str:
    choice = normalize_response(raw)
    if not choice:
        return "Other"
    # exact match
    if choice in topics:
        return choice
    # case-insensitive match
    for t in topics:
        if choice.lower() == t.lower():
            return t
    # partial match heuristics
    for t in topics:
        if t.lower() in choice.lower() or choice.lower() in t.lower():
            return t
    return "Other"


KEYWORD_MAP = {
    "Local Government and Policy": ["county", "council", "commission", "mayor", "zoning", "board", "budget"],
    "Crime": ["shooting", "arrest", "charged", "police", "robbery", "assault", "homicide"],
    "Education": ["school", "superintendent", "students", "teacher", "curriculum", "board of education"],
    "Religion and Culture": ["church", "faith", "religion", "worship", "parish", "festival", "cultural"],
    "Food, Family & Lifestyle": ["restaurant", "food", "family", "wedding", "recipe", "lifestyle"],
    "Sports and Recreation": ["game", "match", "coach", "season", "tournament", "athlete", "sports"],
    "Regional and National News": ["federal", "national", "congress", "senate", "governor", "statewide"],
    "Business and Development": ["company", "business", "development", "project", "real estate", "economic"],
    "Environment and Bay Sustainability": ["bay", "environment", "pollution", "water quality", "conservation", "shoreline"],
}


def heuristic_topic(story: dict) -> str:
    text = " ".join(
        filter(None, [story.get("title", ""), story.get("content", ""), " ".join(story.get("tags", []) if isinstance(story.get("tags"), list) else [])])
    ).lower()
    for topic, kws in KEYWORD_MAP.items():
        for kw in kws:
            if kw in text:
                return topic
    return "Other"


def classify(input_path: str, output_path: str, model: str, use_uv: bool, start: int, limit: int, sleep_s: float):
    if not os.path.exists(input_path):
        raise SystemExit(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise SystemExit("Input JSON must be an array of story objects.")

    total = len(data)
    end = total if limit <= 0 else min(total, start + limit)

    print(f"Classifying stories {start}..{end-1} (total {total}) using model {model}")
    for i in range(start, end):
        story = data[i]
        title_preview = (story.get("title") or "")[:80].replace("\n", " ")
        if story.get("topic"):
            print(f"[{i+1}/{total}] SKIP (already has topic): {title_preview}")
            continue

        prompt = build_prompt(story, TOPICS)
        raw = None
        # try LLM with retries
        for attempt in range(3):
            try:
                raw = call_llm(prompt, model, use_uv=use_uv, timeout=60)
                break
            except Exception as e:
                print(f"[{i+1}/{total}] llm attempt {attempt+1} failed: {e}")
                time.sleep(2 + attempt * 2)
        if not raw:
            # fallback heuristic
            topic = heuristic_topic(story)
            print(f"[{i+1}/{total}] Fallback assigned topic: {topic} -- {title_preview}")
            story["topic"] = topic
        else:
            topic = pick_topic_from_response(raw, TOPICS)
            if topic == "Other":
                # try heuristic if LLM returned unusable answer
                h = heuristic_topic(story)
                if h != "Other":
                    topic = h
            story["topic"] = topic
            print(f"[{i+1}/{total}] Assigned topic: {topic} -- {title_preview}")

        # small pause to avoid throttling
        time.sleep(sleep_s)

    # Save output
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    print(f"Saved classified stories to {output_path}")


def cli():
    p = argparse.ArgumentParser(description="Classify Star-Democrat stories into topics using the llm CLI.")
    p.add_argument("--input", "-i", default=os.environ.get("INPUT_FILE", DEFAULT_INPUT))
    p.add_argument("--output", "-o", default=os.environ.get("OUTPUT_FILE", DEFAULT_OUTPUT))
    p.add_argument("--model", "-m", default=os.environ.get("STARD_MODEL", DEFAULT_MODEL))
    p.add_argument("--use-uv", action="store_true", help="Use 'uv run llm' wrapper")
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--limit", type=int, default=0, help="Max number to process (0 = all)")
    p.add_argument("--sleep", type=float, default=0.5, help="Seconds to sleep between LLM calls")
    args = p.parse_args()

    classify(args.input, args.output, args.model, args.use_uv, args.start, args.limit, args.sleep)


if __name__ == "__main__":
    cli()
````

mgrovic: what do i do know

GitHub Copilot: GitHub Copilot

Here’s what to do next:

1) Go to your project folder
```bash
cd /workspaces/jour329w_fall2025/grovic/stardem_topics
ls -l
```
Make sure classify_topics.py and stardem_sample.json are here.

2) Install and configure llm (Groq)
```bash
uv run llm install llm-groq
uv run llm keys get groq || uv run llm keys set groq
```

3) Quick model test (optional)
```bash
echo "Say hi" | uv run llm -m groq/meta-llama/llama-4-scout-17b-16e-instruct
```

4) Run a small test batch
```bash
uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct --input stardem_sample.json --output stardem_topics_classified.json --limit 5
uv run jq '.[0:5] | .[] | {title, topic}' stardem_topics_classified.json
```

5) Run the full classification
```bash
uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct --input stardem_sample.json --output stardem_topics_classified.json
```

6) Explore results with Datasette
```bash
uv run sqlite-utils insert stardem_topics.db stories stardem_topics_classified.json --pk id || uv run sqlite-utils insert stardem_topics.db stories stardem_topics_classified.json
uv run datasette stardem_topics.db
```
Then open the forwarded port (Ports tab → globe) or use:
```bash
$BROWSER http://localhost:8001
```

If you hit errors, paste the terminal output and I’ll troubleshoot fast.

mgrovic: /workspaces/jour329w_fall2025/.venv/bin/python3: can't open file '/workspaces/jour329w_fall2025/classify_topics.py': [Errno 2] No such file or directory

GitHub Copilot: GitHub Copilot

You ran the script from the wrong path. The file is here:
- /workspaces/jour329w_fall2025/grovic/stardem_topics/classify_topics.py

Do this in the terminal:

```bash
# go to the script folder
cd /workspaces/jour329w_fall2025/grovic/stardem_topics
ls -l  # should show classify_topics.py and stardem_sample.json

# ensure llm + Groq are set up
uv run llm install llm-groq
uv run llm keys get groq || uv run llm keys set groq

# quick test on a few stories
uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct --input stardem_sample.json --output stardem_topics_classified.json --limit 5

# full run
uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct --input stardem_sample.json --output stardem_topics_classified.json
```

From workspace root (alternative):

```bash
uv run python grovic/stardem_topics/classify_topics.py --use-uv --input grovic/stardem_topics/stardem_sample.json --output grovic/stardem_topics/stardem_topics_classified.json
```

When done, the output will be saved to stardem_topics_classified.json in the same folder.

mgrovic: can't open file '/workspaces/jour329w_fall2025/grovic/stardem_topics/classify_topics.py': [Errno 2] No such file or directory

GitHub Copilot: GitHub Copilot

I created the script at the correct path. Run it from that folder.

````python
"""
Classify Star-Democrat stories into topics using the `llm` CLI (Groq models).
Reads stardem_sample.json and writes stardem_topics_classified.json.

Usage:
  cd /workspaces/jour329w_fall2025/grovic/stardem_topics
  uv run llm install llm-groq
  uv run llm keys get groq || uv run llm keys set groq
  uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct
"""
from __future__ import annotations
import argparse
import json
import os
import shlex
import subprocess
import time
from typing import List

TOPICS: List[str] = [
    "Local Government and Policy",
    "Crime",
    "Education",
    "Religion and Culture",
    "Food, Family & Lifestyle",
    "Sports and Recreation",
    "Regional and National News",
    "Business and Development",
    "Environment and Bay Sustainability",
    "Other",
]

DEFAULT_INPUT = "stardem_sample.json"
DEFAULT_OUTPUT = "stardem_topics_classified.json"
DEFAULT_MODEL = "groq/meta-llama/llama-4-scout-17b-16e-instruct"


def build_prompt(story: dict, topics: List[str]) -> str:
    title = (story.get("title") or "").strip()
    content = (story.get("content") or story.get("summary") or story.get("body") or "").strip()
    prompt = (
        "Assign this news story to EXACTLY ONE topic from the list below.\n"
        "Return ONLY the topic name exactly as written.\n\n"
        "Topics:\n" + "\n".join(f"- {t}" for t in topics) + "\n\n"
        f"Title:\n{title}\n\nContent:\n{content}\n"
    )
    # truncate very long prompts
    MAX = 16000
    if len(prompt) > MAX:
        cut = max(2000, MAX - 4000)
        prompt = prompt[:cut] + "\n\n[TRUNCATED]\n"
    return prompt


def call_llm(prompt: str, model: str, use_uv: bool = False, timeout: int = 60) -> str:
    """
    Call the `llm` CLI (optionally via `uv run`) with prompt on stdin.
    Tries a few common subcommands for compatibility.
    """
    prefix = ["uv", "run"] if use_uv else []
    candidates = [
        prefix + ["llm", "complete", "--model", model, "--temperature", "0", "--max-tokens", "24"],
        prefix + ["llm", "--model", model, "--temperature", "0", "--max-tokens", "24"],
        prefix + ["llm", "text", "--model", model],
    ]
    last_err = None
    for cmd in candidates:
        try:
            proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout)
            out = (proc.stdout or "").strip()
            err = (proc.stderr or "").strip()
            if proc.returncode == 0 and out:
                return out
            if proc.returncode == 0 and err:
                return err
            last_err = (cmd, proc.returncode, err)
        except FileNotFoundError as e:
            last_err = (cmd, "notfound", str(e))
        except subprocess.TimeoutExpired as e:
            last_err = (cmd, "timeout", str(e))
    raise RuntimeError(f"llm CLI failed; last error: {last_err}")


def normalize_choice(raw: str) -> str:
    if not raw:
        return ""
    for line in raw.splitlines():
        s = line.strip()
        if s:
            return s
    return raw.strip()


def choose_topic(raw: str, topics: List[str]) -> str:
    choice = normalize_choice(raw)
    if not choice:
        return "Other"
    if choice in topics:
        return choice
    for t in topics:
        if choice.lower() == t.lower():
            return t
    for t in topics:
        if t.lower() in choice.lower() or choice.lower() in t.lower():
            return t
    return "Other"


KEYWORD_MAP = {
    "Local Government and Policy": ["county", "council", "commission", "commissioners", "mayor", "zoning", "budget", "ordinance"],
    "Crime": ["shooting", "arrest", "charged", "police", "robbery", "assault", "homicide", "theft"],
    "Education": ["school", "students", "teacher", "superintendent", "curriculum", "board of education"],
    "Religion and Culture": ["church", "faith", "religion", "worship", "parish", "festival", "cultural"],
    "Food, Family & Lifestyle": ["restaurant", "food", "family", "recipe", "lifestyle", "dining"],
    "Sports and Recreation": ["game", "match", "coach", "season", "tournament", "athlete", "sports"],
    "Regional and National News": ["federal", "national", "congress", "senate", "governor", "statewide"],
    "Business and Development": ["company", "business", "development", "project", "real estate", "economic", "employer"],
    "Environment and Bay Sustainability": ["bay", "environment", "pollution", "water quality", "conservation", "shoreline", "habitat"],
}


def heuristic_topic(story: dict) -> str:
    tags = story.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    text = " ".join([story.get("title", ""), story.get("content", ""), " ".join(tags)]).lower()
    for topic, kws in KEYWORD_MAP.items():
        for kw in kws:
            if kw in text:
                return topic
    return "Other"


def classify_list(
    stories: List[dict],
    model: str,
    use_uv: bool,
    start: int,
    limit: int,
    sleep_s: float,
) -> List[dict]:
    total = len(stories)
    end = total if limit <= 0 else min(total, start + limit)
    print(f"Processing {start}..{end-1} of {total} with model: {model}")
    for i in range(start, end):
        story = stories[i]
        title_preview = (story.get("title") or "")[:80].replace("\n", " ")
        if story.get("topic"):
            print(f"[{i+1}/{total}] Skip (already has topic): {title_preview}")
            continue
        prompt = build_prompt(story, TOPICS)
        raw = ""
        for attempt in range(3):
            try:
                raw = call_llm(prompt, model, use_uv=use_uv, timeout=60)
                break
            except Exception as e:
                print(f"[{i+1}/{total}] llm failed (attempt {attempt+1}): {e}")
                time.sleep(2 + attempt * 2)
        if not raw:
            topic = heuristic_topic(story)
            story["topic"] = topic
            print(f"[{i+1}/{total}] Heuristic topic: {topic} -- {title_preview}")
        else:
            topic = choose_topic(raw, TOPICS)
            if topic == "Other":
                ht = heuristic_topic(story)
                if ht != "Other":
                    topic = ht
            story["topic"] = topic
            print(f"[{i+1}/{total}] Topic: {topic} -- {title_preview}")
        time.sleep(sleep_s)
    return stories


def main():
    ap = argparse.ArgumentParser(description="Classify Star-Democrat stories into topics using llm CLI (Groq).")
    ap.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Input JSON file (list of stories).")
    ap.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Output JSON file.")
    ap.add_argument("--model", "-m", default=os.environ.get("STARD_MODEL", DEFAULT_MODEL), help="LLM model for `llm` CLI.")
    ap.add_argument("--use-uv", action="store_true", help="Use `uv run llm` wrapper.")
    ap.add_argument("--start", type=int, default=0, help="Start index.")
    ap.add_argument("--limit", type=int, default=0, help="Max items to process (0=all).")
    ap.add_argument("--sleep", type=float, default=0.5, help="Seconds to sleep between calls.")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"Input not found: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        stories = json.load(f)
    if not isinstance(stories, list):
        raise SystemExit("Input JSON must be a list of story objects.")

    updated = classify_list(stories, args.model, args.use_uv, args.start, args.limit, args.sleep)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
    print(f"Saved classified stories to {args.output}")


if __name__ == "__main__":
    main()
````

Run it:
```bash
cd /workspaces/jour329w_fall2025/grovic/stardem_topics
uv run llm install llm-groq
uv run llm keys get groq || uv run llm keys set groq
uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct
```

Open the output:
```bash
uv run jq '.[0:5] | .[] | {title, topic}' stardem_topics_classified.json
```

mgrovic: Requirement already satisfied: llm-groq in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (0.9)
Requirement already satisfied: llm>=0.18 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm-groq) (0.27.1)
Requirement already satisfied: groq in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm-groq) (0.31.1)
Requirement already satisfied: click in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (8.3.0)
Requirement already satisfied: condense-json>=0.1.3 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (0.1.3)
Requirement already satisfied: openai>=1.55.3 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (1.108.1)
Requirement already satisfied: click-default-group>=1.2.3 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (1.2.4)
Requirement already satisfied: sqlite-utils>=3.37 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (3.38)
Requirement already satisfied: sqlite-migrate>=0.1a2 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (0.1b0)
Requirement already satisfied: pydantic>=2.0.0 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (2.11.9)
Requirement already satisfied: PyYAML in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (6.0.2)
Requirement already satisfied: pluggy in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (1.6.0)
Requirement already satisfied: python-ulid in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (3.1.0)
Requirement already satisfied: setuptools in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (80.9.0)
Requirement already satisfied: pip in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (25.2)
Requirement already satisfied: puremagic in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from llm>=0.18->llm-groq) (1.30)
Requirement already satisfied: anyio<5,>=3.5.0 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from openai>=1.55.3->llm>=0.18->llm-groq) (4.10.0)
Requirement already satisfied: distro<2,>=1.7.0 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from openai>=1.55.3->llm>=0.18->llm-groq) (1.9.0)
Requirement already satisfied: httpx<1,>=0.23.0 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from openai>=1.55.3->llm>=0.18->llm-groq) (0.28.1)
Requirement already satisfied: jiter<1,>=0.4.0 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from openai>=1.55.3->llm>=0.18->llm-groq) (0.11.0)
Requirement already satisfied: sniffio in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from openai>=1.55.3->llm>=0.18->llm-groq) (1.3.1)
Requirement already satisfied: tqdm>4 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from openai>=1.55.3->llm>=0.18->llm-groq) (4.67.1)
Requirement already satisfied: typing-extensions<5,>=4.11 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from openai>=1.55.3->llm>=0.18->llm-groq) (4.15.0)
Requirement already satisfied: idna>=2.8 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from anyio<5,>=3.5.0->openai>=1.55.3->llm>=0.18->llm-groq) (3.10)
Requirement already satisfied: certifi in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from httpx<1,>=0.23.0->openai>=1.55.3->llm>=0.18->llm-groq) (2025.8.3)
Requirement already satisfied: httpcore==1.* in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from httpx<1,>=0.23.0->openai>=1.55.3->llm>=0.18->llm-groq) (1.0.9)
Requirement already satisfied: h11>=0.16 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from httpcore==1.*->httpx<1,>=0.23.0->openai>=1.55.3->llm>=0.18->llm-groq) (0.16.0)
Requirement already satisfied: annotated-types>=0.6.0 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from pydantic>=2.0.0->llm>=0.18->llm-groq) (0.7.0)
Requirement already satisfied: pydantic-core==2.33.2 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from pydantic>=2.0.0->llm>=0.18->llm-groq) (2.33.2)
Requirement already satisfied: typing-inspection>=0.4.0 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from pydantic>=2.0.0->llm>=0.18->llm-groq) (0.4.1)
Requirement already satisfied: sqlite-fts4 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from sqlite-utils>=3.37->llm>=0.18->llm-groq) (1.0.3)
Requirement already satisfied: tabulate in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from sqlite-utils>=3.37->llm>=0.18->llm-groq) (0.9.0)
Requirement already satisfied: python-dateutil in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from sqlite-utils>=3.37->llm>=0.18->llm-groq) (2.9.0.post0)
Requirement already satisfied: six>=1.5 in /workspaces/jour329w_fall2025/.venv/lib/python3.12/site-packages (from python-dateutil->sqlite-utils>=3.37->llm>=0.18->llm-groq) (1.17.0)
redacted
/workspaces/jour329w_fall2025/.venv/bin/python3: can't open file '/workspaces/jour329w_fall2025/grovic/stardem_topics/classify_topics.py': [Errno 2] No such file or directory

GitHub Copilot: GitHub Copilot

I’ll create the script at the correct path and ready to run.

````python
"""
Classify Star-Democrat stories into topics using the `llm` CLI (Groq models).
Reads stardem_sample.json and writes stardem_topics_classified.json.

Usage (from this folder):
  cd /workspaces/jour329w_fall2025/grovic/stardem_topics
  uv run llm install llm-groq
  uv run llm keys get groq || uv run llm keys set groq
  uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import time
from typing import List

TOPICS: List[str] = [
    "Local Government and Policy",
    "Crime",
    "Education",
    "Religion and Culture",
    "Food, Family & Lifestyle",
    "Sports and Recreation",
    "Regional and National News",
    "Business and Development",
    "Environment and Bay Sustainability",
    "Other",
]

DEFAULT_INPUT = "stardem_sample.json"
DEFAULT_OUTPUT = "stardem_topics_classified.json"
DEFAULT_MODEL = "groq/meta-llama/llama-4-scout-17b-16e-instruct"


def build_prompt(story: dict, topics: List[str]) -> str:
    title = (story.get("title") or "").strip()
    content = (story.get("content") or story.get("summary") or story.get("body") or "").strip()
    prompt = (
        "Assign this news story to EXACTLY ONE topic from the list below.\n"
        "Return ONLY the topic name exactly as written.\n\n"
        "Topics:\n" + "\n".join(f"- {t}" for t in topics) + "\n\n"
        f"Title:\n{title}\n\nContent:\n{content}\n"
    )
    # Truncate extremely long content
    if len(prompt) > 18000:
        keep = 16000
        head = prompt[:keep]
        prompt = head + "\n\n[TRUNCATED]\n"
    return prompt


def call_llm(prompt: str, model: str, use_uv: bool = False, timeout: int = 60) -> str:
    """
    Call the `llm` CLI (optionally via `uv run`) with the prompt on stdin.
    Try a few subcommands for compatibility.
    """
    base = ["uv", "run"] if use_uv else []
    candidates = [
        base + ["llm", "complete", "--model", model, "--temperature", "0", "--max-tokens", "24"],
        base + ["llm", "--model", model, "--temperature", "0", "--max-tokens", "24"],
        base + ["llm", "text", "--model", model],
    ]
    last_err = None
    for cmd in candidates:
        try:
            proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout)
            out = (proc.stdout or "").strip()
            err = (proc.stderr or "").strip()
            if proc.returncode == 0 and out:
                return out
            if proc.returncode == 0 and err:
                return err
            last_err = (cmd, proc.returncode, err)
        except FileNotFoundError as e:
            last_err = (cmd, "notfound", str(e))
        except subprocess.TimeoutExpired as e:
            last_err = (cmd, "timeout", str(e))
    raise RuntimeError(f"llm CLI failed; last error: {last_err}")


def normalize_choice(raw: str) -> str:
    if not raw:
        return ""
    for line in raw.splitlines():
        s = line.strip()
        if s:
            return s
    return raw.strip()


def choose_topic(raw: str, topics: List[str]) -> str:
    choice = normalize_choice(raw)
    if not choice:
        return "Other"
    if choice in topics:
        return choice
    for t in topics:
        if choice.lower() == t.lower():
            return t
    for t in topics:
        if t.lower() in choice.lower() or choice.lower() in t.lower():
            return t
    return "Other"


def classify_list(
    stories: List[dict],
    model: str,
    use_uv: bool,
    start: int,
    limit: int,
    sleep_s: float,
) -> List[dict]:
    total = len(stories)
    end = total if limit <= 0 else min(total, start + limit)
    print(f"Processing {start}..{end-1} of {total} with model: {model}")
    for i in range(start, end):
        story = stories[i]
        title_preview = (story.get("title") or "")[:80].replace("\n", " ")
        if story.get("topic"):
            print(f"[{i+1}/{total}] Skip (already has topic): {title_preview}")
            continue
        prompt = build_prompt(story, TOPICS)
        raw = ""
        for attempt in range(3):
            try:
                raw = call_llm(prompt, model, use_uv=use_uv, timeout=60)
                break
            except Exception as e:
                print(f"[{i+1}/{total}] llm failed (attempt {attempt+1}): {e}")
                time.sleep(2 + attempt * 2)
        topic = choose_topic(raw, TOPICS) if raw else "Other"
        story["topic"] = topic
        print(f"[{i+1}/{total}] Topic: {topic} -- {title_preview}")
        time.sleep(sleep_s)
    return stories


def main():
    ap = argparse.ArgumentParser(description="Classify Star-Democrat stories into topics using the llm CLI (Groq).")
    ap.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Input JSON file (list of stories).")
    ap.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Output JSON file.")
    ap.add_argument("--model", "-m", default=os.environ.get("STARD_MODEL", DEFAULT_MODEL), help="LLM model for `llm` CLI.")
    ap.add_argument("--use-uv", action="store_true", help="Use `uv run llm` wrapper.")
    ap.add_argument("--start", type=int, default=0, help="Start index.")
    ap.add_argument("--limit", type=int, default=0, help="Max items to process (0=all).")
    ap.add_argument("--sleep", type=float, default=0.5, help="Seconds to sleep between calls.")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"Input not found: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        stories = json.load(f)
    if not isinstance(stories, list):
        raise SystemExit("Input JSON must be a list of story objects.")

    updated = classify_list(stories, args.model, args.use_uv, args.start, args.limit, args.sleep)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
    print(f"Saved classified stories to {args.output}")


if __name__ == "__main__":
    main()
````

Run it:
```bash
# ensure folder exists and run from there
mkdir -p /workspaces/jour329w_fall2025/grovic/stardem_topics
cd /workspaces/jour329w_fall2025/grovic/stardem_topics

# make sure stardem_sample.json is here
ls -l stardem_sample.json

# Groq plugin and key (you already have them)
uv run llm install llm-groq
uv run llm keys get groq || uv run llm keys set groq

# classify (first 5 to test)
uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct --limit 5

# full run
uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct
```

mgrovic: 

Your script should:
- Use the `llm` command-line tool with an appropriate Groq model (e.g., `groq/meta-llama/llama-4-scout-17b-16e-instruct` or `groq-kimi-k2` or `groq/meta-llama/llama-4-maverick-17b-128e-instruct`)
- Process each story and add a `topic` field
- Save the enhanced stories to `stardem_topics_classified.json`
- Print progress as it processes stories

**Tip**: Have the script use subprocess to call the `llm` command. You should provide this document (`stardem_topics.md`) as a reference.

Workspace: Enable Grok Code Fast 1 for all clients
[object Object]

mgrovic: @workspace /new Enable: "Enable Grok Code Fast 1 for all clients"

Workspace: Sure, here is the file you requested:[classify_topics.py](command:github.copilot.openFile?%5B%7B%22value%22%3A%5B%7B%22name%22%3A%22classify_topics.py%22%7D%5D%2C%22baseUri%22%3A%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fclassify_topics.py%22%2C%22scheme%22%3A%22vscode-copilot-file%22%2C%22authority%22%3A%224473d31c-0e6b-4709-853c-bbd01b27eb8b%22%7D%7D%5D)

Create File...

mgrovic: Your script should provide your topic list and ask the LLM to:
- Choose the single best-fitting topic from your list
- Make sure your list has an option for "Other" or "None" if it's not exhaustive

Example prompt structure:
```python
topic_list = ["Local Government", "Education", "Public Safety", ...]  # Your list

prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {story['title']}
Content: {story['content']}

Return only the topic name from the list above.
"""
```

#### Script Requirements:

Your script should:
- Use the `llm` command-line tool with an appropriate Groq model (e.g., `groq/meta-llama/llama-4-scout-17b-16e-instruct` or `groq-kimi-k2` or `groq/meta-llama/llama-4-maverick-17b-128e-instruct`)
- Process each story and add a `topic` field
- Save the enhanced stories to `stardem_topics_classified.json`
- Print progress as it processes stories

**Tip**: Have the script use subprocess to call the `llm` command. You should provide this document (`stardem_topics.md`) as a reference.

Workspace: It looks like you may not have tests set up in this repository yet.
[object Object]

mgrovic: @workspace /tests Accept: "It looks like you may not have tests set up in this repository yet."

Workspace: 

mgrovic: @workspace /setupTests

Workspace: Because this workspace includes Python scripts (e.g., in utils and the task involving `classify_topics.py`) alongside JavaScript/React applications (e.g., with `vite.config.js` and package.json files), testing frameworks should cover both languages. For Python, pytest is preferred for its simplicity and extensibility over unittest. For JavaScript, Vitest is ideal for Vite-based projects due to its speed and integration, while Jest is a solid alternative for broader React testing.



Pick a testing framework
[object Object]

mgrovic: @workspace /setupTests pytest: "Pick a testing framework"

Workspace: Let's set up pytest in your workspace by creating a basic test file and installing the framework.



Apply Changes



To install pytest, run the following command in your terminal:
```sh
pip install pytest
```

You can run your tests with the following command:
```sh
pytest
```

To enable rich UI integration in VS Code, confirm your Python testing framework to enable test discovery.

Configure Test Framework

mgrovic: @workspace /setupTests Your script should provide your topic list and ask the LLM to:
- Choose the single best-fitting topic from your list
- Make sure your list has an option for "Other" or "None" if it's not exhaustive

Example prompt structure:
```python
topic_list = ["Local Government", "Education", "Public Safety", ...]  # Your list

prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {story['title']}
Content: {story['content']}

Return only the topic name from the list above.
"""
```

#### Script Requirements:

Your script should:
- Use the `llm` command-line tool with an appropriate Groq model (e.g., `groq/meta-llama/llama-4-scout-17b-16e-instruct` or `groq-kimi-k2` or `groq/meta-llama/llama-4-maverick-17b-128e-instruct`)
- Process each story and add a `topic` field
- Save the enhanced stories to `stardem_topics_classified.json`
- Print progress as it processes stories

**Tip**: Have the script use subprocess to call the `llm` command. You should provide this document (`stardem_topics.md`) as a reference.

Workspace: Let's create a basic test file to get you started with pytest, matching the existing naming convention in your tests directory:



Apply Changes



Then, we'll need to install pytest in your workspace:
```sh
uv add --dev pytest
```

Finally, you can run your tests with the following command:
```sh
uv run pytest
```

mgrovic: 
Your script should provide your topic list and ask the LLM to:
- Choose the single best-fitting topic from your list
- Make sure your list has an option for "Other" or "None" if it's not exhaustive

Example prompt structure:
```python
topic_list = ["Local Government", "Education", "Public Safety", ...]  # Your list

prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {story['title']}
Content: {story['content']}

Return only the topic name from the list above.
"""
```

#### Script Requirements:

Your script should:
- Use the `llm` command-line tool with an appropriate Groq model (e.g., `groq/meta-llama/llama-4-scout-17b-16e-instruct` or `groq-kimi-k2` or `groq/meta-llama/llama-4-maverick-17b-128e-instruct`)
- Process each story and add a `topic` field
- Save the enhanced stories to `stardem_topics_classified.json`
- Print progress as it processes stories

**Tip**: Have the script use subprocess to call the `llm` command. You should provide this document (`stardem_topics.md`) as a reference.

Workspace: ```python
import unittest
from unittest.mock import patch, MagicMock

class TestClassifyTopics(unittest.TestCase):
    def test_topic_list(self):
        topic_list = ["Local Government", "Education", "Public Safety", "Business", "Agriculture", "Environment", "Community", "Sports", "Development", "Other"]
        self.assertIn("Local Government", topic_list)
        self.assertIn("Other", topic_list)
        self.assertEqual(len(topic_list), 10)

    @patch('subprocess.run')
    def test_process_story(self, mock_run):
        mock_run.return_value = MagicMock(stdout='Local Government')
        story = {'title': 'City Council Meeting', 'content': 'The city council met to discuss local issues.'}
        
        topic_list = ["Local Government", "Education", "Public Safety", "Business", "Agriculture", "Environment", "Community", "Sports", "Development", "Other"]
        prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {story['title']}
Content: {story['content']}

Return only the topic name from the list above.
"""
        
        # Simulate calling the llm command
        assigned_topic = mock_run(prompt)
        
        self.assertEqual(assigned_topic.stdout.strip(), 'Local Government')
        self.assertIn(assigned_topic.stdout.strip(), topic_list)

    @patch('subprocess.run')
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open', new_callable=MagicMock)
    def test_classify_stories_full(self, mock_open, mock_load, mock_dump, mock_run):
        # Mock stories
        stories = [
            {'title': 'City Council Meeting', 'content': 'The city council met to discuss local issues.'}
        ]
        mock_load.return_value = stories
        mock_run.return_value = MagicMock(stdout='Local Government')
        
        # Mock file handles
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Simulate the script logic
        topic_list = ["Local Government", "Education", "Public Safety", "Business", "Agriculture", "Environment", "Community", "Sports", "Development", "Other"]
        for story in stories:
            prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {story['title']}
Content: {story['content']}

Return only the topic name from the list above.
"""
            result = mock_run(['llm', '-m', 'groq/meta-llama/llama-4-scout-17b-16e-instruct', prompt], capture_output=True, text=True, check=True)
            story['topic'] = result.stdout.strip()
        
        # Check that dump was called with updated stories
        mock_dump.assert_called_once_with(stories, mock_file, indent=2)

if __name__ == '__main__':
    unittest.main()
```
```json
{
  "fileName": "assignments/test_stardem_topics.py"
}
```

mgrovic: how do i run it

GitHub Copilot: ```bash
cd /workspaces/jour329w_fall2025/grovic/stardem_topics
python code.py
```

mgrovic: Your script should provide your topic list and ask the LLM to:
- Choose the single best-fitting topic from your list
- Make sure your list has an option for "Other" or "None" if it's not exhaustive

Example prompt structure:
```python
topic_list = ["Local Government", "Education", "Public Safety", ...]  # Your list

prompt = f"""
Assign this news story to exactly ONE topic from the following list:
{', '.join(topic_list)}

Choose the topic that best represents what this story is primarily about.

Title: {story['title']}
Content: {story['content']}

Return only the topic name from the list above.
"""
```

#### Script Requirements:

Your script should:
- Use the `llm` command-line tool with an appropriate Groq model (e.g., `groq/meta-llama/llama-4-scout-17b-16e-instruct` or `groq-kimi-k2` or `groq/meta-llama/llama-4-maverick-17b-128e-instruct`)
- Process each story and add a `topic` field
- Save the enhanced stories to `stardem_topics_classified.json`
- Print progress as it processes stories

**Tip**: Have the script use subprocess to call the `llm` command. You should provide this document (`stardem_topics.md`) as a reference. should this be two scripts or one

GitHub Copilot: One script with a switch is best. Add a --mode flag to support both “LLM decides” and “You provide the list.”

Here’s a single script that does both.

````python
import argparse, json, os, subprocess, shlex, time
from typing import List

DEFAULT_INPUT = "stardem_sample.json"
DEFAULT_OUTPUT = "stardem_topics_classified.json"
DEFAULT_MODEL = "groq/meta-llama/llama-4-scout-17b-16e-instruct"

DEFAULT_TOPICS = [
    "Local Government and Policy",
    "Crime",
    "Education",
    "Religion and Culture",
    "Food, Family & Lifestyle",
    "Sports and Recreation",
    "Regional and National News",
    "Business and Development",
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
    cmd = f"echo {quoted} | {runner} -m {shlex.quote(model)} --temperature 0 --max-tokens 24"
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
````

Run it:
- Option 2 (You decide – pick from your list)
```bash
cd /workspaces/jour329w_fall2025/grovic/stardem_topics
uv run python classify_topics.py --use-uv --mode list --model groq/meta-llama/llama-4-scout-17b-16e-instruct
```

- Option 1 (LLM decides topics)
```bash
cd /workspaces/jour329w_fall2025/grovic/stardem_topics
uv run python classify_topics.py --use-uv --mode llm --model groq/meta-llama/llama-4-scout-17b-16e-instruct
```

- Custom topic list file
```bash
# topics.txt: one topic per line (include Other)
uv run python classify_topics.py --use-uv --mode list --topics-file topics.txt
```

mgrovic: no flag max token or tempature

GitHub Copilot: GitHub Copilot

You want no max-tokens or temperature flags. I updated the llm call to only pass the model.

````python
# ...existing code...
def call_llm(prompt: str, model: str, use_uv: bool, timeout: int = 60) -> str:
    quoted = shlex.quote(prompt)
    runner = "uv run llm" if use_uv else "llm"
    # no --max-tokens, no --temperature
    cmd = f"echo {quoted} | {runner} -m {shlex.quote(model)}"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "llm call failed")
    return (proc.stdout or "").strip() or (proc.stderr or "").strip()
# ...existing code...
````

Run it:
```bash
cd /workspaces/jour329w_fall2025/grovic/stardem_topics
uv run python classify_topics.py --use-uv --model groq/meta-llama/llama-4-scout-17b-16e-instruct
```