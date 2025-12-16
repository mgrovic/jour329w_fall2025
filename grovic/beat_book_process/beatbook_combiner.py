#!/usr/bin/env python3
"""
Combine two beat book markdown sources into one comprehensive, geography-centered
environment & aquaculture beat guide for the Easton Star Democrat.

ENHANCED VERSION: Emphasizes operational details, specific contacts with full info,
actionable checklists, and practical field guidance.

Usage (recommended to avoid 413 errors):
  uv run python beatbook_combiner.py \
    --source-a beatbook_output.md \
    --source-b beatbook_star_dem_environment_llama4_maverick.md \
    -m groq/meta-llama/llama-4-maverick-17b-128e-instruct \
    --summarize --sectional \
    -o beatbook_combined.md
"""

import argparse
import sys
from pathlib import Path
from textwrap import dedent
import llm

BASE_INSTRUCTIONS = dedent("""\
You are tasked with creating a HIGHLY ACTIONABLE environment and aquaculture beat guide for the Easton Star Democrat.

CRITICAL REQUIREMENTS:

**GEOGRAPHY IS CENTRAL**
- Every issue, source, institution, and story MUST specify location
- Primary: Talbot County; Secondary: Dorchester, Caroline, Kent, Queen Anne's counties
- Key waterways: Chesapeake Bay, Choptank River, Miles River, Tred Avon River, Chester River, Nanticoke River, Wye River
- Always note jurisdictional boundaries (county vs state vs federal)

**OPERATIONAL DEPTH REQUIRED**
- Don't just list—explain HOW to use the information
- Include contact details (phone/email when available)
- Provide access instructions (where to get documents, when meetings occur)
- Give specific examples with citations [Story Title] (docref: news/XXXX)

**ACTIONABLE, NOT ENCYCLOPEDIC**
- Every section must answer: "What does a reporter DO with this?"
- Include step-by-step checklists where appropriate
- Specify WHO to call for WHICH geographic area
- Tell reporters WHERE to go, WHEN to go, WHAT to bring

**SOURCES**
Source A (beatbook_output.md): Comprehensive reference with 100+ contacts, story citations, geographic detail
Source B (beatbook_star_dem_environment_llama4_maverick.md): Structured framework with checklists and workflows

**YOUR TASK**: Combine the structure of Source B with the rich operational detail of Source A.

FORMAT: Markdown with ## headers, ### subheaders, bullet points, bold for **names/places** on first mention.
TONE: Direct, practical, professional journalism.
CITATIONS: [Story Title] (docref: news/XXXX)
""")

