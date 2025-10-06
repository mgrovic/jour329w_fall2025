# CNS More Datasette

Now that you've worked with CNS data and created some collections, let's explore more advanced ways to enrich and analyze that data using Datasette. We'll use two powerful features: enrichments to enhance your data with AI analysis, and embeddings to find semantic relationships between stories.

### Getting Started

What we're going to do is take your existing CNS work and enhance it with Datasette's AI capabilities. You'll learn how to automatically enrich data with AI-generated insights and explore semantic relationships through embeddings.

1. In the Terminal, cd into the directory with your last name.
2. Create a directory called cns_more_datasette using mkdir
3. cd into that new directory
4. Create a file called notes.md using touch. Keep that file open.
5. Open that document and put "CNS More Datasette" and today's date at the top, then save it
6. Do cd .. twice to get back to the main directory (/workspaces/jour329w_fall2025)
7. In the Terminal, do the git add, commit, pull and push your changes as described in the `setup.md` file.

### Use Your Existing Database

For this assignment, we'll use the `cns.db` database you created in the `cns_datasette` assignment, which already contains all the CNS stories in a `stories` table.

```bash
# Copy your existing database to your new directory
cp ../cns_datasette/cns.db ./cns.db

# Verify your database has the stories
uv run sqlite-utils tables cns.db --counts
```

You should see a `stories` table with the 4000 CNS posts. If it has 8000 posts, you did the insert command twice, and here's how to fix that:

```bash
rm cns.db
uv run sqlite-utils insert cns.db stories ../../data/story_summaries.json
```

### Set Up OpenAI API Key

The datasette-enrichments plugin uses OpenAI's API for AI analysis. You'll need to set up your API key:

1. I will provide you with an OpenAI API key for this assignment
2. Set it as an environment variable in your Codespace:

```bash
# Set your OpenAI API key (replace with the key I provide)
export DATASETTE_SECRETS_OPENAI_API_KEY="your-api-key-here"

# Verify it's set
echo $DATASETTE_SECRETS_OPENAI_API_KEY
```

**Important**: Keep this API key secure and DO NOT commit it to your repository. The environment variable will only last for your current session.

### Install Datasette and Plugins

Install the tools we'll need:

```bash
# Install Datasette and the plugins we'll use
uv add datasette sqlite-utils
uv run datasette install datasette-enrichments-gpt datasette-codespaces datasette-embeddings

# Verify installation
uv run datasette --version
```

Let's configure Datasette to use the OpenAI API key. In the Terminal, do the following:

```bash
touch metadata.json
```

Then copy the contents of this file into `metadata.json`: https://gist.githubusercontent.com/dwillis/419c9187b19e9b82775c3783dd5d8ff4/raw/0186dd53b01ecce6e34a98dd242fae2f6892565a/metadata.json

### Exploring Datasette Enrichments

Enrichments let you use AI to automatically analyze and enhance your data. Let's try several different types of analysis.

First, launch Datasette with your database.

```bash
# Launch Datasette with enrichments enabled
uv run datasette cns.db --metadata metadata.json
```

When you run that, in the terminal you'll see something like this:

```bash
Running on GitHub Codespace: improved-zebra-5rw9ggwcj6w
https://improved-zebra-5rw9ggwcj6w-8001.preview.app.github.dev/
http://127.0.0.1:8001/-/auth-token?token=14a1df6a02959ca502d93c42e6183cd74b1f2c6a330b47bbe4837c54216135e2
INFO:     Started server process [4297]
```

_This part is important_: you'll need to copy the portion of the second url that starts with "~/auth-token" to the end of the line, and then paste it onto the end of your Datasette web interface and hit Return. You'll know if you did it right by going to the stories table: there should be a gear icon right next to "stories".

#### Enrichment 1: Keywords or Sentiment

1. In Datasette, facet by Topic and choose "Chesapeake Bay". There should be 36 stories.
2. Click on the "Enrich selected data" button
3. Choose "AI analysis with OpenAI GPT"
4. Choose the gpt-4o model
5. Use the menu to create and populate a new column based on an existing column. For example, you could use the summary to generate keywords, or have the LLM perform sentiment analysis using the title.
6. Before running, you'll need to plug in the API key I gave you. Need to get it? Use the command from above in the Terminal!
7. Run the enrichment and observe the results

Run this enrichment and document in `notes.md`:
- Do the results make sense?
- Any surprising patterns?
- Anything you don't like about this?

#### Enrichment 2: Topics

1. Go back to the full stories table and use the drop-down menu to search for stories where the summary contains "annapolis". Should be 87 rows.
2. Cick that gear icon and click on the "Enrich selected data" button
3. Choose "AI analysis with OpenAI GPT"
4. Choose the gpt-4o model
5. Using the topics we've generated together, write a prompt that includes them in `notes.md` (and has the {{ summary }} column) and paste that into the Prompt section.
6. Create a new column name for the output.
7. Add your OpenAI key again

Run this enrichment and document in `notes.md`:
- Do the results make sense?
- Any surprising patterns?
- Anything you don't like about this?

### Working with Embeddings

Now let's explore semantic relationships using the embeddings plugin.

#### Generate Embeddings

First, create embeddings for your stories:

