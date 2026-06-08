# GEMINI — Agent Configuration Index

> **I am an index file.** All AI tools (opencode, claude, cursor, windsurf, etc.) symlink here via AGENTS.md / CLAUDE.md / .clinerules / .cursorrules / .windsurfrules / copilot-instructions.md.
>
> **MEMORY_ROOT** = `/home/aditya/Desktop/Projects/MEMORY` (set by session-start.sh)
> Use `$MEMORY_ROOT/memory/modules/<file>.md` to load modules from any working directory.

## Always Load (core — every session)

Loaded automatically by `session-start.sh` step 1:

| Module | Lines | What It Contains |
|--------|-------|-----------------|
| `$MEMORY_ROOT/memory/modules/01-core-rules.md` | 324 | Session protocol, Karpathy, prod standards, self-healing, code review |
| `$MEMORY_ROOT/memory/modules/02-cli-tools.md` | 398 | 54-tool dispatch table, guardrails, zero-token CLI, token optimization |

## Load by Task

| Task | Module |
|------|--------|
| ML training, model serving, MLOps | `$MEMORY_ROOT/memory/modules/03-ml-engineering.md` (292 lines) |
| Security audit, secret scanning | `$MEMORY_ROOT/memory/modules/04-security.md` (147 lines) |
| UI/UX design, animations, 3D, Remix | `$MEMORY_ROOT/memory/modules/05-ui-ux.md` (260 lines) |
| Web dev, project setup, SEO | `$MEMORY_ROOT/memory/modules/06-web-dev.md` (305 lines) |
| Resumes, LinkedIn, job hunt | `$MEMORY_ROOT/memory/modules/07-job-hunt.md` (145 lines) |
| Architecture, SAGA, CQRS, EDA | `$MEMORY_ROOT/memory/modules/08-architecture.md` (198 lines) |
| Roadmap, GitHub tricks, OSM, misc | `$MEMORY_ROOT/memory/modules/09-misc.md` (210 lines) |

## Quick Reference

```
MEMORY_ROOT=/home/aditya/Desktop/Projects/MEMORY
symlinks:   AGENTS.md, CLAUDE.md, .clinerules, .cursorrules → GEMINI.md
opencode:   reads GEMINI.md → agent loads relevant modules
dashboard:  http://localhost:8082 — vector search across all modules
Makefile:   cd $MEMORY_ROOT && make validate  — check all modules
            cd $MEMORY_ROOT && make seed     — re-vector ChromaDB
            cd $MEMORY_ROOT && make stats    — module sizes + token savings
```

## File Tree

```
$MEMORY_ROOT/
├── GEMINI.md                    ← THIS FILE — index (56 lines)
├── AGENTS.md -> GEMINI.md       ← all AI tools symlink here
├── .githooks/                   ← tracked hooks: post-commit auto-seeds vector DB
├── memory/
│   ├── modules/                 ← 9 focused modules (2,279 lines total)
│   ├── memory-bank/             ← progress, decisions, session logs
│   ├── vector_db/               ← ChromaDB (disk-based, 0 RAM)
│   └── LESSONS_LEARNED.md       ← cross-project error patterns
├── tools/                       ← dashboard.py, seed_vector_db.py
├── Makefile                     ← validate, seed, stats, hooks targets
├── config/                      ← opencode, README
└── dotfiles/                    ← bash, git, starship, tmux
```
