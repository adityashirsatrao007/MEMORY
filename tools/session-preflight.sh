#!/bin/bash
# Session preflight: generates a compact context blob for opencode sessions.
# Run at session start to have skill catalog ready.
# Output: prints skill catalog summary or writes to a file.

set -euo pipefail

MEMORY_ROOT="${MEMORY_ROOT:-$HOME/Desktop/Projects/MEMORY}"
CATALOG="$MEMORY_ROOT/memory/skills_catalog.md"
CATALOG_JSON="$MEMORY_ROOT/memory/skills_catalog.json"
SKILL_DIR="$MEMORY_ROOT/.agents/skills"
BLOB_DIR="$MEMORY_ROOT/memory/session_blobs"

# Generate catalog if missing or stale
if [ ! -f "$CATALOG" ] || [ "$(find "$SKILL_DIR" -name SKILL.md -newer "$CATALOG" 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "  Regenerating skill catalog..."
    python3 "$MEMORY_ROOT/tools/generate_skill_catalog.py" --md-only 2>/dev/null
fi

# Count skills
SKILL_COUNT=$(ls -d "$SKILL_DIR"/*/SKILL.md 2>/dev/null | wc -l)

# Generate compact blob (top 300 skills by name, one-liner each)
mkdir -p "$BLOB_DIR"
BLOB="$BLOB_DIR/preflight_context.md"

echo "# Session Preflight — $(date -Iseconds)" > "$BLOB"
echo "Skills available: $SKILL_COUNT" >> "$BLOB"
echo "" >> "$BLOB"

# Extract name + description from each skill's frontmatter (fast, no full reads)
echo "## Skill Index (top 300 by name)" >> "$BLOB"
count=0
for skill_dir in "$SKILL_DIR"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_file="${skill_dir}SKILL.md"
    if [ ! -f "$skill_file" ]; then
        continue
    fi
    
    name=$(basename "$skill_dir")
    desc=$(head -20 "$skill_file" | grep -i "^description:" | head -1 | sed 's/^description:[[:space:]]*//' | tr -d '"' | tr -d "'" | cut -c1-120)
    
    if [ -n "$desc" ]; then
        echo "- **$name**: $desc" >> "$BLOB"
    else
        echo "- **$name**" >> "$BLOB"
    fi
    
    count=$((count + 1))
    [ $count -ge 300 ] && break
done

echo "" >> "$BLOB"
echo "Showing $count of $SKILL_COUNT skills. Full catalog: \`$CATALOG\`" >> "$BLOB"
echo "Search: \`skill-find \"<query>\"\` | Vector: \`memory-search \"<query>\"\`" >> "$BLOB"

echo "  Preflight blob: $BLOB ($count skills, $(wc -c < "$BLOB") bytes)"
