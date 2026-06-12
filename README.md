> **Copyright (c) 2026 Aditya Shirsatrao. All rights reserved.**  
> Proprietary — see [LICENSE](LICENSE). No copying, cloning, or distribution without written permission.

# MEMORY — Agent Configuration & Cross-Device Setup

<p align="center">
  <strong>One-shot agent environment for AI-assisted development.</strong><br>
  Clone → paste one prompt → full agent toolchain on any machine.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-Proprietary-red.svg?style=for-the-badge" alt="License: Proprietary">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL2-ff69b4?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/LLM-Free%20Proxy%20(2.7B%20tokens%2Fmonth)-brightgreen?style=for-the-badge" alt="Free LLM proxy">
</p>

---

## Overview

MEMORY is a portable agent-environment configuration system. It packages everything an AI coding agent needs — shell config, CLI tools, vector database, LLM proxy, and 15+ agent-skills — into a single reproducible setup.

One `git clone` and one pasted prompt, and any machine becomes a full agent development environment.

---

## Features

- **Zero-cost LLM proxy** — 90+ models across 12 free providers, ~2.7B tokens/month combined free tier
- **Vector knowledge base** — ChromaDB-backed agent memory with semantic search
- **15+ integrated tools** — Swarms, NeoAgent, MiMo, Hermes, Agent-Reach, Free Claude Code, Mistral Vibe, and more
- **Cross-platform** — Linux, macOS, Windows (WSL2) from a single setup script
- **Agent skills** — 50+ reusable skills (diagnose, review, TDD, design, writing, PM, etc.)
- **Token-optimized** — Lazy mode (~70 tokens/session) for routine tasks, full mode (~1420 tokens) for complex work
- **Private & secure** — All cookies/keys stored locally, never uploaded

---

## Project Structure

```
MEMORY/
├── AGENTS.md                  Agent configuration & rules (loaded by all agents)
├── GEMINI.md                  Gemini-specific config (symlink target)
├── CLAUDE.md → GEMINI.md      Claude-specific config (symlink)
├── LICENSE                    Proprietary license
├── README.md                  This file
├── SETUP.md                   Full setup prompt for agents
├── Makefile                   Build: validate, seed, stats, hooks
│
├── memory/
│   ├── modules/               Knowledge base (13 module files)
│   ├── vector_db/             ChromaDB persistent storage
│   └── memory-bank/           Session progress tracking
│
├── tools/
│   ├── dashboard.py           ChromaDB dashboard (FastAPI, port 8083)
│   ├── seed_vector_db.py      Vector DB seeder with hash-based skip
│   └── validate_ui.py         UI design validation
│
├── config/
│   └── .aider.conf.yml        Aider configuration
│
├── .agents/skills/            50+ agent skills (installed)
├── dotfiles/                  Shell, git, starship, tmux configs
├── .githooks/                 Git hooks (auto-re-vector DB on commit)
└── .github/workflows/         CI workflow
```

---

## Tool Manifest

| Category | Tools |
|----------|-------|
| **LLM Proxy** | [freellmapi](http://localhost:3001/v1) — 90+ models, ~2.7B tokens/mo |
| **Model Router** | [fcc-server](http://localhost:8082/admin) — 1130 models, 12+ providers |
| **Agent Frameworks** | Swarms v13, NeoAgent v2.4, MiMo-Code, Hermes Agent v0.15 |
| **Internet Access** | Agent-Reach v1.5 (YouTube, Twitter, Reddit, RSS, web) |
| **Coding Agents** | Free Claude Code (fcc-claude), Mistral Vibe CLI |
| **AI Skills (50+)** | diagnose, review, TDD, prototype, handoff, html-plan, drawio, grill-me, edit-article, caveman, and more |

---

## Quick Start

| Step | Action |
|------|--------|
| 1 | `git clone https://github.com/adityashirsatrao007/MEMORY ~/Desktop/Projects/MEMORY` |
| 2 | Open **[SETUP.md](SETUP.md)** — copy the prompt block and paste into any AI agent |
| 3 | `source ~/Desktop/Projects/MEMORY/bin/session-start.sh ~/Desktop/Projects/MEMORY` |

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                      Agent Process                       │
│  (Claude / Gemini / OpenCode / Antigravity)              │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ AGENTS.md   │  │ Tool Manifest│  │ Agent Skills    │  │
│  │ (rules)     │  │ (manifest)   │  │ (50+)          │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                │                   │           │
│         ▼                ▼                   ▼           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              MEMORY Knowledge Base               │   │
│  │        (ChromaDB vector search, 13 modules)      │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │           freellmapi Proxy (port 3001)            │   │
│  │    90+ models · 12 providers · 2.7B tokens/mo     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

The agent reads `AGENTS.md` on startup (~100 tokens), loads the tool manifest only when needed (~400 tokens), and queries the vector DB for relevant knowledge. All LLM calls route through the local proxy to preserve API budget.

---

## Infrastructure

| Service | Port | Purpose |
|---------|------|---------|
| freellmapi proxy | 3001 | Zero-cost LLM routing (OpenAI-compatible) |
| fcc-server | 8082 | Model router for Free Claude Code (1130 models) |
| MEMORY Dashboard | 8083 | ChromaDB vector search UI |
| NeoAgent | 3333 | Autonomous agent process |

### freellmapi — Zero-Cost LLM Proxy

Routes all LLM calls through local providers instead of paid APIs. ~2.7B free tokens/month across 12 providers (Cloudflare, Google, Cohere, OpenAI-compat, and more).

| Detail | Value |
|--------|-------|
| **Endpoint** | `http://localhost:3001/v1` |
| **API key** | `freellmapi-c72bebe9578ae453d5d77b79af6e988e19405950c2087632` |
| **Models** | 90+ across Cloudflare, Google, Cohere, OpenAI-compat |
| **Auth header** | `Authorization: Bearer <key>` |
| **Chat endpoint** | `POST /v1/chat/completions` |
| **Dashboard** | Web UI at `http://localhost:3001` |
| **Failover** | Auto-routes to next provider on rate-limit or error |

The proxy automatically benches rate-limited keys and falls back to the next available provider. All API keys are stored in `~/.config/global-apikeys/keys.env` and loaded via `source ~/.config/global-apikeys/load_keys.sh`.

### fcc-server — Model Router

Free Claude Code server with 1130 models across 12+ providers.

| Detail | Value |
|--------|-------|
| **Admin UI** | `http://localhost:8082/admin` |
| **Client** | `fcc-claude <prompt>` |
| **Default provider** | Fireworks |
| **Config** | `~/.fcc/.env` |

---

## Platform Compatibility

| OS | Status | Notes |
|----|--------|-------|
| Linux (Ubuntu 24.04+) | ✅ Primary | Everything native |
| macOS (Sequoia+) | ✅ Supported | Requires Homebrew |
| Windows (WSL2) | ✅ Supported | Ubuntu 24.04 on WSL2 |

---

## License

Proprietary — © 2026 Aditya Shirsatrao. All rights reserved. See [LICENSE](LICENSE).

This repository is made publicly viewable **for portfolio/reference purposes only**. No license is granted to copy, clone, distribute, or use any content as AI training data.
