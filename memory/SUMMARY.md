# Anthropic Research & Engineering — Knowledge Summary

> Last updated: 2026-06-23 — Integrated into MEMORY modules (see §Strategic Relevance below)

---

## Models & Product Lineup

| Model | Type | Context | Notes |
|-------|------|---------|-------|
| **Claude 4 Sonnet** | Flagship | 200K | Anthropic's most intelligent model. Top of the reasoning/agents frontier. |
| **Claude 3.5 Haiku** | Fast/cheap | 200K | Cost-optimized for classification, routing, non-reasoning tasks. |
| **Claude 4 Opus** | Coming | — | Mentioned as "incoming". No confirmed date. |

**Key differentiators vs GPT-4o, Gemini 2.5 Pro:**
- Claude 4 Sonnet leads on reasoning, math, coding benchmarks at similar cost
- 200K context window across all models
- Computer use (beta): models can "see" screens, move cursor, click, type
- Strong safety architecture (constitutional AI, interpretability tools)

**Known gaps vs competitors:**
- No native multimodal image generation (vs Gemini/GPT-4o)
- No native video understanding (vs Gemini)
- No full-agent platform outside Claude Code (vs ChatGPT Tasks/Gemini Agents)
- No live web search natively within Claude chat (Projects can fetch — narrower)

---

## Research Papers

