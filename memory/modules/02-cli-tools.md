# CLI Tools, Token Optimization & Terminal Stack

> Extracted from `GEMINI.md`. See `memory/modules/01-core-rules.md` for core agent rules, `memory/modules/04-security.md` for security scanning tools.

---

## 🪙 Token Optimization — Read This First

### At the START of every session on an existing project:
1. Read `memory-bank/progress.md` FIRST — tells you exactly where things left off
2. Read `memory-bank/architecture.md` — gives the full codebase map without exploring files
3. Read `memory-bank/decisions.md` — tells you WHY things are built a certain way
4. Only then explore individual files if something specific is needed

### Never read these (covered by .agentignore):
- `node_modules/`, `dist/`, `build/`, `.next/`, `out/` — build outputs, never useful
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` — too long, zero value
- `*.min.js`, `*.map`, `*.d.ts` — generated files
- `coverage/`, `.pytest_cache/`, `*.log` — test/log artifacts

### Never re-read files already in context:
- If a file was already read this session → use the content already in context
- Never call view_file or read_file on the same path twice in one session

### CLI-first (saves tokens vs reading whole files):
- **Maximize Command-Line Output**: Always prefer shell/CLI tools over reading whole files.
- Finding something? → `grep -r "keyword" --include="*.ts" .` not read every file
- Checking git state? → `git status` + `git diff` not read source files
- Debugging? → `tail -50 logs/app.log` not open the whole log
- Checking port? → `lsof -i :3000` not read server config
- Running quality checks? → `make ci` (1 tool call) not lint+typecheck+test separately
- Observability? → Run `codeburn status` or `codeburn optimize` to check context growth.
- **OpenCode CLI Delegation**: Delegate heavy tasks via `opencode run "<message>"`.

### Advanced Token-Saving Enforcement (EXTREME OPTIMIZATION)
- **AST-Based Code Extraction**: ALWAYS prefer `ast-grep` or `jq` over `grep` for code extraction.
- **Automated Memory Bank Archiving**: Keep `memory-bank/progress.md` clean. Move progress logs older than 14 days into archive.
- **Strict `git diff` Limits**: NEVER run raw `git diff` without capping output. Use `git diff --stat` first.
- **Paging Enforcement**: Use `bat --line-range <start>:<end>` or `sed -n '<start>,<end>p'`.
- **Context-Isolated Subagents**: Delegate heavy log-reading or codebase searches to a `research` subagent.

### Use templates — don't write from scratch:
- GitHub Actions CI → copy from `/home/aditya/bin/templates/github-actions/`
- Makefile → copy from `/home/aditya/bin/templates/Makefile`
- Docker Compose → copy from `/home/aditya/bin/templates/docker-compose.yml`

### Use parallel subagents for independent tasks:
- Frontend + Backend can be built simultaneously using subagents
- Research + Coding can happen in parallel
- Never do sequentially what can be done in parallel

### One conversation = one task:
- Each project = its own fresh conversation
- Each bug fix = its own fresh conversation
- Never mix unrelated tasks in one conversation

### GitHub Actions runs tests for free (2000 min/month):
- Agent writes the CI workflow ONCE during project setup
- All subsequent test runs happen in GitHub's cloud — zero local credits

---

## ⚡ ZERO-TOKEN CLI OPERATION RULEBOOK (MANDATORY — READ BEFORE EVERY ACTION)

This section defines the EXACT CLI tool to use for every operation. Using the wrong tool wastes tokens. This is non-negotiable.

### Enforcement Layer
There is a guardrail PATH wrapper at `~/bin/guardrails/` that shadows 8 slow tools (grep, cat, ls, find, du, top, ps, sed). If you try to use any of them, a warning fires telling you the modern replacement. **The warning is a signal — switch tools immediately.**

### 🔍 SEARCHING (Never use `grep` in bash — use `rg`)
```bash
rg "pattern" .                          # replaces: grep -r "pattern" .
rg "pattern" --type ts .               # search only TypeScript files
rg "pattern" -l .                      # list only filenames
rg "TODO|FIXME" .                      # multi-pattern search
fd "*.env" .                           # replaces: find . -name "*.env"
fd "component" --type f .              # files only
```

### 📁 LISTING FILES (Never use `ls` — use `eza`)
```bash
eza -la --git                          # replaces: ls -la
eza --tree --level 2                   # directory tree
eza --tree --level 3 --git-ignore      # tree ignoring .gitignore
```

### 📄 READING FILES (Never use `cat` — use `bat`)
```bash
bat src/index.ts                       # with syntax highlighting
bat --line-range 10:50 file.ts         # specific range
```

### 🔄 GIT OPERATIONS (Use `lazygit` TUI or `git` + `delta`)
```bash
lazygit                                # full TUI
git diff | delta                       # beautiful diff
git log --oneline -20                  # compact history
gh pr list                             # list PRs
gh issue list                          # list issues
```

### 📊 PROJECT ANALYSIS (Use these FIRST before reading any files)
```bash
onefetch                               # instant repo summary
tokei                                  # count lines of code
dust -n 10                             # top 10 largest directories
duf                                    # disk usage summary
```

### 🌐 HTTP / API TESTING (Never use curl manually — use `http`)
```bash
http GET https://api.example.com/users
http POST api.example.com/login email=a pass=b
```

### 📦 JSON / YAML PROCESSING (Never read raw files — use `jq`/`yq`)
```bash
jq '.dependencies' package.json
yq '.services' docker-compose.yml
```

### 🔁 TEXT REPLACEMENT (Use `sd` not `sed`)
```bash
sd 'old_text' 'new_text' file.ts
sd 'localhost:3000' 'localhost:8000' **/*.ts
```

### 📝 READING MARKDOWN DOCS (Use `glow` not `cat` or `view_file`)
```bash
glow README.md
glow memory-bank/progress.md
```

### 🖥️ PROCESS MONITORING (Use `btop` not `top`/`ps`)
```bash
btop                                   # full TUI system monitor
procs                                  # replaces: ps aux
```

### 📡 NETWORK (Use `nmap` for discovery, `http` for requests)
```bash
nmap -sn 192.168.1.0/24
nmap -p 3000,8080,5432 localhost
```

### 🪟 SESSION MANAGEMENT (Always use `tmux` for long tasks)
```bash
tmux new-session -d -s <name>
tmux send-keys -t <name> "<cmd>" Enter
tmux list-sessions
tmux attach -t <name>
```

### ⚡ PACKAGE MANAGEMENT (Use `bun` not `npm`)
```bash
bun install
bun run dev
bun add <package>
bun x <tool>
```

### 🧠 AGENT TOKEN-SAVING PRIORITY ORDER
When starting work on any codebase, follow this EXACT sequence:
1. `onefetch` — get repo summary (0 file reads)
2. `glow memory-bank/progress.md` — get current status (1 tool call)
3. `eza --tree --level 2 --git-ignore` — understand structure (0 file reads)
4. `tokei` — know what languages/how much code (0 file reads)
5. `rg "TODO\|FIXME\|HACK" .` — find known issues (0 file reads)
6. Only THEN open specific files with `bat` if needed

### 🎯 COMPLETE TOOL DISPATCH TABLE — 54 Tools, Zero Thinking Required

Every installed CLI tool has an exact trigger condition. When the condition is met, the agent MUST fire the tool without deliberating.

| # | Condition | Tool | Why |
|---|-----------|------|-----|
| 1 | Starting work on any project | `onefetch` | Instant repo summary |
| 2 | Starting work on any project | `eza --tree --level 2 --git-ignore` | Directory structure |
| 3 | Starting work on any project | `tokei` | Language breakdown |
| 4 | Starting work on any project | `fastfetch` | CPU/RAM/GPU/OS snapshot |
| 5 | Need to understand a new repo | `enola generate_snapshot` | Full arch snapshot |
| 6 | Need codebase dependency graph | `enola explore` | Symbols, imports, call chains |
| 7 | Need blast radius / impact analysis | `enola impact_analysis <target>` | Shows what breaks if X changes |
| 8 | Need architecture diagram | `d2` | Text → PNG/SVG |
| 9 | Need AI pair programming (multi-file) | `aider --model ollama/qwen2.5-coder:3b` | Git-first pair coder |
| 10 | Need token/cost observability | `codeburn optimize` | Finds waste |
| 11 | Need token/cost status | `codeburn status` | Today + month spend |
| 12 | Need git commit message | `comet` | AI-generated via Ollama |
| 13 | Need git diff | `git diff \| delta` | Syntax-highlighted diffs |
| 14 | Need git TUI | `lazygit` | Full git TUI |
| 15 | Need git history | `git log --oneline -20` | Compact history |
| 16 | Need GitHub operations | `gh` | PRs, issues, repos, releases |
| 17 | Searching text in files | `rg` (NOT grep) | 3-5x faster |
| 18 | Reading any file | `bat` (NOT cat) | Syntax highlighting |
| 19 | Listing directory | `eza` (NOT ls) | Icons, git status |
| 20 | Finding files by name | `fd` (NOT find) | 10x faster |
| 21 | Disk usage analysis | `dust` (NOT du) | Visual tree |
| 22 | Disk usage summary | `duf` (NOT df) | Mount points |
| 23 | Process monitoring | `procs` (NOT ps) | Colorized, tree view |
| 24 | System resource overview | `btm` or `btop` (NOT top) | GPU/CPU/RAM/network |
| 25 | Text replacement across files | `sd` (NOT sed for bulk) | Clearer syntax |
| 26 | JSON processing | `jq` | Query/modify JSON |
| 27 | Large JSON interactive browse | `jless` | Don't open in editor |
| 28 | Building jq queries interactively | `jnv` | Live jq query builder |
| 29 | JSON interactive processing | `fx` | Better than raw jq |
| 30 | YAML processing | `yq` | Query/modify YAML |
| 31 | Markdown reading | `glow` (NOT cat/bat for .md) | Rendered markdown |
| 32 | API calls | `http` (NOT curl) | Cleaner syntax |
| 33 | Shell history search | `atuin` | Database-backed |
| 34 | Directory navigation | `zoxide` | Smart cd |
| 35 | Fuzzy finding | `fzf` | Universal fuzzy finder |
| 36 | Quick CLI help | `tldr` (not man) | Practical examples |
| 37 | Postgres queries | `pgcli` (not psql) | Auto-complete |
| 38 | Container management | `docker` | Start/stop/exec |
| 39 | Environment variables | `direnv` | Per-directory env |
| 40 | Secret scanning (git) | `gitleaks` | Scan git history |
| 41 | Secret scanning (files) | `trufflehog` | Scan files/S3 |
| 42 | Vulnerability scanning | `trivy` | Scan containers, fs, repos |
| 43 | Static analysis / code health | `semgrep` | Find bugs, enforce patterns |
| 44 | Command benchmarking | `hyperfine` | Precision timing |
| 45 | Network scanning | `nmap` | Port scanning |
| 46 | Python deps | `uv` (NOT pip) | 10-100x faster |
| 47 | Node deps | `bun` (NOT npm) | 10x faster |
| 48 | Python tool installs | `pipx` (NOT pip --global) | Isolated installs |
| 49 | Process management (daemons) | `pm2` | Keep servers alive |
| 50 | Session management (long tasks) | `tmux` | Survives terminal close |
| 51 | CLI via OpenAPI spec | `onlycli <spec>` | 35x cheaper than MCP |
| 52 | Output compression for LLM | `rtk` | Compress 60-90% |
| 53 | Output stripping for LLM | `lowfat` | Strip verbose CLI |
| 54 | Agent skills management | `tessl` | Install/remove skills |

**Failure conditions** (rule violations, not suggestions):
- Using `grep` = FAILED. Use `rg`.
- Using `cat` on any file = FAILED. Use `bat` or `glow`.
- Using `ls` = FAILED. Use `eza`.
- Using `find` = FAILED. Use `fd`.
- Using `du` = FAILED. Use `dust`.
- Using `ps` = FAILED. Use `procs`.
- Using `top` = FAILED. Use `btop` or `btm`.
- Using `curl` for API calls = FAILED. Use `http`.
- Starting a session without `onefetch` + `eza --tree` = FAILED.
- Using `sed` for batch rename/replace = FAILED. Use `sd`.
- Reading a JSON file without `jless`/`jq`/`jnv`/`fx` = FAILED.
- Using `npm` or `pip` = FAILED. Use `bun` or `uv`.
- Leaving a long process without `tmux` = FAILED.

---

## Global Error Learnings & Guardrails (Permanent Memory)

1. **Staging Bloat Prevention:** Never stage virtual environments, package lockfiles, or build packages to Git.
2. **Port Mismatch Checks:** Cross-reference frontend config files with backend startup parameters.
3. **OCR Metadata Noise Removal:** Strip properties/particulars sections before regex matching.
4. **Devanagari Numeral Conversion:** Translate Devanagari numerals to standard digits.
5. **OCR Pipeline Quality Early-Exit:** Implement quality-threshold early-exit.
6. **UI Click Event Handling:** Explicitly invoke input clicks with `e.stopPropagation()`.

---

## 🖥️ Terminal Environment Standards

### Starship Prompt (Mandatory)
```bash
curl -sS https://starship.rs/install.sh | sh
eval "$(starship init bash)"
```
Config lives at `~/.config/starship.toml`.

### tmux Session Management (Mandatory for Long-Running Tasks)
```bash
tmux new-session -d -s <project-name>
tmux send-keys -t <project-name> "bun run dev" Enter
tmux attach -t <project-name>
```
Session naming: `<project>-dev`, `<project>-api`, `<project>-train`.

---

## 🛠️ Installed Agent Tools — Always Available

### Binaries (globally available)
| Tool | Purpose |
|------|---------|
| rtk | Compress shell outputs 60-90% |
| lowfat | Strip verbose CLI output for LLMs |
| onlycli | OpenAPI spec → CLI binary |
| comet | AI git commit messages via Ollama |
| graphify | Codebase knowledge graph MCP |
| tessl | Agent skills package manager |
| enola | Architecture analysis |
| aider | Git-first AI pair programmer |
| uv | Python package manager |
| codeburn | AI agent cost/token observability |
| fx | Interactive JSON viewer |

### MCP Servers
| Server | Command | Purpose |
|--------|---------|---------|
| chromadb | chromadb (in venv) | Disk-based vector search (SQLite, 0 RAM overhead) |

### Vector Database (ChromaDB)
- Path: `memory/vector_db/chroma.sqlite3` — disk-based, no daemon needed
- Dashboard: `http://localhost:8082` — search across all modules
- API: `curl localhost:8082/api/search?q=<query>`

### Claude Code Skills (~/.claude/skills/)
| Slash Command | Token Savings |
|--------------|--------------|
| /diff-only | 60-80% output tokens |
| /smart-read | 40-90% input tokens |
| /trim | 55-70% input tokens |
| /checkpoint | 8k-40k → ~500 tokens |

### Cloned Repos (~/tools/agent-tools/)
agent-tact, agentguard, ai-plugin-gatekeeper, claude-deepseek-bridge, claude-smart-model-router, clawpiggy, lean-code, mcp-graphify-autotrigger, openclaw-litecache, pomelo-context, skill-model-router, smart-library-app, trache

### Claude→DeepSeek Bridge
```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=sk-YOUR_DEEPSEEK_KEY
export ANTHROPIC_MODEL=deepseek-v4-pro
claude
```

---

## 🛠️ Specialized Tool Matrix

### 1. Fastfetch
- **When:** Dropped into new server/container — fast hardware snapshot.
- **Command:** `fastfetch --logo none`

### 2. Terrastruct D2 (`d2`)
- **When:** Generating System Architectures, ERDs, Sequence Diagrams, Data Flows.
- **Why:** Text → high-quality SVGs/PNGs, version-controllable.

### 3. Enola (`enola`)
- **When:** Architecture analysis, dependency impact analysis, codebase graph exploration.
- **Command:** `enola explore <module>` or `enola impact_analysis <target>`

### 4. Graphify (`graphify`)
- **When:** Building/updating codebase knowledge graph for persistent cross-session context.
- **Command:** `graphify serve <output-path>/graph.json`

### 5. GitHub Starter Workflows
- **When:** Initializing CI/CD for new repos.
- **Why:** Official templates for deployment, testing, security scanning.

### 6. Trivy
- **When:** Static analysis security check on containers, filesystems, git repos.
- **Why:** CVEs, IaC misconfigurations, SBOM, secrets.

### 7. Aider
- **When:** Pair-programming, multi-file refactoring, automated code gen with git.
- **Command:** `aider --model <model>`

### 8. Uv
- **When:** ALL Python package management. Replaces pip + pipenv + poetry.
- **Command:** `uv add <package>`, `uv run <script>`, `uv sync`

### 9. Codeburn
- **When:** AI agent cost/token observability, context optimization.
- **Command:** `codeburn status`, `codeburn optimize`

### 10. TruffleHog
- **When:** Before committing/pushing code, auditing repo security.
- **Why:** Verifies leaked credentials by testing against provider.

### 11. Dynamic Tool Prioritization Strategy
- Prioritize tools based on performance, speed, and exact fit.
- Prefer native specialized tools over generic alternatives.
- Always select the tool that returns exact data with smallest text footprint.

### 12. Elite GitHub Marketplace Stack
- **CodeQL** (`github/codeql-action`): Security/vulnerability scanning on every PR.
- **Super-Linter** (`github/super-linter`): Code formatting enforcement.
- **Dependabot**: Zero-touch dependency updates and CVE patching.
- **Codecov** (`codecov/codecov-action`): Visual test coverage reporting.

### 13. Elite Developer Terminal Stack
- **Terminal & Shell:** `wezterm`, `starship`, `atuin`, `zoxide`, `fzf`
- **File Management:** `eza`, `bat`, `fd`, `dust`
- **Search & Text:** `rg` / `ripgrep`
- **System Monitoring:** `btop`
- **Git & Workflow:** `delta`
- **Benchmarking:** `hyperfine`
- **Documentation:** `glow`

### 14. Transparent Execution Protocol (Auto-Display)
For background execution > a few seconds, run inside `tmux` and pop open terminal:
```bash
export DISPLAY=:0
wezterm start -- bash -c "tmux attach -t agent-tasks"
```

### 15. CodeBurn — Token & Cost Observability

| Action | Command | Purpose |
|--------|---------|---------|
| Status | `codeburn status` | Today's token/cost usage |
| Optimize | `codeburn optimize` | Find context waste, suggest fixes |
| Aliases | `codeburn alias` | List available commands |
| Logging | `codeburn log --type system "message"` | Manually log cost events |

Session costs auto-log to `memory/memory-bank/progress.md` on shell exit.

### 16. Global Error Logging & Self-Correction Protocol
- Log all error signatures and resolution patterns to `memory/LESSONS_LEARNED.md`.
- Cross-reference `memory/LESSONS_LEARNED.md` before writing code or fixing bugs.
