#!/usr/bin/env python3
"""MCP Memory Server — stdio transport (for local MCP clients like opencode)."""
import os, sys
os.environ.setdefault("FASTMCP_LOG_LEVEL", "ERROR")
os.environ.setdefault("MEMORY_ROOT", os.path.expanduser("~/Desktop/Projects/MEMORY"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from server import server
server.run(transport="stdio")