# Enhanced section specifications with specific requirements
SECTION_SPECS = [
    (1, "Purpose and Local Context", "500-700", dedent("""\
        OPEN with clear geographic map: Talbot County (primary), list key waterways, towns.
        Explain WHY geography matters (working waterfront, watersheds, jurisdictional complexity).
        Include 4-5 recent story citations showing coverage breadth.
        Set stage for why this beat requires geographic precision.
        """)),
    
    (2, "Background Briefing (Core Issues)", "1000-1500", dedent("""\
        For EACH issue, specify geography:
        - Water quality: WHICH rivers/counties are worst? Name specific impaired waterways.
        - Fisheries: WHERE are key harvesting areas? Map species to locations.
        - Climate change: WHICH shorelines face greatest threats?
        - Industrial pollution (DAF): WHY concentrated in Caroline County? Affected watersheds?
        - Conservation: WHICH areas have preservation priority?
        
        Include 6-8 story citations across different geographies.
        Note jurisdictional complexity: "State waters, county planning, federal wetlands..."
        """)),
    
    (3, "Aquaculture Deep Dive", "1000-1200", dedent("""\
        CREATE GEOGRAPHIC MAP of aquaculture:
        - "Oyster farming concentrated in: Eastern Bay (Queen Anne's), Miles River (Talbot)..."
        - List shore-based facilities with locations
        - Map siting conflicts by geography: "St. Michaels harbor conflicts..."
        - Explain regulatory jurisdiction by geography
        
        MUST INCLUDE: Aquaculture Proposal Checklist (8-10 items) with:
        1. Location details (GPS, acreage, depth, proximity to channels)
        2. Species and methods
        3. Regulatory permits needed
        4. Environmental assessments required
        5. Community response tracking
        6. Conflict identification
        7. Economic projections
        8. Applicant background checks
        """)),
    
    (4, "Source Profiles (People)", "1800-2200", dedent("""\
        CRITICAL: Extract 18-22 key contacts from Source A.
        
        ORGANIZE BY:
        1. State officials (statewide coverage)
        2. County officials (separate by county)
        3. Waterway-specific (by river/creek)
        4. Regional environmental leaders
        5. Scientists/researchers
        6. Watermen/industry
        
        FOR EACH CONTACT:
        - **Name in bold** - Title, Organization
        - **Geographic coverage**: "Choptank River watershed (Caroline/Talbot/Dorchester)"
        - **Expertise**: Specific topics
        - **When to call**: Specific situations
        - **Contact info**: Phone/email if available from Source A
        - **Recent activity**: Quote or action with citation [Story] (docref: XXX)
        
        PRIORITIZE: Sources appearing multiple times in Source A, those with specific geographic mandates.
        
        EXAMPLES TO INCLUDE (extract details from Source A):
        - Matt Pluta (Choptank Riverkeeper)
        - Annie Richards (Chester Riverkeeper)
        - Alan Girard (CBF Eastern Shore Director)
        - Chris Van Hollen (US Senator)
        - Johnny Mautz (State Senator - multi-county)
        - Ward Slacum (Oyster Recovery Partnership)
        - Jeff Harrison (Talbot Watermen)
        - Sara Love (Delegate)
        - Christopher Judy (DNR Shellfish)
        - Allison Colden (CBF Maryland)
        """)),
    
    (5, "Organization Overviews (Institutions)", "1000-1400", dedent("""\
        List 12-15 key institutions from Source A.
        
        FOR EACH:
        - **Organization name**
        - **Geographic jurisdiction**: Statewide? County-specific? Which waterways?
        - **Local offices**: "ShoreRivers has three riverkeepers: Chester (Kent/QA), Choptank (Caroline/Talbot/Dorchester), Sassafras (Kent/Cecil)"
        - **Key programs**: Name specific initiatives with geographic focus
        - **Contact strategy**: "Get on press list at [contact]; attend quarterly meetings [when/where]"
        - **Recent coverage**: 1-2 citations showing their work
        - **What they regulate/do**: Jurisdictional clarity
        
        INCLUDE: DNR, MDE, Chesapeake Bay Foundation, ShoreRivers, Talbot/Caroline/Dorchester County Councils, Army Corps, NOAA, ASMFC, Talbot Watermen Association, Eastern Shore Land Conservancy, Chesapeake Bay Trust, MARBIDCO
        
        Note jurisdictional overlap: "Aquaculture: DNR for leases, counties for shore access, Corps for wetlands"
        """)),
    
    (6, "Documents, Data, and Tools", "700-900", dedent("""\
        For each document type:
        - What it is
        - WHERE to get it: Specific office/website
        - WHAT to look for: Key fields/sections
        - Geographic relevance: Which areas covered
        - Specific example from Source A with citation
        
        MUST INCLUDE:
        1. Aquaculture lease applications (DNR Shellfish Division)
        2. Oyster stock assessments (annual, DNR)
        3. Blue crab winter dredge survey (DNR)
        4. ASMFC striped bass assessments
        5. MDE discharge permits (NPDES)
        6. MDE inspection reports
        7. Erosion/sediment control plans
        8. Water quality monitoring data (ShoreRivers, CBF, DNR)
        9. Dead zone measurements (VIMS)
        10. County comprehensive plans
        
        **FOIA/PRA Playbook** (5-7 steps):
        1. Identify specific document needed
        2. Determine jurisdiction (county/state/federal)
        3. Draft request (be specific)
        4. Submit to correct office (list contacts)
        5. Follow up timeline (5 days state, 10 days county)
        6. Appeal process if denied
        7. Alternative sources if blocked
        """)),
    
    (7, "Story Opportunities (with integrated reporting tips)", "800-1000", dedent("""\
        Provide 7-9 CONCRETE story ideas.
        
        FOR EACH:
        - **Story headline/concept**
        - **Location**: Specific county, waterway, town
        - **Documents to obtain**: List 3-4 specific docs with where to get them
        - **Who to call**: List 4-6 specific sources with their geographic expertise
        - **Angles**: 2-3 potential narrative approaches
        - **Geographic dimension**: Why this location matters
        - **Timing**: When to pursue (seasonal, legislative, etc.)
        
        EXAMPLE FORMAT:
        **Story: Aquaculture Siting Conflicts in St. Michaels Harbor**
        - Location: St. Michaels, Miles River, Talbot County
        - Obtain: DNR lease applications for Miles River (dnr.maryland.gov), St. Michaels harbor master logs (town hall), planning commission minutes (town website)
        - Call: Jeff Harrison (Talbot Watermen - 410-XXX-XXXX), St. Michaels harbor master, Christopher Judy (DNR Shellfish), local oyster farmers, adjacent property owners
        - Angles: Economic benefits vs navigation safety; tourism impact; working waterfront conflicts
        - Why here: St. Michaels = high-value tourism + active harbor + growing aquaculture
        - Timing: Spring when lease applications typically filed
        
        Draw from Source A citations and issues.
        """)),
    
    (8, "Field Reporting and Safety", "400-500", dedent("""\
        PRACTICAL FIELD GUIDANCE:
        
        **By Location Type:**
        - Aquaculture sites (water access): How to arrange boat access, what to bring, tide considerations
        - Construction sites: Permission requirements, safety gear, who to notify
        - Wildlife refuges: Permit requirements by facility
        - County facilities: Hours, parking, access restrictions
        
        **Field Day Checklist:**
        1. Weather/tide check (specific websites/resources)
        2. Location scouting (Google maps, property boundaries)
        3. Equipment list: Camera, notebook, waders, life jacket, phone charger, business cards
        4. Contacts pre-arranged: Call 24hrs ahead
        5. Safety notification: Tell editor where going, expected return
        6. Backup plan: Weather-dependent alternative location
        
        **Geographic Safety Considerations:**
        - Tilghman Island oyster operations: Check tides at [website], park at [location]
        - Caroline County DAF sites: Private property, get written permission
        - Blackwater Wildlife Refuge: Visitor permit required, check hours
        - Winter water reporting: Hypothermia risk, buddy system required
        
        **Seasonal access issues by county**
        """)),
    
    (9, "Beat Cadence and Calendar", "500-700", dedent("""\
        **MONTHLY CALENDAR** (by month, listing specific recurring events):
        
        January: Blue crab survey results (DNR); Legislative session begins (Annapolis)
        February: Oyster season peak; Committee hearings (track environmental bills)
        March: Waterfowl migration reporting; Legislative session ends
        April: Aquaculture lease applications filed; Spring planting season
        [Continue through December]
        
        **RECURRING MEETINGS** (with dates/times/locations):
        - Talbot County Council: 2nd/4th Tuesday, 6pm, County Office Building, Easton
        - Caroline County Commissioners: [day/time/location]
        - Dorchester County Council: [day/time/location]
        - Maryland Aquaculture Coordinating Council: Quarterly (dates vary, Annapolis)
        - ShoreRivers board meetings: [when/where]
        
        **GEOGRAPHIC ROTATION** (4-week cycle):
        Week 1: Talbot County focus (council meeting, local issues)
        Week 2: Dorchester/Caroline (check in with sources)
        Week 3: Regional Bay-wide (CBF, DNR updates)
        Week 4: Kent/Queen Anne's (alternate coverage)
        
        **ANNUAL EVENTS**:
        - October: US Oyster Festival (St. Mary's County)
        - November: Waterfowl Festival (Easton)
        - [List 8-10 more with locations]
        
        **SOURCE CHECK-IN SCHEDULE**:
        Weekly: Riverkeepers (Mon AM)
        Bi-weekly: DNR contacts, county officials
        Monthly: Scientists, advocacy groups
        Quarterly: Federal officials
        """)),
    
    (10, "Ethics, Legal, and Accuracy Checks", "400-500", dedent("""\
        **GEOGRAPHIC PITFALLS**:
        - Watershed boundaries ≠ county boundaries: "Pollution in Caroline affects Dorchester waters"
        - Jurisdictional complexity: "State lease in county waters with federal wetlands oversight"
        - Attribution by geography: "This is Choptank issue → call Matt Pluta, not Annie Richards"
        
        **ACCURACY CHECKS**:
        1. Verify geographic details: Which river, which county, which tributary?
        2. Cross-check jurisdiction: Who actually regulates this?
        3. Confirm source geographic expertise: Do they cover this area?
        4. Multiple sources for contested claims
        5. Scientific claims: Cite peer-reviewed studies
        
        **COMMON PITFALLS FROM SOURCE A**:
        - [Extract 5-6 specific verification warnings from Source A]
        - Biased sources in aquaculture debates
        - Incomplete water quality data
        - Outdated regulatory information
        - Conflicting scientific studies
        
        **LEGAL CONSIDERATIONS**:
        - Active litigation: Label clearly, avoid prejudging
        - Scientific uncertainty: Use appropriate caveats
        - Permit disputes: Present all sides
        - Property rights vs public waters
        """)),
    
    (11, "Contact List", "500-700", dedent("""\
        **QUICK REFERENCE TABLE** (not repetitive of Section 4—this is streamlined)
        
        Organize as:
        
        **STATE-LEVEL:**
        Name | Title | Organization | Geographic Coverage | Phone | Email | Primary Topics
        
        **TALBOT COUNTY:**
        [5-6 key contacts]
        
        **DORCHESTER COUNTY:**
        [3-4 key contacts]
        
        **CAROLINE COUNTY:**
        [3-4 key contacts]
        
        **KENT COUNTY:**
        [2-3 key contacts]
        
        **QUEEN ANNE'S COUNTY:**
        [2-3 key contacts]
        
        **WATERWAY-SPECIFIC:**
        Choptank River: Matt Pluta (ShoreRivers) - [phone] - Caroline/Talbot/Dorchester
        Chester River: Annie Richards (ShoreRivers) - [phone] - Kent/Queen Anne's
        [Continue for other rivers]
        
        **FEDERAL:**
        [3-4 contacts]
        
        Total: 25-30 contacts with FULL contact details extracted from Source A.
        Include office phone, cell if available, email, best time to reach.
        """)),
    
    (12, "Citations and Further Reading", "300-400", dedent("""\
        Organize 15-20 story citations BY GEOGRAPHY AND TOPIC:
        
        **TALBOT COUNTY:**
        - Aquaculture: [3-4 citations]
        - Water quality: [2-3 citations]
        - Development: [2-3 citations]
        
        **CAROLINE COUNTY (DAF focus):**
        - [4-5 DAF-related citations]
        
        **DORCHESTER COUNTY:**
        - [2-3 citations]
        
        **REGIONAL/BAY-WIDE:**
        - [4-5 citations]
        
        **MULTI-COUNTY ISSUES:**
        - [2-3 citations]
        
        For each: [Story Title] (docref: news/XXXX) - Brief (10-15 word) description of what it illustrates
        
        **FURTHER READING:**
        - Key reports from DNR, MDE, CBF (with URLs)
        - Useful datasets (with access instructions)
        - Background reading on Chesapeake Bay issues
        """)),
]

