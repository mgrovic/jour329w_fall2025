Star-Dem Entities                  Nov 5

Model 1: groq/meta-llama/llama-4-maverick-17b-128e-instruct

Model 2: groq/moonshotai/kimi-k2-instruct-0905

Model for attempt 2.5: groq/moonshotai/kimi-k2-instruct-0905


My first two attempts went exactly the same. Which suprised me because I changed up some key parts of the prompt, but I didn't get any change in the output. I let the LLM cook and the inital prompt put no limits on the number of people in the metadata, which caused some stories to have 20+ people listed (bad). It also listed StarDemocrat as an organization (bad again) I think I messed something up, now that I am thinking about it, because even when I changed models, I still got identical metadata ... interesting. The results however seemed super accurate, every single person in the story was listed as were all the organizations. My next time around I made the prompt way more specfic, adding in phrases like, - Determine importance by how much of the story is focued on the person, or what role they play in the story. List from 1-6 people and Do not include the Star Democrat as an Organization. These were just based on the errors. Even though I changed these, they still didn't work, and looked the same. To be honest I have no clue what I did wrong, but I changed a bunch of stuff, (prompt, LLM model, etc ) and saw no change. Ran this like 5 times (which took forever.) 



