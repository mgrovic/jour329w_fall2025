import json
from groq import Groq
import os
from pathlib import Path

# Initialize Groq client using environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "Missing GROQ_API_KEY environment variable. Set it securely in your environment."
    )

client = Groq(api_key=GROQ_API_KEY)


def load_people(file_path):
    """Load the people list from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_stories(file_path):
    """Load stories from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_story_content(stories_data):
    """Extract content from stories JSON"""
    contents = []
    for story in stories_data:
        if 'content' in story:
            contents.append({
                'title': story.get('title', 'Untitled'),
                'content': story['content']
            })
    return contents

def generate_source_context(person_name, person_info, all_story_content):
    """Generate context for a single person using Groq"""
    
    # Prepare story content for the prompt - use fewer stories with less content
    story_text = "\n\n".join([
        f"Story: {s['title']}\n{s['content'][:800]}..." 
        for s in all_story_content[:10]  # Reduced to 10 stories with 800 chars each
    ])
    
    prompt = f"""Based on the following news stories, analyze this person as a journalist source:

Person: {person_name}
{person_info}

News Stories Context:
{story_text}

Please provide:
1. **Why Valuable**: A 2-3 sentence explanation of why this person is a valuable source for a journalist
2. **Area of Expertise**: Their specific areas of expertise relevant to journalism
3. **When to Contact**: Specific scenarios when a journalist should reach out to them

Format your response as:
WHY VALUABLE: [your text]
EXPERTISE: [your text]
CONTACT WHEN: [your text]

Keep it concise and journalist-focused."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",  # or "mixtral-8x7b-32768" or "llama-3.1-70b-versatile"
        max_tokens=1000,
        temperature=0.7,
    )
    
    return chat_completion.choices[0].message.content

def parse_people_markdown(md_content):
    """Parse markdown to extract individual people entries"""
    import re
    
    people = []
    lines = md_content.split('\n')
    
    for line in lines:
        # Look for lines that start with - or * and contain **Name:**
        if line.strip().startswith(('-', '*')) and '**Name:**' in line:
            # Extract name using regex
            name_match = re.search(r'\*\*Name:\*\*\s*([^—]+)', line)
            if name_match:
                name = name_match.group(1).strip()
                # Store the entire line as info
                people.append({
                    'name': name,
                    'info': line.strip()
                })
    
    return people

def main():
    # File paths
    people_file = "people_appendix.md"
    stories_v11 = "stories_with_entities_v11.json"
    stories_v12 = "stories_with_entities_v12.json"
    output_file = "source_contexts.md"
    
    print("Loading data...")
    
    # Load people
    people_md = load_people(people_file)
    people_list = parse_people_markdown(people_md)
    print(f"Found {len(people_list)} people")
    
    # Load stories from both versions
    stories_11 = load_stories(stories_v11)
    stories_12 = load_stories(stories_v12)
    
    # Extract content from both
    content_11 = extract_story_content(stories_11)
    content_12 = extract_story_content(stories_12)
    
    # Combine all story content
    all_content = content_11 + content_12
    print(f"Loaded {len(all_content)} stories")
    
    # Process each person
    results = []
    for i, person in enumerate(people_list, 1):
        print(f"Processing {i}/{len(people_list)}: {person['name']}")
        try:
            context = generate_source_context(
                person['name'], 
                person['info'], 
                all_content
            )
            results.append({
                'name': person['name'],
                'original_info': person['info'],
                'journalist_context': context
            })
        except Exception as e:
            print(f"Error processing {person['name']}: {e}")
            results.append({
                'name': person['name'],
                'original_info': person['info'],
                'journalist_context': f"ERROR: {str(e)}"
            })
    
    # Write results to markdown
    print(f"\nWriting results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Journalist Source Contexts\n\n")
        f.write("*Generated from news story analysis*\n\n")
        f.write("---\n\n")
        
        for result in results:
            f.write(f"## {result['name']}\n\n")
            f.write(f"### Original Information\n")
            f.write(f"{result['original_info']}\n\n")
            f.write(f"### Journalist Context\n")
            f.write(f"{result['journalist_context']}\n\n")
            f.write("---\n\n")
    
    print(f"Done! Processed {len(results)} people.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()