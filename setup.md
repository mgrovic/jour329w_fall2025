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
   git commit -m "first commit"
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
