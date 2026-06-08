## 🐙 GitHub Project Standards (Auto-Applied to Every Repo)

When the agent creates or initializes a GitHub repo, it MUST create these files and configure rules automatically:
- **PR Template:** Copy `/home/aditya/bin/templates/git/pull_request_template.md` to `.github/PULL_REQUEST_TEMPLATE.md`
- **Bug Issue Template:** Copy `/home/aditya/bin/templates/git/bug_report.md` to `.github/ISSUE_TEMPLATE/bug_report.md`
- **Feature Issue Template:** Copy `/home/aditya/bin/templates/git/feature_request.md` to `.github/ISSUE_TEMPLATE/feature_request.md`

### Branch Protection Rules (apply via `gh` CLI after repo creation):
```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":0}' \
  --field restrictions=null
```

---

## ⚡ Makefile Standards (Every Project Gets This)

Every project Makefile MUST include these universal targets at minimum:

```makefile
.PHONY: dev build test lint typecheck ci clean setup

setup:        ## Install all dependencies
	bun install || pip install -r requirements.txt

dev:          ## Start development server
	bun run dev || uvicorn main:app --reload

build:        ## Production build
	bun run build

test:         ## Run all tests
	bun test || pytest -v

lint:         ## Run linter
	bunx eslint . || ruff check .

typecheck:    ## Run type checker
	bunx tsc --noEmit || mypy .

ci:           ## Full CI pipeline (lint + typecheck + test)
	make lint && make typecheck && make test

clean:        ## Remove build artifacts
	rm -rf .next dist build __pycache__ .pytest_cache node_modules

deploy:       ## Deploy to production
	vercel --prod || fly deploy
```

---

## 🪝 Pre-commit Hooks (Auto-installed on Every Project)

The agent MUST install `pre-commit` hooks on every new project via `setup-project`. Hooks run automatically before every `git commit` — zero manual effort.

To initialize, copy the standard config template from `/home/aditya/bin/templates/git/pre-commit-config.yaml` to `.pre-commit-config.yaml` in the project root, then run: `pre-commit install`.

---

## 🗂️ Dotfiles Repo (Disaster Recovery)

All personal configs are version controlled at `github.com/adityashirsatrao007/dotfiles`.
If the machine is ever wiped, the agent restores everything with one command.

### What is backed up:
- `~/.bashrc`, `~/.bash_aliases`
- `~/.config/starship.toml`
- `~/.config/opencode/`
- `~/bin/` (all custom scripts including `sync-agent-rules`, `setup-project`)
- `~/.tmux.conf`
- `/home/aditya/Desktop/Projects/GEMINI.md`

### Agent behaviour:
- When modifying any dotfile or adding a new script to `~/bin/`, the agent MUST commit and push to the dotfiles repo immediately after.
- Command: `cd ~/dotfiles && git add -A && git commit -m "update: <what changed>" && git push`


---

## 🤖 Vibe Coding Tool Stack & Agent Orchestration

