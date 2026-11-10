# Creation identity and Song of creation

Completed 10 November 2026. The user loves the detailed mosaic at full size but finds it confused at home-screen size. They selected **B — simpler light and wave** unchanged for the shared catalogue/home-screen identity, and requested a circular Song of creation item at 1.5 times the initial square export's edge. The [live design brief](../../../../stories/creation/design-brief.md) and [UX contract](../../../../docs/ux.md#home-screen-apps) own the adopted intent and presentation.

The detailed mosaic now illustrates **Song of creation** in the final playable chapter, using the already preserved [1254 × 1254 circular original](<../../../2026.11.06 story icons/masters/creation.png>). Its [576px item export](../../../../stories/creation/assets/icons/song-of-creation.png) has transparent corners and displays at 144px diameter on the reference phone viewport, 1.5 times the previous 96px rectangle edge. No redraw was needed. The [1254 × 1254 square master](<../../../2026.11.06 app icon/2026.11.06-shared-icons/creation-square.png>) also remains unchanged and matches its original generated source byte for byte. The separate full-page ending retains its tapestry-inspired painting, with its credit clarified to distinguish it from the item's mosaic.

## Retained artwork

| Option | Artwork | Outcome |
|---|---|---|
| A — closer light and wave | [1254px PNG](light-and-wave-close.png) | Retained as a useful comparison reference: a closer composition keeps much of the mosaic detail and remains busier at small sizes. It is a generated reinterpretation, not a pixel crop. |
| B — simpler light and wave | [1254px PNG](light-and-wave-simple.png) | Selected by the user: fewer broad gold and turquoise curves, calm indigo space, and a single green sweep. Exported to [the shared catalogue/home-screen icon](../../../../stories/creation/icon.png). |

Both identity drafts used the built-in image tool. [Exact requests and source paths](requests.json) preserve the unchanged original input and record selection; the original generation paths describe the working checkout. Image files were moved from the active follow-up without re-encoding.

Review instruction: compare with the original at 60, 40 and 32 CSS pixels, on light and dark grounds, with a simulated rounded home-screen mask. Visual inspection favoured B, followed by the user's selection. This is an art-direction judgment, not a human recognition test or native-device installation check.

## Reproduce the exports

From the repository root on macOS:

    sips --resampleHeightWidth 256 256 'archive/2026.11.05 creation study/production/2026.11.10-icons/light-and-wave-simple.png' --out stories/creation/icon.png
    sips --resampleHeightWidth 576 576 'archive/2026.11.06 story icons/masters/creation.png' --out stories/creation/assets/icons/song-of-creation.png

The shared [story-icon exporter manifest](<../../../2026.11.06 story icons/manifest.json>) also points to the selected simpler master, so regenerating the catalogue icons preserves this choice. Identity artwork has straight square corners; the platform supplies its own home-screen mask. The in-game item uses its source's transparent circular silhouette and the manuscript's circular outline metadata.

## Verification outcome

Creation lint returned zero errors and the eight existing warnings (seven mixed-fate cases and the 20,000-state fixed-analysis limit). Parsed rules, chapter structure and readings match the previous manuscript after excluding the changed item icon, artwork credit and source offsets. The old item export was removed only after confirming its archived copy is byte-identical.

After identity selection, the export is an opaque 256 × 256 PNG; all nine checks in the home-screen and story-icon browser suites passed. A server of the existing production output beneath /make-something/ confirmed the catalogue's 64px image, Creation's touch icon and manifest resolve to the selected export, served bytes match the runtime file, and there are no page errors. No application build was needed because the catalogue text, paths and application code are unchanged. No hosted publication was performed.

The final circular item passed a separate Chromium check at 390 × 844: jumped to A day of rest, completed both closing combinations by dragging, confirmed the 576px source displays at 144px diameter with transparent corners and the circular outline class, and observed no page errors. Visually inspected the completed result after its creation animation. These checks do not establish native-device installation or refresh of an existing pinned icon. Temporary comparison pages, captures and logs were discarded under the verification policy.
