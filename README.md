> **Copyright (c) 2026 Aditya Shirsatrao. All rights reserved.**  
> Proprietary — see [LICENSE](LICENSE). No copying, cloning, or distribution without written permission.

# MEMORY — The Ultimate AI Agent Infrastructure

<p align="center">
  <strong>Your entire AI development environment, reproducible in one command.</strong><br>
  ~2.7B free LLM tokens/month · 1200+ models · 50+ agent skills · ChromaDB vector brain<br>
  One-shot setup across Linux, macOS, and WSL2.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-Proprietary-red.svg?style=for-the-badge" alt="License: Proprietary">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL2-ff69b4?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/LLM-Free%20Proxy%20(2.7B%20tokens%2Fmonth)-brightgreen?style=for-the-badge" alt="Free LLM proxy">
  <img src="https://img.shields.io/badge/Models-1200%2B-8A2BE2?style=for-the-badge" alt="1200+ models">
  <img src="https://img.shields.io/badge/Skills-50%2B-orange?style=for-the-badge" alt="50+ skills">
  <img src="https://img.shields.io/badge/GPG%20Signing-Enabled-success?style=for-the-badge" alt="GPG Signing">
  <img src="https://img.shields.io/badge/API%20Keys-12%20Providers-blue?style=for-the-badge" alt="API Keys">
</p>

---

## Table of Contents

