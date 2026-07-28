#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────
#  MEMORY — Setup
#  Run this script after cloning the repo.
# ──────────────────────────────────────────────────────

BOLD='\033[1m'
DIM='\033[2m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║              MEMORY — Setup                  ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""

# ─── Step 1: Check Python ───────────────────────────────

echo -e "${BOLD}[1/4] Checking prerequisites...${NC}"

PYTHON=""
for candidate in python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" &>/dev/null; then
        ver=$("$candidate" --version 2>&1 | grep -oP '\d+\.\d+')
        major="${ver%.*}"
        minor="${ver#*.}"
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ] 2>/dev/null; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "  ${RED}✗ Python 3.10+ not found${NC}"
    case "$(uname -s)" in
        Linux*)
            if command -v apt &>/dev/null; then
                echo "  → sudo apt install python3 python3-venv python3-pip"
            elif command -v dnf &>/dev/null; then
                echo "  → sudo dnf install python3 python3-pip"
            elif command -v pacman &>/dev/null; then
                echo "  → sudo pacman -S python python-pip"
            else
                echo "  Install it: https://www.python.org/downloads/"
            fi
            ;;
        Darwin*)
            echo "  → brew install python@3.12"
            echo "  (If you don't have Homebrew: https://brew.sh)"
            ;;
        *)
            echo "  Install it: https://www.python.org/downloads/"
            ;;
    esac
    exit 1
fi
echo -e "  ${GREEN}✓${NC} $("$PYTHON" --version) at $(command -v "$PYTHON")"

# ─── Step 2: Create virtual environment ─────────────────

echo -e "${BOLD}[2/4] Setting up virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    "$PYTHON" -m venv .venv
    echo -e "  ${GREEN}✓${NC} Created .venv"
else
    echo -e "  ${DIM}→ .venv already exists${NC}"
fi

# ─── Step 3: Install Python dependencies ────────────────

echo -e "${BOLD}[3/4] Installing dependencies...${NC}"
source .venv/bin/activate
pip install -q -U pip setuptools wheel 2>/dev/null
pip install -q chromadb 2>/dev/null && echo -e "  ${GREEN}✓${NC} chromadb installed"
echo -e "  ${GREEN}✓${NC} Dependencies ready"

# ─── Step 4: Verify setup ───────────────────────────────

echo ""
echo -e "${BOLD}[4/4] Setup complete${NC}"
echo ""
echo -e "  ${GREEN}Quick start:${NC}"
echo "    source .venv/bin/activate"
echo "    make validate"
echo ""

# Copy env example if not present
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo -e "  ${DIM}→ Created .env from .env.example (edit if needed)${NC}"
fi
