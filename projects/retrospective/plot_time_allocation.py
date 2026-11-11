#!/usr/bin/env python3
"""Visualize the sum of recorded agentic duration, partitioned among initial prompts."""

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from plot_dataset import (
    COLORS, INK, MUTED, PAPER, configure_style, duration_label,
    load_snapshot, local_time, np, plt, style_axis,
)
from matplotlib.patches import Patch, Rectangle


STEER_COLORS = ["#dce7e9", "#a8cfcb", "#72aaa4", "#367e78", "#174d49"]
STEER_LABELS = ["0 steers", "1 steer", "2–3 steers", "4–7 steers", "8+ steers"]


def steer_band(count):
    return 0 if count == 0 else 1 if count == 1 else 2 if count <= 3 else 3 if count <= 7 else 4


def treemap(items, x, y, width, height):
    """A binary treemap: split on the long side near half the remaining duration."""
    if len(items) == 1:
        return [(items[0], x, y, width, height)]
    cumulative = np.cumsum([row["seconds"] for row in items])
    split = int(np.argmin(abs(cumulative[:-1] - cumulative[-1] / 2))) + 1
    fraction = cumulative[split - 1] / cumulative[-1]
    if width >= height:
        return (treemap(items[:split], x, y, width * fraction, height)
                + treemap(items[split:], x + width * fraction, y, width * (1 - fraction), height))
    return (treemap(items[:split], x, y, width, height * fraction)
            + treemap(items[split:], x, y + height * fraction, width, height * (1 - fraction)))


def draw_prompts(ax, ranked, total):
    width, height = 100, 30
    tiles = treemap(ranked, 0, 0, width, height)
    assert len(tiles) == len(ranked)
    assert np.isclose(sum(w * h for _, _, _, w, h in tiles), width * height)
    for row, x, y, w, h in tiles:
        assert np.isclose(w * h / (width * height), row["seconds"] / total)
        assert x >= 0 and y >= 0 and x + w <= width + 1e-9 and y + h <= height + 1e-9
        band = steer_band(row["steers"])
        rectangle = Rectangle((x, y), w, h, facecolor=STEER_COLORS[band], edgecolor=PAPER,
                              linewidth=0.45, gid=f"prompt-{row['prompt_id']}")
        ax.add_patch(rectangle)
        # Labels are decoration; tiny prompts retain their actual area and stay unlabeled.
        if row["rank"] <= 12 and w >= 5.5 and h >= 3:
            color = INK if band < 3 else "#ffffff"
            label = f"#{row['rank']}\n{duration_label(row['seconds'])}\n{row['steers']} steers"
            ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=10,
                    weight="bold", color=color, linespacing=1.6, clip_on=True)
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.set_aspect("equal")
    ax.axis("off")


def duration_hour_groups(ranked):
    bounds = [0, 60, 300, 900, 3600, 10800, np.inf]
    labels = ["Under 1m", "1–5m", "5–15m", "15–60m", "1–3h", "3h+"]
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


def draw_duration_hours(ax, ranked, total, *, title="Time by loop length", x_max=None):
    groups = duration_hour_groups(ranked)
    hours = [group["hours"] for group in groups]
    assert np.isclose(sum(hours) * 3600, total)
    ax.set_title(title, fontsize=16, weight="normal", color="#595959", pad=18)
    ax.set_facecolor("white")
    ax.set_axisbelow(True)
    ax.grid(False)
    ax.grid(axis="x", color="#d9d9d9", linewidth=0.8)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.spines["left"].set_color("#bfbfbf")
    ax.tick_params(length=0, pad=8, colors="#595959")
    ax.barh(range(6), hours, color="#4472c4", height=0.58, zorder=3)
    for i, group in enumerate(groups):
        prompts, steers = group["prompts"], group["steers"]
        label = f"{prompts} {'prompt' if prompts == 1 else 'prompts'} + {steers} {'steer' if steers == 1 else 'steers'}"
        ax.annotate(label, (group["hours"], i),
                    xytext=(7, 0), textcoords="offset points", va="center", fontsize=10, color="#404040")
    ax.set_yticks(range(6), [group["label"] for group in groups], fontsize=11)
    ax.invert_yaxis()
    ax.set_xlim(0, x_max if x_max is not None else max(10, np.ceil(max(hours) * 1.6 / 10) * 10))
    ax.set_xlabel("Total agentic duration (hours)", color="#595959", labelpad=12)


