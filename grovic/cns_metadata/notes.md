CNS Metadata 09/25/2025 Miles Grovic

Story 1
https://cnsmaryland.org/2022/03/03/biden-administration-preps-new-rules-covering-sexual-misconduct-at-schools-colleges/ 
Biden administration preps new rules covering sexual misconduct

up to 3 key people (with title or role)

Education Secretary Betsy DeVo
President of the Uited States Joe Biden 
Democratic Representative of Connecticut Rosa DeLauro 

up to 3 main organizations/institutions

The Department of Education 
National Education Association
It’s On Us


up to 3 geographic locations

Washington DC

3 short (two-word) topics you would assign

Title XI 
Education Policy
Human Rights



what kind of story is this - breaking news, feature, analysis, investigation, other

Breaking news

a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people (greater impact means higher score)

3

LLM Answer - groq
uv run python -m newspaper --url=https://cnsmaryland.org/2022/03/03/biden-administration-preps-new-rules-covering-sexual-misconduct-at-schools-colleges/ -of=text \
| llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
  \"url\": \"the url of the story\",
  \"people\": [\"list of up to 3 people with their titles/roles\"],
  \"organizations\": [\"government agencies, companies, groups mentioned\"],  
  \"locations\": [\"cities, counties, states, specific places\"],
  \"topics\": [\"3-5 topic tags, max 2 words each\"],
  \"story_type\": \"breaking news, feature, analysis, investigation, other\",
  \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\"
}"

"people": [
    "Betsy DeVos - former U.S. Secretary of Education",
    "Joe Biden - President of the United States",
    "Tracey Vitchers - executive director of It’s On Us"
  ],
  "organizations": [
    "Biden administration",
    "U.S. Department of Education",
    "National Education Association (NEA)",
    "It’s On Us",
    "Foundation for Individual Rights in Education (FIRE)"
  ],
  "locations": [
    "Washington, D.C.",
    "Connecticut",
    "North Carolina",
    "Massachusetts"
  ],
  "topics": [
    "Title IX",
    "sexual misconduct",
    "campus policy",
    "Biden reversal"
  ],
  "story_type": "feature",
  "impact": 4

uv run python -m newspaper --url=https://cnsmaryland.org/2022/03/03/biden-administration-preps-new-rules-covering-sexual-misconduct-at-schools-colleges/ -of=text \
| llm -m claude-4-sonnet
 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
 \"url\": \"the url of the story\",
 \"people\": [\"list of up to 3 people with their titles/roles\"],
 \"organizations\": [\"government agencies, companies, groups mentioned\"], 
 \"locations\": [\"cities, counties, states, specific places\"],
 \"topics\": [\"3-5 topic tags, max 2 words each\"],
 \"story_type\": \"breaking news, feature, analysis, investigation, other\",
 \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\"
}"

LLM Answer - Claude
 "people": [
    "Joe Biden - President",
    "Betsy DeVos - Former Education Secretary", 
    "Catherine Lhamon - Assistant Secretary for Civil Rights"
  ],
  "organizations": [
    "Biden administration",
    "Department of Education",
    "Trump White House",
    "National Education Association",
    "It's On Us",
    "Foundation for Individual Rights in Education"
  ],
  "locations": [
    "Washington"
  ],
  "topics": [
    "Title IX",
    "Sexual misconduct",
    "Education policy",
    "LGBTQ+ rights",
    "Due process"
  ],
  "story_type": "breaking news",
  "impact": "4"


Story 2
  https://cnsmaryland.org/2020/01/24/trump-ukraine-obstruction-continues-house-democrats-tell-senate-impeachment-trial/
  Trump Ukraine obstruction continues, House Democrats tell Senate impeachment trial

My Answers 
up to 3 key people (with title or role)
President  of the United States Donald Trump
Democratic Reprasentative of California Adam Schiff, the lead manager and chairman of the House Intelligence Committee.
Republican Senator LLindsey Graham

up to 3 main organizations/institutions
House Intelligence Committee
Senate 
Congress

up to 3 geographic locations
Ukraine
Russia 
White House

3 short (two-word) topics you would assign
Foregin Affairs 
Political Polarization

what kind of story is this - breaking news, feature, analysis, investigation, other
feature

a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people (greater impact means higher score)
4




uv run python -m newspaper --url=https://cnsmaryland.org/2020/01/24/trump-ukraine-obstruction-continues-house-democrats-tell-senate-impeachment-trial/ -of=text \
| llm -m claude-4-sonnet "Extract structured metadata from this news story and return as JSON with these exact fields:
{
 \"url\": \"the url of the story\",
 \"people\": [\"list of up to 3 people with their titles/roles\"],
 \"organizations\": [\"government agencies, companies, groups mentioned\"], 
 \"locations\": [\"cities, counties, states, specific places\"],
 \"topics\": [\"3-5 topic tags, max 2 words each\"],
 \"story_type\": \"breaking news, feature, analysis, investigation, other\",
 \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\"
}"
LLM Answer - Claude

