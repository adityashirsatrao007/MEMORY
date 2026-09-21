---
created: 2026-06-21T12:04:27.135779
category: session
tags: ["config", "mcp", "opencode", "vscode", "infra"]
---

Session 2026-06-21: Migrated opencode MCP from stdio-shim to URL/SSE. Configured VS Code globally (settings.json mcp.servers + github.copilot.chat.mcpServers) and project-level .vscode/mcp.json. All agents now share one persistent SSE daemon on :8932.