def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    return p.read_text(encoding="utf-8")

def get_model(model_name: str | None):
    if model_name:
        try:
            return llm.get_model(model_name)
        except Exception:
            for prefix in ("groq", "openai", "anthropic", "ollama"):
                cand = f"{prefix}/{model_name}"
                try:
                    return llm.get_model(cand)
                except Exception:
                    pass
            raise
    return llm.get_model()

def _resp_text(resp) -> str:
    if hasattr(resp, "text"):
        t = resp.text
        if callable(t):
            try:
                return t()
            except Exception:
                return ""
        return t
    return str(resp)

def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 0) -> list[str]:
    chunks = []
    i = 0
    n = len(text)
    while i < n:
        end = min(i + chunk_size, n)
        chunks.append(text[i:end])
        i = end - overlap
        if i <= 0:
            break
    return chunks

def summarize_chunk(model, chunk: str, label: str) -> str:
    """Enhanced summarization that preserves operational details"""
    prompt = f"""Condense this {label} fragment while PRESERVING operational details.

MUST KEEP:
- Geographic specifics: counties, rivers, towns, specific locations
- Key contacts: name + title + organization + phone/email + geographic coverage area
- Institutions: full name + jurisdiction + what they regulate + where located
- Major environment/aquaculture issues: paired with specific places
- Story citations: [Title] (docref: news/XXXX)
- Contact details: phone numbers, email addresses, office locations
- Meeting schedules: days, times, locations
- Specific document names and where to get them
- Concrete examples and case studies

REMOVE:
- Repetitive general statements
- Vague descriptions
- Filler text
- Redundant context

FRAGMENT:
{chunk[:3500]}
"""
    resp = model.prompt(prompt)
    return _resp_text(resp).strip()

