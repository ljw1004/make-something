#!/usr/bin/env python3
"""Compare independent duration buckets with cumulative views on two numeric axes."""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator

from plot_category_loop_lengths import AREAS, AREA_COLORS, load_area_snapshot
from plot_dataset import configure_style, local_time, np, plt
from plot_time_allocation import duration_hour_groups


def style_axes(ax, xlabel, ylabel):
    ax.set_facecolor("white")
    ax.set_axisbelow(True)
    ax.grid(color="#dddddd", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color("#bfbfbf")
    ax.tick_params(length=0, pad=7, colors="#595959")
    ax.set_xlabel(xlabel, labelpad=12, color="#595959")
    ax.set_ylabel(ylabel, labelpad=12, color="#595959")


def legend(figure, y):
    handles = [Line2D([], [], color=AREA_COLORS[area], marker="o", linewidth=1.5,
                      label=title + (" (includes Other)" if area == "game-engine" else ""))
               for area, title in AREAS.items()]
    figure.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.52, y),
                  ncol=3, frameon=False, labelcolor="#595959", fontsize=10)


def footer(figure, metadata, y):
    snapshot = local_time(metadata["captured_at_utc"])
    figure.text(0.08, y,
                f"Prompts include steers; words include pasted text. {metadata['status_counts']['open']} open loops excluded. Snapshot {snapshot:%d %b %Y}.",
                fontsize=9, color="#7f7f7f")


def bucket_figure(bands, metadata):
    figure = plt.figure(figsize=(12, 8.3), facecolor="white")
    ax = figure.add_axes([0.09, 0.22, 0.87, 0.60])
    style_axes(ax, "Total agentic duration in the bucket (hours)", "Total words in the bucket")
    # Short numeric labels keep the crowded low-duration region legible. Full
    # bucket names and exact values are available on hover in the SVG export.
    offsets = {
        "art": [(-9, 8), (-8, 12), (0, 12), (9, 16), (-2, 9), (5, 7)],
        "story": [(-13, 7), (-8, 15), (10, 12), (0, 20), (0, 20), (0, 16)],
        "game-engine": [(12, 10), (8, 20), (0, 15), (12, -7)],
    }
    details = {}
    for area, rows in bands.items():
        for i, band in enumerate(rows):
            prompts = band["prompts"] + band["steers"]
            if not prompts:
                continue
            gid = f"bucket-{area}-{i}"
            ax.scatter(band["hours"], band["words"], s=prompts * 5,
                       color=AREA_COLORS[area], alpha=0.65, edgecolor="white", linewidth=0.7,
                       zorder=3, gid=gid)
            offset = offsets[area][i] if i < len(offsets[area]) else (0, 15)
            ax.annotate(str(i + 1), (band["hours"], band["words"]), xytext=offset,
                        textcoords="offset points", ha="center", va="center", fontsize=9,
                        color=AREA_COLORS[area], zorder=4)
            details[gid] = (f"{AREAS[area]} · {band['label']} · {band['hours']:.2f} hours · "
                            f"{band['words']:,} words · {prompts} prompts "
                            f"({band['prompts']} initial + {band['steers']} steers)")
    maximum_hours = max(band["hours"] for rows in bands.values() for band in rows)
    maximum_words = max(band["words"] for rows in bands.values() for band in rows)
    ax.set_xlim(-maximum_hours * 0.025, np.ceil(maximum_hours * 1.15))
    ax.set_ylim(0, np.ceil(maximum_words * 1.12 / 1000) * 1000)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    figure.suptitle("Each duration bucket: words and hours", y=0.97, fontsize=16, color="#595959")
    figure.text(0.5, 0.915, "One bubble per area and duration band · bubble area represents prompt count",
                ha="center", fontsize=11, color="#595959")
    legend(figure, 0.888)
    size_handles = [plt.scatter([], [], s=count * 5, color="#a5a5a5", alpha=0.65,
                                edgecolor="white", label=f"{count} prompts") for count in (25, 75, 150)]
    ax.legend(handles=size_handles, loc="upper right", frameon=False, fontsize=9,
              labelspacing=1.6, borderpad=1, labelcolor="#595959")
    figure.text(0.09, 0.105, "1  Under 1m       2  1–5m       3  5–15m       4  15–60m       5  1–3h       6  3h+",
                fontsize=10, color="#595959")
    footer(figure, metadata, 0.05)
    return figure, details


