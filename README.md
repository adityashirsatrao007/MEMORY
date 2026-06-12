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
</p>

---

## Why MEMORY?

AI agents are useless without infrastructure. Every new machine means hours of setup — installing tools, configuring shells, hunting for API keys, wiring up models. MEMORY eliminates that entirely.

**One `git clone` + one pasted prompt = a production-ready agent workstation with:**

- 1200+ LLM models at **zero cost** (~2.7B free tokens/month)
- 7 integrated agent frameworks (Swarms, NeoAgent, MiMo, Hermes, FCC, Vibe, Agent-Reach)
- 50+ reusable AI skills (diagnose, review, TDD, prototype, html-plan, handoff, grill-me...)
- Persistent vector memory (ChromaDB)
- Pre-configured shell, git, tmux, starship
- Private — all keys and cookies stay local

**What would take a day to set up takes 60 seconds.**

---

## The Tools — What You Get

### 🔷 LLM Layer

#### freellmapi Proxy
Zero-cost unified LLM gateway. Routes every request through a smart failover chain across 12 free providers.

| Feature | Detail |
|---------|--------|
| **Endpoint** | `http://localhost:3001/v1` (OpenAI-compatible) |
| **Token budget** | ~2.7B free tokens/month combined across providers |
| **Model count** | 90+ models |
| **Failover** | Auto-bench rate-limited keys, fall through providers |
| **Providers** | Cloudflare, Google, Cohere, OpenAI-compat, Groq, Mistral, DeepSeek, Moonshot (Kimi), Z.AI, NVIDIA NIM, OpenRouter, Liquid |
| **Auth** | `Authorization: Bearer freellmapi-c72bebe9578ae453d5d77b79af6e988e19405950c2087632` |
| **Dashboard** | Web UI at `http://localhost:3001` |

**Highlight models available:**

| Model | Provider | Notes |
|-------|----------|-------|
| `deepseek-ai/deepseek-v4-flash` | DeepSeek | Flagship reasoning model |
| `deepseek-ai/deepseek-v4-pro` | DeepSeek | Pro reasoning, highest accuracy |
| `qwen/qwen3-coder-480b-a35b-instruct` | Qwen (Cloudflare) | 480B coding specialist |
| `gemini-2.5-flash` / `gemini-2.5-pro` | Google | Google's latest reasoning |
| `gemini-3.5-flash` | Google | Latest gen, high speed |
| `gemini-3.1-pro-preview` | Google | Preview of next-gen pro |
| `mistralai/mistral-large-3-675b-instruct-2512` | Mistral | 675B flagship |
| `minimaxai/minimax-m2.7` | MiniMax | Latest MiniMax model |
| `moonshotai/kimi-k2.6` | Moonshot/Kimi | Kimi's latest reasoning |
| `openai/gpt-oss-120b` | OpenAI-compat | 120B open-source variant |
| `openai/gpt-4.1` | OpenAI-compat | Latest GPT iteration |
| `meta/llama-4-maverick-17b-128e-instruct` | Meta (Cloudflare) | Llama 4 Maverick |
| `meta-llama/llama-4-scout-17b-16e-instruct` | Meta | Llama 4 Scout |
| `nvidia/nemotron-3-super-120b-a12b` | NVIDIA NIM | Enterprise reasoning |
| `nvidia/nemotron-3-ultra-550b-a55b` | NVIDIA NIM | Ultra-scale reasoning |
| `command-a-03-2025` | Cohere | Cohere's latest |
| `z-ai/glm-5.1` | Z.AI | GLM next-gen |
| `groq/compound` / `groq/compound-mini` | Groq | Ultra-low latency |
| `@cf/moonshotai/kimi-k2.6` | Cloudflare | Kimi via Cloudflare |

Every model auto-routes through the proxy. No API key management, no rate-limit babysitting, no cost tracking.

#### fcc-server (Free Claude Code Router)
1130 models across 12+ providers, one CLI.

| Feature | Detail |
|---------|--------|
| **Admin UI** | `http://localhost:8082/admin` |
| **Client** | `fcc-claude "your prompt"` |
| **Models** | 1130+ across 12+ providers |
| **Default** | Fireworks (fast, free) |
| **Config** | `~/.fcc/.env` — DeepSeek, OpenRouter, Mistral, Kimi, Wafer, NVIDIA, OpenCode |

Switches between Claude, Gemini, DeepSeek, Mistral, and 1000+ others from a single CLI. No vendor lock-in.

---

### 🔷 Agent Frameworks

#### Swarms v13.0.0
Multi-agent orchestration framework. Coordinate swarms of AI agents for complex tasks.