def summarize_source(model, text: str, label: str, target_words: int = 1200) -> str:
    """Enhanced summarization focusing on extracting actionable details"""
    raw_chunks = chunk_text(text, chunk_size=4000)
    partial_summaries = []
    for idx, ch in enumerate(raw_chunks, 1):
        print(f"  Summarizing {label} chunk {idx}/{len(raw_chunks)} (preserving operational details)", file=sys.stderr)
        partial = summarize_chunk(model, ch, label)
        partial_summaries.append(partial)
    
    merged = "\n\n".join(partial_summaries)
    
    final_prompt = f"""Merge the following partial summaries of {label} into a single high-signal digest (~{target_words} words).

CRITICAL: Preserve ALL operational details:
- Contact information (names, titles, organizations, phone/email, geographic coverage)
- Specific locations (counties, rivers, towns, addresses)
- Meeting details (days, times, locations)
- Document sources (where to obtain, what to look for)
- Story citations with docref numbers
- Institutional jurisdictions and what they regulate
- Specific programs and initiatives with geographic focus

Unify and deduplicate while KEEPING specifics.
Select 15-20 strongest citations [Title] (docref: news/XXXX).
Keep concrete examples over abstract descriptions.

PARTIAL SUMMARIES:
{merged[:25000]}
"""
    resp = model.prompt(final_prompt)
    return _resp_text(resp).strip()

