# CodeBurn Repository Analysis & Memory

CodeBurn (`getagentseal/codeburn`) is an open-source terminal UI (TUI) dashboard and macOS menu bar application for local cost and token usage observability across major AI coding assistants. 

---

## 💡 Product Context & Architecture

CodeBurn runs **entirely locally**, requiring no proxy wrapper, no middleman servers, and no external API keys. It achieves this by reading session databases and log files directly off the local disk and calculates costs using a local LiteLLM pricing database.

```
                  ┌──────────────────────────────────────────────┐
                  │                 user machine                 │
                  │                                              │
                  │  ┌──────────────┐          ┌──────────────┐  │
                  │  │ AI Assistant │          │ AI Assistant │  │
                  │  │ (e.g. Cursor)│          │  (e.g. CLI)  │  │
                  │  └──────┬───────┘          └──────┬───────┘  │
                  │         │ write                   │ write    │
                  │         ▼ logs/db                 ▼ logs/db  │
                  │  ┌──────────────┐          ┌──────────────┐  │
                  │  │ SQLite/JSON  │          │  Protobuf/   │  │
                  │  │   on disk    │          │  JSON files  │  │
                  │  └──────┬───────┘          └──────┬───────┘  │
                  │         │                         │          │
                  │         │   ┌─────────────────┐   │          │
                  │         └──►│    CodeBurn     │◄──┘          │
                  │             │   Dashboard     │              │
                  │             └────────┬────────┘              │
                  │                      │ pulls                 │
                  │                      ▼                       │
                  │             ┌─────────────────┐              │
                  │             │ LiteLLM Pricing │              │
                  │             │ (Local Cache)   │              │
                  │             └─────────────────┘              │
                  └──────────────────────────────────────────────┘
```

### Supported AI Coding Assistants (25+)
*   **Claude Code** (`~/.claude/projects/`)
*   **Cursor IDE** (`state.vscdb` SQLite database)
*   **Google Antigravity / agy** (local language server RPC HTTPS protocol + status line hook)
*   **Gemini CLI** (`~/.gemini/tmp/`)
*   **Mistral Vibe** (`~/.vibe/logs/session/`)
*   **GitHub Copilot** (`~/.copilot/` + VS Code chat transcripts)
*   **Codex** (`~/.codex/sessions/`)
*   **Cline / Roo Code / KiloCode** (`ui_messages.json` inside task directories)
*   **IBM Bob** (`ibm.bob-code/tasks`)
*   **OpenCode** (`opencode*.db` SQLite database)
*   **Codebuff** (`chat-messages.json`)
*   **Warp** (`warp.sqlite`)
*   **Forge** (`.forge.db` SQLite database)
*   **Pi / OMP** (`~/.pi/` or `~/.omp/` session JSONL)
*   **Kimi Code** (`~/.kimi/sessions/`)

---

## 🛠️ CLI Interface & Commands

CodeBurn can be installed globally via `npm` or `brew` or run directly with `npx codeburn`.

```bash
codeburn                             # Runs interactive TUI dashboard (default: 7 days)
codeburn today                       # Today's cost & token usage
codeburn month                       # Current calendar month usage
codeburn status                      # Compact one-liner dashboard output (today + month)
codeburn report                      # Full token/cost report with custom options
  --from 2026-04-01 --to 2026-04-10  # Filter by date range
  --project myapp                    # Case-insensitive project substring filter
  --provider claude                  # Filter to specific AI provider
  --format json                      # Outputs JSON data structure
codeburn optimize                    # Scans session logs for token waste & prints shell fixes
codeburn compare                     # Compares model metrics (accuracy, cost, speed, one-shot)
codeburn yield                       # Correlates AI sessions with git commits (tracks productive spend)
codeburn plan set claude-max         # Configures subscription spend plans ($200/mo Claude Max, etc.)
codeburn currency GBP                # Configures custom currencies (ISO 4217 support via Frankfurter API)
codeburn model-alias "proxy-name" "real-name"  # Maps unknown proxy models to LiteLLM equivalents
```

---

## 🪐 Antigravity CLI Integration

Antigravity uses a custom provider implementation in `src/providers/antigravity.ts` that differs from traditional providers because **it relies on a live process** rather than solely parsing log files off the disk.

### 1. Process Discovery & RPC
1.  **Discovery**: Scans command lines via `ps` (POSIX) or `Get-CimInstance Win32_Process` (Windows) to identify the running Antigravity language server.
2.  **Authentication**: Extracts the server port (e.g. `--https_server_port`, `--extension_server_port`) and CSRF security token (e.g. `--csrf_token`, `--extension_server_csrf_token`) from the process arguments.
3.  **RPC Request**: Makes a Connect-protocol HTTPS request to the server's endpoint `/exa.language_server_pb.LanguageServerService/GetCascadeTrajectoryGeneratorMetadata` to fetch live conversation metadata.
4.  **Pricing Mapping**: Strips execution suffixes (`-high`, `-medium`, `-low`, `-agent`) to map models (e.g. `gemini-3.5-flash-high`) into canonical LiteLLM counterparts (e.g. `gemini-3.5-flash`).

### 2. Status Line Hook (`codeburn antigravity-hook install`)
For short-lived CLI sessions (`agy`) that terminate before the dashboard's 30-second refresh catches the process:
*   Appends JSON payloads to `~/.cache/codeburn/antigravity-statusline.jsonl`.
*   Deduplicates monotonic status line events using deltas to avoid double-counting input/output tokens.
*   Resolves ephemeral POSIX ports using `lsof -a -i -P -n -p <pid>` to match active background listeners.

### 3. Caching & Eviction
*   Data is cached in `~/.cache/codeburn/antigravity-results.json`.
*   If the language server is offline, the cache is read as the primary fallback.
*   Performs cache eviction against live cascade folders (`~/.gemini/antigravity/conversations/`) so deleted sessions are automatically cleaned up from CodeBurn.

---

## ⚡ Technical Implementations of Note

### Cost Tracking & Cache Optimization
Pricing uses a local daily-cached copy of LiteLLM (`~/.cache/codeburn/litellm-pricing.json`) with an hardcoded snapshot backup (`litellm-snapshot.json`) to prevent fuzzy name mismatches.
*   **Token types handled**: Input, output, reasoning/thoughts (billed at output rate), cache creation, cache read, and web search requests ($0.01/request).
*   **Defense in Depth**: Clamps token prices at $0-$1/token to prevent malicious/corrupt pricing files from inflating costs or generating negative values.
*   **Local Models**: Suppresses warnings for local inference models (e.g., matching GGUF signatures or `ollama` tags like `:tag`) since they are effectively free.

### "One-Shot Rate" Metric
For editing operations, CodeBurn measures file-aware retry loops:
*   A **retry** is flagged when a file is edited, a bash command runs, and the same file is immediately re-edited.
*   The **one-shot rate** is the % of edit cycles completed successfully without requiring a retry.
