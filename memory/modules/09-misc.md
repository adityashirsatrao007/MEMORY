# Misc — Roadmaps, GitHub Tricks, OSM, AlgoTracker, Skills

> Extracted from `GEMINI.md`. Catch-all for sections not covered in other modules.

---

## 🗺️ AI Engineering Roadmap 2026 — 5-Month Production Track

> Philosophy: **Fundamentals → Retrieval → Agents → Production → Safety**

### ⚠️ Core Warning
- Do NOT touch LangChain until you've built RAG from primitives
- Do NOT skip foundation phase
- Prototypes ≠ Production. Production = traceability + observability + evals + rollback

### Month 1: Foundation
**Topics:** Python Mastery (async, decorators, types), Git + APIs + SQL, Docker, LLM Mechanics (tokens, embeddings), Raw API Integration
**Channels:** Corey Schafer, ArjanCodes, 3Blue1Brown, DeepLearning.AI, Krish Naik
**Courses:** Python for Everybody, AI for Everyone, Prompt Engineering

### Month 2: Core Skills & Infrastructure
**Topics:** RAG from scratch, Vector DBs (Pinecone/ChromaDB), GPU infra (Ollama/vLLM), Context Engineering, ReAct agent from scratch
**Channels:** Matthew Berman, James Briggs, AssemblyAI
**Courses:** Building Systems with ChatGPT API, Hugging Face course

### Month 3: Agentic AI & Orchestration
**Topics:** Multi-agent (CrewAI, LangGraph), Tool Use & Function Calling, MCP, Memory Architectures, Agent Evaluation
**Channels:** AI Jason, LangChain official, Simon Willison
**Courses:** DeepLearning.AI agent courses, LangGraph tutorials

### Month 4: Production MLOps
**Topics:** FSDP distributed training on K8s, LLMOps, Monitoring (Langfuse), Evals (RAGAS), Experiment Tracking (MLflow), CI/CD for AI, Scalable Serving (KServe), Semantic Caching
**Channels:** MLOps.community, Hugging Face, Unsloth, TechWorld with Nana
**Courses:** Hugging Face course, W&B learning, Terraform

### Month 5: Safety, Ethics & Governance (Ongoing)
- Prompt Injection, Jailbreaking, Data Privacy
- NeMo Guardrails, EU AI Act, Red Teaming
- **Resources:** Learn Prompting, Simon Willison, EU AI Act summaries

### 5-Month Compressed Plan
```
Month 1: Python + Git + API app + SQL + raw LLM calls
Month 2: RAG from scratch + vector DB + Ollama + ReAct agent
Month 3: Multi-agent + memory + tool use + MCP + evals
Month 4: FSDP on K8s + MLflow registry + Evidently + CI/CD
Month 5: Deploy full AI app + monitoring + safety + red-team
```

### Production MLOps Stack
| Tool | Phase | Purpose |
|------|-------|---------|
| Feast | 2 | Feature store |
| Great Expectations | 2 | Data validation |
| FSDP / DeepSpeed | 3 | Distributed training |
| Triton Inference Server | 4 | Model serving |
| Langfuse | 4 | LLM tracing |
| Evidently | 4 | Model monitoring |
| MLflow | 4 | Model registry |
| DVC | 4 | Data versioning |
| Prometheus + Grafana | 4 | Dashboards |

### Senior MLOps Pipeline Strategy
- DVC: Track datasets, map models to data versions
- MLflow Registry: Tag models as Staging/Production
- CT (Continuous Training): Data drift → auto-retraining
- NVIDIA Triton / ONNX: Export → serve on high-performance servers
- Evidently AI / Grafana: Live drift + latency monitoring

---

## 🐙 GitHub Power Tricks — Hidden Superpowers

### 1. GitMCP (gitmcp.io)
Convert any GitHub repo into AI-readable format.
Paste URL → GitMCP converts → Tell Claude/ChatGPT to analyze.

### 2. github.com → github.dev
Change domain: `github.com` → `github.dev` for browser VS Code.

