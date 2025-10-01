import json
import re

# Load tags
with open('data/tags.json', 'r') as f:
    tags = json.load(f)

# Add new category and tag logic
for tag in tags:
    name = tag.get('name', '').lower()
    # If tag name contains 'cns', 'capital news service', or similar
    if re.search(r'\bcns\b', name) or 'capital news service' in name:
        tag['category'] = 'Capital News Service'

# Save updated tags
with open('data/tags.json', 'w') as f:
    json.dump(tags, f, indent=2)

print('Tags with CNS or Capital News Service have been updated to category Capital News Service.')
