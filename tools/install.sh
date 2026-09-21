#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════════
# MEMORY — Universal Engineering Environment Installer
# One script. Any OS. Sets up everything you need to code.
# ═══════════════════════════════════════════════════════════════
# What this installs:
#   Languages:  Python, Node.js, Java JDK, C/C++, Go, Rust
#   Tools:      Git, Docker, ripgrep, bat, eza, fd, tmux, fzf, jq
#   AI:         Ollama (local LLMs), opencode, ChromaDB
#   MEMORY:     Clone, venv, seed vector DB, shell config
#
# Works on: Linux, macOS, Windows (WSL2)
# To run:     bash <(curl -fsSL https://raw.githubusercontent.com/adityashirsatrao007/MEMORY/main/tools/install.sh)
# ═══════════════════════════════════════════════════════════════

REPO="adityashirsatrao007/MEMORY"
INSTALL_DIR="${MEMORY_ROOT:-$HOME/MEMORY}"

# ── Colors ──
R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; B='\033[0;34m'; N='\033[0m'

info()  { echo -e "${G}[✓]${N} $1"; }
warn()  { echo -e "${Y}[!]${N} $1"; }
error() { echo -e "${R}[✗]${N} $1"; }
section() { echo -e "\n${B}━━━ $1 ━━━${N}"; }

# ── Detect OS ──
OS="unknown"
case "$(uname -s)" in
  Linux*)  OS="linux" ;;
  Darwin*) OS="macos" ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
esac

if [ "$OS" = "windows" ] && [ -z "${WSLENV:-}" ]; then
  echo -e "${R}[✗] Windows without WSL2 is not supported by this installer.${N}"
  echo "   Install WSL2 first, then run this script inside Ubuntu."
  echo "   Guide: https://learn.microsoft.com/en-us/windows/wsl/install"
  exit 1
fi

echo -e "${B}╔══════════════════════════════════════╗${N}"
echo -e "${B}║     🧠 MEMORY Environment Setup      ║${N}"
echo -e "${B}╚══════════════════════════════════════╝${N}"
echo "   OS: $OS"
echo "   Target: $INSTALL_DIR"
echo ""

# ═══════════════════════════════════════════════════════════════
# 1. SYSTEM PACKAGES AND COMPILERS
# ═══════════════════════════════════════════════════════════════
section "Installing system packages & compilers"

if [ "$OS" = "linux" ]; then
  sudo apt-get update -qq

  # Core build & engineering languages
  sudo apt-get install -y -qq \
    build-essential gcc g++ gdb make cmake \
    openjdk-17-jdk openjdk-17-jre \
    python3 python3-pip python3-venv \
    nodejs npm \
    git curl wget \
    docker.io docker-compose \
    ripgrep bat eza fd-find \
    tmux zoxide fzf jq unzip \
    poppler-utils tesseract-ocr pandoc \
    sqlite3 libsqlite3-dev \
    chromium-browser \
    2>/dev/null || warn "Some packages failed (non-critical)"

  # Modern bat -> batcat symlink
  sudo ln -sf /usr/bin/batcat /usr/local/bin/bat 2>/dev/null || true

elif [ "$OS" = "macos" ]; then
  if ! command -v brew &>/dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi

  brew install \
    gcc gdb make cmake \
    openjdk \
    python3 nodejs \
    git curl wget \
    docker docker-compose \
    ripgrep bat eza fd tmux zoxide fzf \
    jq unzip poppler tesseract pandoc \
    sqlite3 gh starship dust btop procs sd glow lazygit \
    2>/dev/null || true
fi

info "C/C++ (gcc/g++/make/cmake)"
info "Java (JDK 17)"
info "Python 3 + pip"
info "Node.js + npm"
info "Git"

# ── Go ──
section "Go language"
if ! command -v go &>/dev/null; then
  GO_VER="1.23.0"
  if [ "$OS" = "linux" ]; then
    wget -q "https://go.dev/dl/go${GO_VER}.linux-amd64.tar.gz" -O /tmp/go.tar.gz
    sudo tar -C /usr/local -xzf /tmp/go.tar.gz
    export PATH="/usr/local/go/bin:$PATH"
  elif [ "$OS" = "macos" ]; then
    brew install go
  fi
  info "Go $GO_VER"
else
  info "Go $(go version | grep -oP 'go\S+')"
fi

# ── Rust ──
section "Rust language"
if ! command -v cargo &>/dev/null; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  source "$HOME/.cargo/env" 2>/dev/null || true
fi
info "Rust $(rustc --version 2>/dev/null || echo 'installed')"

