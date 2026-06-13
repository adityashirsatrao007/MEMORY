#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────
#  MEMORY — Setup & License Activation
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
echo -e "${BOLD}║         MEMORY — Setup & Activation         ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""

# ─── Step 1: Check Python ───────────────────────────────

echo -e "${BOLD}[1/5] Checking prerequisites...${NC}"

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
    echo "  Install it: https://www.python.org/downloads/"
    echo "  Or on Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  Or on macOS: brew install python@3.12"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} $("$PYTHON" --version) at $(command -v "$PYTHON")"

# ─── Step 2: Create virtual environment ─────────────────

echo -e "${BOLD}[2/5] Setting up virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    "$PYTHON" -m venv .venv
    echo -e "  ${GREEN}✓${NC} Created .venv"
else
    echo -e "  ${DIM}→ .venv already exists${NC}"
fi

# ─── Step 3: Install Python dependencies ────────────────

echo -e "${BOLD}[3/5] Installing dependencies...${NC}"
source .venv/bin/activate
pip install -q -U pip setuptools wheel 2>/dev/null
pip install -q chromadb 2>/dev/null && echo -e "  ${GREEN}✓${NC} chromadb installed"
echo -e "  ${GREEN}✓${NC} Dependencies ready"

# ─── Step 4: License check ──────────────────────────────

echo -e "${BOLD}[4/5] Checking license status...${NC}"

LICENSE_FILE="$HOME/.config/memory/license.jwt"
LICENSE_KEY=""

if [ -f "$LICENSE_FILE" ]; then
    TOKEN=$(cat "$LICENSE_FILE")
    # Try online verification
    VERIFY_URL="https://memory-license-server.onrender.com/verify"
    FP=$(echo -n "$(hostname)-$(uname -s)-$(uname -m)" | sha256sum | cut -d' ' -f1)
    RESULT=$(curl -s -m 5 -X POST "$VERIFY_URL" \
        -H "Content-Type: application/json" \
        -d "{\"token\":\"$TOKEN\",\"machine_fingerprint\":\"$FP\"}" 2>/dev/null || echo '{"valid":false}')
    VALID=$(echo "$RESULT" | grep -o '"valid":true' || true)
    if [ -n "$VALID" ]; then
        TIER=$(echo "$RESULT" | grep -o '"tier":"[^"]*"' | cut -d'"' -f4 || echo "active")
        echo -e "  ${GREEN}✓${NC} License active (${TIER})"
    else
        echo -e "  ${YELLOW}⚠ License token found but could not verify server.${NC}"
        echo -e "  ${DIM}  → Offline grace may apply. Will use existing license.${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠ No license key found.${NC}"
    echo ""
    echo -e "  ${BOLD}This software requires a license for commercial use.${NC}"
    echo ""
    echo -e "  ${BOLD}Option A — Personal / Non-commercial use (FREE):${NC}"
    echo -e "  ${DIM}  Set this environment variable to skip the license check:${NC}"
    echo "    export MEMORY_NON_COMMERCIAL=1"
    echo ""
    echo -e "  ${BOLD}Option B — Get a trial or purchase a license:${NC}"
    echo "    1. Open this URL in your browser:"
    echo -e "       ${GREEN}https://adityashirsatrao007.github.io/MEMORY/docs/pricing.html${NC}"
    echo "    2. Enter your email and click 'Start Trial'"
    echo -e "    3. Copy the ${BOLD}license key${NC} shown on screen (also sent via email)"
    echo "    4. Run this command to activate:"
    echo -e "       ${GREEN}make license key=MEM-TRIAL-XXXX-XXXX-XXXX${NC}"
    echo ""
    echo -e "  ${YELLOW}Proceeding without activation — tools will prompt for license.${NC}"
fi

# ─── Step 5: Verify setup ───────────────────────────────

echo ""
echo -e "${BOLD}[5/5] Setup complete${NC}"
echo ""
echo -e "  ${GREEN}Quick start:${NC}"
echo "    source .venv/bin/activate"
echo "    make validate"
echo ""
echo -e "  ${DIM}If you see a license error, set MEMORY_NON_COMMERCIAL=1 or activate a key.${NC}"
echo ""

# Copy env example if not present
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo -e "  ${DIM}→ Created .env from .env.example (edit if needed)${NC}"
fi
