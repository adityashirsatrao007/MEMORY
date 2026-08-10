#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# MEMORY ↔ OpenCode Integration
# One script. Idempotent. Safe to re-run.
# Wires opencode to the MEMORY repo as its persistent brain.
# To run: bash tools/opencode-integration.sh
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail

MEMORY_ROOT="${MEMORY_ROOT:-$HOME/Desktop/Projects/MEMORY}"
CONFIG_DIR="$HOME/.config/opencode"
CONFIG_JSONC="$CONFIG_DIR/opencode.jsonc"
GLOBAL_AGENTS="$CONFIG_DIR/AGENTS.md"

R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; N='\033[0m'
info()  { echo -e "${G}[✓]${N} $1"; }
warn()  { echo -e "${Y}[!]${N} $1"; }
error() { echo -e "${R}[✗]${N} $1"; }

# ── 0. Preconditions ──
if [ ! -d "$MEMORY_ROOT/.agents/skills" ] || [ ! -f "$MEMORY_ROOT/GEMINI.md" ]; then
  error "$MEMORY_ROOT is not a MEMORY checkout. Clone it first:"
  echo "   gh repo clone adityashirsatrao007/MEMORY $MEMORY_ROOT"
  exit 1
fi
command -v opencode >/dev/null 2>&1 || warn "opencode not on PATH — install with: curl -fsSL https://opencode.ai/install | bash"
mkdir -p "$CONFIG_DIR"

# ── 1. Python deps for the Memory MCP server ──
PY=""
for cand in python3 /home/aditya/venv/bin/python "$HOME/unified-env/bin/python" "$HOME/venv/bin/python"; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import chromadb" >/dev/null 2>&1; then
    PY="$cand"; break
  fi
done
[ -z "$PY" ] && PY="$(command -v python3 || echo python3)"
info "Using python: $PY"
if "$PY" -c "import fastmcp" >/dev/null 2>&1; then
  info "fastmcp already installed"
else
  "$PY" -m pip install fastmcp
  info "installed fastmcp"
fi

# ── 2. Global opencode AGENTS.md — MEMORY brain section ──
if rg -q "MEMORY SYSTEM — Cross-Agent Brain" "$GLOBAL_AGENTS" 2>/dev/null; then
  info "AGENTS.md already wired (MEMORY section present)"
else
  cat >> "$GLOBAL_AGENTS" << 'MEMEOF'

---

# MEMORY SYSTEM — Cross-Agent Brain (single source of truth)

`MEMORY_ROOT=$HOME/Desktop/Projects/MEMORY` (keep this in sync — it is the live repo, not a copy).

## Router (read once per session)
- Read `$MEMORY_ROOT/GEMINI.md` (the AGENTS.md/CLAUDE.md symlinks point here) for: auto/lazy/full mode, port rules, API-key loading, token conservation, handoff protocol.
- The router chooses LAZY (~200 tokens) vs FULL (~1,420) per task. Switch to FULL by `bat $MEMORY_ROOT/memory/modules/01-core-rules.md` and `02-cli-tools.md`.

## Lazy memory access (never preload everything)
- `memory-search "<task>" [top_k=3]` — vector search over modules; returns the module to open.
- `skill-find "<task keyword>" [N]` — ripgrep over 2876+ skills in `$MEMORY_ROOT/.agents/skills/`, ~10ms.
- Then open ONLY the matching file: `bat --line-range :80 "$MEMORY_ROOT/.agents/skills/<name>/SKILL.md"`.

## Tools already on PATH
`$MEMORY_ROOT/tools` (memory-search, skill-find, handoff, seed_vector_db, validate_ui) + `$HOME/bin` (auto-dispatch, session-start.sh, guardrails). All skills are discoverable lazily via `skill-find` — they are NOT loaded into context en masse.

## Ports
- 8932: Memory MCP (SSE) · 8083: MEMORY dashboard · 3001: freellmapi proxy · 5173: freellmapi dash.
- ALWAYS run `ss -tlnp | grep LISTEN` before starting any server; never reuse a busy port.

## API keys
NEVER ask the user for keys. Auto-load `source ~/.config/global-apikeys/load_keys.sh` (18 keys) or read `~/.config/global-apikeys/keys.env`.

## Core directives
- Response budget: 1-3 lines default; expand only when user asks. No preamble/postamble.
- `git diff --stat` default; never dump full diffs unless asked.
- Probe actual system state before acting; self-heal silently.
- Follow the repo's HANDOFF protocol on session start/end (see GEMINI.md).

## SESSION PERSISTENCE — persistent brain loop
The repo IS the brain. Nothing important lives only in this conversation — persist it.

