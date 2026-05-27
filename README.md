# MEMORY — Aditya's Agent Configuration Hub

Central repository for all AI agent memory and configuration files.

## Contents

| File | Purpose |
|------|---------|
| `AGENTS.md` | Main agent rules — source of truth (also aliased as `GEMINI.md`, `CLAUDE.md`) |
| `CLAUDE.md` | Symlink/copy of AGENTS.md for Claude Code |
| `GEMINI.md` | Symlink/copy of AGENTS.md for Gemini CLI |
| `.clinerules` | Copy for Cline agent |
| `.cursorrules` | Copy for Cursor IDE |
| `.windsurfrules` | Copy for Windsurf IDE |
| `.github/copilot-instructions.md` | Copy for GitHub Copilot |
| `VIBE_CODER_GUIDE.md` | Web design aesthetic & layout reference |
| `.agentignore` | Universal agent file-reading blacklist |
| `.aider.conf.yml` | Aider AI pair programmer config |
| `.continuerc.json` | Continue.dev extension config |
| `opencode.json` | Opencode agent config |
| `opencode/` | Opencode CLI configuration files |

## Usage

Symlink or copy the relevant file from this repo into any project's root:

```bash
# Example: use central AGENTS.md in a project
ln -sf ~/Desktop/Projects/MEMORY/AGENTS.md /path/to/project/AGENTS.md
```
