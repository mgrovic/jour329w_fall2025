<<<<<<< HEAD
# Setting Up Your Development Environment with GitHub Codespaces

This guide will walk you through setting up a modern Python development environment using GitHub Codespaces and uv (a fast Python package manager).

## Step 1: Fork the Class Repository

1. **Fork the class repository**
   - Go to the class repository: `https://github.com/dwillis/jour329w_fall2025`
   - Click the "Fork" button in the top-right corner
   - Select your GitHub account as the destination
   - Keep the repository name as `jour329w_fall2025`
   - Make sure it's set to "Public" (required for free Codespaces)
   - Click "Create fork"

2. **Your forked repository is ready**
   - You now have your own copy of the class repository
   - You can make changes without affecting the original
   - You'll be able to sync updates from the instructor's repository later

## Step 2: Launch GitHub Codespaces

1. **Start a Codespace**
   - On your forked repository page, click the green "Code" button
   - Select the "Codespaces" tab
   - Click "Create codespace on main"
   - Wait for the environment to build (this may take 2-3 minutes the first time)

2. **Your development environment is ready!**
   - You'll see VS Code running in your browser
   - Python, UV, and other tools are pre-installed
   - The terminal is available at the bottom of the screen

## Step 3: Set Up Your Python Environment

1. **Open the terminal in Codespaces**
   - The terminal should already be visible at the bottom
   - If not, go to View → Terminal (or press Ctrl+`)

2. **Initialize your Python project with UV**
   - UV is already installed in your Codespace
   - Run: `uv init --python 3.12`
   - This creates a basic Python project structure with Python 3.12

## Step 4: Install Essential Python Packages

1. **Install the LLM command-line tool and plugins**
   - With your virtual environment activated, run:
   ```bash
   uv add llm
   uv run llm install llm-groq llm-gemini llm-anthropic
   ```
   - This installs the LLM CLI tool and plugins for Groq, Gemini, and Anthropic models

2. **Install additional packages**
   - Also install these libraries we'll be using:
   ```bash
   uv add sqlite_utils csvkit newspaper4k
   ```

3. **Verify the installation**
   - Run: `uv run llm --version`
   - You should see the LLM version information

## Step 5: Configure LLM Models

1. **Create and set up API keys (some of them will be provided by instructor)**
   - For Groq: `uv run llm keys set groq`
   - For Anthropic: `uv run llm keys set anthropic`
   - You'll be prompted to enter your API keys when available

2. **Test the LLM command directly**
   - In the terminal, run: `uv run llm models`
   - This should show available models from OpenAI, Groq, and Anthropic plugins

## Common Commands You'll Use

- `uv add [package-name]`: Install a new package
- `uv run python script.py`: Run a Python script
- `uv run llm "Your prompt here"`: Chat with default AI model
- `uv run llm -m SOMEMODEL "Your prompt"`: Use specific model
- `uv run llm models`: List all available AI models
- `uv sync`: Sync your environment with the project requirements

## Commit Often!

**Commit your changes**: Use Git to commit and push your work regularly:
   ```bash
   git add .
   git commit -m "replace with your commit msg"
   git pull origin main
   git push origin main
   ```

## Syncing Your Fork with Upstream

When the instructor adds new materials or assignments, you'll need to sync your fork:

1. **Set up the upstream remote (one-time setup)**
   ```bash
   git remote add upstream https://github.com/dwillis/jour329w_fall2025.git
   ```

2. **Sync with upstream (do this regularly)**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   git push origin main
   ```

3. **Verify your remotes**
   ```bash
   git remote -v
   ```
   You should see both `origin` (your fork) and `upstream` (instructor's repo)

## Managing Your Codespace

**To stop your Codespace:**
- Click the Codespaces tab in your repository
- Click the three dots next to your active Codespace
- Select "Stop codespace"

**To restart your Codespace:**
- Click "Open in Codespaces" from your repository
- Your environment and files will be exactly as you left them
=======
# Setup Guide: Installing AI Tools for Journalism (GitHub Codespaces)

This guide walks you through setting up your GitHub Codespaces environment for this class. Pay attention to the instructions closely.

## What We're Setting Up

- **GitHub Codespaces**: Cloud-based development environment
- **llm**: Simon Willison's command-line tool for working with Large Language Models
- **llm-groq**: Plugin to access LLMs hosted by Groq
- **jq**: JSON processing tool (pre-installed in Codespaces)

## Step 1: Set Up Your GitHub Repository and Codespace

We'll use a fork-and-pull workflow, so that I can add materials later and you can update your repositories with them.

### Fork the Course Repository
1. Go to this repository on GitHub: https://github.com/dwillis/jour329w_fall2025
2. Click the "Fork" button in the top-right corner
3. Create the fork in your personal GitHub account, leaving the name the same.

### Launch Your Codespace
1. From your forked repository, click the green "Code" button
2. Select the "Codespaces" tab
3. Click "Create codespace on main"
4. Wait for the environment to initialize (this may take 2-3 minutes)

### Set Up Repository Remotes
Once your Codespace loads, open the terminal and run:

```bash
# Add the original course repo as "upstream" for getting updates
git remote add upstream https://github.com/dwillis/jour329w_fall2025.git

# Verify your remotes are set up correctly
git remote -v
```

You should see:
- `origin` pointing to your fork
- `upstream` pointing to the original course repository

## Step 2: Install Python Tools Using uv

Codespaces comes with Python installed; this guide uses `uv` (a lightweight, universal virtualenv manager) to create isolated, repeatable environments and install CLI tools inside the Codespace. To install it, copy and paste this into the terminal:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

You should see this:

```bash
installing to /home/codespace/.local/bin
  uv
  uvx
everything's installed!
```

If you see that, you can go ahead and create a project by running this command:

```bash
uv init
```

You should see several new files, including pyproject.toml, main.py and .python-version. Now let's add the `llm` library to your project:

```bash
uv add llm
```

#### Verify installation:
```bash
uv run llm --version
```

It should say: llm, version 0.27.1. Basically, whenever we add a Python library or run a command, we're going to preface it with `uv run`. Like this next one, for installing the `llm-groq` plugin.

#### Install groq plugin

```bash
uv run llm install llm-groq
```

## Step 3: Set up API access

#### Get a Groq API key:
1. Go to https://console.groq.com/
2. Sign up for a free account
3. Navigate to "API Keys" in the dashboard
4. Create a new API key
5. Copy the key (it starts with `gsk_`)

#### Configure the API key in Codespaces:
```bash
uv run llm keys set groq
```

When prompted, paste your API key. You might need to wait a second for a "Paste" button to become visible.

**Important**: Your API key is stored securely in your Codespace and won't be visible to others or committed to your repository.

## Step 4: Test your setup

### See available models

```bash
uv run llm models
```

We'll try one of the newer models, Kimi's K2.

### Test basic llm functionality:
```bash
uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "Give me 10 names for a pet iguana"
```

You should get back a reasonable? list of names.

### Test JSON processing with a simple example:
```bash
uv run echo '{"title": "Test Article", "content": "This is test content about local government."}' | jq '.content' | llm -m groq/moonshotai/kimi-k2-instruct-0905 "What is the main topic?"
```

## Getting Course Updates

Throughout the semester, I will add new materials to the main course repository. Here's how to get those updates in your Codespace:

### Sync with the main course repository:
```bash
# Fetch the latest changes from the instructor's repository
git fetch upstream

# Make sure you're on your main branch
git checkout main

# Merge the instructor's updates into your repository
git merge upstream/main

# Push the updates to your GitHub fork
git push origin main
```

### If you encounter merge conflicts:
1. Git will tell you which files have conflicts
2. Use the VS Code interface in Codespaces to resolve conflicts
3. Look for conflict markers and choose which changes to keep
4. Save the files and commit:
```bash
git add .
git commit -m "Resolve merge conflicts with course updates"
```

## Working in Codespaces

### Codespaces Features
- **VS Code Interface**: Full VS Code editor in your browser
- **Terminal Access**: Click Terminal → New Terminal
- **File Explorer**: Browse files in the left sidebar
- **Extensions**: VS Code extensions work normally
- **Auto-save**: Your work is automatically saved

### Managing Your Codespace
- **Stopping**: Codespaces auto-stop after 30 minutes of inactivity
- **Restarting**: Go to github.com/codespaces to restart a stopped Codespace
- **Multiple Codespaces**: You can run multiple Codespaces if needed

## Troubleshooting

### If llm models aren't working:
- Verify your API key is set: `llm keys list`
- Check that your Codespace has internet access (it should by default)
- Ensure you haven't exceeded API rate limits

### Codespace Issues:
- If your Codespace becomes unresponsive, restart it from github.com/codespaces (or hit reload)
- If you lose your API key, you'll need to reset it with `llm keys set groq`
- Files are automatically saved, but you need to manually commit and push your work

### Git Issues:
- Use the VS Code source control panel (left sidebar) for a visual Git interface
- Or use terminal commands as shown above
- If confused, use `git status` to see what's happening

##Install llm-anthropic plugin

If you want to compare with Claude models, install the Anthropic plugin into the same `uv` environment (or into your active virtualenv):

```bash
# Using uv
uv run llm install llm-anthropic
```

Then set up your Anthropic API key:
```bash
uv run llm keys set anthropic
```
You'll need an API key from https://console.anthropic.com/

>>>>>>> 01a7b79d61d73e7911d126ee7e44f10dab5a8fcc
