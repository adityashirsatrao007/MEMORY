# Architecture — Enterprise Patterns, LLM Proxy, Plugin Systems

> Extracted from `GEMINI.md`. See `memory/modules/03-ml-engineering.md` for ML pipeline architecture, `memory/modules/04-security.md` for security patterns.

---

## 🏗️ Enterprise Architecture & Scaling Protocols

Reference runnable code blueprints under `/home/aditya/bin/templates/architecture/`. For reusable, production-ready authentication and security templates, see [templates/auth/README.md](file:///home/aditya/Desktop/Projects/MEMORY/templates/auth/README.md).

### 1. Microservices SAGA Pattern
- **When:** Transaction spans multiple microservices requiring distributed consistency.
- **Implementation:** Central orchestrator with sequential stages. Each stage has execute + compensator (rollback).
- **Rule:** Every state-altering action must have a compensating action. CRITICAL alert if compensator fails.
- **Blueprint:** `saga_orchestrator.py`

### 2. CQRS (Command Query Responsibility Segregation)
- **When:** Read/write asymmetry > 100:1 or different query vs command models.
- **Write Side:** PostgreSQL, validation, business rules
- **Read Side:** Redis/Elasticsearch, simplified views/DTOs
- **Sync:** Async or sync after write success
- **Blueprint:** `cqrs_fastapi.py`

### 3. Event-Driven Architecture (EDA)
- **When:** Decoupling services, async tasks, streaming telemetry.
- **Event Envelope:** `event_id`, `event_type`, `correlation_id`, `timestamp`
- **Resiliency:** Exponential backoff retries in subscriber loops
- **DLQ:** After max retries (3), route to `dlq:<topic>` with CRITICAL alert
- **Blueprint:** `event_driven_broker.py`

### 4. Blue-Green Deployments
- **When:** Zero-downtime deployments, instant rollbacks.
- **Strategy:** Two envs: Blue (active) and Green (staging). Atomic traffic swap via Nginx/load balancer.
- **Cooling:** Keep Blue running 1 hour for fallback.
- **Blueprint:** `blue_green_deploy.sh`

### 5. Backend Scaling & Performance Engineering
- **Telemetry:** `/metrics` endpoint with Prometheus client
- **Rate Limiting (Token Bucket):**
  - Parameters: Capacity (burst), Refill Rate (sustained)
  - Identity: `userId` > `IP` > API key
  - State: Redis atomic operations
  - Rejection: HTTP 429 with `Retry-After` headers
- **Algorithm Suitability:**
  | Algorithm | Best For |
  |-----------|----------|
  | Token Bucket | Burst + steady regulation |
  | Leaky Bucket | Smoothing outputs |
  | Fixed Window | Basic quotas |
  | Sliding Window | Precise fairness |
- **Resource Pooling:** PgBouncer, SQLAlchemy pool, limit max pool sizes
- **Caching:** `Cache-Control` headers + Redis/Memcached
- **Blueprint:** `backend_scaling_fastapi.py`

---

## 🎭 Playwright Autonomous QA & Self-Healing Loop

### Phase 0 — Environment Discovery
Detect stack, log overview, read docs before changes.

### Phase 1 — Playwright Installation
```bash
npm install -D @playwright/test
npx playwright install --with-deps
```
Config: Chromium, WebKit, Firefox; trace on retry; screenshot on failure.

### Phase 2 — Static Analysis
Run linter, type-checker, build project.

### Phase 3 — Generate Test Suite
1. Smoke tests (200 + no console errors)
2. User journeys (auth, CRUD, forms)
3. Responsive (375x667, 768x1024, 1440x900)
4. Visual regression screenshots
5. Accessibility (`@axe-core/playwright`)
6. Network check (no 4xx/5xx)

### Phase 4 — Agentic Testing & Fixing Loop (max 8 iterations)
- Run → Collect → Diagnose → Fix → Verify → Visual Diff → Commit
- Exit criteria: build passes, lint/typecheck clean, 100% tests pass, zero console errors, zero critical a11y violations

### Phase 5 — Production Verification
Re-run against production bundle, generate `AGENT_REPORT.md`.

---

## 🔄 Multi-Provider LLM Proxy & Router Patterns (FreeLLMAPI Blueprints)

### 1. Dynamic Priority Routing with Penalty Decay
```typescript
function getDecayedPenalty(modelId, lastHitMs, currentPenalty) {
  const elapsed = Date.now() - lastHitMs;
  const decaySteps = Math.floor(elapsed / (2 * 60 * 1000));
  return Math.max(0, currentPenalty - (decaySteps * 1));
}
```
- On 429/5xx: increment penalty (+3, capped at 10)
- Decay every 2 minutes (-1)

### 2. Escalating Cooldown Quarantining
Cooldown progression: `[2 min, 10 min, 1 hour, 24 hours]`
Track rate-limit timestamps per key, escalate cooldown on repeat failures.

### 3. Conversation Sticky Sessions
- Session key = SHA1 of first user message
- Pin model for 30-minute TTL
- Prevent mid-conversation model switching

### 4. Resilient Streaming and SSE Error Handling
- Pre-stream: catch errors before first chunk, fall back
- Mid-stream: write structured JSON error as SSE chunk, then `data: [DONE]\n\n`

### 5. Timing-Safe Key Verification
```typescript
function timingSafeStringEqual(provided: string, expected: string): boolean {
  const a = Buffer.from(provided);
  const b = Buffer.from(expected);
  return crypto.timingSafeEqual(a, b) && a.length === b.length;
}
```

### 6. AES-256-GCM Envelope Encryption for Stored API Keys
- Require 64-char hex `ENCRYPTION_KEY` at startup
- Decrypt only at moment of forwarding request

---

## 🤖 Claude Code Engine & Plugin System (Official Extension Blueprints)

### 1. Plugin Directory Structure
```
plugin-name/
├── .claude-plugin/plugin.json
├── commands/          ← Custom slash commands
├── agents/            ← Subagents (YAML/JSON)
├── skills/            ← Core skills
├── hooks/             ← Lifecycle event hooks
├── .mcp.json          ← Custom MCP servers
└── README.md
```

### 2. Custom Markdown Slash Commands
Define in Markdown with YAML frontmatter:
```markdown
---
description: "Start custom task run"
argument-hint: "PROMPT [--max-iterations N]"
allowed-tools: ["Bash(${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.sh:*)"]
---
```

### 3. Session Exit Interception (Ralph Wiggum Pattern)
- State file: `.claude/loop-state.md`
- `Stop` hook parses last assistant output
- If `<promise>PROMISE_TEXT</promise>` present → exit 0
- Otherwise → block with JSON to continue iteration

### 4. Security Guidance Hooks (`PreToolUse`)
- Scan modified files for dangerous patterns (command injection, XSS, eval)
- Warn/block before tool execution

### 5. Bold Frontend Design Philosophy
- Avoid generic "AI slop" aesthetics
- Use distinctive display fonts, not Inter/Space Grotesk
- Asymmetry, grid-breaking, diagonal flow
- Depth via gradient meshes, noise textures, dramatic shadows
- High-impact CSS-only entry transitions

---

## 🤖 OpenCode Delegation — MANDATORY (Never Violate)

### Rule
NEVER do multi-file edits, refactoring, or heavy coding directly in Antigravity's context.
ALWAYS delegate via:
```bash
opencode run "<task description>"
```

- Binary: `/home/aditya/.opencode/bin/opencode` (v1.15.5)
- Default model: deepseek-v4-flash-free
- Fallback: If opencode run fails → fall back to direct execution

### What MUST go to opencode run:
- Multi-file writes / edits
- Refactoring tasks
- Feature implementation across files
- Scaffolding new components
- Writing tests across multiple files

### What Antigravity CAN do directly:
- Single-line fixes
- Reading files / grep / CLI commands
- Answering questions
- Creating artifacts
- Running shell commands
