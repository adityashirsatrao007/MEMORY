# GEMINI — Agent Config Index
`MEMORY_ROOT=/home/aditya/Desktop/Projects/MEMORY`

## Mode Selection
`MEMORY_MODE=lazy` — **RECOMMENDED** (~70 tokens, vector search on demand)
`MEMORY_MODE=full` — preload core modules (~1420 tokens, faster first response)

Set with: `export MEMORY_MODE=lazy` in bashrc or per-session.

## LAZY Mode (search, don't load)
Search vector DB for context instead of loading module files:
```
memory-search "<task description>" [top_k=3]
```
Examples:
- `memory-search "token optimization rules"` → CLI rules, silent output, read cache
- `memory-search "safety and security protocol"` → security module
- `memory-search "ML engineering workflow"` → ML module, model selection tree
- `memory-search "web dev deployment"` → web/SEO module

The result tells you which module file has the answer. Open only that file with `bat --line-range :80 "$MEMORY_ROOT/memory/modules/XX-*.md"`. DO NOT load any module proactively.

## FULL Mode (preload at session start)
### Always Load
- `$MEMORY_ROOT/memory/modules/01-core-rules.md` — session protocol, Karpathy, prod standards, code review, zero assumption
- `$MEMORY_ROOT/memory/modules/02-cli-tools.md` — 54-tool dispatch table, guardrails, token optimization, failure conditions

### Load by Task
| Task | Module |
|------|--------|
| ML/MLOps | `03-ml-engineering.md` (292) |
| Security | `04-security.md` (147) |
| UI/UX | `05-ui-ux.md` (260) |
| Web/SEO | `06-web-dev.md` (305) |
| Job hunt | `07-job-hunt.md` (145) |
| Architecture | `08-architecture.md` (198) |
| Misc | `09-misc.md` (210) |

## Quick
`MEMORY_ROOT=$MEMORY_ROOT` | `memory-search` | Makefile: `make {validate,seed,stats}`