### 1. Local Coding Agents & CLI Assistants
These are the zero-token-cost local AI coding agents installed and configured on this machine:
- **`aider`** ([aider-chat/aider](file:///home/aditya/Desktop/Projects/GEMINI.md#L1195)) — Git-first AI pair programmer for terminal. Ideal for fast multi-file edits. Run: `aider --model ollama/qwen2.5-coder:3b`
- **`goose`** ([block/goose](https://github.com/block/goose)) — Open-source on-machine AI agent via MCP. Extensible for custom workflows.
- **`opencode`** — Already configured. AGENTS.md points to GEMINI.md.
- **`RA.Aid`** ([ai-christianson/RA.Aid](https://github.com/ai-christianson/RA.Aid)) — LangGraph-powered CLI agent designed to execute multi-step coding goals.
- **`MyCoder.ai`** ([drivecore/mycoder](https://github.com/drivecore/mycoder)) — Modular CLI agent with native GitHub integration.
- **`Gemini CLI`** ([google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)) — Official Google Gemini terminal assistant.
- **`claude-code`** ([anthropics/claude-code](https://github.com/anthropics/claude-code)) — Official high-autonomy terminal agent by Anthropic.

### 2. AI-Driven Task & Multi-Agent Orchestration
When a project is too large for a single agent session, utilize these tools to coordinate:
- **`vibe-kanban`** ([BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban)) — Visual Kanban board to track and orchestrate 10+ parallel coding agents across projects.
- **`Claude Task Master`** ([eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master)) — Compatible with popular AI IDEs, breaks down work into subtasks to prevent context bloat.
- **`agent-hub`** ([Dominic789654/agent-hub](https://github.com/Dominic789654/agent-hub)) — Local-first multitask board for routing, sequencing, and observing repo-local coding agents.
- **`Bernstein`** ([chernistry/bernstein](https://github.com/chernistry/bernstein)) — Deterministic orchestrator that spawns parallel coding agents from a single goal, verifies with tests, and auto-commits.
- **`VibeGrid`** ([jcanizalez/vibegrid](https://github.com/jcanizalez/vibegrid)) — Multi-agent terminal manager with task queues and inline diff reviews.
- **`Boomerang Tasks`** — Roo Code feature that auto-decomposes goals into a structured queue of subtasks distributed across specialized agents.

### 3. Repository Auditing, Linting, & Health
AI-generated code needs checks to keep it clean and performant:
- **`AgentLint`** ([0xmariowu/AgentLint](https://github.com/0xmariowu/AgentLint)) — 33 evidence-backed checks for AI-friendly repos (verifies file structure, instruction quality, build setup, session continuity, and security posture).
- **`sober-coding`** ([mansourfaye229-dot/sober-coding](https://github.com/mansourfaye229-dot/sober-coding)) — Language-agnostic vibe code quality analyzer. Performs 27 checks across security (secrets, path traversal), architecture (god files, deep nesting), code duplication, and error handling. Provides sobriety scoring (SOBER, TIPSY, BLACKOUT) and CLI fix suggestions.
- **`toprank`** ([nowork-studio/toprank](https://github.com/nowork-studio/toprank)) — Open-source Claude Code plugin with 9 SEO and Google Ads skills to fetch PageSpeed/Search Console metrics and ship fixes directly.

### 4. Context & Cost Tracking
- **`Budi`** ([siropkin/budi](https://github.com/siropkin/budi)) — Local-first cost analytics for AI coding agents. Tracks token usage and spend across Claude Code and Cursor.
- **`memov`** ([memovai/memov](https://github.com/memovai/memov)) — Git-based, traceable memory layer for Claude Code to track session context.

### 5. Prompt & Documentation Engineering
- **`LynxPrompt`** ([GeiserX/LynxPrompt](https://github.com/GeiserX/LynxPrompt)) — Self-hostable AI config management platform for teams. Manages AGENTS.md, CLAUDE.md, .cursor/rules/, and slash commands.
- **`Prompt Tower`** ([backnotprop/prompt-tower](https://github.com/backnotprop/prompt-tower)) — Sends complex code blocks to LLMs, bundling files together for large-scale refactors.
- **`CodeGuide`** ([codeguide.dev](https://www.codeguide.dev/)) — Builds detailed, AI-readable project documentation before initiating an agent session.

### Agent Execution Rule for Complex Projects
When a project has more than 5 distinct components (e.g., frontend + backend + auth + DB + CI/CD):
1. Create a `tasks/` folder in the project root.
2. Write a `tasks/master-plan.md` breaking the project into numbered atomic tasks.
3. Launch parallel subagents, one per task group.
4. Update `memory-bank/progress.md` after each subagent completes.

---

## 🔍 Code Review & Documentation Protocol (Mandatory)

This protocol governs how the agent audits, reviews, and documents all changes before submitting work or pushing to GitHub.

### 1. Automated Code Quality Audits (Self-Healing Check)
Before declaring any task done, the agent MUST run the following checks and resolve all failures autonomously:
- **Sobriety Audit:** Run `sober check .` (or `sober-coding` command) to analyze code health. The codebase sobriety score must exceed `85`. If any issues are flagged as TIPSY, HUNGOVER, or BLACKOUT, the agent must fix them using `sober fix <ID>`.
- **AI-Friendliness Audit:** Run `agentlint check` (or similar command) to ensure the codebase remains readable, structured, and continuous for other agents.
- **Pre-commit Checks:** Run `pre-commit run --all-files` locally to verify that linters, formatters, and secret scans (`gitleaks`) pass successfully.
- **Unit Testing:** Execute `make test` or `bun test` and ensure all tests pass with zero failures.

### 2. Git & Pull Request Review Protocol
Before pushing branches or raising a Pull Request:
- **Review Diffs:** Run `git diff | delta` to visually inspect all changes. Verify that:
  1. No debugging statements, console logs, or temporary code markers are left.
  2. No credentials or secrets are present in the diff.
  3. No package lockfiles or node_modules are staged.
- **Diff Analysis:** For complex changes, run `reviewcerberus` (or similar Git diff reviewer) to perform a local security, performance, and quality analysis on the branch differences.
- **PR Description:** Write a clear description utilizing the `.github/PULL_REQUEST_TEMPLATE.md` conventions:
  - Reference Conventional Commits in the PR title (`feat:`, `fix:`, `docs:`, `refactor:`).
  - Explicitly document what was tested and provide instructions for manual verification.

### 3. Documentation & Memory Maintenance
- **Walkthrough Artifact:** For any major technical changes, create or update `docs/walkthrough.md` mapping the exact changes made, files modified, and test results.
- **CodeGuide Docs:** If initiating a new module or complex subsystem, run `codeguide` (or similar) to auto-generate AI-readable documentation of the architecture.
- **Memory Bank Sync:** Ensure `memory-bank/activeContext.md` and `memory-bank/progress.md` are updated to reflect the exact state, decisions, and immediate next steps.
- **Dotfiles Check:** If any change was made to the terminal environment or custom scripts in `~/bin/`, immediately push the updates to the dotfiles repository:
  ```bash
  cd ~/dotfiles && git add -A && git commit -m "update: terminal rules" && git push
  ```

---

## ⚡ ZERO-TOKEN CLI OPERATION RULEBOOK (MANDATORY — READ BEFORE EVERY ACTION)

This section defines the EXACT CLI tool to use for every operation. Using the wrong tool wastes tokens. This is non-negotiable.

