# Self-Hosting

MEMORY is designed to run entirely on your own infrastructure. No external services are required.

## Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 2 GB | 8 GB |
| Storage | 1 GB | 10 GB |
| OS | Ubuntu 22.04+ | Ubuntu 24.04 |
| Python | 3.10 | 3.12 |
| ChromaDB | 0.4.x | 0.5.x |

## Architecture

```
User Agents → GEMINI.md (symlinked) → memory/modules/*.md → ChromaDB
                                            ↓
                                    tools/install.sh
                                    Makefile (validate, seed, stats)
```

## Setup

```bash
git clone https://github.com/adityashirsatrao007/MEMORY.git
cd MEMORY
make all   # validate + seed
```

## Proxy Setup (Optional)

For zero-cost LLM access, run the freellmapi proxy:

```bash
git clone https://github.com/tashfeenahmed/freellmapi.git
cd freellmapi
pip install -r requirements.txt
python main.py --port 3001
```

Then configure your agent to route through `localhost:3001`.

## Monitoring

- **Dashboard**: `localhost:8083` — real-time module usage and token savings
- **ChromaDB**: `localhost:8000` — vector database admin
- **Logs**: `memory/modules/11-error-logs.md` — failure mode catalog

## Backup

```bash
# Backup modules (not ChromaDB — re-seed is fast)
tar czf memory-backup-$(date +%Y%m%d).tar.gz memory/modules/ tools/ Makefile
```
