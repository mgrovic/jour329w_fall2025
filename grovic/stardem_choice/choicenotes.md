Stardem Choice       11/12/25


#### Experiment Design
- What specific aspects did you vary in each version?
I changed prompt to include title for names, add another meta data column that identifies the population that is most impacted. I also wanted to test enviorment for its compatibility with aqua culture. 
- What were your hypotheses about what would improve results?
I thought it would make the meta data the best version of itself. I thought that adding more meta data would better make a beat book as it would unveil more of the full story. 
- Why did you choose these particular variations?
I chose my variations because I wanted to to see how well aquaculture was identified in the enviormental section, to see if these could be combined into one beatbook, if there should be one beat book that mostly focuses on enviorment but includes aquaculture as a big part. 

#### Comparative Analysis
- Which version produced the best results overall? Why?
To be honest I don't think any of my exports are excellent. I would absoultely love some help improving my prompt before creating my beatbook. The enviorment metadata is decent, but I think that it needs to be cleaned up (the impact column is pretty wack) overall attempt two was probablt the best, as it got the people places and enviormental topics correct, but the impact table 

- Were there specific categories (people/places/organizations) where one version excelled?
Yeah I was super pleased with the enviormental column for most of the versions. It did a great job breaking the stories into different enviormental focusi, going above and beyond the examples I gave in the script. 
- Did any version have unexpected strengths or weaknesses?
All versions struggled with impact. I have Culture, policy and economics as examples and if they didn't fit into one of those three it wouldn't create something similar. 
- How consistent were entity names across versions?
The consistency was near perfection which I found suprising. The enviormental tab had the most variance, with some being more specifc or broad than others, but people, place and instituion it was near perfect. 

#### Prompt Engineering Insights
- What prompt elements had the biggest impact on quality?
The examples given to the AI seemed pretty important. When I gave a lot of examples the LLM seemed more willing to branch out from the given cateogories and properly identify what actually fit the story (enviormental focus) but when I gave very few examples (impact) the AI seemed boxed in. 
- Did adding examples help? What kind of examples worked best?
Well I didn't look at this question as I answered the first one, but I think the kind of examples that worked the best were more specific, for the reasons stated above. When only listing 2 or 3 I feel like the LLM took it as a multiple choice, while when I gave a bunch of nicher, more specific examples, the LLM felt free to expand. 
- How specific should instructions be?
Broad enough for you to not box the LLM in and not lead it to an answer you want, but specific enough so it includes all the specifc information that you want it to find. This seems vague but its a fine line you must ride. 
- What caused the LLM to make mistakes?
Not giving enough context or examples, boxing the LLM in, not giving 

#### Final Recommendations
- If you were creating a beat book, which version would you use?
Version 2 of the Enviorment Json.
- What's your recommended prompt and model combination?
I think my prompt is pretty fire but I would love to clean it up a bit, so it does the niche things I want it to, the model for me is pretty clearly Maverick, as it does the best job of pulling specific places and people, and keeps things super unified. 
- What remaining issues need to be addressed?
I can't get positions or titles to be listed. I need to clean up the impact column and make usre the LLM is able to add its own options for that category. 

1. **Choice Justification**: Why did you choose this path?
I chose this path so I could better refine my prompt and metadata. 
2. **Process Documentation**: 
   - Step-by-step record of what you tried
   I reworked my prompt pretty heavily 
   Step 1: changed prompt to include title for names,
   Step 2 add another meta data column that identifies the population that is most impacted. 
   Step 3: Added a column for the enviormental focus of the article. 
   Step 4: Ran it twice on the Enviormental Json (to compare it to my work from the past assignment)
   Step: 5 Ran in on the AquaJson to see how it compared to enviormetnal and my past prompts on Aqua. 
   - All prompts you tested (You extract structured entities (people, places, organizations) from LOCAL NEWS stories
all centered on the same topic/beat. Focus on entities that matter for a beat book
(long-term coverage). Prefer government officials, recurring stakeholders, key locations,
formal organization names. Skip generic roles unless uniquely identifying (e.g. "Maryland
Department of Natural Resources"). Exclude pure descriptors (e.g., "the agency", "officials").

Return ONLY a single JSON object with keys:
- docref: copy from input if present (else null)
- people: list of the most important peoples names and their title strings)
- geographic_focus: list of place names (strings)
- key_institutions: list of org names (strings)
- environmental_focus: list of environmental themes (strings)
- impact: which population is most impacted 

Rules:
- Do not include duplicates.
- Only include entities clearly mentioned.
- If none found for a category, return an empty list.
- Determine importance by how much of the story is focused on the person, or what role they play in the story. List from 1–6 people.
- Do not include the Star Democrat as an organization (exclude “Star Democrat” / “The Star Democrat”).

Example:
Input snippet:
"Talbot County Council President Chuck Callahan said the Chesapeake Bay cleanup
plan needs broader support from the Maryland Department of Natural Resources."

Example output:
{{
  "people": ["Donald Trump: President of the United States", "Ben Cardin: Former Maryland Senator", "Andrew Barnet: Co-Owner of Open Book Farm"],
  "geographic_focus": ["Annapolis", "Gunpowder Falls"],
  "key_institutions": ["EPA", "NOAA"],
  "environmental_focus": [
    "Water pollution",
    "Air pollution",
    "Habitat loss",
    "Erosion",
    "Climate change",
    "Waste management",
    "Deforestation",
    "Overfishing",
    "Wetland destruction",
    "Other"
  ]
  "impact": ["Economy" , "Culture", "Policy"]
}}

Story input:
docref: {docref}
title: {title}
byline: {byline}
content: {content}

Return ONLY the JSON object.
""")
   - All models you used
   groq/moonshotai/kimi-k2-instruct-0905
   groq/meta-llama/llama-4-maverick-17b-128e-instruct

5. **Examples**: 
   - Option 2: Include the best examples of generated content

   Seaweed boom? - The global market for seaweed could see significant growth; can the U.S. get in on the aquaculture and ecological wave?
   
   ["Rafael Cuevas Uribe", "Rick Zechman", "Martien van Nieuwkoop"]	["California", "Maine", "Hawaii", "Alaska", "Humboldt Bay", "Chesapeake Bay", "Gulf of Mexico", "Puget Sound"]	["California State Polytechnic University, Humboldt", "IMARC Group", "Meticulous Market Research Pvt. Ltd.", "World Bank", "NOAA", "Environmental Defense Fund"]	["Seaweed farming", "Aquaculture", "Climate change", "Water pollution", "Ecosystem conservation"]	["Economy"]


   Appreciating oysters

   	["Eastern Shore", "Chesapeake Bay", "Delaware Bay", "Gulf Coast", "Easton", "Maryland"]	["Maryland Department of Natural Resources"]	["Water pollution", "Overfishing", "Habitat loss"]	["Culture", "Economy"]

6. **Reflection**: What did you learn? What would you do differently?
I would specify my impact column, that felt like a loss. I would rework the prompt (again) to properly show the title/position of the people included. I learned a lot about what you need to give to the LLM in order for it to produce the correct metadata. It really is a fine line, as you have to figure out what you want the LLM to know to create the metadata, but also when you are too specifc or give it too much, that will often leak into the meta data. 