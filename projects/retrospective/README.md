# Retrospective

This project collects evidence about the human–agent development process behind **Make Something Worthwhile**, including its surviving prototypes and locally saved conversations.

## Prototype history

- [Prototype sequence and playback](prototype-history.md): Lucian's selected pre-Markdown sequence, story lineups, dated Git/publication evidence, local launch instructions, the Markdown/salvage transition and limits on dating the move from Dot to Codex.
- [serve-prototypes.mjs](serve-prototypes.mjs): serves the preserved browser prototypes locally with cache in ignored scratch space; the history document also explains the separate Bell Orchard/Mneme server.
- [Static collection](../../archive/prototypes/index.html): the nine selected prototypes, including browser-only Bell Orchard and Mneme adapters. [Build](build-prototypes.mjs) and [verify](verify-prototypes.mjs) it separately from the current game; [hosting instructions](prototype-history.md#static-collection) cover GitHub Pages.

## Dataset

- [agentic-loops.csv](agentic-loops.csv): one row per initial prompt, with text, timing, outcome, steer count, word counts for the prompt and each steer, and source locations.
- [metadata.json](metadata.json): capture time, scope, counts and excluded turns for the current snapshot.
- [build_dataset.py](build_dataset.py): reproducible extraction using Python's standard library. Reads the local Codex database and logs without modifying them.
- [test_build_dataset.py](test_build_dataset.py): small synthetic checks for message deduplication, steers, timing, interruption, failure and capture boundaries.
- [add_word_counts.py](add_word_counts.py): adds word counts to the saved snapshot without refreshing its prompts, steers or timing. [word_counts.py](word_counts.py) owns counting rules; [test_word_counts.py](test_word_counts.py) checks text boundaries and snapshot preservation.
- **[plots/time-by-loop-length.png](plots/time-by-loop-length.png): a plain bar chart of total agentic hours by loop length**, with `N prompts + M steers` labels beside each bar. Also available as [PDF](plots/time-by-loop-length.pdf).
- **The same chart by area:** [art](plots/time-by-loop-length-art.png), [story](plots/time-by-loop-length-story.png), and [game-engine including other](plots/time-by-loop-length-game-engine.png), with a shared hours scale. [Three-page PDF](plots/time-by-loop-length-by-area.pdf).
- **[All three areas in one chart](plots/time-by-loop-length-combined.png):** each duration band has three colored subrows, labeled `N prompts, M words`. Here prompts include initial prompts and steers, and words include both. [One-page PDF](plots/time-by-loop-length-combined.pdf).
- [plot_category_loop_lengths.py](plot_category_loop_lengths.py): joins the timing and classification snapshots to render the separate area charts and the combined chart.
- **[plots/time-allocation.png](plots/time-allocation.png): the total recorded agentic duration divided among individual prompts**, with time-weighted breakdowns. Also available as [PDF](plots/time-allocation.pdf) and [SVG with prompt details on hover](plots/time-allocation.svg).
- [plot_time_allocation.py](plot_time_allocation.py): renders the time-allocation view and the standalone loop-length chart from the same saved snapshot.
- [plots/overview.png](plots/overview.png): four charts and headline duration statistics from the saved snapshot.
- [plots/agentic-loops.pdf](plots/agentic-loops.pdf): the overview followed by one larger chart per page.
- [plot_dataset.py](plot_dataset.py): renders the charts from the CSV and metadata without refreshing the source dataset.

The snapshot includes archived conversations. It selects top-level threads whose recorded working directory is exactly this repository's path; subagent threads and conversations in other directories are excluded. The source is the local thread index plus its referenced rollout logs, not an account-wide conversation export. Deleted or unavailable history cannot be recovered by this dataset.

## Prompt categories

[prompt-classifications.csv](prompt-classifications.csv) contains **GPT-6 Luna** classifications for the initial prompts, with the exact model, source hashes, coverage checks and totals in [classification-metadata.json](classification-metadata.json). Join it to the timing dataset on `prompt_id`; the original prompt text and durations stay in `agentic-loops.csv`.

Each row has one `primary_category`: **art**, **story**, **game-engine** or **other**. Art covers illustrations and visual assets; story covers narrative, educational content and authored combinations; game-engine covers shared code, interface behavior and tooling. Other covers requests outside those subjects. The [classification guide](classification-guide.md) owns the full rubric and the boundary between story-specific mechanics and shared engine behavior.

`secondary_categories` lists substantive additional work, separated by semicolons. `confidence` is Luna's high/medium/low assessment, not a calibrated probability. `evidence_basis` records whether the classification relies on the prompt, preceding context, or unresolved evidence. Each row includes a short rationale, model name, stable conversation/turn IDs and a normalized 180-character prompt preview for reading the file; use the source dataset for the complete prompt.

Luna reads each prompt and supplied context. Generic approvals and continuations receive the subject of the work they refer to, when recoverable. The supplied context contains the conversation title, two preceding user messages, the last preceding assistant final reply, and available referenced pasted text. Long context and very large attachments are explicitly truncated; images are not reinterpreted. Mixed classifications describe the initial request and do not apportion the loop's elapsed time among activities or later steers. The category-hour summaries assign each loop once, to its primary category.

To prepare a new classification pass:

```sh
python3 -B projects/retrospective/prepare_classification.py
```

Give each generated `worker-N-input.jsonl` packet to Luna with the classification guide, retaining conversations together. Save its per-record judgments as `worker-N-output.jsonl` in the same scratch directory, review flagged and representative cases, then consolidate:

```sh
python3 -B projects/retrospective/merge_classifications.py
```

These scripts prepare evidence and validate/merge model decisions; they do not assign categories by keyword. The merger requires one valid decision for every source prompt and an unchanged source-dataset hash. Raw worker packets and outputs are disposable scratch material; the CSV, concise metadata and guide are retained deliverables.

The initial pass classified all 537 prompts. Runtime records confirmed that all three workers used `gpt-6-luna` at low reasoning effort. Follow-up Luna reviews corrected missed mixed requests, context errors and taxonomy boundaries, and incorporated nine pasted requests. Validation confirmed exact ID coverage and joins, source/rubric/output hashes, and conservation of all associated steer counts and recorded hours. There are 54 mixed requests; confidence is high for 478 rows, medium for 58 and low for one. This is reviewed model classification rather than a human-labeled accuracy benchmark.

## Plots

Start with **time allocation** when the quantity of interest is agentic duration. The total is **135.7 hours** across the 534 initial prompts with recorded end events. It includes completed, failed and interrupted turns; the three open turns have unknown final durations and are excluded. Overlapping turns are summed separately, and each initial prompt is assigned its entire loop, including work added through steers.

The **area bar charts** use the same plain appearance, duration bins, and hours axis as each other. The combined chart places Art, Story and Game-engine in three colored subrows within each duration band, with more vertical room for the bars and count labels. Its `N prompts, M words` labels count all initial prompts plus steers in the bucket, and all words in those messages and their pasted text. The separate-area charts retain their initial-prompt and steer labels. All groupings use Luna's primary category and fold `other` into `game-engine` for plotting. Each loop, including all its steers and their words, belongs to its initial prompt's area and duration band. Open turns are excluded from bars. The renderer checks the classification/source hashes and reconciles all three groups to the original totals.

- **Prompt rectangles:** one rectangle per initial prompt, with area exactly proportional to its share of the total recorded duration. Color encodes steer count; the legend gives hours in each steer group. The largest labeled tiles carry duration ranks. Open the SVG in a browser to hover over any rectangle for its prompt excerpt, ID, conversation, duration, outcome and steer count. Small prompts keep their actual area instead of receiving a minimum visual size.
- **Time by loop length:** summed hours in each duration band. The right of each bar reads `N prompts + M steers`, counting initial prompts and all their mid-turn steers separately. Hours are read from the axis, with no hour or percentage annotations. Every band contributes to the same 135.7-hour total. The standalone export uses a white background, one blue bar series, gray gridlines and ordinary typography.
- **Time concentration:** accumulated hours as prompts are added from longest to shortest. The first **27 prompts account for 50.8%** of all recorded time; the first **90 account for 80.1%**.

For example, the 334 loops shorter than five minutes account for only **6.6% of all recorded duration**, even though they are most of the ended prompts. This is the distinction between a time-weighted view and a count of prompts.

The earlier four-chart overview supplies complementary views of individual turns:

1. **Duration bands:** counts and percentages of completed loops in six explicitly unequal duration bands.
2. **Timeline:** one point per ended turn, with distinct colors and shapes for completed, failed and interrupted outcomes. The logarithmic duration axis accommodates seconds through hours; open turns have no plotted duration.
3. **Daily prompts:** initial prompts grouped by their Los Angeles start date and stacked by outcome. Steers do not count as new prompts. The first and last dates have partial coverage.
4. **Steers and duration:** individual completed turns grouped by steer count, with middle-50% bars and median diamonds on a logarithmic duration axis. Horizontal jitter only separates overlapping dots. Longer turns also give more opportunity to steer, so this association does not establish causation.

In the initial snapshot, the median completed loop lasts **2m 50s**, the 90th percentile is **38m 06s**, and the longest lasts just over **6 hours**. The headline statistics use all 493 completed turns. The plots preserve the dataset's outcome and timing qualifications below; elapsed durations are not human working hours or compute usage.

To regenerate the time-allocation exports, standalone, separate-area and combined loop-length charts, and earlier overview, install the plotting dependencies into ignored scratch space and run:

```sh
python3 -m venv runs/retrospective-plot-venv
runs/retrospective-plot-venv/bin/python -m pip install -r projects/retrospective/plot-requirements.txt
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B projects/retrospective/plot_time_allocation.py
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B projects/retrospective/plot_category_loop_lengths.py
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B projects/retrospective/plot_dataset.py
```

The scripts check outcome counts, missing durations and the totals represented by each grouping. The time-allocation renderer also verifies that every rectangle's area matches its share of total duration, all rectangles fit inside the plot, and all 534 prompts receive SVG hover details. Optional `--dataset` and `--output` arguments select different input and output directories. Regenerate the plots after refreshing the dataset; each figure labels the source snapshot's capture time. These requested charts are retained deliverables, while the virtual environment and font cache are disposable.

The initial plotting pass reconciled every grouped total with the CSV, visually checked the overview, and verified the PNG and five-page PDF exports.

The time-allocation pass reconciled the hour totals and all 534 rectangle areas, visually checked the labels, and verified its PNG, one-page PDF and 534 unique SVG prompt-detail entries against the CSV. The earlier overview also regenerated successfully after extracting shared loading and styling helpers.

The plain loop-length chart reconciles 534 initial prompts and 491 steers across its six bands. Its standalone PNG and PDF and the corresponding panel in the time-allocation exports use the revised count labels.

The separate and combined area charts preserve those same 534 initial prompts, 491 steers and 135.7 recorded hours collectively, with three open turns excluded. The combined chart therefore labels 1,025 prompts in total. Their labels and shared scale were visually checked. The separate-area PDF contains one page per area; the combined chart has a one-page PDF.

## Word counts

Words are Unicode letter/number sequences, keeping internal apostrophes and hyphens within a word. Punctuation and Markdown markers do not count as words; numbers do. This is a reproducible text measure, not an estimate of manual typing effort.

At the user's request, counts include complete pasted-text attachments, including quoted documents, code and debug logs. Each attachment counts once per message that supplies it; supplying the same text in another message counts again. Paste-wrapper headings, previews and filesystem paths are excluded. For clarification replies, only the user's answer counts, excluding the assistant's question and generated IDs. Response annotations count user comments and the request, excluding the selected assistant text and generated instructions. Images and non-text attachments are excluded. Missing pasted text causes an error rather than a zero-word estimate.

The word-count enrichment recovered all 1,028 messages in the original snapshot, including 21 clarification replies and nine pasted-text attachments. These contain 111,400 words: 88,074 in initial prompts and 23,326 in steers. The chart includes 111,330 words across the 1,025 messages in ended loops, excluding the three open loops and their 70 words. It preserves every previous CSV value, including initial prompt text, durations, outcomes and steer counts. Luna's classifications are unchanged; their metadata retains the pre-enrichment source hash and records the new source hash. Summary totals and counting rules are recorded under `word_count` in [metadata.json](metadata.json).

To add or reproduce counts for an existing snapshot, without including newer conversations or messages:

```sh
python3 -B projects/retrospective/add_word_counts.py
```

This reads the original source logs through the saved capture time and each row's observed boundary. It verifies message identities, text, steer counts and total coverage before replacing any dataset files. The regular dataset exporter also includes word counts for future snapshots. Nine synthetic checks cover timing, deduplication, clarification answers, response annotations, pasted text, and enrichment that leaves a frozen open loop unchanged despite later messages. A repeat enrichment produces identical files.

## What a row means

An **initial prompt** is the first actual user message recorded in a turn. Later user messages in that same turn are **steers**: they increase `steer_count` without starting another timing row. Replies to clarification questions count as user messages; a reply that starts a new turn has its own row. A new prompt such as “continue” after an interruption also starts a separate row. Automatically injected instructions, context and agent messages are not user prompts.

The primary measure, **`duration_seconds`**, is the runtime's recorded `duration_ms / 1000` from turn start to its terminal event. If a terminal event lacks this field, the exporter uses the difference between logged start/end timestamps and marks the source accordingly. This is elapsed loop time, including tool calls, waiting and work added by steers. It is not model compute time or an estimate of the effort caused solely by the initial wording. Parallel subagent durations are not added to it. Time between separate turns is excluded.

**`prompt_to_end_seconds`** is a second measure: terminal-event timestamp minus initial-user-message timestamp. It excludes setup before the user message was logged. Logged timestamps and the runtime's internal timer have slightly different boundaries, so this measure need not equal `duration_seconds`.

Keep the outcome when analyzing durations:

- `completed`: a terminal completion event without an error; this does not establish that the user's task was successfully accomplished.
- `failed`: a terminal completion event carrying an error, including service or usage-limit failures.
- `interrupted`: an explicit turn-aborted event.
- `open`: no terminal event in the captured records. Duration and end time stay blank. This can mean ongoing work or incomplete history; the exporter does not guess which.

For open rows, `observed_seconds` runs only to the last observed log entry. It is a lower bound on the observed span, not a completed duration, and does not assert continuous activity. The current dataset-building turn can therefore appear as open in its own snapshot. For an analysis of normally finished loops, filter to `status == "completed"`.

## Columns

All timestamps are ISO 8601 UTC. Use `America/Los_Angeles` when presenting local dates. Numeric durations are seconds, rounded to milliseconds. Blank fields mean unavailable, not zero.

| Column | Meaning |
|---|---|
| `conversation_id` | Stable local thread ID. |
| `conversation_title` | Recorded title, with whitespace collapsed and truncated to 160 characters. |
| `archived` | Whether the conversation was archived at capture: `0` or `1`. |
| `turn_id`, `root_turn_id` | Recorded turn identifiers. The exporter stops if a separate continuation/root relationship requires a new grouping decision. |
| `turn_trigger` | Recorded trigger, such as `composer` or `send_user_message_async_question`. |
| `prompt_id` | Unique client ID of the initial user message. |
| `prompt_kind` | `text` or `question_reply`. |
| `prompt_text` | Initial prompt's logged text; text blocks joined with a newline. Attachments are not copied. Existing literal escapes and question-reply wrappers are preserved. |
| `prompt_at_utc` | Timestamp of the initial user-message event. |
| `started_at_utc`, `ended_at_utc` | Logged lifecycle event timestamps. |
| `status` | `completed`, `failed`, `interrupted` or `open`. |
| `duration_seconds` | Primary elapsed loop time; blank for open rows. |
| `duration_source` | `reported_duration_ms`, `event_timestamps`, or blank when open. |
| `prompt_to_end_seconds` | Elapsed time from the recorded initial prompt to the terminal event; blank when open. |
| `steer_count` | Additional user messages within the same turn. |
| `prompt_word_count` | Words in the initial prompt, including its pasted text. |
| `steer_word_counts` | JSON array containing one integer per steer, in source-log order after message-ID deduplication. |
| `steer_word_count` | Sum of the per-steer word counts. |
| `total_word_count` | Initial-prompt words plus all steer words for the loop. |
| `last_observed_at_utc` | Terminal-event timestamp, or last available log timestamp for an open row. |
| `observed_seconds` | Logged start to `last_observed_at_utc`; never substituted for an open row's duration. |
| `end_reason` | Recorded interruption reason, when present. |
| `error_message` | Recorded terminal error, when present. |
| `source_log` | Log path relative to the Codex home recorded in metadata. |
| `start_line`, `prompt_line`, `end_line` | One-based physical line numbers in that source log. |

CSV quoting preserves multiline prompt text. Read it with a CSV parser rather than treating each physical line as a row, and parse `steer_word_counts` as JSON. Only initial prompt text is retained; the dataset records word counts without copying assistant replies, tool output, attachments or steer text.

## Refresh and verify

From the repository root:

```sh
python3 -B -m unittest discover -s projects/retrospective -p 'test_*.py' -v
python3 -B projects/retrospective/build_dataset.py
```

The exporter defaults to `~/.codex` and this repository. Use `--codex-home`, `--repository` or `--output` to override those locations. It replaces the CSV and metadata, leaving the documentation and other project material intact.

Each extraction freezes an event cutoff and source-file byte limits before reading. Newer events and partial trailing records are excluded. It understands both paginated `item_completed/UserMessage` events and legacy `user_message` events, deduplicates client IDs, and rejects copied history across conversations, missing message IDs, negative durations and ambiguous lifecycle records. Turns without a user message are excluded and listed in metadata rather than assigned invented prompts.

The initial snapshot contains 537 prompt rows across 95 conversations: 493 completed, 22 failed, 19 interrupted and 3 open. Its 491 steers account for the remaining messages. Four synthetic checks passed. Independent reconciliation against the separate history index matched all 521 indexed prompt rows, their 1,007 user messages and all 520 indexed terminal durations; the other 16 prompt rows use legacy logs. CSV identifiers, counts, outcomes and missing-duration rules also passed validation. The snapshot's exact capture time and exclusions are in metadata.

The dataset is a requested retrospective deliverable, not a retained verification transcript. Keep any temporary analysis output in ignored `runs/` space. The [engineering retention policy](../../docs/engineering.md#verification-records) governs verification artifacts.