def loop_length_figure(ranked, total, metadata, *, title="Time by loop length", x_max=None,
                       open_count=None, scope_note=None):
    """A plain standalone bar chart, with counts decorating the measured hours."""
    with plt.rc_context({"figure.facecolor": "white", "savefig.facecolor": "white",
                         "font.family": "DejaVu Sans", "font.size": 11}):
        figure = plt.figure(figsize=(11, 6.5))
        draw_duration_hours(figure.add_axes([0.12, 0.17, 0.85, 0.70]), ranked, total, title=title, x_max=x_max)
        snapshot = local_time(metadata["captured_at_utc"])
        if open_count is None:
            open_count = metadata['status_counts']['open']
        figure.text(0.12, 0.06 if scope_note else 0.045,
                    f"{len(ranked)} prompts · {sum(row['steers'] for row in ranked)} steers · "
                    f"{open_count} open {'turn' if open_count == 1 else 'turns'} excluded · snapshot {snapshot:%d %b %Y}",
                    fontsize=9, color="#7f7f7f")
        if scope_note:
            figure.text(0.12, 0.028, scope_note, fontsize=9, color="#7f7f7f")
        return figure


def render_loop_length(output, ranked, total, metadata):
    figure = loop_length_figure(ranked, total, metadata)
    for extension in ("png", "pdf"):
        figure.savefig(output / f"time-by-loop-length.{extension}", dpi=180, facecolor="white")
    plt.close(figure)


def draw_concentration(ax, ranked, total):
    cumulative = np.cumsum([row["seconds"] for row in ranked]) / 3600
    total_hours = total / 3600
    style_axis(ax, "How concentrated is the time?", "Accumulate the longest prompt first, then the next longest")
    ax.fill_between(np.arange(len(ranked) + 1), np.r_[0, cumulative], color="#e0ece8", zorder=2)
    ax.plot(np.arange(len(ranked) + 1), np.r_[0, cumulative], color=COLORS["completed"], linewidth=2.3, zorder=3)
    for share, location in [(0.5, (0.20, 0.29)), (0.8, (0.44, 0.56)), (0.9, (0.70, 0.78))]:
        count = int(np.searchsorted(cumulative, total_hours * share)) + 1
        value = cumulative[count - 1]
        ax.scatter([count], [value], color=INK, s=30, zorder=4)
        ax.annotate(f"{count} prompts\n{value:.1f}h · {value / total_hours:.1%}", (count, value),
                    xytext=location, textcoords="axes fraction", fontsize=10, color=INK,
                    arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.7},
                    bbox={"boxstyle": "round,pad=0.2", "fc": PAPER, "ec": "none"})
    ax.set_xlim(0, len(ranked))
    ax.set_ylim(0, total_hours * 1.10)
    ax.axhline(total_hours, color=MUTED, linewidth=0.6, linestyle=":")
    ax.text(len(ranked) * 0.99, total_hours * 1.025, f"All {total_hours:.1f}h", ha="right", fontsize=10, color=MUTED)
    ax.set_ylabel("Accumulated agentic hours")
    ax.set_xlabel("Number of prompts, ranked longest first")


