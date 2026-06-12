# Migration Guide

## From Monolithic GEMINI.md (Pre-v1.0)

MEMORY v1.0 replaces the old single-file approach with modular architecture. Migration is automatic if you clone fresh.

### If you have a customized GEMINI.md

1. Back up your custom config: `cp GEMINI.md GEMINI.md.backup`
2. Clone MEMORY fresh: `git clone https://github.com/adityashirsatrao007/MEMORY.git`
3. Port your custom rules into the appropriate module in `memory/modules/`
4. Run `make seed` to index your changes

### Breaking Changes

| Before | After | Impact |
|--------|-------|--------|
| Single `GEMINI.md` (3,622 lines) | 12 modules in `memory/modules/` | Auto-routed — no action needed |
| Root-level docs | `docs/` directory | Update any direct links |
| Direct `curl`/`wget` usage | Guardrailed to `httpie` | Transparent — runs via dispatch |
| `pip` installs | `uv` preferred | Fallback to pip if uv absent |

## From Other Agent Systems

### Switching from Claude Code only

MEMORY works with any agent. Just symlink `GEMINI.md` to your agent's config file:
- Cursor: `ln -sf $PWD/GEMINI.md .cursorrules`
- Windsurf: `ln -sf $PWD/GEMINI.md .windsurfrules`
- Copilot: `ln -sf $PWD/GEMINI.md .github/copilot-instructions.md`
