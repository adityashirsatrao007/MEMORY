## Current Focus
Repository fully set up and integrated — all CLI tools installed, vector DB seeded (246 chunks), GitHub Student Pack integrations ready.

## Active Decisions
- GEMINI.md is a lightweight 158-line index (NOT the old 3543-line monolith)
- 19 modules in memory/modules/ cover all domains (01-20, with 13 newly created)
- Vector DB: ChromaDB with 246 chunks from 23 files
- All agent config files symlink to GEMINI.md (no duplication)
- 27 CLI tools installed with 8 guardrails
- GitHub Student Pack: DigitalOcean $200, MongoDB $50, Clerk, Stripe, Datadog configured

## Open Questions
- Should activeContext.md be auto-regenerated each session?
- MongoDB Atlas migration from ChromaDB for production scale?