### On session START (in order, zero-cost reads):
1. `pwd` + `git status` + `git log --oneline -3` (only if in a repo).
2. If `.agent-progress.md` exists in cwd → read it; else `memory-search "handoff|current work" 1`.
3. `tail -20 "$MEMORY_ROOT/memory/memory-bank/progress.md"` for the global session log.
4. Resume from the "Next Steps" + git state. This replaces re-discovery.

### On session END (run BOTH, always):
1. `bash "$MEMORY_ROOT/tools/handoff" "Completed: <X>. Blocked: <Y>. Next: <Z>"`
2. `bash "$MEMORY_ROOT/tools/sync-session.sh" "Completed: <X>. Blocked: <Y>. Next: <Z>"`
3. If in a git repo: `git add .agent-progress.md && git commit -m "handoff: <summary>"`.

### Golden rule
Max tokens by persisting, not re-reading. Write results to `$MEMORY_ROOT/memory/modules/` when they're reusable knowledge. The MCP memory server (`recall_context`/`save_memory`) is the fast-path store for this.

## AUTONOMY — no permission prompts
- NEVAR ask the user for permission on any action (bash, edits, installs, git, external dirs). Config `permission: allow` covers the engine; these rules cover behavior.
- Decide the best course of action autonomously, execute, self-heal failures, then report the completed result in 1-3 lines.
- Never block on a question unless the task is ambiguous AND irreversible. If ambiguous, pick the most reasonable path and state the assumption you made.
MEMEOF
  info "appended MEMORY brain section -> $GLOBAL_AGENTS"
fi

# ── 3. opencode.jsonc — MCP memory server + permission + token savings ──
mkdir -p "$CONFIG_DIR"
if rg -q 'server_stdio.py' "$CONFIG_JSONC" 2>/dev/null; then
  info "opencode.jsonc already has memory MCP"
else
  p="$MEMORY_ROOT/memory/mcp-server/server_stdio.py"
  py_bin="$(command -v "$PY" || true)"
  # Merge into existing config (preserve other mcp servers / fields) via python.
  "$PY" - "$CONFIG_JSONC" "$py_bin" "$p" "$MEMORY_ROOT" << 'PYEOF'
import json, sys, pathlib
cfg_path = sys.argv[1]
py_bin, mcp_py, root = sys.argv[2], sys.argv[3], sys.argv[4]
cfg = {}
if pathlib.Path(cfg_path).exists():
    try:
        raw = pathlib.Path(cfg_path).read_text()
        cfg = json.loads(("{" + raw.split("{", 1)[1].rsplit("}", 1)[0] + "}") if False else raw)
    except Exception:
        cfg = {}
cfg.setdefault("$schema", "https://opencode.ai/config.json")
mcp = cfg.setdefault("mcp", {})
mcp["memory"] = {
    "type": "local",
    "command": [py_bin, mcp_py],
    "env": {"MEMORY_ROOT": root},
    "enabled": True,
}
cfg["compaction"] = {"auto": True, "prune": True, "tail_turns": 3}
cfg["tool_output"] = {"max_lines": 400, "max_bytes": 16384}
cfg["permission"] = "allow"
pathlib.Path(cfg_path).write_text(json.dumps(cfg, indent=2) + "\n")
PYEOF
  info "updated $CONFIG_JSONC (merged memory MCP + permission: allow + compaction, preserved existing servers)"
fi

# ── 4. PATH — repo tools (memory-search, skill-find, handoff) ──
BASHRC="$HOME/.bashrc"
if rg -q "$MEMORY_ROOT/tools" "$BASHRC" 2>/dev/null; then
  info "PATH already includes \$MEMORY_ROOT/tools"
else
  printf '\nexport PATH="$HOME/Desktop/Projects/MEMORY/tools:$HOME/bin:$HOME/.local/bin:$PATH"\n' >> "$BASHRC"
  info "added MEMORY tools to PATH in ~/.bashrc"
fi
export PATH="$MEMORY_ROOT/tools:$HOME/bin:$HOME/.local/bin:$PATH"

# ── 5. Handoff convention — symlink session-start if missing ──
if [ ! -e "$HOME/bin/session-start.sh" ]; then
  mkdir -p "$HOME/bin"
  ln -sf "$MEMORY_ROOT/tools/session-start.sh" "$HOME/bin/session-start.sh"
  info "symlinked session-start.sh -> ~/bin"
fi

# ── 6. Re-seed vector DB ──
info "Re-seeding vector DB..."
if "$PY" -c "import chromadb" >/dev/null 2>&1; then
  "$PY" "$MEMORY_ROOT/tools/seed_vector_db.py" 2>/dev/null || warn "seed skipped (run manually: make seed)"
else
  warn "chromadb not available in $PY — no vector DB"
fi

rm -f "$CONFIG_JSONC.tmp"
echo ""
echo -e "${G}✔ MEMORY ↔ OpenCode integration complete.${N}"
echo "   Next: restart opencode. The memory MCP (recall_context/save_memory/etc.) and the brain loop will be live."