# CLI Tools & Token Optimization

## 54-Tool Dispatch Table
| # | Condition | Tool |
|---|-----------|------|
| 1 | Starting any project | `onefetch` |
| 2 | Starting any project | `eza --tree --level 2 --git-ignore` |
| 3 | Starting any project | `tokei` |
| 4 | Starting any project | `fastfetch` |
| 5 | New repo understanding | `enola generate_snapshot` |
| 6 | Dependency graph | `enola explore` |
| 7 | Blast radius | `enola impact_analysis <target>` |
| 8 | Architecture diagram | `d2` |
| 9 | AI pair programming | `aider --model ollama/qwen2.5-coder:3b` |
| 10 | Token observability | `codeburn optimize` |
| 11 | Token cost status | `codeburn status` |
| 12 | Git commit message | `comet` |
| 13 | Git diff | `git diff | delta` or `git diff --stat` |
| 14 | Git TUI | `lazygit` |
| 15 | Git history | `git log --oneline -20` |
| 16 | GitHub operations | `gh` |
| 17 | Text search in files | `rg` (NOT grep) |
| 18 | Read any file | `bat` (NOT cat) |
| 19 | List directory | `eza` (NOT ls) |
| 20 | Find files by name | `fd` (NOT find) |
| 21 | Disk usage analysis | `dust` (NOT du) |
| 22 | Disk usage summary | `duf` (NOT df) |
| 23 | Process monitoring | `procs` (NOT ps) |
| 24 | System resource overview | `btm` or `btop` (NOT top) |
| 25 | Text replacement across files | `sd` (NOT sed for bulk) |
| 26 | JSON processing | `jq` |
| 27 | Large JSON interactive browse | `jless` |
| 28 | Building jq queries interactively | `jnv` |
| 29 | JSON processing | `fx` |
| 30 | YAML processing | `yq` |
| 31 | Markdown reading | `glow` (NOT cat/bat for .md) |
| 32 | API calls | `http` (NOT curl) |
| 33 | Shell history search | `atuin` |
| 34 | Directory navigation | `zoxide` |
| 35 | Fuzzy finding | `fzf` |
| 36 | Quick CLI help | `tldr` (not man) |
| 37 | Postgres queries | `pgcli` (not psql) |
| 38 | Container management | `docker` |
| 39 | Environment variables | `direnv` |
| 40 | Secret scanning (git) | `gitleaks` |
| 41 | Secret scanning (files) | `trufflehog` |
| 42 | Vulnerability scanning | `trivy` |
| 43 | Static analysis | `semgrep` |
| 44 | Command benchmarking | `hyperfine` |
| 45 | Network scanning | `nmap` |
| 46 | Python deps | `uv` (NOT pip) |
| 47 | Node deps | `bun` (NOT npm) |
| 48 | Python tool installs | `pipx` (NOT pip --global) |
| 49 | Process management (daemons) | `pm2` |
| 50 | Session management (long tasks) | `tmux` |
| 51 | CLI from OpenAPI spec | `onlycli <spec>` |
| 52 | Output compression for LLM | `rtk` |
| 53 | Output stripping for LLM | `lowfat` |
| 54 | Agent skills management | `tessl` |

## Failure Conditions
| Violation | Use Instead |
|-----------|------------|
| `grep` | `rg` |
| `cat` | `bat` or `glow` |
| `ls` | `eza` |
| `find` | `fd` |
| `du` | `dust` |
| `ps` | `procs` |
| `top` | `btop` or `btm` |
| `curl` (API calls) | `http` |
| Session without `onefetch` + `eza --tree` | Run pre-flight sequence |
| `sed` for batch rename | `sd` |
| Reading JSON without `jq`/`jless`/`jnv` | Use JSON tool |
| `npm` or `pip` | `bun` or `uv` |
| Long process without `tmux` | Start tmux session |

## Token Optimization Priority (every session)
1. `rm -f .session-read-cache` — clear cached reads
2. `onefetch` — repo summary (0 reads)
3. `bat --line-range :30 memory/memory-bank/progress.md` — current status (faster than glow)
4. `eza --tree --level 2 --git-ignore` — structure
5. `tokei` — code breakdown
6. `rg "TODO|FIXME|HACK" .` — known issues
Only THEN open files with `bat` if needed.

## Additional Token Rules
- **Silent CLI** — suppress all command output unless error. Use `> /dev/null 2>&1 || echo "FAIL: ..."`.
- **One-line reporting** — no prose explanations. `✅ done: N files, +X -Y lines` or `❌ error: ...`.
- **No re-read** — if file was already read this session, use cached content. Track in `.session-read-cache`. Check with `grep -q "^file:" .session-read-cache` before reading.
- **Enola before read** — `enola explore` gives symbols in ~200 tokens vs file read (500-2000).
- **rg scope narrow** — `rg "pattern" --type ts -l .` for filenames only, then `bat --line-range` matches.
- **No full diff** — use `git diff --stat` for summary. Full diff only if user asks.
- **Cached vector search** — `curl -s localhost:8082/api/search?q=X` instead of reading modules.

