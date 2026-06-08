# GEMINI — Agent Configuration Index

> **I am an index file.** All AI tools (opencode, claude, cursor, windsurf, etc.) symlink here via AGENTS.md / CLAUDE.md / .clinerules / .cursorrules / .windsurfrules / copilot-instructions.md.
>
> My purpose is to tell you which module files to load. Do not load me and stop — read the relevant modules below.

## Always Load (core — every session)

These modules govern basic agent behavior and are loaded automatically by `session-start.sh`:

| Module | What It Contains |
|--------|-----------------|
| [`memory/modules/01-core-rules.md`](memory/modules/01-core-rules.md) | Session start protocol, hallucination prevention, Karpathy guidelines, tool installation, production standards, self-healing, memory bank, code review |
| [`memory/modules/02-cli-tools.md`](memory/modules/02-cli-tools.md) | 54-tool dispatch table, guardrails, zero-token CLI rulebook, token optimization, auto-dispatch, session-start.sh |

## Load by Task

| If you are doing this… | Load this module |
|------------------------|-----------------|
| ML training, model serving, MLOps | [`memory/modules/03-ml-engineering.md`](memory/modules/03-ml-engineering.md) |
| Security audit, secret scanning, password hashing | [`memory/modules/04-security.md`](memory/modules/04-security.md) |
| UI/UX design, animations, 3D, Remix docs | [`memory/modules/05-ui-ux.md`](memory/modules/05-ui-ux.md) |
| Web dev, project setup, SEO, CODVYN | [`memory/modules/06-web-dev.md`](memory/modules/06-web-dev.md) |
| Resume writing, LinkedIn, job applications | [`memory/modules/07-job-hunt.md`](memory/modules/07-job-hunt.md) |
| System architecture, SAGA, CQRS, EDA, scaling | [`memory/modules/08-architecture.md`](memory/modules/08-architecture.md) |
| Everything else (roadmap, GitHub tricks, OSM, misc) | [`memory/modules/09-misc.md`](memory/modules/09-misc.md) |

## Quick Reference

> **symlinks:** AGENTS.md, CLAUDE.md, .clinerules, .cursorrules, .windsurfrules, .github/copilot-instructions.md → all point here
>
> **opencode:** reads this index → agent decides which modules to load
>
> **session-start.sh (step 1):** auto-loads `memory/modules/01-core-rules.md` and `memory/modules/02-cli-tools.md`
>
> **auto-dispatch:** `auto-dispatch <task>` suggests the right tool + module
>
> **memory dashboard:** `http://localhost:8082` — search across all modules via vector DB

## Architecture

```
/home/aditya/Desktop/Projects/MEMORY/
├── GEMINI.md                    ← THIS FILE — index, 7KB
├── AGENTS.md -> GEMINI.md       ← all AI tools symlink here
├── memory/
│   ├── modules/                 ← 9 focused module files, ~2,278 lines total
│   │   ├── 01-core-rules.md     (324 lines — always loaded)
│   │   ├── 02-cli-tools.md      (397 lines — always loaded)
│   │   ├── 03-ml-engineering.md (292 lines — on demand)
│   │   ├── 04-security.md       (147 lines — on demand)
│   │   ├── 05-ui-ux.md          (260 lines — on demand)
│   │   ├── 06-web-dev.md        (305 lines — on demand)
│   │   ├── 07-job-hunt.md       (145 lines — on demand)
│   │   ├── 08-architecture.md   (198 lines — on demand)
│   │   └── 09-misc.md          (210 lines — on demand)
│   ├── memory-bank/             ← session logs, progress, decisions
│   ├── vector_db/               ← ChromaDB with all modules seeded
│   └── LESSONS_LEARNED.md       ← cross-project error patterns
├── tools/                       ← dashboard, seed scripts
├── config/                      ← opencode, Makefiles, README
└── dotfiles/                    ← bash, git, starship, tmux configs
```
