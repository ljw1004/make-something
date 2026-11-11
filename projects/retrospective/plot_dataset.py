#!/usr/bin/env python3
"""Render an overview PNG and a five-page PDF from the saved timing snapshot."""

import argparse
from collections import Counter
import csv
from datetime import datetime, timedelta
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import numpy as np


PAPER = "#faf9f6"
INK = "#193641"
MUTED = "#586b72"
GRID = "#dde2df"
COLORS = {"completed": "#287d76", "failed": "#c67727", "interrupted": "#8660a3", "open": "#a9b3b7"}
TZ = ZoneInfo("America/Los_Angeles")
STATUS_LABELS = {"completed": "Completed", "failed": "Failed", "interrupted": "Interrupted", "open": "Open"}


def local_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(TZ)


def duration_label(seconds):
    rounded = round(seconds)
    if rounded < 60:
        return f"{rounded}s"
    if rounded < 3600:
        return f"{rounded // 60}m {rounded % 60:02d}s"
    return f"{rounded // 3600}h {(rounded % 3600) // 60:02d}m"


def style_axis(ax, title, subtitle):
    ax.set_title(title, loc="left", fontsize=14, weight="bold", pad=30, color=INK)
    ax.text(0, 1.035, subtitle, transform=ax.transAxes, fontsize=10, color=MUTED)
    ax.set_facecolor(PAPER)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRID, linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(GRID)
    ax.tick_params(length=0, pad=7)


def duration_axis(ax, max_minutes):
    ax.set_yscale("log")
    ax.set_yticks([1 / 60, 10 / 60, 1, 10, 60, 360], ["1s", "10s", "1m", "10m", "1h", "6h"])
    ax.set_ylim(1 / 60, max(720, max_minutes * 1.3))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis="y", which="minor", length=0)
    ax.set_ylabel("Elapsed duration · logarithmic scale", labelpad=9)


def duration_bands(ax, rows):
    values = np.array([row["seconds"] for row in rows if row["status"] == "completed"])
    counts, _ = np.histogram(values, bins=[0, 60, 300, 900, 3600, 10800, np.inf])
    assert sum(counts) == len(values)
    style_axis(ax, "1  How long do loops last?", f"{len(values):,} completed turns · counts in unequal duration bands")
    bars = ax.bar(range(6), counts, color=COLORS["completed"], width=0.67, zorder=3)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, count + max(counts) * 0.025,
                f"{count}\n{count / len(values):.1%}", ha="center", va="bottom", fontsize=10, color=INK)
    ax.set_xticks(range(6), ["Under 1m", "1–5m", "5–15m", "15–60m", "1–3h", "3h+"])
    ax.set_ylim(0, max(counts) * 1.28)
    ax.set_ylabel("Completed turns")
    ax.set_xlabel("Elapsed duration")


def timeline(ax, rows):
    open_count = sum(row["status"] == "open" for row in rows)
    style_axis(ax, "2  Each loop over time", f"One point per ended turn · {open_count} open turns have no duration")
    for status, marker in [("completed", "o"), ("failed", "X"), ("interrupted", "D")]:
        subset = [row for row in rows if row["status"] == status]
        ax.scatter([row["local_at"] for row in subset], [row["seconds"] / 60 for row in subset],
                   s=19 if status == "completed" else 34, marker=marker, color=COLORS[status],
                   alpha=0.53 if status == "completed" else 0.85, linewidths=0,
                   label=f"{STATUS_LABELS[status]} ({len(subset)})", zorder=3)
    duration_axis(ax, max(row["seconds"] / 60 for row in rows if row["seconds"] is not None))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2, tz=TZ))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d", tz=TZ))
    ax.set_xlim(min(row["local_at"] for row in rows) - timedelta(hours=6),
                max(row["local_at"] for row in rows) + timedelta(hours=6))
    ax.legend(loc="lower right", frameon=True, facecolor=PAPER, edgecolor="none", fontsize=9,
              ncol=3, handletextpad=0.3, columnspacing=0.8)
    ax.set_xlabel("Initial prompt date · Los Angeles time")


def daily_counts(ax, rows):
    first = min(row["local_at"].date() for row in rows)
    last = max(row["local_at"].date() for row in rows)
    days = [first + timedelta(days=i) for i in range((last - first).days + 1)]
    counts = Counter((row["local_at"].date(), row["status"]) for row in rows)
    assert sum(counts.values()) == len(rows)
    style_axis(ax, "3  How many prompts each day?", "Initial prompts only · first and last dates have partial coverage")
    bottom = np.zeros(len(days))
    for status in COLORS:
        heights = np.array([counts[(day, status)] for day in days])
        ax.bar(range(len(days)), heights, bottom=bottom, color=COLORS[status], width=0.72,
               label=STATUS_LABELS[status], zorder=3)
        bottom += heights
    for i, count in enumerate(bottom):
        ax.text(i, count + max(bottom) * 0.025, str(int(count)), ha="center", fontsize=10, color=INK)
    labels = [day.strftime("%b\n%d") for day in days]
    labels[0] += "*"
    labels[-1] += "*"
    ax.set_xticks(range(len(days)), labels)
    ax.set_ylim(0, max(bottom) * 1.26)
    ax.set_ylabel("Initial prompts")
    ax.set_xlabel("Prompt date · Los Angeles time · * partial coverage")
    ax.legend(loc="upper right", ncol=2, frameon=False, fontsize=9)


