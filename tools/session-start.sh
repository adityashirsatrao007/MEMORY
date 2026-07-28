#!/usr/bin/env bash
# MEMORY — Session Start Script
# Run as first action every session

MEMORY_ROOT="${MEMORY_ROOT:-$(pwd)}"

# 1. Clear session read cache
rm -f .session-read-cache 2>/dev/null

# 2. Activate venv if in MEMORY repo
if [ -f "$MEMORY_ROOT/.venv/bin/activate" ]; then
    source "$MEMORY_ROOT/.venv/bin/activate"
    export MEMORY_NON_COMMERCIAL=1
fi

# 3. Set environment
export MEMORY_ROOT
export MEMORY_MODE="lazy"
export PATH="$MEMORY_ROOT/tools:$HOME/bin:$HOME/.local/bin:$PATH"

# 4. Check git status
if git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Branch: $(git branch --show-current)"
    echo "Last: $(git log --oneline -1)"
fi

# 5. Read handoff if exists
if [ -f ".agent-progress.md" ]; then
    echo "=== HANDOFF ==="
    head -20 .agent-progress.md
    echo "==============="
fi

echo "Session ready. Mode: lazy (~200 tokens)"
