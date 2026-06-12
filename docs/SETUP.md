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

---

## Setup Prompt (Agent Handoff)

> Copy the block below and paste into your AI agent on a new machine.

\`\`\`
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
\`\`\`

## Verification

\`\`\`bash
source ~/Desktop/Projects/MEMORY/bin/session-start.sh ~/Desktop/Projects/MEMORY
\`\`\`
