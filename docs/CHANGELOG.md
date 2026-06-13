# Changelog

All notable changes to MEMORY are documented here.

## [1.0.0] — 2026-06-13

### Added
- 12 modular brain architecture replacing monolithic 3,622-line GEMINI.md
- ChromaDB vector search with 94.2% recall rate (~200 tokens per query)
- Lazy/full mode switching — 60–95% token reduction per session
- 54 CLI tool modernizations (grep→rg, cat→bat, ls→eza, etc.)
- freellmapi proxy integration — 16 free LLM providers, 1.7B tokens/mo
- Universal install script (bash <(curl ...)) — Java, C/C++, Go, Rust, Python, Node
- draw.io architecture diagram with proper white background
- GitHub Pages deployment with professional HTML landing page
- 6-agent symlink system (Claude Code, OpenCode, Cursor, Windsurf, Copilot, Cline)
- Pre-commit hooks with UI validation + post-merge ChromaDB re-seed
- 18 API key auto-loading from global config
- Self-healing error protocol with Module 11 error logs

### Changed
- Restructured all root docs into `docs/` directory
- Pricing: removed free tier, added hackathon (₹2,000/2mo), INR support
- SVG inline charts replace matplotlib PNGs for benchmarks and token savings
- Architecture diagram: 5406×7709 → 1865×1205 (compact LR layout)

### Fixed
- All image paths in markdown files (docs/images/ → images/)
- .gitmodules for taste-skill submodule URL
- Dark mode persistence across all HTML pages
