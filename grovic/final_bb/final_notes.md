# Final Notes

---
## bbd1notes.md

Beat Book Draft 2: 11/20/2025

Model: Maverick
Prompt: Generator.py from the email you sent me, with a bunch of revision so that it actually cooked up the batches the right way for my script and made a full on beatbook. Also once it made the Beatbook JSON I combined with my original prompt so it looked the way I wanted. There were a bunch of steps in between this. The first “book” I made was interesting. It was like a mini beat book (beatbook_“topic”.md)  for all 42 or 44 (whatever number it was) of my individual JSON batches. This was interesting to look at, as there was random JSON data in each one (not related to anything except Environment/AquaCulture). Once I got this and read though, and decided that I definitely needed to incorporate more structure into my beatbook, so I installed my og prompt (which I thought outlined the basics of a beatbook decently well) and let it cook. It failed a bunch of times, one time making it through 43/44 batches and failed. 

I am still a very big fan of Maverick after using it for this beat book. When I finally got it to work my “final” draft “beatbook_output.md”, was the finished product. I have a LOT of issues with this, as it is far from perfect, but I think that it is my best effort yet. It is super specific and expands on almost everything. I am a big fan of the way it's broken down in SOME aspects. Overall there are repetitive weird headings and headings are not clear, but I really like how it emphasizes a location, and does a mini specific beatbook on how to report on the environment there. It is super chaotic and repeats format with different information, I assume this is because of batches. I also really don't like docref: news/19B9101A54E5E250) that are thrown in the beatbook randomly (even though I thought I took those out of my JSON). I also compared this against my first beatbook that you produced and it seemed like something in the middle of the two would be perfect. Like this recent beatbook has amazing information and specifics but doesnt do a good job of instructing how to use this info, while the one that you made on the local model was explanatory but really lacked specifics. One short, one long and when I asked Claude to look at both of them it said: Document 1 = Comprehensive encyclopedia (reference tool) Document 2 = Practical manual (execution tool) and I feel like that is a good way to put it. I would really like my next step to be that in between. 

---
## bbd3notes.md

For beatbook draft three I made it my mission to take the beatbooks that I have created to start refining and specifying, in order to get the best product. My first step was to ask copilot to make a script that both combined my first two drafts (draft1: a short but well organized beatbook, with strong narrative but lacking in detail) and (draft2: an extremely long beatbook with a plethera of information and specifics but very poor organization and an obsurd lack of narritive) and that focused the book geopraphicly. I thought that both of these two drafts had very strong upside, so I assumed if I created a script that combined the two drafts (beatbook_combiner.py) that it would create a perfect beatbook. 
The final product that came from beatbook_combiner.py was beatbook_combined.md (lol). My first time reading through I was pretty impressed with the final product, as it did exactly what I wanted, hitting all three of my marks. 
1. It was well organized, and hit all the categories that I wanted it to.
2. It categorized a lot of information by county/location, making it more geographically focused.
3. It took draft 2's insane amount of information and distributed it well, organizationaly. 

Although I was quite happy with the result, I could sense that it was still missing something, so I shot you an email, asking about this draft. You said it was obviously lacking narrative, as it was still pretty bullet point heavy (left over from draft 2). 

This lead me to the next part of draft 3, which was a bit easier. I had copilot edit my combiner script to take the combined.md script and make it take the information from the combined beatbook, keeping the organizational structure, but making it more narrative based. 

---
## finalnotes.md

LLM notes: 
Here's a summary of everything we accomplished today:

