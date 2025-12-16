## Guide Build Notes

Goal: produce a clear, non‑technical “How to Make a Beat Book” using the artifacts in this folder plus prior assignments.

Sources referenced
- Scripts: extract_people.py, classify_people.py, classify_topics.py, combine_people.py, add_metadata.py, beatbook_narrative.py, generate_beatbook.py, beatbook_cleaner.py, beatbook_combiner.py, fix_beatbook.py
- Notes: bbd1notes.md, bbd3notes.md, collectionsnotes.md, datasettenotes.md, moredatasettenotes.md, embeddingsnotes.md, stardem_*_notes.md
- Drafts/outputs: beatbook_output.md, beatbook_narrative.md, beatbook_revised.md, beatbook_cleaned.md, beatbook_combined.md

LLM process
- Collected file inventory of grovic/beat_book_process
- Drafted an outline with 10 sections (prereqs → deliverables)
- Grounded each step in specific scripts and example commands
- Added guardrails for QA/fact‑checking and iteration

Deliverables created
- how_to_make_a_beat_book.md – main step‑by‑step guide
- copilot.md – narrative summary of this short session

Assumptions
- Scripts run from grovic/beat_book_process
- Data lives under data/ and prior utilities (e.g., utils/) are available if needed
- Minor script adjustments may be required depending on local data paths

Next steps
- Run the pipeline end‑to‑end on a small subset of stories
- Verify classifications and entity merges, then scale up
- Revise the draft Markdown and finalize a “revised” version

Copilot summary

Summary (for assignment submission)
- Goal: Build a non-technical, reporter-first “How to Make a Beat Book,” grounded in your existing scripts, notes, and prior drafts.
- Inputs: Used `extract_people.py`, `classify_people.py`, `classify_topics.py`, `combine_people.py`, `add_metadata.py`, `beatbook_narrative.py`, `generate_beatbook.py`, `beatbook_cleaner.py`, `beatbook_combiner.py`, plus notes (`bbd*`, collections/datasette/embeddings), and drafts (`beatbook_output.md`, `beatbook_revised.md`, `beatbook_combined.md`).
- Process: Inventoried folder contents, created a 10-section outline, emphasized narrative craft over code, added practical reporting routines, documents “how to read,” and ethics/accuracy guardrails; appended an appendix on “Future Stories” and “Past Stories.”
- Deliverables: `how_to_make_a_beat_book.md` (rewritten, narrative-focused), `copilot.md` (session summary).


This is a very short, practical, to the point beatbook guide. It explains the ideas, steps and overall tone of the beatbook very well. My biggest critque is it tells the reader how to create a beatbook by hand, not using code, an llm or any vibecoding resources (copilot etc). 

I think if a very smart person, with a plethera of time and resources had the oppurtunity to read this how to guide and create a beatbook, it would turn out quite well.

I took this feedback and added a section section, telling them how I made my beatbook, as a kind of, example guide as to what I did.

I took the notes from my 4 drafts and then final product and created a script that made a roadmap, teaching someone how to best create a beatbook like mine. The first part, telling the reader how it should look/be formatted, mixed with my steps and process, I think made it a very good how to guide. 

Pick your posion of either 
how someone would make a beatbook by hand - how_to_make_a_beat_book.md
or 
a specifc in depth, code focused - project_roadmap.md