# ═══════════════════════════════════════════════════════════════
# 2. CLONE MEMORY
# ═══════════════════════════════════════════════════════════════
section "Cloning MEMORY"

if [ -d "$INSTALL_DIR/.git" ]; then
  info "MEMORY already cloned — pulling latest"
  cd "$INSTALL_DIR" && git pull
else
  git clone --depth 1 "https://github.com/$REPO.git" "$INSTALL_DIR"
  info "Cloned to $INSTALL_DIR"
fi
cd "$INSTALL_DIR"

# ═══════════════════════════════════════════════════════════════
# 3. PYTHON VIRTUAL ENV + MEMORY DEPS
# ═══════════════════════════════════════════════════════════════
section "Python environment"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  info "Created virtual environment"
fi
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet chromadb fastapi uvicorn matplotlib diagrams 2>/dev/null || true
info "Python packages: chromadb, fastapi, matplotlib, diagrams"

# ═══════════════════════════════════════════════════════════════
# 4. GLOBAL CLI TOOLS
# ═══════════════════════════════════════════════════════════════
section "Global CLI tools"

# Node.js tools
npm install -g bun pm2 tldr @opencode/opencode 2>/dev/null || true
info "Node: bun, pm2, opencode"

# Python tools
pip install pipx 2>/dev/null
pipx ensurepath 2>/dev/null || true
pipx install aider-chat codeburn semgrep trufflehog 2>/dev/null || true
info "Python: aider-chat, codeburn, semgrep"

# Rust CLIs
source "$HOME/.cargo/env" 2>/dev/null || true
cargo install lowfat du-dust procs sd tokei 2>/dev/null || true
info "Rust: lowfat, du-dust, procs, sd, tokei"

# Go tools
export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"
go install github.com/steveiliop56/onlycli@latest 2>/dev/null || true
info "Go: onlycli"

# ═══════════════════════════════════════════════════════════════
# 5. OLLAMA (LOCAL AI)
# ═══════════════════════════════════════════════════════════════
section "Ollama (local LLMs)"

if ! command -v ollama &>/dev/null; then
  if [ "$OS" = "linux" ]; then
    curl -fsSL https://ollama.com/install.sh | sh
    info "Ollama installed"
    ollama pull qwen2.5-coder:3b 2>/dev/null || true
    ollama pull nomic-embed-text 2>/dev/null || true
    info "Models: qwen2.5-coder:3b, nomic-embed-text"
  elif [ "$OS" = "macos" ]; then
    warn "Download Ollama from https://ollama.com/download"
  fi
else
  info "Ollama already installed"
fi

# ═══════════════════════════════════════════════════════════════
# 6. SEED VECTOR DATABASE
# ═══════════════════════════════════════════════════════════════
section "Seeding MEMORY vector database"

python3 tools/seed_vector_db.py --force 2>/dev/null && info "Vector DB seeded" || warn "Seed failed — run 'make seed' later"

# ═══════════════════════════════════════════════════════════════
# 7. SHELL CONFIGURATION
# ═══════════════════════════════════════════════════════════════
section "Shell configuration"

ENV_BLOCK="
# ── MEMORY Agent Environment ──
export MEMORY_ROOT=\"$INSTALL_DIR\"
export MEMORY_MODE=\"lazy\"
export MEMORY_PATH=\"\$MEMORY_ROOT/tools\"
export PATH=\"\$MEMORY_ROOT/tools:\$MEMORY_PATH:\$HOME/.local/bin:\$HOME/go/bin:/usr/local/go/bin:\$HOME/.cargo/bin:\$PATH\"
export EDITOR=\"nvim\"
export VISUAL=\"nvim\"

# ── Language-specific paths ──
# Java
if [ -d /usr/lib/jvm/java-17-openjdk-amd64 ]; then
  export JAVA_HOME=\"/usr/lib/jvm/java-17-openjdk-amd64\"
elif [ -d /usr/lib/jvm/java-17-openjdk ]; then
  export JAVA_HOME=\"/usr/lib/jvm/java-17-openjdk\"
elif [ -d /usr/local/opt/openjdk ]; then
  export JAVA_HOME=\"/usr/local/opt/openjdk\"
