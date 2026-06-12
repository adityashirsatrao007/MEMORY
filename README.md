> **Copyright (c) 2026 Aditya Shirsatrao. All rights reserved.**  
> Proprietary — see [LICENSE](LICENSE). No copying, cloning, or distribution without written permission.

# MEMORY — Agent Configuration & Cross-Device Setup

<p align="center">
  <strong>One-shot agent environment for AI-assisted development.</strong><br>
  Clone → paste one prompt → full agent toolchain on any machine.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-Proprietary-red.svg?style=for-the-badge" alt="License: Proprietary">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL2-ff69b4?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/LLM-Free%20Proxy%20(1.7B%20tokens%2Fmonth)-brightgreen?style=for-the-badge" alt="Free LLM proxy">
</p>

---

## Overview

MEMORY is a portable agent-environment configuration system. It packages everything an AI coding agent needs — shell config, CLI tools, vector database, LLM proxy, and 15+ agent-skills — into a single reproducible setup.

One `git clone` and one pasted prompt, and any machine becomes a full agent development environment.

---

## Features

- **Zero-cost LLM proxy** — 90+ models across 12 free providers, 1.7B tokens/month
- **Vector knowledge base** — ChromaDB-backed agent memory with semantic search
- **15+ integrated tools** — Swarms, NeoAgent, MiMo, Hermes, Agent-Reach, Free Claude Code, Mistral Vibe, and more
- **Cross-platform** — Linux, macOS, Windows (WSL2) from a single setup script
- **Agent skills** — 50+ reusable skills (diagnose, review, TDD, design, writing, PM, etc.)
- **Token-optimized** — Lazy mode (~70 tokens/session) for routine tasks, full mode (~1420 tokens) for complex work
- **Private & secure** — All cookies/keys stored locally, never uploaded

---

## Project Structure

```
MEMORY/
├── AGENTS.md                  Agent configuration & rules (loaded by all agents)
├── GEMINI.md                  Gemini-specific config (symlink target)
├── CLAUDE.md → GEMINI.md      Claude-specific config (symlink)
├── LICENSE                    Proprietary license
├── README.md                  This file
├── Makefile                   Build: validate, seed, stats, hooks
│
├── memory/
│   ├── modules/               Knowledge base (13 module files)
│   ├── vector_db/             ChromaDB persistent storage
│   └── memory-bank/           Session progress tracking
│
├── tools/
│   ├── dashboard.py           ChromaDB dashboard (FastAPI, port 8083)
│   ├── seed_vector_db.py      Vector DB seeder with hash-based skip
│   └── validate_ui.py         UI design validation
│
├── config/
│   └── .aider.conf.yml        Aider configuration
│
├── .agents/skills/            50+ agent skills (installed)
├── dotfiles/                  Shell, git, starship, tmux configs
├── .githooks/                 Git hooks (auto-re-vector DB on commit)
└── .github/workflows/         CI workflow
```

---

## Tool Manifest

