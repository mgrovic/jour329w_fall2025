# CNS Collections

Beat reporting is the backbone of journalism - reporters who specialize in covering specific topics, institutions, or geographic areas over time. Capital News Service has covered many beats over the years, from Maryland state politics to environmental issues to local government.

### Getting Started

What we're going to do is create a collection of stories from a specific beat, add structured metadata, and use AI embeddings to understand the patterns and relationships within that coverage. This will help you see how beat reporting should create a network of stories, sources, and themes.

1. In the Terminal, cd into the directory with your last name.
2. Create a directory called cns_collections using mkdir
3. cd into that new directory
4. Create a file called notes.md using touch. Keep that file open.
5. Open that document and put "CNS Collections - [Your Beat Name]" and today's date at the top, then save it
6. Do cd .. twice to get back to the main directory (/workspaces/jour329w_fall2025)
7. In the Terminal, do the git add, commit, pull and push your changes as described in the `setup.md` file.

### Setup

Install the llm-anthropic plugin and set your Claude API key value if you haven't already.

```bash
uv run llm install llm-anthropic
# check to see if you have the key set
uv run llm keys
# if not, set it
uv run llm keys set anthropic
```

### Choose Your Beat

First, you need to pick a topic to focus on. Let's look at the available topics:

```bash
# See the available topic categories
cat data/topics.csv
```

### Find Your Stories

Now you need to identify and collect stories from your chosen beat using the `story_summaries.json` file. Each story in this file has a `topic` field that corresponds to one of the topics from `topics.csv`.

First, let's see what topics are available and how many stories are in each:

```bash
# Count stories by topic
uv run sqlite-utils memory data/story_summaries.json \
  "SELECT topic, COUNT(*) as story_count 
   FROM story_summaries 
   GROUP BY topic 
   ORDER BY story_count DESC" --csv
```

Choose a topic from the list that has a good number of stories (aim for at least 50). Then query for all stories in that topic and save them to a JSON file named after your topic. Use this as a template:

```bash
# Save all stories for your chosen topic
# Replace 'Elections' with your actual topic name as it appears in the data
uv run sqlite-utils memory data/story_summaries.json \
  "SELECT * FROM story_summaries 
   WHERE topic = 'Elections'" \
  --json-cols > story_summaries_elections.json
```

**Examples for other topics:**

```bash
# For Maryland Government & Politics:
uv run sqlite-utils memory data/story_summaries.json \
  "SELECT * FROM story_summaries 
   WHERE topic = 'Maryland Government & Politics'" \
  --json-cols > story_summaries_maryland_government_politics.json

# For Education:
uv run sqlite-utils memory data/story_summaries.json \
  "SELECT * FROM story_summaries 
   WHERE topic = 'Education'" \
  --json-cols > story_summaries_education.json

# For Baltimore:
uv run sqlite-utils memory data/story_summaries.json \
  "SELECT * FROM story_summaries 
   WHERE topic = 'Baltimore'" \
  --json-cols > story_summaries_baltimore.json
```

Verify your results:

```bash
# Check how many stories you got
uv run jq 'length' story_summaries_elections.json

```

Document in `notes.md`:
- What topic did you choose?
- How many stories are in your topic?

### Design Your Metadata Schema

Since the `story_summaries.json` file already had AI-generated summaries, you'll enhance these stories with beat-specific metadata. Design a consistent schema that will help you understand your beat's ecosystem:

**Required Fields (all beats should have these):**
- **people**: Array of key people mentioned (names only)
- **geographic_focus**: Primary location (county, city, region, or "statewide")
- **key_institutions**: Organizations, agencies, companies involved

You should add any other metadata that you think would be useful. Be sure to describe what and why in `notes.md`.

### Add Metadata with LLM Assistance

Now you'll use the LLM to help extract and standardize metadata from the story summaries and titles. Create a Python script called `add_metadata.py`:

```bash
touch add_metadata.py
```

And paste the following in it:

```python
import json
import subprocess
import time
from pathlib import Path

def extract_metadata(story_title, story_content, schema_prompt):
    """Use LLM to extract structured metadata from story title and summary."""
    prompt = f"""
Extract metadata from this news story in JSON format using only the title and summary provided.

Schema to follow:
{schema_prompt}

Story Title: {story_title}
Story Summary: {story_content}

Return only valid JSON with the metadata. If information is not available, use an empty array:
"""
    
    try:
        result = subprocess.run([
            'llm', '-m', 'groq/qwen/qwen3-32b', prompt
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Parse and validate the JSON response
            response_text = result.stdout.strip()
            # Remove any markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('\n', 1)[0]
            
            metadata = json.loads(response_text)
            return metadata
        else:
            return {"error": "LLM failed", "stderr": result.stderr}
    except Exception as e:
        return {"error": str(e)}

# Load your beat stories - UPDATE THE FILENAME to match your topic!
# Example: 'story_summaries_environment.json' or 'story_summaries_government_politics.json'
with open('story_summaries_environment.json') as f:  # CHANGE THIS FILENAME
    stories = json.load(f)

# Define your schema prompt based on your beat - CUSTOMIZE THIS!
schema_prompt = """
{
  "people": ["Person Name 1", "Person Name 2"],
  "geographic_focus": "Baltimore City",
  "key_institutions": ["Maryland General Assembly", "Department of Environment"],
  "beat_specific_field": "value"
}
"""

# Process each story
enhanced_stories = []
for i, story in enumerate(stories):
    print(f"Processing {i+1}/{len(stories)}: {story['title']}")
    
    metadata = extract_metadata(story['title'], story['summary'], schema_prompt)
    
    # Add metadata to story
    enhanced_story = story.copy()
    enhanced_story['metadata'] = metadata
    enhanced_stories.append(enhanced_story)
    
    # Be respectful to the API
    time.sleep(1)

# Save the enhanced collection
with open('enhanced_beat_stories.json', 'w') as f:
    json.dump(enhanced_stories, f, indent=2)

print(f"Processed {len(enhanced_stories)} stories with metadata")
```

**Important**: Customize the `schema_prompt` variable for your specific beat before running the script. Choose the beat-specific fields that make sense for your topic.

Run the script and document any issues in `notes.md`. 

### Load into SQLite Database

Use sqlite-utils to create a database from your enhanced collection:

```bash
# Create database and import your stories
uv run sqlite-utils insert beat_stories.db stories enhanced_beat_stories.json --pk link

# Extract metadata arrays into separate tables for easier querying
uv run sqlite-utils extract beat_stories.db stories "metadata.people" --table people --fk story_link
uv run sqlite-utils extract beat_stories.db stories "metadata.key_institutions" --table institutions --fk story_link

```

Now you can run browse the data using Datasette

First, install datasette:

```bash
uv add datasette
uv run datasette beat_stories.db
```

### Analysis and Insights

Using facets and filters, explore patterns in your beat:

1. **Key Players**: Who appears most frequently? What roles do they play?

2. **Geographic Patterns**: Which areas get the most coverage?

3. **Institutional Network**: Which organizations appear in stories?

Do these findings make sense? Document your findings in `notes.md`

### Reflection

Conclude your `notes.md` with reflection on:

- What did the structured metadata reveal about this beat?
- How could this approach help a beat reporter?
- What would you do differently with more time or data?

### Submission

When you are finished, add, commit and push your changes:

```bash
git add .
git commit -m "CNS beat collection analysis"
git pull origin main
git push origin main
```

Submit the link to your  `notes.md` in ELMS.
