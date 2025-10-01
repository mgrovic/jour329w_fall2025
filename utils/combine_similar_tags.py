import json
import re
from collections import defaultdict, Counter

INPUT_PATH = '/workspaces/jour329w_fall2025/data/tags.json'
OUTPUT_PATH = '/workspaces/jour329w_fall2025/grovic/cns_tag_browser/vite-client/public/tags.json'

def normalize_name(name):
    return re.sub(r'[^a-z0-9 ]', '', name.lower()).strip()

def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        tags = json.load(f)
    combined = defaultdict(lambda: {
        'ids': [], 'count': 0, 'descriptions': [], 'links': [], 'names': [], 'slug': '', 'taxonomy': '', 'meta': []
    })
    for tag in tags:
        norm = normalize_name(tag.get('name', ''))
        entry = combined[norm]
        entry['ids'].append(tag['id'])
        entry['count'] += tag.get('count', 0)
        desc = tag.get('description', '').strip()
        if desc:
            entry['descriptions'].append(desc)
        entry['links'].append(tag.get('link'))
        entry['names'].append(tag.get('name', ''))
        entry['slug'] = tag.get('slug', entry['slug'])
        entry['taxonomy'] = tag.get('taxonomy', entry['taxonomy'])
        entry['meta'] += tag.get('meta', [])
    output_tags = []
    for norm, entry in combined.items():
        # Use the most common name as display name
        name_counter = Counter(entry['names'])
        display_name = name_counter.most_common(1)[0][0]
        output_tags.append({
            'id': entry['ids'][0],
            'count': entry['count'],
            'descriptions': entry['descriptions'],
            'links': entry['links'],
            'name': display_name,
            'all_names': entry['names'],
            'slug': entry['slug'],
            'taxonomy': entry['taxonomy'],
            'meta': entry['meta'],
        })
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output_tags, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
