# Memory Architecture

## System Design

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Tools                           │
│  Claude Code  ·  OpenCode  ·  Cursor  ·  Windsurf  ·   │
│  Copilot  ·  Cline  (6 agents, 6 symlinks → 1 source)   │
└────────────────────────┬────────────────────────────────┘
                         │ symlink
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   GEMINI.md (Router)                      │
│  Routes by task type → lazy mode (~200 tok) or full mode  │
│  (~1,420 tok). Threshold: search recall > confidence.    │
└──────┬──────────────────────────────────────┬───────────┘
       │ lazy load                            │ vector search
       ▼                                      ▼
┌─────────────────┐            ┌──────────────────────────┐
│ 12 × Module .md │ ──seed──→ │     ChromaDB (vector)     │
│ (2,045 lines)   │  (make)   │    94.2% recall · 0.8s    │
└─────────────────┘            └──────────────────────────┘
```

## Key Design Decisions

1. **Symlinks over copies**: 6 config files point to one GEMINI.md — no drift
2. **Lazy-first**: Vector search before module load. 200 tokens vs 3,622
3. **Self-seeding**: Post-merge git hook re-seeds ChromaDB when modules change
4. **Self-healing**: Error → Diagnose → Fix → Re-run → Verify loop
5. **CLI routing**: 54 legacy→modern dispatchers (grep→rg, cat→bat, etc.)

## Data Flow

1. Agent task arrives at GEMINI.md via symlink
2. GEMINI.md parses intent → queries ChromaDB (~200 tokens)
3. If ChromaDB returns relevant chunk: use it (lazy mode)
4. If not: load full module(s) (full mode, ~1,420 tokens)
5. Agent executes with context → result returned
6. On error: Module 11 (Error Logs) + self-healing protocol

For the visual diagram, see [docs/images/architecture.png](docs/images/architecture.png).
