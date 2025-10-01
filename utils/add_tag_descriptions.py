import json

INPUT_PATH = '/workspaces/jour329w_fall2025/data/tags.json'
OUTPUT_PATH = '/workspaces/jour329w_fall2025/grovic/cns_tag_browser/vite-client/public/tags.json'

GENERIC_DEFINITIONS = {
    'maryland': 'An eastern U.S. state known for its Chesapeake Bay and proximity to Washington, D.C.',
    'baltimore': 'A major city in Maryland, known for its harbor and history.',
    'trump': 'Refers to Donald Trump, former U.S. president.',
    'school': 'Educational institution for children and young adults.',
    'police': 'Law enforcement organization or personnel.',
    # Add more generic definitions as needed
}

def generate_description(tag_name):
    name = tag_name.strip('"').lower()
    for key, definition in GENERIC_DEFINITIONS.items():
        if key in name:
            return definition
    return f"Stories tagged with '{tag_name.strip('"')}' cover news, events, or topics related to {tag_name.strip('"')}."

def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        tags = json.load(f)
    for tag in tags:
        if not tag.get('description'):
            tag['description'] = generate_description(tag.get('name', 'this tag'))
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
