# Web Development — Projects, SEO & CODVYN

> Extracted from `GEMINI.md`. See `memory/modules/05-ui-ux.md` for design standards and library stack.

---

## 📁 Every New Project — Mandatory Setup

When creating any new project, the agent MUST run the local setup first and wait for explicit user approval before publishing/pushing to GitHub:

### Phase 1: Local Setup & Running
1. Create folder inside `/home/aditya/Desktop/Projects/<project-name>/`
2. `git init` inside the project folder
3. `git config init.defaultBranch main`
4. Run `/home/aditya/bin/setup-project /home/aditya/Desktop/Projects/<project-name>` — installs git hooks, .gitignore, .editorconfig, Makefile, and memory-bank docs templates.
5. Initialize the application server and run the development server (e.g. `pm2 start npm --name <project-name> -- run dev`).
6. Verify the server is running, and print the localhost URL (e.g. `http://localhost:<port>`) immediately.
7. **STOP & WAIT FOR APPROVAL:** Present the working local application. Do NOT push, create a GitHub repo, or upload anything.

### Phase 2: GitHub Publishing (Only AFTER explicit User approval)
8. Once the user approves:
   - **Crucial Authentication Rule:** Always use `env -u GITHUB_TOKEN gh ...` to prevent sandbox dummy tokens from overriding local credentials.
   - Run `env -u GITHUB_TOKEN gh repo create adityashirsatrao007/<project-name> --private --push --source=.`
   - Push the commits to the remote main tracking branch.

---

## 🖼️ README Images — Mandatory Storage Rule

When any image is used in a README (screenshots, demo GIFs, diagrams, logos):
1. **NEVER** use external image URLs
2. **NEVER** use absolute system paths
3. **ALWAYS** save into `docs/images/` inside the project folder
4. **ALWAYS** use a relative path in the README markdown

```
project/
├── docs/
│   └── images/
│       ├── screenshot-home.png
│       ├── demo.gif
│       └── architecture.png
└── README.md
```

Usage: `![Home Screen](docs/images/screenshot-home.png)`

---

## 🎨 CODVYN Workflow — Visual-First UI Development

> Stack: **Antigravity** (Browser Agent) + **Stitch** (UI Builder) + **Claude** (Prompt Refiner)
> Philosophy: Borrow the *look* from any site — keep the *functionality* from your own idea.

### How It Works (6 Steps)
```
01 Paste master prompt into Claude (design URL + raw idea)
02 Claude returns structured, Stitch-ready prompt
03 Paste into Antigravity: "start building and follow Codvyn"
04 Antigravity browses reference URL → extracts colors, fonts, spacing
05 Antigravity sends refined prompt to Stitch via MCP → builds UI
06 Review & iterate in Antigravity chat
```

### Step 1: Enable Browser in Antigravity
1. Settings → Integrations → Browser Tools → Toggle ON
2. Enable Screenshot capture, DOM inspection, External URL access

### Step 2: Connect Stitch via MCP
```bash
npm install -g @stitch/mcp-server
stitch-mcp --version
```

**Config (`~/.stitch/mcp-config.json`):**
```json
{
  "apiKey": "YOUR_STITCH_API_KEY",
  "projectId": "YOUR_PROJECT_ID",
  "port": 3456,
  "allowedOrigins": ["antigravity://app"]
}
```

**Start:** `stitch-mcp start --config ~/.stitch/mcp-config.json`

**Connect in Antigravity:** Settings → MCP Connections → Add New:
- Name: Stitch UI Builder
- URL: http://localhost:3456
- Protocol: MCP v1
- Auth: Bearer YOUR_STITCH_API_KEY

### Step 3: The Master Prompt
Fill two placeholders:
- `{DESIGN_REFERENCE_LINK}` — URL of site whose visual style to borrow
- `{RAW_PROMPT}` — Your rough idea for what you're building

The prompt tells Claude to:
1. Extract ONLY visual info from the reference link
2. Get features ONLY from the raw prompt
3. Output a structured Stitch-ready build prompt

### CODVYN Design Reference Examples
| Site | Aesthetic |
|------|-----------|
| `linear.app` | Dark, minimal, ultra-clean SaaS |
| `vercel.com` | Bold typography, high contrast |
| `stripe.com` | Premium, trustworthy |
| `apple.com` | Cinematic scroll, editorial |
| `leerob.io` | Minimalist personal/portfolio |

### When to Invoke CODVYN
User says: "build me a landing page", "make a dashboard", "design a website like X", "create a UI for..."

---

## 🌐 Complete Website SEO & Ranking Protocol (2026)

### 1. Google Search Console & Setup
- Register property immediately after deployment
- Verify ownership via DNS TXT records
- Submit `sitemap.xml` (auto-generated at build time)
- Ensure `robots.txt` points to correct sitemap

### 2. Technical SEO Essentials
- Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1
- 100% responsive, mobile-first
- HTTPS with clean redirect rules
- Clean, semantic URLs without excessive parameters

