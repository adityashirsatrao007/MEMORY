# Setup Guide

> Install MEMORY on any OS — Linux, macOS, or Windows (WSL2).

## Prerequisites

| Requirement | Minimum |
|------------|---------|
| Python | 3.10+ |
| Git | 2.30+ |
| Disk | 2 GB free |
| RAM | 4 GB (8 GB recommended) |

## Quick Install (Linux / macOS / WSL2)

Paste this into your terminal:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/adityashirsatrao007/MEMORY/main/tools/install.sh)
```

## Manual Step-by-Step

### 1. Clone the Repository

```bash
# Linux / macOS / WSL2
git clone https://github.com/adityashirsatrao007/MEMORY.git ~/MEMORY
cd ~/MEMORY

# Windows (Git Bash / PowerShell)
git clone https://github.com/adityashirsatrao007/MEMORY.git %USERPROFILE%\MEMORY
cd %USERPROFILE%\MEMORY
```

### 2. Platform-Specific Dependencies

#### 🐧 Linux (Debian/Ubuntu)
```bash
sudo apt-get update && sudo apt-get install -y \
  git curl wget build-essential python3 python3-pip python3-venv \
  nodejs npm ripgrep bat eza fd-find tmux zoxide fzf jq unzip \
  poppler-utils tesseract-ocr pandoc chromium-browser
sudo ln -sf /usr/bin/batcat /usr/local/bin/bat 2>/dev/null
```

#### 🍎 macOS
```bash
# Install Homebrew first if missing
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install git curl wget python3 nodejs ripgrep bat eza fd \
  tmux zoxide fzf jq unzip poppler tesseract pandoc \
  gh starship dust btop procs sd tokei onefetch fastfetch \
  glow lazygit hyperfine nmap fx yq
```

#### 🪟 Windows (WSL2)
```bash
# Install WSL2 first, then inside Ubuntu:
sudo apt-get update && sudo apt-get install -y \
  git curl wget build-essential python3 python3-pip python3-venv \
  nodejs npm ripgrep bat eza fd-find tmux zoxide fzf jq unzip \
  poppler-utils tesseract-ocr pandoc
sudo ln -sf /usr/bin/batcat /usr/local/bin/bat 2>/dev/null
```

### 3. Python Virtual Environment

```bash
# All platforms
python3 -m venv .venv
source .venv/bin/activate    # Linux/macOS
# .venv\Scripts\activate     # Windows (Git Bash)
pip install --upgrade pip
pip install chromadb fastapi uvicorn matplotlib diagrams
```

### 4. Install CLI Tools

```bash
# Node.js tools
npm install -g bun pm2 tldr @opencode/opencode

# Python tools
pip install pipx && pipx ensurepath
pipx install aider-chat codeburn semgrep trufflehog

# Rust tools (optional, for speed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
cargo install lowfat du-dust procs sd tokei
```

### 5. Install Ollama (Local LLM)

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS — download from https://ollama.com/download

# Pull coding model
ollama pull qwen2.5-coder:3b
ollama pull nomic-embed-text
```

### 6. Configure Your Shell

Add to `~/.bashrc`, `~/.zshrc`, or PowerShell profile:

```bash
# MEMORY configuration
export MEMORY_ROOT="$HOME/MEMORY"
export MEMORY_MODE="lazy"      # "lazy" (~70 tokens) or "full" (~1420)
export PATH="$MEMORY_ROOT/tools:$PATH"

# Modern CLI replacements
alias grep='rg'
alias cat='bat'
alias ls='eza --icons'
alias ll='eza -la --icons --git'
alias du='dust'
alias top='btop'
alias ps='procs'
alias sed='sd'
alias find='fd'
```

Then reload: `source ~/.bashrc`

### 7. Seed the Vector Database

```bash
cd ~/MEMORY
source .venv/bin/activate
python tools/seed_vector_db.py --force
```

### 8. Start the Dashboard (Optional)

```bash
pm2 start tools/dashboard.py --name memory-dashboard --interpreter python3
pm2 save
```

The dashboard runs at `http://localhost:8082`.

### 9. Link Your AI Agent

| Agent | File | Command |
|-------|------|---------|
| Claude Code | `CLAUDE.md` | Symlink already exists |
| OpenCode | `AGENTS.md` | Symlink already exists |
| Cursor | `.cursorrules` | Symlink already exists |
| Windsurf | `.windsurfrules` | Symlink already exists |
| Copilot | `.github/copilot-instructions.md` | Symlink already exists |

For Claude Code, also configure:

```bash
# ~/.claude/settings.json
{
  "projectSettings": {
    "instructions": "/path/to/MEMORY/GEMINI.md"
  }
}
```

For OpenCode:

```json
// opencode.json (already in repo root)
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["/path/to/MEMORY/GEMINI.md"]
}
```

### 10. Verify Installation

```bash
make validate          # Check all modules
make seed              # Seed vector DB
make stats             # Module statistics
curl localhost:8082    # Dashboard health check
```

## Verification Checklist

```bash
echo "Node: $(node --version)"
echo "Python: $(python3 --version)"
echo "Ollama: $(ollama --version 2>/dev/null || echo 'install ollama')"
echo "OpenCode: $(opencode --version 2>/dev/null || echo 'install opencode')"
echo "ChromaDB: $(python3 -c 'import chromadb; print(chromadb.__version__)' 2>/dev/null || echo 'install chromadb')"
echo "MEMORY_ROOT: $MEMORY_ROOT"
```

## Windows (Native — No WSL2)

Windows without WSL2 has limited support. You can:

1. **Install Python** from [python.org](https://python.org)
2. **Install Git** from [git-scm.com](https://git-scm.com)
3. **Install Node.js** from [nodejs.org](https://nodejs.org)
4. Use Git Bash for terminal commands
5. Skip: `bat`, `eza`, `fd-find`, `btop`, `dust`, `procs` — they're Linux-only
6. Use native equivalents: `findstr` for grep, `dir` for ls, `type` for cat

For the best experience, use WSL2.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `chromadb` install fails | `pip install chromadb --no-build-isolation` |
| `ollama` not found | Restart shell after install, or add `export PATH=$PATH:/usr/local/bin` |
| Port 8082 in use | Change port in `tools/dashboard.py` or use `pm2 delete memory-dashboard` |
| Symlinks broken on Windows | Run Git Bash or PowerShell as Administrator; use `New-Item -ItemType SymbolicLink` |
| Vector DB seed fails | Delete `memory/vector_db/` and re-run `make seed` |

## Next Steps

- Read the [README](../README.md) for full documentation
- Check [TOKEN_SAVINGS.md](TOKEN_SAVINGS.md) for context optimization
- Browse [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- View benchmarks in [BENCHMARKS.md](BENCHMARKS.md)
