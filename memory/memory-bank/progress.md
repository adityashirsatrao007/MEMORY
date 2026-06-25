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



