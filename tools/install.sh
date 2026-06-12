#!/usr/bin/env bash
set -euo pipefail

# MEMORY — Cross-Platform Installer
# Detects OS and installs dependencies accordingly.

REPO="adityashirsatrao007/MEMORY"
BRANCH="main"
INSTALL_DIR="${MEMORY_ROOT:-$HOME/MEMORY}"

echo "🧠 MEMORY Installer"
echo "━━━━━━━━━━━━━━━━━━"

# --- Detect OS ---
OS="unknown"
case "$(uname -s)" in
  Linux*)  OS="linux" ;;
  Darwin*) OS="macos" ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
esac

# Windows check: require WSL2
if [ "$OS" = "windows" ] && [ -z "${WSLENV:-}" ]; then
  echo "❌ Windows without WSL2 is not supported by this installer."
  echo "   Please use WSL2 or follow the manual setup in docs/SETUP.md"
  exit 1
fi

echo "📦 Detected OS: $OS"
echo "📁 Install target: $INSTALL_DIR"

# --- Clone / Pull ---
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "🔄 MEMORY already installed — pulling latest..."
  cd "$INSTALL_DIR" && git pull
else
  echo "📥 Cloning MEMORY..."
  git clone --depth 1 "https://github.com/$REPO.git" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# --- Python venv ---
if [ ! -d ".venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet chromadb fastapi uvicorn matplotlib diagrams

# --- System deps ---
echo "🔧 Installing system dependencies..."
if [ "$OS" = "linux" ]; then
  sudo apt-get update -qq
  sudo apt-get install -y -qq \
    git curl wget python3 python3-pip python3-venv \
    nodejs npm ripgrep bat eza fd-find tmux zoxide fzf \
    jq unzip poppler-utils tesseract-ocr pandoc chromium-browser 2>/dev/null || true
  sudo ln -sf /usr/bin/batcat /usr/local/bin/bat 2>/dev/null || true
elif [ "$OS" = "macos" ]; then
  if ! command -v brew &>/dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  brew install git curl wget python3 nodejs ripgrep bat eza fd \
    tmux zoxide fzf jq unzip poppler tesseract pandoc \
    gh starship dust btop procs sd glow lazygit 2>/dev/null || true
fi

# --- Node.js tools ---
echo "📦 Installing Node.js CLI tools..."
npm install -g bun pm2 tldr @opencode/opencode 2>/dev/null || true

# --- Python tools ---
echo "📦 Installing Python CLI tools..."
pip install pipx 2>/dev/null
pipx ensurepath 2>/dev/null
pipx install aider-chat codeburn semgrep trufflehog 2>/dev/null || true

# --- Rust tools ---
if ! command -v cargo &>/dev/null; then
  echo "🦀 Installing Rust..."
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
fi
source "$HOME/.cargo/env" 2>/dev/null || true
cargo install lowfat du-dust procs sd tokei 2>/dev/null || true

# --- Ollama ---
if ! command -v ollama &>/dev/null; then
  echo "🤖 Installing Ollama..."
  if [ "$OS" = "linux" ]; then
    curl -fsSL https://ollama.com/install.sh | sh
  elif [ "$OS" = "macos" ]; then
    echo "   Download from https://ollama.com/download — install manually"
  fi
fi

# --- Seed vector DB ---
echo "🌱 Seeding vector database..."
python3 tools/seed_vector_db.py --force 2>/dev/null || echo "   ⚠️ Seed failed — run 'make seed' later"

# --- Shell config ---
BASHRC_ADDITIONS='
# MEMORY
export MEMORY_ROOT="'"$INSTALL_DIR"'"
export MEMORY_MODE="lazy"
export PATH="$MEMORY_ROOT/tools:$PATH"
'

if [ -f "$HOME/.bashrc" ]; then
  if ! grep -q "MEMORY_ROOT" "$HOME/.bashrc" 2>/dev/null; then
    echo "$BASHRC_ADDITIONS" >> "$HOME/.bashrc"
    echo "   ✅ Added to ~/.bashrc"
  fi
elif [ -f "$HOME/.zshrc" ]; then
  if ! grep -q "MEMORY_ROOT" "$HOME/.zshrc" 2>/dev/null; then
    echo "$BASHRC_ADDITIONS" >> "$HOME/.zshrc"
    echo "   ✅ Added to ~/.zshrc"
  fi
fi

# --- Done ---
echo ""
echo "━━━━━━━━━━━━━━━━━━"
echo "✅ MEMORY installed!"
echo ""
echo "   📁 $INSTALL_DIR"
echo "   📖 Read the docs: $INSTALL_DIR/docs/"
echo ""
echo "   Next steps:"
echo "   1. Restart your shell or run: source ~/.bashrc"
echo "   2. Run: make validate"
echo "   3. Start coding with your AI agent!"
echo ""
echo "   🧠 Your agents will never forget."
echo "━━━━━━━━━━━━━━━━━━"
