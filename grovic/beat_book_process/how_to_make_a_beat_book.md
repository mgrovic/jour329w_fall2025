# How to Make a Beat Book

This guide is about building a reporter’s beat book: a living, practical reference that helps you find stories, understand stakeholders, and work efficiently in a specific place. It focuses on craft and structure over code. Use the scripts and notes in this folder as supporting tools, not the main event.

## What a Beat Book Should Do
- Explain the beat’s scope and local context in plain language.
- Map the people and institutions that actually move the story.
- Turn recurring issues into clear themes with examples and evidence.
- Offer workflows for reporting: how to prepare, who to call, where to go, what to ask, how to verify.
- Stay grounded in the geography, history, and lived experience of the communities you cover.

## 1) Gather and Read Deeply
- Pull together stories, notes, clippings, council agendas, press releases, and your own interviews. Skim, then read closely.
- Mark anything that repeats: names, institutions, places, arguments, jargon. Recurrence signals importance.
- For this class, start with your own prior assignments and the materials in [grovic/beat_book_process](.).

Output: a short memo describing the beat in your own words—what it is, where it happens, why it matters locally.

## 2) Map Stakeholders by Influence, Not Just Category
- List the actors that keep showing up: officials, advocates, scientists, watermen, businesses, community leaders.
- For each, note what power they actually have, when they appear in news, and how they tend to frame issues.
- Group them by influence and geography (e.g., “Talbot County Council,” “Choptank watershed scientists,” “DNR Shellfish,” “ShoreRivers”).

Output: a tidy “people and orgs to watch” section that’s brief, specific, and local. Prioritize by recurrence and relevance.

## 3) Identify Themes and Flashpoints
- Turn repeated topics into 8–12 sub‑beats (e.g., aquaculture leasing conflicts, septic regulations, stormwater fees, Bay cleanup funding, rural land use, flooding and resilience).
- For each sub‑beat, write:
  - what it covers and why it matters here
  - who the stakeholders are and what they argue
  - where it shows up (specific rivers, towns, councils)
- Cite real stories or documents when you can—evidence keeps your beat book honest.

Output: a “Sub‑Beats” section with short, vivid explanations tied to places and people.

## 4) Build Practical Reporting Routines
- For each sub‑beat, define a routine: what to check weekly/monthly, where to be physically, who to call first, who to call second.
- Examples: “Before a County Council meeting, pull agenda packets and staff reports. After, call the sponsor, the critic, and one affected resident. Then check staff memos and permitting databases.”
- Include realistic email/phone templates for officials, scientists, and community sources.

Output: a “How I Work This Beat” section—checklists and call trees, not theory.

## 5) Documents, Data, and How to Read Them
- List the core documents you actually use: aquaculture lease applications, oyster stock assessments, Bay water quality reports, county planning documents, enforcement actions.
- For each, show where to get it, what fields matter, and common red flags.
- Tie documents to places and recurring disputes (e.g., “Miles River leases,” “Talbot stormwater hearings,” “Choptank monitoring”).

Output: a documents/data section that teaches a new reporter how to read and use them, with local examples.

## 6) Ethics and Accuracy in Local Context
- Be explicit about fairness: who gets quoted, who gets context, who gets follow‑up.
- Note common pitfalls: advocacy framing that collapses complexity, selective data, meeting theater.
- Commit to verifying numbers, names, and jurisdictions. Clarify what each agency can and cannot do.

Output: a short “Guardrails” section you’ll actually follow.

## 7) Structure the Beat Book
Organize your beat book so it’s easy to use:
- Beat Overview: two or three paragraphs in plain language.
- Sub‑Beats: 8–12 entries with stakeholders, places, why it matters.
- People & Orgs to Watch: grouped by sector with notes on influence and geography.
- Documents & Data: what to pull, how to read, where to get it.
- Reporting Routines: checklists and contact trees.
- Tips: how to avoid getting spun, when to go into the field, how to read water quality reports.
- Open Questions: 10–15 grounded story ideas that aren’t answered yet.

Use the drafts in this folder—[beatbook_output.md](beatbook_output.md), [beatbook_combined.md](beatbook_combined.md), and [beatbook_revised.md](beatbook_revised.md)—as raw material. Edit for clarity, locality, and actionability.

## 8) Draft the Voice
- Write clean Markdown with clear headers, short paragraphs, and concrete nouns. Avoid generic national framing unless it truly applies.
- Keep geography central. Name rivers, towns, counties. Respect jurisdictional boundaries.
- Make it practical: “Call X for Y,” “Check Z before the meeting,” “If A happens, verify B with C.”

## 9) Fact‑Check and Revise
- Read through once for structure, once for precision. Fix names, titles, places, dates.
- Confirm powers and limits of agencies and councils.
- Ensure every tip is realistic and locally grounded. Remove fluff.

Optional supporting tools in this folder can help you polish or restructure, but the goal is a reporter‑friendly manual:
- [beatbook_narrative.py](beatbook_narrative.py) can turn bullet lists into flowing text.
- [beatbook_cleaner.py](beatbook_cleaner.py) and [beatbook_combiner.py](beatbook_combiner.py) can help reorganize sections.

## 10) Deliverables
- Your beat book (Markdown) in this directory, written for a non‑technical reporter.
- A short process note in [guide_notes.md](guide_notes.md) explaining how you built it and what you’d improve.
- A narrative summary of your Copilot/LLM session in [copilot.md](copilot.md).

## Common Pitfalls (and Fixes)
- Too many names, not enough guidance → Cut lists; expand “how to use” notes.
- Vague geography → Add specific rivers, towns, counties, and jurisdictions.
- Generic advice → Replace with local examples and real workflows.
- Unverified claims → Add citations or remove; better to be precise than broad.

---
A beat book is a promise to future you: it saves time, keeps you fair, and makes your reporting sharper. Keep it small, strong, and local—and update it as the beat evolves.

## Appendix: Sections for Future and Past Stories
Design two short, reusable sections that keep your reporting pipeline healthy and retrospective insights accessible.

### Future Stories
- Pitch Queue: 6–12 ideas, each with a one‑line nut graf, key sources, and the first document you’ll pull. Tie each pitch to a specific place (river/town/county).
- Calendar & Triggers: upcoming council agendas, permit milestones, seasonal cycles (oyster harvests, monitoring releases), grant deadlines.
- Pre‑Reporting Checklist: what to read, who to call first/second, field visit plan (where to go, who to meet, what to observe).
- Risk & Verification Notes: what could be wrong or missing; how you’ll check numbers, jurisdictions, and claims.

Structure example:
- Title: “Miles River lease expansion debate”
- Why now: DNR hearing scheduled; local opposition forming in St. Michaels.
- Place: Miles River (Talbot County) — lease coordinates.
- First calls: DNR Shellfish; Talbot Council staff; ShoreRivers; nearby watermen.
- First docs: lease application; past minutes; water quality reports.

### Past Stories
- Coverage Index: a list of relevant stories you (or your outlet) have run, with a one‑line summary and what changed afterward.
- Stakeholder Follow‑Ups: note promises/commitments made (by agency, council, company) and whether they happened.
- Lessons Learned: reporting techniques that worked, pitfalls, missing voices, and better sources discovered later.
- Open Threads: unresolved questions and what evidence you still need.

Structure example:
- Headline: “Choptank monitoring expansion announced”
- Outcome: monitoring began; first data published quarterly.
- Follow‑ups: county budget increased; community group formed.
- What worked: early call to Riverkeeper yielded technical context; FOIA for procurement timeline.
- Still open: long‑term funding; data accessibility.
