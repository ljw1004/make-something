#!/usr/bin/env python3
"""Render the final message-count chart from the authoritative combined dataset."""

import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from matplotlib.ticker import FuncFormatter
import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent


AREAS = {"art": "Art", "story": "Story", "game-engine": "Game-engine"}
AREA_COLORS = {"art": "#4472c4", "story": "#ed7d31", "game-engine": "#70ad47"}


def style_axes(ax, xlabel, ylabel):
    ax.set_facecolor("white")
    ax.set_axisbelow(True)
    ax.grid(color="#dddddd", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color("#bfbfbf")
    ax.tick_params(length=0, pad=7, colors="#595959")
    ax.set_xlabel(xlabel, labelpad=12, color="#595959")
    ax.set_ylabel(ylabel, labelpad=12, color="#595959")


def load_timed_groups(dataset):
    """Aggregate anonymous initial prompts and their individual steering messages."""
    fields = {"sequence", "source", "area", "word_count", "duration_seconds", "steers"}
    groups = {area: [] for area in AREAS}
    runs = json.loads((dataset / "message-counts.json").read_text())
    if not isinstance(runs, list):
        raise ValueError("Expected a list of runs")
    for index, run in enumerate(runs, start=1):
        if not isinstance(run, dict) or set(run) != fields:
            raise ValueError(f"Unexpected fields in run {index}")
        if type(run["sequence"]) is not int or run["sequence"] != index:
            raise ValueError(f"Expected chronological sequence {index}")
        if run["source"] not in ("codex", "dot") or run["area"] not in groups:
            raise ValueError(f"Unknown source or area in run {index}")
        words, seconds, steers = run["word_count"], run["duration_seconds"], run["steers"]
        if (type(words) is not int or words < 0 or type(seconds) not in (int, float)
                or not math.isfinite(seconds) or seconds < 0 or not isinstance(steers, list)):
            raise ValueError(f"Invalid initial prompt or duration in run {index}")
        previous_delay = 0
        for steer in steers:
            if not isinstance(steer, dict) or set(steer) != {"delay_seconds", "word_count"}:
                raise ValueError(f"Unexpected steer fields in run {index}")
            delay, count = steer["delay_seconds"], steer["word_count"]
            if (type(count) is not int or count < 0 or type(delay) not in (int, float)
                    or not math.isfinite(delay) or not previous_delay <= delay <= seconds):
                raise ValueError(f"Invalid steer count, timing or order in run {index}")
            words += count
            previous_delay = delay
        groups[run["area"]].append({"sequence": run["sequence"], "source": run["source"], "seconds": seconds,
                                    "steers": len(steers), "words": words})
    if any(not rows for rows in groups.values()):
        raise ValueError("The chart requires timed runs in each area")
    return groups


def duration_hour_groups(ranked):
    bounds = [0, 60, 300, 900, 3600, 6 * 3600, np.inf]
    labels = ["Under 1m", "1–5m", "5–15m", "15–60m", "1–6h", "6h+"]
    assert len(bounds) == len(labels) + 1
    hours, counts, steer_counts, word_counts = [], [], [], []
    for low, high in zip(bounds, bounds[1:]):
        subset = [row for row in ranked if low <= row["seconds"] < high]
        counts.append(len(subset))
        steer_counts.append(sum(row["steers"] for row in subset))
        word_counts.append(sum(row["words"] for row in subset))
        hours.append(sum(row["seconds"] for row in subset) / 3600)
    assert sum(counts) == len(ranked)
    assert sum(steer_counts) == sum(row["steers"] for row in ranked)
    assert sum(word_counts) == sum(row["words"] for row in ranked)
    return [{"label": label, "hours": hour, "prompts": count, "steers": steer_count, "words": words}
            for label, hour, count, steer_count, words in zip(labels, hours, counts, steer_counts, word_counts)]


def cumulative_figure(groups):
    # The 6h cutoff includes every Art and Game-engine run without rounding.
    bands = {area: duration_hour_groups(rows) for area, rows in groups.items()}
    # Widen the chart and plotting rectangle by 1.5x, preserving their height.
    figure_width = 6.5 * 1.5
    plot_width = 13 * (0.97 - 0.075) / (2 + 0.28) * 1.5
    plot_height = 7.2 * (0.77 - 0.22)
    figure = plt.figure(figsize=(figure_width, 4.95), facecolor="white")
    ax = figure.add_axes([0.145, 0.15, plot_width / figure_width, plot_height / 4.95])
    style_axes(ax, "Cumulative duration of agentic runs",
               "how many prompts, including mid-run steering prompts")
    maximum_hours = max(sum(band["hours"] for band in rows) for rows in bands.values())
    maximum_prompts = max(sum(band["prompts"] + band["steers"] for band in rows) for rows in bands.values())
    ax.set_xlim(0, np.ceil(maximum_hours * 1.03))
    ax.set_ylim(0, maximum_prompts * 1.17)
    # Stop hour labels/gridlines at 140 while retaining the full Story endpoint.
    ax.set_xticks(np.arange(0, 141, 20))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    area_labels = {
        "art": ((10, 0), "left", "center"),
        "story": ((0, -36), "right", "top"),
        "game-engine": ((-48, 14), "left", "bottom"),
    }
    # These labels describe cumulative duration cutoffs, not each area's maximum.
    # Only the final label rounds the longest duration; intermediate cutoffs
    # use the exact boundaries above.
    longest = max(row["seconds"] for group in groups.values() for row in group)
    longest_label = f"{longest / 3600:.0f}h"
    cutoffs = ["1m", "5m", "15m", "1h", "6h", longest_label]
    label_font = FontProperties(family="DejaVu Sans", size=6.5)
    bounds = [TextPath((0, 0), label, prop=label_font).get_extents()
              for label in cutoffs if len(label) == 2]
    # One size fits the short labels closely; 15m may extend beyond its circle.
    marker_size = (max(np.hypot(box.width, box.height) for box in bounds) + 1.5) ** 2
    for area_index, (area, rows) in enumerate(bands.items()):
        populated = [(i, band) for i, band in enumerate(rows) if band["prompts"]]
        hours = np.cumsum([band["hours"] for _, band in populated])
        prompts = np.cumsum([band["prompts"] + band["steers"] for _, band in populated])
        assert np.isclose(hours[-1], sum(row["seconds"] for row in groups[area]) / 3600)
        assert prompts[-1] == sum(1 + row["steers"] for row in groups[area])
        color = AREA_COLORS[area]
        # Complete each area's line and labeled circles before drawing the next area.
        area_zorder = 2 + area_index * (2 * len(cutoffs) + 1)
        ax.plot(np.r_[0, hours], np.r_[0, prompts], color=color, linewidth=1.8, zorder=area_zorder)
        for x, y, (i, band) in zip(hours, prompts, populated):
            # Draw each circle and its text together so overlapping dots naturally
            # cover earlier dots, including their labels. Keep edge circles whole.
            zorder = area_zorder + 1 + 2 * i
            ax.scatter(x, y, s=marker_size, color=color, edgecolors="none",
                       zorder=zorder, clip_on=False)
            ax.text(x, y, cutoffs[i], ha="center", va="center", fontproperties=label_font,
                    color="white", zorder=zorder + 1, clip_on=False)
        total_words = sum(row["words"] for row in groups[area])
        average = total_words / prompts[-1]
        offset, horizontal, vertical = area_labels[area]
        ax.annotate(f"{AREAS[area]}, {total_words / 1000:.0f}kwords\n(avg {average:.0f} words/prompt)",
                    (hours[-1], prompts[-1]),
                    xytext=offset, textcoords="offset points", ha=horizontal, va=vertical,
                    fontsize=10, color=color, linespacing=1.25,
                    zorder=area_zorder + 2 * len(cutoffs) + 0.5)
    ax.text(0.03, 0.965, "How I prompted", transform=ax.transAxes,
            ha="left", va="top", fontsize=14, color="#595959", zorder=50)
    ax.text(0.03, 0.90, f"Cumulative totals from shortest agentic runs (<1m) to longest ({longest_label})", transform=ax.transAxes,
            ha="left", va="top", fontsize=9.5, color="#595959", zorder=50)
    all_rows = [row for rows in groups.values() for row in rows]
    total_prompts = sum(1 + row["steers"] for row in all_rows)
    total_words = sum(row["words"] for row in all_rows)
    total_hours = sum(row["seconds"] for row in all_rows) / 3600
    ax.text(0.03, 0.845,
            f"Total {total_prompts} prompts, {total_words / 1000:.0f} kwords, {total_hours:.0f}hrs agentic runs",
            transform=ax.transAxes, ha="left", va="top", fontsize=9.5, color="#595959", zorder=50)
    return figure


def render(dataset, output):
    groups = load_timed_groups(dataset)
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 10,
                         "text.color": "#595959", "figure.facecolor": "white",
                         "savefig.facecolor": "white"}):
        figure = cumulative_figure(groups)
        output.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output, dpi=180, facecolor="white")
        plt.close(figure)
    print(f"Saved {output}; all chart totals reconcile to message-counts.json.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATA)
    parser.add_argument("--output", type=Path, default=PROJECT / "message-counts.png")
    args = parser.parse_args()
    render(args.dataset, args.output)
