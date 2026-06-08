# MEMORY — Agent Configuration & Cross-Device Setup

> Copy the prompt below, paste it to **Antigravity** (or any agent) on your new machine.
> It works on **Linux**, **macOS**, and **Windows (WSL2)**.

---

## Setup Prompt — Copy & Paste This Into Antigravity

```
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
```

---

## After Setup — First Session

After running the prompt above, run this to verify the agent can see your full toolchain:

```bash
source ~/Desktop/Projects/MEMORY/bin/session-start.sh ~/Desktop/Projects/MEMORY
```

Expected output (minimal — just error reports and repo summary):
```
Aditya ~ git version 2.53.0
---------------------------
```

If you see missing tool warnings, the agent will auto-install them.

---

## What Gets Installed

| Layer | Tools |
|---|---|
| **Shell** | bash, zoxide, fzf, starship, tmux |
| **Lang runtimes** | Node 24, Python 3, Go, Rust |
| **Package mgrs** | npm, bun, pipx, cargo |
| **CLI replacements** | rg, bat, eza, fd, dust, btop, procs, sd |
| **Agent tools** | opencode, aider, ollama, codeburn |
| **Git** | gh, lazygit, delta, gitleaks, trufflehog |
| **Dev tools** | docker, pm2, hyperfine, entr, ngrok |
| **Security** | trivy, semgrep, gitleaks |
| **Data** | jq, yq, fx, jless, chromadb |
| **Monitor** | btm, btop, procs, duf, fastfetch |
| **Vector DB** | ChromaDB dashboard at localhost:8082 |

---

## Platform Notes

| OS | Notes |
|---|---|
| **Linux** | Everything native. Run the prompt directly. |
| **macOS** | Needs Homebrew pre-installed. Some system packages differ (no apt). The prompt auto-detects. |
| **Windows** | **Must use WSL2** (Ubuntu 24.04). Run inside WSL terminal. Docker Desktop for WSL. |