### 3. On-Page & Semantic SEO
- Exactly one `<h1>` per page, sequential `<h2>`–`<h3>`
- Unique `<title>` (<60 chars) and meta description (<160 chars)
- HTML5 semantic elements (`<article>`, `<section>`, `<nav>`, `<aside>`)
- Focus states, 48px+ tap targets, descriptive `alt` tags

### 4. Image & Asset Optimization
- WebP/AVIF format
- Descriptive hyphenated filenames
- Explicit `width` and `height` attributes

### 5. Backlinks & Promotion
- Blog posts, guest sharing, Product Hunt
- Low-quality/spam links strictly avoided

---

## Standard Project Specification Templates

When initiating a new project, place specs under `docs/`:
- **PRD:** Copy `/home/aditya/bin/templates/specs/PRD.md` to `docs/PRD.md`
- **DESIGNDOC:** Copy `/home/aditya/bin/templates/specs/DESIGNDOC.md` to `docs/DESIGNDOC.md`
- **TECHSTACK:** Copy `/home/aditya/bin/templates/specs/TECHSTACK.md` to `docs/TECHSTACK.md`

---

## 📄 PDF & Document Extraction Tools

> The agent MUST NEVER say "I cannot read PDFs".

### Installed Tools
| Tool | Command | What It Does |
|------|---------|-------------|
| `pdftotext` | `pdftotext input.pdf output.txt` | Extract text |
| `pdftoppm` | `pdftoppm -png -r 300 input.pdf output` | PDF → PNG images |
| `pdfimages` | `pdfimages -png input.pdf output` | Extract images |
| `tesseract` | `tesseract input.png output` | OCR for scans |

### Self-Healing Protocol for File Reading
1. PDF → `pdftotext "file.pdf" /tmp/extracted.txt`
2. Scanned PDF → `pdftoppm -png -r 300` then `tesseract`
3. Extract images → `pdfimages -png`
4. PDF to HTML → `pdftohtml`
5. PDF to markdown → `pandoc input.pdf -t markdown`
6. PDF info → `pdfinfo input.pdf`

---

## 🐙 GitHub Contribution (For External Repos)

- Always fork first: `gh repo fork <owner>/<repo> --clone --remote`
- Always check `CONTRIBUTING.md` before writing code
- Always check for duplicate issues/PRs
- Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`
- Never push to `main`/`master` of external repos directly
- Never submit PR with failing tests or lint errors
- Security bugs: never file as public issue — use private advisory

---

## 🐙 GitHub Project Standards (Auto-Applied to Every Repo)

When creating or initializing a GitHub repo:
- **PR Template:** Copy `/home/aditya/bin/templates/git/pull_request_template.md` to `.github/PULL_REQUEST_TEMPLATE.md`
- **Bug Report Template:** Copy `/home/aditya/bin/templates/git/bug_report.md` to `.github/ISSUE_TEMPLATE/bug_report.md`
- **Feature Request Template:** Copy `/home/aditya/bin/templates/git/feature_request.md` to `.github/ISSUE_TEMPLATE/feature_request.md`

### Branch Protection Rules
```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":0}' \
  --field restrictions=null
```

---

## ⚡ Makefile Standards

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

ci:           ## Full CI pipeline
	make lint && make typecheck && make test

clean:        ## Remove build artifacts
	rm -rf .next dist build __pycache__ .pytest_cache node_modules

deploy:       ## Deploy to production
	vercel --prod || fly deploy
```

---

## 🪝 Pre-commit Hooks

The agent MUST install `pre-commit` hooks on every new project via `setup-project`.
Copy config from `/home/aditya/bin/templates/git/pre-commit-config.yaml` to `.pre-commit-config.yaml`, then run: `pre-commit install`.

---

## 🗂️ Dotfiles Repo (Disaster Recovery)

All personal configs at `github.com/adityashirsatrao007/dotfiles`.

### What is backed up:
- `~/.bashrc`, `~/.bash_aliases`
- `~/.config/starship.toml`
- `~/.config/opencode/`
- `~/bin/` (all custom scripts)
- `~/.tmux.conf`
- `/home/aditya/Desktop/Projects/GEMINI.md`

### Agent behaviour:
- When modifying any dotfile or adding a script to `~/bin/`, commit and push immediately:
  ```bash
  cd ~/dotfiles && git add -A && git commit -m "update: <what changed>" && git push
  ```

---

## 🤖 Vibe Coding Tool Stack & Agent Orchestration

### 1. Local Coding Agents
- `aider` — Git-first AI pair programmer
- `goose` — Open-source on-machine agent via MCP
- `opencode` — Already configured
- `Gemini CLI` — Official Google Gemini terminal assistant
- `claude-code` — Official Anthropic terminal agent

### 2. Multi-Agent Orchestration
- `Claude Task Master` — Subtask decomposition

### 3. Repository Auditing
- `semgrep` — SAST + secrets detection
- `toprank` — SEO + Google Ads plugin

### 4. Prompt & Documentation Engineering
- `LynxPrompt` — AI config management
- `CodeGuide` — AI-readable project docs

### Agent Execution Rule for Complex Projects
If >5 components: create `tasks/master-plan.md`, launch parallel subagents, update `memory-bank/progress.md` after each.
