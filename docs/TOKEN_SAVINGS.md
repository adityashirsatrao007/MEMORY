# Token Savings Analysis

## How MEMORY Saves 60-95% of Your Context Budget

Every AI coding session has a limited context window. A monolithic instruction file burns through it immediately. MEMORY's modular lazy-loading changes this entirely.

## Lines per Session

| Mode | Lines Loaded | Tokens (approx) | vs Monolith |
|------|-------------|-----------------|-------------|
| **Old Monolithic** | 3,622 | ~18,000 | Baseline |
| **Full Mode** (core + CLI + task) | 1,420 | ~7,100 | **−60%** |
| **Lazy Mode** (vector search) | 200 | ~1,000 | **−95%** |

![Token Savings](docs/images/token-savings.png)

## Cost Impact

| Service | Per Call | Per Session | Annual (1000 sessions) |
|---------|----------|-------------|----------------------|
| Claude Sonnet (direct) | $0.003 | ~$6.00 | $6,000 |
| Gemini Flash (direct) | $0.00015 | ~$0.30 | $300 |
| Local Ollama | $0.00001 | ~$0.02 | $20 |
| freellmapi + MEMORY Lazy | **$0** | **$0** | **$0** |
| freellmapi + MEMORY Full | **$0** | **$0** | **$0** |

![Cost Comparison](docs/images/cost-comparison.png)

## The Math

**Without MEMORY:**
- 3,622 lines × 5 tokens/line = ~18,100 tokens just for instructions
- Claude Sonnet 200K context: **9% consumed before any work**
- After 3-4 exchanges: context full, agent forgets, hallucinations begin

**With MEMORY Lazy:**
- 200-line vector search result = ~1,000 tokens
- Claude Sonnet 200K context: **0.5% consumed**
- ~190K tokens available for actual work

**With MEMORY Full:**
- 1,420 lines = ~7,100 tokens
- Claude Sonnet 200K context: **3.5% consumed**
- ~193K tokens available

## Token Breakdown by Module

| Module | Lines | Tokens | % of Total |
|--------|-------|--------|------------|
| 01 Core Rules | 115 | 575 | 3.2% |
| 02 CLI Tools | 160 | 800 | 4.4% |
| 03 ML Engineering | 292 | 1,460 | 8.1% |
| 04 Security | 147 | 735 | 4.1% |
| 05 UI/UX | 274 | 1,370 | 7.6% |
| 06 Web Dev | 305 | 1,525 | 8.4% |
| 07 Job Hunt | 145 | 725 | 4.0% |
| 08 Architecture | 198 | 990 | 5.5% |
| 09 Misc | 255 | 1,275 | 7.0% |
| 10 Lessons | 17 | 85 | 0.5% |
| 11 Errors | 30 | 150 | 0.8% |
| 12 Repo Teachings | 107 | 535 | 3.0% |

**Total:** 2,045 lines / ~10,225 tokens (full load)
**With lazy:** ~200 lines / ~1,000 tokens (95% reduction)

## Tips for Maximum Savings

1. **Always search before load** — `memory-search "<topic>"` hits ChromaDB first
2. **Use freellmapi proxy** — routes across 16 free providers, 1.7B tokens/month
3. **Silent CLI mode** — suppress output with `> /dev/null 2>&1 || echo "FAIL: ..."`
4. **Output compression** — pipe through `lowfat` or `rtk` for 60-90% compression
5. **Session hygiene** — start fresh after 15-20 messages; use `.agent-progress.md` for handoff
