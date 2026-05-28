# Remix Docs Site — Architecture

## Tech Stack
- **Server:** Node.js, Express.js (v4.19)
- **Frontend Core:** HTML5 semantic container templates
- **Styling:** Vanilla CSS3, custom properties for design tokens, inline SVG Noise filter overlays
- **Interactions:** Vanilla JavaScript (custom keyboard listeners, overlay traps, IntersectionObserver anchor scrollspy)
- **Deployment & Persistence:** PM2 Process Manager, git repositories

## Folder Structure
```
remix-docs-site/
├── .github/
│   └── workflows/
│       └── ci.yml        ← GitHub Actions CI pipeline
├── docs/
│   └── images/           ← Relative asset directory
├── memory-bank/          ← Core project state documents
│   ├── progress.md
│   ├── architecture.md
│   └── decisions.md
├── index.html            ← Primary semantic layout
├── index.css             ← Styling system & design tokens
├── index.js              ← Micro-interactions & keyboard listeners
├── server.js             ← Express production server
├── package.json          ← Node dependencies & script mappings
├── Makefile              ← Project targets runner
└── .gitignore            ← Exclusion rules
```

## Production Standards Mapping
- **Security Headers:** Configured in Express middleware (`Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`).
- **Telemetry Health check:** Mapped `/health` and `/ready` endpoints returning server timestamp and system readiness states.
- **Graceful Shutdown:** `SIGTERM` and `SIGINT` lifecycle listeners gracefully terminate the Express server process.
- **Explicit CORS:** Origin allowed list restricts requests to localhost mappings.
