Star-Dem Topic Entities 11/10/25

I picked Aquaculture. Most interesting topic to me because of a) fishing and b) relying on a trade for culture and economy makes me want to know more c) seems niche enough where a beat book on this topic would be pretty important IMO

V1/V2 groq/openai/gpt-oss-120b

V3

- Are the extracted entities accurate? Check 5-10 stories in detail
Attempt 2 looks super accurate! I have no clue what went on with attempt 1
- Are there false positives (entities that shouldn't be there)?
Not in V1 or V2
- Are there false negatives (important entities that were missed)?
Every Org and Place was missing
- Do the entities match what you see when reading the stories?
Yep, V2 did it pretty perfectly 

#### Entity Quality
- **People**: Are full names captured correctly? Are titles/roles included appropriately?
No roles, but thats on me
- **Places**: Are location names consistent (e.g., "Easton" vs "Easton, MD")? Are they specific enough?
Nope, there are a bunch of Easton, Easton Maryland and Easton MD. need to be specified. 
- **Organizations**: Are organization names complete and accurate? Are abbreviations expanded?
All org names are complete, there are some acronyms, but it seems like abbreviations are expanded. 

#### Comparison Between Models/Prompts
- How do the results differ between your two runs?
- Which model/prompt produced better results? Why?
- Did focusing on "important" entities improve quality?
- Are there systematic differences in how entities are extracted?

#### Topic-Specific Patterns
- What are the most frequently mentioned people in this topic? Use this query:
```sql
SELECT value as person, COUNT(*) as mentions
FROM stories_v1, json_each(metadata_people)
GROUP BY person
ORDER BY mentions DESC
LIMIT 20
```

- What are the most common places? Organizations?
- Do these patterns make sense for your chosen topic?
- Are there any surprising or unexpected entities?
- What changes would you need to make to ensure that a beat book built with this information would be properly scoped?