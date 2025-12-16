
import anthropic
import os

def load_file(file_path):
    """Load content from a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(file_path, content):
    """Save content to a file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_roadmap(notes, client):
    """Use Claude to transform notes into a detailed roadmap"""
    
    prompt = f"""You are helping create a detailed, step-by-step roadmap from project notes. 

Here are the raw notes from a project:
<project_notes>
{notes}
</project_notes>

Please transform these notes into a comprehensive, easy-to-follow roadmap that someone else could use to replicate this process. The roadmap should:

1. **Start with an overview** - What was accomplished? What's the end goal?

2. **Break down into clear phases** - Organize the work into logical stages

3. **Provide step-by-step instructions** - For each phase:
   - What to do
   - Why it matters
   - Tools/technologies needed
   - Common pitfalls and how to avoid them
   - Expected outcomes

4. **Include technical details** - Commands, file formats, API setup, etc.

5. **Add helpful context** - Explain decisions, alternatives considered, troubleshooting tips

6. **Use clear formatting**:
   - Headers for major sections
   - Numbered steps for sequences
   - Bullet points for lists
   - Code blocks for commands/code
   - Callout boxes for important warnings or tips

7. **Make it beginner-friendly** - Assume the reader is competent but unfamiliar with this specific process

The tone should be:
- Clear and instructional
- Encouraging but realistic about challenges
- Practical and action-oriented
- Comprehensive without being overwhelming

Format the output as a proper markdown document with a title, table of contents, and well-organized sections."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def main():
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # File paths
    notes_file = "combined_notes.md"
    output_file = "project_roadmap.md"
    
    print("Loading notes...")
    
    # Load notes
    notes = load_file(notes_file)
    print(f"Loaded {notes_file} ({len(notes)} characters)")
    
    print("\nGenerating roadmap with Claude...")
    print("This may take a minute...\n")
    
    try:
        roadmap = generate_roadmap(notes, client)
        
        print("Saving roadmap...")
        save_file(output_file, roadmap)
        
        print(f"\n✓ Done! Created {output_file}")
        print(f"  Total length: {len(roadmap)} characters")
        print(f"\nYour roadmap is ready to share!")
        
    except Exception as e:
        print(f"\n✗ Error generating roadmap: {e}")
        print("\nTroubleshooting tips:")
        print("- Check that ANTHROPIC_API_KEY is set correctly")
        print("- Verify combined_notes.md exists and is readable")
        print("- If notes are very long, consider splitting into sections")

if __name__ == "__main__":
    main()