| Category | Tools |
|----------|-------|
| **LLM Proxy** | [freellmapi](http://localhost:3001/v1) — 90+ models, 0-cost |
| **Model Router** | [fcc-server](http://localhost:8082/admin) — 1130 models, 12+ providers |
| **Agent Frameworks** | Swarms v13, NeoAgent v2.4, MiMo-Code, Hermes Agent v0.15 |
| **Internet Access** | Agent-Reach v1.5 (YouTube, Twitter, Reddit, RSS, web) |
| **Coding Agents** | Free Claude Code (fcc-claude), Mistral Vibe CLI |
| **AI Skills (50+)** | diagnose, review, TDD, prototype, handoff, html-plan, drawio, grill-me, edit-article, caveman, and more |

---

## Quick Start

### Step 1 — Clone

```bash
git clone https://github.com/adityashirsatrao007/MEMORY ~/Desktop/Projects/MEMORY
```

### Step 2 — Paste the Setup Prompt

Copy the entire block below and paste it into **Antigravity** (or any agent) on your new machine:

````
You are setting up my MEMORY agent system from scratch on this new machine.

## Step 1: Clone repos
git clone https://github.com/adityashirsatrao007/MEMORY ~/Desktop/Projects/MEMORY
git clone https://github.com/adityashirsatrao007/dotfiles ~/dotfiles  # if exists, skip if 404

## Step 2: Install system packages (platform-detect automatically)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sudo apt-get update && sudo apt-get install -y \
    git curl wget build-essential python3 python3-pip python3-venv \
    nodejs npm docker.io sqlite3 ripgrep bat eza fd-find \
    tmux zoxide fzf jq unzip p7zip-full poppler-utils \
    tesseract-ocr pandoc chromium-browser || true
  sudo ln -sf /usr/bin/batcat /usr/local/bin/bat 2>/dev/null
elif [[ "$OSTYPE" == "darwin"* ]]; then
  brew install git curl wget python3 nodejs sqlite3 ripgrep bat eza fd \
    tmux zoxide fzf jq unzip poppler tesseract pandoc \
    gh starship dust btop procs sd tokei onefetch fastfetch \
    glow lazygit hyperfine nmap entr fx yq || true
elif [[ "$OSTYPE" == "msys" ]] || [[ -n "$WSLENV" ]]; then
  sudo apt-get update && sudo apt-get install -y \
    git curl wget build-essential python3 python3-pip python3-venv \
    nodejs npm sqlite3 ripgrep bat eza fd-find \
    tmux zoxide fzf jq unzip poppler-utils tesseract-ocr pandoc || true
fi

## Step 3: Install global CLI tools (Node.js + Python)
npm install -g bun pm2 tldr 2>/dev/null
pip3 install --user pipx && pipx ensurepath
source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null
pipx install aider-chat codeburn comet semgrep trufflehog 2>/dev/null || true

## Step 4: Install Rust CLIs
if ! command -v cargo &>/dev/null; then curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y; fi
source "$HOME/.cargo/env" 2>/dev/null
cargo install lowfat du-dust procs bat sd tokei eza 2>/dev/null || true

## Step 5: Install Ollama + pull coding model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5-coder:3b
ollama pull nomic-embed-text  # for vector embeddings

## Step 6: Install Go tool (for onlycli)
if ! command -v go &>/dev/null; then
  wget https://go.dev/dl/go1.23.0.linux-amd64.tar.gz -O /tmp/go.tar.gz
  sudo tar -C /usr/local -xzf /tmp/go.tar.gz
  export PATH=$PATH:/usr/local/go/bin
fi
go install github.com/steveiliop56/onlycli@latest 2>/dev/null || true

## Step 7: Set up bashrc additions
cat >> ~/.bashrc << 'BASHRC_EOF'
# MEMORY agent aliases
alias grep=rg
alias cat=bat
alias ls='eza --icons'
alias ll='eza -la --icons --git'
alias du='dust'
alias top=btop
alias ps='procs'
alias sed='sd'
alias find='fd'
alias v='nvim'
alias gl='lazygit'
source ~/.cargo/env 2>/dev/null
source ~/.local/bin/pipx ensurepath 2>/dev/null
export MEMORY_ROOT="$HOME/Desktop/Projects/MEMORY"
export MEMORY_MODE=lazy  # ~70 tokens/session (full=~1420)
export PATH="$MEMORY_ROOT/tools:$PATH"
export EDITOR=nvim
BASHRC_EOF
source ~/.bashrc

## Step 8: Install opencode
npm install -g @opencode/opencode 2>/dev/null || bun install -g @opencode/opencode 2>/dev/null
mkdir -p ~/.config/opencode
cp "$HOME/Desktop/Projects/MEMORY/config/opencode.json" ~/.config/opencode/ 2>/dev/null || true

## Step 9: Set up guardrails
mkdir -p ~/bin/guardrails
for tool in grep cat ls find du top ps sed; do
  cat > ~/bin/guardrails/"$tool" << 'GUARD'
#!/bin/bash
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
for cmd in $(which -a TOOL 2>/dev/null); do
  cmd_dir="$(cd "$(dirname "$cmd")" && pwd)"
  if [ "$cmd_dir" != "$SELF_DIR" ]; then
    exec "$cmd" "$@"
  fi
done
exec /usr/bin/TOOL "$@"
GUARD
  sed -i "s/TOOL/$tool/g" ~/bin/guardrails/"$tool"
  chmod +x ~/bin/guardrails/"$tool"
done
echo 'export PATH="$HOME/bin/guardrails:$PATH"' >> ~/.bashrc

## Step 10: Install the auto-dispatch script
cp "$HOME/Desktop/Projects/MEMORY/tools/dispatch/auto-dispatch" ~/bin/ 2>/dev/null || true
chmod +x ~/bin/auto-dispatch 2>/dev/null || true

## Step 11: Set up ChromaDB vector dashboard
cd ~/Desktop/Projects/MEMORY
pip3 install -r tools/static/requirements.txt 2>/dev/null || pip3 install chromadb fastapi uvicorn
pm2 start tools/static/supermemory_dashboard.py --name memory-dashboard --interpreter python3
pm2 save

## Step 12: Seed the vector database
cd ~/Desktop/Projects/MEMORY
python3 tools/static/seed_vector_db.py 2>/dev/null || python3 -c "
from pathlib import Path
import chromadb, json, hashlib
c = chromadb.PersistentClient(path='memory/vector_db')
try: c.delete_collection('memories')
except: pass
col = c.create_collection('memories')
mem_path = Path('memory/modules')
chunks = []
for f in sorted(mem_path.glob('*.md')):
    text = f.read_text()
    for i, line in enumerate(text.split('\n')):
        if line.strip() and not line.startswith('#'):
            chunks.append((f'{f.stem}:{i}', line.strip(), {'source': f.name, 'section': f.stem}))
ids, texts, metas = zip(*chunks) if chunks else (['init'], ['init'], [{}])
col.add(ids=list(ids), documents=list(texts), metadatas=list(metas))
print(f'Seeded {len(ids)} chunks')
"

## Step 13: Verify everything
echo "=== Verification ==="
echo "Node: $(node --version)"
echo "Python: $(python3 --version)"
echo "Ollama: $(ollama --version 2>/dev/null || echo 'missing')"
echo "OpenCode: $(opencode --version 2>/dev/null || echo 'missing')"
echo "PM2: $(pm2 --version 2>/dev/null || echo 'missing')"
curl -s localhost:8082/ 2>/dev/null | head -1 || echo "Dashboard: start with 'pm2 start memory-dashboard'"
echo ""
echo "=== DONE ==="
echo "Next: paste 'session-start.sh' output below to verify agent sees the system."
echo "Run: source ~/bin/session-start.sh ~/Desktop/Projects/MEMORY"
````

### Step 3 — Verify

```bash
source ~/Desktop/Projects/MEMORY/bin/session-start.sh ~/Desktop/Projects/MEMORY
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                      Agent Process                       │
│  (Claude / Gemini / OpenCode / Antigravity)              │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ AGENTS.md   │  │ Tool Manifest│  │ Agent Skills    │  │
│  │ (rules)     │  │ (manifest)   │  │ (50+)          │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                │                   │           │
│         ▼                ▼                   ▼           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              MEMORY Knowledge Base               │   │
│  │        (ChromaDB vector search, 13 modules)      │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │           freellmapi Proxy (port 3001)            │   │
│  │    90+ models · 12 providers · 1.7B tokens/mo     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

The agent reads `AGENTS.md` on startup (~100 tokens), loads the tool manifest only when needed (~400 tokens), and queries the vector DB for relevant knowledge. All LLM calls route through the local proxy to preserve API budget.

---

## Infrastructure

| Service | Port | Purpose |
|---------|------|---------|
| freellmapi proxy | 3001 | Zero-cost LLM routing (OpenAI-compatible) |
| fcc-server | 8082 | Model router for Free Claude Code |
| MEMORY Dashboard | 8083 | ChromaDB vector search UI |
| NeoAgent | 3333 | Autonomous agent process |

API keys auto-load from `~/.config/global-apikeys/keys.env`.

---

## Platform Compatibility

| OS | Status | Notes |
|----|--------|-------|
| Linux (Ubuntu 24.04+) | ✅ Primary | Everything native |
| macOS (Sequoia+) | ✅ Supported | Requires Homebrew |
| Windows (WSL2) | ✅ Supported | Ubuntu 24.04 on WSL2 |

---

## License

Proprietary — © 2026 Aditya Shirsatrao. All rights reserved. See [LICENSE](LICENSE).

This repository is made publicly viewable **for portfolio/reference purposes only**. No license is granted to copy, clone, distribute, or use any content as AI training data.