```
$ swarms --help
▄     ▄    Swarms  v13.0.0
▀█████▀    Groq +3 more · Multi-Agent Framework
```

**Use cases:** Parallel code review, multi-agent research, distributed task execution, agent hierarchies.

#### NeoAgent v2.4.3
AutoGPT-style autonomous agent. Give it a goal, it plans and executes independently.

```
$ neoagent --help
Usage: neoagent <command> [args]
```

**Use cases:** Long-running autonomous tasks, research workflows, recursive improvement loops.

#### MiMo-Code
Coding assistant with native internet access via the MiMo platform.

```
$ mimo --help
█▀▄▀█ █ █▄ ▄█ █▀▀█ █▀▀ █▀▀█ █▀▀▄ █▀▀▀
```

**Use cases:** Code generation with live web context, API integration, documentation research.

#### Hermes Agent v0.15.2 (Nous Research)
Self-improving AI agent with a built-in learning loop — creates skills from experience, improves them during use, persists knowledge across sessions.

```
$ hermes --version
Hermes Agent v0.15.2 (2026.5.29.2)
```

**Available binaries:** `hermes`, `hermes-acp`, `hermes-agent`

**Use cases:** Persistent assistant that learns your patterns, cross-platform (Telegram, Discord, Slack, WhatsApp, CLI), scheduled automations, subagent delegation.

#### Free Claude Code (fcc-claude)
Claude Code with any backend — swap between 1130 models.

```
$ fcc-claude "refactor this module"
```

**Use cases:** Full Claude Code experience without paying for Claude, model-agnostic coding assistant.

#### Mistral Vibe CLI v2.15.0
Mistral's agentic coding CLI with ACP support.

```
$ vibe --help
```

**Available binaries:** `vibe`, `vibe-acp`

**Use cases:** AI-native coding workflows, autonomous programming, agent-to-agent communication (ACP).

---

### 🔷 Internet Access Layer

#### Agent-Reach v1.5.0
Gives any AI agent full internet access — YouTube, Twitter, Reddit, Xiaohongshu, Bilibili, RSS, web pages, GitHub.

```
$ agent-reach --help
usage: agent-reach {setup,install,configure,doctor,uninstall,skill,format,transcribe,check-update,watch,version}
```

**Capabilities:**

| Platform | Access Type | Configuration |
|----------|-------------|---------------|
| Web pages | Read any URL | None |
| YouTube | Subtitles + video search | None |
| RSS/Atom | Read any feed | None |
| GitHub | Repos, issues, PRs | None |
| Twitter/X | Read/search (via Nitter) | Cookie config optional |
| Reddit | Read/search | Cookie config optional |
| Xiaohongshu | Content reading | Cookie config |
| Bilibili | Video content | Cookie config |
| Douyin | Content reading | Cookie config |

Built-in diagnostics: `agent-reach doctor` tells you exactly what works and what needs configuration.

**Use cases:** Let your agent research the web, summarize YouTube videos, monitor RSS feeds, scrape documentation, search social media — all from a single tool.

---

### 🔷 AI Skills (50+)

Pre-built agent capabilities, loaded on demand. Each skill is a self-contained instruction set the agent follows.

| Category | Skills |
|----------|--------|
| **Engineering** | `diagnose` — debug hard bugs · `tdd` — test-driven dev · `review` — code review · `prototype` — throwaway prototypes · `improve-codebase-architecture` — refactoring · `migrate-to-shoehorn` — type migration · `scaffold-exercises` — exercise stubs · `request-refactor-plan` — refactor RFCs |
| **Design** | `design-an-interface` — API design · `html` — self-contained HTML · `html-diagram` — SVG architecture maps · `html-plan` — visual plans · `drawio-skill` — draw.io diagrams |
| **Writing** | `edit-article` · `writing-beats` · `writing-fragments` · `writing-shape` · `teach` — skill authoring |
| **Strategy** | `grill-me` — stress-test plans · `grill-with-docs` — plan vs domain model · `zoom-out` — architecture context · `ubiquitous-language` — domain glossary |
| **PM** | `to-issues` · `to-prd` · `triage` · `qa` · `handoff` — agent handoff |
| **Utility** | `caveman` — ultra-compressed comms · `setup-matt-pocock-skills` · `setup-pre-commit` · `git-guardrails-claude-code` · `full-output-enforcement` · `obsidian-vault` |
| **Taste/UI** | `brandkit` · `gpt-taste` · `image-to-code` · `imagegen-frontend-mobile` · `imagegen-frontend-web` · `redesign-existing-projects` · `stitch-design-taste` · `high-end-visual-design` · `industrial-brutalist-ui` · `minimalist-ui` · `soft-ui` |

---

### 🔷 Agent Memory Layer

