# MEMORY Repository Walkthrough

## Architecture
```
GEMINI.md (197KB, 3543 lines) ─── MASTER rules file
  ├── .clinerules              ─┐
  ├── .cursorrules             ─┤
  ├── .windsurfrules           ─┤  All symlinks to
  ├── AGENTS.md                ─┤  GEMINI.md
  ├── CLAUDE.md                ─┤
  ├── opencode/AGENTS.md       ─┘
  └── .github/copilot-instructions.md

14-lessons-learned.md ─── error log (moved to modules/)
dotfiles/ ─────────── bashrc, gitconfig, starship.toml, tmux.conf
templates/ ────────── animation libs, frontend refs, diagrams
tools/ ────────────── MCP server, dashboard, SDK, OpenWebUI tool
memory-bank/ ──────── progress, architecture, decisions, activeContext, walkthrough
vector_db/ ────────── ChromaDB persistent storage (gitignored)
```

## Key Files
| File | Purpose |
|------|---------|
| GEMINI.md | Master agent configuration (3543 lines, 197KB) |
| 14-lessons-learned.md | Permanent error memory + prevention patterns |
| opencode.json | Points OpenCode to AGENTS.md → GEMINI.md |
| .agentignore | Prevents agents from reading build artifacts |
| tools/mcp_server.py | ChromaDB MCP server for semantic memory search |
| dotfiles/install.sh | Symlinks bashrc, gitconfig, starship, tmux |

## Setup Steps
1. `git clone` to ~/Desktop/Projects/MEMORY
2. `cd dotfiles && ./install.sh && source ~/.bashrc`
3. Install CLI tools (see README.md)
4. `mkdir -p vector_db tools/static` (for MCP server + dashboard)