## CodeBurn Observability
| Action | Command |
|--------|---------|
| Status | `codeburn status` |
| Optimize | `codeburn optimize` |
| Log system event | `codeburn log --type system "msg"` |
Costs auto-log to progress.md on shell exit.

## Auto Mode Switching — NEVER Manual
Start every session in **lazy** (~70 tokens). Switch to **full** (~1420 tokens) ONLY when the task requires it. Decision matrix (hardcoded — never ask user):

| If user asks for this | Use mode | Reason |
|---|---|---|
| "what is", "find", "explain", "read this file" | **lazy** | Simple lookup, one search |
| Single command, one file edit | **lazy** | Don't waste tokens |
| "build", "create", "implement", "refactor" | **full** | Need all rules |
| 3+ git operations in same task | **full** | CLI rules needed |
| After 3+ memory-search calls on same task | **full** | You keep searching = you need the rules loaded |

Switch with: `bat "$MEMORY_ROOT/memory/modules/01-core-rules.md"` (lazy→full).
Stay lazy by running `memory-search "<task>"` instead of loading files.

## Skill Discovery (do NOT load all 1147)
**1147 skills exist in `$MEMORY_ROOT/.agents/skills/`. Loading even 10 summaries costs more than doing the task.**
Find the right skill with minimum token spend:
1. **Name match** — `ls $MEMORY_ROOT/.agents/skills/ | rg -i "<keyword>"` (fastest, ~50 tokens)
2. **Description match** — `rg "description" $MEMORY_ROOT/.agents/skills/*/SKILL.md -l | head -5` (~100 tokens)
3. **Vector DB** — `memory-search "skill for <task>" 2` (~200 tokens)
4. **Load** — `bat --line-range :80 "$MEMORY_ROOT/.agents/skills/<match>/SKILL.md"` — read first 80 lines, stop if not relevant
5. **Abort** — no match? Do the task directly. No skill is better than a wrong skill.

## Silent CLI (MANDATORY — saves 30-40% tokens)
- EVERY bash command: suppress output unless error. Pattern: `cmd > /dev/null 2>&1 || echo "FAIL: cmd: $?"`
- `git add/commit/push`: silent. Only show on conflict: `git add -A 2>&1 | grep -v "^$" || true`
- Never `echo "Done"` or `echo "=== Section ==="` — those are wasted tokens
- Success = zero output. Error = one line.
- Reporting: one line max. `✅ N files, +X -Y` not prose paragraphs.

## Ollama as Primary Workhorse (zero-token coding)
- Simple edits (1-2 files), lint fixes, test writing → `aider --model ollama/qwen2.5-coder:3b --message "<task>"`
- Complex multi-file tasks → `opencode run "<task>"` (uses your credits)
- Coordination, questions, CLI → Antigravity directly
- Ollama and opencode are free/billed workhorses. Antigravity context is the expensive resource — use it for orchestration only.

## Vector DB First (search before load)
Before loading any module, search the vector DB:
```bash
curl -s "localhost:8082/api/search?q=your+topic" | jq -r '.memories[0].content // empty'
```
If vector DB returns a relevant chunk (~200 tokens), USE IT instead of loading the module (500-1000 tokens). Only load module if vector DB misses.

## Enola Pre-Flight for ALL Unfamiliar Repos
Before reading ANY file in an unfamiliar repo:
```bash
enola generate_snapshot . && enola explore <module>
```
This gives architecture, symbols, deps in ~50 tokens. Reading files blindly costs 500-2000 tokens each.

## Session Context Rules
- **Stale unloading**: when switching between domains (ML→UI→Security), actively note that previous module context is stale. Do not reference rules from unloaded modules.
- **No README loading**: README files are for humans. Never load them unless user explicitly asks.
- **Binary check before read**: `file -b --mime-encoding path` — skip if returns "binary"
- **Context budget**: if session feels bloated (>50K input), summarize and start fresh.

## Guardrails (auto-installed by session-start.sh)
8 wrappers at `~/bin/guardrails/` shadow: grep→rg, cat→bat, ls→eza, find→fd, du→dust, top→btop, ps→procs, sed→sd.

## Auto-Dispatch
`auto-dispatch <task>` suggests the right tool + module. Installed at `~/bin/auto-dispatch`.

## Output Compression
- All CLI output → pipe through `lowfat` (strips verbose): `cmd | lowfat`
- For known-verbose: `cmd | rtk` (60-90% compression)
- Markdown files → `glow` (compact rendered view)
- JSON files → `jq` or `jless` (never raw)
