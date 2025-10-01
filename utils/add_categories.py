import json
import re

# Simple rules for guessing category
person_keywords = ['Mr.', 'Ms.', 'Dr.', 'President', 'Senator', 'Governor', 'Mayor', 'Officer', 'Chief', 'Judge', 'Attorney', 'Detective', 'Commissioner']
event_keywords = ['protest', 'election', 'conference', 'meeting', 'summit', 'festival', 'hearing', 'trial', 'ceremony', 'parade', 'game', 'debate']
place_keywords = ['city', 'county', 'state', 'park', 'school', 'hospital', 'Baltimore', 'Maryland', 'Washington', 'Annapolis', 'District', 'Police', 'Station', 'University', 'Center']

# Expand as needed for your data

def guess_category(tag_name):
    name = tag_name.lower()
    # Person: contains person keywords or looks like a full name
    if any(kw.lower() in name for kw in person_keywords) or re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', tag_name):
        return 'Person'
    # Event: contains event keywords
    if any(kw.lower() in name for kw in event_keywords):
        return 'Event'
    # Place: contains place keywords
    if any(kw.lower() in name for kw in place_keywords):
        return 'Place'
    # Thing: single capitalized word (could be organization, object, etc)
    if re.match(r'^[A-Z][a-z]+$', tag_name):
        return 'Thing'
    return 'Other'

with open('data/tags.json', 'r') as f:
    tags = json.load(f)

for tag in tags:
    tag['category'] = guess_category(tag['name'])

with open('data/tags.json', 'w') as f:
    json.dump(tags, f, indent=2)

print('Categories added to data/tags.json!')
