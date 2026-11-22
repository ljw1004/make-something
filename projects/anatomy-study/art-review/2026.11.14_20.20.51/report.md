# Anatomy: thirteen artwork directions

This report consolidates production and review of the [artwork comparison](../../art-study/README.md), governed by the [active design brief](../../../../contrib/anatomy/design-brief.md) and [icon guide](../../../../docs/icon-guide.md). Consolidation began 14 November 2026 at 20:20:51 America/Los_Angeles; the directory timestamp records that point, not an invented start time for the earlier individual production checks.

## Version and scope

The unchanged source manuscript has SHA-256 `d6920c636ce31af51a80b341237c1ba3375d29daf23b71834aeb2eae8ff63229`. Each direction retains a full manuscript copy, with artwork for chapters **1, 4, 8 and 18**. Other chapters have neutral placeholders. This is a style comparison, with no adopted production direction or publication.

Thirteen separate artist subagents received the [common assignment](../../art-study/artist-instructions.md), story context and their assigned inspiration. Artists did not receive the other artists' images or concepts. The five initial directions are modern student, doctor poster, 1950s illustration, 1800s atlas and contemporary cut paper. Eight further directions cover every supplied `farout-*` reference: researcher, cozy, fun, graphic design, lecture notes, macabre, Star Trek and watercolor.

Each artist used built-in imagegen and retained the selected masters and exact requests. Production scripts perform extraction, alpha masking, scale and registered compositing. Four-view contact sheets show completed browser states; the gallery links to each independently playable manuscript. Source images, prompts, extraction records and scripts are indexed in each theme's README.

## Checks and outcomes

All thirteen copies passed native story and artwork lint with **zero errors and six existing mixed-fate warnings**. All copies contain the original 29 chapter records, including the epilogue, and 156 parsed recipes. Parsed comparison confirmed unchanged chapter introductions, goals, supplies, hotspot identities, item identities and names, compound slots, readings, recipes, ingredient fates and tutorial references. Presentation metadata intentionally differs. The original manuscript hash remained unchanged.

Browser checks covered all **52 selected chapters** at **390×844**, **390×640** and **1280×900**. Each check loaded the real player, entered the chapter, dragged the required items through the illustrated route, reached the continuation control, checked image decoding and reloaded the completed state. Routes used three combinations for chapter 1, four for chapter 4, five for chapter 8 and five for chapter 18. All passed after the placement repair described below, without page errors or broken artwork. Default-phone checks were repeated on affected themes after later export repairs. This records viewport coverage plus targeted final rechecks, not a claim that every intermediate export was retested at every size.

Independent informed visual reviewers inspected contact sheets, standalone assets and relevant source atlases, including fitted states. Review prompts requested neighboring atlas fragments, clipping, disconnected assemblies, registration and background discontinuities. These reviewers knew the intended subjects; the checks are not blind recognition trials. Repaired artwork was assigned to a reviewer who had not seen that sample's previous version.

| Finding | Final treatment and outcome |
|---|---|
| Modern arm muscle and mineral fittings did not match the scene precisely | Mirrored/registered the muscle and fitted mineral patches to the actual circular windows; browser assembly and later contextual review passed. |
| Neighboring atlas subjects intruded into several exports | Revised measured cell bounds for Vintage and Cut-paper; added localized alpha masks for Modern, Classic, Cut-paper, Researcher, Lecture Notes and Star Trek. Fresh source comparisons found no remaining foreign fragments or lost legitimate components in those targets. |
| Cozy background extension stretched paper and initially included part of a hand | Sampled genuinely blank paper, preserved uniform grain scale and mirrored the extension. Fresh review found continuous paper and preserved illustration at player scale. |
| Graphic Design supplies collided with the goal area on short phones | Raised authored supply rows and enlarged the explanatory header. All four chapters then passed at all three viewports. |
| Macabre lower-ground join was visible | Mirrored a blank strip at its existing uniform scale. Fresh review found no visible join at the former boundary and preserved upper anatomy. |
| Modern fitted mitochondrion crossed the membrane | Moved it inward without changing scale. A fresh composite review found it inside the membrane with distinguishable nucleus and mitochondrion. This extra fitting belongs to the unselected next chapter. |
| Watercolor repeated a source panel's lower paper border | Excluded the border from the blank-ground sample before composing the arm. Fresh review of all four backgrounds and refreshed player sheets found preserved headers, natural paper and no repeated borders or conspicuous seams. |

Final contact sheets and gallery are the retained visual deliverables. Detailed browser captures, review composites, scratch source copies and raw logs are disposable verification artifacts and are removed after consolidation.

The final informed review found no remaining actionable integration defects in its inspected samples. Lecture Notes retains a thin pale extraction fringe on artificial dark ground; it is inconspicuous at player size on the actual pale scene and was not judged to need another repair. Minor overlap of the Modern nucleus and fitted mitochondrion leaves both structures distinguishable. These scoped findings do not certify every anatomical detail.

## Repeatable checks and limits

Start the ordinary local server with `npm run dev`, then open [the gallery](http://127.0.0.1:5173/projects/anatomy-study/art-study/gallery.html). Each play link starts a complete manuscript copy. The bug button jumps to chapters 1, 4, 8 and 18. At each viewport, exercise the chapter's displayed goals, inspect partial and completed fittings, reload, and check that the completed state persists. Run `node src/lint/cli.ts projects/anatomy/art-study/<theme>/anatomy.md` for native validation. Each theme's README gives its export command and source mapping.

The retained [browser check](../../art-study/checks/capture.mjs) runs as `node projects/anatomy/art-study/checks/capture.mjs <theme-slug> ...`. Its default viewport is 390×844; use `CAPTURE_HEIGHT=640` for the short phone or `CAPTURE_WIDTH=1280 CAPTURE_HEIGHT=900` for desktop. Captures and results go to ignored `runs/anatomy-art/`. The [semantic check](../../art-study/checks/verify-semantics.ts) runs as `node projects/anatomy/art-study/checks/verify-semantics.ts projects/anatomy/art-study/*/anatomy.md`. Run these from the repository root. After default-phone capture, `uv run --with pillow python projects/anatomy/art-study/contact-sheets.py` rebuilds the requested sheets. Remove scratch captures and logs when their outcomes have been recorded.

Final gallery inspection found thirteen sections, thirteen decoded contact-sheet images and 26 successful sheet/play links, with no page errors.

The inspection establishes technical integration and identifies visible defects within the requested sample. It does not establish medical accuracy of every generated mark, student comprehension, human preference, native touch behavior or suitability of the unillustrated rest of the book. The sheets show one completed arrangement per chapter; alternative legal action orders and item positions can produce different compositions. Deliberate anatomical and molecular enlargements are part of the brief, not a claim of literal common scale.
