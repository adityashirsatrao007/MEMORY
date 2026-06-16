## Current Focus
Repository setup and configuration — verified all dotfile symlinks, converted 7 duplicated GEMINI.md copies to symlinks, created vector_db/ infrastructure, and logged all error prevention patterns.

## Active Decisions
- GEMINI.md is the single 197KB master rules file (3543 lines)
- All agent config files symlink to GEMINI.md (no duplication)
- 14-lessons-learned.md (in modules/) is the error log — memory/LESSONS_LEARNED.md is a symlink to it
- vector_db/ is gitignored (ChromaDB persistent storage)
- tools/static/ is for the dashboard frontend

## Open Questions
- Should activeContext.md be auto-regenerated each session?
