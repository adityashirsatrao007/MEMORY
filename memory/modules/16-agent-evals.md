# Agent Evals, Skill Composition & Harness Design

> Patterns distilled from industry research. These are design principles for MEMORY's own architecture, not dependencies.

---

## 1. Eval Methodology — Design Evals as Diagnostics, Not Targets

### Core Principles (from "Demystifying Evals")

| Principle | Application in MEMORY |
|-----------|----------------------|
| Evals measure real capabilities, not benchmark scores | Each module should have a concrete capability it enables (not "lines of docs") |
| Evals are diagnostics, not targets | Use evals to find regressions, not to claim quality |
| Never overfit to eval benchmarks | Don't optimize module structure for `make validate` — optimize for agent efficacy |
| Build eval suites that stress-test specific failure modes | Each module should identify its failure mode (e.g., 01-core-rules failure = agent asks permission instead of acting) |

### Eval-First Design Gate (MANDATORY)

Before adding ANY new module, rule, or tool to MEMORY:
```bash
# 1. Define success criteria: "What specific agent behavior does this improve?"
# 2. Define regression test: "How do I know if this breaks?"
# 3. Define measurement: "What metric proves it works?"
# 4. Only then: implement.
```

### MEMORY Eval Catalog

| Eval | What It Measures | How to Run |
|------|-----------------|------------|
| Module validation | All modules exist with >= 10 lines of content | `make validate` |
| Vector DB coverage | Every module is searchable via ChromaDB | `make seed` then `curl localhost:8082/api/search?q=<key phrase>` |
| Tool availability | All documented CLI tools are installed | `for tool in $(rg "^#+ \`(.+)\`" memory/modules/ -o --no-filename \| sort -u); do which $tool &>/dev/null \|\| echo MISSING: $tool; done` |
| Session handoff quality | .agent-progress.md written at session end | `test -f .agent-progress.md` |
| Cross-module consistency | No contradicting rules across modules | `rg "NEVER\|ALWAYS\|MANDATORY" memory/modules/*.md` — review conflicts |
| Skill description quality | Every skill has a meaningful trigger description | `rg "^description:" .agents/skills/*/SKILL.md \| grep -i "documentation and guidelines for"` — flag generic stubs |

---

## 2. Agent Skill Composition Pattern

### Anatomy of a Skill

Every skill in MEMORY should follow this structure:

```
Skill = Trigger + Instructions + Toolset + Validation
```

| Component | Description | Example |
|-----------|-------------|---------|
| **Trigger** | When this skill activates | `rg -i "<keyword>"` match on user message, or explicit user invocation |
| **Instructions** | What the agent should do | Step-by-step procedure, guardrails, edge cases |
| **Toolset** | What tools are needed | Bash, Read, Write, specific CLI tools |
| **Validation** | How to verify the skill worked | Output format check, exit code, test command |

### Skill Quality Gates

Before creating/editing a skill, verify:

1. **Trigger is specific** — Does it match the right requests and avoid false positives?
2. **Instructions are actionable** — Can a fresh agent execute them without asking questions?
3. **Toolset is bounded** — Does the skill restrict dangerous tools?
4. **Validation exists** — How does the agent know the skill worked?

### Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Trigger too broad | Matches noise, wastes context | Narrow to specific keywords or regex |
| Instructions assume prior context | Agent has no memory of earlier turns | Self-contained instructions |
| No validation step | Agent declares success but output is wrong | Add explicit check at end |
| Toolset unlisted | Agent uses wrong tools for the task | List exact tools in instructions |

---

## 3. Agent Harness Design Principles (from Anthropic's "Effective Harnesses")

### Three Essential Traits

Every agent harness (the scaffolding around the model) should have:

```
Trait 1: Interleaved Agent + User Control
  - Agent runs autonomously for well-scoped subtasks
  - User can interject at any point
  - Agent displays state in real-time (tool calls, reasoning, progress)
  → MEMORY: session handoff, .agent-progress.md, make session-end

Trait 2: Multi-Level Instrumentation
  - Agent actions are traceable at granular level
  - Tool calls, state transitions, and outputs are logged
  - Traces are inspectable for debugging and improvement
  → MEMORY: tools/handoff, error-logs.md, lessons-learned.md

Trait 3: Tool Security Boundary
  - Tools run in sandboxed/dispatched environments
  - Agent proposes actions, harness dispatches them
  - Dangerous operations require approval or have rollback
  → MEMORY: guardrails at ~/bin/guardrails/, opencode delegation
```

### Harness Self-Audit

Before running any multi-step agent task, check:
- [ ] Can user interject? (session handoff exists)
- [ ] Are tool calls traceable? (output captured)
- [ ] Are dangerous tools sandboxed? (guardrails active)
- [ ] Is there a rollback plan? (git, undo, restore)
- [ ] Are resource limits set? (timeout, token budget)

---

## 4. Recursive Self-Improvement Pattern

### Two-Layer Architecture (from Anthropic SEI)

```
Layer 1: Improvement Agent (senior model)
  - Reviews current system architecture
  - Proposes specific improvements
  - Generates PR with changes

Layer 2: Data/Execution Agent (junior model)
  - Generates training data or test cases
  - Runs validation and verification
  - Reports results

Human Gate: PR approval between cycles
  - Review proposed changes
  - Accept or reject
  - Merge and trigger next cycle
```

### Application to MEMORY

MEMORY already has this pattern:
- **Improvement Agent**: This agent (loading modules, making changes)
- **Data Agent**: `make validate + make seed` (verification + vector DB)
- **Human Gate**: User reviews changes before commit

**Enhancement**: Formalize the improvement loop:
```bash
# Self-improvement cycle:
# 1. make validate         — check current state
# 2. <make changes>        — improve modules
# 3. rg "TODO|FIXME|HACK"  — find remaining issues
# 4. make validate         — verify changes
# 5. make seed             — propagate to vector DB
# 6. git diff --stat       — review scope
# 7. user approval         — human gate
```

### Diminishing Returns Awareness

Self-improvement cycles produce diminishing returns after 3-4 iterations. Signs to stop iterating:
- Changes are cosmetic (wording, formatting)
- No new failure modes discovered
- Vector DB search returns same results before and after
- Module line count grows without new capability

---

## 5. Agent Expertise & Feedback Loops

### Expertise Emergence (from "Agentic Coding Expertise")

Agent expertise improves through:
1. **Scaffolding quality** — better tool definitions, clearer instructions
2. **Feedback loops** — capturing successes and failures
3. **Iteration** — repeated exposure to similar problems

### MEMORY's Feedback Architecture

```
Success Path:
  Task → Agent executes → Success → logs to progress.md
  No structural change needed.

Failure Path:
  Task → Agent fails → logs to 11-error-logs.md
  → Root cause analysis → 14-lessons-learned.md
  → If pattern repeats: update module or create new one

Optimization Path (ExPO-like):
  Session history → Identify successful trajectories
  → Extract reusable patterns → Encode in modules
  → Prune dead ends → Collapse over-specific rules
```

### Trajectory Pruning Rule

When a module exceeds 200 lines, audit for:
- Rules that have never been triggered (no grep match in 30 days)
- Redundant rules covered by newer modules
- Overly specific rules that should be collapsed
- Examples that should be in SUMMARY.md, not active rules
