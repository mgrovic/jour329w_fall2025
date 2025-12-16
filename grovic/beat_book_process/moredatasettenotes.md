Miles Grovic 10/08/2025

- Do the results make sense?
Yes, they are all based on the story, however sometimes they are TO locked in and are just the most occuring word. This sometimes makes them super super specifc, which itsn't the most usefuel. 

- Any surprising patterns?
Depending on story content, the list of key words will be ordered in dashes, numbers or no sort of ordering indicators. 
When you say one or two words, the LLM will defineitly favor giving one word answers. 


- Anything you don't like about this?
A lot I have already mentioned. Werid formatting, forced two words, and super niche and specifc terms (ie Forest buffers is a term not too many people are searching for I could only assume). We could definitely exclude Chesapeake Bay as a keyword, as that is already the topic, so we would have to specify in our prompt. 

With all this being said, I think there wasn't all that much wrong if we cleaned up our prompt, and were much more specific (ie give me a list of tags with the same format everytime (numbered 1-5) excluding the topic name (chesapeake bay). If possible use one word but if the tag requries two then use that required two words. Make it broad enough that if someone was searching through stories it would be easy enough to find them.)


Pt. 2

- What words or phrases did you try?
Sports
Fishing
Election
- Do the results make sense?
For sports, the results made total sense. The top story was about pickleball and how it helps caner patients etc. Fishing was interesting, as it seems like there were very few if any fishing stories, which then lead the embeddings to find sport stories, which I guess are the closest semanticlly to fishing. When I searched for elections, it was a similar result to my sport search, a good, clear result of stories that were centered around elections. 
- Anything you don't like about this?
I think that overall this is a very clinical way to search for key terms, without necessarily needing the word to appear in the story or its description. I do wish that if there were stories that did not have similar results, that datasette would somehow let us know, for example, if the emeddings were under .25, the site would alert us that there are no strong story matches. 