### 3. Press `.` (Dot) on Any Repo
VS Code Web instantly. Same as `github.dev` but ninja shortcut.

### 4. Gitingest (gitingest.com)
Change URL: `github.com` → `gitingest.com`. Repo X-ray with architecture summary.

### 5. Direct ZIP Download
Append `/archive/refs/heads/main.zip` to any repo URL.

### 6. GitHub Search Dorking
| Query | What It Finds |
|-------|---------------|
| `language:javascript authentication` | JS auth implementations |
| `good first issue` | Beginner-friendly OSS issues |
| `stars:>1000 language:rust` | Popular Rust projects |

### 7. Repo Insights Tab
Contributor graph, code frequency, commit timeline, network graph.

### 8. GitHub Profile README
Create repo named after your username → becomes portfolio page.

### 9. Raw Code Clean View
Append `?plain=1` to GitHub file URL.

### Quick Reference
| Trick | How |
|-------|-----|
| Browser VS Code | `github.com` → `github.dev` OR press `.` |
| AI-readable repo | `github.com` → `gitmcp.io` |
| Repo X-ray | `github.com` → `gitingest.com` |
| ZIP download | Append `/archive/refs/heads/main.zip` |
| Clean raw code | Append `?plain=1` |
| Find beginner issues | `good first issue` search |

---

## 💰 Open-Source Monetization (OSM) Repository Index

| Original Repo | Tech Stack | Payout | User Fork |
|:---|---:|:---|:---|
| rudderlabs/rudder-server | Go, TypeScript | **$2,000** per bounty | OSM-rudder-server |
| Expensify/App | JS, Android/iOS | **$250-$500** per bounty | OSM-App |
| AppFlowy-IO/AppFlowy | Flutter, Rust | **$500/mo** (Mentorship) | OSM-AppFlowy |
| triggerdotdev/trigger.dev | Next.js, TS | **$50-$200** per bounty | OSM-trigger.dev |
| ether/etherpad-lite | JavaScript | **~$80** per bounty | OSM-etherpad-lite |
| BusKill/buskill-app | Shell, Python | **~$2,340** per bounty | OSM-buskill-app |
| oliexdev/openScale | Java, C++ | **~$30** per bounty | OSM-openScale |

### OSM Execution Protocol
1. Locate target fork
2. Read CONTRIBUTING.md before coding
3. Run setup autonomously (`bun install`, `pip install`, etc.)
4. Conventional commits: `fix(bounty-12): <description>`

---

## 📊 AlgoTracker — DSA Practice Platform

