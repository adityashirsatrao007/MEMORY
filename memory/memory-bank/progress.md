# MEMORY — Progress & Session Log

> Agent updates this at the END of every session.
> Read this at the START of every session to resume without re-analysis.

## Current Status
<!-- Agent updates: what state is the project in right now? -->

## What's Done
- [ ] Project scaffolded

## What's In Progress
<!-- Nothing yet -->

## What's Next
<!-- Agent fills based on plan -->

## Known Issues / Tech Debt
<!-- Agent notes anything that needs attention later -->

## Session Log
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
