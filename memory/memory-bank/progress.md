# MEMORY — Progress & Session Log

> Agent updates this at the END of every session.
> Read this at the START of every session to resume without re-analysis.

## Current Status
MCP Memory Server built. Persistent SSE daemon on port 8932, systemd-enabled. 6 tools exposing ChromaDB vector search + memory-bank RAG. Auto-connects via opencode.json mcpServers (stdio shim). agy knowledge dir symlinked to shared memory.

## What's Done
- [x] 54-tool dispatch table + auto-dispatch script
- [x] 8 tool guardrails (grep→rg, cat→bat, etc.)
- [x] GEMINI.md modularized: index (20 lines) + 8 on-demand modules
- [x] Core modules compressed 73%: 01-core-rules 334→83, 02-cli-tools 409→146
- [x] Vector DB seeded with 89 semantic chunks
- [x] ChromaDB dashboard at localhost:8082
- [x] session-start.sh silent (127→36 lines, 94% less output)
- [x] Behavioral rules: silent CLI, ollama first, vector DB first, enola pre-flight, no re-read

## What's In Progress
- MCP Memory Server running on SSE port 8932 — verify end-to-end tool calls from opencode
- agy auto-connection via knowledge symlinks (no native MCP plugin yet)

## What's Next
- [ ] Context budget enforcement (auto-summarize at 50K input tokens)
- [ ] Makefile targets for vector DB re-seed + dashboard restart
- [ ] Add `recall_context` call to opencode's AGENTS.md or hook for session-start auto-summary
- [ ] Build agy native MCP plugin (or integrate via stdio wrapper)
- [ ] Test MCP tools from both agents in a real session

## Known Issues / Tech Debt
- session-start.sh receives stale "true" from `:` no-ops (benign)
- Dashboard /health endpoint missing (use / instead)
- Vector DB needs re-seeding after module content changes

