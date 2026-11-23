# Message data and reproduction

**`message-counts.json` is the sole authoritative input to the chart.** It preserves 1,072 plotted runs and their 1,853 human messages, including 781 steers. Runs appear in initial-prompt order, numbered `sequence: 1` through `1072` across Codex, Dot and ChatGPT. Each run contains the initial prompt's word count, the whole run's duration, and an ordered list of its steers with their individual word counts and relative arrival times. [Dataset](message-counts.json) · [Chart](../message-counts.png)

For example, this illustrative record represents a two-hour Story run with a 40-word initial prompt and two steers:

```json
{
  "sequence": 42,
  "source": "codex",
  "area": "story",
  "word_count": 40,
  "duration_seconds": 7200,
  "steers": [
    {"delay_seconds": 120, "word_count": 12},
    {"delay_seconds": 1800, "word_count": 25}
  ]
}
```

The first steer arrived two minutes after the initial prompt, and the second arrived thirty minutes after it. These are delays from the initial prompt, not gaps between steers. This example contributes three messages, 77 words and two hours. Duration belongs to the whole run and is not repeated for each steer. A run without steers has an empty list.

| Field | Meaning |
|---|---|
| `sequence` | Chronological rank of this initial prompt among the retained timed runs across sources. `1` came first. |
| `source` | `codex` for local sessions, `dot` for the earlier Dot dataset, or `chatgpt` for the account export. |
| `area` | The initial prompt's `art`, `story` or `game-engine` area. The original Other category is included in Game-engine. |
| `word_count` | Human-written words in the **initial prompt only**. |
| `duration_seconds` | Elapsed duration of the whole run, counted once. |
| `steers` | Subsequent human messages belonging to this run, in arrival order. |
| `steers[].delay_seconds` | Seconds from the initial prompt's logged arrival to this steer. It is a relative elapsed interval, not a timestamp or time of day. |
| `steers[].word_count` | Human-written words in this individual steer. |

Codex grouping follows recorded turns. Dot and ChatGPT grouping follows reviewed response intervals. Each steer retains its own arrival delay even when it introduced a different request. The whole run takes the area of its initial request.

There are no message contents, replies, attachments, dates, timestamps, time-of-day fields, original message or conversation identifiers, or model rationales. The sequence preserves which initial prompt came first, without retaining when it was sent or the gap between runs. It does not number steers or imply completion order: separate runs can overlap. Within each run, steer order and relative delays are preserved. Only runs with usable durations are included, and the sequence has no gaps for omitted runs. The earlier consolidated CSV has been removed to keep one authoritative input.

The audited data totals **781 steers, 1,853 messages, 124,992 words and 265.4215815556 hours**. The main README gives totals by source and area and defines the counting and timing rules. [Chart explanation](../README.md)

To generate the JSON from private conversation sources, follow [Generating message-counts.json](../README.md#generating-message-countsjson). That procedure covers extraction, attachment audits, Luna classification and Dot response-boundary review, chronology and anonymization. The original extraction scripts and private review inputs are not retained here; the commands below redraw the chart from the existing JSON.

## Redraw the chart

[plot_message_counts.py](plot_message_counts.py) validates the allowed fields, consecutive sequence numbers, source/category labels, nonnegative word counts, and ordered steer delays within each run's duration. It then derives run word totals and steer counts from the individual messages and checks that every duration bucket conserves them. It draws the final PNG at 1755 × 891 with linear scales; its cumulative ordering still follows run duration rather than chronology.

Run these commands from the repository root:

```sh
python3 -m venv runs/retrospective-plot-venv
runs/retrospective-plot-venv/bin/python -m pip install -r "archive/2026.11.11 message counts/sources/requirements.txt"
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B "archive/2026.11.11 message counts/sources/plot_message_counts.py"
```

The default output is `archive/2026.11.11 message counts/message-counts.png`. Use `--dataset` to select another directory containing `message-counts.json`, or `--output runs/retrospective-preview.png` for a temporary preview. The virtual environment, font cache and previews are disposable scratch material.

The 23 November refresh preserved each baseline run's measurements and recomputed its sequence from recovered start times to accommodate earlier ChatGPT runs. The generation procedure records the source inputs and review steps. [Generation procedure](../README.md#generating-message-countsjson)