"people": [
    "Adam Schiff - Lead House impeachment manager and Chairman of House Intelligence Committee",
    "Donald Trump - President of the United States",
    "Joe Biden - Former Vice President"
  ],
  "organizations": [
    "House of Representatives",
    "Senate",
    "House Intelligence Committee",
    "White House",
    "MSNBC",
    "NBC"
  ],
  "locations": [
    "Washington",
    "Ukraine",
    "California",
    "Colorado",
    "Minnesota",
    "South Carolina"
  ],
  "topics": [
    "Impeachment trial",
    "Ukraine scandal",
    "Congressional obstruction",
    "National security",
    "Senate proceedings"
  ],
  "story_type": "breaking news",
  "impact": 5
}



uv run python -m newspaper --url=https://cnsmaryland.org/2020/01/24/trump-ukraine-obstruction-continues-house-democrats-tell-senate-impeachment-trial/ -of=text \
| llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
 \"url\": \"the url of the story\",
 \"people\": [\"list of up to 3 people with their titles/roles\"],
 \"organizations\": [\"government agencies, companies, groups mentioned\"], 
 \"locations\": [\"cities, counties, states, specific places\"],
 \"topics\": [\"3-5 topic tags, max 2 words each\"],
 \"story_type\": \"breaking news, feature, analysis, investigation, other\",
 \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\"
}"
LLM Answer - Groq

 "people": [
    "Rep. Adam Schiff (D-CA, lead House manager)",
    "President Donald Trump",
    "Rep. Jason Crow (D-CO)"
  ],
  "organizations": [
    "House Intelligence Committee",
    "U.S. Senate",
    "Democratic Party",
    "Republican Party"
  ],
  "locations": [
    "Washington, D.C.",
    "Ukraine"
  ],
  "topics": [
    "impeachment trial",
    "Ukraine aid",
    "obstruction of Congress",
    "national security",
    "witnesses"
  ],
  "story_type": "breaking news",
  "impact": 4
}

Story 3
https://cnsmaryland.org/2019/10/25/in-baltimore-presidents-family-and-friends-bid-cummings-a-final-farewell/
In Baltimore, presidents, family and friends bid Cummings a final farewell

My Answers 
up to 3 key people (with title or role)
Repratentative Elijah Cummings
Baltimore Resident Laura Louden 
Reverand Matthew Watley

up to 3 main organizations/institutions
Morgan State University
Congress

up to 3 geographic locations
New Psalmist Baptist Church
Baltimore
Maryland

3 short (two-word) topics you would assign
Civil Rights 
Influential Baltimorean 
Political Passing


what kind of story is this - breaking news, feature, analysis, investigation, other
Feature

a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people (greater impact means higher score)
2



uv run python -m newspaper --url=https://cnsmaryland.org/2019/10/25/in-baltimore-presidents-family-and-friends-bid-cummings-a-final-farewell/-of=text \ | llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
 \"url\": \"the url of the story\",
 \"people\": [\"list of up to 3 people with their titles/roles\"],
 \"organizations\": [\"government agencies, companies, groups mentioned\"], 
 \"locations\": [\"cities, counties, states, specific places\"],
 \"topics\": [\"3-5 topic tags, max 2 words each\"],
 \"story_type\": \"breaking news, feature, analysis, investigation, other\",
 \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\"
}"

LLM Answer -Groq 
"people": ["Rep. Elijah Cummings", "Barack Obama (former President)", "Maya Rockeymoore Cummings (widow)"],
  
"organizations": ["New Psalmist Baptist Church", "Johns Hopkins Hospital", "Morgan State University", "United States Capitol", "House of Representatives"],

"locations": ["Baltimore", "Annapolis", "Washington D.C.", "South Baltimore", "Inner Harbor"],

"topics": ["funeral", "tribute", "civil rights", "legacy", "politics"],
 
"story_type": "feature",

"impact": 4

uv run python -m newspaper --url=https://cnsmaryland.org/2019/10/25/in-baltimore-presidents-family-and-friends-bid-cummings-a-final-farewell/ -of=text | llm -m claude-4-sonnet "Extract structured metadata from this news story and return as JSON with these exact fields:
{
  \"url\": \"the url of the story\",
  \"people\": [\"list of up to 3 people with their titles/roles\"],
  \"organizations\": [\"government agencies, companies, groups mentioned\"],  
  \"locations\": [\"cities, counties, states, specific places\"],
  \"topics\": [\"3-5 topic tags, max 2 words each\"],
  \"story_type\": \"breaking news, feature, analysis, investigation, other\",
  \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\"
}"

