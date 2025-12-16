Star-Dem Topic Entities 11/10/25

I picked Aquaculture. Most interesting topic to me because of a) fishing and b) relying on a trade for culture and economy makes me want to know more c) seems niche enough where a beat book on this topic would be pretty important IMO

V1/V2 groq/openai/gpt-oss-120b

V3 glm-4.6:cloud


V4: groq/meta-llama/llama-4-maverick-17b-128e-instruct


- Are the extracted entities accurate? Check 5-10 stories in detail
Attempt 2 and Attempt 4 looks super accurate! I have no clue what went on with attempt 1
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
Nope, there are a bunch of Easton, Easton Maryland and Easton MD. need to be specified. (For v4 it spefified all names)
- **Organizations**: Are organization names complete and accurate? Are abbreviations expanded?
All org names are complete, there are some acronyms, but it seems like abbreviations are expanded. 

#### Comparison Between Models/Prompts
- How do the results differ between your two runs?
V3: All i Did was change the model and it gave me 0 zip zed meta data. Imma run it again but that makes me mad! 

- Which model/prompt produced better results? Why?
Not glm-4.6:cloud!!!!!!! groq/openai/gpt-oss-120b did well but groq/meta-llama/llama-4-maverick-17b-128e-instructV4, gave the best results

- Did focusing on "important" entities improve quality?
There were not much differences between V2 and V4 in terms of pulling Metadata, except the economic focus column. I guess that one is more subjective... but they were pretty figgerent



#### Topic-Specific Patterns
- What are the most frequently mentioned people in this topic? Use this query:
```sql
SELECT value as person, COUNT(*) as mentions
FROM stories_v1, json_each(metadata_people)
GROUP BY person
ORDER BY mentions DESC
LIMIT 20
```

Linda Haddaway King	6
Jack Brooks	6
Gigi Windley	6
George O'Donnell	6

- What are the most common places? Organizations?

Places:
Tangier Island	11
St. Michaels	11
Elkton	11

Orgs: 
Queen Anne's County Waterman's Association	10
Chesapeake Charities	9
St. Mary's River Watershed Association	7

- Do these patterns make sense for your chosen topic?
The places and Orgs are pretty self explanatory, as 2 of the top orgs are water specific organizations located in the bay. 

Tangier Island is a small island located on the Chesapeake bay, with a super bay orianted community so that checks out
St. Michaels is another city located on the water, this one land locked. Not completely sure why this town over all the others on the bay is so mentioned but that may be important to look into. 
Same with Elkton ^^

- What changes would you need to make to ensure that a beat book built with this information would be properly scoped?

To best create a beatbook, I would clean and standardize place names, add titles to the peoples names (without that they are close to usless) expand entity extraction to cover all relevant organizations and issues, include metadata about economics and environment. I think that we would definitely need to train the book on more stories if possible, and include a new metadata column, if it affects culture, economics, or bay health: something like this 