# Contraptions — abandoned

The user abandoned this story on **9 November 2026** and renamed it **Contraptions**.
It was previously developed as **Builder**, **A Fair in the Air** and **The Next Box**.
The conclusion is straightforward: we did not find a worthwhile experience, and
abandoning it was the right call. This is a failure archive, with no pending
redevelopment, artwork assignment or release.

The [post-mortem](2026.11.09-post-mortem.md) records the failure and what to learn
from it. The [authoring guide](../../docs/story-authoring.md#cautionary-tale-contraptions)
owns the reusable lessons. Earlier positive reviews and proposed next experiments
retain their historical scope; they do not override the user's decision.

## Retained work

- [Retired story](story/contraptions.md), [retired design brief](story/design-brief.md),
  [runtime artwork and animation](story/assets/) and [catalogue icon](story/icon.png).
  This is the last live v48 implementation, renamed for archival. It is no longer
  under `stories/` or in the published catalogue.
- [Initial study and readability revision](2026.11.07-initial-study.md): original
  research, v1–v27, canonical Blender sources, early artwork, playtests and review
  outcomes. These remain at their existing relative locations in this archive.
- [Follow-on development](2026.11.07-follow-on/README.md): v28–v48, movable
  workpieces, white instruction pages, larger parts, individual fittings, sparse
  text, physical continuity repairs and working animations. Its production sources
  and attributed playtests are preserved together.
- [Narrative redevelopment](2026.11.07-follow-on/narrative-redevelopment.md):
  source research and the rejected city-rescue and sinister-supplier treatments.
  These were attempts to earn the constructions' purpose, not accepted future work.
- [Final worthwhile-assembly study](2026.11.07-follow-on/worthwhile-study.md):
  ordinary Sweeper and Carrier prototypes, revisions, twenty AI chapter sessions,
  question-wording experiments and their limitations. The proposed drawing engine
  and other next candidates are closed with the project.

## Preservation and use

This keeps the study's first archive date, **7 November 2026**. The existing
`2026.11.07 builder study` home was renamed rather than starting a second archive.
The later active study moved into `2026.11.07-follow-on/`; the former live story
moved into `story/`. Before relocation, commit `06725dc6` holds the original layout.

All 1,565 tracked files were inventoried before moving. Artwork, animations,
source models/scripts, JSON records and frozen playtest deliverables retain their
original bytes, verified against the pre-move inventory: this includes 789 frozen
playtest files and 527 image/model assets. Markdown navigation and artwork links were rebased where needed;
the retired story's title and filename became Contraptions. The old archive index
is retained as a dated record, and explicit closure notices identify superseded
development recommendations. Historical source hashes, prompts, commands, player
reports and raw path strings still identify their original versions. Production
scripts are historical source material, not supported commands to republish the
story. No user-supplied image originals were present; conceptual references and the
local Blender example path remain recorded in the development history.

The repository's existing archive exclusion keeps this material out of the hosted
site. Archival does not migrate or erase browser saves at the old story URL. The
story-specific backlog and active project entry have been removed. Shared engine
features developed during this work remain governed by the current specifications;
their usefulness is separate from this story's failure.


## Retirement checks

The rebuilt catalogue contains the six remaining live stories and no Contraptions
or Builder entry. The old story and active study directories are absent. All 627
image references in the retired manuscript resolve, and its 33 chapters and 521
recipes are unchanged; only the story heading was renamed. TypeScript checking,
the production build, four catalogue/loading unit tests and seven Chromium
catalogue/loading/icon checks passed. Archive exclusion from hosting is unchanged.

The retired manuscript's linter still reports its previously known
`opportunity-analysis-limit` at the 100-alternative frontier; no other error or
warning was reported. This archival pass does not reopen that story or its analysis
work. Navigation checks found no newly broken links; historical references to
superseded assets and disposable run paths remain records of their original layout.
Temporary inventories and check outputs were discarded after recording these results.
