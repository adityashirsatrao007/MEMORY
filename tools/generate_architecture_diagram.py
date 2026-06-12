#!/usr/bin/env python3
"""Generate architecture diagram for MEMORY system."""

import os
from pathlib import Path
from diagrams import Diagram, Edge, Cluster
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.database import Mongodb
from diagrams.onprem.client import User
from diagrams.programming.language import Python
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.blank import Blank

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "docs" / "images"
os.makedirs(IMAGES, exist_ok=True)

graph_attr = {
    "bgcolor": "#1C1C1E",
    "fontcolor": "#E5E5E7",
    "fontsize": "14",
    "pad": "0.5",
    "dpi": "200",
}

node_attr = {
    "fontcolor": "#E5E5E7",
    "fontsize": "10",
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

    with Cluster("Agent Tools (symlinks to GEMINI.md)", graph_attr={"bgcolor": "#2C2C2E", "fontcolor": "#A1A1A6"}):
        claude = User("Claude Code\nCLAUDE.md")
        opencode = User("OpenCode\nAGENTS.md")
        cursor = User("Cursor\n.cursorrules")
        windsurf = User("Windsurf\n.windsurfrules")
        copilot = User("Copilot\ncopilot-instructions")

    gemini = LinuxGeneral("GEMINI.md\n(Router / Decision Engine)")

    with Cluster("12 Memory Modules (lazy-loaded on demand)", graph_attr={"bgcolor": "#2C2C2E", "fontcolor": "#A1A1A6"}):
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
        a >> Edge(color="#CC5833", style="dashed", label="symlink") >> gemini

    modules = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]
    gemini >> Edge(color="#2E4036", label="lazy load") >> modules[0]
    for i in range(len(modules) - 1):
        modules[i] >> Edge(color="#555557") >> modules[i + 1]

    for m in modules:
        m >> Edge(color="#4A7C6F", style="dotted", label="seed") >> chroma

    chroma >> Edge(color="#57cda4", style="bold", label="search") >> gemini

print("  ✅ Architecture diagram saved")
