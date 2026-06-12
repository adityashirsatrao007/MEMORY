# MCP Guide

## What is MCP?

Model Context Protocol (MCP) is an open standard for connecting AI agents to external tools and data sources. MEMORY uses MCP to extend agent capabilities beyond its 12 built-in modules.

## Available MCP Servers

| Server | Purpose | How to Use |
|--------|---------|------------|
| shadcn | UI component generation | `npx -y shadcn@latest mcp serve` |
| magic-ui | Design system components | `npx -y @magicuidesign/cli@latest mcp` |
| playwright | Browser automation | `npx -y @playwright/mcp@latest` |
| firecrawl | Web scraping | `npx -y firecrawl-mcp` |
| chrome-tabs | Browser tab management | `npx -y @pokutuna/mcp-chrome-tabs@latest` |
| clay | Analytics platform | `npx -y @clayhq/clay-mcp@latest` |

## Adding a New MCP Server

Add to `~/.gemini/antigravity/mcp_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "API_KEY": "${MY_KEY}"
      }
    }
  }
}
```

## Notes

- MCP servers must be installed per-agent. MEMORY's GEMINI.md configures the agent to use them.
- API keys for MCP servers go in `~/.config/global-apikeys/keys.env`.
- For production, use permanent PM2 processes (not npx).