**URL:** [algotracker.in](https://www.algotracker.in)
**Creator:** Chandan Agrawal

### What It Is
Free web-based DSA practice tracker with:
- 800+ DSA problems organized by topic
- Blind75 curated list (2-week interview prep)
- LeetCode 150 list (1-2 month prep)
- SQL challenges, System Design (LLD & HLD)
- C++ solutions bundled
- Progress tracking (localStorage)

### How to Use
- **2 weeks to interview:** Blind75
- **1-2 months:** LeetCode150
- **Ongoing:** Systematic topic coverage

---

## 🎛️ Antigravity Awesome Skills Catalog & Installation Protocol

### Installation
```bash
npx antigravity-awesome-skills --claude     # → ~/.claude/skills/
npx antigravity-awesome-skills --gemini     # → ~/.gemini/skills/
npx antigravity-awesome-skills --cursor     # → ~/.cursor/skills/
npx antigravity-awesome-skills --antigravity # → ~/.agents/skills/
npx antigravity-awesome-skills --codex     # → ~/.codex/skills/
npx antigravity-awesome-skills --path <dir>
```

### Context Optimization
- Category filter: `--category development,backend,security,ai-ml`
- Risk exclusions: `--risk safe,none`
- Tag filters: `--tags debugging,typescript-`

### Trust & Safety
- `none`: Text-based reasoning only
- `safe`: Read-only actions
- `critical`: State-changing actions
- `offensive`: Pentesting/red-team
- `unknown`: Unclassified

### Curated Bundles
- **Web Wizard:** Radix UI, Tailwind, minimalist layouts
- **Hacker Pack:** OWASP, threat modeling, pentest
- **Product Pack:** Feature planning, copywriting, SEO
- **Essentials:** Clean code, debugging, TDD

---

## 📄 Standard Project Specification Templates

Place under `docs/`:
- **PRD:** Copy `/home/aditya/bin/templates/specs/PRD.md` to `docs/PRD.md`
- **DESIGNDOC:** Copy `/home/aditya/bin/templates/specs/DESIGNDOC.md` to `docs/DESIGNDOC.md`
- **TECHSTACK:** Copy `/home/aditya/bin/templates/specs/TECHSTACK.md` to `docs/TECHSTACK.md`
- **Claude Codes:** Use the prompt stacking cheat sheet at [$MEMORY_ROOT/templates/CLAUDE_CODES.md](file:///home/aditya/Desktop/Projects/MEMORY/templates/CLAUDE_CODES.md) for custom formatting, tones, and expert modules.
- **Quant Red Flag Analyst:** Use the system instructions at [$MEMORY_ROOT/templates/QUANT_RED_FLAG_ANALYST.md](file:///home/aditya/Desktop/Projects/MEMORY/templates/QUANT_RED_FLAG_ANALYST.md) for Bloomberg-style institutional financial terminal applications.



## Google Stitch API Frontend Protocol

The agent MUST fully utilize the Google Stitch API (`stitch` MCP server) for ALL frontend and UI generation tasks.

**Tools:** `generate_screen_from_text`, `create_design_system`, `edit_screens`, `generate_variants`

**Rule:** Never write UI from scratch. 100% utilization of Stitch API for building interfaces.

## Autonomous Permission Handling
If sandbox blocks a command, use `ask_permission` tool to request permanent exception. Do this autonomously.

## Autonomous Design Decisions (Vibe Coder)
Analyze project type, select perfect Aesthetic + Layout + Animation stack. Pass directives to Stitch API.

---

## 🏗️ Antigravity Infrastructure (local system)

### Port Reservation
| Port | Service | Status |
|------|---------|--------|
| 3001 | freellmapi API | PM2 - permanent |
| 5173 | freellmapi dashboard | dev |
| 8082 | MEMORY dashboard | optional |
| 8083 | MEMORY dashboard (alt) | optional |

### freellmapi Proxy (0-cost LLM)
**Always use freellmapi instead of direct provider APIs to save tokens.**
- Base URL: `http://localhost:3001/v1`
- Key: Load from `~/.config/global-apikeys/keys.env` (FREELLMAPI_KEY)
- Model: `auto` (auto-routes across 12 free providers)
- Auto-failover, 1.7B free tokens/month

### API Key Loading
```bash
source ~/.config/global-apikeys/load_keys.sh
```
Available keys: GROQ, MISTRAL, GEMINI, OPENROUTER, CEREBRAS, NVIDIA_NIM, HUGGINGFACE, OPENCODE, ZAI, DEEPSEEK, KIMI, FIREWORKS, WAFER, GITHUB, COHERE, CLOUDFLARE, FREELLMAPI

### Free Claude Code (fcc)
Free Claude Code routes Anthropic Messages API traffic from Claude Code to free/paid/local providers.
- Install: `curl -fsSL "https://github.com/Alishahryar1/free-claude-code/blob/main/scripts/install.sh?raw=1" | sh`
- Run proxy: `fcc-server`
- Use Claude: `fcc-claude`
- Admin UI: `http://localhost:8082/admin`
- Config through Admin UI (set provider key, model, etc.)
- Supports 17 providers: NVIDIA NIM, OpenRouter, Gemini, DeepSeek, Mistral, etc.

### Token Optimization Rules
1. Use freellmapi proxy for all LLM calls (0-cost)
2. Use local embedding (ChromaDB default = ONNX, free)
3. Never call direct Gemini/OpenAI APIs unless freellmapi is down
4. Use `vector DB first` — search before loading modules
5. Dashboard `/api/ask` routes through freellmapi (not Gemini)
