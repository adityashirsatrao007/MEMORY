#!/usr/bin/env python3
"""Generate README diagrams with WHITE backgrounds for docs/print."""

from license import require_license
require_license()

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

WHITE = "#FFFFFF"
LIGHT_BG = "#F5F5F7"
TEXT = "#1D1D1F"
MUTED = "#6E6E73"
GRID = "#D2D2D7"
ACCENT1 = "#2E4036"
ACCENT2 = "#CC5833"
ACCENT3 = "#4A7C6F"
ACCENT4 = "#6B4C7A"
ACCENT5 = "#3A6B8C"

plt.rcParams.update({
    "figure.facecolor": WHITE,
    "axes.facecolor": LIGHT_BG,
    "axes.edgecolor": GRID,
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "grid.color": GRID,
    "grid.alpha": 0.5,
    "font.family": "sans-serif",
    "font.size": 11,
})


def generate_token_savings():
    fig, ax = plt.subplots(figsize=(10, 5.5))

    labels = ["Old Monolithic\nGEMINI.md", "Full Mode\n(Core + CLI + Task)", "Lazy Mode\n(Vector Search)"]
    values = [3622, 1420, 200]
    savings = [0, 60, 95]
    colors = [ACCENT2, ACCENT1, ACCENT3]

    bars = ax.bar(labels, values, color=colors, width=0.55, edgecolor=GRID, linewidth=0.8)

    for bar, val, save in zip(bars, values, savings):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 80,
                f"{val} lines", ha="center", va="bottom",
                fontsize=13, fontweight="bold", color=TEXT)
        if save > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                    f"−{save}%", ha="center", va="center",
                    fontsize=16, fontweight="bold", color=WHITE,
                    bbox=dict(boxstyle="round,pad=0.3",
                              facecolor=TEXT, edgecolor="none", alpha=0.7))

    ax.set_ylabel("Lines Loaded Per Session", fontsize=12, fontweight="semibold")
    ax.set_title("Token Economics: Lines per Session by Mode", fontsize=15, fontweight="bold",
                 pad=16, color=TEXT)
    ax.set_ylim(0, 4400)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
    ax.tick_params(axis="x", labelsize=10)

    fig.tight_layout()
    path = IMAGES / "token-savings.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"  ✅ {path}")


def generate_module_sizes():
    fig, ax = plt.subplots(figsize=(10, 6.5))

    modules = [
        ("01 Core Rules", 115, ACCENT2),
        ("02 CLI Tools", 160, ACCENT1),
        ("03 ML Engineering", 292, ACCENT3),
        ("04 Security", 147, "#8B4513"),
        ("05 UI/UX", 274, ACCENT4),
        ("06 Web Dev", 305, ACCENT5),
        ("07 Job Hunt", 145, "#5A6B5A"),
        ("08 Architecture", 198, "#7A6B4A"),
        ("09 Misc", 255, "#6B5A4A"),
        ("10 Lessons Learned", 17, MUTED),
        ("11 Error Logs", 30, MUTED),
        ("12 Architectural Patterns", 107, "#4A6B7A"),
    ]

    names = [m[0] for m in modules]
    lines = [m[1] for m in modules]
    colors = [m[2] for m in modules]

    bars = ax.barh(names, lines, color=colors, height=0.6, edgecolor=GRID, linewidth=0.6)
    ax.set_xlabel("Lines", fontsize=12, fontweight="semibold")
    ax.set_title("Module Sizes (lines of instructions)", fontsize=15, fontweight="bold",
                 pad=16, color=TEXT)
    ax.invert_yaxis()

    for bar, val in zip(bars, lines):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                str(val), ha="left", va="center", fontsize=10, color=MUTED)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, 380)
    ax.tick_params(axis="y", labelsize=9)

    fig.tight_layout()
    path = IMAGES / "module-sizes.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"  ✅ {path}")


def generate_cost_comparison():
    fig, ax = plt.subplots(figsize=(10, 5))

    models = ["Claude Sonnet\n(per call)", "Gemini Flash\n(per call)", "Local Ollama\n(per call)",
              "freellmapi\n(per call)", "MEMORY Lazy\n(per session)", "MEMORY Full\n(per session)"]
    costs = [0.003, 0.00015, 0.00001, 0.00000, 0.00000, 0.00000]
    colors = [ACCENT2, ACCENT2, ACCENT3, ACCENT1, ACCENT1, ACCENT1]

    ax.bar(models, costs, color=colors, width=0.5, edgecolor=GRID, linewidth=0.6)
    ax.set_ylabel("Cost (USD)", fontsize=12, fontweight="semibold")
    ax.set_title("Cost Per Call/Session", fontsize=15, fontweight="bold",
                 pad=16, color=TEXT)
    ax.set_yscale("log")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=8)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.4f"))

    for bar, val in zip(ax.patches, costs):
        if val == 0:
            ax.text(bar.get_x() + bar.get_width() / 2, 0.000005,
                    "FREE", ha="center", va="bottom",
                    fontsize=11, fontweight="bold", color=ACCENT3)

    fig.tight_layout()
    path = IMAGES / "cost-comparison.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"  ✅ {path}")


def generate_benchmark_horizontal():
    fig, ax = plt.subplots(figsize=(10, 5.5))

    metrics = [
        "Session Init (lazy)",
        "Session Init (full)",
        "Vector Search (avg)",
        "Module Load (avg)",
        "Full Audit Cycle",
    ]
    times = [0.3, 1.5, 0.8, 0.4, 4.2]
    savings_vs_old = [92, 60, 0, 0, 80]

    x = np.arange(len(metrics))
    width = 0.35

    bars = ax.bar(x, times, width, color=[ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5],
                  edgecolor=GRID, linewidth=0.6)

    ax.set_ylabel("Time (seconds)", fontsize=12, fontweight="semibold")
    ax.set_title("Benchmark: MEMORY Agent Performance Metrics", fontsize=15, fontweight="bold",
                 pad=16, color=TEXT)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, val, save in zip(bars, times, savings_vs_old):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{val}s" + (f" (-{save}%)" if save > 0 else ""),
                ha="center", va="bottom", fontsize=9, fontweight="bold", color=TEXT)

    fig.tight_layout()
    path = IMAGES / "benchmark-times.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"  ✅ {path}")


def generate_stacked_savings():
    fig, ax = plt.subplots(figsize=(8, 5))

    categories = ["Per Session\nToken Cost", "Time to\nFirst Action", "Memory\nFootprint", "Context\nQuality"]
    old = [100, 100, 100, 30]
    new = [5, 8, 12, 95]

    x = np.arange(len(categories))
    width = 0.3

    ax.bar(x - width / 2, old, width, label="Old Monolithic", color=ACCENT2, edgecolor=GRID, linewidth=0.6)
    ax.bar(x + width / 2, new, width, label="MEMORY Modular", color=ACCENT1, edgecolor=GRID, linewidth=0.6)

    ax.set_ylabel("Score (100 = best)", fontsize=12, fontweight="semibold")
    ax.set_title("Before vs After: MEMORY System Impact", fontsize=15, fontweight="bold",
                 pad=16, color=TEXT)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.legend(fontsize=10, facecolor=WHITE, edgecolor=GRID)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 120)

    fig.tight_layout()
    path = IMAGES / "before-after.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"  ✅ {path}")


def main():
    print("🎨 Generating README diagrams (white bg)...")
    generate_token_savings()
    generate_module_sizes()
    generate_cost_comparison()
    generate_benchmark_horizontal()
    generate_stacked_savings()
    print(f"\n📁 All saved to {IMAGES}/")


if __name__ == "__main__":
    main()
