Miles Grovic 09/22/2025 
uv run sqlite-utils memory data/tags.json "select name, count, url from tags order by count desc limit 30"

The "tags.json" file is organized alphabetically by the first letter of the tag name. It is quite difficult to determine which tag is the frquently occuring, as they are not ordered by number. There are certianly quirys or code I could use to sort this data. After asking ChatGPT (https://chatgpt.com/share/68d32271-38a4-8006-985b-fa4477979841), I was reinformed of JQ which is kind of like grep but for json files. I could use a jq code to sort the data by number of tags and not names. 
 
 uv run python -m newspaper --url=https://cnsmaryland.org/2025/01/19/marcus-garvey-pardon-brings-long-awaited-joy-to-supporters/ |
uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "You are an expert at categorizing topics for news stories. Read the text and provide no more than 5 topics."
1. Posthumous Pardon  
2. Marcus Garvey Legacy  
3. Racial Justice & Activism  
4. Jamaican Diaspora Celebration  
5. Presidential Clemency

 uv run python -m newspaper --url=https://cnsmaryland.org/2025/01/19/marcus-garvey-pardon-brings-long-awaited-joy-to-supporters/ | 
uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "If you were working at a newspaper and had to tag this article, so it would be found with similar articles, what would 5 one or two word tags you would use?"
1. Garvey-Pardon  
2. Posthumous-Justice  
3. Black-Diaspora  
4. Biden-Legacy  
5. UNIA-History

uv run python -m newspaper --url=https://cnsmaryland.org/2025/01/19/marcus-garvey-pardon-brings-long-awaited-joy-to-supporters/ | 
uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "What 5 words best describe this article, content-wise?"
Posthumous pardon, racial justice, vindication, diaspora celebration, legacy

uv run python -m newspaper --url=https://cnsmaryland.org/2025/01/19/marcus-garvey-pardon-brings-long-awaited-joy-to-supporters/ |
uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "If you were working at a newspaper and had to tag this article, so it would be found with similar articles, what would 5 one or two word tags you would use? Rank them 1-5 by which most accurately describes the story." 
1. Garvey-pardon  
2. Posthumous-justice  
3. Black-activism  
4. Biden-clemency  
5. Jamaican-hero

uv run python -m newspaper --url=https://cnsmaryland.org/2025/01/19/marcus-garvey-pardon-brings-long-awaited-joy-to-supporters/ |
uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "If you were working at a newspaper and had to tag this article, so it would be found with similar articles, what would 5 one or two word tags you would use? Make them broad enough that they are not just specific to this story and could be helpful to find similar stories. Rank them 1-5 by which most accurately describes the story."
1. Pardon  
2. Civil-rights  
3. Legacy  
4. Activism  
5. Black-history

I think overall, this assignment was pretty interesting. It was a bit repetitive, as I just slightly changed the query to the LLM each time to attempt to have the LLM give me a variety of answers. It was fairly simple to think of changes for the LLM query, however I may have kept them too similar, as the answers didn’t change much. I think that this could've been a bit less tedious if there was a way to save the code I entered, straight into my notes, as I entered it into the terminal. To be honest I had a pretty easy time with this assignment workflow wise, besides the copying code into notes. I was pretty confused how this story was tagged barrack-obama in the first place. It mentioned him once, as was a minimal part of the article. In the future, if we do this for our own project, if we run this query for multiple stories at once, rank the options, and have a command that could select the most appropriate tag, and limit the number of tags to (1/110?) of the total number of articles. (or something of the sort). Obviously this would depend on the accuracy of the LLM and how much we trust them. It would also require all stories to fit in a finite number of tags. (unless we make the tags more general and less story specific).

