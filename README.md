# MEMORY — Aditya's Workspace & Agent Configuration Hub

Central repository for all system configurations, dotfiles, AI agent rules, and automation setups. This repository serves as the ultimate source of truth to bootstrap any new developer machine in a single step.

---

## 📂 Repository Contents

| File / Folder | Purpose |
|:---|:---|
| [`AGENTS.md`](file:///home/aditya/Desktop/Projects/MEMORY/AGENTS.md) | Central Agent rules (mirrored as `GEMINI.md` and `CLAUDE.md`). |
| [`CLAUDE.md`](file:///home/aditya/Desktop/Projects/MEMORY/CLAUDE.md) | Global rules template for Claude Code. |
| [`GEMINI.md`](file:///home/aditya/Desktop/Projects/MEMORY/GEMINI.md) | Global rules template for Gemini CLI and Antigravity. |
| [`.clinerules`](file:///home/aditya/Desktop/Projects/MEMORY/.clinerules) | Global rules template for Cline-family agents (Roo Code, KiloCode). |
| [`.cursorrules`](file:///home/aditya/Desktop/Projects/MEMORY/.cursorrules) | Global rules template for Cursor IDE. |
| [`.windsurfrules`](file:///home/aditya/Desktop/Projects/MEMORY/.windsurfrules) | Global rules template for Windsurf IDE. |
| [`.github/copilot-instructions.md`](file:///home/aditya/Desktop/Projects/MEMORY/.github/copilot-instructions.md) | Rules template for GitHub Copilot. |
| [`VIBE_CODER_GUIDE.md`](file:///home/aditya/Desktop/Projects/MEMORY/VIBE_CODER_GUIDE.md) | Premium web design layout, animation, and aesthetic standards. |
| [`.agentignore`](file:///home/aditya/Desktop/Projects/MEMORY/.agentignore) | Global blacklist directory/file list to prevent agents from reading junk. |
| [`.aider.conf.yml`](file:///home/aditya/Desktop/Projects/MEMORY/.aider.conf.yml) | Configuration file for Aider AI pair programmer. |
| [`.continuerc.json`](file:///home/aditya/Desktop/Projects/MEMORY/.continuerc.json) | Configuration file for Continue.dev extension. |
| [`opencode.json`](file:///home/aditya/Desktop/Projects/MEMORY/opencode.json) | Main configuration file mapping Opencode to `AGENTS.md`. |
| [`dotfiles/`](file:///home/aditya/Desktop/Projects/MEMORY/dotfiles/) | Configs for terminal tools: bashrc, starship.toml, tmux.conf, gitconfig. |
| [`templates/`](file:///home/aditya/Desktop/Projects/MEMORY/templates/) | Reusable blueprints (Remix, Makefile, Github Actions, Docker Compose). |
| [`memory-bank/`](file:///home/aditya/Desktop/Projects/MEMORY/memory-bank/) | Documentation for the MEMORY repository state. |

---

## 🚀 Bootstrap a New PC (Setup Guide)

Follow these steps to fully configure a new development environment.

### Step 1: Clone the Repository
Clone the central memory repo to your `Projects` folder:
```bash
git clone https://github.com/adityashirsatrao007/MEMORY.git ~/Desktop/Projects/MEMORY
```

### Step 2: Install Core Dotfiles (Symlink)
Execute the install script to symlink your bash shell, starship prompt, tmux window manager, and global git configs:
```bash
cd ~/Desktop/Projects/MEMORY/dotfiles
chmod +x install.sh
./install.sh
source ~/.bashrc
```

### Step 3: Install all Developer CLI Tools
Run the single installation script or command block matching your toolset (see detailed list below).

---

## 🛠️ CLI Tools Directory & Installation Mappings

Below is the complete list of CLI tools used in this workspace, their uses, and exact installation commands.

### 1. Global Setup (Copy-Paste Core Script)
Run this single block to install all package-managed tools at once:
```bash
# Update and install system dependencies
sudo apt-get update && sudo apt install -y bat eza ripgrep direnv gh docker.io pipx git tmux build-essential curl

# Setup pipx environment
pipx ensurepath

# Install Python global CLIs via pipx
pipx install semgrep
pipx install pgcli
pipx install dvc

# Install Node.js global CLIs
npm install -g pm2 tldr codeburn
```

### 2. Standalone Binary Installations
Run these individual commands for tools requiring custom releases:

*   **Trivy** (Security Vulnerability & IaC Scanner):
    ```bash
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin
    ```
*   **Gitleaks** (Secrets Leak Detector):
    ```bash
    curl -sL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_x64.tar.gz | sudo tar -xz -C /usr/local/bin gitleaks
    ```
*   **Lazygit** (TUI Git Manager):
    ```bash
    curl -sL "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_$(uname -s)_$(uname -m).tar.gz" | sudo tar -xz -C /usr/local/bin lazygit
    ```
*   **Zoxide** (Smarter `cd` matching engine):
    ```bash
    curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | bash
    ```
*   **Ollama** (Local LLM Execution Engine):
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```

---

### 3. Detailed Tool List & Use Cases

| CLI Tool | Purpose | Primary CLI Commands |
|:---|:---|:---|
| **codeburn** | AI agent cost and token observability dashboard. | `codeburn`, `codeburn optimize` |
| **gh** | Command-line client for GitHub actions, repos, issues. | `gh repo create`, `gh pr create` |
| **pm2** | Process manager for active background Node.js servers. | `pm2 list`, `pm2 logs` |
| **semgrep** | Static analysis scanner for code security and style. | `semgrep scan --config auto` |
| **trivy** | Scans directories, Docker images, and repos for CVEs. | `trivy fs .` |
| **gitleaks** | Prevents committed API keys and passwords from pushing. | `gitleaks detect -v` |
| **lazygit** | Interactive terminal layout for staging and committing. | `lazygit` |
| **ripgrep (`rg`)** | Ultrafast recursive code finder (saves agent read tokens). | `rg "query"` |
| **bat** | Syntax-highlighted code output viewer in terminal. | `bat filename` |
| **eza** | Structured colorized alternative to `ls` displaying git status. | `eza -la --git` |
| **direnv** | Automatic context-based environment variable loading. | `direnv allow` |
| **zoxide** | Learns your directory jump patterns to bypass long `cd` commands. | `z` |
| **tldr** | Simplified manual pages with common command examples. | `tldr tar` |
| **pgcli** | PostgreSQL client with auto-completion and syntax styling. | `pgcli -u postgres` |
| **dvc** | Data version controller for machine learning file staging. | `dvc init`, `dvc add` |
| **ollama** | Run models (llama3.2, phi3) locally on native machines. | `ollama run llama3.2` |

---

## 🎨 Design Rules & Workspace Standards

All development projects inside this workspace conform to the strict Apple HIG and Clinical/Dark Luxury standards documented in [`VIBE_CODER_GUIDE.md`](file:///home/aditya/Desktop/Projects/MEMORY/VIBE_CODER_GUIDE.md).

For custom system diagram generation, use the python templates stored in:
*   [templates/diagrams/](file:///home/aditya/Desktop/Projects/MEMORY/templates/)