def build_master_prompt(src_a: str, src_b: str, summarized: bool) -> str:
    tag_a = "SUMMARIZED (preserving operational details) beatbook_output.md" if summarized else "beatbook_output.md"
    tag_b = "SUMMARIZED beatbook_star_dem_environment_llama4_maverick.md" if summarized else "beatbook_star_dem_environment_llama4_maverick.md"
    limit = 25000 if not summarized else 120000
    
    extraction_reminder = dedent("""\
    
    **EXTRACTION PRIORITIES FROM SOURCE A (beatbook_output.md):**
    - Extract 18-22 KEY CONTACTS with full details: name, title, org, geographic coverage, phone/email if available, expertise, when to call, recent quotes with citations
    - Extract SPECIFIC meeting schedules: day, time, location for county councils, state agencies
    - Extract PHONE NUMBERS and EMAIL ADDRESSES when present
    - Extract SPECIFIC STORY CITATIONS: [Title] (docref: news/XXXX) - aim for 15-20 across all sections
    - Extract OPERATIONAL DETAILS: where to get documents, what to look for in them, specific examples
    - Extract GEOGRAPHIC SPECIFICS: which counties, rivers, towns are affected by which issues
    
    **STRUCTURE FROM SOURCE B (beatbook_star_dem_environment_llama4_maverick.md):**
    - Use the 12-section framework
    - Include all checklists (Aquaculture Proposal, Field Day, FOIA/PRA)
    - Follow the actionable, practical tone
    - Organize by geography within sections
    
    **COMBINE BY:**
    - Taking Source B's structure and filling it with Source A's specific operational details
    - Making everything geographic: every issue, source, institution tied to place
    - Making everything actionable: tell reporters exactly what to do, not just what exists
    """)
    
    return f"""{BASE_INSTRUCTIONS}
{extraction_reminder}

=== SOURCE A: {tag_a} ===
{src_a[:limit]}

=== SOURCE B: {tag_b} ===
{src_b[:limit]}

=== END SOURCES ===
"""

def generate_section(model, master_prompt: str, num: int, title: str, range_spec: str, special_instructions: str) -> str:
    """Enhanced section generation with specific requirements"""
    section_prompt = f"""{master_prompt}

Generate ONLY section ## {num}) {title}.
Target words: {range_spec}.

**SPECIFIC REQUIREMENTS FOR THIS SECTION:**
{special_instructions}

**CRITICAL REMINDERS:**
- Extract specific operational details from Source A (phone numbers, meeting times, specific locations)
- Tie everything to geography (counties, rivers, towns)
- Make it actionable: tell reporters exactly what to do
- Include citations [Story Title] (docref: news/XXXX)
- Use bullet points, tables, and checklists for scannability
- Bold **key names and places** on first mention

Do not include other sections or a global introduction.
Return ONLY the requested section in Markdown format.
"""
    resp = model.prompt(section_prompt)
    text = _resp_text(resp).strip()
    
    # Ensure proper header format
    if not text.lower().startswith(f"## {num}"):
        text = f"## {num}) {title}\n\n{text}"
    
    return text