1. Reviewed Beatbook Documents
Compared two versions of a journalism beatbook
Confirmed one was the full version with names/contacts, the other was redacted (PII removed)
This is standard practice for creating shareable vs. internal documents
2. Built Source Context Generator (Python Script #1)
Goal: Analyze journalists' sources and explain why they're valuable
Inputs:
people_appendix.md (list of people/sources)
stories_with_entities_v11.json and v12.json (news stories with full content)
Process:
Initially set up with Anthropic API, switched to Groq at your request
Parses people from markdown (bullet list format)
Sends each person + story content to LLM
Generates: Why valuable, area of expertise, when to contact
Output: source_contexts.md
Challenges solved:
Parsing markdown format (had to update for your specific bullet-list structure)
Token limit errors → reduced story content and switched to smaller model (llama-3.1-8b-instant)
Added resume functionality with progress tracking
3. Built Beatbook Merger (Python Script #2)
Goal: Add source profiles to beatbook while matching its writing style
Process:
Loads both source_contexts.md and beatbook_cleaned_redacted.md
Uses Claude to analyze beatbook's style/tone
Rewrites source profiles to match that exact style
Handles large files by processing in chunks
Merges everything into one cohesive document
Output: beatbook_with_sources.md
Final Result
You now have two automated scripts that:

Generate journalist-focused context for sources based on news coverage
Integrate those sources into your beatbook with consistent style and tone


My final beatbook was a toughie to make. What i did to make the final - 

Step one, strip all names, links and emails out of my latest beatbook. This was because they were often fake, incorrect or wrong. This took a while as I had to find a way to do this without disrupting the content that was correct. This is beatbook_cleaned_redacted.md

Step two, I created a list of all names and positions from the json data that was relevant to the topic and local people. I then took this list and used groq and (peoplefixer.py) to take these specific names and scan the Json files with the extracted meta data and story content, to describe these people and why they are relevant to the eastern shore, the enviorment and aquaculture. This took me FOREVER. it produced(source_contexts.md)

Step three, use claude sonnet to combine the two together, stripped beatbook and new updated names, and make the names sound like they were written with the first beatbook. 

In my opinion this new beatbook is phenomenal, but the names section is too long. Although its too long its accurate, provides great detail, and would be super helpful. The way that I am looking at this beatbook is in two parts. Part one is the information exluding people, the guide to beat. The second part is an appendix of names, with thier position, title and extra information to help best utalize these contacts. 

Pretty Proud of this. 

---
## neralyfinalnotes.md

This was a super interesting process and I am still struggling with the fact checking portion. 

My inital beatbook I took my draft 3 and asked Claude Sonnet 4.5 to clean it. The result I got was pretty damn good IMO (aside from the plethera of obvious false names/links/emails.) Reading through and fact checking this beatbook has made me personally super interested in the topic itself (more than I already was lol). the information here is really really good when it's correct and thats my next step. 

As I went through and attempted to fact check my book, it became obvious that the errors mostly consited of people and their titles. So I wanted to create some scripts to fix this (these all fail btw so unlucky). My first course of action was to strip all the names and thier titles from my json data (this is people.csv and people12.csv). Once this was done I created a script that would remove people without titles and organize them by categorey. This gave me People_categorized.csv. While looking through this data, I saw that a good number of these people were not specific to the area, so I decided to narrow the list down once more to just people local to Maryland Delaware and Virginia. Once I had this list I tried over and over and over again to create a script to fact check my beatbook using fix_beatbook.py. (the script also removed emails, phone numbers and links) Last night I finally thought I did it, as it went through line by line "checking" for factual info using the names. It did a mostly good job removing emails and phone numbers and so on, but overall it changed almost nothing. Something that I recently realized is that if a name and title are completely wrong, how will the llm know how to fix the context given, without the story content. IDK pissing me off. Worked on this for like 5 hours and didn't go anyhwere. But the content avalible is so so juicy and good. Like such a good spread of non profit officals, scientists, government officals etc. 

I really want this beatbook to be good because it has such potential. 

Fact checking: https://docs.google.com/document/d/13babdrfY3sl97hsEB6BtyCgBYfNQXOL3wL6I-Oc4eZ8/edit?usp=sharing

---
## choicenotes.md

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
{
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
  ],
  "impact": ["Economy" , "Culture", "Policy"]
}

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
