# Retrospective

This project collects evidence about the human–agent development process behind **Make Something Worthwhile**, including its surviving prototypes and locally saved conversations.

## Prototype history

- [Prototype sequence and playback](prototype-history.md): Lucian's selected pre-Markdown sequence, story lineups, dated Git/publication evidence, local launch instructions, the Markdown/salvage transition and limits on dating the move from Dot to Codex.
- [serve-prototypes.mjs](serve-prototypes.mjs): serves the preserved browser prototypes locally with cache in ignored scratch space; the history document also explains the separate Bell Orchard/Mneme server.
- [Static collection](../../archive/prototypes/index.html): the nine selected prototypes, including browser-only Bell Orchard and Mneme adapters. [Build](build-prototypes.mjs) and [verify](verify-prototypes.mjs) it separately from the current game; [hosting instructions](prototype-history.md#static-collection) cover GitHub Pages.

## Dataset

- [combined-conversations.csv](combined-conversations.csv): the combined Codex and Dot dataset, with source IDs, message counts, human-word counts, categories and recorded durations. Codex rows are loops including their steers; Dot rows are individual messages with blank run durations. Sum `user_message_count`, rather than row counts, for the total number of user messages.
- [combined-metadata.json](combined-metadata.json): source hashes, counting rules, duration conventions, per-source totals and combined totals. [combine_sources.py](combine_sources.py) rebuilds these files without changing either source snapshot; [tests](test_combine_sources.py) cover the import boundaries.
- [dots-conversation-data.csv](dots-conversation-data.csv): the user-supplied Dot export, preserved unchanged, including its message/reply timestamps, text and original word counts.
- [agentic-loops.csv](agentic-loops.csv): the original Codex snapshot, one row per initial prompt, with text, timing, outcome, steer count, word counts for the prompt and each steer, and source locations.
- [metadata.json](metadata.json): capture time, scope, counts and excluded turns for the Codex snapshot.
- [build_dataset.py](build_dataset.py): reproducible extraction using Python's standard library. Reads the local Codex database and logs without modifying them.
- [test_build_dataset.py](test_build_dataset.py): small synthetic checks for message deduplication, steers, timing, interruption, failure and capture boundaries.
- [add_word_counts.py](add_word_counts.py): adds word counts to the saved snapshot without refreshing its prompts, steers or timing. [word_counts.py](word_counts.py) owns counting rules; [test_word_counts.py](test_word_counts.py) checks text boundaries and snapshot preservation.
- [attachment-audit.json](attachment-audit.json): content hashes, human-authorship decisions and selected spans for every text attachment in the snapshot.
- **[plots/time-by-loop-length.png](plots/time-by-loop-length.png): the original Codex-only bar chart of total agentic hours by loop length**, with `N prompts + M steers` labels beside each bar. Also available as [PDF](plots/time-by-loop-length.pdf).
- **Codex durations by area:** [art](plots/time-by-loop-length-art.png), [story](plots/time-by-loop-length-story.png), and [game-engine including other](plots/time-by-loop-length-game-engine.png), with a shared hours scale. [Three-page PDF](plots/time-by-loop-length-by-area.pdf).
- **[All three areas in one chart](plots/time-by-loop-length-combined.png):** each duration band has three colored subrows, labeled `N prompts, M words`. Here prompts include initial prompts and steers, and words include both. [One-page PDF](plots/time-by-loop-length-combined.pdf).
- [plot_category_loop_lengths.py](plot_category_loop_lengths.py): joins the timing and classification snapshots to render the separate area charts and the combined chart.
- **Preferred cumulative view:** [prompts against hours](plots/cumulative-prompts-hours.png), with area averages and duration labels inside the graph, and [exact values and duration bands on hover](plots/cumulative-prompts-hours.svg). The [bucket bubbles](plots/words-hours-buckets.png) remain an alternative, with a [hoverable SVG](plots/words-hours-buckets.svg) and a [two-page PDF of both views](plots/representation-options.pdf). [Renderer](plot_representation_options.py).
- **[plots/time-allocation.png](plots/time-allocation.png): the original Codex-only duration divided among individual prompts**, with time-weighted breakdowns. Also available as [PDF](plots/time-allocation.pdf) and [SVG with prompt details on hover](plots/time-allocation.svg).
- [plot_time_allocation.py](plot_time_allocation.py): renders the time-allocation view and the standalone loop-length chart from the same saved snapshot.
- [plots/overview.png](plots/overview.png): four charts and headline duration statistics from the original Codex snapshot.
- [plots/agentic-loops.pdf](plots/agentic-loops.pdf): the overview followed by one larger chart per page.
- [plot_dataset.py](plot_dataset.py): renders the charts from the CSV and metadata without refreshing the source dataset.

The Codex snapshot includes archived conversations. It selects top-level threads whose recorded working directory is exactly this repository's path; subagent threads and conversations in other directories are excluded. Its source is the local thread index plus its referenced rollout logs, not an account-wide conversation export. Deleted or unavailable history cannot be recovered by this dataset.

The combined dataset contains **1,264 user messages and 94,746 human-written words**:

| Source | User messages | Human-written words | Plotted duration |
|---|---:|---:|---:|
| Codex | 1,028 | 74,803 | 135.7 hours |
| Dot | 236 | 19,943 | Excluded: no run durations |
| Combined | 1,264 | 94,746 | 135.7 hours from Codex |

**Dot is excluded from all duration charts.** All 236 messages lack recorded run durations and steer counts. Although 232 have visible-reply intervals, their last reply can be unrelated background work: row 222 spans a brainstorming request to a publishing update 51h 34m later, and row 225 spans a task-deletion request to a deployment update 29h 25m later. These intervals remain in their original columns for reference; `duration_seconds` stays blank. The charts therefore contain **1,025 messages and 74,733 words** across 534 timed Codex loops, excluding three open Codex loops.

Dot remains useful for message text, categories and word counts. Each exported message contributes once, with no additional steer messages invented. It extends text coverage back to 26 October 2026; its last message is on 11 November, later than the frozen Codex capture. Dot does not supply conversation IDs, so its messages do not establish an additional conversation count.

Dot's `prompt_text` uses the same word tokenizer as Codex. The original supplied counts total 19,941; recounting changes 79 individual values and adds two words overall. Original values remain in `source_prompt_word_count`. One empty-text Dot message still counts as a message and contributes zero words; image contents and absent attachment bodies do not add words. Rebuild the combined dataset with `python3 -B projects/retrospective/combine_sources.py`.

## Prompt categories

[prompt-classifications.csv](prompt-classifications.csv) contains **GPT-6 Luna** classifications for the Codex initial prompts, with the exact model, source hashes, coverage checks and totals in [classification-metadata.json](classification-metadata.json). Join it to the timing dataset on `prompt_id`; the original prompt text and durations stay in `agentic-loops.csv`.

[dot-classifications.csv](dot-classifications.csv) adds Luna classifications for all 236 Dot messages using the same categories. Stable IDs have the form `dot:message:N`; [dot-classification-metadata.json](dot-classification-metadata.json) records source hashes, context, validation and runtime confirmation of `gpt-6-luna` at low reasoning effort. Dot counts are 122 story, 93 game-engine, 10 art and 11 other. The combined importer retains both sources' labels for message/word analysis. Duration plots use Codex labels only, folding Other into Game-engine.

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

For a new Dot classification pass, run `python3 -B projects/retrospective/classify_dot.py prepare`, give the three generated packets to Luna with the same category rubric, then run `python3 -B projects/retrospective/classify_dot.py merge` and `python3 -B projects/retrospective/combine_sources.py`. Dot context includes preceding messages and visible replies; the classifier prioritizes the user's requested work when later replies concern a different subject. Low-confidence, Other and long-duration cases were reviewed against that context. Classification inputs and worker outputs live temporarily under `runs/retrospective-dot-classification/`.

The initial pass classified all 537 prompts. Runtime records confirmed that all three workers used `gpt-6-luna` at low reasoning effort. Follow-up Luna reviews corrected missed mixed requests, context errors and taxonomy boundaries, and incorporated nine pasted requests. Validation confirmed exact ID coverage and joins, source/rubric/output hashes, and conservation of all associated steer counts and recorded hours. There are 54 mixed requests; confidence is high for 478 rows, medium for 58 and low for one. This is reviewed model classification rather than a human-labeled accuracy benchmark.

## Plots

Start with the **cumulative view** to compare interaction counts with agentic duration, with average human-written words per prompt labeled for each area. The Codex snapshot contributes **135.7 hours** across 534 timed loops, including completed, failed and interrupted turns. Three open Codex loops and the entire Dot source are outside these charts. Overlapping loops are summed separately, including work added through steers.

The **area bar charts** use the same plain appearance, duration bins, and hours axis as each other. The combined chart places Art, Story and Game-engine in three colored subrows within each duration band. Its `N prompts, M words` labels count Codex initial prompts and steers and their human-written words. The separate-area charts distinguish initial prompts and steers. All groupings use Luna's primary category and fold `other` into `game-engine` for plotting. Steers stay with their initial prompt's area and duration band. Untimed loops are excluded. The renderer checks the Codex source/classification hashes and reconciles all three groups to the snapshot totals.

The **representation sketches** give both quantities numeric axes while preserving hours horizontally. Bucket bubbles place each nonempty area/duration bucket at its total hours and words, with bubble area proportional to its message count. Small numbers identify duration bands; SVG hover details provide exact values. The cumulative view starts each area at zero and adds the six duration bands from shortest to longest, plotting cumulative prompts against cumulative hours. Each marker is a running total, and each straight segment adds the next bucket's hours and prompts. Accumulation follows loop length rather than conversation chronology. Each endpoint gives the area's total; segment slopes express prompts per recorded agentic hour, not a quality or productivity score. The standalone graph preserves the former right panel's physical plot dimensions. Earlier bar charts remain for comparison.

Labels beside the final dots show `Area, Nkwords` and `(avg N words/prompt)` on separate lines. Total human-written words are rounded to the nearest thousand: Art 10kwords, Story 46kwords, and Game-engine including Other 18kwords. Story is right-aligned below its endpoint, Art is left-aligned to its right, and Game-engine is left-aligned above its endpoint, shifted left to avoid the Story line. Averages divide each area's plotted words by all its plotted user messages, rounding to whole words: Art 56, Story 91, and Game-engine including Other 55 words per prompt.

The title, **How I prompted: cumulative totals**, and subtitle, **From shortest agentic runs (1m) to longest (6h)**, sit inside the plot. The axes read **How many prompts** and **Cumulative duration of agentic runs**; duration values remain in hours. Footnotes are omitted from the chart, with counting definitions and scope retained here. The plotting rectangle and scales retain the Codex-only chart's proportions.

Uniform solid colored circles closely fit their small white two-character labels; `15m` may extend beyond the circle. Cutoffs are `1m`, `5m`, `15m`, `1h`, `3h` and `6h`. Each dot accumulates runs shorter than that duration, rather than labeling an individual run or the area's maximum. The shared `6h` label includes the whole final bucket, rounding the longest recorded run of 6h 00m 21s. Game-engine ends at `1h` because its longer buckets are empty. Dots stay at their data coordinates and may overlap. Draw order is Art's line and labeled circles, then Story's line and labeled circles, then Game-engine's line and labeled circles. SVG hover details retain the bucket names, cutoff labels and cumulative totals.

- **Prompt rectangles:** one rectangle per initial prompt, with area exactly proportional to its share of the total recorded duration. Color encodes steer count; the legend gives hours in each steer group. The largest labeled tiles carry duration ranks. Open the SVG in a browser to hover over any rectangle for its prompt excerpt, ID, conversation, duration, outcome and steer count. Small prompts keep their actual area instead of receiving a minimum visual size.
- **Original Codex time by loop length:** summed hours in each duration band. The right of each bar reads `N prompts + M steers`, counting initial prompts and all their mid-turn steers separately. Hours are read from the axis, with no hour or percentage annotations. Every band contributes to its original 135.7-hour total. The standalone export uses a white background, one blue bar series, gray gridlines and ordinary typography.
- **Time concentration:** accumulated hours as prompts are added from longest to shortest. The first **27 prompts account for 50.8%** of all recorded time; the first **90 account for 80.1%**.

In the original Codex snapshot, the 334 loops shorter than five minutes account for only **6.6% of its recorded duration**, even though they are most of the ended prompts. This is the distinction between a time-weighted view and a count of prompts.

The earlier Codex-only four-chart overview supplies complementary views of individual turns:

1. **Duration bands:** counts and percentages of completed loops in six explicitly unequal duration bands.
2. **Timeline:** one point per ended turn, with distinct colors and shapes for completed, failed and interrupted outcomes. The logarithmic duration axis accommodates seconds through hours; open turns have no plotted duration.
3. **Daily prompts:** initial prompts grouped by their Los Angeles start date and stacked by outcome. Steers do not count as new prompts. The first and last dates have partial coverage.
4. **Steers and duration:** individual completed turns grouped by steer count, with middle-50% bars and median diamonds on a logarithmic duration axis. Horizontal jitter only separates overlapping dots. Longer turns also give more opportunity to steer, so this association does not establish causation.

In the initial snapshot, the median completed loop lasts **2m 50s**, the 90th percentile is **38m 06s**, and the longest lasts just over **6 hours**. The headline statistics use all 493 completed turns. The plots preserve the dataset's outcome and timing qualifications below; elapsed durations are not human working hours or compute usage.

To regenerate the time-allocation exports, standalone, separate-area and combined loop-length charts, and earlier overview, install the plotting dependencies into ignored scratch space and run:

```sh
python3 -m venv runs/retrospective-plot-venv
runs/retrospective-plot-venv/bin/python -m pip install -r projects/retrospective/plot-requirements.txt
python3 -B projects/retrospective/combine_sources.py
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B projects/retrospective/plot_time_allocation.py
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B projects/retrospective/plot_category_loop_lengths.py
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B projects/retrospective/plot_representation_options.py
MPLCONFIGDIR=runs/retrospective-mpl-cache runs/retrospective-plot-venv/bin/python -B projects/retrospective/plot_dataset.py
```

The scripts check source hashes, missing durations and grouped totals. The time-allocation renderer also verifies that every rectangle's area matches its share of duration, all rectangles fit inside the plot, and all 534 prompts receive SVG hover details. Optional `--dataset` and `--output` arguments select different input and output directories. All duration renderers use the original Codex snapshot. The separate combined-data command rebuilds message/word totals while keeping Dot run durations blank. These requested charts are retained deliverables, while the virtual environment and font cache are disposable.

The initial plotting pass reconciled every grouped total with the CSV, visually checked the overview, and verified the PNG and five-page PDF exports.

The time-allocation pass reconciled the hour totals and all 534 rectangle areas, visually checked the labels, and verified its PNG, one-page PDF and 534 unique SVG prompt-detail entries against the CSV. The earlier overview also regenerated successfully after extracting shared loading and styling helpers.

The plain loop-length chart reconciles 534 initial prompts and 491 steers across its six bands. Its standalone PNG and PDF and the corresponding panel in the time-allocation exports use the revised count labels.

The separate and combined area charts reconcile 534 timed Codex loops, 491 steers, 1,025 messages, 74,733 words and 135.7 hours. Three open Codex loops are excluded. Their labels and shared scale were visually checked. The separate-area PDF contains one page per area; the combined chart has a one-page PDF.

The representation sketches use the same validated category join and reconcile all bucket totals and cumulative endpoints. Both views have 16 populated buckets with SVG hover details. The cumulative plot keeps its original physical dimensions and scales. The two-page PDF and label placement were checked. Nineteen synthetic checks cover the original extraction/word policy and the combined import, including keeping reply intervals separate from run durations, missing intervals, timestamp consistency, unknown steer counts, mixed row-grain totals and source changes invalidating a combined snapshot.

## Word counts

Words are Unicode letter/number sequences, keeping internal apostrophes and hyphens within a word. Punctuation and Markdown markers do not count as words; numbers do. This is a reproducible text measure, not an estimate of manual typing effort.

The user's policy is to count human writing: trust every word entered directly as theirs, audit every text attachment, and exclude images. Direct input is accepted without trying to detect AI authorship or copied passages. Text attachments use the decisions in [attachment-audit.json](attachment-audit.json), bound to the exact content hashes. Mixed attachments count only the reviewed human-written spans. Each submitted occurrence counts, so sending the same human-written text again adds its words again; this measures communicated writing, not unique keystrokes.

Paste-wrapper headings, previews and filesystem paths are excluded. For clarification replies, only the user's answer counts, excluding the assistant's question and generated IDs. Response annotations count user comments and the request, excluding selected assistant text and generated instructions. Images and non-text attachments contribute zero words. Missing, changed or newly encountered text attachments stop the exporter until their content is audited, instead of being silently included or assigned zero. Plotting also checks that the audit matches the word-count metadata.

The Codex audit covered all 1,028 messages, nine text-attachment occurrences (seven unique contents), and 68 image blocks. All text attachments occur in initial prompts. Complete first-person editorial feedback documents were counted based on their content and conversation context; that attribution is an audit judgment rather than independently verified authorship.

| Text attachment group | Occurrences | Words previously counted | Human-written words counted | Decision |
|---|---:|---:|---:|---|
| Drag-event JSON trace | 1 | 34,734 | 0 | Generated diagnostics, explicitly excluded by the user. |
| Cookbook manuscript excerpt | 3 | 1,983 | 120 | Count 40 words per submission: rewritten synopsis, headings, image captions and chapter prose. Exclude unchanged manuscript text, asset paths and other scaffolding. |
| Mars editorial/artwork feedback | 4 | 6,288 | 6,288 | Keep the full chapter-by-chapter feedback documents. |
| Settlement editorial feedback | 1 | 1,261 | 1,261 | Keep the full feedback document. |

The Cookbook selections were compared with `stories/cookbook/cookbook.md` at commit `30522b05441304b7a364a183abdc287d8a654a34`, the last committed version before the first paste. The user described the attachment as their suggested rewrite of the first three chapters. The audit retains exact character spans and source references without copying the attachments into the repository.

The revised Codex snapshot contains **74,803 human-written words**: 51,477 in initial prompts and 23,326 in steers. Its timed records contribute **74,733 words** across 1,025 messages, excluding three open loops and their 70 words. Within this Codex source, the Game-engine 5–15m bucket contains **1,877 words**, down from 36,611; its 38 initial prompts, 17 steers and 5.318 hours remain intact. Only four rows' word counts changed: the trace and the three Cookbook submissions. Every timing value, message count, original prompt text and Luna classification is unchanged. Classification metadata preserves the pre-enrichment source hash and records the current source hash. Counting rules, the audit hash and totals are recorded under `word_count` in [metadata.json](metadata.json).

To add or reproduce counts for an existing snapshot, without including newer conversations or messages:

```sh
python3 -B projects/retrospective/add_word_counts.py
```

This reads the original source logs through the saved capture time and each row's observed boundary. It verifies message identities, text, steer counts and total coverage before replacing any dataset files. The regular dataset exporter also includes word counts for future snapshots and requires new attachment contents to be audited first. Eleven synthetic checks cover timing, deduplication, clarification answers, response annotations, full/partial/excluded attachments, changed-content detection, image exclusion, direct-input trust, and enrichment that leaves a frozen open loop unchanged despite later messages. A repeat enrichment produces identical files.

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
| `prompt_word_count` | Human-written words in the initial prompt, including audited human portions of its text attachments. |
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
