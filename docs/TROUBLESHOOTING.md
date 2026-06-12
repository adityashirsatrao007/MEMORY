# Troubleshooting

## Common Issues

### `make validate` fails — module missing
```
Error: Module 03 not found at memory/modules/03-ml-engineering.md
```
**Fix:** Run `git submodule update --init --recursive` or re-clone the repo.

### ChromaDB import error
```
ModuleNotFoundError: No module named 'chromadb'
```
**Fix:** `pip install chromadb` (Python 3.10+ required).

### Pre-commit hook blocks everything
```
✖ UI Validation failed: font-family warning in .agents/skills/...
```
**Fix:** Use `git commit --no-verify` to bypass, or fix the offending file. This is a known issue — the UI validation scan is overly broad.

### Vector search returns no results
```
$ memory-search "query"
→ empty
```
**Fix:** Re-seed the database: `make seed`. If still empty, check ChromaDB is running on port 8000.

### Broken symlink
```
$ readlink -f CLAUDE.md
→ (empty or wrong path)
```
**Fix:** Re-run the symlink commands from [INSTALL.md](INSTALL.md).

### OOM during install
**Fix:** Serialize installs: `apt` → `cargo` → `ollama`. See Module 11 (Error Logs) for the full failure mode catalog.

## Logs

All recorded failure modes are in `memory/modules/11-error-logs.md`. Check there first before opening an issue.
