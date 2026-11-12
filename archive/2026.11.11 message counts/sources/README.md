# Message data and reproduction

**[message-counts.json](message-counts.json) is the sole authoritative input to the [final chart](../message-counts.png).** It preserves all 597 plotted runs and their 1,260 individual human messages: 597 initial prompts and 663 steers. Runs appear in the chronological order of their initial prompts, numbered `sequence: 1` through `597` across both Codex and Dot. Each run is one object containing the initial prompt's word count, the whole run's duration, and an ordered list of steers with their individual word counts and relative arrival times.

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
| `sequence` | Chronological rank of this initial prompt among the retained timed runs, across both sources. `1` came first. This is a new ordinal, not an original message ID. |
| `source` | `codex` or `dot`; the current chart combines both. |
| `area` | The initial prompt's `art`, `story` or `game-engine` area. The original Other category is included in Game-engine. |
| `word_count` | Human-written words in the **initial prompt only**. |
| `duration_seconds` | Elapsed duration of the whole run, counted once. |
| `steers` | Subsequent human messages belonging to this run, in arrival order. |
| `steers[].delay_seconds` | Seconds from the initial prompt's logged arrival to this steer. It is a relative elapsed interval, not a timestamp or time of day. |
| `steers[].word_count` | Human-written words in this individual steer. |

Both assistants use this format. Codex grouping follows its recorded turns; Dot grouping follows the previously reviewed continuous response episodes. Each Dot steer retains its own arrival delay even when it introduced a different request. Area describes the whole run's initial request; a separate category for each steer is not inferred.

There are no message contents, replies, attachments, dates, timestamps, time-of-day fields, original message or conversation identifiers, or model rationales. The sequence preserves which initial prompt came first, without retaining when it was sent or the gap between runs. It does not number steers or imply completion order: separate runs can overlap. Within each run, steer order and relative delays are preserved. Only runs with usable durations are included, and the sequence has no gaps for omitted runs. The earlier consolidated CSV has been removed to keep one authoritative input.

The data totals remain **663 steers, 1,260 messages, 94,729 words and 213.9425937153 hours**. Codex contributes 534 runs, 491 steers, 1,025 messages and 74,733 words; Dot contributes 63 runs, 172 steers, 235 messages and 19,996 words. The [explanation](../README.md) defines the categories, word-count policy, duration measure and exclusions.

[plot_message_counts.py](plot_message_counts.py) validates the allowed fields, consecutive sequence numbers, source/category labels, nonnegative word counts, and ordered steer delays within each run's duration. It then derives run word totals and steer counts from the individual messages and checks that every duration bucket conserves them. It draws the final PNG at 1755 × 891 with linear scales; its cumulative ordering still follows run duration rather than chronology.

Run these commands from the repository root:

```sh
python3 -m venv runs/retrospective-plot-venv
runs/retrospective-plot-venv/bin/python -m pip install -r "archive/2026.11.11 message counts/sources/requirements.txt"
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B "archive/2026.11.11 message counts/sources/plot_message_counts.py"
```

The default output is `archive/2026.11.11 message counts/message-counts.png`. Use `--dataset` to select another directory containing `message-counts.json`, or `--output runs/retrospective-preview.png` for a temporary preview. The virtual environment, font cache and previews are disposable scratch material.

The individual measurements were recovered from the original saved word-count and processing records, with relative delays calculated from source message times in memory. No words were distributed artificially across steers. Every run's source, area, duration, message count and total words reconciled exactly with the previous chart input. The restored detail reproduced the accepted chart pixel for pixel. Conversation-bearing recovery inputs and temporary tooling were not retained in this directory.
