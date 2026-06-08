# MEMORY — Aditya's Workspace & Agent Configuration Hub

Central repository for all system configurations, AI agent rules, CLI tool mappings, dotfiles, and automation setups. Bootstraps any new machine in a single clone.

---

## 📂 Repository Layout

```
📁 MEMORY/
├── GEMINI.md              ← Master agent rules (single source of truth)
├── AGENTS.md → GEMINI.md  ← Symlinks for every AI tool
├── CLAUDE.md → GEMINI.md
├── .clinerules → GEMINI.md
├── .cursorrules → GEMINI.md
├── .windsurfrules → GEMINI.md
├── .github/copilot-instructions.md → GEMINI.md
├── opencode.json          ← Opencode config (points to AGENTS.md)
│
├── config/
│   ├── opencode/          ← Opencode sub-config
│   ├── VIBE_CODER_GUIDE.md
│   ├── ZERO_PROMPTING_DIRECTIVE.md
│   ├── .aider.conf.yml
│   ├── .continuerc.json
│   ├── .editorconfig
│   ├── Makefile
│   └── README.md
│
├── memory/
│   ├── LESSONS_LEARNED.md     ← Cross-project error memory
│   ├── memory-bank/           ← Project state (progress, architecture, decisions)
│   └── vector_db/             ← ChromaDB (gemini ignored)
│
├── tools/
│   └── dashboard.py           ← Memory dashboard (localhost:8082)
│
├── templates/
│   ├── animations/            ← GSAP, Motion.dev, ReactBits, scroll patterns
│   ├── ASTRO_STARTERKIT.md
│   └── DEPLOYMENT_WORKFLOW.md
│
├── dotfiles/
│   ├── bash/bashrc
│   ├── git/gitconfig
│   ├── starship/starship.toml
│   └── install.sh
│
├── docs/
│   ├── codeburn.md
│   ├── images/
│   └── diagrams/
│
└── scratch/
```

---

## 🚀 Quick Start (New Machine)

```bash
git clone https://github.com/adityashirsatrao007/MEMORY.git ~/Desktop/Projects/MEMORY

# Step 2: Dotfiles
cd ~/Desktop/Projects/MEMORY/dotfiles && chmod +x install.sh && ./install.sh && source ~/.bashrc

# Step 3: CLI Tools (see below)
```

---

## 🛠️ CLI Tool Installation Reference

### One-Shot Script (Package Managers)

```bash
sudo apt update && sudo apt install -y bat eza ripgrep direnv gh docker.io pipx git tmux build-essential curl
pipx ensurepath
pipx install semgrep pgcli dvc graphifyy enola aider
npm install -g pm2 tldr codeburn
cargo install lowfat delta dust hyperfine onefetch jless jnv
```

### Standalone Binaries

| Tool | Install Command |
|------|----------------|
| **Trivy** | `curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \| sudo sh -s -- -b /usr/local/bin` |
| **Gitleaks** | `curl -sL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_x64.tar.gz \| sudo tar -xz -C /usr/local/bin gitleaks` |
| **Lazygit** | `curl -sL "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_$(uname -s)_$(uname -m).tar.gz" \| sudo tar -xz -C /usr/local/bin lazygit` |
| **Zoxide** | `curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh \| bash` |
| **Ollama** | `curl -fsSL https://ollama.com/install.sh \| sh` |
| **OnlyCLI** | Go build: `go install github.com/clementd64/onlycli@latest` |
| **Uv** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

---

## 🔧 Full Tool Inventory & Auto-Trigger Rules

The agent automatically selects the right CLI based on the task — zero tokens wasted.

| Category | Tool | Auto-Trigger Condition |
|----------|------|----------------------|
| **Search** | `rg` | Any code search (replaces grep) |
| **Files** | `fd` | Find files by name (replaces find) |
| **Listing** | `eza` | List directory with git status (replaces ls) |
| **Reading** | `bat` | View file with syntax highlighting (replaces cat) |
| **Markdown** | `glow` | Read rendered .md files |
| **JSON** | `jless` | Interactive JSON browser (>50 lines) |
| **JSON** | `fx` | Interactive JSON processor |
| **YAML** | `yq` | Query YAML files |
| **Text replace** | `sd` | Bulk find/replace across files |
| **Git diff** | `delta` | Syntax-highlighted diffs |
| **Git TUI** | `lazygit` | Interactive staging/committing |
| **Processes** | `procs` | Find/list processes (replaces ps) |
| **Monitor** | `btop` | GPU/CPU/RAM system monitor |
| **HTTP** | `http` | API testing with httpie |
| **Architecture** | `enola` | Codebase dependency graphs |
| **Code graph** | `graphify` | Persistent MCP codebase context |
| **Pair prog.** | `aider` | Multi-file AI coding with git |
| **Python** | `uv` | Package management 10-100x faster |
| **API→CLI** | `onlycli` | OpenAPI spec → CLI (35x cheaper than MCP) |
| **Tokens** | `codeburn` | Agent cost and token observability |
| **Compression** | `rtk` | Shrink CLI output 60-90% for LLM |
| **Strip output** | `lowfat` | Remove verbose CLI noise for agents |
| **Git commits** | `comet` | AI commit messages via local Ollama |
| **Skills** | `tessl` | Agent skills package manager |
| **Secrets** | `trufflehog` | Verify leaked credentials pre-commit |
| **Security** | `semgrep` | SAST and code quality scanning |
| **CVE scan** | `trivy` | Container/filesystem vulnerability scan |
| **Secrets** | `gitleaks` | Git history secret scanning |
| **Diagrams** | `d2` | Architecture/flow/ERD diagrams as code |
| **PC info** | `fastfetch` | Hardware/OS snapshot |
| **Benchmark** | `hyperfine` | Precision command benchmarking |
| **Dirs** | `dust` | Directory space usage (replaces du) |
| **Disk** | `duf` | Disk usage summary |
| **Network** | `nmap` | Port/network scanning |
| **File mgr** | `yazi` | Terminal file manager |
| **History** | `atuin` | Shell history database with search |
| **Jump** | `zoxide` | Smart directory jumping (replaces cd) |
| **Fuzzy** | `fzf` | Universal fuzzy finder |

---

## 🌐 Running Services

| Service | Port | Purpose | Status |
|---------|------|---------|--------|
| Qdrant | 6333 | Supamem vector DB backend | ✅ tmux |
| Memory Dashboard | 8082 | ChromaDB vector memory UI | ✅ tmux |
| Graphify | — | Codebase knowledge graph MCP | ✅ tmux |

---

## 🧠 Agent Rules (GEMINI.md)

`GEMINI.md` is the single source of truth. Every AI tool (Claude Code, Cursor, Windsurf, Cline, Copilot, Opencode) symlinks to it. Contents:

- Session start protocol & memory load
- Zero-token CLI rulebook (60+ tool mappings)
- ML/DL decision tree (model, dataset, VRAM, tracking)
- UI/UX design standards (Apple HIG, dark luxury)
- Architecture diagrams (D2, diagrams, matplotlib)
- Code review & security audit protocols
- Enterprise patterns (SAGA, CQRS, EDA)
- Password security (Argon2, bcrypt)
- And 15+ other domain-specific playbooks

---

## 🔄 Dotfiles Backup

All configs version-controlled here and mirrored at `github.com/adityashirsatrao007/dotfiles`. On machine wipe:

```bash
git clone https://github.com/adityashirsatrao007/dotfiles.git && cd dotfiles && ./install.sh
```