LLM Answers-Claude
"people": [
    "Elijah Cummings - Late Democratic Congressman",
    "Barack Obama - Former President", 
    "Maya Rockeymoore Cummings - Congressman's Widow"
  ],
  "organizations": [
    "New Psalmist Baptist Church",
    "Morgan State University",
    "United States Capitol",
    "Johns Hopkins Hospital",
    "House of Representatives",
    "Congress"
  ],
  "locations": [
    "Baltimore",
    "Maryland",
    "Washington",
    "Annapolis",
    "Inner Harbor",
    "South Baltimore",
    "West Side"
  ],
  "topics": [
    "Funeral Service",
    "Political Legacy",
    "Civil Rights",
    "Public Service",
    "Congressional Honor"
  ],
  "story_type": "feature",
  "impact": "4"
}

Story 4
https://cnsmaryland.org/2019/10/10/maryland-delaware-pennsylvania-fight-clean-water-rollback/
Maryland, Delaware, Pennsylvania fight clean water rollback

up to 3 key people (with title or role)
Don Parrish, AFB senior director of congressional relations
Ben Grumbles, Maryland Environment Secretary 
Donald Trump, President of the United States of America

up to 3 main organizations/institutions
Environmental Protection Agency
The EPA
The Trump Administration


up to 3 geographic locations
Chesapeake Bay
Maryland
Delaware

3 short (two-word) topics you would assign
Enviormental Policy 
Chesapeake Bay 
Nature Conservation 


what kind of story is this - breaking news, feature, analysis, investigation, other
Feature/Analysis


a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people (greater impact means higher score)
3

LLM Answers-Claude

 "people": [
    "Brian Frosh - Maryland Attorney General",
    "Andrew Wheeler - Trump EPA Administrator", 
    "Ben Grumbles - Maryland Environment Secretary"
  ],
  "organizations": [
    "Environmental Protection Agency",
    "Maryland Attorney General's Office",
    "Army Corps of Engineers",
    "American Farm Bureau",
    "Chesapeake Bay Foundation",
    "Delaware Department of Natural Resources and Environmental Control",
    "Pennsylvania Department of Environmental Protection",
    "Chesapeake Climate Action Network"
  ],
  "locations": [
    "Washington",
    "Maryland",
    "Delaware", 
    "Pennsylvania",
    "Chesapeake Bay",
    "West Virginia",
    "California"
  ],
  "topics": [
    "Clean Water",
    "EPA Rollback",
    "Environmental Policy",
    "State Rights",
    "Chesapeake Bay"
  ],
  "story_type": "breaking news",
  "impact": "4"
}


uv run python -m newspaper --url=https://cnsmaryland.org/2019/10/10/maryland-delaware-pennsylvania-fight-clean-water-rollback/ -of=text | llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
 \"url\": \"the url of the story\",
 \"people\": [\"list of up to 3 people with their titles/roles\"],
 \"organizations\": [\"government agencies, companies, groups mentioned\"], 
 \"locations\": [\"cities, counties, states, specific places\"],
 \"topics\": [\"3-5 topic tags, max 2 words each\"],
 \"story_type\": \"breaking news, feature, analysis, investigation, other\",
 \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\"
}"

LLM Answers-Groq

"people": ["Brian Frosh, Maryland Attorney General", "Andrew Wheeler, EPA Administrator", "Ben Grumbles, Maryland Environment Secretary"],

 "organizations": ["Environmental Protection Agency", "Maryland Department of the Environment", "Chesapeake Bay Foundation", "American Farm Bureau", "Delaware Department of Natural Resources and Environmental Control", "Pennsylvania Department of Environmental Protection"],

"locations": ["Maryland", "Delaware", "Pennsylvania", "Chesapeake Bay", "West Virginia", "California"],

"topics": ["water rollback", "Clean Water Act", "Chesapeake Bay", "federalism", "pollution"],

"story_type": "feature",

"impact": 4


Story 5 
https://cnsmaryland.org/2017/09/15/marylands-undocumented-immigrants-in-their-own-words/
Maryland’s undocumented immigrants: In their own words

up to 3 key people (with title or role)
President Donald Trump
House Minority Leader Nancy Pelosi
Nathaly Uribe Robledo Undocumented 

up to 3 main organizations/institutions
Deferred Action for Childhood Arrivals program
University of Maryland, Baltimore County
CASA

up to 3 geographic locations
Maryland 
Chile 


3 short (two-word) topics you would assign
Immigration Policy 



what kind of story is this - breaking news, feature, analysis, investigation, other



a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people (greater impact means higher score)

