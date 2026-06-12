# Architecture

## Overview

MEMORY is a modular, cross-agent knowledge system. A single `GEMINI.md` file routes to 12 on-demand modules via symlinks from 6 AI agents, with a ChromaDB vector store for fast retrieval.

```mermaid
flowchart TB
    subgraph AGENTS["Agent Tools"]
        direction LR
        C1["Claude Code"]
        C2["OpenCode"]
        C3["Cursor"]
        C4["Windsurf"]
        C5["Copilot"]
    end
    G["GEMINI.md"]
    subgraph MOD["12 Memory Modules"]
        M1["01 Core<br/>115 lines"]
        M2["02 CLI<br/>160 lines"]
        M3["03 ML<br/>292 lines"]
        M4["04 Security<br/>147 lines"]
        M5["05 UI/UX<br/>274 lines"]
        M6["06 Web<br/>305 lines"]
        M7["07 Job Hunt<br/>145 lines"]
        M8["08 Arch<br/>198 lines"]
        M9["09 Misc<br/>255 lines"]
        M10["10 Lessons<br/>17 lines"]
        M11["11 Errors<br/>30 lines"]
        M12["12 Repos<br/>107 lines"]
    end
    V["ChromaDB<br/>Vector Store"]
    C1 & C2 & C3 & C4 & C5 -->|symlink| G
    G -->|lazy load| M1
    M1 --> M2 --> M3 --> M4 --> M5 --> M6 --> M7 --> M8 --> M9 --> M10 --> M11 --> M12
    M1 & M2 & M3 & M4 & M5 & M6 & M7 & M8 & M9 & M10 & M11 & M12 -.->|seed| V
    V -.->|search| G
```

## Core Design Decisions

### 1. Symlink-Based Instruction Injection
**Why:** Six different agent tools (Claude Code, OpenCode, Cursor, Windsurf, Copilot, Cline) each read different filenames for instructions. Symlinks make them all point to the same `GEMINI.md` without duplication.

### 2. Modular On-Demand Loading
**Why:** A single 3,622-line monolithic file consumed 100% of context in minutes. Breaking into 12 modules + lazy loading saves 60-95% of tokens per session.

### 3. Vector DB as Primary Search
**Why:** Loading a 300-line module costs ~1,500 tokens. Searching ChromaDB returns the relevant chunk (~200 tokens) in milliseconds. Modules load only when the search misses.

## Key Components

| Component | Tech | Role |
|-----------|------|------|
| **GEMINI.md** | Markdown | Router/Index — auto-switches lazy↔full mode |
| **12 Modules** | Markdown | Domain-specific instructions loaded on demand |
| **ChromaDB** | Vector DB | Semantic search across all module content |
| **freellmapi** | Node.js | 0-cost LLM proxy (16 providers, 1.7B tokens/mo) |
| **FCC** | Python | Free Claude Code routing to 17 providers |
| **Guardrails** | Shell scripts | 8 CLI wrappers (grep→rg, cat→bat, etc.) |
| **Session Hook** | Shell script | `session-start.sh` — auto-runs every session |

## Data Flow

```
User Request
    │
    ▼
GEMINI.md (routed via symlink from agent tool)
    │
    ├── Lazy path ──► ChromaDB search ──► return chunk (~200 tokens)
    │
    └── Full path ──► Load 01-core-rules.md + 02-cli-tools.md
                      └──► Load task-specific module
                           └──► Execute
                                └──► Verify (semgrep + gitleaks +
                                       pre-commit + symlink check)
```

## Port Map

| Port | Service | Type |
|------|---------|------|
| 3001 | freellmapi API | PM2 permanent |
| 5173 | freellmapi dashboard | On-demand dev |
| 8082 | ChromaDB / FCC admin | Optional |
| 8083 | Dashboard (alt) | Optional |