```bash
# Generate embeddings using the datasette-embeddings plugin
# The plugin will use your OPENAI_API_KEY environment variable
DATASETTE_SECRETS_OPENAI_API_KEY=$DATASETTE_SECRETS_OPENAI_API_KEY uv run datasette cns.db
```

In the Datasette interface:

1. Navigate to the stories table
2. Look for "Embeddings" functionality 
3. Generate embeddings for the content column (or title + content combined)
4. Choose an appropriate embedding model (like sentence-transformers/all-MiniLM-L6-v2)

#### Explore Semantic Similarity

Once embeddings are generated:

1. **Find similar stories**: Click on any story and use "Find similar" to discover related coverage
2. **Search by concept**: Try searching for concepts like "budget crisis" or "environmental protection"
3. **Cluster analysis**: Look for stories that cluster together thematically

Document your findings:

```bash
# Try these similarity searches in Datasette
# Search for stories similar to budget-related content
# Search for environment/pollution related stories  
# Search for political/election content
```

In `notes.md`, create sections for:
- **Unexpected Connections**: Stories that seemed unrelated but were found to be similar
- **Topic Clusters**: Groups of stories that naturally cluster together
- **Coverage Gaps**: Topics that seem underrepresented when you search for them

### Advanced Enrichments

Now let's try some custom enrichments that are particularly useful for journalism:

#### Source Diversity Analysis

Create an enrichment to analyze source diversity:

1. Extract quoted sources from story content
2. Classify sources by type (official, expert, citizen, etc.)
3. Analyze gender representation if names are provided
4. Look at geographic diversity of sources

#### Story Impact Scoring

Design an enrichment to assess potential story impact:

1. Analyze language for urgency indicators
2. Identify policy implications
3. Assess local vs. statewide relevance  
4. Look for follow-up potential

#### Fact-Checking Flags

Create an enrichment that identifies claims that might need fact-checking:

1. Identify statistical claims
2. Flag controversial topics
3. Highlight claims about government spending or policy
4. Mark statements that could benefit from verification

Document your custom enrichment ideas in `notes.md` even if you can't fully implement them.

### Data Quality and Ethics

As you experiment with AI enrichments, consider:

**Accuracy Questions:**
- How often do the AI classifications seem wrong?
- What types of errors do you notice?
- Which enrichments seem most/least reliable?

**Bias Considerations:**
- Do sentiment analysis results seem fair across different topics?
- Are there patterns in entity extraction that might reflect bias?
- How might these tools affect editorial decisions?

**Practical Applications:**
- Which enrichments would genuinely help a newsroom?
- What workflows would benefit from automated analysis?
- Where is human judgment still essential?

Write a reflection section addressing these questions.

### Comparative Analysis

Use your enrichments and embeddings to conduct some comparative analysis:

#### Geographic Coverage Patterns

```bash
# Analyze which Maryland regions get the most coverage
# Look for stories that mention specific counties/cities
# Use embeddings to find geographically-related story clusters
```

#### Institutional Coverage

```bash
# Identify which government agencies appear most frequently
# Find stories about similar institutions using embeddings
# Track how different institutions are portrayed
```

#### Temporal Patterns

```bash
# Look at how topics change over time in your dataset
# Use embeddings to track evolving coverage of long-running stories
# Identify seasonal patterns in coverage
```

### Building a Newsroom Dashboard

Design (even if you don't build) a Datasette-powered dashboard for a newsroom using enrichments and embeddings:

1. **Story Similarity Alerts**: Automatically flag when new stories are similar to recent coverage
2. **Source Diversity Monitoring**: Track diversity metrics across coverage
3. **Topic Gap Analysis**: Identify undercover topics in your beat
4. **Fact-Check Queue**: Automatically flag stories with claims needing verification
5. **Impact Prediction**: Highlight stories likely to generate significant reader interest

Sketch out this dashboard concept in your `notes.md`.

### Reflection and Next Steps

Conclude your `notes.md` with reflection on:

- **Most Useful Features**: Which enrichments provided the most valuable insights?
- **Accuracy Assessment**: How reliable were the AI analyses?
- **Workflow Integration**: How could these tools fit into actual newsroom workflows?
- **Ethical Considerations**: What concerns arose about AI-assisted journalism?
- **Future Applications**: What other enrichments would you want to try?

### Submission

When you are finished, add, commit and push your changes:

```bash
git add .
git commit -m "Datasette enrichments and embeddings analysis"
git pull origin main
git push origin main
```

Submit the link to your analysis directory in ELMS. Your directory should contain:
- `notes.md` with your complete analysis and reflections  
- `cns.db` with your enriched data
- Screenshots of interesting findings from Datasette
- Any custom scripts you created

### Extra Credit

Want to go further? Try these advanced challenges:

- **Custom Embedding Models**: Experiment with different embedding models and compare results
- **Cross-Dataset Analysis**: Compare CNS coverage patterns with national news trends
- **Automated Alerts**: Create a system that alerts when stories match specific criteria
- **Network Analysis**: Use embeddings to create visualizations of story relationships
- **Temporal Embedding Analysis**: Track how story themes evolve over time using embeddings

Remember: The goal is to understand how AI can augment journalism while being critical about its limitations. Focus on practical applications that would genuinely help reporters and editors do better work.