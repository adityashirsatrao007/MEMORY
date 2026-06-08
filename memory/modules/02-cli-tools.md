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
1. `onefetch` — repo summary (0 reads)
2. `glow memory-bank/progress.md` — current status
3. `eza --tree --level 2 --git-ignore` — structure
4. `tokei` — code breakdown
5. `rg "TODO|FIXME|HACK" .` — known issues
Only THEN open files with `bat` if needed.

## Additional Token Rules
- **Silent CLI** — suppress all command output unless error. Use `> /dev/null 2>&1 || echo "FAIL: ..."`.
- **One-line reporting** — no prose explanations. `✅ done: N files, +X -Y lines` or `❌ error: ...`.
- **No re-read** — if file was already read this session, use cached content. Track in `.session-read-cache`.
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

## Guardrails (auto-installed by session-start.sh)
8 wrappers at `~/bin/guardrails/` shadow: grep→rg, cat→bat, ls→eza, find→fd, du→dust, top→btop, ps→procs, sed→sd. They warn then still run original command — switch tools immediately on warning.

## Auto-Dispatch
`auto-dispatch <task>` suggests the right tool + module. Installed at `~/bin/auto-dispatch`.

## rtk Auto-Pipe
All long-output commands should pipe through rtk: `cmd | rtk`. If running interactively and output expected, use `cmd | lowfat`.
