# MEMORY Repository Walkthrough

## Architecture
```
GEMINI.md (158 lines) ─── Lightweight index/router
  ├── .clinerules              ─┐
  ├── .cursorrules             ─┤
  ├── .windsurfrules           ─┤  All symlinks to
  ├── AGENTS.md                ─┤  GEMINI.md
  ├── CLAUDE.md                ─┤
  └── .github/copilot-instructions.md

memory/modules/ ─────────── 19 domain-specific modules
  ├── 01-core-rules.md (180 lines)    — Session protocol
  ├── 02-cli-tools.md (170 lines)     — 54-tool dispatch
  ├── 03-ml-engineering.md (516 lines) — Full MLOps
  ├── 04-security.md (147 lines)      — Auth patterns
  ├── 05-ui-ux.md (321 lines)         — Design system
  ├── 06-web-dev.md (293 lines)       — Web projects
  ├── 07-job-hunt.md (145 lines)      — ATS + LinkedIn
  ├── 08-architecture.md (198 lines)  — Enterprise patterns
  ├── 09-misc.md (255 lines)          — Roadmaps, tricks
  ├── 10-lessons-learned.md (22 lines) — Directives
  ├── 11-error-logs.md (30 lines)     — Error history
  ├── 12-repo-teachings.md (67 lines) — Pattern catalog
  ├── 13-devops-cicd.md (120 lines)   — CI/CD, Docker, PM2
  ├── 14-lessons-learned.md (305 lines) — 15 error lessons
  ├── 15-3d-web-design.md (85 lines)  — R3F, GSAP, Three.js
  ├── 16-agent-evals.md (198 lines)   — Eval methodology
  ├── 17-mongodb-vector.md (80 lines) — MongoDB Atlas
  ├── 18-datadog-monitoring.md (65 lines) — Monitoring
  ├── 19-clerk-auth.md (95 lines)     — Auth integration
  └── 20-stripe-payments.md (95 lines) — Payments

memory/vector_db/ ───────── ChromaDB (246 chunks)
tools/ ──────────────────── 12 scripts
.devcontainer/ ──────────── GitHub Codespaces config
```

## Key Features
1. **Lazy/Full Mode** — Vector DB search-first (~200 tokens) vs full module load (~2000 tokens)
2. **27 CLI Tools** — Modern replacements (rg, bat, eza, fd, dust, btop, etc.)
3. **8 Guardrails** — Shadow wrappers intercept legacy commands
4. **Session Handoff** — .agent-progress.md bridges sessions seamlessly
5. **Vector Search** — `memory-search "topic"` finds answers in <1 second
6. **GitHub Student Pack** — $200 DigitalOcean, $50 MongoDB, free auth/payments/monitoring

## Token Economics
| Mode | Lines | Tokens | Savings |
|------|-------|--------|---------|
| Old monolith | 3,622 | ~5,000 | baseline |
| Full mode | ~1,420 | ~2,000 | 60% |
| Lazy mode | ~200 | ~300 | 95% |
