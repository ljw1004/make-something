# Prototype sequence, playback and the Markdown transition

Recorded on 11 November 2026 from Lucian's selected retrospective sequence, the repository's Git history, archived source and release receipts, and available local Codex conversation records. This is a history of selected experiences, not every intervening experiment or a claim that each was developed immediately after the previous one.

Lucian's order is **1 → 2 → 3 → 4 → 5 → 7** below. The numbering deliberately preserves the supplied sequence; no sixth stage has been inferred. The first four stages were preserved together in one commit, so that commit cannot independently establish their internal order. Bell/Mneme also have earlier timestamped logical-play records. The sequence itself is attributed to Lucian's recollection in the 11 November conversation.

## Dates and editions

All dates below use **America/Los_Angeles**. These October dates are **PDT, UTC−07:00**. Distinguish a recorded play or publication from a Git preservation timestamp: neither necessarily identifies the first implementation or the first time Lucian played it. Filesystem modification times were not used.

| Stage | Prototype and stories | Best established date | Surviving experience |
|---|---|---|---|
| 1 | **After the Rain** | Preserved **25 Oct 2026, 19:36:39**, commit [`0126784b`](https://github.com/ljw1004/make-something/commit/0126784b). | Three watershed challenges: The first rain, Two banks, one river, and After the cloudburst. Elemental recipes, structures and a diagrammatic flood board. |
| 2 | **The Bell Orchard; Mneme** | Bell v1 logical play starts **25 Oct, 15:58:24.935**; Mneme v1 **15:58:31.439**. V2 records start **16:18:28.682** and **16:20:39.630**, respectively. Browser readers preserved in `0126784b` at **19:36:39**. | Text and combination buttons. Bell concerns a flooded orchard and a bell carrying the drowned city's memory; Mneme concerns a keeper whose preservation prevents change. Both v1 and v2 remain addressable. These play timestamps establish logical prototypes, not browser launch times. |
| 3 | **Hands-on table** | Preserved **25 Oct, 19:36:39**, `0126784b`. Exact introduction time unresolved. | A free worktable and a shelf of elemental materials. Drag ingredients together; take further copies from the shelf. Earth + Water makes Clay. Small symbols accompany labels. |
| 4 | **Shared canvas** | The [design record](../../archive/2026.10.30%20initial%20experiments/docs/shared-canvas.md) dates it to **25 Oct**; preserved **19:36:39**, `0126784b`. | **Elements, Forms and Ideas** modes. One object per concept; parents remain and a child appears nearby. Pan/zoom and reusable constructions. These are modes/sketches rather than three complete story campaigns. |
| 5a | **Elements: A World to Make** | Published **26 Oct, 22:26:01.097416**; preserved **22:40:18**, [`515715f1`](https://github.com/ljw1004/make-something/commit/515715f1). | A short four-stage story starting with Earth, Water, Air and Fire. Make a bowl and bricks, then develop food, comfort and further discoveries. Draggable text tiles and outlined places; no illustrated objects or scenery. |
| 5b | **Cooking: From Hearth to Snack Cake** (`food`) | Shared-campaign release published **27 Oct, 12:43:59**; preserved **12:57:20**, [`331f8519`](https://github.com/ljw1004/make-something/commit/331f8519). | Four chapters: The roadside hearth, The dairy and bakehouse, The pastry workshop, The small cake line. Starts with Grain, Millstone, Water, Fruit and Press; first goals are flatbread and fruit juice. Draggable text tiles, without illustrations. |
| 7a | **Elements: A River Worth Returning To** (`elements-basket-continuity-v10`) | Final UX/content release published **29 Oct, 09:07:49.540401**; preserved **09:48:32**, [`dbb9ffa7`](https://github.com/ljw1004/make-something/commit/dbb9ffa7). | 31 chapters, 217 recipes, 30 illustrated locations. A developed river-community campaign with smaller working sessions and continuity between creations. |
| 7b | **The Kitchen Caravan** (`kitchen-caravan-small-sessions-v8`) | Same **29 Oct, 09:07:49.540401** publication and **09:48:32** preservation. | 35 chapters, 192 recipes, 35 illustrated locations. Breakfast, lunches, baking, birthday food, tea, desserts and departure supper. |

Stage 5 groups two experiences in Lucian's sequence; its two release dates are different. The earliest preserved standalone Cooking browser story found is the `food` edition above. These records do not establish a Cooking build before the first Mars prototype. Early Elements does predate Mars. This distinction concerns development evidence, not the order in which Lucian remembers playing the stories.

### Attribution: all selected prototypes were Dot/cloud

**Lucian confirmed on 11 November 2026 that every prototype in the selected sequence was developed by Dot/cloud.** He did not do significant work on the laptop until afterwards. This firsthand clarification resolves the earlier provisional attribution of stages 1–4 to a possible laptop/Codex phase. Their local commit records preservation of cloud-produced work; it does not establish local development.

| Selected stage | Development attribution | Provenance and preservation |
|---|---|---|
| **1 — After the Rain** | **Dot/cloud**, confirmed by Lucian. | Preserved locally in `0126784b` on 25 October at 19:36:39 PDT. |
| **2 — Bell Orchard / Mneme** | **Dot/cloud**, confirmed by Lucian. | Same local preservation commit; timestamped plays establish that the logical versions already existed earlier that afternoon. |
| **3 — Hands-on table** | **Dot/cloud**, confirmed by Lucian. | Same local preservation commit, including implementation and interaction evidence. |
| **4 — Shared canvas** | **Dot/cloud**, confirmed by Lucian. | Same local preservation commit, including the Elements/Forms/Ideas implementation and reviews. |
| **5 — Elements: A World to Make / From Hearth to Snack Cake** | **Dot/cloud**, confirmed by Lucian and supported by cloud release records. | `515715f1` and `331f8519` belong to the 110-commit block fetched into this checkout on 29 October. Their release records describe cloud Site publication on 26 and 27 October. |
| **7 — Elements v10 / Kitchen v8** | **Dot/cloud**, confirmed by Lucian and supported by cloud release records. | `dbb9ffa7` is the final commit in that fetched block. Its publication receipt identifies a `/workspace/shared/` source checkout and the 29 October cloud release. |

The development sequence is therefore **Dot/cloud for all selected pre-Markdown prototypes, followed by significant laptop work afterwards**. The local Markdown commits and salvage are documented below; their Git timestamps do not recover the missing first Codex conversation. Attribution of the initial prototypes rests on Lucian's explicit account, with Git and release receipts establishing preservation/publication events. An earlier scenario replayed through the archive's later shared UI can include subsequent runtime work.

Other stories available around the selected stages:

- **Stage 4:** Elements, Forms and Ideas were the shared canvas's three modes. Joinery was a separate geometric comparison retained at `/?experiment=joinery`, outside the selected sequence.
- **Stage 5a:** the short Elements release shipped alongside **Mars: The Expedition** and **A Republic of Ideas**; the earlier **Estuary** experiment remained preserved separately.
- **Stage 5b:** Cooking was one of seven short shared-runtime stories: **From Hearth to Snack Cake**, **The Guest and the Fast** (Theology), **After the Flood** (Restoration), **The Sheltered Shore**, **Why This Boat?** (Causation), **The Last Train** (Literature), and **The School by the Well** (Chinese thought). The three earlier worlds remained available.
- **Stage 7:** the six featured stories were **Mars: A Light That Answers**, **Atlas of Questions**, **Elements: A River Worth Returning To**, **The Kitchen Caravan**, **The Copy Workroom**, and **Divinity: Disputed Questions**. An optional lighter Divinity story and a separate Mars-creature route also existed. The main registry retained 61 scenario identities, including earlier versions; this does not mean 61 distinct finished stories.

## Static collection

The nine selected prototypes are also available as a generated static collection at **[Before Markdown](https://ljw1004.github.io/make-something/archive/prototypes/)**. It includes both Bell/Mneme revisions and all three shared-canvas modes. Every entry runs with ordinary static hosting; no Node server or API is needed by a player. These are HTML pages plus their JavaScript, CSS and artwork, not single-file downloads. To host elsewhere, copy the whole `archive/prototypes/` directory and preserve its layout. Its game links and artwork resolve relative to the pages, including beneath the GitHub project prefix.

From the repository root:

```sh
node projects/retrospective/build-prototypes.mjs
node projects/retrospective/verify-prototypes.mjs
```

The isolated exporter uses the root's locked Vite dependencies and the unchanged `2026.10.30 initial experiments/` source. It builds in disposable `runs/` space and writes only `archive/prototypes/`, with a generated file inventory for obsolete-bundle cleanup. Rebuild this collection separately from `npm run build`, which still builds only the current Markdown application. The verifier needs the installed Playwright Chromium browser (`npx playwright install chromium` on a fresh checkout).

The [editable static sources](static/) own the collection page and browser adapters. The exporter retains the original text reader's presentation, strips only the four logical models' Node screening entry points, and reuses the archived run creation, hashing, recording and replay functions verbatim. Text runs remain in page memory and can be downloaded in the original replay format. The board clients retain their original persistence behavior under a separate `retrospective-prototypes-1:` namespace. No old saves are migrated. Only the three selected shared-campaign scenarios and their required artwork are exported; the current story catalogue is unchanged.

GitHub Pages remains configured for **Deploy from a branch → main → /(root)**. The root [`_config.yml`](../../_config.yml) permits the generated collection while excluding every other archive sibling, including future dated archives. Add any new non-dated archive sibling to its exclusions. The verification command rejects an accidentally published archive sibling or an excluded export. Do not add `.nojekyll`, which would bypass those exclusions. Publish by committing this project's source/adapters/documentation, the generated collection and the Pages configuration, then pushing to `main`; preserve the existing Pages access settings.

For a plain local static preview, run `python3 -m http.server 4189 --bind 127.0.0.1` at the repository root and open <http://127.0.0.1:4189/archive/prototypes/>. This local server exposes the checkout only on loopback; GitHub's exclusions apply to GitHub publication. The verifier separately serves only the export beneath `/make-something/archive/prototypes/`, exercising the nested hosted path.

## Run the preserved versions locally

These commands are the explicitly requested retrospective playback exception to the [archive policy](../../archive/README.md). The preserved archive remains unchanged and the production application does not depend on it. The archive's nested instructions remain historical.

From the repository root, use Node.js **22.18 or later** (the checks here used **25.2.1**). On a fresh checkout, install the current root's locked dependencies:

```sh
npm ci
```

Start the archived browser prototypes with the dedicated helper:

```sh
node projects/retrospective/serve-prototypes.mjs
```

This uses the archived tree as the web root, binds only `127.0.0.1:4187`, writes Vite cache under ignored `runs/retrospective-vite-cache`, and bypasses the active application's Vite configuration. It serves the archive's original `public/` assets at their expected URLs. It does not build, rewrite or publish the old application. Stop it with Ctrl+C. If the port is already occupied, reuse the known retrospective server or choose another port explicitly:

```sh
RETROSPECTIVE_PORT=4188 node projects/retrospective/serve-prototypes.mjs
```

Use that chosen port in the links below. The first and third-to-seventh stages share this server:

| Stage | URL on the default port |
|---|---|
| 1 — After the Rain | <http://127.0.0.1:4187/?experiment=flood> |
| 3 — Hands-on table | <http://127.0.0.1:4187/?experiment=hands> |
| 4 — Shared canvas, Elements | <http://127.0.0.1:4187/> |
| 4 — Forms / Ideas | <http://127.0.0.1:4187/?mode=forms> / <http://127.0.0.1:4187/?mode=ideas> |
| 5a — Elements | <http://127.0.0.1:4187/elements-discovery.html> |
| 5b — Cooking | <http://127.0.0.1:4187/campaign.html?world=food> |
| 7a — Elements v10 | <http://127.0.0.1:4187/campaign.html?world=elements-basket-continuity-v10> |
| 7b — Kitchen v8 | <http://127.0.0.1:4187/campaign.html?world=kitchen-caravan-small-sessions-v8> |

**Bell Orchard and Mneme need their separate API server.** In another terminal, from the repository root:

```sh
node 'archive/2026.10.30 initial experiments/experiments/story-server.ts'
```

It binds only `127.0.0.1:5180`. Use [Bell v1](http://127.0.0.1:5180/bell-v1) and [Mneme v1](http://127.0.0.1:5180/mneme-v1) for their original logical editions, or [Bell v2](http://127.0.0.1:5180/bell) and [Mneme v2](http://127.0.0.1:5180/mneme) for the default revised readers. Sessions live only in the server's memory; the reader's **Download this run** action exports one when requested. Ctrl+C stops the server.

The browser boards generally retain progress in browser storage. Use a fresh browser profile to see untouched openings; changing the origin/port also gives a separate storage origin. The prototype's own Reset starts its story again. The plain Cooking route is `world=food`, not the later 20-chapter `hearth-to-twinkie-v3` or 35-chapter Kitchen route.

### Which historical bytes are being played?

The archive is the working-tree snapshot preserved before the rebuild, based on commit `1e8567d3`. Its [source manifest](../../archive/2026.10.30%20initial%20experiments/SOURCE-MANIFEST.json) records 15,871 original file hashes. The playback routes open surviving editions in that snapshot. Some earlier entries received later UI fixes; old campaign scenarios use the retained shared runtime. An introduction date therefore does not promise an exact rollback of every interface file to that date.

For an exact source comparison, use `git show COMMIT:original/path` or inspect the release's sealed `site-source/` and source manifest. The pre-archive Git paths have no `archive/2026.10.30 initial experiments/` prefix. Do not replace the current working tree to inspect an earlier commit. The first flood engine, interface and stylesheet were compared with `0126784b` and match exactly. The table and canvas also retain earlier partial UI snapshots, but those fragments are not presented here as independent runnable sites.

## Did these all precede Markdown? When was salvage?

**Yes. Every selected prototype runs the older TypeScript-authored models, not the Markdown parser.** The last selected release was published on the morning of 29 October, before the recorded Markdown syntax commit that evening. Separate milestones matter:

| Local datetime | Milestone and evidence |
|---|---|
| **29 Oct 2026, 21:39:01 PDT** | [`1c95988a`](https://github.com/ljw1004/make-something/commit/1c95988a), **A new markdown syntax**, adds `markdown-requirements.md` and notes. This is syntax/design work, not the rebuilt player. |
| **30 Oct, 00:54:53 PDT** | [`1e8567d3`](https://github.com/ljw1004/make-something/commit/1e8567d3), **Add reviewed Markdown stories and reagent lifecycle syntax**. Manuscripts and specification are preserved before replacing the runtime. The [legacy assessment](../../archive/2026.10.30%20initial%20experiments/notes.md#30-october-2026--fresh-start-assessment) records the user's request to archive the old project and salvage guidance. |
| **30 Oct, 02:31:40 PDT** | [`eb5b6a58`](https://github.com/ljw1004/make-something/commit/eb5b6a58), **Rebuild around Markdown stories and archive legacy experiments**. This is the completed **runtime rebuild and salvage pass**: preserve old source, inventory documents, reconcile guidance, and build the shared Markdown parser/engine, browser, linter and playtesting tools. |
| **30 Oct, 07:40:11 PDT** | [`f5125875`](https://github.com/ljw1004/make-something/commit/f5125875), **restructure repository**. Consolidates documentation and moves `docs/salvage-index.md` to `archive/salvage-index.md`. This is a follow-up reorganization, not the start of salvage. |

The salvage pass inventoried **1,082 Markdown paths / 747 distinct texts** and extracted **2,223 source-linked passages**, alongside preserving the **15,871-file** legacy source tree. It carried forward selected design, authoring, UX, engineering and evaluation guidance while explicitly superseding old rules that conflicted with the new specification. See the [salvage index](../../archive/salvage-index.md), [archive policy](../../archive/README.md) and [dated rebuild notes](../../notes.md#30-october-2026--markdown-rebuild). Inventory coverage does not establish a new manual factual review of every archived sentence.

The archive originally lived at `archive/legacy-2026-10-30/`; its current directory is `archive/2026.10.30 initial experiments/`. Historical records and some provenance links still use the former name.

## When did this project's conversations move from Dot to Codex?

**All selected prototypes are now attributed to Dot/cloud by Lucian's explicit clarification; the exact first Codex conversation date remains unavailable.** He places significant laptop work after those prototypes. Git's author identity alone cannot distinguish Dot, Codex and a human committing on the same user's behalf.

The available evidence establishes three different boundaries:

1. **The earliest retained activity in this laptop checkout is 25 October at 19:34:50 PDT.** The remote-tracking reflog records the first fetch of `9c3662d5` then; the HEAD/branch reflogs begin with an initial pull at **19:35:01**. This checkout creates `0126784b` at **19:36:39** and pushes it at **19:36:53**. These establish local Git operations, not a Codex conversation or authorship of all the source being committed.
2. **The intervening cloud-era history arrives here on 29 October.** The remote-tracking reflog jumps from `0126784b` to `dbb9ffa7` in a fetch at **29 Oct, 12:36:57**; HEAD follows in a fast-forward pull at **12:37:27**. That range contains **110 commits**, beginning with `8a4437dc` (26 Oct, 07:17:18). They arrive from `origin`, rather than appearing as 110 local commit operations in this checkout. Lucian attributes this earlier remote work to Dot. Later the reflog records the local syntax commit at **29 Oct, 21:39:01**, and the local rebuild/salvage commit at **30 Oct, 02:31:40**. This distinguishes local operations from imported history, while leaving the identity of the process that performed local operations unresolved.
3. **The earliest retained project-specific Codex conversation starts on 31 October.** Its metadata records **31 Oct 2026, 20:38:06.175 PDT** (`2026-11-01T03:38:06.175Z`), source `vscode`, originator `codex_vscode`, project working directory `/Users/ljw/code/combination-challenge`. The first retained user prompt is **20:39:09.467 PDT**: “I have a hunch that ‘kitchen’ might benefit from icons,” followed by a request to recover the Settler icon-development process. It already presupposes earlier work. This is the oldest surviving local record, not evidence that Codex was first used then.

The conversation ID is `01a1952f-94f4-7951-9c98-7b87e758b449`. Its local log, relative to `~/.codex`, is `sessions/2026/10/31/rollout-2026-10-31T20-38-06-01a1952f-94f4-7951-9c98-7b87e758b449.jsonl`: session metadata is at line 1 and the first user-message event at line 17. The current thread database's earliest timestamp agrees; there were no earlier project threads under another matching working directory in that database. The [dataset metadata](metadata.json) and [CSV](agentic-loops.csv) independently report the same first retained prompt. These sources are local history, not an account-wide Dot/ChatGPT conversation export. No earlier cloud conversation transcript was available for this account in the inspected material.

Thus the defensible wording is: **all selected prototypes were developed by Dot/cloud; significant laptop work came afterwards, with the Markdown migration visibly local on 29–30 October; the exact first Codex conversation remains unresolved.** The prototypes and salvage both predate the earliest Codex chat still retained locally. Neither the first local Git operation nor the dataset's retention boundary establishes the start of substantial local development or first Codex use.

The checkout distinction comes from `.git/logs/refs/remotes/origin/main` lines 1–4 and `.git/logs/HEAD` lines 1–4. Reflogs record this repository's reference changes and are not transferred by an ordinary Git fetch/pull. Commit author/committer timestamps, by contrast, travel with the imported commit objects. The GitHub-created initial commit `9c3662d5` is dated **25 Oct, 19:26:13**, but this checkout first records receiving it at **19:34:50**. The number of imported commits is reproducible with `git rev-list --count 0126784b..dbb9ffa7`. There are no retained reflog entries between the 25 October push and 29 October fetch; that does not rule out uncommitted editing, read-only Git commands or activity in another checkout.

## Evidence and reproduction of the dating

- **User-selected order:** this retrospective conversation, 11 November 2026. Preserve it as the chosen sequence, with the uncertainty about internal ordering of the first commit's bundled experiments.
- **Development attribution:** Lucian's explicit correction in the same conversation: “In fact they were all dot/cloud. I didn't do anything on the laptop of significance until afterwards.” This supersedes the earlier inference from the first local commit.
- **Early stories:** `startedAt` in archived `results/logical-players/fun-bell-1.json`, `fun-bell-2.json`, `fun-mneme-1.json` and `fun-mneme-2.json`. Convert their UTC values to Los Angeles time. The story-server source maps `/bell` and `/mneme` to v2 and the `-v1` paths to v1.
- **Elements publication:** [three-world release receipt](../../archive/2026.10.30%20initial%20experiments/results/three-worlds-release-20261027/deployment-success.json) and [release scope](../../archive/2026.10.30%20initial%20experiments/results/three-worlds-release-20261027/README.md).
- **Cooking publication and seven-story lineup:** [shared-campaign release record](../../archive/2026.10.30%20initial%20experiments/results/shared-campaign-ui-preservation-20261027/README.md), plus `git show 331f8519:experiments/tangible-campaign/ui/scenarios.ts`.
- **Final two selected scenarios:** [UX/content publication receipt](../../archive/2026.10.30%20initial%20experiments/results/game-checkpoints-20261029/ux-content/PUBLICATION-RECEIPT.json), [preservation report](../../archive/2026.10.30%20initial%20experiments/results/ux-content-validation-20261029/REPORT.md), and archived `experiments/tangible-campaign/ui/current-scenarios.ts`.
- **Conversation boundary:** the retained local log above and the existing dataset. The database was opened read-only; this investigation did not refresh or alter the dataset, plots or source conversations.

Useful local history queries:

```sh
git log --reverse --diff-filter=A --format='%h %aI %s' -- elements-discovery.html
git log --reverse --diff-filter=A --format='%h %aI %s' -- campaign.html
git log --reverse --format='%h %aI %s' -- docs/salvage-index.md archive/salvage-index.md
git show --stat 1c95988a
git show --stat 1e8567d3
git show eb5b6a58:docs/salvage-index.md
git reflog --all --date=iso-strict
git rev-list --count 0126784b..dbb9ffa7
```

Reflog is local evidence and can expire; another clone need not contain it. Git commit objects and the checked-in release records are the durable evidence. Commit hyperlinks point to the repository's current GitHub name, `ljw1004/make-something`; older logs use `combination-challenge`.

## Playback verification and limits

The 11 November local Chromium checks loaded the listed browser families and the six featured late campaigns without page errors. The new launch helper was checked on port 4191 across all nine documented board/mode routes, including successful image loading in both selected late campaigns. All four Bell/Mneme routes (v1 and v2) accepted their first combination. Food and early Elements had no image elements; real drags produced **Grain + Millstone → Flour** and **Earth + Water → Clay**. Early Elements retained Clay after reload; the flood engine advanced a turn. A late Mars combination and reload also passed while checking the shared runtime. All 25 checked local documentation links resolve, seven selected archived files match their cited commits, and the helper's syntax and diff whitespace checks pass.

The subsequent static export passes 13 launch routes under `/make-something/archive/prototypes/`: the nine selected prototypes, both v1 text readers and two additional shared-canvas modes. All 86 complete branches supplied by the original Bell and Mneme screening functions (Bell paths exercised in both revisions) were played through the adapted reader; downloaded observations and state hashes replay successfully in the unchanged Node runner. Real drags and saved-progress reloads pass for early Elements and Cooking. All 28 exported illustrations decode. Mobile gallery/reader layouts, unknown-reader handling, absence of API requests, separate save keys and Pages exclusion coverage pass. The campaign's asset validation remains unchanged; path adaptation happens only at image rendering. Its autosave storage alias receives the same namespace as the reader.

These are bounded browser and replay checks. They do not constitute complete replays of every board campaign, validation of every historical layout, or new judgments of enjoyment. The exact first/last user play dates and the missing early conversation history remain unknown. Verification output is disposable under the [engineering policy](../../docs/engineering.md#verification-records); retain these concise outcomes and runnable instructions, not new screenshots or transcripts.
