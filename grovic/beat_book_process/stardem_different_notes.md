
- Goal: Build an easy, interactive, narrative-free mini-website that pulls unique names from `people_md_de_va.csv`, uses context from `beatbook_revised.md`, and looks “super pretty”.
- Features:
  - Random draw card that uses each name once (localStorage) with reset.
  - Clean detail pages: Name, Title, brief context snippets (no narrative).
  - Optional Groq “maverick” expansion to provide concise additional info on click.
- Data/Logic:
  - Load people from CSV; dedupe variants (including scrambled names) via normalized name + letter-signature.
  - Pick best (longest, non-empty) sentence-cased title across duplicates.
  - Extract brief context lines from `beatbook_revised.md` with links/emails/phones stripped.
- UI:
  - Dark gradient, card-based theme; grid panels for People by Category.
  - Removed “Organizations (top mentions)” and “Places (top mentions)” per request.
- Fixes/Notes:
  - Addressed requirements path error by installing Flask directly or using absolute path.
  - Ensured no repeats both in random draw and category lists.
  - Provided Groq integration plan (requires `GROQ_API_KEY`) to show “More Info” via model `maverick`.


This was the summary o what I wanted to do. It worked for the moooost part. but my big thing that I wanted to work didn't. and that was when u clicked on one of the peoples names, it would call an LLM to tell you more context about this person based on their name and title. 

I think a tool like this would be super sick to go along with my beatbook (when i take ur advice and take the names: that are mostly incorrect out)
