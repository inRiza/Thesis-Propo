#!/usr/bin/env python3
"""Generate accurate first-order vs MOGen comparison figure (Gote et al., 2023)."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "chapter-2-first-order-vs-mogen.pdf"

ORANGE_FILL = "#FFE0B2"
ORANGE_EDGE = "#E65100"
GRAY_EDGE = "#616161"
PANEL_EDGE = "#BDBDBD"
TEXT = "#212121"
MUTED = "#616161"


def draw_panel(ax, xy, wh, title):
    x, y = xy
    w, h = wh
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.2,
            edgecolor=PANEL_EDGE,
            facecolor="white",
            mutation_aspect=1,
            zorder=0,
        )
    )
    ax.text(
        x + 0.12,
        y + h - 0.18,
        title,
        fontsize=10,
        fontweight="bold",
        color=MUTED,
        ha="left",
        va="top",
        zorder=2,
    )


def draw_node(ax, xy, label, *, highlight=False, dashed=False, r=0.28):
    face = ORANGE_FILL if highlight else "white"
    edge = ORANGE_EDGE if highlight else GRAY_EDGE
    ls = "--" if dashed else "-"
    ax.add_patch(
        Circle(
            xy,
            r,
            facecolor=face,
            edgecolor=edge,
            linewidth=1.8,
            linestyle=ls,
            zorder=3,
        )
    )
    ax.text(
        xy[0],
        xy[1],
        label,
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="center",
        color=TEXT,
        zorder=4,
    )


def draw_edge(ax, p, q, *, color=GRAY_EDGE, arrow=False, label=None, label_offset=(0, 0.18)):
    style = "->" if arrow else "-"
    ax.annotate(
        "",
        xy=q,
        xytext=p,
        arrowprops=dict(
            arrowstyle=style,
            color=color,
            lw=1.6,
            shrinkA=14,
            shrinkB=14,
            mutation_scale=12,
        ),
        zorder=2,
    )
    if label:
        mx = (p[0] + q[0]) / 2 + label_offset[0]
        my = (p[1] + q[1]) / 2 + label_offset[1]
        ax.text(
            mx,
            my,
            label,
            fontsize=8,
            color=MUTED,
            ha="center",
            va="center",
            zorder=5,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.92),
        )


def main():
    fig, ax = plt.subplots(figsize=(7.6, 4.0), dpi=200)
    ax.set_xlim(0, 15.2)
    ax.set_ylim(0, 8.0)
    ax.set_aspect("equal")
    ax.axis("off")

    # --- Panel (a): first-order dyadic graph ---
    draw_panel(ax, (0.3, 0.7), (6.6, 6.8), "(a) Graf orde-pertama (dyadic)")

    # equilateral-ish triangle, generous spacing
    a = np.array([3.55, 5.15])
    b = np.array([1.95, 2.95])
    c = np.array([5.15, 2.95])
    draw_node(ax, a, "A", r=0.30)
    draw_node(ax, b, "B", r=0.30)
    draw_node(ax, c, "C", r=0.30)

    # undirected edges — no sequential path labels (conceptually correct)
    draw_edge(ax, a, b)
    draw_edge(ax, a, c)
    draw_edge(ax, b, c)

    ax.text(
        4,
        1.45,
        f"Interaksi digabung jadi tepi berpasangan;\nurutan langkah hilang tanpa adanya \textit{state} yang menyimpan.",
        fontsize=7.5,
        color=MUTED,
        ha="center",
        va="center",
        linespacing=1.55,
    )

    # --- Panel (b): MOGen path --- 
    draw_panel(ax, (7.35, 0.7), (7.5, 6.8), "(b) Jalur MOGen (orde-K)")

    y = 4.05
    xs = [8.35, 9.75, 11.15, 12.55, 13.95]
    labels = ["S0", "A", "B", "C", "St"]
    steps = ["C1", "C2", "C3", ""]

    for i, (x, lab) in enumerate(zip(xs, labels)):
        highlight = lab in {"A", "B", "C"}
        dashed = lab in {"S0", "St"}
        draw_node(ax, (x, y), lab, highlight=highlight, dashed=dashed, r=0.28)

    for i in range(len(xs) - 1):
        draw_edge(
            ax,
            (xs[i], y),
            (xs[i + 1], y),
            color=ORANGE_EDGE,
            arrow=True,
            label=steps[i] if steps[i] else None,
            label_offset=(0, 0.58),
        )

    ax.text(
        11.15,
        1.45,
        "Urutan jalur disimpan sebagai path data.\nKeadaan awal S0 dan target Starget eksplisit.",
        fontsize=7.5,
        color=MUTED,
        ha="center",
        va="center",
        linespacing=1.55,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, format="pdf", bbox_inches="tight", pad_inches=0.08)
    # also png for quick preview
    fig.savefig(OUT.with_suffix(".png"), format="png", bbox_inches="tight", pad_inches=0.08, dpi=200)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
