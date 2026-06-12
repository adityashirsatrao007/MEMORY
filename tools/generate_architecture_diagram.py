#!/usr/bin/env python3
"""Generate architecture diagram for MEMORY system (WHITE background)."""

import os
from pathlib import Path
from diagrams import Diagram, Edge, Cluster
from diagrams.onprem.database import Mongodb
from diagrams.onprem.client import User
from diagrams.programming.language import Python
from diagrams.generic.os import LinuxGeneral

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "docs" / "images"
os.makedirs(IMAGES, exist_ok=True)

graph_attr = {
    "bgcolor": "white",
    "fontcolor": "#1D1D1F",
    "fontsize": "14",
    "pad": "0.5",
    "dpi": "200",
    "color": "#D2D2D7",
}

node_attr = {
    "fontcolor": "#1D1D1F",
    "fontsize": "10",
}

cluster_attr = {
    "bgcolor": "#F5F5F7",
    "fontcolor": "#6E6E73",
    "bordercolor": "#D2D2D7",
    "style": "rounded",
}

with Diagram(
    "MEMORY Architecture — Symlink Web + Module Load Chain",
    filename=str(IMAGES / "architecture"),
    outformat="png",
    show=False,
    graph_attr=graph_attr,
    node_attr=node_attr,
    direction="TB",
):

    with Cluster("Agent Tools (symlinks to GEMINI.md)", graph_attr=cluster_attr):
        claude = User("Claude Code\nCLAUDE.md")
        opencode = User("OpenCode\nAGENTS.md")
        cursor = User("Cursor\n.cursorrules")
        windsurf = User("Windsurf\n.windsurfrules")
        copilot = User("Copilot\ncopilot-instructions")

    gemini = LinuxGeneral("GEMINI.md\n(Router / Decision Engine)")

    with Cluster("12 Memory Modules (lazy-loaded on demand)", graph_attr=cluster_attr):
        m1 = Python("01 Core Rules")
        m2 = Python("02 CLI Tools")
        m3 = Python("03 ML Eng.")
        m4 = Python("04 Security")
        m5 = Python("05 UI/UX")
        m6 = Python("06 Web Dev")
        m7 = Python("07 Job Hunt")
        m8 = Python("08 Arch.")
        m9 = Python("09 Misc")
        m10 = Python("10 Lessons")
        m11 = Python("11 Errors")
        m12 = Python("12 Repos")

    chroma = Mongodb("ChromaDB\n(Vector Search)")

    agents = [claude, opencode, cursor, windsurf, copilot]
    for a in agents:
        a >> Edge(color="#CC5833", style="dashed", fontcolor="#6E6E73", label="symlink") >> gemini

    modules = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]
    gemini >> Edge(color="#2E4036", fontcolor="#6E6E73", label="lazy load") >> modules[0]
    for i in range(len(modules) - 1):
        modules[i] >> Edge(color="#D2D2D7") >> modules[i + 1]

    for m in modules:
        m >> Edge(color="#4A7C6F", style="dotted", fontcolor="#6E6E73", label="seed") >> chroma

    chroma >> Edge(color="#2E4036", style="bold", fontcolor="#6E6E73", label="search") >> gemini

print("  ✅ Architecture diagram saved (white bg)")