#### ChromaDB Vector Database
Persistent semantic memory with a FastAPI dashboard.

- **Storage:** `memory/vector_db/`
- **Dashboard:** `http://localhost:8083`
- **Seeding:** `make seed` (auto-skips unchanged files via content hash)
- **Search:** Agent queries relevant modules by semantic similarity
- **Auto-update:** Git hooks re-vector on every commit to `memory/modules/`

The agent doesn't need to re-read every knowledge file — it searches the vector DB for relevant context in milliseconds.

---

### 🔷 Shell & Environment

Pre-configured dotfiles that make any terminal productive instantly:

| Tool | Role | Alias |
|------|------|-------|
| `zoxide` | Smarter cd | `z` |
| `fzf` | Fuzzy finder | `ctrl+T` |
| `starship` | Prompt | Minimal, fast |
| `tmux` | Terminal multiplexer | Session management |
| `bat` | Cat with syntax | `cat` |
| `eza` | Modern ls | `ls`, `ll` |
| `fd` | Modern find | `find` |
| `ripgrep` | Fast grep | `grep` |
| `dust` | Disk usage | `du` |
| `btop` | System monitor | `top` |
| `procs` | Modern ps | `ps` |
| `sd` | Modern sed | `sed` |
| `lazygit` | Git TUI | `gl` |

---

## Quick Start

| Step | Action |
|------|--------|
| 1 | `git clone https://github.com/adityashirsatrao007/MEMORY ~/Desktop/Projects/MEMORY` |
| 2 | Open **[SETUP.md](SETUP.md)** — copy the prompt block and paste into any AI agent |
| 3 | `source ~/Desktop/Projects/MEMORY/bin/session-start.sh ~/Desktop/Projects/MEMORY` |

The setup prompt auto-detects your OS (Linux, macOS, WSL2) and installs everything: system packages, language runtimes, CLIs, agent tools, vector DB, shell config — with no manual intervention.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Agent Process                           │
│  (Claude Code / Gemini CLI / OpenCode / Antigravity)         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│  │ AGENTS.md   │  │ Tool Manifest    │  │ Agent Skills    │  │
│  │ ~100 tokens │  │ ~400 tokens      │  │ (50+, lazy)    │  │
│  └──────┬──────┘  └──────┬───────────┘  └───────┬────────┘  │
│         │                │                       │           │
│         ▼                ▼                       ▼           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ChromaDB Vector Brain                    │   │
│  │  (semantic search · 13 modules · auto-updated)       │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            freellmapi Proxy (port 3001)               │   │
│  │  90+ models · 12 providers · 2.7B tokens/month        │   │
│  │  Cloudflare · Google · Cohere · Groq · Mistral · ...  │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          fcc-server (port 8082)                       │   │
│  │  1130 models · Claude/DeepSeek/Mistral/Kimi/...      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Platform Compatibility

| OS | Status | Notes |
|----|--------|-------|
| Linux (Ubuntu 24.04+) | ✅ Primary | Everything native. Fully tested. |
| macOS (Sequoia+) | ✅ Supported | Requires Homebrew. Auto-detected. |
| Windows (WSL2) | ✅ Supported | Ubuntu 24.04 on WSL2. |

---

## Why This Exists

Setting up an AI development environment should not take a day. Every time you get a new machine, you should be productive in minutes, not hours. MEMORY is the result of hundreds of hours of configuration engineering — distilled into one reproducible setup.

**It solves:**
- ❌ "I need to install 30+ tools manually"
- ❌ "I don't know which API keys to configure"
- ❌ "My agent doesn't know about the tools on this machine"
- ❌ "I'm paying for tokens I could get for free"
- ❌ "My shell is useless without aliases and plugins"
- ❌ "I have no agent memory — every session starts from zero"

---

## Infrastructure Reference

| Service | Port | Purpose | Access |
|---------|------|---------|--------|
| freellmapi proxy | 3001 | Unified LLM gateway (OpenAI API) | `POST http://localhost:3001/v1/chat/completions` |
| freellmapi UI | 3001 | Model dashboard | `http://localhost:3001` |
| fcc-server | 8082 | Model router admin | `http://localhost:8082/admin` |
| MEMORY Dashboard | 8083 | ChromaDB vector search | `http://localhost:8083` |
| NeoAgent | 3333 | Autonomous agent | `neoagent` CLI |

All API keys auto-load from `~/.config/global-apikeys/keys.env`.

---

## License

Proprietary — © 2026 Aditya Shirsatrao. All rights reserved. See [LICENSE](LICENSE).

This repository is made publicly viewable **for portfolio/reference purposes only**. No license is granted to copy, clone, distribute, or use any content as AI training data.
