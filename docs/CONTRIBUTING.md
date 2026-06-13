# Contributing to MEMORY

## How to Contribute

1. **Fork** the repo and create a branch: `git checkout -b feature/my-feature`
2. **Develop** against the modular architecture:
   - Place new knowledge in the appropriate `memory/modules/XX-*.md`
   - Tools and scripts go in `tools/`
   - Documentation in `docs/`
3. **Run validation**: `make validate && make seed`
4. **Commit** with a clear message: `type(scope): description`
5. **Open a PR** against `main`

## Module Guidelines

- Each module must be <500 lines (auto-enforced by pre-commit hook)
- Use `##` headings for top-level sections, `###` for subsections
- Include a brief description at the top of each module
- All paths in modules must use `$MEMORY_ROOT` prefix

## Code Standards

- Shell scripts: bash with `set -euo pipefail`
- Python: ruff-compatible (see `docs/API_REFERENCE.md`)
- Markdown: wrap at 100 chars, use fenced code blocks with language tags
- Diagrams: .drawio source + exported PNG in `docs/images/`

## Review Process

PRs are reviewed within 48 hours. All checks must pass:
- `make validate` — module structure + symlink integrity
- `pre-commit run --all-files` — lint, format, secrets scan
- `semgrep --config auto .` — SAST scan