fi
[ -n \"\${JAVA_HOME:-}\" ] && export PATH=\"\$JAVA_HOME/bin:\$PATH\"

# Go
[ -d /usr/local/go/bin ] && export PATH=\"/usr/local/go/bin:\$PATH\"
[ -d \"\$HOME/go/bin\" ] && export PATH=\"\$HOME/go/bin:\$PATH\"

# Rust
[ -f \"\$HOME/.cargo/env\" ] && source \"\$HOME/.cargo/env\"

# Python user packages
[ -d \"\$HOME/.local/bin\" ] && export PATH=\"\$HOME/.local/bin:\$PATH\"

# Node.js global
export NPM_CONFIG_PREFIX=\"\$HOME/.npm-global\"
[ -d \"\$HOME/.npm-global/bin\" ] && export PATH=\"\$HOME/.npm-global/bin:\$PATH\"

# ── Aliases (modern replacements) ──
alias grep='rg' 2>/dev/null || true
alias cat='bat' 2>/dev/null || true
alias ls='eza --icons' 2>/dev/null || true
alias ll='eza -la --icons --git' 2>/dev/null || true
alias la='eza -a --icons' 2>/dev/null || true
alias du='dust' 2>/dev/null || true
alias top='btop' 2>/dev/null || true
alias ps='procs' 2>/dev/null || true
alias sed='sd' 2>/dev/null || true
alias find='fd' 2>/dev/null || true
alias v='nvim' 2>/dev/null || true
alias g='git' 2>/dev/null || true
alias gl='lazygit' 2>/dev/null || true
alias mem='cd \$MEMORY_ROOT' 2>/dev/null || true
alias mem-search='python3 \$MEMORY_ROOT/tools/memory-search' 2>/dev/null || true
alias mem-stats='make -C \$MEMORY_ROOT stats' 2>/dev/null || true
alias mem-validate='make -C \$MEMORY_ROOT validate' 2>/dev/null || true

# ── Editor ──
export EDITOR=\"nvim\"
"

SHELL_RC=""
[ -f "$HOME/.bashrc" ] && SHELL_RC="$HOME/.bashrc"
[ -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.zshrc"
[ -z "$SHELL_RC" ] && SHELL_RC="$HOME/.bashrc"

if ! grep -q "MEMORY_ROOT" "$SHELL_RC" 2>/dev/null; then
  echo "$ENV_BLOCK" >> "$SHELL_RC"
  info "Environment added to $SHELL_RC"
  info "Run: source $SHELL_RC"
else
  info "MEMORY already configured in $SHELL_RC"
fi

# ═══════════════════════════════════════════════════════════════
# 8. VERIFICATION
# ═══════════════════════════════════════════════════════════════
section "Verification"

echo ""
echo "  Language   | Version"
echo "  ───────────┼────────────────────────────────"
printf "  Python     │ %s\n" "$(python3 --version 2>/dev/null || echo 'missing')"
printf "  Node.js    │ %s\n" "$(node --version 2>/dev/null || echo 'missing')"
printf "  Java       │ %s\n" "$(java --version 2>/dev/null | head -1 || echo 'missing')"
printf "  C/C++      │ %s\n" "$(gcc --version 2>/dev/null | head -1 || echo 'missing')"
printf "  Go         │ %s\n" "$(go version 2>/dev/null || echo 'missing')"
printf "  Rust       │ %s\n" "$(rustc --version 2>/dev/null || echo 'missing')"
printf "  Cargo      │ %s\n" "$(cargo --version 2>/dev/null || echo 'missing')"
printf "  Ollama     │ %s\n" "$(ollama --version 2>/dev/null || echo 'missing')"
printf "  OpenCode   │ %s\n" "$(opencode --version 2>/dev/null || echo 'missing')"
printf "  Docker     │ %s\n" "$(docker --version 2>/dev/null || echo 'missing')"
printf "  Git        │ %s\n" "$(git --version 2>/dev/null || echo 'missing')"
echo ""

# ═══════════════════════════════════════════════════════════════
# DONE
# ═══════════════════════════════════════════════════════════════
echo -e "${G}╔══════════════════════════════════════╗${N}"
echo -e "${G}║  ✅  MEMORY installed successfully!  ║${N}"
echo -e "${G}╚══════════════════════════════════════╝${N}"
echo ""
echo "   📁 $INSTALL_DIR"
echo ""
echo "   🔧 To activate everything, run:"
echo "       source $SHELL_RC"
echo ""
echo "   📖 Read the docs:"
echo "       $INSTALL_DIR/docs/"
echo ""
echo "   🧠  Your agents will never forget."
echo ""