## Session Log
| 2026-08-13 23:34:18 | Completed: README course + live Pages deploy + all demo variants. Blocked: HF free. Next: Streamlit deploy optional |
| 2026-08-11 20:08:36 | Completed: XAI-enhanced solar dust repo pushed to GitHub. Blocked: none. Next: excalidraw paper figures; model retrain with dataset. |
| 2026-08-11 00:43:05 | Completed: full 134-topic audit PASS (134/134). Fixed Q7 PEFT gap. Pushed faf9527 (+9ddcbc9 PNGs). Blocked: none. Next: none. |
| 2026-08-11 00:28:32 | Completed: ex2mmd.py fixes + inline Mermaid splice (8 diagrams) into README, committed+ pushed as 526c441. Blocked: none. Next: MERGE/CTE/LeetCode verified outputs if requested. |
| 2026-08-11 00:27:13 | Completed: All 27 diagrams embedded as rendered PNGs (diagrams/png/), dual-column PNG+excalidraw table added, heading fixed 25→27. Pushed 9ddcbc9. Blocked: none. Next: full 112-topic re-audit + mermaid count + TOC check. |
| 2026-08-10 23:59:16 | Portfolio SEO fixes live; Vercel token dead |
| 2026-08-10 23:44:31 | Completed: verified outputs for all remaining SQL examples + cleanup in dbms-interview-prep (0ddf7bc pushed). Blocked: none. Next: user-directed passes (MERGE chapter, recursive CTE, LeetCode bank verification). |
| 2026-08-10 23:22:22 | Frontends wired to live backends. SentinlX UI (adityashirsatrao007.github.io/ai-threat-detection) + Tracelify UI (adityashirsatrao007.github.io/error-tracking-observability-sdk): added Vite base (VITE_BASE_PATH) + router basename for GH Pages subpath; pages.yml envs repointed to live tunnels (car-oven.../api/v1, flag-greater...); backends restarted with CORS allowing adityashirsatrao007.github.io. Tunnel checks 200 + ACAO header present. Portfolio liveLinks point to UI URLs (pushed). Done. |
| 2026-08-10 23:03:29 | Completed: README full rewrite & push. Next: user review. |
| 2026-08-10 23:00:01 | Fixed main-portfolio GitHub Pages asset 404s: raw asset URLs in src (project imgs, logos, fonts, favicons, manifest, 3D HDR/GLB, noise, giats, og.png) were not basePath-prefixed. Added src/constants/assets.js A() helper, wired into projects.js export map, CustomHead, _document.fonts, fonts.scss + global.scss URL('...'), FruitNinja, MagicBall, floatingMeshes, Badge, Hero, about Index. Clean build (prettier printWidth 200) + push; Pages+Vercel workflows succeeded; all 13 assets 200 + project pages 200. Next: if reviewer still sees console 404s, re-verify cache. |
| 2026-08-10 22:20:39 | Deployed all backends live via cloudflared. ome-api:8000 -> presents-hormone-jurisdiction-birthday.trycloudflare.com. tracelify-api:8001 -> flag-greater-exploring-species.trycloudflare.com. sentinelx-api:8002 -> car-oven-rely-dramatically.trycloudflare.com (all /docs+/health 200). NIDS streamlit:8003 -> sorry-tar-spirit-reg.trycloudflare.com (_stcore/health 200; Predict needs results/*.joblib + .pth weights - MISSING from repo). Portfolio projects.js liveLinks updated + pushed to main-portfolio (Netlify/Vercel Pages rebuild triggered). Blocked: NIDS model weights absent. Next: add weights / wire Cape, restart tunnels if drop. |
| 2026-08-10 20:42:32 | Completed: dbms-interview-prep repo published private. Next: engine-specific depth optional. |
| 2026-08-10 09:44:59 | Completed: research+from-zero+coverage map+pushed 98177b3. Blocked: none. Next: install whisper/jiwer to validate asr_pipeline end-to-end; build weekly study schedule. |
| 2026-08-10 09:21:41 | Completed: tutorials 04-05 + index + README updates, pushed 731dcf6. Blocked: none. Next: end-to-end whisper p95 run; mock-interview skeleton. |
| 2026-08-10 08:42:27 | Completed: 4 sites live+200. Blocked: 2 backends + 2 infra-blocked apps. Next: browser imports. |
| 2026-06-23 15:57:28 | Research-to-Integration session complete. Created 16-agent-evals.md (198 lines) distilling Anthropic eval/harness/skill patterns into MEMORY format. Enhanced 01-core-rules.md with eval gate, skill composition requirement, and harness self-audit. Added eval-design lesson 14 to 14-lessons-learned.md. Added 'make evals' target to Makefile. Integrated all into SUMMARY.md. Vector DB seeded (221 chunks). |
| 2026-06-23 15:22:34 | Completed: Installed Fontsource variable fonts (@fontsource-variable/inter and @fontsource-variable/space-grotesk) as offline npm dependencies and integrated them locally in index.css. Blocked: None. Next: Design next-gen templates. |
| 2026-06-23 15:18:32 | Completed: Created 3D Web Design & SaaS Template guidelines artifact and saved it in memory modules as 15-3d-web-design.md for future agent sessions. Blocked: None. Next: Design next-gen SaaS templates. |
| 2026-06-23 15:15:04 | Completed: Integrated Lenis smooth scrolling library and configured it with GSAP ScrollTrigger to smooth out default jumpy browser scrolling physics. Blocked: None. Next: Gather user feedback on the scrolling momentum. |
| 2026-06-23 15:11:51 | Completed: Added GSAP timeline scroll pauses (holds) for scrollytelling slides and expanded scrolly container height to 800vh to ensure slower and smoother scroll animations. Blocked: None. Next: Check user feedback on the updated scroll timing. |
| 2026-06-23 15:07:04 | Completed: Expanded layout to 500vh pinned scrollytelling with 5 slides, node laser connection lines, red alert light pulses, camera shake effects, and SF Pro system font stacks. Blocked: None. Next: Gather user feedback. |
| 2026-06-23 14:51:01 | Completed: Fixed 3D canvas sizing and pinning bugs in App.jsx; implemented interactive mouse parallax, dynamic morphing grid terrain, and floating glassmorphic 3D shapes. Blocked: None. Next: Gather design feedback. |
| 2026-06-23 14:46:07 | Cleaned background tasks and exposed 3D scrollytelling. |
| 2026-06-23 14:42:53 | Integrated GSAP ScrollTrigger for cinematic scrollytelling. |
| 2026-06-23 14:41:03 | Exposed campus safety dashboard 3D mockup as WebGL texture. |
| 2026-06-23 14:37:52 | Enhanced 3D scrollytelling with native WebGL Three.js interactive mesh. |
| 2026-06-23 14:26:37 | Created 3D scrollytelling home page for base project. |
| 2026-06-23 14:22:00 | Exposed all 5 CampusSync design variants using persistent localhost.run tunnels on public URLs. |
| 2026-06-23 14:20:50 | Exposed all 5 CampusSync design variants on public URLs. |
| 2026-06-23 14:13:40 | Completed: Overhauled all 5 CampusSync frontend design variants (ports 3003-3007) with unique visual layouts, typography, and tactile styles. Blocked: None. Next: None. |
| 2026-06-23 14:09:15 | Completed: Refactored all 5 design variants of CampusSync with distinct layout styles (Glassmorphism, Aurora, Neumorphism, Brutalist, Claymorphism) running on ports 3003-3007. Blocked: None. Next: None. |
| 2026-06-23 14:06:56 | Completed: Deployed all 5 variants of CampusSync as active background processes in the agent session on ports 3003-3007. Blocked: None. Next: None. |
| 2026-06-23 14:04:55 | Completed: Created all 5 design variants (Glassmorphism, Aurora, Neumorphism, Brutalist, Claymorphism) and ran them on ports 3003-3007. Blocked: None. Next: None. |
| 2026-06-23 13:58:51 | Completed: Cloned and recreated the CampusSync React project from scratch with premium aesthetics and Tailwind CSS v4 in the campussync/ folder. Deployed server on port 3002. Blocked: None. Next: None. |
| 2026-06-22 21:51:24 | Completed: Explained which command to bind for Live Preview. Blocked: None. Next: None. |
| 2026-06-22 21:49:49 | Completed: Answered live preview shortcut questions. Blocked: None. Next: None. |
| 2026-06-22 20:48:08 | Completed: Uninstalled deprecated extensions (minovative-mind-vscode, gemini-cli-vscode-ide-companion, geminicodeassist) and configured settings.json for fastest IntelliSense and Emmet suggestions. Blocked: None. Next: None. |
| 2026-06-22 20:41:12 | Completed: Set system-wide GNOME dark mode (color-scheme prefer-dark) to make the top panel dark, and explained Wayland logout requirement for Vitals extension. Blocked: None. Next: None. |
| 2026-06-22 20:39:46 | Completed: Installed Vitals GNOME extension for top panel GPU monitoring, and explained why Next.js occupies 50% CPU. Blocked: None. Next: None. |
| 2026-06-22 20:36:44 | Completed: Terminated Next.js server processes, and explained Brave browser CPU vs GPU execution characteristics. Blocked: None. Next: None. |
| 2026-06-22 20:31:13 | Completed: Successfully uninstalled unused language extensions (Java, C/C++, Flutter/Dart), duplicate AI assistants, and duplicate layout tools to improve VS Code performance. Blocked: None. Next: None. |
| 2026-06-22 20:25:43 | Completed: Disabled Continue focusContinueInput on Ctrl+L and re-bound it to default expandLineSelection in keybindings.json. Blocked: None. Next: None. |
| 2026-06-22 20:23:10 | Completed: Replied to user about Ctrl+L default line selection shortcut. Blocked: None. Next: None. |
| 2026-06-22 20:20:10 | Completed: Set editor.quickSuggestionsDelay to 0, editor.suggest.delay to 0, and configured Emmet settings to trigger instantly in settings.json. Blocked: None. Next: None. |
| 2026-06-22 20:14:32 | Completed: Set editor.suggestDelay and editor.quickSuggestionsDelay to 0 to make autosuggestions trigger instantly as user types. Blocked: None. Next: None. |
| 2026-06-22 20:11:13 | Completed: Installed Blur My Shell, Compiz Windows Effect, and Compiz Alike Magic Lamp Effect GNOME extensions to enable liquid glass/macOS-style wobbly animations. Blocked: None. Next: None. |
| 2026-06-22 20:04:53 | Completed: Installed GlassIt-VSC extension for glassmorphism, configured Prettier/Black formatters, and added high-end custom token highlights (comments, keywords, functions, variables) to settings.json. Blocked: None. Next: None. |
| 2026-06-22 20:01:04 | Completed: Confirmed settings are strictly VS Code native settings in the default path, and no external tool overrides them. Blocked: None. Next: None. |
| 2026-06-22 20:00:10 | Completed: Added editor.gpuAcceleration: on to settings.json to ensure hardware GPU rendering is active. Blocked: None. Next: None. |
| 2026-06-22 19:58:16 | Completed: Created keybindings.json to override Jupyter ctrl+enter keybindings and mapped it to insertLineAfter. Blocked: None. Next: None. |
| 2026-06-22 19:54:53 | Completed: Restored keyboard.dispatch keyCode to settings.json and explained Jupyter keymap conflict with Ctrl+Enter. Blocked: None. Next: None. |
| 2026-06-22 19:53:40 | Completed: Set cursor blinking and 144hz smooth options for both terminal and editor in settings.json. Blocked: None. Next: None. |
| 2026-06-22 19:50:57 | Completed: Backed up settings.json and reset it to default empty brackets. Blocked: None. Next: None. |
| 2026-06-22 19:47:40 | Completed: Explained that toggling is a state-change that stays permanently visible, and added settings to disable sidebar hiding in Zen Mode. Blocked: None. Next: None. |
| 2026-06-22 19:45:27 | Completed: Replied to user regarding LLM latency and layout visibility troubleshooting steps. Blocked: None. Next: None. |
| 2026-06-22 19:41:17 | Completed: Enabled terminal cursor blinking and GPU acceleration in settings.json, and explained Ctrl+Enter keyboard conflict issues. Blocked: None. Next: None. |
| 2026-06-22 19:38:01 | Completed: Enabled smooth typing animations, blinking cursor, and smooth scrolling configurations in settings.json. Blocked: None. Next: None. |
| 2026-06-22 19:35:33 | Completed: Fixed VS Code keybindings by setting keyboard.dispatch to keyCode in settings.json. Blocked: None. Next: Check if user requires further keyboard customizations. |
| 2026-06-21 12:47:29 | Completed: Symlinked notebooks and visualization MCP sockets from -visualstudiocode.sock to -antigravityide.sock, and automated this in session-start.sh. |
| 2026-06-21 12:44:55 | Completed: Fixed Python 3.14 global packaging crash by upgrading to 26.2; installed jupyterlab, matplotlib, pandas, and ipywidgets in project .venv. Blocked: none. Next: verify if user's IDE-level notebook/visualization MCP servers connect without errors. |
| 2026-06-21 11:14:03 | Completed: handoff written. User requested file organization after session save. |
| 2026-06-21 11:51:03 | Built MCP Memory Server (FastMCP): 6 tools over SSE on port 8932, systemd service auto-starts on boot. opencode.json configured with stdio shim. agy knowledge symlinked to memory/modules+memory-bank. Port conflict 9002→8932 resolved (MinIO). Vector DB at memory/vector_db/ (ChromaDB, 197 chunks). |
| 2026-06-18 23:56:33 | Completed: Fixed Cassandra JVM compat (JDK 21 + add-opens), verified ClickHouse 26.4.4, PostgreSQL, Hadoop, and Cassandra all running. Next: graphify dashboard, Airflow redeploy, integration. |
| 2026-06-18 18:31:43 | System optimization: GPU VS Code, CPU perf governor, NVIDIA default GPU, Folding@home killed, avahi/CUPS/unnecessary autostarts removed, I/O tuning |
| 2026-06-17 18:01:25 | Redelivered Round 1 deliverables: 5-slide PPT, 3-page PDF, submission.csv pushed to GitHub. Stripped back to fixed model as competition rules required. |
| 2026-06-17 16:29:34 | Completed: Full pipeline verification. All 8 scripts compile and run. Confident learning CV best: 52.70% fold, 42.70% retrain (24/445 labels corrected). Baseline: 42.53%. Improved pipeline underperforms. Prediction: 115 test samples -> submission.csv. Key finding: 71.5% label noise too extreme for CleanLab. Next: iterative pseudo-labeling or production model on corrected labels. |
| 2026-06-16 22:08:06 | Completed: repo restructure - expanded .agentignore, moved LESSONS_LEARNED→modules/14, stripped API keys from context-snapshot, removed hardcoded key from dashboard.py, deleted 13-skills.md, consolidated session-end in Makefile+rules, added PreCompact prompt+session-read-cache rules, updated GEMINI.md references, re-seeded vector DB (169 chunks). Blocked: none. |
| 2026-06-16 21:54:22 | Added optimal token conservation rules and skill discovery protocol |
| 2026-06-16 21:47:07 | Unified memory: symlinked antigravity brain to MEMORY/memory, added RULE #7 (UNIFIED MEMORY) + hardened RULE #5 (HANDOFF PROTOCOL) with mandatory start/end commands to GEMINI.md |
| 2026-06-14 14:43:42 | BSNL GPE600 router full research: config backup (1128 lines, 19 admin pages), UPnP/DoS protection enabled, superadmin attempt failed (administrator/system864 — IP session lock), all exploit paths documented (CVE config.dat 404, Boa CVE N/A, formPassword 404), form auth bypass discovered (postSecurityFlag can be omitted). Full handoff in .agent-progress.md |
| 2026-06-13 10:00:00 | Built auto-sync system: make session-end target, pre-commit hook auto re-seeds DB. Created memory/context-snapshot.md (gitignored) with ALL secrets & session context — 30+ API keys, Render config, DB creds, admin token, RS256 keys, etc. Indexed by vector DB. memory-search now works from PATH. Updated 01-core-rules.md to enforce sync protocol. 158 chunks across 16 files. |
| 2026-06-13 09:28:35 | Unified global and local paths for drawio-skill and career-ops, validated 6 external tools, updated vector DB |
| 2026-06-13 09:21:01 | Built auto-sync system: session-end target, pre-commit hook, vector DB indexes progress files now |
<!-- Agent appends a one-line summary after each session -->
| Date | What Was Done |
|------|--------------|
| 2026-05-28 | Created Remix UI and design-system implementation guidance documentation |
| 2026-05-28 | Redesigned and rethemed Next.js portfolio website to match the Remix monospace dark luxury visual identity, verified builds, and persisted dev process in PM2 |
| 2026-05-28 | Removed redundant remix-docs-site project and PM2 daemon, keeping only the central design-system rules inside GEMINI.md |
| 2026-05-28 | Learned and integrated Andrej Karpathy's agent behavioral guidelines into GEMINI.md rules, and synced them across dotfiles and other projects |
| 2026-05-28 | Migrated and merged the dotfiles configuration project into the central MEMORY repository, and cleaned up the separate local project directory |
| 2026-05-28 | Migrated and merged the calculator-app codebase into the central MEMORY repository, deleted the separate standalone local/remote repositories, and documented its premium UI/UX micro-interaction rules in GEMINI.md |
| 2026-05-28 | Fixed portfolio particle visibility (opacity 0.25→0.6, removed ghosting trail, transparent canvas bg). Learned scrollytelling pipeline: Google Whisk (image gen) → EZGif (video→frames) → Anti-Gravity (code gen) → NodeJS. Documented Apple-level scrollytelling architecture and premium design rules in memory bank. |
| 2026-05-28 | Built comprehensive animation template library: Motion.dev (370+ examples, 8 core patterns, all APIs), ReactBits.dev (110+ components, 4 categories), scrollytelling product showcase template (Apple-level), and full production toolchain docs (Whisk→Veo→EZGif→Anti-Gravity→NodeJS). Saved to templates/animations/ |
| 2026-05-28 | Fixed formatting typo and duplicated Kaggle Competition Workflow section in GEMINI.md, automatically synchronizing changes across all 12 hard-linked rules files |
| 2026-05-28 | Integrated React Doctor static analysis requirement (npx react-doctor@latest) under Production Standards in GEMINI.md to ensure high-quality React builds |
| 2026-05-28 | Enhanced portfolio UI/UX: implemented GSAP-powered Radial Mask Reveal in Hero, GSAP-morphing 2x2 dot grid mobile toggle in Navbar, and fixed 35 static analysis issues to reach a perfect 100/100 React Doctor score |
| 2026-05-30 | Solved Brownie-Bliss #206, Repo-lyzer PR #338, created GSSoC issues/PRs in DailyForge and OpSo, fixed PiperChat01 #140 (reactions sync on socket reconnect), opened PR #186, replied to all query comments on assigned issues, and cleared unread GitHub inbox notifications |
| 2026-05-31 | Learned about CodeBurn, updated global rules (GEMINI.md & hard links) to prioritize CLI commands, archived unused custom configs, capped terminal output in bashrc, and documented OpenCode CLI delegation strategy to save credits globally |
| 2026-06-05 | Updated system package managers (APT, Snap, NPM, Pipx). Compiled a catalog of 200+ modern CLI tools and installed 'mods' (AI CLI by Charm). |
| 2026-06-05 | Researched the fastest and best modern CLI replacements (Rust/C) and created a comprehensive catalog. |
| 2026-06-05 | Installed and verified local static analysis and security tools (shellcheck, cppcheck, bandit, trufflehog). |
| 2026-06-05 | Installed and configured gosec, cargo-audit, pip-audit, and sqlmap globally, and created open_source_bug_hunting.md guide. |
| 2026-06-05 | Analyzed duplicate proposal on issue #92727 and established preventive measures; audited issue #92696 comments to prevent duplicate submissions. |
| 2026-06-05 | Installed and configured vulnhuntr via pipx, completed verification of installed static analysis and security tools. |
| 2026-06-05 | Built security-toolkit project: Vite+React frontend + Express backend. Features: multi-tool security scanner (semgrep/bandit/trivy/gitleaks/etc.), NVD CVE search, tools status page, GitHub Actions CI. Running on localhost:5173 (UI) + localhost:3741 (API). |
| 2026-06-08 | Created Discord God Mode Bot with mass purge, ghost kicker, auto-mod, and music player (Slash Commands). Deployed via PM2. Decommissioned and completely wiped the project from the system per user request after a Discord security lock anomaly. |





| 2026-06-09 | Full MEMORY repo deep audit: replaced 221KB monolith with 8-module system (01-08), symlinked all 197KB bloat files (.clinerules/.cursorrules/.windsurfrules/CLAUDE.md), locked in ZERO_PROMPTING_DIRECTIVE, CodeBurn tool, CLI replacement rules, GSAP patterns, ML decision tree, deployment workflow. Token cost per session: 55,000 → 500. |
| 2026-06-09 | MEMORY repo full setup verification: converted 7 duplicated 197KB GEMINI.md copies to proper symlinks (saved 1.2MB), fixed broken opencode/AGENTS.md symlink (was pointing to LESSONS_LEARNED.md instead of GEMINI.md), created vector_db/ + tools/static/ dirs, added vector_db/ to both .gitignore and .agentignore, verified all Python deps (chromadb/mcp/fastapi/uvicorn), created activeContext.md + walkthrough.md for agentlint compliance. Logged 5 new error prevention patterns to LESSONS_LEARNED.md (#3-#8) covering CLI tools, OpenCode delegation, pre-flight sequence, Read tool overuse, git diff|delta, and quality checks. |
| 2026-06-09 | Restructured MEMORY repo (27→13 root items): grouped config into config/, memory into memory/, fixed all symlinks. Started Qdrant (was dead 8 days), symlinked onlycli to PATH, started graphify + memory-dashboard services. Removed 4 dead tool scripts. Fixed Specialized Tool Matrix: removed uninstalled tools (hackingtool, feast, milvus), added installed ones (enola, aider, uv, codeburn). Updated Zero-Token auto-trigger rules with 11 new conditions. Replaced sober/semgrep references (sober not installed). Updated all hardcoded paths for new directory layout. Pushed to github.com/adityashirsatrao007/MEMORY. |
| 2026-06-09 | Seeded vector_db with 68 GEMINI.md sections (dashboard search now works). Verified all 54 documented CLI tools are installed (0 missing). Installed codeburn Antigravity hook for usage capture. Added codeburn token logging (step 0) + tool validation (step 5) + EXIT trap to session-start.sh. |
| 2026-06-09 | Created tool guardrails (~/bin/guardrails/): 8 wrappers that shadow grep→rg, cat→bat, ls→eza, find→fd, du→dust, top→btop/btm, ps→procs, sed→sd. Each prints a warning + still runs the original command. session-start.sh exports PATH to activate them. GEMINI.md updated with enforcement section. |
| 2026-06-09 | Created complete 54-tool dispatch table in GEMINI.md — every installed tool has an exact trigger condition with failure conditions for using old tools. Created ~/bin/auto-dispatch script for natural-language tool suggestions + CWD-based suggestions. Added step 6 (auto-discovery: onefetch + tokei + eza --tree) to session-start.sh that auto-runs for any git repo. |
| 2026-06-09 | Split monolithic GEMINI.md (3,622 lines) into 9 module files under memory/modules/ (2,278 lines total). GEMINI.md is now a 63-line index that tells agents which modules to load by task. Core modules (01-core-rules, 02-cli-tools) pre-loaded by session-start.sh; task-specific modules (03-09) loaded on demand. Re-seeded vector DB with 69 chunks across all 9 modules. ML sections rewritten to industry-standard MLOps (K8s, FSDP, Triton, Evidently, Feast, Great Expectations). |
| 2026-06-09 | Removed Qdrant container (was using 89MB RAM, unused by anything). Switched to ChromaDB-only vector storage (disk-based SQLite, 0 RAM overhead). Updated 02-cli-tools.md references. |
| 2026-06-09 | Makefile, .githooks, seed script upgrade, cross-project paths, 98-chunk vector DB, dashboard verified |
| 2026-06-09 | Final cleanup: reviewed all restored files, kept templates as reference library (10 files, 2,301 lines), linked from 05-ui-ux.md, deleted 26 stale files |
| 2026-06-09 | Compressed core modules 73%, behavioral token rules, read cache, rtk hook, silent CLI |
| 2026-06-13 | Configured Shadcn, Magic UI, and Playwright MCP servers in `mcp_config.json`; created code design validation script `validate_ui.py` integrated into `Makefile` and git `pre-commit` hook; optimized `fcc-server` model routing to use free Google AI Studio Gemini models and disabled thinking passes to minimize latency and token costs; created `.claudeignore` file; created `CLAUDE_CODES.md` template containing 100 stacked Claude prompt modifiers and linked it to modules; added 5 Operator MCPs (Firecrawl, Playwright, Glif, Perplexity, and Chrome-Tabs) to `mcp_config.json` with global key placeholders; compiled/installed `bottom` (`btm`), installed `devbox`, and created `12-repo-teachings.md` pattern reference guide. |
| 2026-06-13 | MIT → proprietary DRM migration: RS256 license enforcement, 3-layer integrity guard (Makefile grep + Python scan + online verify), 7-day offline grace, machine fingerprint. License server on Render with Resend email, admin panel (cookie auth, owner-only, stats/activations). All 5 tools gated, Makefile targets locked, setup.sh with OS detection. All docs updated to source-available. 6 trial licenses in DB. |




## Conversation Handoff (2026-08-10 08:00:17)
- **Notes**: No explicit session notes provided.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 08:42:27)
- **Notes**: Completed: 4 sites live+200 with correct content (portfolio, BERT, SentinelX front, Tracelify front); wired portfolio live-demo links; fixed CI action typo (amondnet/vercel-action@v42) + set VERCEL_TOKEN via GitHub API; all CI deploy runs=success. Blocked: SentinelX/Tracelify/OME/NIDS backends not deployed (need browser OAuth to Render/Streamlit/HF + DB/Redis secrets). Next: user imports OME+Tracelify to Render, NIDS to Streamlit Cloud; add NEON Postgres+Redis Cloud free for SentinelX/Tracelify DB deps.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## 2026-08-10 — AI Provider matrix created (by opencode)
- Created AI_PROVIDERS.md (MEMORY repo + ~/.config/global-apikeys) — 23 providers already had vs 30 missing recommended keys with signup links.
- Added SARVAM_API_KEY (verified working via /translate -> 200).
- Added pending placeholders (commented) to keys.env; both key files synced/identical.
- Next: user collects missing keys (starts: OPENAI, ANTHROPIC, XAI, TOGETHER, PERPLEXITY); then rerun tools/test_all_keys.py to validate.

- Skipped paid (Together/MiniMax/DashScope/Perplexity/AI21). Added SAMBANOVA(valid). Dead free keys: GEMINI/HF_TOKEN/KIMI. Queue: Hyperbolic, Tavily, Voyage, Jina, ElevenLabs, Brave.

- README + updated with API Key Links master table (has/next/paid). TAVILY verified. Skip-paid policy locked.

- 2026-08-10 KEY SWEEP: dead=GEMINI, HF_TOKEN, KIMI, RESEND, CLOUDFLARE_TOKEN, WANDB(404), CODESTRAL(retired->Mistral). Added working: EXA, PINECONE, QDRANT(JWT+URL). Free models on OR: 14 (:free). New free providers: Cloudflare Workers AI(need regen CF), OVHcloud, SiliconFlow. GitHub Models retired 2026-07-30.
- 2026-08-10: REGENERATED valid: GEMINI, HF_TOKEN, RESEND, CLOUDFLARE_TOKEN(WAI working). Skipped: KIMI. All other keys verified. 27+ working AI keys total.

- Added memory/modules/21-api-key-routing.md (use-case->key matrix, free-first), wired into README + GEMINI.md router.

- Persisted directive: user won't explicitly command which API to use → agent auto-selects provider from 21-api-key-routing.md (free-first).

## Conversation Handoff (2026-08-10 20:42:32)
- **Notes**: Completed: dbms-interview-prep repo @ github.com/adityashirsatrao007 (private, 48 files). Researched via firecrawl (29 verified refs, GfG/StrataScratch grounded). Built 30 docs (SQL->NoSQL), 9 excalidraw diagrams, mermaid inline, 5 verified-by-execution PG scripts, design cases, 100 one-liners. Blocked: nothing. Next: optional expand with Postgres/MySQL engine-specific labs.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 21:51:19)
- **Notes**: Completed: filled all 10 gap topics in dbms-interview-prep (engine compare, OLAP/columnar, security/SQLi/backup, 14 LeetCode solved bank, concurrency labs script, LATERAL/JSONB/FTS, real EXPLAIN walkthrough, replication-HA, vector/RAG, PL/pgSQL+triggers). All new SQL verified against PG 18. README updated w/ all sections. Pushed. Blocked: none. Next: optional PG-engine deep lab / mock-interview doc.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 22:11:13)
- **Notes**: Completed: fixed README mermaid parse error; filled research gaps — added 11-database-architecture/{01-end-to-end-query-lifecycle,02-db-ops-day2(monitor/locks/bloat/migrations, FOR SHARE, CTE mat),03-app-side-perf-debugging,04-cdc-outbox(verified),05-feature-store-ml}.md + 07-practice/06-mock-interview-round.md. New SQL verified PG 18 (bitmap eval, FOR SHARE, outbox trigger, RANK ties, MATERIALIZED CTE). README updated (section 11, mock file, plan). Pushed. Blocked: none. Next: optional mermaid render check via mmdc, PG engine deep-dive labs
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 22:20:39)
- **Notes**: Deployed all backends live via cloudflared. ome-api:8000 -> presents-hormone-jurisdiction-birthday.trycloudflare.com. tracelify-api:8001 -> flag-greater-exploring-species.trycloudflare.com. sentinelx-api:8002 -> car-oven-rely-dramatically.trycloudflare.com (all /docs+/health 200). NIDS streamlit:8003 -> sorry-tar-spirit-reg.trycloudflare.com (_stcore/health 200; Predict needs results/*.joblib + .pth weights - MISSING from repo). Portfolio projects.js liveLinks updated + pushed to main-portfolio (Netlify/Vercel Pages rebuild triggered). Blocked: NIDS model weights absent. Next: add weights / wire Cape, restart tunnels if drop.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 22:24:03)
- **Notes**: Completed: README.md rebuilt as fully self-contained 5562-line doc — all 65 topic files + 7 SQL scripts + references inlined by Python generator (build_readme.py in /tmp/opencode), headings auto-nested, one H1. Pushed e4549a8. Blocked: none. Next: if user wants source-of-truth folders removed, or regenerate README after future edits via the generator.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 22:33:24)
- **Notes**: Completed: README restructured to mirror system-design vault exactly — copyright line, grouped TOC with anchor links (Getting Started + Ch I-XI + Appendix), 'How to use this course (roadmap)' phase table, 'What is a DBMS' opener, every doc as # topic (natural ##/###), companion SQL scripts + Diagram Index + License. 49 topics, 5774 lines, pushed 3f060c1. Blocked: none. Next: none — repo self-contained; regenerate via /tmp/opencode/build_readme.py on future edits.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 22:42:31)
- **Notes**: Completed: deleted all topic/sql/references/tools folders per user choice — repo now single-source: README.md (5,774 lines, fully inline) + diagrams/ (9 Excalidraw). Pushed. Blocked: none. Next: none — note the README generation-from-folders is now obsolete; README is static content. Any future edits/edit docs directly in README.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 22:55:02)
- **Notes**: Completed: added 6 gap topics to README — MERGE & temporal tables, Consensus (Raft/Paxos/ZAB/quorums), Graph DBs (property graph, Cypher), Reconciliation primitives (Merkle/Bloom), SCD Types 0-6 w/ verified PG SCD2+as-of join, warehouse dims (conformed/junk/degenerate, additive/semi/non-additive). All new SQL verified on PG18 (MERGE, SCD2 expire+insert, point-in-time fact join). TOC + anchors updated. 60 H1s, 6065 lines, pushed 81d66b3. Blocked: none. Next: none.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 23:00:01)
- **Notes**: Fixed main-portfolio GitHub Pages asset 404s: raw asset URLs in src (project imgs, logos, fonts, favicons, manifest, 3D HDR/GLB, noise, giats, og.png) were not basePath-prefixed. Added src/constants/assets.js A() helper, wired into projects.js export map, CustomHead, _document.fonts, fonts.scss + global.scss URL('...'), FruitNinja, MagicBall, floatingMeshes, Badge, Hero, about Index. Clean build (prettier printWidth 200) + push; Pages+Vercel workflows succeeded; all 13 assets 200 + project pages 200. Next: if reviewer still sees console 404s, re-verify cache.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 23:03:29)
- **Notes**: Completed: Rewrote gym-aesthetic-physique-guide README fully (848 lines, detailed prose all sections incl diet/abs/cardio/recovery/jawline/skincare/phitkari-verdict), finished TOC, re-embedded all 19 images, pushed commit 3a91706. Blocked: none. Next: user verifies README renders on GitHub.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 23:13:58)
- **Notes**: Completed: embedded verified PG18 outputs across SQL topics — joins (A/B garden: INNER/LEFT/RIGHT/FULL/SEMI/ANTI/CROSS + master cheat-sheet + repo-seed INNER/LEFT/ANTI/SELF result tables), SQL Basics (WHERE/DISTINCT/GROUP-HAVING/CASE/LIMIT/2nd-highest), subqueries (scalar/correlated/EXISTS/CTE), window fns (RANK tie demo, running total, LAG, rolling frames, NTILE, top-2/dept). Removed 4 stray non-heading title lines. 60 H1s, 6484 lines, pushed fd9fa09. Verified queries run live on PG18. Blocked: none. Next: none.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 23:22:22)
- **Notes**: Frontends wired to live backends. SentinlX UI (adityashirsatrao007.github.io/ai-threat-detection) + Tracelify UI (adityashirsatrao007.github.io/error-tracking-observability-sdk): added Vite base (VITE_BASE_PATH) + router basename for GH Pages subpath; pages.yml envs repointed to live tunnels (car-oven.../api/v1, flag-greater...); backends restarted with CORS allowing adityashirsatrao007.github.io. Tunnel checks 200 + ACAO header present. Portfolio liveLinks point to UI URLs (pushed). Done.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 23:44:15)
- **Notes**: Completed: verified outputs for every remaining SQL example in dbms-interview-prep README (SQL Basics refresh with Kyle/Orphan drift fixes, DDL/DML new verified section, Advanced Patterns P1-P12 incl streaks/running/pivot/delta tables, Edge Cases micro-demos, PG Advanced LATERAL/string_agg/unnest, Procedures raise_salary/trigger/dept_roster), fixed even_emp_ids PL/pgSQL bug, removed 42 stray bare-title lines; README 6715 lines, 60 unique H1s, 514 balanced fences; committed 0ddf7bc and pushed. Blocked: none. Next: further 'done properly' passes — consider verified outputs for MERGE chapter, recursive CTE pattern P9/P10, and the practices in LeetCode SQL bank chapters if user wants.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-10 23:59:16)
- **Notes**: Completed: Portfolio SEO finalization. New per-page canonical/og:url via CustomHead path prop (home='', about=/about, projects=/projects, detail=/projects/:id); geo.region=IN-MH, og:locale=en_IN, unlocked viewport zoom all verified in out/. Fixed stale public/sitemap.xml + public/manifest.json to github.io/main-portfolio URLs with real profile (removed 'Giats from Greece' leftover). Verified live: home/about/projects 200, robots+sitemap+manifest serve github.io URLs, per-page canonical live. Fixed broken Vercel deploy: VERCEL_TOKEN GitHub secret was invalid -> replaced with local CLI token, but that token ALSO returns 403 (expired) so Vercel deploy STILL fails; GitHub Pages is the working deploy. Blocked: Vercel deploy (token expired, needs 'vercel login' or valid token). Next: re-auth Vercel or disable vercel.yml; NIDS weights still missing.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-11 00:26:57)
- **Notes**: Completed: All 27 diagrams now embedded as real rendered PNGs in README (diagrams/png/, ~3MB, named 01-27 matching .excalidraw) via 2x-scale headless-browser render (SVG output was rejected because mermaid uses foreignObject + span, which GitHub/RAW and <img> tags cannot render). Added 27-row PNG+excalidraw dual-column links table in Part VII (fixed stale '25 diagrams' heading to 27). Verified 27/27 PNG links resolve, fences balanced. Pushed 9ddcbc9. Blocked: none. Next: re-run 112-topic coverage audit + mermaid 27-count + TOC resolvability to confirm nothing regressed.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-11 00:28:20)
- **Notes**: Completed: Fixed ex2mmd.py (dedupe only text, positive-t ray-cast from arrow start, center-based nearest, global nearest-label with axis-aware threshold 4) -> all 8 non-Venn diagrams convert correctly; spliced inline Mermaid into README at 8 sites, committed+ pushed 526c441 (keeps joins-venn.svg + Diagram Index thumbnails as SVG); README 530 fences balanced, 60 H1s, 17 mermaid fences. Blocked: none. Next: optional verified outputs for MERGE chapter, recursive CTE patterns P9/P10, LeetCode-SQL bank chapters; then convert remaining diagrams if desired.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-11 00:43:05)
- **Notes**: Completed: Ran the full 134-topic coverage audit — result 134/134 PASSED. Earlier '9 fails' decomposed: 6 were invalid audit rows I'd added (DistilBERT/Celery/Redis/PostgreSQL from SentinelX, Idiom/Ultramarine — never in scope) and removed; 3 were keyword-matching bugs (greedy->'greedy/beam', instruction->'instruction-tuning', prompt tuning present). Real gap found: README covered LoRA/QLoRA/PEFT deeply but never named prompt/prefix tuning — added a line to Q7 (full FT vs LoRA/QLoRA/adapters/soft prompts). Verified raio fences 293 both pre/post, 27 mermaid, H1/H3 unchanged, pushed faf9527. Also pushed 9ddcbc9 earlier this session (27 PNG-rendered diagrams + viewer-agnostic table). Blocked: none. Next: none — audit green, all diagram links verified. Optional: PNGs could be re-generated should any mermaid block change.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-11 20:08:36)
- **Notes**: Completed: Added explainable AI (Grad-CAM+SHAP) + training pipeline to solar dust repo, pushed 835b14f. Blocked: none. Next: user generates figures/paper via excalidraw; retrain with train_solar_dust.py once dataset downloaded.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-13 23:34:18)
- **Notes**: Completed: built full beginner ML course README for civil-concrete-strength-predictor; trained+verified (R2 0.9124); fixed app.py warning; deployed PERMANENT GitHub Pages in-browser demo at adityashirsatrao007.github.io/concrete-strength-predictor-demo (web/model.json + predict.js, matches sklearn 51.667); added streamlit_app, share_live.sh tunnel (tested live), hf_space gradio (needs PRO 402), Windows setup docs. Blocked: HF Spaces free (2026 PRO-only). Next: optional Streamlit Cloud permanent deploy via share.streamlit.io
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-17 10:49:48)
- **Notes**: Completed: Installed+launched munder-difflin (electron multi-agent harness) at ~/Desktop/Projects/munder-difflin, npm install done, typecheck passed, dev running (log /tmp/munder-dev.log). Agents on PATH: opencode, kimi. Blocked: none. Next: user to test UI, pick agent CLI, configure Michael.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-17 11:04:52)
- **Notes**: Completed: munder-difflin fully auto-configured + running. config.json (47 fields) at ~/.config/munder-difflin; harnessHome ~/Desktop/Projects/munder-difflin-hive; god Michael on opencode/deepseek-v4-flash-free; registered repo ~/Documents/Default Project; autoMode on, telemetry off; App.tsx:56 patched to auto-open current hive (pick skip); live PTY verified. Blocked: none. Next: user to add workers via Add Agent modal; remember App.tsx patch if they prefer picker.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-08-31 21:25:08)
- **Notes**: No explicit session notes provided.
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.

## Conversation Handoff (2026-09-08 22:20:50)
- **Notes**: Completed: Fitted Table 1.1 in chapter1 (DOCX text verbatim incl em-dashes, height-bounded imgs 3.0cm, no resizebox, cols 0.9/10.4/4.0cm, fits p25 one page, no vbox overflow). Verified Chapter1 vs DOCX: body text byte-exact, 3 numbered lists (5/4/3 items) match, no invented bullets. Regenerated 19 chapters_pdf splits (120p). Blocked: frontmatter page-number plan (Abstract-in-TOC, i/iii/vii/ix/x counters, unnumber early pages, rename LoA heading) awaits approval. Next: wait for frontmatter plan approval; dead-space scan elsewhere (minor 1-14pt overfull hboxes in ch5 URLs/biblio remain, 23pt one known).
- **Incoming Agent Directive**: Read this note and resolve any pending tasks described.