def add_svg_titles(path, ranked, total):
    """Keep the exported chart standalone, with native browser hover details per prompt."""
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    tree = ET.parse(path)
    by_id = {f"prompt-{row['prompt_id']}": row for row in ranked}
    found = set()
    for element in tree.iter():
        row = by_id.get(element.get("id"))
        if row is None:
            continue
        found.add(row["prompt_id"])
        title = ET.Element("{http://www.w3.org/2000/svg}title")
        excerpt = " ".join(row["prompt_text"].replace("\\n", " ").split())
        if len(excerpt) > 700:
            excerpt = excerpt[:697] + "…"
        title.text = (f"#{row['rank']} · {duration_label(row['seconds'])} · {row['seconds'] / total:.2%} of total\n"
                      f"{row['steers']} steers · {row['status']} · {row['local_at']:%b %d, %Y %H:%M %Z}\n"
                      f"{row['conversation_title']}\n{excerpt}\nPrompt ID: {row['prompt_id']}")
        element.insert(0, title)
    assert len(found) == len(ranked)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def render(dataset, output):
    rows, metadata = load_snapshot(dataset)
    ranked = sorted((row for row in rows if row["seconds"] is not None),
                    key=lambda row: (-row["seconds"], row["prompt_id"]))
    for rank, row in enumerate(ranked, 1):
        row["rank"] = rank
    total = sum(row["seconds"] for row in ranked)
    cumulative = np.cumsum([row["seconds"] for row in ranked])
    halfway_count = int(np.searchsorted(cumulative, total / 2)) + 1
    halfway_share = cumulative[halfway_count - 1] / total
    steer_hours = [sum(row["seconds"] for row in ranked if steer_band(row["steers"]) == band) / 3600
                   for band in range(5)]
    status_hours = {status: sum(row["seconds"] for row in ranked if row["status"] == status) / 3600
                    for status in ("completed", "failed", "interrupted")}
    assert np.isclose(sum(steer_hours) * 3600, total)
    assert np.isclose(sum(status_hours.values()) * 3600, total)
    configure_style()
    figure = plt.figure(figsize=(17, 13))
    figure.text(0.055, 0.952, f"How {total / 3600:.1f} agentic hours split across prompts", fontsize=28, weight="bold")
    figure.text(0.055, 0.917, f"All recorded durations · {len(ranked)} initial prompts with an end event · "
                f"{len(rows) - len(ranked)} open turns excluded", fontsize=13, color=MUTED)
    figure.text(0.055, 0.866, f"The longest {halfway_count} prompts account for {halfway_share:.1%} of all recorded time.",
                fontsize=18, weight="bold", color=COLORS["completed"])
    figure.text(0.055, 0.820, "Every rectangle is one initial prompt. Its area is its share of the total duration. Color shows steer count.",
                fontsize=12, color=MUTED)
    draw_prompts(figure.add_axes([0.055, 0.45, 0.91, 0.35]), ranked, total)
    figure.legend([Patch(facecolor=color) for color in STEER_COLORS],
                  [f"{label} · {hours:.1f}h" for label, hours in zip(STEER_LABELS, steer_hours)],
                  loc="center", bbox_to_anchor=(0.51, 0.422), ncol=5, frameon=False, fontsize=11,
                  handlelength=1.4, columnspacing=1.8)
    draw_duration_hours(figure.add_axes([0.155, 0.14, 0.305, 0.215]), ranked, total)
    draw_concentration(figure.add_axes([0.60, 0.14, 0.36, 0.215]), ranked, total)
    figure.text(0.055, 0.077, "Included time: " + " · ".join(f"{status} {hours:.1f}h" for status, hours in status_hours.items())
                + ". These are log outcomes, not quality ratings.", fontsize=10, color=MUTED)
    figure.text(0.055, 0.052, "Durations include tools, waits and steers. Overlapping loops are summed separately; this is not compute time or human working hours.",
                fontsize=10, color=MUTED)
    snapshot = local_time(metadata["captured_at_utc"])
    figure.text(0.055, 0.028, f"Saved dataset · captured {snapshot:%b %d, %Y at %H:%M %Z} · "
                "rectangle numbers rank prompts by duration; open the SVG in a browser for prompt details on hover", fontsize=9, color=MUTED)
    output.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(output / f"time-allocation.{extension}", dpi=180)
    plt.close(figure)
    add_svg_titles(output / "time-allocation.svg", ranked, total)
    render_loop_length(output, ranked, total, metadata)
    print(json.dumps({"ended_prompts": len(ranked), "total_hours": total / 3600,
                      "prompts_reaching_half": halfway_count, "their_duration_share": float(halfway_share),
                      "status_hours": status_hours, "steer_group_hours": steer_hours,
                      "outputs": [str(output / f"time-allocation.{ext}") for ext in ("png", "pdf", "svg")]
                                 + [str(output / f"time-by-loop-length.{ext}") for ext in ("png", "pdf")]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    render(args.dataset, args.output or args.dataset / "plots")
