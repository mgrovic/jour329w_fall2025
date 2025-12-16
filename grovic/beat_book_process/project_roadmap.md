# Creating an AI-Powered Journalism Beatbook: A Complete Roadmap

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites and Setup](#prerequisites-and-setup)
3. [Phase 1: Data Preparation and Extraction](#phase-1-data-preparation-and-extraction)
4. [Phase 2: Initial Beatbook Generation](#phase-2-initial-beatbook-generation)
5. [Phase 3: Refinement and Organization](#phase-3-refinement-and-organization)
6. [Phase 4: Source Integration](#phase-4-source-integration)
7. [Phase 5: Quality Control and Fact-Checking](#phase-5-quality-control-and-fact-checking)
8. [Tools and Technologies](#tools-and-technologies)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Best Practices and Lessons Learned](#best-practices-and-lessons-learned)

## Project Overview

### What You'll Accomplish
This roadmap guides you through creating a comprehensive journalism beatbook using AI tools. A beatbook is a journalist's reference guide containing key sources, locations, organizations, and background information for covering a specific topic or geographic area.

### End Goal
You'll produce a professional beatbook that includes:
- Well-organized topical sections with narrative guidance
- Geographic focus by county/region
- Comprehensive source directory with context and expertise areas
- Practical reporting instructions and contact strategies
- Fact-checked, accurate information

### Expected Timeline
- **Total Time**: 3-4 weeks (part-time)
- **Phase 1**: 3-5 days
- **Phase 2**: 1 week
- **Phase 3**: 3-5 days
- **Phase 4**: 1 week
- **Phase 5**: 3-5 days

> **Note**: This process involves significant iteration and refinement. Expect to cycle through phases multiple times.

## Prerequisites and Setup

### Required Skills
- Basic Python programming
- Command line familiarity
- JSON/CSV data handling
- Text editing and markdown

### Required Tools
- Python 3.8+
- API access to AI services (Groq, Anthropic Claude, or similar)
- Text editor capable of handling large files
- Spreadsheet software (Excel/Google Sheets)

### Data Requirements
- **News story dataset** in JSON format with fields:
  - `docref`: Document reference
  - `title`: Article headline
  - `byline`: Author information
  - `content`: Full article text
- **Minimum 40-50 articles** for meaningful results

### Initial Setup

1. **Create project directory structure**:
```
beatbook-project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
├── scripts/
├── drafts/
└── final/
```

2. **Install required Python packages**:
```bash
pip install anthropic groq pandas json markdown
```

3. **Set up API credentials** in environment variables or config file

## Phase 1: Data Preparation and Extraction

### Objective
Transform raw news articles into structured metadata that will inform your beatbook creation.

### Step 1.1: Develop Entity Extraction Prompt

Create a prompt that extracts key information from news articles:

```python
EXTRACTION_PROMPT = """
You extract structured entities (people, places, organizations) from LOCAL NEWS stories
all centered on the same topic/beat. Focus on entities that matter for a beat book
(long-term coverage). Prefer government officials, recurring stakeholders, key locations,
formal organization names.

Return ONLY a single JSON object with keys:
- docref: copy from input if present (else null)
- people: list of important people with titles (strings)
- geographic_focus: list of place names (strings)
- key_institutions: list of org names (strings)
- environmental_focus: list of environmental themes (strings)
- impact: which population is most impacted

Rules:
- Do not include duplicates
- Only include entities clearly mentioned
- If none found for a category, return an empty list
- List 1-6 most important people based on story focus
- Exclude the source publication name
"""
```

### Step 1.2: Test and Refine Extraction

1. **Start small**: Test on 5-10 articles first
2. **Iterate on prompt**: Based on results, adjust:
   - Add more examples for better category understanding
   - Specify title/position requirements for people
   - Clarify geographic scope (local vs. national)

> **💡 Pro Tip**: Give many specific examples rather than few general ones. LLMs perform better with concrete examples than abstract categories.

### Step 1.3: Run Full Extraction

```python
# Example extraction script structure
def extract_entities(articles, model="groq/meta-llama/llama-4-maverick-17b-128e"):
    results = []
    for article in articles:
        # Send article to LLM with extraction prompt
        # Parse JSON response
        # Handle errors and retries
        results.append(extracted_data)
    return results
```

**Expected Output**: JSON file with structured entities from all articles

> **⚠️ Warning**: Token limits can cause failures. Consider splitting long articles or using models with larger context windows.

## Phase 2: Initial Beatbook Generation

### Objective
Create your first complete beatbook draft using the extracted entities.

### Step 2.1: Design Beatbook Structure Prompt

Your beatbook generation prompt should specify:
- Overall organization (geographic, topical, or hybrid)
- Section types (background, key players, reporting strategies)
- Writing style (narrative vs. reference)
- Specific inclusions (contact strategies, story angles)

### Step 2.2: Choose Your AI Model

Based on the project notes, **Maverick (Llama-4-Maverick-17b-128e)** performed best for:
- Maintaining consistency across sections
- Including specific details
- Proper geographic organization

### Step 2.3: Generate Initial Draft

1. **Batch processing**: Process extracted data in chunks to avoid overwhelming the model
2. **Include resume functionality**: Long generations can fail partway through
3. **Save incremental progress**: Don't lose work to API timeouts

```python
def generate_beatbook_batch(batch_data, batch_number, total_batches):
    prompt = f"""
    Create a journalism beatbook section (batch {batch_number}/{total_batches})
    using this data: {batch_data}
    
    Include:
    - Geographic organization by county/region
    - Key sources with expertise areas
    - Background context
    - Reporting strategies
    - Story angles and seasonal considerations
    """
    # Process and return section
```

### Expected Outcomes
- **Draft 1 characteristics**:
  - Well-organized structure
  - Strong narrative flow
  - May lack specific details
  - Good instructional content

> **Common Issue**: Random document references (`docref: news/19B9101A54E5E250`) may appear. Clean these in post-processing.

## Phase 3: Refinement and Organization

### Objective
Combine the strengths of multiple drafts while addressing their individual weaknesses.

### Step 3.1: Generate Complementary Draft

Create a second draft optimized for different strengths:
- More detailed information
- Expanded source listings
- Specific examples and case studies

### Step 3.2: Analyze Draft Strengths

Document the characteristics of each draft:
- **Draft 1**: Comprehensive encyclopedia (reference tool)
- **Draft 2**: Practical manual (execution tool)

### Step 3.3: Create Combination Script

```python
# beatbook_combiner.py structure
def combine_beatbooks(draft1_path, draft2_path):
    # Load both drafts
    # Identify complementary sections
    # Merge while preserving best elements:
    #   - Draft 1's organization
    #   - Draft 2's detailed information
    #   - Geographic focus from both
    return combined_beatbook
```

### Step 3.4: Enhance Narrative Flow

If the combined result is too bullet-point heavy:

1. **Create narrative enhancement script**
2. **Preserve organizational structure**
3. **Convert bullets to flowing prose**
4. **Maintain all factual information**

### Expected Outcomes
- Well-organized structure
- Geographic categorization
- Rich information content
- Improved narrative flow

## Phase 4: Source Integration

### Objective
Replace inaccurate AI-generated contacts with verified, contextual source information.

### Step 4.1: Clean Existing Content

Create a script to remove problematic elements:
```python
def clean_beatbook(beatbook_path):
    # Remove fake emails, phone numbers, links
    # Strip inaccurate names and titles
    # Preserve all other content
    return cleaned_beatbook
```

**Output**: `beatbook_cleaned_redacted.md`

### Step 4.2: Extract Real Sources

From your original JSON data:
1. **Create people list**: Extract all names and positions
2. **Filter for relevance**: Focus on local/regional sources
3. **Categorize by expertise**: Group by topic area

```python
# Extract relevant people from JSON
def extract_people_from_stories(json_files):
    people = []
    for story in stories:
        # Extract names and titles
        # Filter for local relevance
        # Categorize by topic
    return people
```

### Step 4.3: Generate Source Contexts

Use AI to analyze why each source is valuable:

```python
# peoplefixer.py or source_context_generator.py
def generate_source_context(person, relevant_stories):
    prompt = f"""
    Analyze this person: {person}
    Based on these stories: {relevant_stories}
    
    Provide:
    - Why they're valuable as a source
    - Area of expertise
    - When to contact them
    - Relevant background
    """
    return context
```

**Expected Output**: `source_contexts.md`

> **⚠️ Token Limit Warning**: Reduce story content if hitting API limits. Switch to smaller models if necessary (e.g., llama-3.1-8b-instant).

### Step 4.4: Merge Sources into Beatbook

Use Claude Sonnet to:
1. **Analyze beatbook writing style**
2. **Rewrite source profiles to match**
3. **Integrate seamlessly into existing structure**

```python
def merge_sources_with_beatbook(beatbook_path, sources_path):
    # Analyze existing style
    # Rewrite source contexts to match
    # Insert into appropriate sections
    return final_beatbook
```

### Expected Outcomes
- Accurate source information
- Consistent writing style throughout
- Rich source context and expertise areas
- Practical contact guidance

> **Note**: The sources section may be quite long. Consider treating it as an appendix to the main beatbook.

## Phase 5: Quality Control and Fact-Checking

### Objective
Verify accuracy and improve overall quality of your beatbook.

### Step 5.1: Systematic Fact-Checking

Create a fact-checking workflow:

1. **Extract claims for verification**:
   - Names and titles
   - Organization information
   - Contact details
   - Statistical claims

2. **Cross-reference with original sources**:
   - Compare against your JSON story data
   - Verify through external sources
   - Flag inconsistencies

3. **Document findings**:
   - Create a fact-check spreadsheet
   - Track verification status
   - Note corrections needed

### Step 5.2: Address Common Issues

**Typical problems and solutions**:

- **Fake contact information**: Remove all AI-generated emails/phones
- **Incorrect titles**: Verify against recent news coverage
- **Outdated positions**: Check if people have moved roles
- **Non-local sources**: Remove or flag as external contacts

### Step 5.3: Content Quality Review

1. **Structure assessment**:
   - Clear section organization
   - Logical information flow
   - Appropriate detail level

2. **Utility evaluation**:
   - Practical reporting guidance
   - Actionable contact strategies
   - Comprehensive coverage

3. **Style consistency**:
   - Unified voice throughout
   - Appropriate tone for audience
   - Clear, accessible language

### Expected Outcomes
- Verified, accurate information
- Professional presentation quality
- Maximum utility for working journalists
- Clear documentation of any remaining uncertainties

## Tools and Technologies

### AI Services Comparison

| Service | Best For | Pros | Cons |
|---------|----------|------|------|
| **Groq/Maverick** | Entity extraction, detailed content | Fast, consistent, specific details | Token limits |
| **Claude Sonnet** | Style matching, combination tasks | Excellent instruction following | Rate limits |
| **Local models** | Privacy, cost control | No API costs, private | May lack quality |

### Recommended Tool Stack

**For beginners**:
- Groq (Maverick model) for generation
- Claude for refinement
- Python with basic libraries

**For advanced users**:
- Multiple model comparison
- Custom fine-tuning
- Advanced prompt engineering

### File Management Best Practices

```
beatbook-project/
├── data/
│   ├── stories_v11.json          # Original article data
│   ├── extracted_entities.json    # Processed entity data
│   └── people_categorized.csv     # Source lists
├── scripts/
│   ├── entity_extractor.py       # Data processing
│   ├── beatbook_generator.py     # Initial generation
│   ├── beatbook_combiner.py      # Draft combination
│   └── source_merger.py          # Final integration
├── drafts/
│   ├── beatbook_draft1.md        # First attempt
│   ├── beatbook_draft2.md        # Second iteration
│   ├── beatbook_combined.md      # Merged version
│   └── beatbook_cleaned.md       # Sanitized version
└── final/
    ├── beatbook_final.md          # Complete product
    └── source_appendix.md         # Detailed source list
```

## Troubleshooting Guide

### Common Issues and Solutions

**Entity Extraction Problems**:
- *Issue*: Inconsistent entity recognition
- *Solution*: Provide more specific examples in prompt
- *Prevention*: Test on small batches first

**Generation Failures**:
- *Issue*: Process fails partway through
- *Solution*: Implement resume functionality, process in smaller batches
- *Prevention*: Monitor token usage, use chunking strategy

**Quality Issues**:
- *Issue*: Too repetitive or poorly organized
- *Solution*: Adjust prompts for better structure, post-process for consistency
- *Prevention*: Better initial prompt design, multiple draft approach

**Fact-Checking Challenges**:
- *Issue*: Difficulty verifying AI-generated information
- *Solution*: Focus on information that can be traced to source articles
- *Prevention*: Emphasize source-based generation in prompts

### Performance Optimization

1. **API Management**:
   - Implement rate limiting
   - Add retry logic with exponential backoff
   - Monitor token usage

2. **Processing Efficiency**:
   - Use batch processing for large datasets
   - Cache intermediate results
   - Implement checkpointing for long operations

3. **Quality Control**:
   - Validate JSON outputs before processing
   - Implement sanity checks on generated content
   - Use multiple models for comparison

## Best Practices and Lessons Learned

### Prompt Engineering Insights

1. **Example Quality Matters**: Specific, varied examples produce better results than generic ones
2. **Balance Specificity**: Too rigid constraints limit creativity; too loose produces inconsistent results
3. **Iterative Refinement**: Expect to adjust prompts multiple times based on output quality

### Model Selection Guidelines

1. **Consistency vs. Creativity**: Maverick excelled at consistent, detailed output
2. **Task Specialization**: Different models for different phases (extraction vs. combination vs. style matching)
3. **Fallback Options**: Have backup models ready for when primary choices fail

### Process Management

1. **Save Everything**: Intermediate results are valuable for troubleshooting and iteration
2. **Document Decisions**: Keep notes on what works and what doesn't
3. **Expect Iteration**: Plan for multiple rounds of refinement

### Quality Assurance

1. **Human Review Essential**: AI output always needs human verification
2. **Source Verification**: Prioritize accuracy over completeness
3. **User Testing**: Have potential users review for practical utility

### Final Success Criteria

Your beatbook is ready when it includes:
- ✅ Accurate, verified source information
- ✅ Clear geographic and topical organization  
- ✅ Practical reporting guidance
- ✅ Professional presentation quality
- ✅ Comprehensive coverage of your beat area

> **💡 Final Tip**: The process is iterative by nature. Embrace the refinement cycle and don't expect perfection on the first attempt. Each iteration teaches you something valuable about both your topic and the AI tools you're using.