# Installation

## Quick Install (All OS)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/adityashirsatrao007/MEMORY/main/tools/install.sh)
```

This installs: Python 3.10+ · ChromaDB · git hooks · symlinks

## Manual Setup

```bash
git clone https://github.com/adityashirsatrao007/MEMORY.git
cd MEMORY
make hooks          # install git hooks + seed vector DB
```

### Symlink for your agent

```bash
# Claude Code
ln -sf $PWD/GEMINI.md CLAUDE.md

# Cursor
ln -sf $PWD/GEMINI.md .cursorrules

# OpenCode
ln -sf $PWD/GEMINI.md AGENTS.md
```

## Requirements

- Python 3.10+
- `pip install chromadb`
- Linux / macOS / Windows (WSL2)

## Verify Installation

```bash
make validate   # checks all modules exist
make stats      # shows module sizes
make seed       # (re)seeds ChromaDB
```

See [docs/SETUP.md](docs/SETUP.md) for the full setup guide including agent handoff protocol, API key configuration, and troubleshooting.