def cumulative_figure(bands, metadata):
    figure, axes = plt.subplots(1, 2, figsize=(13, 7.2), facecolor="white")
    figure.subplots_adjust(left=0.075, right=0.97, bottom=0.22, top=0.77, wspace=0.28)
    details = {}
    for ax, quantity, ylabel in zip(axes, ("words", "messages"), ("Cumulative words", "Cumulative prompts")):
        style_axes(ax, "Cumulative agentic duration (hours)", ylabel)
        maximum_hours = max(sum(band["hours"] for band in rows) for rows in bands.values())
        ax.set_xlim(0, np.ceil(maximum_hours * 1.12))
        ax.xaxis.set_major_locator(MultipleLocator(20))
        for area, rows in bands.items():
            populated = [band for band in rows if band["prompts"]]
            hours = np.cumsum([band["hours"] for band in populated])
            values = np.cumsum([band["words"] if quantity == "words" else band["prompts"] + band["steers"]
                               for band in populated])
            assert np.isclose(hours[-1], sum(band["hours"] for band in rows))
            ax.plot(np.r_[0, hours], np.r_[0, values], color=AREA_COLORS[area], linewidth=1.8, zorder=2)
            for i, (x, y, band) in enumerate(zip(hours, values, populated)):
                gid = f"cumulative-{quantity}-{area}-{i}"
                ax.scatter(x, y, s=28, color=AREA_COLORS[area], edgecolor="white", linewidth=0.5,
                           zorder=3, gid=gid)
                details[gid] = (f"{AREAS[area]} · through {band['label']} · "
                                f"{x:.2f} cumulative hours · {y:,} cumulative {quantity}")
            final = "Game-engine" if area == "game-engine" else AREAS[area]
            ax.annotate(final, (hours[-1], values[-1]), xytext=(0, 11), textcoords="offset points",
                        ha="center", fontsize=10, color=AREA_COLORS[area])
        maximum_value = max(sum(band["words"] if quantity == "words" else band["prompts"] + band["steers"]
                                for band in rows) for rows in bands.values())
        ax.set_ylim(0, maximum_value * 1.17)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    figure.suptitle("How words and prompts accumulate alongside hours", y=0.96, fontsize=16, color="#595959")
    figure.text(0.5, 0.895, "Add duration bands from shortest to longest; each dot is the next running total",
                ha="center", fontsize=11, color="#595959")
    legend(figure, 0.865)
    figure.text(0.075, 0.105, "Duration-band order: Under 1m → 1–5m → 5–15m → 15–60m → 1–3h → 3h+.",
                fontsize=10, color="#595959")
    footer(figure, metadata, 0.05)
    return figure, details


def svg_details(path, details):
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    tree = ET.parse(path)
    found = set()
    for node in tree.getroot().iter():
        gid = node.get("id")
        if gid in details:
            title = ET.Element("{http://www.w3.org/2000/svg}title")
            title.text = details[gid]
            node.insert(0, title)
            found.add(gid)
    assert found == set(details)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def render(dataset, output):
    groups, _, metadata = load_area_snapshot(dataset)
    bands = {area: duration_hour_groups(rows) for area, rows in groups.items()}
    assert sum(band["words"] for rows in bands.values() for band in rows) == metadata["word_count"]["ended_loop_words"]
    output.mkdir(parents=True, exist_ok=True)
    configure_style()
    with plt.rc_context({"text.color": "#595959", "font.size": 10, "savefig.facecolor": "white"}):
        with PdfPages(output / "representation-options.pdf") as pdf:
            for name, builder in [("words-hours-buckets", bucket_figure), ("cumulative-words-prompts-hours", cumulative_figure)]:
                figure, details = builder(bands, metadata)
                figure.savefig(output / f"{name}.png", dpi=180, facecolor="white")
                figure.savefig(output / f"{name}.svg", facecolor="white")
                svg_details(output / f"{name}.svg", details)
                pdf.savefig(figure, facecolor="white")
                plt.close(figure)
    print(f"Two representation sketches saved in {output}; all totals reconciled to the existing snapshot.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    render(args.dataset, args.output or args.dataset / "plots")
