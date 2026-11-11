#!/usr/bin/env python3
"""Plot agentic hours by loop length for art, story and game-engine (including other)."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

from plot_dataset import configure_style, load_snapshot, local_time, np, plt
from plot_time_allocation import duration_hour_groups, loop_length_figure
from matplotlib.backends.backend_pdf import PdfPages


AREAS = {"art": "Art", "story": "Story", "game-engine": "Game-engine"}
AREA_COLORS = {"art": "#4472c4", "story": "#ed7d31", "game-engine": "#70ad47"}


def combined_loop_length_figure(groups, metadata, x_max):
    """Three colored subrows in each duration band, sharing one hours axis."""
    with plt.rc_context({"figure.facecolor": "white", "savefig.facecolor": "white",
                         "font.family": "DejaVu Sans", "font.size": 11}):
        figure = plt.figure(figsize=(11, 10.8))
        ax = figure.add_axes([0.12, 0.14, 0.85, 0.74])
        ax.set_facecolor("white")
        ax.set_axisbelow(True)
        ax.grid(False)
        ax.grid(axis="x", color="#d9d9d9", linewidth=0.8)
        ax.spines[["top", "right", "bottom"]].set_visible(False)
        ax.spines["left"].set_color("#bfbfbf")
        ax.tick_params(length=0, pad=8, colors="#595959")
        centers = np.arange(6) * 4
        for offset, (area, title) in zip((-1, 0, 1), AREAS.items()):
            bands = duration_hour_groups(groups[area])
            assert np.isclose(sum(band["hours"] for band in bands) * 3600,
                              sum(row["seconds"] for row in groups[area]))
            positions = centers + offset
            label = f"{title} (includes Other)" if area == "game-engine" else title
            ax.barh(positions, [band["hours"] for band in bands], height=0.82,
                    color=AREA_COLORS[area], label=label, zorder=3)
            for y, band in zip(positions, bands):
                prompts, words = band["prompts"] + band["steers"], band["words"]
                counts = f"{prompts:,} {'prompt' if prompts == 1 else 'prompts'}, {words:,} {'word' if words == 1 else 'words'}"
                ax.annotate(counts, (band["hours"], y), xytext=(7, 0), textcoords="offset points",
                            va="center", fontsize=10, color="#404040")
        ax.set_yticks(centers, [band["label"] for band in bands])
        ax.set_ylim(centers[-1] + 1.9, -1.9)
        ax.set_xlim(0, x_max)
        ax.set_xlabel("Total agentic duration (hours)", color="#595959", labelpad=12)
        figure.suptitle("Time by loop length and area", y=0.965, fontsize=16,
                       weight="normal", color="#595959")
        figure.legend(*ax.get_legend_handles_labels(), loc="upper center",
                      bbox_to_anchor=(0.545, 0.928), ncol=3, frameon=False,
                      labelcolor="#595959", fontsize=11)
        ended = [row for group in groups.values() for row in group]
        snapshot = local_time(metadata["captured_at_utc"])
        figure.text(0.12, 0.057,
                    f"{len(ended) + sum(row['steers'] for row in ended):,} prompts · {sum(row['words'] for row in ended):,} words · "
                    f"{metadata['status_counts']['open']} open turns excluded · snapshot {snapshot:%d %b %Y}",
                    fontsize=9, color="#7f7f7f")
        figure.text(0.12, 0.033, "Prompts include steers; words include pasted text. Each loop uses its initial prompt’s primary category.",
                    fontsize=9, color="#7f7f7f")
        return figure


def load_area_snapshot(dataset):
    """Join and validate the classified snapshot, folding Other into Game-engine."""
    rows, metadata = load_snapshot(dataset)
    classification_path = dataset / "prompt-classifications.csv"
    provenance = json.loads((dataset / "classification-metadata.json").read_text())
    for path, expected in [(dataset / "agentic-loops.csv", provenance["source_sha256"]),
                           (classification_path, provenance["classifications_sha256"])]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Source differs from the classified snapshot: {path}")
    with classification_path.open(newline="", encoding="utf-8") as handle:
        labels = list(csv.DictReader(handle))
    by_id = {row["prompt_id"]: row for row in labels}
    if len(by_id) != len(labels) or set(by_id) != {row["prompt_id"] for row in rows}:
        raise ValueError("Classification IDs must uniquely and exactly cover the timing dataset")
    groups = {area: [] for area in AREAS}
    open_counts = {area: 0 for area in AREAS}
    for row in rows:
        category = by_id[row["prompt_id"]]["primary_category"]
        area = "game-engine" if category == "other" else category
        if row["seconds"] is None:
            open_counts[area] += 1
        else:
            groups[area].append(row)
    ended = [row for row in rows if row["seconds"] is not None]
    assert sum(map(len, groups.values())) == len(ended)
    assert sum(open_counts.values()) == metadata["status_counts"]["open"]
    assert sum(row["steers"] for group in groups.values() for row in group) == sum(row["steers"] for row in ended)
    assert sum(row["words"] for group in groups.values() for row in group) == metadata["word_count"]["ended_loop_words"]
    assert np.isclose(sum(row["seconds"] for group in groups.values() for row in group),
                      sum(row["seconds"] for row in ended))
    return groups, open_counts, metadata


def render(dataset, output):
    groups, open_counts, metadata = load_area_snapshot(dataset)
    maximum_band_hours = max(band["hours"] for group in groups.values() for band in duration_hour_groups(group))
    common_x_max = max(10, float(np.ceil(maximum_band_hours * 1.6 / 10) * 10))
    output.mkdir(parents=True, exist_ok=True)
    configure_style()
    pdf_path = output / "time-by-loop-length-by-area.pdf"
    summary = {}
    with PdfPages(pdf_path, metadata={"Title": "Agentic time by loop length and area"}) as pdf:
        for area, title in AREAS.items():
            group = groups[area]
            seconds = sum(row["seconds"] for row in group)
            note = "Primary category per prompt; mixed loops counted once. Same hours scale on all three charts."
            if area == "game-engine":
                note = "Includes Other. Primary category per prompt; mixed loops counted once. Same hours scale on all three charts."
            figure = loop_length_figure(group, seconds, metadata, title=f"{title}: time by loop length",
                                        x_max=common_x_max, open_count=open_counts[area], scope_note=note)
            figure.savefig(output / f"time-by-loop-length-{area}.png", dpi=180, facecolor="white")
            pdf.savefig(figure, facecolor="white")
            plt.close(figure)
            summary[area] = {"plotted_prompts": len(group), "steers": sum(row["steers"] for row in group),
                             "hours": seconds / 3600, "open_turns_excluded": open_counts[area]}
    combined = combined_loop_length_figure(groups, metadata, common_x_max)
    combined_path = output / "time-by-loop-length-combined"
    for extension in ("png", "pdf"):
        combined.savefig(combined_path.with_suffix(f".{extension}"), dpi=180, facecolor="white")
    plt.close(combined)
    print(json.dumps({"areas": summary, "common_axis_max_hours": common_x_max,
                      "pdf": str(pdf_path), "combined_pdf": str(combined_path.with_suffix('.pdf'))}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    render(args.dataset, args.output or args.dataset / "plots")
