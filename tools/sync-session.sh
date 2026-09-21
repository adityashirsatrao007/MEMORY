#!/bin/bash
# Copyright (c) 2026 Aditya Shirsatrao
# MIT License — see LICENSE file.
#
# Sync session progress to memory + re-seed vector DB.
# Run this at the END of every agent session.
#
# Usage:
#   make session-end MSG="did X, Y, Z"
#   # or directly:
#   bash tools/sync-session.sh "did X, Y, Z"
#
# If MSG is empty, reads from agent-progress draft if it exists.

set -e
MEMORY_ROOT="${MEMORY_ROOT:-/home/aditya/Desktop/Projects/MEMORY}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
MSG="${*}"

# 1. Read msg from arg, or from draft, or prompt
if [ -z "$MSG" ]; then
    if [ -f "$MEMORY_ROOT/.agent-progress.md" ]; then
        MSG=$(grep -m1 '## Session Notes' -A1 "$MEMORY_ROOT/.agent-progress.md" | tail -1 | sed 's/^[-* ]*//')
    fi
fi
if [ -z "$MSG" ]; then
    MSG="Session work (no summary provided)"
fi

# 2. Escaped for markdown table
ESCAPED=$(echo "$MSG" | sed 's/|/\\|/g')

# 3. Append to progress.md session log
PROGRESS_FILE="$MEMORY_ROOT/memory/memory-bank/progress.md"
if ! grep -q '^## Session Log' "$PROGRESS_FILE" 2>/dev/null; then
    # No session log section yet — create one after Current Status section
    printf '\n## Session Log\n| Date | What Was Done |\n|------|--------------|\n' >> "$PROGRESS_FILE"
fi

# Find the Session Log section and append after the last table row
sed -i "/^## Session Log/,/^## /{ /^## Session Log/a\\
| $TIMESTAMP | $ESCAPED |
}" "$PROGRESS_FILE" 2>/dev/null || {
    # Fallback: just append at end
    echo "| $TIMESTAMP | $ESCAPED |" >> "$PROGRESS_FILE"
}

echo "  ✅ Appended to memory/memory-bank/progress.md"

# 4. Update .agent-progress.md timestamp
AGENT_PROGRESS="$MEMORY_ROOT/.agent-progress.md"
if [ -f "$AGENT_PROGRESS" ]; then
    sed -i "s/^- \*\*Timestamp\*\*:.*/- **Timestamp**: $TIMESTAMP/" "$AGENT_PROGRESS"
    echo "  ✅ Updated .agent-progress.md timestamp"
fi

# 5. Re-seed vector DB (picks up all file changes)
echo "  Re-seeding vector DB..."
cd "$MEMORY_ROOT"
# Activate project venv for chromadb
if [ -f .venv/bin/activate ]; then
    . .venv/bin/activate 2>/dev/null || true
fi
python3 tools/seed_vector_db.py --force 2>&1 | sed 's/^/    /'
echo "  ✅ Vector DB re-seeded"
echo ""
echo "  ✅ Session synced. Next agent will find this context via memory-search."