### 1. Teaching Claude Why (2026-06-12)
[Paper](https://www.anthropic.com/research/teaching-claude-why) | [PDF](https://anthropic-2025-teaching-claude-why.s3.us-east-1.amazonaws.com/teaching-claude-why.pdf)

**What:** Fine-tuning models to output intermediate reasoning traces that train-time supervision can use to teach model to reason before answering.

**Key findings:**
- Trained Claude to output reasoning in a scratchpad format
- Grade the intermediate reasoning for correctness to improve the model's reasoning capabilities
- Reasoning step supervision significantly improves logical consistency
- Mathematical problem-solving and multi-step reasoning get the biggest lifts
- Related to the "STaR" (Self-Taught Reasoner) line of work

**Production relevance:** Moat against pure RL-scaling approaches — reasoning transparency is a safety and debuggability advantage.

### 2. Recursive Self-Improvement — When AI Builds Itself (2026-05-31)
[Blog](https://www.anthropic.com/engineering/when-ai-builds-itself) | Repo: [Anthropic SEI](https://github.com/anthropics/SEI)

**What:** An end-to-end pipeline where Claude 4 Opus improves its own code and Claude 3.5 Sonnet generates training data. Validates that models can bootstrap their own improvements without human annotation at every step.

**Key findings:**
- Claude 4 Opus modified its own RL training code, Claude 3.5 Sonnet generated training examples
- Final system achieved 68% pass@1 on SWE-bench (from ~50% in earlier Claude 3.5 Sonnet baseline)
- Two-layer architecture: Improvement Agent (Opus) + Data Agent (Sonnet)
- Human stays in loop for approval of modifications via PRs
- Self-play loop where the model codes improvements, then those improvements are used to train the next checkpoint

**Limitations noted by authors:**
- Gains diminish after 3-4 iterations → capability ceiling
- Each self-play cycle carries misalignment risk if improvements "optimize for the wrong thing"
- Not yet an autonomous bootstrapping singularity — human oversight still essential

**Production relevance:** Suggests future where fine-tuning pipelines are partially automated. Human role shifts from generating data to approving PRs against training code.

### 3. Agentic Coding Expertise (late May 2026)
[Blog](https://www.anthropic.com/research/agentic-coding-expertise)

**What:** Study of how LLM-based coding agents' expertise evolves with iteration and feedback. Introduction of ExPO (Expertise via Preference Optimization) — a method for amplifying agent ability by steering toward successful trajectories.

**Key findings:**
- ExPO modifies agent behavior by optimizing toward trajectories that lead to test-passing
- Applied to Claude 3.5 Sonnet coding agent → significant improvement in task completion rate
- Analysis of "expertise emergence patterns": how agents learn planning, debugging, tool choice
- 3 evaluation paradigms: research IDE, SWE-bench, internal deployment tasks
- Expertise is not just about the model — scaffolding, tooling, feedback loops all matter

**Production relevance:** Framework for measuring and improving agent performance over time. Applied to Claude Code's internal development processes.

### 4. NLA (Natural Language Annotations)
[Blog](https://www.anthropic.com/research/nla)

**What:** Technique for teaching models to follow nuanced policy by annotating training data with structured natural language.

**Key findings:**
- Instead of labeling data with binary flags, annotate with natural language descriptions of desired behavior
- Allows models to internalize nuanced rules impossible to capture in simple labels
- Improved refusal behavior — fewer false positives/negatives on edge cases
- Particularly useful for content policy, safety guardrails, and style adherence

**Production relevance:** Powers Claude's nuanced refusal behavior and style consistency.

### 5. Clio — Claude insight
[Blog](https://www.anthropic.com/research/clio)

**What:** Privacy-preserving analytics system that automatically identifies and categorizes themes in Claude conversations.

**Key findings:**
- Clusters conversations by topic without storing raw conversation data
- Revealed surprising usage patterns: creative writing, resume tailoring, emotional support
- Used internally at Anthropic to understand how Claude is actually being used
- Privacy-preserving by design — no human reads raw conversations

**Production relevance:** Product roadmap input — features like Projects, Artifacts, and Styles were partially informed by Clio findings.

### 6. Interpretability & Safety Papers (Known)

| Paper | Year | Finding |
|-------|------|---------|
| **Golden Gate Claude** | 2024 | Localized interpretability — found a single feature for "Golden Gate Bridge" |
| **Scaling Monosemanticity** | 2024 | Extracted millions of interpretable features from Claude 3 Sonnet |
| **Constitutional AI** | 2022 | Training models to self-correct using principles (no RLHF needed for values) |

---

## Engineering Blog Posts

### 1. Effective Harnesses for Long-Running Agents (2026-04-18)
[Blog](https://www.anthropic.com/engineering/effective-harnesses-long-running-agents)

**What:** Design principles for agent harnesses — the scaffolding around the model that manages execution, tools, feedback, and recovery.

**Key insights:**
- **Trait 1: Interleaved agent + user control signals** — Agent can run autonomously but user can interject at any point. Real-time display of agent state keeps human in loop.
- **Trait 2: Multi-level instrumentation** — Harness must expose traces at granular level (tool calls, thought process, state transitions) for debugging and improvement.
- **Trait 3: Tool security boundary** — Tools run in sandboxed environments; agent proposes, harness dispatches.
- **Missing trait: Human approval before tool invocation** — Acknowledged as future work.
- All traits visible in Claude Code's design.

**Production relevance:** Directly informed Claude Code and Claude Agent SDK.

### 2. Advanced Tool Use (2025)
[Blog](https://www.anthropic.com/engineering/advanced-tool-use)

**What:** Training Claude to use tools effectively — the foundation of the agent ecosystem.

**Key insights:**
- Parallel tool calls (call multiple tools simultaneously)
- Tool choice strategies (force specific tool, let model decide)
- Structured tool outputs that Claude can reason over
- Chain-of-thought before tool use improves reliability

**Production relevance:** Powers Claude Code, MCP, and all agent tooling.

### 3. Building a C Compiler (2026-05-28)
[Blog](https://www.anthropic.com/engineering/building-c-compiler)

**What:** Full C compiler built using Claude Code in an autonomous loop over 30+ hours.

**Key insights:**
- Claude Code wrote a C compiler (subset of C23 → x86-64) via iterative autonomous development
- Started with lexer → parser → code gen → optimization → self-hosting attempts
- Converged on a ~30K LoC compiler producing correct x86-64 assembly
- Continuous agent loop with testing feedback at each compile-test cycle
- Self-hosting experiment: compiler failed to compile itself due to missing features (structs, unions, long long)
- Demonstrated that long-running agent loops can produce working systems from scratch

**Production relevance:** Validates the long-running agent paradigm. Shows both capability and current limits (self-hosting failure).

### 4. Demystifying Evals (2025-2026)
[Blog](https://www.anthropic.com/engineering/demystifying-evals)

**What:** Framework for designing and evaluating LLM evaluations — avoiding the "eval trap" where evals measure the wrong thing.

**Key insights:**
- **Avoid:**
  - Overfitting to eval benchmarks (teach to the test)
  - Using evals as targets rather than diagnostics
  - Over-relying on a single benchmark
- **Do:**
  - Design evals that measure the real-world capability you care about
  - Build eval suites that stress-test specific failure modes
  - Use evals to identify regressions, not to claim capability
- Introduced Claude's internal eval framework

**Production relevance:** Directly applicable to agent evaluation methodology.

### 5. Agent Skills (2026-06-01)
[Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

**What:** Framework for composing agent behaviors as reusable "skills" that combine prompts, tools, and validation. Used to extend Claude Code capabilities.

**Key insights:**
- Skills are composable units combining a prompt, a toolset, and validation criteria
- Claude Code ships with built-in skills (e.g., computer use, web search, code review)
- Skills can be authored declaratively and shared
- Skills solve the "incidental complexity" problem — agents don't need to figure out everything from scratch
- The skill architecture allows safe extension of agent capabilities without modifying core agent code

**Production relevance:** Directly maps to how skills work in Claude Code's ecosystem. Most mature instantiation of this capability.

### 6. Infrastructure Noise (2026-04-03)
[Blog](https://www.anthropic.com/engineering/infrastructure-noise)

**What:** Analysis of how infrastructure-level variability (Kubernetes scheduling, network latency, resource contention) impacts ML training reliability and how Anthropic addressed it.

**Key insights:**
- Identified "noise signatures" from infrastructure that cause training instability
- Built monitoring to distinguish infrastructure failures from model failures
- Developed automated recovery procedures for common infrastructure issues
- Noise reduction improved training reliability significantly

**Production relevance:** Lessons applicable to any large-scale ML training operation.

---

## Claude Code Ecosystem

### Core Information
- **CLI documentation**: [docs.anthropic.com/en/docs/claude-code/](https://docs.anthropic.com/en/docs/claude-code/overview)
- **Repo**: github.com/anthropics/claude-code (public — [issue #525 on README mentions repo is public](https://github.com/anthropics/claude-code/issues/525))
- **Capabilities**: Code editing, terminal commands, file management, git integration, web search, MCP tool integration, computer use (beta)
- **Slash commands**: /help, /doc, /permit, /clear, /compact, /cost, /settings, /doctor, /terminal-setup, /language, /model, /config, /diff-mode, /init
- **Settings**: JSON config file with profiles, per-project CLI detection & config reading, custom slash commands, skill & hook support
- **CLAUDE.md / AGENTS.md**: Per-project instructions files auto-read on session start
- **MCP**: Full MCP client — add stdio or streamable HTTP servers
- **Hooks**: Pre-tool, post-tool, stop, subagent stop, session start/end
- **Claude Code agents**: user-defined agents with separate instructions, tools, settings, and model. Use `/agent` to invoke.

### Ecosystem Components
| Component | Description |
|-----------|-------------|
| **Claude Code** | Terminal-based AI coding agent (CLI) |
| **Claude Code agents** | User-defined sub-agents with custom instructions & tools |
| **Claude Agent SDK** | Python/TypeScript SDK for building custom agent servers |
| **Managed Agents** | Anthropic-hosted agent platform (build, deploy, monitor) |
| **MCP** | Model Context Protocol — open standard for model-tool integration |
| **Claude Design** | Visual design tool integrated with Claude |
| **Skills** | Extensible capability bundles for Claude Code |

### Agent SDK
[Documentation](https://docs.anthropic.com/en/docs/claude-code/agent-sdk)

- Build custom agent servers in Python or TypeScript
- Agents communicate with Claude API through a protocol layer
- Supports: custom tools, multiple models, middleware, observability
- Use case: wrap internal tools, databases, or APIs as agent-accessible resources

### Managed Agents
[Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/managed-agents)

- Anthropic-hosted serverless agent platform
- Define agent configuration (model, tools, instructions) via API
- Can use MCP servers as tool providers
- Supports Claude 4 Sonnet and Claude 3.5 Haiku
- Hands-free execution without a UI

### MCP Protocol
- Open standard connecting models to tools/resources
- Client-server architecture: Anthropic hosts spec, many client implementations
- Growing ecosystem of community-built MCP servers

---

## Key URLs & Resources

### Research Pages
| Resource | URL |
|----------|-----|
| Research index | https://www.anthropic.com/research |
| Engineering blog | https://www.anthropic.com/engineering |
| Claude Code overview | https://docs.anthropic.com/en/docs/claude-code/overview |
| Agent SDK | https://docs.anthropic.com/en/docs/claude-code/agent-sdk |
| MCP spec | https://modelcontextprotocol.io |
| Claude API docs | https://docs.anthropic.com/en/docs |
| System status | https://status.anthropic.com |

### Key Papers
| Paper | URL |
|-------|-----|
| Teaching Claude Why | https://www.anthropic.com/research/teaching-claude-why |
| Recursive Self-Improvement (SEI) | https://www.anthropic.com/engineering/when-ai-builds-itself |
| Agentic Coding Expertise | https://www.anthropic.com/research/agentic-coding-expertise |
| NLA | https://www.anthropic.com/research/nla |
| Clio | https://www.anthropic.com/research/clio |
| Constitutional AI | https://www.anthropic.com/research/constitutional-ai |

### Engineering Posts
| Post | URL |
|------|-----|
| Effective Harnesses for Long-Running Agents | https://www.anthropic.com/engineering/effective-harnesses-long-running-agents |
| Advanced Tool Use | https://www.anthropic.com/engineering/advanced-tool-use |
| Building a C Compiler | https://www.anthropic.com/engineering/building-c-compiler |
| Demystifying Evals | https://www.anthropic.com/engineering/demystifying-evals |
| Agent Skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills |
| Infrastructure Noise | https://www.anthropic.com/engineering/infrastructure-noise |

### GitHub
| Repo | Description |
|------|-------------|
| github.com/anthropics/claude-code | Claude Code CLI (public) |
| github.com/anthropics/SEI | Self-Improving coding pipeline (public) |

---

## Strategic Context for MEMORY Project

### Integration Status (2026-06-23)

| Pattern | Source | Integrated In |
|---------|--------|--------------|
| Eval-first design gate | Demystifying Evals + Agentic Coding Expertise | `01-core-rules.md` (new section) + `16-agent-evals.md` |
| Skill composition (trigger + instructions + toolset + validation) | Agent Skills blog | `01-core-rules.md` (new section) + `16-agent-evals.md` §2 |
| Agent harness traits (interleaved control, instrumentation, security boundary) | Effective Harnesses | `01-core-rules.md` (Harness Self-Audit) + `16-agent-evals.md` §3 |
| Recursive self-improvement two-layer architecture | SEI pipeline | `16-agent-evals.md` §4 |
| Eval-as-diagnostic, eval-design lessons | Demystifying Evals | `14-lessons-learned.md` (lesson 14) |
| Eval catalog + `make evals` target | All of the above | `Makefile` + `16-agent-evals.md` §1 |

### Open Questions
1. Does Anthropic have a dedicated memory/state persistence system comparable to MEMORY's vector DB?
2. How does Claude Code's agent scaffolding compare to MEMORY's module architecture?
3. Are there Anthropic papers on long-term agent memory?
4. What is the concrete relationship between SEI-style self-improvement and MEMORY's experience logging?

---

## Next Steps for This Research

1. **Deeper on Claude Code architecture**: Dig into specific tool implementation patterns, explore the AGENTS.md/CLAUDE.md ecosystem, understand hook system fully
2. **Read SEI paper fully**: Pull the full paper from the PDF link
3. **Claude Design exploration**: Investigate the design tool capabilities
4. **Anthropic API pricing**: Document current pricing tiers
5. **Managed Agents deep-dive**: API, auth, deployment patterns
6. **Competitive mapping**: DeepSeek, OpenAI, Google/Gemini agent ecosystems side-by-side
