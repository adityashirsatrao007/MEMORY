# Competition

## Competitive Landscape

| Product | Approach | Key Difference from MEMORY |
|---------|----------|--------------------------|
| Claude Code (default) | Monolithic CLAUDE.md | MEMORY's modular architecture uses 95% fewer tokens |
| Cursor AI | Per-project rules (.cursorrules) | MEMORY provides 12 pre-built, cross-agent modules |
| Windsurf | .windsurfrules | MEMORY works with 6 agents, not just one |
| GitHub Copilot | copilot-instructions.md | MEMORY includes vector search + CLI guardrails |
| Continue.dev | IDE plugin | MEMORY is agent-agnostic, works in any terminal |
| Supermemory | RAG-based memory | MEMORY is modular + lazy-loaded, not just a vector DB |
| Dify | Visual AI workflow builder | MEMORY is developer-focused, works with existing agents |

## Differentiation

1. **Cross-agent**: A single config (GEMINI.md) works for 6 different agents via symlinks
2. **Lazy loading**: 200 lines vs 3,622 lines — 95% fewer tokens
3. **Vector-first**: ChromaDB search before module load — 0.8s average recall
4. **54 CLI tools**: Legacy → modern auto-routing built in
5. **Free LLM proxy**: 16 providers at zero cost via freellmapi
6. **Self-healing**: Error protocol + audit checks built into the Makefile