def steers(ax, rows):
    completed = [row for row in rows if row["status"] == "completed"]
    bands = [(0, 0), (1, 1), (2, 3), (4, 7), (8, float("inf"))]
    groups = [np.array([row["seconds"] / 60 for row in completed if lo <= row["steers"] <= hi])
              for lo, hi in bands]
    assert sum(len(group) for group in groups) == len(completed)
    style_axis(ax, "4  Longer loops often have more steers", "Completed turns · association, not evidence that steers cause longer work")
    rng = np.random.default_rng(20261111)
    for i, group in enumerate(groups):
        if not len(group):
            continue
        q1, median, q3 = np.percentile(group, [25, 50, 75])
        ax.scatter(i + rng.uniform(-0.24, 0.24, len(group)), group, s=16,
                   color=COLORS["completed"], alpha=0.35, linewidths=0, zorder=3)
        ax.vlines(i, q1, q3, color=INK, linewidth=5, alpha=0.65, zorder=4)
        ax.scatter([i], [median], color=INK, edgecolors=PAPER, linewidths=1, s=55, marker="D", zorder=5)
        ax.annotate(duration_label(median * 60), (i, median), xytext=(11, 8), textcoords="offset points",
                    fontsize=10, color=INK, weight="bold", zorder=6,
                    bbox={"boxstyle": "round,pad=0.18", "fc": PAPER, "ec": "none", "alpha": 0.9})
    duration_axis(ax, max(row["seconds"] / 60 for row in completed))
    ax.set_xlim(-0.5, 4.65)
    ax.set_xticks(range(5), [f"{label}\nn = {len(group)}" for label, group in
                            zip(["0 steers", "1 steer", "2–3", "4–7", "8+"], groups)])
    ax.set_xlabel("Dots: individual turns · bars: middle 50% · diamonds: medians")


def load_snapshot(dataset):
    metadata = json.loads((dataset / "metadata.json").read_text())
    with (dataset / "agentic-loops.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["seconds"] = float(row["duration_seconds"]) if row["duration_seconds"] else None
        row["steers"] = int(row["steer_count"])
        row["local_at"] = local_time(row["prompt_at_utc"])
        if (row["seconds"] is None) != (row["status"] == "open"):
            raise ValueError(f"Unexpected missing duration: {row['turn_id']}")
        if row["seconds"] is not None and row["seconds"] <= 0:
            raise ValueError(f"Nonpositive duration cannot use a log axis: {row['turn_id']}")
    assert len(rows) == metadata["initial_prompts"]
    assert dict(Counter(row["status"] for row in rows)) == metadata["status_counts"]
    return rows, metadata


def configure_style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": INK,
                         "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                         "figure.facecolor": PAPER, "savefig.facecolor": PAPER, "pdf.fonttype": 42})


def render(dataset, output):
    rows, metadata = load_snapshot(dataset)
    values = np.array([row["seconds"] for row in rows if row["status"] == "completed"])
    median, p90 = np.percentile(values, [50, 90])
    snapshot = local_time(metadata["captured_at_utc"])
    date_range = f"{min(row['local_at'] for row in rows):%b %d} – {max(row['local_at'] for row in rows):%b %d, %Y}"
    subtitle = f"{len(rows):,} initial prompts · {metadata['conversations']} conversations · {date_range}"
    footnote = "Elapsed time includes tools, waits and steers; simultaneous turns can overlap. Completed is a log outcome, not a quality rating."
    provenance = f"Saved dataset · captured {snapshot:%b %d, %Y at %H:%M %Z} · open turns excluded from duration charts"
    configure_style()
    output.mkdir(parents=True, exist_ok=True)
    overview = plt.figure(figsize=(17, 12.5))
    overview.text(0.065, 0.953, "A closer look at your agentic loops", fontsize=29, weight="bold")
    overview.text(0.065, 0.919, subtitle, fontsize=13, color=MUTED)
    for x, value, label in [
        (0.065, str(len(values)), "completed turns"),
        (0.300, duration_label(median), "median completed duration"),
        (0.535, duration_label(p90), "90th percentile duration"),
        (0.770, duration_label(max(values)), "longest completed loop"),
    ]:
        overview.text(x, 0.867, value, fontsize=24, weight="bold", color=COLORS["completed"])
        overview.text(x, 0.844, label, fontsize=11, color=MUTED)
    grid = overview.add_gridspec(2, 2, left=0.065, right=0.97, bottom=0.115, top=0.765,
                                hspace=0.60, wspace=0.24)
    charts = [duration_bands, timeline, daily_counts, steers]
    for index, draw in enumerate(charts):
        draw(overview.add_subplot(grid[index // 2, index % 2]), rows)
    overview.text(0.065, 0.045, footnote, fontsize=10, color=MUTED)
    overview.text(0.065, 0.025, provenance, fontsize=9, color=MUTED)
    overview.savefig(output / "overview.png", dpi=180)
    with PdfPages(output / "agentic-loops.pdf", metadata={"Title": "Agentic loop retrospective",
                  "Subject": subtitle, "Author": "Make Something Worthwhile"}) as pdf:
        pdf.savefig(overview)
        for draw in charts:
            figure = plt.figure(figsize=(13, 8))
            figure.text(0.09, 0.95, subtitle, fontsize=12, color=MUTED)
            draw(figure.add_axes([0.09, 0.20, 0.86, 0.62]), rows)
            figure.text(0.09, 0.07, footnote, fontsize=9, color=MUTED)
            figure.text(0.09, 0.045, provenance, fontsize=9, color=MUTED)
            pdf.savefig(figure)
            plt.close(figure)
    plt.close(overview)
    print(json.dumps({"rows": len(rows), "completed": len(values),
                      "median_seconds": float(median), "p90_seconds": float(p90),
                      "maximum_seconds": float(max(values)), "completed_over_one_hour": int(sum(values >= 3600)),
                      "outputs": [str(output / "overview.png"), str(output / "agentic-loops.pdf")]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    render(args.dataset, args.output or args.dataset / "plots")
