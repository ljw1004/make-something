# Make Something Worthwhile

## Philosophy

**Make Something Worthwhile** is part game but part educational toy: playing can leave you with real understanding of how things are made and how ideas work. Treat players as capable of serious learning, from proper culinary technique and practical construction to master's-level theology and intellectual history made approachable to high-schoolers. In the spirit of *Why Don't You?*, invite curiosity, making and discovery through enjoyable play, with knowledge and skills worth carrying into life beyond the game.

The [authoring guide's worthwhile-hook requirement](docs/story-authoring.md#require-a-worthwhile-hook) makes this the bar for accepting a premise, including when an AI author must decline to develop one.

## Project

Combination stories authored in Markdown, with illustrated editions of Settlement, Cookbook, Mars and Creation. Cookbook uses Cook’s Pen illustrations, including domestic tea and dinner scenes; Mars uses physical expedition equipment and integrated landscapes. The browser game, story linter, checkpoint generator and logical AI playtester share one parser and game engine. The project has three commitments: combination, enjoyable interactive play and an empirical loop that can reject weak ideas.

## Run the game

Use Node.js 22.18 or later.

```sh
npm install
npx playwright install chromium webkit
npm run dev
```

Open the local address printed by Vite. Drag things together; compatible partners are highlighted without revealing the future result. Goals sit at the bottom and become the next-chapter arrow when complete. Reopen the chapter text through its goals for the applicable recovery action; automatic chapter introductions have only **Begin**. The discreet bug icon toggles the debug pane for live story editing and checkpoint jumps. See [UX](docs/ux.md) for the interaction and recovery rules.

Seven icon styles are retained as [reference collections](references/icon-sets/), each with its own description and preview.

**Settlement** uses rustic coloured woodcuts: `/make-something.html?story=stories/settlement/settlement.md`.

Its [completed narrative study](archive/2026.11.06%20settlement%20study/narrative-study.md) preserves early craft while arranging shared provision, culture and investigation into a cumulative progression, with motivating chapter openings and guidance for unfamiliar work. The current revision follows a harvest festival with studio work, scientific investigations and an encyclopedia, with matching production artwork.

**Cookbook** teaches practical cooking through pen-and-wash illustrations, from breakfast through afternoon tea to dinner: `/make-something.html?story=stories/cookbook/cookbook.md`. See its [design examples](stories/cookbook/design-examples.png) and lasting [design brief](stories/cookbook/design-brief.md). The completed [Cookbook study](<archive/2026.11.01 cookbook study/README.md>) retains the adaptation research, artistic directions and verdicts, comparisons, production source art and all 35 completed cookbook page PNGs.

**Mission to Mars** follows a solo astronaut from a crash through shelter, farming, an uncertain discovery and a return built with local iron: `/make-something.html?story=stories/mars/mars.md`. The [live story](stories/mars/mars.md), [design brief](stories/mars/design-brief.md) and [three moments of play](stories/mars/design-examples.png) preserve its austere physical character. The completed [Mars study](archive/2026.11.01%20mars%20study/README.md) retains the unchanged v12 reference, earlier versions, production artwork and review outcomes.

**Creation** gives you Earth, Air, Fire and Water to make stars, a living world and minds that begin creating for themselves: `/make-something.html?story=stories/creation/creation.md`. Its 187 combinations across 26 chapters use 182 circular illustrations, 22 painted backgrounds and evolving landscape hotspots. See the [story](stories/creation/creation.md), [design brief](stories/creation/design-brief.md), [three moments of play](stories/creation/design-examples.png), [supplied art references](<archive/2026.11.05 creation study/inspiration/README.md>) and [completed Creation study](<archive/2026.11.05 creation study/README.md>).

The player fetches Markdown as an ordinary file. These routes work in development and the production build:

| Player URL | Markdown fetched |
|---|---|
| `/make-something.html?story=stories/settlement/settlement.md` | `/stories/settlement/settlement.md` |
| `/make-something.html?story=stories/cookbook/cookbook.md` | `/stories/cookbook/cookbook.md` |
| `/make-something.html?story=stories/theology/theology.md` | `/stories/theology/theology.md` |
| `/make-something.html?story=stories/mars/mars.md` | `/stories/mars/mars.md` |
| `/make-something.html?story=stories/creation/creation.md` | `/stories/creation/creation.md` |
| `/make-something.html` | `/story.md` (supply this file to use this route) |

The `story` parameter points to a `.md` file on the same server. Relative paths resolve against the player page, so the same layout works under a website subdirectory; root-relative paths also work. Without the parameter, the player always requests `story.md` beside itself. A missing story displays an error. Relative artwork references resolve against the Markdown file's directory; absolute HTTP(S) image URLs also work. Markdown is rendered without executing embedded HTML or scripts.

The former `combinations.html` and `combinations-dev.html` routes are removed without redirects. Update old bookmarks to the new player filename, keeping their story parameter. Renaming only the player page leaves manuscript URLs unchanged, so progress, drafts and tutorial completion remain available on the same origin. The hosted repository-path change described below gives those stories new URLs.

Mars now uses the accepted 24-chapter v12 story at the main route. Future edits belong in `stories/mars`; the v12 reference stays unchanged. The completed study and its artwork sources are archived together. The [promotion record](archive/2026.11.01%20mars%20study/promotion/README.md) records copy integrity, checks and the existing exhaustive-lint limit. Project drafts for ongoing work stay outside the published catalogue and build; use the [authoring workflow](docs/story-authoring.md#check-and-preview-a-draft) to preview them.

`npm run build` runs TypeScript checking and Vite bundling. Story lint and analysis are separate steps: use `npm run lint -- STORY` to validate a changed story, or `npm run lint` for an explicit check of all stories. Lint errors fail that command; warnings require author review. Application and engine changes do not require story analysis. Neither building, `npm run dev` nor ordinary story loading runs the CLI linter. The live editor displays its own diagnostics without blocking saving or preview.

Chromium supports the browser tests, checks that story-heading icons are square, and measures actual hotspot hit areas for `place:` lint. Story lint reuses one browser across manuscripts; authored pixel coordinates also require background dimensions, while only manuscripts containing `place:` entries need hotspot hit-area measurements. The application build does not launch Chromium. The [specification](docs/story-format-spec.md) owns artwork and placement validation.

The editable HTML sources are [`index-dev.html`](index-dev.html), [`make-something-dev.html`](make-something-dev.html), [`simulator-story-dev.html`](simulator-story-dev.html) and [`simulator-interactions-dev.html`](simulator-interactions-dev.html). Vite serves these templates at `/`, `/index.html`, `/make-something.html`, `/simulator-story.html` and `/simulator-interactions.html` during development, even when older generated pages exist. It serves manuscripts and artwork directly at their repository paths under `/stories/`. Development also provides adjacent graphical player routes for draft previews, such as `/projects/example-study/make-something.html?story=draft.md`; these are not generated for publication.

The build writes `index.html`, `make-something.html`, `simulator-story.html`, `simulator-interactions.html` and compiled JavaScript/CSS under `assets/` into the repository root. It renders the catalogue cards directly into `index.html` and the plain story lists into both terminal pages, with no separate `stories.json` request. The original `stories/` directory supplies Markdown and artwork; neither the stories nor adjacent player pages are copied into the build. The players depend on their shared bundles and are not standalone HTML files.

Deploy the generated root pages, `icon.png`, `assets/` and `stories/` together, preserving their layout. The shared app icon follows the [identity guidance](docs/ux.md#catalogue-and-story-identity); home-screen titles, story icons and conditional Home navigation follow the [home-screen UX](docs/ux.md#home-screen-apps). Editing a manuscript or its artwork does not require rebuilding JavaScript. Adding/removing a story or changing its catalogue title/description requires rebuilding the catalogue and terminal story lists. Development regenerates the catalogue on each page request. See [GitHub Pages publication](#github-pages-publication) for this repository's setup.

Root output is intentional: Vite's warning that `build.outDir` equals the root is expected. The build requires `emptyOutDir: false` and never clears the repository. After successful output, it deletes only obsolete bundles listed in `assets/build-files.json` by the previous build. Keep that generated inventory in Git with the bundles; unrelated files are left alone. Edit the `-dev.html` templates and source code, then rebuild the generated pages.

### Browser text terminals

The [story simulator](simulator-story.html) (fast mode) and [interaction simulator](simulator-interactions.html) (detailed mode) are full-page, keyboard-operated demonstrations of the same text engine used by the human CLI and AI playtester. They use a centered 100-character monospace column, light text on black, simple Markdown styling and persistent text-only scrollback. The [UX contract](docs/ux.md#browser-terminals) describes their layout and input behavior.

Run `npm run dev` and open `/simulator-story.html` or `/simulator-interactions.html`, then type a story number. The numbered menu includes each manuscript's title and description. Each page has its own title and no navigation between modes. Direct links use the same relative manuscript paths as the graphical player, with an optional one-based chapter:

- `/simulator-story.html?story=stories/mars/mars.md`
- `/simulator-interactions.html?story=stories/mars/mars.md&chapter=3`

Choosing a story creates an ordinary browser-history entry, so Back returns to the story list. The full menu and echoed choice remain at the top of the scrollback. Without `chapter`, the runner starts at chapter one. A direct chapter link reconstructs the menu and choice, synthesizes a checkpoint through the existing runner, includes its earlier chapter history in scrollback and continues through the ending. As play reaches a chapter, the URL updates without adding history entries, reloading or replacing the current in-memory state. Sharing or refreshing that address creates a fresh checkpoint for that chapter; the URL does not encode the visitor's actual choices. These pages do not access graphical saves or editor drafts.

Fast mode accepts a menu number. Detailed mode accepts `Inspect A` or `Combine A with B`; `i`/`c` and item names complete immediately, placing the block cursor at the next input position. Shared prefixes wait for disambiguation. Keys that cannot advance the command can overtype an earlier completion, shown by a temporary underline. Space/Tab accepts ambiguous name boundaries. Recognized names are blue; Backspace at the end steps back by command parts or shared prefixes, with ordinary editing inside the line. Press Enter to submit, or leave the input blank to refresh the board. Up/Down has no command-history or scrolling action. Typing works without clicking the permanently bordered input first; each response brings that input into view. The engine, checkpoint planner, text runner, command parser and CLI completer remain unchanged; completion and cursor presentation live in the browser adapter. No server API or AI call is required.

`npm run build` includes both pages in the ordinary root deployment. On GitHub Pages they open at [Story simulator](https://ljw1004.github.io/make-something/simulator-story.html) and [Interaction simulator](https://ljw1004.github.io/make-something/simulator-interactions.html). The former `text-fast.html` and `text-detailed.html` pages are removed.

### GitHub Pages publication

Keep the generated `index.html`, `make-something.html`, `simulator-story.html`, `simulator-interactions.html` and `assets/` in Git alongside the source and original stories. Configure GitHub **Settings → Pages → Build and deployment → Deploy from a branch**, selecting **main** and **/(root)**. The catalogue is served at `https://ljw1004.github.io/make-something/`; for example, Mars opens at `make-something.html?story=stories/mars/mars.md` beneath that address.

Browser progress, drafts and tutorial completion for the previous `/combination-challenge/` site remain under their original manuscript-URL keys; they are not automatically moved to `/make-something/`. The repository rename changes the hosted story paths, following the [story identity rule](docs/ux.md#catalogue-and-story-identity). Updating the local Git remote and package name does not change localhost story URLs. GitHub redirects the renamed repository's Git URLs, but [project-site URLs are excluded from that redirect](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

The root [`_config.yml`](_config.yml) excludes all four `-dev.html` templates, documentation, source, tests, historical archives, projects and the retired `dist/` directory. The frozen [`archive/prototypes/`](archive/prototypes/README.md) collection is the sole published archive exception. Its README is the collection index, linking to each playable GitHub Pages page and recording the history and static playback instructions. The finished pages and assets are a self-contained archive item; do not rebuild or revise them. Add any new non-published root files or non-dated archive directories to the exclusion list; dated archive folders are excluded by `archive/20*`. It also disables Jekyll's theme and automatic Markdown-page generation, preserving the raw manuscripts. Do not add a root `.nojekyll`: that would bypass the exclusions and publish the rest of the repository.

Keep verification, building and publication separate. Choose the preparation steps for the changed files:

| Change | Verification | Build |
|---|---|---|
| Engine or browser application | Run the relevant automated tests; no story-wide lint or analysis is required. | `npm run build` |
| Manuscript or artwork | `npm run lint -- STORY` for each changed story; resolve errors and review warnings. | Only if the catalogue also changes. |
| Catalogue entries, titles or descriptions | Check the affected catalogue entries; lint any changed stories as above. | `npm run build` |
| Application and story changes together | Perform both applicable verification steps. | `npm run build` |

When publishing, commit the changed source and original story/artwork files together with any regenerated root pages and bundles, including the bundle inventory and obsolete-bundle removals, then push to `main`. An all-story audit remains an explicit `npm run lint` step; it is not part of the application build or a prerequisite for publishing engine changes. GitHub handles publication of committed files; there is no custom Actions workflow or separate publishing branch. Access settings are independent of this layout.

The former `/dist/` pages and flattened manuscript paths are retired. Browser saves, drafts and tutorial completion at those old Markdown URLs remain stored under their old keys; this layout change does not migrate or delete them. New URLs under `stories/` have their own state, following the [story identity rule](docs/ux.md#catalogue-and-story-identity).

## Edit a story live

Click the **bug icon** to toggle the debug pane. With the desktop editor open, the game uses a 390px preview pane and the Markdown editor fills the remaining window space. Closing it restores the full game area; scenery and objects follow the [responsive framing rule](docs/ux.md#work-surface-and-dragging). Opening it aligns the caret, editor scroll and chapter dropdown with the current gameplay chapter; see the [debug-pane contract](docs/ux.md#debug-pane).

Edits save immediately and update the current game view, including open readings, goals, rules and backgrounds. When there are local edits, a red pen replaces the bug icon; both toggle the same pane. The panel opens automatically on desktop if the story URL has a saved draft **or** its editor was last left open; closing it is remembered but does not override a saved draft.

The chapter dropdown above the editor normally follows your caret; [gameplay chapter arrivals](docs/ux.md#debug-pane) also update its title and scroll the editor while preserving the caret. Choose a chapter to generate its starting checkpoint from the current draft; if your caret is elsewhere, the editor scrolls to that chapter and places it at the end of the heading. Choosing the chapter you are already editing preserves your position. Chapter-heading lightbulbs also offer **Jump to checkpoint**. Use the first chapter to start again.

On screens narrower than 900px, the icon opens a compact **Jump to chapter** picker instead. Tap a chapter to generate its checkpoint; the current chapter is highlighted. The Markdown editor is unavailable at that width. Local drafts still power the game and retain their red-pencil indicator. Resizing back to desktop restores the editor session.

Each draft shadows its original story URL in this browser. Closing the editor, restarting the game and reloading keep the draft. **Delete draft…** is a separate, confirmed action that reloads the original file. To export your Markdown, focus the text, select all (Cmd+A or Ctrl+A), and copy (Cmd+C or Ctrl+C) into a file for you to publish yourself. Nothing uploads automatically.

Cmd+F (Ctrl+F on other platforms) opens Find/Replace. The count reads **3 of 15** for a selected match, or **? of 15** after moving the caret elsewhere; previous/next searches from that position. See [UX](docs/ux.md#debug-pane) for the complete search behavior.

Item, hotspot and chapter references appear in blue; `> NOTE:` comments appear in muted grey italics. Hover a reference for its descriptions, properties, creating/using combinations and goals; chapter hover shows its introduction, position and goals. Hover a Markdown image for a preview. Hold Cmd (Ctrl off macOS) to underline a reference, then click to go to its declaration. Clicking a declaration, or a reference with no declaration, opens a live references list beneath the editor. F12 follows the same navigation; Shift+F12 opens references directly. See [UX](docs/ux.md#debug-pane) for declaration, reference-list and keyboard behavior.

Invalid Markdown still produces a best-effort preview. Temporarily deleting the current chapter can move that preview elsewhere; restoring the text returns to the previous game position until you interact with the game. Game actions, deliberate reading/dismissal and scrolling establish a new position. Editing alone does not commit these provisional changes.

Fast diagnostics update shortly after typing; continuation and exclusivity analysis runs in one background worker. Squiggles have hover explanations. The scrollable diagnostics list stays in source order; click an entry to select its text and show its compact related-location bullets. Clicking it again collapses the bullets while keeping it selected. Only the selected diagnostic's related locations are shown. Existing diagnostics and related locations follow insertions/deletions while updated analysis is pending.

Items and hotspots require explicit declarations, including recipe results. Missing declarations are errors; declarations without references produce warnings. Forward references are supported, and incomplete drafts still save and preview. See the [specification](docs/story-format-spec.md#specification) for declaration syntax and the [authoring guide](docs/story-authoring.md#give-chapters-a-purpose-and-a-manageable-working-set) for keeping primitive supplies in their intended chapters.

Every blue lightbulb overlays the bottom-right of its applicable text and toggles a menu, without expanding or collapsing diagnostics. Cmd+. (Ctrl+. on other platforms) opens actions on the caret's row; use arrow keys and Enter to choose, or Escape to dismiss. See [UX](docs/ux.md#debug-pane) for the interaction contract.

Mixed-fate warnings break down preservation, consumption and transformation, including defaults and implicit slot installation. Their popup names the item and offers **always preserve**, **always transform** or **always consume**, limited to fates already present. Long item headings are truncated; hover the heading for the full name. A fix consolidates the authored uses in one saved, undoable edit. Choices incompatible with implicit slot behavior explain the constraint. Fixes wait for current diagnostics after typing. Three-goal and three-hotspot warnings offer **Suppress warning with an explanation**, inserting the [required acknowledgment](docs/story-format-spec.md) and selecting its reason placeholder.

Drafts use browser local storage, keyed by the full Markdown URL. Two player routes resolving to the same URL share a draft; changing the website origin or story path creates a separate one. Other tabs' versions remain available under **Saved copies**, without replacing your open buffer. Each editing session retains its latest saved buffer; loading a saved copy also preserves the current buffer. Older session copies are currently kept without automatic pruning, and the list shows copies differing from the open text. A failed save produces a visible warning and leaves the text available to select and copy. Browser data clearing, storage eviction and private browsing can remove local drafts; copy the Markdown into a file when you want a backup outside this browser.

## Story layout

The bundled manuscripts use their story names as filenames:

```text
stories/<slug>/<slug>.md
stories/<slug>/assets/...
```

Multiple manuscripts can share a directory and its artwork: for example, `stories/theology/theology.md` and `stories/theology/alternate.md` can both reference `assets/scene.webp` in `stories/theology/assets/`. Catalogue discovery finds `.md` manuscripts under `stories/`, excluding the reserved filename `design-brief.md` (case-insensitive). A story may keep its durable editorial and visual intent in that companion brief. Keep research, iteration notes and other non-story documentation in its project directory.

The linter, checkpoint and playtesting tools accept the path relative to `stories/`, such as `theology/theology.md`, or a filename without `.md`, such as `theology`, when that short name is unique. `npm run play -- list` lists the full paths. The [analyzer](#story-analysis) takes explicit file paths relative to the current directory or absolute paths, and recognizes stories by content. The browser uses each Markdown URL for independent drafts and saves, including when manuscripts share a directory. Neither the path nor filename is the player-facing title. Vite serves `stories/` at its repository path, matching the published layout. Start with the [authoring guide](docs/story-authoring.md) when writing a story and consult the [specification](docs/story-format-spec.md) for syntax and semantics.

Settlement (`settlement`) and Theology (`theology`) were renamed from Elements (`elements`) and Divinity (`divinity`) on 31 October 2026. The old story routes, including the earlier `elements-icons` route, are no longer served. Existing browser saves and drafts remain under their original URLs; the renames do not migrate or delete them.

The manuscripts were subsequently renamed from `story.md` to `<slug>.md`, and folder-only `?story=<slug>` links were replaced by file paths. Saves and drafts for those former Markdown URLs likewise remain at their old keys; they are not migrated to the new filenames.

## Tools

| Tool | Command | Purpose |
|---|---|---|
| Browser game | `npm run dev` | Start the local Vite server. |
| Debug pane | **bug/red pen icon** | Edit a durable local draft on desktop; jump to a chapter on mobile. |
| Story linter | `npm run lint` | Check all stories against the specification; errors fail the command, warnings require author review. |
| Type checker | `npm run check` | Check active TypeScript source. |
| Default tests | `npm test` | Run semantic tests and Chromium interaction checks. |
| Browser tests | `npm run browser-test` | Run just the Chromium checks. |
| Production build | `npm run build` | Type-check and bundle the browser game; story lint is separate. |
| Checkpoint generator | `npm run checkpoint -- STORY CHAPTER_INDEX [OUTPUT.json]` | Prepare a chapter through a legal replay. |
| Logical player | `npm run play -- list` | List stories; start human play with `npm run play -- --fast STORY` or `--detailed STORY`. |
| AI playtester | `npm run playtest -- --fast ...` or `--detailed ...` | Run a JSON agent process or service through the selected player interface. |
| Evaluator | `npm run evaluate -- SESSION` | Verify frozen replay and write an evidence profile. |
| Story analyzer | `npm run analyze -- FILE` | Print six plain-text answers, or use `--table FILE ...` for a comparison; [counting guide](docs/story-authoring.md#analyze-combination-structure). |

Useful authoring commands:

```sh
npm run lint -- mars --details
npm run lint -- --json
npm run checkpoint -- mars 3 /tmp/mars-chapter-4.json
```

Lint also checks optional content against goal-directed progression using the pessimistic construction-set calculation in the [formal lint catalogue](docs/story-format-spec.md#lint-rules). Opportunity warnings name a blocking chapter/dependency and link to relevant source rules. Fast editor diagnostics remain available while deep checks run in the worker.

Measure construction-set analysis:

```sh
npm run lint -- --analysis-stats
npm run lint -- --json --analysis-stats
```

Analysis stops at the 101st distinct alternative in a construction-set family or merged chapter frontier. Each set has one working state; independent goals do not generate a search over partially completed subsets. Statistics distinguish cumulative construction-set evaluations, engine operations and the largest family of alternatives. JSON adds chapter counts, OPTIONAL item counts and phase/timing details. The [specification](docs/story-format-spec.md#opportunities-for-authored-content) defines the algorithm and its deliberate approximation; [working notes](notes.md#31-october-2026-retained-opportunity-linter) record its acceptance and verification.

Lint details include source lines; JSON includes a UTF-16 text span (`from`, `to`, end-exclusive) for every diagnostic and related locations for contrasting rules. Checkpoints work through preceding goals and their dependencies, preferring preparations whose inputs already exist and avoiding unrelated combinations. Chapter indices are zero-based. These are legal developer witnesses, not fresh player experiences or a claim of globally shortest solutions.

### Story analysis

Run `npm run analyze -- path/to/story.md` for the six-line structural summary. See [combination structure and analysis](docs/story-authoring.md#analyze-combination-structure) for when to use it, counting definitions, comparison tables and detailed checkpoint measurements.

## Logical playtesting

See [fun playtests and command-line play](docs/fun-and-evaluation.md#logical-playtesting) for human play, AI sessions, retained run files and independent grading.

## Documentation map

Each document owns one aspect of working here. Update the owning document and link to it from elsewhere.

| Document | Purpose |
|---|---|
| This README | Project orientation, setup, directory layout, tool catalog. |
| [Story format](docs/story-format-spec.md) | Markdown syntax, game semantics and required diagnostics. |
| [Story authoring](docs/story-authoring.md) | The iteration process, active-brief ownership, review assignments, reusable physical/intellectual story techniques, analysis and draft checks. |
| [Icon guide](docs/icon-guide.md) | Detailed graphics production, recognition review, scene registration and artwork integration. |
| [Active projects](projects/README.md) | Work in progress and the editorial/research backlog. |
| [UX](docs/ux.md) | All current player and authoring UX decisions, their known motivations, and maintenance rules; no historical log. |
| [Engineering](docs/engineering.md) | Implementation boundaries, technical constraints and testing policy. |
| [Fun and evaluation](docs/fun-and-evaluation.md) | Experience criteria, playtest workflow and canonical player/grader rubrics. |
| [Backlog](projects/backlog.md) | Current story directions, unresolved work and future ideas. |
| [Completed authenticity pass](<archive/2026.10.30 authenticity improvements/authenticity-improvements-2026-10-30.md>) | Historical findings, implemented changes, retained decisions and supporting evidence. |
| [Archive](archive/README.md) and [salvage index](archive/salvage-index.md) | Archival policy, preservation and provenance of recovered guidance. |
| [Working notes](notes.md) | Dated hypotheses, decisions, work performed and evidence limits. |
| [Agent instructions](AGENTS.md) | Repository-specific instructions for coding agents. |

## Repository map

Maintain the [strict directory hygiene defined in AGENTS.md](AGENTS.md#directory-hygiene).

- `src/story/`: source-located Markdown model and parser.
- `src/engine/`: deterministic state, actions, needs, exclusivity and retention analysis.
- `src/lint/`: specification diagnostics and CLI.
- `src/web/`: browser presentation, touch/pointer handling, reading and persistence.
- `src/debug/`: legal replay checkpoint planning.
- `src/analysis/`: structural story statistics and measurements of a legal reference replay.
- `src/playtest/`: player observations, frozen sessions, AI transport and evaluation.
- `docs/`: standing specifications, adopted guidance and reusable workflows.
- `projects/`: active project briefs, research, plans and supporting material; see the [project index](projects/README.md).
- `stories/`: active stories and their assets.
- `runs/`: ignored trial generations, intermediate artwork, review sheets and verification output; see the [retention policy](docs/engineering.md#verification-records) for selected production and requested deliverables.
- `archive/`: historical source and research; follow its [usage policy](archive/README.md).