- [Why MEMORY?](#why-memory)
- [What's Inside — Complete File Catalog](#whats-inside--complete-file-catalog)
  - [Root Files](#root-files)
  - [`memory/` — Agent Knowledge Base](#memory--agent-knowledge-base)
  - [`config/` — IDE & Tool Configurations](#config--ide--tool-configurations)
  - [`dotfiles/` — Shell Environment & Aliases](#dotfiles--shell-environment--aliases)
  - [`tools/` — Agent Utilities](#tools--agent-utilities)
  - [`.agents/skills/` — 46 Reusable Agent Skills](#agentsskills--46-reusable-agent-skills)
  - [`.githooks/` — Local Git Automation](#githooks--local-git-automation)
  - [`.github/` — CI/CD & Copilot](#github--cicd--copilot)
  - [`templates/` — Project Scaffolds & References](#templates--project-scaffolds--references)
- [Global Key Infrastructure](#global-key-infrastructure)
  - [API Keys Database](#api-keys-database)
  - [SSH Key Management](#ssh-key-management)
  - [GPG Commit Signing](#gpg-commit-signing)
- [LLM Layer — All Models Available](#llm-layer--all-models-available)
  - [freellmapi Proxy (90+ Models)](#freellmapi-proxy-90-models)
  - [fcc-server (1130 Models)](#fcc-server-1130-models)
- [Agent Frameworks — In-Depth](#agent-frameworks--in-depth)
  - [Swarms v13.0.0](#swarms-v1300)
  - [NeoAgent v2.4.3](#neoagent-v243)
  - [MiMo-Code](#mimo-code)
  - [Hermes Agent v0.15.2 (Nous Research)](#hermes-agent-v0152-nous-research)
  - [Free Claude Code (fcc-claude)](#free-claude-code-fcc-claude)
  - [Mistral Vibe CLI v2.15.0](#mistral-vibe-cli-v2150)
- [Internet Access Layer — Agent-Reach v1.5](#internet-access-layer--agent-reach-v15)
- [Agent Skills — Complete Catalog of 50+](#agent-skills--complete-catalog-of-50)
- [Agent Memory — ChromaDB Vector Database](#agent-memory--chromadb-vector-database)
- [Shell Environment — Every Tool Explained](#shell-environment--every-tool-explained)
- [Automated GitHub Project Creation](#automated-github-project-creation)
- [Architecture — How Everything Connects](#architecture--how-everything-connects)
- [Quick Start](#quick-start)
- [Platform Compatibility](#platform-compatibility)
- [License](#license)

---

## Why MEMORY?

AI agents are useless without infrastructure. Every new machine means hours of setup — installing tools, configuring shells, hunting for API keys, wiring up models, setting up GPG signatures, configuring git, and debugging environment variables. MEMORY eliminates that entirely.

**One `git clone` + one pasted prompt = a production-ready agent workstation with:**

- **1200+ LLM models** at zero cost (~2.7B free tokens/month combined across 12+ providers)
- **46 agent skills** — reusable instruction sets for diagnose, review, TDD, prototype, design, writing, and more
- **12 LLM providers** — DeepSeek, Google Gemini, Mistral, Groq, Cohere, Cloudflare, OpenRouter, NVIDIA NIM, Moonshot (Kimi), Z.AI, OpenAI-compat, and Liquid
- **7 integrated agent frameworks** — Swarms, NeoAgent, MiMo, Hermes, Free Claude Code, Mistral Vibe, and Agent-Reach
- **Persistent vector memory** — ChromaDB with semantic search, auto-updated on every commit
- **Pre-configured shell** — eza, bat, ripgrep, fd, zoxide, fzf, starship, tmux, delta, lazygit
- **Global key infrastructure** — centralized API keys database, SSH key pair, GPG commit signing
- **Auto-loaded environment** — every bash session automatically sources all API keys, paths, and aliases
- **GitHub-ready** — `gh` CLI authenticated, GPG-signed commits, `delta` diff viewer, `lazygit` TUI
- **CI/CD** — Trivy vulnerability scanning and Gitleaks secret detection on every push
- **Cross-platform** — same setup works on Linux, macOS, and Windows (WSL2)

**What takes a day to set up now takes 60 seconds.**

---

## What's Inside — Complete File Catalog

### Root Files

| File | Purpose |
|------|---------|
| `GEMINI.md` | **Master agent configuration.** The single source of truth loaded by every agent (Claude Code, Gemini CLI, OpenCode, Antigravity, Cursor, Windsurf, Continue.dev, Copilot). Contains all behavioral rules, tool dispatching, guardrails, token optimization, and references to 12 modular knowledge files. All other agent configs symlink to this file. |
| `AGENTS.md` → `GEMINI.md` | Symlink — loaded by OpenCode and any agent that reads `AGENTS.md` by convention. |
| `CLAUDE.md` → `GEMINI.md` | Symlink — loaded by Claude Code on startup. |
| `opencode.json` | OpenCode configuration — points to `AGENTS.md` for instructions, sets the workspace root. |
| `LICENSE` | **Proprietary "All Rights Reserved" license.** Explicitly forbids copying, cloning, forking, downloading, distributing, or using as AI training data. This repository is viewable for portfolio/reference purposes only under GitHub ToS. Unauthorized use will be pursued to the fullest extent of law. |
| `README.md` | This file — complete documentation for the entire repository. |
| `SETUP.md` | The one-shot setup prompt for agents. Copy and paste into any AI agent on a new machine — 13 steps that automatically install everything: system packages, language runtimes, CLIs, Ollama, opencode, guardrails, ChromaDB dashboard, vector DB seeding, and verification. |
| `Makefile` | Automation targets: `make validate` (check module integrity), `make seed` (re-seed vector DB), `make stats` (token savings report), `make hooks` (install git hooks), `make fix-paths` (fix relative paths), `make all` (validate + seed). |
| `skills-lock.json` | Lockfile mapping all 46 skills to their source repositories with content hashes. Prevents drift and enables deterministic re-installation. |
| `.agentignore` | **96 rules** telling agents which files to NEVER read. Prevents token waste on build outputs, dependencies, lock files, media, IDE files, database files, and binary artifacts. Each rule saves 100-5000 tokens per session. |
| `.gitignore` | Standard Git ignore rules for the repository. |
| `.agent-progress.md` | Dynamic handoff document — updated at the end of every agent session so the next agent can resume without re-analysis. Contains git status, diff summary, session notes, and directives. |

---

### `memory/` — Agent Knowledge Base

The brain of the system. 13 modular knowledge files + 5 session tracking files + 1 cross-project error memory.

#### Modules (13 files, ~2100 lines total)

| Module | Lines | Purpose |
|--------|-------|---------|
| `01-core-rules.md` | 115 | **Core agent behavior.** Zero-prompting directive (agent must never ask for permission), Karpathy's "vibe coding" standards, Ponytail optimization protocol, production code quality rules, "no broken windows" principle, code review protocol with mandatory lint+typecheck steps, agent-to-agent handoff rules. |
| `02-cli-tools.md` | 160 | **54-tool dispatch table.** Complete catalog of every CLI tool with usage patterns, failure conditions, and token costs. Includes: silent CLI protocol (no verbose flags), token optimization priority order (ollama → vector DB → enola → proxy), guardrail bypass instructions, enola pre-flight sequence. |
| `03-ml-engineering.md` | 292 | **ML/DL engineering workflow.** Docker and Kubernetes patterns, GPU setup (CUDA/cuDNN), API keys for ML providers, data pipeline design (ETL, feature stores, versioning), model training lifecycle, experiment tracking (MLflow, W&B), MLOps best practices. |
| `04-security.md` | 147 | **Repository security.** Hygiene rules (no hardcoded secrets, no `.env` commits), secret scanning with Gitleaks/TruffleHog, `semgrep` SAST rules, git guardrails (block dangerous commands), password hashing standards, dependency vulnerability management. |
| `05-ui-ux.md` | 274 | **Apple HIG design standards.** Complete design system reference: color palettes with neutral/slate requirements, typography scale (SF Pro, Inter), spacing grid (4px increments), animation patterns and timing functions, component library conventions, validation rules that `validate_ui.py` enforces. |
| `06-web-dev.md` | 305 | **Web development.** Full-stack project setup workflow (Next.js, Astro, SvelteKit), SEO optimization checklist, Core Web Vitals, performance budgets, deployment workflows (Vercel, Netlify, Docker), CODVYN patterns. |
| `07-job-hunt.md` | 145 | **Career management.** ATS resume optimization with keyword targeting, LinkedIn profile strategy, interview preparation framework, salary negotiation tactics, portfolio presentation. |
| `08-architecture.md` | 198 | **Enterprise architecture patterns.** SAGA orchestration, CQRS, event sourcing (CDC/Kafka), LLM proxy architecture design, system decomposition strategies, anti-corruption layers. |
| `09-misc.md` | 255 | **General reference.** AI development roadmap, GitHub tips and tricks, OpenStreetMap integration, AlgoTracker setup, terminal productivity, infrastructure management notes (antigravity ports, token budgets, API key rotation). |
| `10-lessons-learned.md` | 17 | **Hardcoded directives.** Zero pushback rule (never argue with user), multi-agent token management, Claude Code routing protocol, priority override instructions. |
| `11-error-logs.md` | 30 | **Historical error records.** OOM errors and their fixes, PEP 668 Python packaging failures, system freeze prevention (memory limits), all past failure modes with verified solutions. |
| `12-repo-teachings.md` | 107 | **18 starred repositories** — architectural knowledge extracted from OpenBB, Ruff, Claude-Code-Rust, and 15 other projects. Patterns, conventions, and design decisions from real-world codebases. |

#### Memory Bank (5 files)

| File | Purpose |
|------|---------|
| `activeContext.md` | Current session focus, active decisions, open questions the agent is working on. Updated by the agent during sessions. |
| `architecture.md` | Tech stack overview, directory structure map, environment variable documentation, data flow diagrams. Auto-populated by agents as the project evolves. |
| `decisions.md` | Key architectural and technical decisions with rationale. Prevents agents from second-guessing or redoing past choices. Documents OpenCode CLI delegation pattern. |
| `progress.md` | Complete session log with 57+ entries spanning the project's history. Documents what's done, what's in progress, what's next, and known issues. |
| `walkthrough.md` | Quick repository orientation — architecture diagram, key file map, setup steps. |

#### Additional

| File | Purpose |
|------|---------|
| `LESSONS_LEARNED.md` | **Permanent cross-project error memory.** 14 documented failure patterns with root cause analysis and standardized resolution protocols. Agents read this before every task to avoid repeating mistakes. Topics: broken PPAs, broken symlinks, legacy CLI usage, OpenCode delegation, pre-flight sequence, token bloat, missing quality checks, documented-but-uninstalled tools, hardcoded paths, bloat creep, agentignore drift, empty directories, and deletion protocol. |

---

### `config/` — IDE & Tool Configurations

| File | Purpose |
|------|---------|
| `.aider.conf.yml` | **Aider AI pair programmer configuration.** Instructs Aider to read `GEMINI.md` as its rules file, ensuring consistent behavior across all coding agents. |
| `.continuerc.json` | **Continue.dev extension configuration.** Instructs the Continue.dev VS Code/JetBrains extension to always read `GEMINI.md` before making changes. |
| `.editorconfig` | **Editor formatting standards.** Enforces 2-space indentation, LF line endings, UTF-8 encoding, and trailing newline across all editors. |
| `opencode/AGENTS.md` → `../../GEMINI.md` | **OpenCode agent rules.** Symlink to master config for OpenCode's agent mode. |

---

### `dotfiles/` — Shell Environment & Aliases

Every terminal session is pre-configured with modern CLI replacements, aliases, environment variables, and tools.

| File | Contents | Key Features |
|------|----------|--------------|
| `bash/bashrc` | **249-line bash configuration** | — Zero-token CLI aliases (`grep`→`rg`, `cat`→`bat`, `ls`→`eza`, `find`→`fd`, `du`→`dust`, `ps`→`procs`, `top`→`btop`, `sed`→`sd`)<br>— `$MEMORY_ROOT` environment variable (points to repo)<br>— `$MEMORY_MODE=lazy` (optimizes agent token usage)<br>— Global API keys auto-loader `source ~/.config/global-apikeys/load_keys.sh`<br>— Zoxide smart navigation (`cd`→`z`)<br>— Starship prompt initialization<br>— Atuin shell history with encrypted sync<br>— NVM, Conda, Cargo path setup<br>— Battery/GPU power management aliases<br>— Agent read cache (`mark-read`, `is-read` functions)<br>— `$PATH` includes MEMORY tools, local bin, cargo, nvm, bun, opencode, guardrails |
| `bash/rtk-hook.sh` | **Output compression hook.** Auto-pipes verbose CLI output through `rtk` to compress lengthy terminal output before it enters context. Prevents token bloat from verbose commands. |
| `git/gitconfig` | **35-line git configuration** | — GPG-signed commits (`signingkey = 0027EFBE3F4CD520`, `gpgsign = true`)<br>— `gh` CLI credential helper (no manual token entry)<br>— `delta` as default pager with syntax highlighting and word-level diffs<br>— `zdiff3` merge conflict style (shows base, ours, theirs)<br>— `main` as default branch<br>— LFS filter support<br>— 500MB post buffer for large pushes |
| `starship/starship.toml` | Starship prompt theme. Minimal, fast, informative shell prompt. |
| `tmux/tmux.conf` | Tmux terminal multiplexer configuration. |
| `install.sh` | **Dotfile installer.** Symlinks all configs to their proper `~` locations in one command. |
| `Makefile` | Make targets for dotfile-specific operations. |
| `.editorconfig` | Editor formatting rules (2-space, LF, UTF-8). |
| `.gitignore` | Gitignore rules for dotfiles. |

---

### `tools/` — Agent Utilities

| Tool | Language | Purpose |
|------|----------|---------|
| `dashboard.py` | **Python (FastAPI)** | ChromaDB vector search dashboard. Runs on port 8083. Provides web UI, search API, and health endpoint. Agents query this for semantic memory recall. Now uses freellmapi proxy for all LLM calls (zero cost). |
| `seed_vector_db.py` | **Python** | Seeds ChromaDB from all 13 module files. Features **content-hash dedup** — skips files that haven't changed since last seed unless `--force` is passed. Auto-runs on post-merge and post-commit hooks. |
| `validate_ui.py` | **Python** | UI quality scanner. Checks all HTML files for: Apple HIG font compliance, banned colors (raw red/green/blue), placeholder text, and missing design tokens. Runs as a pre-commit hook to enforce design standards. |
| `memory-search` | **Bash** | CLI wrapper for ChromaDB semantic search. Example: `memory-search "token optimization"` returns relevant chunks from the knowledge base in milliseconds. |
| `handoff` | **Bash** | Agent session handoff utility. Writes current state (git status, diff, session notes) to `.agent-progress.md` so the next agent picks up without context loss. |

---

### `.agents/skills/` — 46 Reusable Agent Skills

Each skill is a self-contained instruction set the agent loads on demand. Skills are organized by source:

**8 from plannotator/effective-html:**
| Skill | Purpose |
|-------|---------|
| `html` | Create self-contained HTML files for any purpose — reports, explainers, comparisons, decks, prototypes. Includes 20 reference HTML files demonstrating effectiveness patterns. |
| `html-diagram` | Create full-screen SVG architecture diagrams in self-contained HTML. Visualizes system architecture, data flow, component relationships. Includes reference library of 20 HTML effectiveness examples. |
| `html-plan` | Create visually organized plan pages in HTML. Pragmatic, clear structure for project plans, roadmaps, and specs. Includes 20 reference HTML files. |

**15 from Leonxlnx/taste-skill:**
| Skill | Purpose |
|-------|---------|
| `brandkit` | Brand identity creation — logos, color palettes, typography, brand guidelines. |
| `design-taste-frontend` | Frontend design with taste-based styling — modern, aesthetic UI generation. |
| `design-taste-frontend-v1` | Alternative version of taste-driven frontend design. |
| `full-output-enforcement` | Ensures agents produce complete, non-truncated output. Prevents "..." and "would continue" patterns. |
| `gpt-taste` | Taste-aware content generation that matches brand aesthetic. |
| `high-end-visual-design` | Premium/enterprise visual design patterns — luxury aesthetics, polished UI. |
| `image-to-code` | Convert design images/screenshots to working code. |
| `imagegen-frontend-mobile` | Mobile-optimized image generation frontend. |
| `imagegen-frontend-web` | Web-optimized image generation frontend. |
| `industrial-brutalist-ui` | Industrial brutalism design style — raw, structural, utilitarian aesthetics. |
| `minimalist-ui` | Minimalist UI design — clean, sparse, content-first. |
| `redesign-existing-projects` | Redesign existing interfaces with improved aesthetics and UX. |
| `stitch-design-taste` | Combine multiple taste/style systems into a cohesive design. |
| `taste-skill` | Self-contained plugin with 10+ sub-skills, `.claude-plugin/` hooks, research directory, and examples. |

**23 from mattpocock/skills:**
| Skill | Purpose |
|-------|---------|
| `caveman` | **Ultra-compressed communication.** Cuts token usage ~75% by dropping filler, articles, and pleasantries while keeping full technical accuracy. Activated by "caveman mode" or "/caveman". |
| `design-an-interface` | Generate multiple radically different interface designs using parallel sub-agents. "Design it twice" methodology. |
| `diagnose` | **Disciplined debugging loop** for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Includes HITL loop template script. |
| `edit-article` | Edit and improve articles — restructuring, clarity, tightening prose. |
| `git-guardrails-claude-code` | Set up Claude Code hooks that block dangerous git commands (push, reset --hard, clean, branch -D). Includes `block-dangerous-git.sh` script. |
| `grill-me` | **Stress-test interviews.** The agent relentlessly questions the user's plan or design until reaching shared understanding. "Grill me" mode for decision clarity. |
| `grill-with-docs` | Grilling session that challenges plans against the existing domain model (CONTEXT.md) and documented decisions (ADRs). Updates docs inline as decisions crystallise. |
| `handoff` | Compact the current conversation into a handoff document for another agent — preserves context across agent switches. |
| `improve-codebase-architecture` | Find refactoring opportunities, consolidate tightly-coupled modules, make codebases more testable and AI-navigable. Generates DEEPENING.md, HTML-REPORT.md, INTERFACE-DESIGN.md, LANGUAGE.md. |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to `@total-typescript/shoehorn`. |
| `obsidian-vault` | Search, create, and manage notes in an Obsidian vault with wikilinks and index notes. |
| `prototype` | **Build throwaway prototypes.** Two branches: terminal app for state/logic exploration, or multiple UI variations toggleable from one route. Includes LOGIC.md and UI.md guidance. |
| `qa` | Interactive QA session — user reports bugs conversationally, agent files GitHub issues with proper labels and reproduction steps. |
| `request-refactor-plan` | Create detailed refactor plans with incremental commits via user interview. Files as GitHub issues. |
| `review` | **Dual-axis code review.** Reviews changes against two axes simultaneously: Standards (does code follow repo conventions?) and Spec (does code match the originating PRD/issue?). Reports both side-by-side. |
| `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. |
| `setup-matt-pocock-skills` | Sets up agent skills documentation block in AGENTS.md/CLAUDE.md and docs/agents/. Configures issue tracker (GitHub/GitLab/local) and triage labels. |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged, type checking, and tests. |
| `tdd` | **Full test-driven development** with red-green-refactor loop. Includes deep modules on: testing strategies, mocking patterns, interface design, refactoring, and advanced techniques. |
| `teach` | Teach the user new skills with structured mission/glossary/learning-record/resources format. |
| `to-issues` | Break plans, specs, or PRDs into independently-grabbable GitHub issues using vertical slice decomposition. |
| `to-prd` | Convert conversation context into a Product Requirements Document and publish to the issue tracker. |
| `triage` | **Full issue triage state machine** — intake, refinement, prioritization, assignment. Includes AGENT-BRIEF.md and OUT-OF-SCOPE.md for autonomous triage delegation. |
| `ubiquitous-language` | Extract DDD-style domain glossary from conversations. Flags ambiguities, proposes canonical terms. Saves to UBIQUITOUS_LANGUAGE.md. |
| `write-a-skill` | Create new agent skills with proper structure, progressive disclosure, and bundled resources. |
| `writing-beats` | Shape articles as narrative journeys — user picks a starting beat, agent writes it, offers options for the next beat. |
| `writing-fragments` | Mine the user for raw writing material (claims, vignettes, sharp sentences) and append to a document for future use. |
| `writing-shape` | Take raw material markdown and shape it into an article through conversational iteration — openings, structure, formatting. |
| `zoom-out` | Get broader context or higher-level perspective on unfamiliar code sections. "Tell me how this fits into the bigger picture." |

---

### `.githooks/` — Local Git Automation

Three hooks that automate vector DB maintenance and quality enforcement:

| Hook | Trigger | Action |
|------|---------|--------|
| `pre-commit` | Before every commit | Runs `make validate-ui` — scans all changed files for banned colors, placeholder text, and design violations. Blocks the commit if violations found. |
| `post-merge` | After every pull/merge | Checks if `memory/modules/` files changed. If yes, auto-re-seeds ChromaDB so the vector brain stays in sync with the knowledge base. |
| `post-commit` | After every commit | Same as post-merge — re-seeds ChromaDB if module files changed. Ensures the vector database is never stale. |

---

### `.github/` — CI/CD & Copilot

| File | Purpose |
|------|---------|
| `workflows/ci.yml` | **GitHub Actions CI pipeline.** Triggers on push/PR to main/master. Two jobs: Trivy filesystem scan (CRITICAL/HIGH severity vulnerabilities) and Gitleaks secret detection. Runs on every push — no secrets leak into the repo. |
| `copilot-instructions.md` → `../../GEMINI.md` | **GitHub Copilot instructions.** Symlink to master config — Copilot follows the same rules as every other agent. |

---

### `templates/` — Project Scaffolds & References

| Path | Contents | Purpose |
|------|----------|---------|
| `agent-skills/` | Full skill plugin template — commands, hooks, docs, 16+ reference skills, build scripts, Kof commands. | Scaffold for creating new agent skill repositories. |
| `ponytail/` | Full "Ponytail" skill plugin — hooks, pi-extension, benchmarks, tests, Python/Deno/Node implementations, GUI, task files. | Reference implementation of a complete skill system. |
| `animations/` | 8 animation reference files — scrollytelling examples, Framer Motion patterns, Spline 3D references, CSS animation guides. | Resource library for UI animation generation. |
| `CLAUDE_CODES.md` | 100 stacked Claude prompt modifiers — systematic prompt engineering references. | Prompt crafting reference. |

---

## Global Key Infrastructure

### API Keys Database

**Location:** `~/.config/global-apikeys/`

Centralized, auto-loaded credential management for all API keys. Every bash session automatically sources these keys.

| File | Purpose |
|------|---------|
| `keys.env` | **All API keys** stored as `KEY=VALUE` pairs. Last updated 2026-06-12. |
| `load_keys.sh` | **Bash loader** — `source` this file to export all keys (`set -a; source keys.env; set +a`). Called from `~/.bashrc` line 246. |
| `load_keys.py` | Python equivalent — loads keys into `os.environ`. |
| `load_keys.js` | Node.js equivalent — loads keys into `process.env`. |
| `add_key.sh` | Utility script for adding new keys to the database. |
| `project_template.envrc` | Direnv template for per-project environment variable scoping. |

**Currently configured providers (12 total):**

| Provider | Env Variable | Service |
|----------|-------------|---------|
| Groq | `GROQ_API_KEY` | Ultra-low latency LLM inference |
| Google Gemini | `GEMINI_API_KEY` | Gemini 2.5 Flash/Pro |
| OpenRouter | `OPENROUTER_API_KEY` | 200+ model router |
| Cerebras | `CEREBRAS_API_KEY` | Ultra-fast inference |
| NVIDIA NIM | `NVIDIA_NIM_API_KEY` | Enterprise model hosting |
| Hugging Face | `HF_TOKEN` | Model hub + inference |
| OpenCode | `OPENCODE_API_KEY` | OpenCode AI |
| Z.AI | `ZAI_API_KEY` | GLM models |
| DeepSeek | `DEEPSEEK_API_KEY` | DeepSeek V4 |
| Moonshot/Kimi | `KIMI_API_KEY` | Kimi K2 |
| Fireworks | `FIREWORKS_API_KEY` | Fast serverless inference |
| Wafer | `WAFER_API_KEY` | Anthropic-compatible Messages API |

**Unified proxy:** All keys are also routed through `freellmapi` at `http://localhost:3001/v1` — agents can use a single endpoint and key instead of managing 12 separate credentials.

**Auto-load mechanism (`~/.bashrc` line 246):**
```bash
[[ -f "$HOME/.config/global-apikeys/load_keys.sh" ]] && source "$HOME/.config/global-apikeys/load_keys.sh"
```
This runs in every interactive shell — no manual sourcing ever needed.

---

### SSH Key Management

**Key pair location:** `~/.ssh/`

| File | Purpose |
|------|---------|
| `id_ed25519` | **Private key** — Ed25519 algorithm (modern, fast, secure). Created 2026-06-12. |
| `id_ed25519.pub` | **Public key** — registered with GitHub for authentication. |
| `authorized_keys` | Authorized keys file for SSH access to this machine. |
| `known_hosts` | Verified SSH host fingerprints. |

**Usage:** The SSH key enables:
- Password-less `git push`/`git pull` to GitHub
- SSH access to remote servers and VPS instances
- Secure code deployment without credential prompts

**How it's configured:**
```bash
# Generate (done once):
ssh-keygen -t ed25519 -C "adityashirsatrao007@gmail.com"

# GitHub authentication via gh CLI (configured in gitconfig):
# [credential "https://github.com"]
#     helper = !/usr/bin/gh auth git-credential
```

---

### GPG Commit Signing

Every git commit is cryptographically signed for authenticity verification.

| Detail | Value |
|--------|-------|
| **Algorithm** | RSA 4096-bit |
| **Key ID** | `0027EFBE3F4CD520` |
| **Fingerprint** | `2048 2AA3 B910 F525 B12C FB17 0027 EFBE 3F4C D520` |
| **UID** | `Aditya <adityashirsatrao007@gmail.com>` |
| **Capabilities** | Sign, Certify, Encrypt, Authenticate, Reserved |
| **Created** | 2026-06-12 |
| **Trust level** | Ultimate |

**Git configuration (dotfiles/git/gitconfig):**
```ini
[user]
    signingkey = 0027EFBE3F4CD520
[gpg]
    format = openpgp
[commit]
    gpgsign = true
```

**Result:** Every commit displays a `✅ Verified` badge on GitHub, proving the commit came from the legitimate key holder and hasn't been tampered with. This is essential for:
- Supply chain security
- Open source credibility
- Preventing commit spoofing
- Automated CI/CD trust verification

---

## LLM Layer — All Models Available

### freellmapi Proxy (90+ Models)

**Endpoint:** `http://localhost:3001/v1` (OpenAI-compatible)  
**API Key:** `freellmapi-c72bebe9578ae453d5d77b79af6e988e19405950c2087632`  
**Token Budget:** ~2.7B free tokens/month combined across providers  
**Auth:** `Authorization: Bearer <key>`  
**Chat:** `POST /v1/chat/completions`  
**Dashboard:** Web UI at `http://localhost:3001`

**Smart failover:** Auto-benches rate-limited keys and falls through to the next available provider. No configuration needed.

#### Provider Breakdown

| Provider | Models | Access |
|----------|--------|--------|
| **Cloudflare Workers AI** | 20+ | `@cf/*` prefix — qwen, deepseek, meta, google, nvidia, mistral, zai |
| **DeepSeek** | 5+ | `deepseek-ai/*` — v4 flash, v4 pro, coder |
| **Google (via API)** | 8+ | `gemini-*` — 2.5 flash/pro, 3.5 flash, 3.1 pro |
| **Mistral AI** | 8+ | `mistral-*` — large 3, codestral, devstral, magistral, ministral |
| **Groq** | 4+ | `groq/*` — compound, llama, mixtral |
| **Meta (via Cloudflare)** | 4+ | `@cf/meta/*` — llama 3.3, 3.1, 4 |
| **NVIDIA NIM** | 8+ | `nvidia/nemotron-*` — 3 super, 3 ultra, 3 nano |
| **Cohere** | 4+ | `command-*` — command-a, command-r, command-r-plus |
| **Moonshot/Kimi** | 4+ | `moonshotai/*` — kimi-k2.6, kimi-k2-thinking |
| **Z.AI** | 4+ | `z-ai/*` — glm-5.1, glm-4.7, glm-4.5 |
| **OpenRouter** | 3+ | `openrouter/*` — owl-alpha, various community models |
| **OpenAI-compat** | 6+ | `openai/*` — gpt-oss, gpt-4.1, openai-fast |
| **Liquid** | 2+ | `liquid/*` — lfm-2.5 models |
| **MiniMax** | 1+ | `minimaxai/*` — m2.7 |
| **Poolside** | 2+ | `poolside/*` — laguna models |
| **IBM Granite** | 1+ | `@cf/ibm-granite/*` |
| **Nous Research** | 1+ | `nousresearch/*` — hermes-3 |
| **StepFun** | 1+ | `stepfun/*` |

#### Complete Model List (90+)

```
auto                                                        (smart router)
deepseek-ai/deepseek-v4-flash                               (flagship reasoning)
deepseek-ai/deepseek-v4-pro                                 (pro reasoning)
deepseek-ai/DeepSeek-V4-Flash                               (alt endpoint)
deepseek-v4-flash-free                                      (free tier)
deepseek-ai/deepseek-v3.2                                   (v3.2)
qwen/qwen3-coder:free                                       (coding specialist)
qwen/qwen3-coder-480b-a35b-instruct                         (480B coder)
qwen/qwen3-coder-next                                       (next-gen coder)
qwen3-coder:480b, qwen3-coder-next                          (short names)
qwen/qwen3-next-80b-a3b-instruct:free                       (80B MoE)
qwen/qwen3-32b, qwen3-32b                                   (32B general)
qwen-3-235b-a22b-instruct-2507                              (235B MoE)
@cf/qwen/qwen3-30b-a3b-fp8                                  (Cloudflare)
gemini-2.5-flash, gemini-2.5-flash-lite                     (Gemini 2.5)
gemini-2.5-pro                                              (Gemini 2.5 Pro)
gemini-3.5-flash                                            (latest gen)
gemini-3.1-pro-preview                                      (preview)
gemini-3.1-flash-lite-preview                               (flash lite)
gemini-3-flash-preview                                      (3 flash)
mistralai/mistral-large-3-675b-instruct-2512                (675B flagship)
mistral-large-latest, mistral-medium-latest                 (standard tiers)
mistral-small-latest, ministral-8b-latest                   (small + mini)
codestral-latest, devstral-latest                           (coding optimized)
devstral-2:123b                                             (devstral 2)
magistral-medium-latest                                     (magistral)
@cf/moonshotai/kimi-k2.6                                    (via Cloudflare)
moonshotai/kimi-k2.6, moonshotai/Kimi-K2.6                  (Kimi K2)
moonshotai/kimi-k2.6:free                                   (free tier)
kimi-k2-thinking                                            (thinking mode)
minimaxai/minimax-m2.7                                      (MiniMax M2.7)
minimax-m3-free                                             (M3 free tier)
meta/llama-4-maverick-17b-128e-instruct                     (Llama 4 Maverick)
meta-llama/llama-4-scout-17b-16e-instruct                   (Llama 4 Scout)
@cf/meta/llama-4-scout-17b-16e-instruct                     (via Cloudflare)
meta-llama/llama-3.3-70b-instruct:free                      (Llama 3.3 free)
meta-llama/llama-3.1-70b-instruct                           (Llama 3.1)
@cf/meta/llama-3.3-70b-instruct-fp8-fast                    (Cloudflare)
llama-3.3-70b-versatile                                     (Groq)
llama-3.1-8b-instant                                        (8B instant)
meta-llama/llama-3.2-3b-instruct:free                       (3B free)
nvidia/nemotron-3-ultra-550b-a55b:free                      (550B ultra)
nvidia/nemotron-3-super-120b-a12b                           (120B super)
nvidia/nemotron-3-super-120b-a12b:free                      (free tier)
nvidia/nemotron-3-nano-30b-a3b                              (30B nano)
nvidia/nemotron-3-nano-30b-a3b:free                         (free tier)
nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free          (reasoning)
nemotron-3-ultra-free, nemotron-3-super-free                (short names)
nvidia/nemotron-nano-12b-v2-vl:free                         (vision-language)
nvidia/nemotron-nano-9b-v2:free                             (9B nano)
@cf/nvidia/nemotron-3-120b-a12b                             (Cloudflare)
@cf/nvidia/nvidia-nemotron-4-340b-instruct                  (via Cloudflare)
command-a-03-2025, command-a-reasoning-08-2025              (Cohere)
command-r-08-2024, command-r-plus-08-2024                   (Cohere legacy)
z-ai/glm-5.1                                                (GLM 5.1)
z-ai/glm-4.5-air:free, z-ai/glm-4.7-flash                  (GLM tiers)
zai-glm-4.7, glm-4.7-flash, glm-4.5-flash, glm-4.6v-flash  (short names)
openai/gpt-oss-120b, gpt-oss-120b, @cf/openai/gpt-oss-120b (120B OSS)
openai/gpt-oss-120b:free, openai/gpt-oss-20b:free          (free tiers)
openai/gpt-oss-20b, openai/gpt-oss-safeguard-20b           (20B variants)
openai/gpt-4.1                                              (GPT-4.1)
gpt-4o, openai-fast                                         (classic + fast)
groq/compound, groq/compound-mini                           (Groq compound)
big-pickle                                                  (community)
@cf/google/gemma-4-26b-a4b-it                               (Gemma 4 via CF)
google/gemma-4-31b-it, gemma-4-31b-it, gemma4:31b           (Gemma 4 31B)
google/gemma-4-26b-a4b-it:free                              (Gemma 4 26B free)
@cf/ibm-granite/granite-4.0-h-micro                         (IBM Granite)
openrouter/owl-alpha                                        (OpenRouter)
poolside/laguna-m.1:free, poolside/laguna-xs.2:free         (Poolside)
liquid/lfm-2.5-1.2b-instruct:free                           (Liquid 1.2B)
liquid/lfm-2.5-1.2b-thinking:free                           (Liquid thinking)
nousresearch/hermes-3-llama-3.1-405b:free                   (Hermes 3 405B)
stepfun/step-3.7-flash:free                                 (StepFun)
cognitivecomputations/dolphin-mistral-24b-venice-edition:free (Dolphin)
cogito-2.1:671b                                             (Cogito)
mimo-v2.5-free                                              (MiMo free)
```

---

### fcc-server (1130 Models)

**Admin UI:** `http://localhost:8082/admin`  
**Client:** `fcc-claude "your prompt"`  
**Config:** `~/.fcc/.env`

The Free Claude Code server routes requests across 1130 models from 12+ providers:

| Provider | Models | Config Key |
|----------|--------|------------|
| DeepSeek | Full DeepSeek catalog | `DEEPSEEK_API_KEY` |
| OpenRouter | 200+ community/open models | `OPENROUTER_API_KEY` |
| Mistral | Mistral + Codestral + Devstral | `MISTRAL_API_KEY`, `CODESTRAL_API_KEY` |
| Moonshot (Kimi) | Kimi K2 and family | `KIMI_API_KEY` |
| Wafer | Anthropic-compatible models | `WAFER_API_KEY` |
| NVIDIA NIM | Enterprise NIM catalog | `NVIDIA_NIM_API_KEY` |
| OpenCode | OpenCode Zen + Go | `OPENCODE_API_KEY` |
| Fireworks | Fast serverless (default) | `FIREWORKS_API_KEY` |
| Groq | Ultra-low latency | `GROQ_API_KEY` |
| Google | Gemini models | `GEMINI_API_KEY` |

**How to switch models:** Open `http://localhost:8082/admin` → select provider + model → done.

---

## Agent Frameworks — In-Depth

### Swarms v13.0.0

**Binary:** `swarms`  
**Location:** `/home/aditya/.local/bin/swarms`  
**Install:** `pipx install swarms`  
**Purpose:** Multi-agent orchestration framework for coordinating swarms of AI agents.

```
╭─  👾 Swarms  ────────────────────────────────────────────────╮
│  ▄     ▄    Swarms  v13.0.0                                  │
│  ▀█████▀    Groq +3 more · Multi-Agent Framework             │
╰──────────────────────────────────────────────────────────────╯
```

**Use cases:**
- **Parallel code review** — spawn 5 agents to review different parts of a PR simultaneously
- **Multi-agent research** — one agent searches, another synthesizes, a third critiques
- **Hierarchical task execution** — manager agent decomposes tasks, worker agents execute
- **Ensemble reasoning** — multiple models vote on the best answer
- **Automated testing** — agents generate, run, and analyze test results in parallel

---

### NeoAgent v2.4.3

**Binary:** `neoagent`  
**Location:** `/usr/local/bin/neoagent`  
**Install:** `npm install -g neoagent`  
**Purpose:** AutoGPT-style autonomous agent — set a goal, it plans and executes independently.

```
Usage: neoagent <command> [args]
```

**Use cases:**
- **Long-running autonomous tasks** — "research the best architecture for this project and write a proposal"
- **Recursive self-improvement** — agent reflects on its output, identifies gaps, and iterates
- **Complex workflow automation** — multi-step pipelines with decision points and branching
- **Data collection and analysis** — scrape, clean, analyze, and report without hand-holding

---

### MiMo-Code

**Binary:** `mimo`  
**Location:** `/usr/local/bin/mimo`  
**Install:** `npm install -g @mimo-ai/cli`  
**Purpose:** AI coding assistant with native internet access via the MiMo platform.

```
█▀▄▀█ █ █▄ ▄█ █▀▀█ █▀▀ █▀▀█ █▀▀▄ █▀▀▀
```

**Use cases:**
- **Code generation with live context** — reads web docs, API references, and Stack Overflow in real time
- **API integration** — understands live API docs and generates correct integration code
- **Documentation research** — searches the web, reads docs, and generates summaries
- **Multi-modal coding** — supports MiMo's free tier (`mimo-v2.5-free`) through the proxy

---

### Hermes Agent v0.15.2 (Nous Research)

**Binaries:** `hermes`, `hermes-acp`, `hermes-agent`  
**Location:** `/home/aditya/.local/bin/hermes`  
**Install:** `pipx install hermes-agent`  
**Purpose:** Self-improving AI agent with a built-in learning loop.

```
Hermes Agent v0.15.2 (2026.5.29.2)
Project: .../hermes-agent
Python: 3.14.4
OpenAI SDK: 2.24.0
Up to date
```

**Key capabilities:**
- **Learning loop** — creates skills from experience, improves them during use, persists knowledge across sessions
- **Multi-platform** — Telegram, Discord, Slack, WhatsApp, Signal, and CLI from a single gateway
- **Scheduled automations** — built-in cron scheduler for daily reports, nightly backups, weekly audits
- **Subagent delegation** — spawn isolated subagents for parallel workstreams
- **Voice memo transcription** — across all platforms
- **Persistent memory** — FTS5 session search, LLM summarization, Honcho dialectic user modeling
- **Three terminal backends** — local, Docker, SSH, plus serverless (Modal, Daytona)
- **Any model** — OpenRouter, NVIDIA, MiMo, Hugging Face, Google, OpenAI, or custom endpoints

---

### Free Claude Code (fcc-claude)

**Binary:** `fcc-claude`  
**Location:** `/home/aditya/.local/bin/fcc-claude`  
**Purpose:** Claude Code CLI with any model backend.

**How it works:**
1. `fcc-server` runs on port 8082, managing 1130 models across 12 providers
2. `fcc-claude "prompt"` sends requests through the server
3. Server routes to the selected provider/model
4. Switch models anytime via the admin UI at `http://localhost:8082/admin`

**Use cases:**
- Full Claude Code experience without paying for Claude API
- Swap between DeepSeek, Mistral, Gemini, Kimi, and 1000+ others
- Test the same prompt across different models to compare outputs
- Use Claude Code's tool-use and file-editing capabilities with any backend

---

### Mistral Vibe CLI v2.15.0

**Binaries:** `vibe`, `vibe-acp`  
**Location:** `/home/aditya/.local/bin/vibe`  
**Config:** `~/.vibe/.env` (API key stored)  
**Purpose:** Mistral's agentic coding CLI with ACP (Agent Communication Protocol) support.

**Use cases:**
- **AI-native coding** — describe what you want, Vibe builds it
- **ACP agent communication** — agents talk to each other through the ACP protocol
- **Autonomous programming** — Vibe plans, codes, tests, and iterates without hand-holding
- **Multi-agent coordination** — Vibe-acp enables agent-to-agent handoffs

---

## Internet Access Layer — Agent-Reach v1.5

**Binary:** `agent-reach`  
**Location:** `/home/aditya/.local/bin/agent-reach`  
**Install:** `pipx install agent-reach`  
**Purpose:** Gives any AI agent full internet access across 13 platforms.

```
usage: agent-reach {setup,install,configure,doctor,uninstall,skill,format,transcribe,check-update,watch,version}
```

| Subcommand | Purpose |
|------------|---------|
| `setup` | Interactive configuration wizard |
| `install` | One-shot installer with flags |
| `configure` | Set config values or auto-extract from browser |
| `doctor` | Platform availability diagnostics |
| `uninstall` | Remove all config, tokens, and skills |
| `skill` | Manage agent skill registration |
| `format` | Clean and format platform API output |
| `transcribe` | Transcribe audio/video content |
| `check-update` | Check for new versions |
| `watch` | Monitor platforms for changes |

**Platform coverage:**

| Platform | Access | Configuration |
|----------|--------|---------------|
| 🌐 **Web pages** | Read any URL | None needed |
| 📺 **YouTube** | Subtitle extraction + video search | None needed |
| 📡 **RSS/Atom** | Read any feed | None needed |
| 🐙 **GitHub** | Repos, issues, PRs, discussions | None needed |
| 🐦 **Twitter/X** | Read/search (via Nitter) | Optional cookie |
| 💬 **Reddit** | Read/search | Optional cookie |
| 📕 **Xiaohongshu** | Content reading | Cookie config |
| 📺 **Bilibili** | Video content & subtitles | Cookie config |
| 🎵 **Douyin** | Content reading | Cookie config |
| 🎤 **Xiaoyuzhou** | Podcast transcriptions | Cookie config |
| 📺 **YouTube Music** | Audio extraction | None needed |

**Smart routing:** Each platform has "primary + fallback" backends. If one method gets blocked (e.g., yt-dlp banned by Bilibili), Agent-Reach transparently switches to the backup (bili-cli). Users experience zero downtime.

**Self-diagnosis:** `agent-reach doctor` scans every platform and reports which ones work, which need configuration, and exactly how to fix them.

---

## Agent Skills — Complete Catalog of 50+

The skills system is the agent's toolbox — each skill is a self-contained instruction set the agent loads on demand for specific tasks. Skills are lazy-loaded (only read when needed), saving tokens on every session.

### Engineering Skills (12)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `diagnose` | Disciplined debugging — reproduce → minimise → hypothesise → instrument → fix → reg-test | Hard bugs, crashes, performance regressions |
| `tdd` | Red-green-refactor test-driven development | Building features with tests, fixing bugs |
| `review` | Dual-axis code review (Standards + Spec) | PR review, branch review, WIP review |
| `prototype` | Throwaway prototypes — terminal app or UI variations | Exploring designs, sanity-checking data models |
| `improve-codebase-architecture` | Refactoring, consolidation, AI-navigability | Improving codebase structure |
| `migrate-to-shoehorn` | Migrate `as` assertions to `@total-typescript/shoehorn` | Type safety improvements |
| `scaffold-exercises` | Create exercise + solution + explainer structures | Course creation, tutorials |
| `request-refactor-plan` | Detailed refactor plans with incremental commits | Safe refactoring |
| `zoom-out` | Broader context and higher-level perspective | Unfamiliar code, onboarding |
| `caveman` | Ultra-compressed communication (-75% tokens) | Token-constrained sessions |
| `git-guardrails-claude-code` | Block dangerous git commands | Git safety |
| `setup-pre-commit` | Husky + lint-staged + typecheck + tests | Project initialization |

### Design & Visualization Skills (6)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `design-an-interface` | Multiple radically different interface designs | API design, module interfaces |
| `html` | Self-contained HTML — reports, explainers, comparisons, decks | Any deliverable as HTML |
| `html-diagram` | Full-screen SVG architecture diagrams | System visualization |
| `html-plan` | Visually organized plan pages | Project plans, roadmaps |
| `high-end-visual-design` | Premium/enterprise design patterns | Client-facing work |
| `industrial-brutalist-ui` | Raw, structural design aesthetics | Experimental UI |
| `minimalist-ui` | Clean, content-first design | Production UI |

### Writing & Communication Skills (6)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `edit-article` | Restructure, clarify, tighten prose | Editing drafts |
| `writing-beats` | Narrative journey composition | Article writing |
| `writing-fragments` | Mine raw material for future articles | Ideation |
| `writing-shape` | Shape raw material into publishable form | Drafting |
| `teach` | Structured skill instruction | Tutorials, onboarding |
| `ubiquitous-language` | Extract DDD domain glossary | Domain modeling |

### Strategy & Planning Skills (5)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `grill-me` | Stress-test plans through relentless questioning | Planning, decision-making |
| `grill-with-docs` | Challenge plans against domain model + ADRs | Strategic planning |
| `to-issues` | Break plans into vertical-slice GitHub issues | Implementation breakdown |
| `to-prd` | Convert conversation to PRD on issue tracker | Requirements documentation |
| `triage` | Full issue triage state machine | Backlog management |

### Product Management Skills (4)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `qa` | Interactive bug reporting → GitHub issues | Bug tracking |
| `handoff` | Compact conversation for agent switch | Session handoff |
| `setup-matt-pocock-skills` | Configure skill system for new repo | Project onboarding |
| `write-a-skill` | Create new agent skills | Skill authorship |

### Design System Skills (12 from taste-skill)

| Skill | Purpose |
|-------|---------|
| `brandkit` | Brand identity creation |
| `design-taste-frontend` | Taste-driven frontend design |
| `design-taste-frontend-v1` | Alternative taste design |
| `full-output-enforcement` | Prevent truncated output |
| `gpt-taste` | Taste-aware content generation |
| `image-to-code` | Design-to-code conversion |
| `imagegen-frontend-mobile` | Mobile image generation |
| `imagegen-frontend-web` | Web image generation |
| `redesign-existing-projects` | Interface redesign |
| `stitch-design-taste` | Combine design systems |
| `taste-skill` | Complete taste plugin (10+ sub-skills) |

### Utility Skills (5)

| Skill | Purpose |
|-------|---------|
| `obsidian-vault` | Obsidian note management |
| `setup-matt-pocock-skills` | Configure repo for engineering skills |
| `setup-pre-commit` | Add pre-commit hooks to a project |
| `full-output-enforcement` | Ensure complete, non-truncated output |
| `caveman` | Ultra-compressed token-saving mode |

---

## Agent Memory — ChromaDB Vector Database

The vector database is the agent's persistent brain — it stores semantic embeddings of all 13 knowledge modules so the agent can find relevant information in milliseconds without re-reading files.

**Location:** `memory/vector_db/`  
**Backend:** ChromaDB (persistent, embedded)  
**Dashboard:** FastAPI server on port 8083  
**Seeding:** `make seed` or `python3 tools/seed_vector_db.py`

**How it works:**
1. Each module file is split into chunks (by section/paragraph)
2. Each chunk is embedded and stored in ChromaDB with metadata (source file, section name)
3. The agent queries: "find chunks related to 'token optimization'" → vector similarity search
4. ChromaDB returns the most relevant chunks in milliseconds
5. Agent reads only those chunks — saves reading entire files

**Auto-update mechanism:**
- `post-commit` hook: re-seeds DB when module files change
- `post-merge` hook: re-seeds DB when pull brings module changes
- Content-hash dedup: unchanged files are skipped (saves time and API calls)

**Distributed memory bank:**
| Component | Purpose | Access Pattern |
|-----------|---------|----------------|
| ChromaDB vector storage | Semantic search across all modules | Agent queries by topic |
| `memory-bank/` | Session-level progress tracking | Agent reads at start of session |
| `LESSONS_LEARNED.md` | Cross-project error memory | Agent reads before every task |
| `memory-search` tool | CLI wrapper for vector search | `memory-search "query"` |

---

## Shell Environment — Every Tool Explained

Every terminal session is optimized for agent productivity with modern CLI replacements.

### Command Replacements

| Legacy | Modern | Benefit | Token Savings |
|--------|--------|---------|---------------|
| `ls` | `eza --icons` | Color-coded, icons, git status, tree view | ~40% less output |
| `cat` | `bat --style=plain` | Syntax highlighting, line numbers, git integration | ~30% less output |
| `grep` | `rg` (ripgrep) | 10x faster, recursive by default, .gitignore-aware | ~50% less output |
| `find` | `fd` | 5x faster, intuitive syntax, .gitignore-aware | ~40% less output |
| `du` | `dust` | Visual bar chart, top-N sorting, human-readable | ~60% less output |
| `ps` | `procs` | Color-coded, tree view, Docker-aware, searchable | ~50% less output |
| `top` | `btop` | GPU support, mouse support, themes, graphs | ~70% less output |
| `sed` | `sd` | Regex find-replace, in-place with preview | ~30% less output |
| `cd` | `z` (zoxide) | Fuzzy-match frequent dirs, learns your patterns | Saves full cd commands |
| `git diff` | `git diff \| delta` | Syntax highlighting, word-level diffs, side-by-side | ~40% less output |

### Interactive Tools

| Tool | Purpose | How It Works |
|------|---------|--------------|
| `fzf` | Fuzzy finder | Ctrl+T for file search, Ctrl+R for history search, Alt+C for cd |
| `zoxide` | Smart cd | `z proj` → jumps to `/home/.../project`, learns from usage |
| `starship` | Prompt | Fast, minimal prompt with git status, runtime version, timing |
| `tmux` | Terminal multiplexer | Persistent sessions, split panes, detach/reattach |
| `lazygit` | Git TUI | Visual git interface — stage, commit, branch, merge, rebase |
| `atuin` | Shell history | Encrypted sync across machines, fuzzy search, stats |
| `direnv` | Per-directory env | Auto-loads `.envrc` when entering a directory |
| `glow` | Markdown reader | Renders markdown in terminal with formatting and tables |

### Productivity Aliases

| Alias | Expands To | Purpose |
|-------|-----------|---------|
| `v` | `nvim` | Neovim editor |
| `gl` | `lazygit` | Git TUI |
| `bat` | `batcat` | Syntax-highlighted cat |
| `readme` | `glow` | Markdown reading |
| `cr` | `cargo run` | Rust compile+run |
| `cb` | `cargo build` | Rust compile |
| `ct` | `cargo test` | Rust test |
| `cc` | `cargo check` | Rust check |
| `dim` | `brightnessctl set 30%` | Dim screen (battery) |
| `bright` | `brightnessctl set 80%` | Bright screen |
| `battery-status` | `upower ...` | Battery health |
| `gpu-off` | `prime-select intel` | Max battery mode |
| `gpu-on` | `prime-select nvidia` | Performance mode |
| `cyberchef` | Open CyberChef | Encoding/decoding tool |

### Agent Read Cache

Two bash functions that prevent re-reading the same file:

```bash
mark-read /path/to/file   # Mark file as read
is-read /path/to/file     # Check if already read → skip
```

Hooks into `.bashrc` — agents check `is-read` before reading any file. If the file is cached, it's skipped entirely.

---

## Automated GitHub Project Creation

The system is pre-configured to streamline new project creation on GitHub:

**1. Pre-authenticated `gh` CLI:**
```bash
[credential "https://github.com"]
    helper = !/usr/bin/gh auth git-credential
```
GitHub authentication is handled transparently through the `gh` CLI — no manual token entry needed.

**2. GPG-signed commits:**
Every commit is automatically signed with the RSA 4096 GPG key (`0027EFBE3F4CD520`). GitHub displays ✅ Verified badges on all commits.

**3. Git defaults optimized for GitHub:**
```ini
[init]
    defaultBranch = main          # No "master" → rename step needed
[commit]
    gpgsign = true                # Every commit signed automatically
[color]
    ui = auto                     # Colored git output
```

**4. Creating a new project:**
With all infrastructure in place, creating a GitHub project is a one-liner:
```bash
mkdir my-project && cd my-project
git init
gh repo create my-project --private --source=. --remote=origin --push
```

The result:
- Local repo initialized with `main` branch
- GitHub repo created (private or public)
- GPG-signed initial commit pushed
- `gh` handles authentication transparently

**5. Project creation via agent:**
Agents can create GitHub projects autonomously:
```bash
opencode run "scaffold a Next.js project called my-app, create a GitHub repo for it, and push the initial commit"
```
All credentials, signing, and configuration are pre-wired — no manual steps.

---

## Architecture — How Everything Connects

```
                          ┌─────────────────────────────────────────────┐
                          │              THE USER                       │
                          │    (CLI / Telegram / VS Code / Browser)      │
                          └─────────────────────┬───────────────────────┘
                                                │
                          ┌─────────────────────▼───────────────────────┐
                          │           AGENT PROCESS LAYER               │
                          │                                            │
                          │  ┌──────────┐ ┌──────────┐ ┌────────────┐ │
                          │  │ Claude   │ │ Gemini   │ │ OpenCode   │ │
                          │  │ Code     │ │ CLI      │ │ Agent      │ │
                          │  └────┬─────┘ └────┬─────┘ └─────┬──────┘ │
                          │       │             │             │        │
                          │       └──────┬──────┘─────────────┘        │
                          │              │                             │
                          │              ▼                             │
                          │  ┌─────────────────────────────────────┐   │
                          │  │         AGENTS.md (GEMINI.md)        │   │
                          │  │  ~100 token startup · 6 rules · all │   │
                          │  │  behavioral directives               │   │
                          │  └────────────────┬────────────────────┘   │
                          └───────────────────┼────────────────────────┘
                                              │
            ┌─────────────────────────────────┼─────────────────────────────┐
            │                                 │                             │
            ▼                                 ▼                             ▼
  ┌─────────────────────┐     ┌──────────────────────────┐     ┌──────────────────────┐
  │  KNOWLEDGE LAYER    │     │   TOOL INFRASTRUCTURE    │     │   SKILL LAYER        │
  │                     │     │                          │     │                      │
  │  ┌───────────────┐  │     │  ┌────────────────────┐  │     │  ┌────────────────┐  │
  │  │ 13 Modules    │  │     │  │ freellmapi :3001   │  │     │  │ 46 Skills      │  │
  │  │ (2100 lines)  │  │     │  │ 2.7B tokens/mo     │  │     │  │ (lazy loaded)  │  │
  │  └───────┬───────┘  │     │  │ 90+ models         │  │     │  └────────────────┘  │
  │          │          │     │  └────────────────────┘  │     │                      │
  │          ▼          │     │                          │     │                      │
  │  ┌───────────────┐  │     │  ┌────────────────────┐  │     │                      │
  │  │ ChromaDB      │  │     │  │ fcc-server :8082   │  │     │                      │
  │  │ Vector Search │  │     │  │ 1130 models        │  │     │                      │
  │  │ (port 8083)   │  │     │  └────────────────────┘  │     │                      │
  │  └───────┬───────┘  │     │                          │     │                      │
  │          │          │     │  ┌────────────────────┐  │     │                      │
  │          ▼          │     │  │ Agent-Reach        │  │     │                      │
  │  ┌───────────────┐  │     │  │ Internet Access    │  │     │                      │
  │  │ LESSONS       │  │     │  └────────────────────┘  │     │                      │
  │  │ _LEARNED.md   │  │     │                          │     │                      │
  │  └───────────────┘  │     │  ┌────────────────────┐  │     │                      │
  │                     │     │  │ Swarms · NeoAgent  │  │     │                      │
  │                     │     │  │ MiMo · Hermes      │  │     │                      │
  │                     │     │  │ fcc · Vibe         │  │     │                      │
  │                     │     │  └────────────────────┘  │     │                      │
  └─────────────────────┘     └──────────────────────────┘     └──────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────────┐
  │                        PERSISTENCE LAYER                                 │
  │                                                                          │
  │  ┌───────────────┐  ┌───────────────┐  ┌──────────────┐  ┌────────────┐  │
  │  │ dotfiles/     │  │ config/       │  │ .githooks/   │  │ .github/   │  │
  │  │ bashrc, git,  │  │ Aider, Cont.  │  │ pre-commit,  │  │ CI/CD,     │  │
  │  │ tmux, starship│  │ Editorconfig  │  │ post-merge,  │  │ Copilot    │  │
  │  └───────────────┘  └───────────────┘  │ post-commit  │  └────────────┘  │
  │                                        └──────────────┘                  │
  │  ┌───────────────┐  ┌───────────────┐  ┌──────────────────────────────┐  │
  │  │ Global Keys   │  │ SSH Keys      │  │ GPG Signing                  │  │
  │  │ 12 providers  │  │ Ed25519       │  │ RSA 4096 · All commits       │  │
  │  │ Auto-loaded   │  │ GitHub auth   │  │ ✅ Verified on GitHub        │  │
  │  └───────────────┘  └───────────────┘  └──────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
```

**Data flow:**
1. Agent starts → reads `GEMINI.md` (~100 tokens) → learns rules, tool locations, behavioral directives
2. Agent encounters task → matches to tool description in manifest → loads relevant skill on demand
3. Agent needs knowledge → queries ChromaDB vector database (milliseconds) → reads only relevant chunks
4. Agent needs LLM → sends request to freellmapi proxy → proxy routes through 12 providers → 2.7B free tokens
5. Agent needs model routing → uses fcc-server with 1130 model options
6. Agent needs internet → uses Agent-Reach for YouTube, Twitter, Reddit, RSS, web
7. Agent creates project → `gh` CLI creates GitHub repo, GPG signs the commit, `delta` renders diffs
8. Agent commits code → pre-commit hook validates UI quality, post-commit re-seeds vector DB
9. Agent pushes → CI pipeline scans for vulnerabilities and secrets
10. Next agent starts → reads `.agent-progress.md` → resumes without re-analysis

---

## Quick Start

| Step | Action |
|------|--------|
| 1 | `git clone https://github.com/adityashirsatrao007/MEMORY ~/Desktop/Projects/MEMORY` |
| 2 | Open **[SETUP.md](SETUP.md)** — copy the prompt block and paste into any AI agent |
| 3 | `source ~/Desktop/Projects/MEMORY/bin/session-start.sh ~/Desktop/Projects/MEMORY` |

The setup prompt auto-detects your OS (Linux, macOS, WSL2) and installs everything automatically: system packages, language runtimes, CLI tools, agent frameworks, vector database, shell configuration, and verification — with zero manual intervention.

---

## Platform Compatibility

| OS | Status | Notes |
|----|--------|-------|
| Linux (Ubuntu 24.04+) | ✅ Primary | Everything native. Fully tested. GPU support via NVIDIA/CUDA. |
| macOS (Sequoia+) | ✅ Supported | Requires Homebrew. Auto-detected by setup script. |
| Windows (WSL2) | ✅ Supported | Ubuntu 24.04 on WSL2. Docker Desktop for WSL. |

---

## License

Proprietary — © 2026 Aditya Shirsatrao. All rights reserved. See [LICENSE](LICENSE).

This repository is made publicly viewable **for portfolio/reference purposes only**. No license is granted to copy, clone, distribute, or use any content as AI training data.
