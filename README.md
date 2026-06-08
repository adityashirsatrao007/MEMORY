# MEMORY — Agent Configuration Hub

Central repo for AI agent rules, CLI tool dispatch, and workspace configs.

Master rules: [`GEMINI.md`](GEMINI.md) — all AI agents symlink here via AGENTS.md / CLAUDE.md

## Quick Start

```bash
make validate   # Check all 9 module files
make seed       # Re-vector ChromaDB (98 chunks across 10 files)
make stats      # Module sizes and token savings
make all        # validate + seed
```

## File Tree

```
$MEMORY_ROOT/
├── GEMINI.md                     ← Index (56 lines)
├── AGENTS.md -> GEMINI.md       ← All tools symlink here
├── .githooks/                    ← Auto-seed vector DB on module changes
├── memory/
│   ├── modules/                  ← 9 focused modules (2,279 lines)
│   ├── memory-bank/              ← Progress, decisions, architecture
│   ├── vector_db/                ← ChromaDB (disk-based, 0 RAM)
│   └── LESSONS_LEARNED.md        ← Cross-project error patterns
├── tools/                        ← dashboard.py, seed_vector_db.py
├── Makefile                      ← validate, seed, stats, hooks
├── opencode.json                 ← Points instructions to GEMINI.md
└── config/                       ← opencode sub-config
```

**Dashboard:** `http://localhost:8082` — semantic search across all modules
**Vector DB:** 98 chunks from 10 files — `make seed` to rebuild
