# Token Savings Report

## Summary

MEMORY reduces per-session token consumption by **60–95%** compared to a monolithic agent config file.

## Measurements

| Mode | Lines Loaded | Tokens | Context % | Savings |
|------|-------------|--------|-----------|---------|
| Old Monolithic | 3,622 | ~18,000 | 9% | — |
| Full Mode | 1,420 | ~7,100 | 3.5% | −60% |
| Lazy Mode | ~200 | ~1,000 | 0.5% | −95% |

## Cost Impact (per session)

| Provider | Without MEMORY | With MEMORY (Lazy) |
|----------|---------------|-------------------|
| Claude Sonnet | ~$6.00 | ~$0.30 |
| Gemini Flash | ~$0.30 | ~$0.02 |
| Ollama (local) | ~$0.02 | ~$0.001 |
| freellmapi proxy | $0 | $0 |

## Module Breakdown

| Module | Tokens |
|--------|--------|
| 01 Core Rules | 575 |
| 02 CLI Tools | 800 |
| 03 ML Engineering | 1,460 |
| 04 Security | 735 |
| 05 UI/UX | 1,370 |
| 06 Web Dev | 1,525 |
| 07 Job Hunt | 725 |
| 08 Architecture | 990 |
| 09 Misc | 1,275 |
| 10 Lessons Learned | 85 |
| 11 Error Logs | 150 |
| 12 Repo Research | 535 |
| **Total** | **~10,225** |

## Annual Savings

At 20 sessions/day, 250 working days: **~$30,000/year** saved vs. Claude Sonnet without MEMORY.

See [token-savings.html](token-savings.html) for interactive charts.