def single_pass(model, master_prompt: str) -> str:
    """Single-pass generation with enhanced instructions"""
    full_requirements = "\n\n".join([
        f"**Section {num}** ({title}, {range_spec} words):\n{instructions}"
        for num, title, range_spec, instructions in SECTION_SPECS
    ])
    
    resp = model.prompt(f"""{master_prompt}

Generate the FULL 12-section guide now.
Ensure total word count 6000-10000.

**SECTION-SPECIFIC REQUIREMENTS:**
{full_requirements}

**OVERALL REQUIREMENTS:**
- Extract 18-22 contacts with full details in Section 4
- Include all checklists (Aquaculture Proposal, Field Day, FOIA/PRA)
- 15-20 story citations across all sections
- Everything tied to specific geography
- Operational details (phone numbers, meeting times, where to get documents)
- Actionable guidance throughout
""")
    return _resp_text(resp)

def main():
    ap = argparse.ArgumentParser(description="Combine two beatbook markdown sources into one structured guide (ENHANCED VERSION).")
    ap.add_argument("--source-a", default="beatbook_output.md")
    ap.add_argument("--source-b", default="beatbook_star_dem_environment_llama4_maverick.md")
    ap.add_argument("-m", "--model")
    ap.add_argument("-o", "--output", default="beatbook_combined.md")
    ap.add_argument("--dry-run", action="store_true", help="Print combined prompt and exit")
    ap.add_argument("--summarize", action="store_true", help="Summarize both sources first (preserving operational details)")
    ap.add_argument("--sectional", action="store_true", help="Generate each section in separate calls (RECOMMENDED)")
    args = ap.parse_args()

    try:
        src_a = read_file(args.source_a)
        src_b = read_file(args.source_b)
    except FileNotFoundError as e:
        print(f"Missing file: {e}", file=sys.stderr)
        sys.exit(1)

    model = get_model(args.model)
    print(f"Using model: {getattr(model, 'model_id', args.model)}", file=sys.stderr)

    if args.summarize:
        print("Summarizing sources (preserving operational details)...", file=sys.stderr)
        src_a = summarize_source(model, src_a, "beatbook_output.md", target_words=1200)
        src_b = summarize_source(model, src_b, "beatbook_star_dem_environment_llama4_maverick.md", target_words=800)
        print(f"Source A summarized to ~{len(src_a.split())} words", file=sys.stderr)
        print(f"Source B summarized to ~{len(src_b.split())} words", file=sys.stderr)

    master_prompt = build_master_prompt(src_a, src_b, summarized=args.summarize)

    if args.dry_run:
        print(master_prompt)
        print("\n\n=== SECTION-SPECIFIC INSTRUCTIONS ===\n")
        for num, title, range_spec, instructions in SECTION_SPECS:
            print(f"\n**Section {num}: {title}** ({range_spec} words)")
            print(instructions)
        sys.exit(0)

    if args.sectional:
        print("Section-by-section generation (ENHANCED)...", file=sys.stderr)
        parts = []
        out_path = Path(args.output)
        
        for num, title, rng, instructions in SECTION_SPECS:
            print(f"\nGenerating Section {num}: {title} ({rng} words)...", file=sys.stderr)
            sec_md = generate_section(model, master_prompt, num, title, rng, instructions)
            parts.append(sec_md)
            
            # Write incrementally so we don't lose progress
            out_path.write_text("\n\n".join(parts), encoding="utf-8")
            
            sec_words = len(sec_md.split())
            print(f"  Section {num} complete: {sec_words} words", file=sys.stderr)
            
        final_md = "\n\n".join(parts)
    else:
        print("Single-pass generation (ENHANCED)...", file=sys.stderr)
        final_md = single_pass(model, master_prompt)
        Path(args.output).write_text(final_md, encoding="utf-8")

    words = len(final_md.split())
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"COMPLETE: Total word count: {words}", file=sys.stderr)
    
    if words < 6000:
        print(f"⚠️  WARNING: Below target (6000 minimum). Consider regenerating with --sectional.", file=sys.stderr)
    elif words > 10000:
        print(f"⚠️  WARNING: Above target (10000 maximum). May need editing.", file=sys.stderr)
    else:
        print(f"✓ Within target range (6000-10000 words)", file=sys.stderr)
    
    print(f"{'='*60}", file=sys.stderr)
    print(f"Output written to: {args.output}", file=sys.stderr)

if __name__ == "__main__":
    main()