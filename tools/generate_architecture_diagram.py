#!/usr/bin/env python3
"""Generate architecture diagram for MEMORY system (WHITE background, compact layout)."""

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
    "pad": "0.3",
    "dpi": "200",
    "color": "#D2D2D7",
    "ranksep": "0.4",
    "nodesep": "0.3",
}

node_attr = {
    "fontcolor": "#1D1D1F",
    "fontsize": "10",
    "width": "1.0",
    "height": "0.6",
}

cluster_attr = {
    "bgcolor": "#F5F5F7",
    "fontcolor": "#6E6E73",
    "bordercolor": "#D2D2D7",
    "style": "rounded",
    "margin": "10",
}

with Diagram(
    "MEMORY Architecture",
    filename=str(IMAGES / "architecture"),
    outformat="png",
    show=False,
    graph_attr=graph_attr,
    node_attr=node_attr,
    direction="LR",
):

    with Cluster("Agent Tools", graph_attr=cluster_attr):
        claude = User("Claude Code")
        opencode = User("OpenCode")
        cursor = User("Cursor")
        windsurf = User("Windsurf")
        copilot = User("Copilot")

    gemini = LinuxGeneral("GEMINI.md\n(Router)")

    with Cluster("Memory Modules (lazy-loaded)", graph_attr=cluster_attr):
        cols = [
            m1 := Python("01 Core Rules"),
            m2 := Python("02 CLI Tools"),
            m3 := Python("03 ML Eng."),
            m4 := Python("04 Security"),
            m5 := Python("05 UI/UX"),
            m6 := Python("06 Web Dev"),
        ]
        cols2 = [
            m7 := Python("07 Job Hunt"),
            m8 := Python("08 Arch."),
            m9 := Python("09 Misc"),
            m10 := Python("10 Lessons"),
            m11 := Python("11 Errors"),
            m12 := Python("12 Repos"),
        ]

    chroma = Mongodb("ChromaDB\n(Vector Search)")

    agents = [claude, opencode, cursor, windsurf, copilot]
    for a in agents:
        a >> Edge(color="#CC5833", style="dashed", label="symlink") >> gemini

    gemini >> Edge(color="#2E4036", label="lazy") >> cols[0]
    for i in range(len(cols) - 1):
        cols[i] >> Edge(color="#D2D2D7") >> cols[i + 1]
    cols[-1] >> Edge(color="#D2D2D7") >> cols2[0]
    for i in range(len(cols2) - 1):
        cols2[i] >> Edge(color="#D2D2D7") >> cols2[i + 1]

    all_modules = cols + cols2
    for m in all_modules:
        m >> Edge(color="#4A7C6F", style="dotted", label="seed") >> chroma

    chroma >> Edge(color="#2E4036", style="bold", label="search") >> gemini

print("  ✅ Architecture diagram saved (white bg, compact)")
