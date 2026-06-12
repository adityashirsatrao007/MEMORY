#!/usr/bin/env python3
"""Generate README diagrams: architecture, token savings, module sizes."""

import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "docs" / "images"

os.makedirs(IMAGES, exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "#1C1C1E",
    "axes.facecolor": "#2C2C2E",
    "axes.edgecolor": "#555557",
    "axes.labelcolor": "#E5E5E7",
    "text.color": "#E5E5E7",
    "xtick.color": "#A1A1A6",
    "ytick.color": "#A1A1A6",
    "grid.color": "#3A3A3C",
    "grid.alpha": 0.3,
    "font.family": "sans-serif",
    "font.size": 11,
})


def generate_token_savings():
    fig, ax = plt.subplots(figsize=(10, 5.5))

    labels = ["Old Monolithic\nGEMINI.md", "Full Mode\n(Core + CLI + Task)", "Lazy Mode\n(Vector Search)"]
    values = [3622, 1420, 200]
    savings = [0, 60, 95]
    colors = ["#CC5833", "#2E4036", "#4A7C6F"]

    bars = ax.bar(labels, values, color=colors, width=0.55, edgecolor="#3A3A3C", linewidth=0.8)

    for bar, val, save in zip(bars, values, savings):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 80,
                f"{val} lines", ha="center", va="bottom",
                fontsize=13, fontweight="bold", color="#E5E5E7")
        if save > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                    f"−{save}%", ha="center", va="center",
                    fontsize=16, fontweight="bold", color="#FFFFFF",
                    bbox=dict(boxstyle="round,pad=0.3",
                              facecolor="#1C1C1E", edgecolor="none", alpha=0.6))

    ax.set_ylabel("Lines Loaded Per Session", fontsize=12, fontweight="semibold")
    ax.set_title("Token Economics: Lines per Session by Mode", fontsize=15, fontweight="bold",
                 pad=16, color="#FFFFFF")
    ax.set_ylim(0, 4400)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
    ax.tick_params(axis="x", labelsize=10)

    fig.tight_layout()
    path = IMAGES / "token-savings.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✅ {path}")


def generate_module_sizes():
    fig, ax = plt.subplots(figsize=(10, 6.5))

    modules = [
        ("01 Core Rules", 115, "session"),
        ("02 CLI Tools", 160, "tools"),
        ("03 ML Engineering", 292, "ml"),
        ("04 Security", 147, "security"),
        ("05 UI/UX", 274, "design"),
        ("06 Web Dev", 305, "web"),
        ("07 Job Hunt", 145, "career"),
        ("08 Architecture", 198, "arch"),
        ("09 Misc", 255, "misc"),
        ("10 Lessons", 17, "core"),
        ("11 Error Logs", 30, "core"),
        ("12 Repo Teachings", 107, "ref"),
    ]

    domain_colors = {
        "session": "#CC5833",
        "tools": "#2E4036",
        "ml": "#4A7C6F",
        "security": "#8B4513",
        "design": "#6B4C7A",
        "web": "#3A6B8C",
        "career": "#5A6B5A",
        "arch": "#7A6B4A",
        "misc": "#6B5A4A",
        "core": "#555557",
        "ref": "#4A6B7A",
    }

    names = [m[0] for m in modules]
    lines = [m[1] for m in modules]
    colors = [domain_colors[m[2]] for m in modules]

    bars = ax.barh(names, lines, color=colors, height=0.6, edgecolor="#3A3A3C", linewidth=0.6)
    ax.set_xlabel("Lines", fontsize=12, fontweight="semibold")
    ax.set_title("Module Sizes (lines of instructions)", fontsize=15, fontweight="bold",
                 pad=16, color="#FFFFFF")
    ax.invert_yaxis()

    for bar, val in zip(bars, lines):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                str(val), ha="left", va="center", fontsize=10, color="#A1A1A6")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, 380)
    ax.tick_params(axis="y", labelsize=9)

    fig.tight_layout()
    path = IMAGES / "module-sizes.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✅ {path}")


def generate_cost_comparison():
    fig, ax = plt.subplots(figsize=(10, 5))

    models = ["Claude Sonnet\n(per call)", "Gemini Flash\n(per call)", "Local Ollama\n(per call)",
              "freellmapi\n(per call)", "MEMORY Lazy\n(per session)", "MEMORY Full\n(per session)"]
    costs = [0.003, 0.00015, 0.00001, 0.00000, 0.00000, 0.00000]
    colors = ["#CC5833", "#CC5833", "#4A7C6F", "#2E4036", "#2E4036", "#2E4036"]

    ax.bar(models, costs, color=colors, width=0.5, edgecolor="#3A3A3C", linewidth=0.6)
    ax.set_ylabel("Cost (USD)", fontsize=12, fontweight="semibold")
    ax.set_title("Cost Per Call/Session", fontsize=15, fontweight="bold",
                 pad=16, color="#FFFFFF")
    ax.set_yscale("log")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=8)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.4f"))

    for i, (bar, val) in enumerate(zip(ax.patches, costs)):
        if val == 0:
            ax.text(bar.get_x() + bar.get_width() / 2, 0.000005,
                    "FREE", ha="center", va="bottom",
                    fontsize=11, fontweight="bold", color="#57cda4")

    fig.tight_layout()
    path = IMAGES / "cost-comparison.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✅ {path}")


def main():
    print("🎨 Generating README diagrams...")
    generate_token_savings()
    generate_module_sizes()
    generate_cost_comparison()
    print(f"\n📁 All saved to {IMAGES}/")


if __name__ == "__main__":
    main()
