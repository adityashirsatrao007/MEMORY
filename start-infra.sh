#!/usr/bin/env bash
set -e

MEMORY_ROOT=/home/aditya/Desktop/Projects/MEMORY
GODMODE_ROOT=/home/aditya/Desktop/Projects/G0DM0D3
HEADROOM_PORT=8787

echo "=== MEMORY Infrastructure Bootstrap ==="

# 1. Source API keys
if [ -f ~/.config/global-apikeys/keys.env ]; then
  set -a; source ~/.config/global-apikeys/keys.env; set +a
  echo "[ok] API keys loaded"
fi

# 2. Headroom proxy (context optimization layer)
if ! ss -tlnp | grep -q :$HEADROOM_PORT; then
  echo "[start] Headroom proxy on port $HEADROOM_PORT"
  headroom proxy --port $HEADROOM_PORT --memory &
  sleep 2
else
  echo "[ok] Headroom proxy already running on $HEADROOM_PORT"
fi

# 3. G0DM0D3 API (multi-model gateway)
if [ -f "$GODMODE_ROOT/.env" ] && ! ss -tlnp | grep -q :7860; then
  echo "[start] G0DM0D3 API"
  cd "$GODMODE_ROOT" && bash start.sh &
elif ss -tlnp | grep -q :7860; then
  echo "[ok] G0DM0D3 already running on 7860"
fi

# 4. MEMORY dashboard
if ! ss -tlnp | grep -q :8083; then
  echo "[start] MEMORY dashboard"
  python3 "$MEMORY_ROOT/tools/dashboard.py" &
else
  echo "[ok] Dashboard already running on 8083"
fi

# 5. Verify MCP servers
echo "[check] MCP server status:"
claude mcp list 2>/dev/null | grep -E "firecrawl|playwright|headroom|shadcn" || echo "  (run from Claude Code session)"

# 6. Sync graphify if code changed
if [ -f "$MEMORY_ROOT/graphify-out/graph.json" ]; then
  echo "[sync] Updating code knowledge graph"
  graphify update "$MEMORY_ROOT" 2>/dev/null || true
fi

echo "=== Infrastructure ready ==="
echo "  Headroom:   http://127.0.0.1:$HEADROOM_PORT"
echo "  G0DM0D3:    http://127.0.0.1:7860"
echo "  Dashboard:  http://127.0.0.1:8083"
echo ""
echo "  To run Claude through Headroom:"
echo "    headroom wrap claude"
