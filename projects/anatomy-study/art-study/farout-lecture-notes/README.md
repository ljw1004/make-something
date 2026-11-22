# Farout lecture notes — Anatomy artwork candidate

[Play all four illustrated chapters](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/farout-lecture-notes/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

Independent interpretation of [farout-lecture-notes.png](../../inspiration/farout-lecture-notes.png): coloured-pencil hatching, dark handwritten contours, pink/purple/blue/yellow material colours and ruled notebook paper. Only this reference and this candidate's own prior generations informed the refresh; no other theme was inspected.

[Full production source](anatomy.md). Original chapters **1, 4, 8 and 18** have all **33 comparison identities and five relevant fitted layers**. The full copied manuscript preserves gameplay. Other chapters remain explicitly unillustrated.

## Current production

The four backgrounds now contain **only blank ruled paper**, mechanically repeated from the empty lower portion of this candidate's generated arm master. Every anatomical drawing belongs to an interactive object. The earlier diagram backgrounds are retained as source masters, never used as current scenery.

The membrane bag supplies both its blue aqueous-volume pixels and its complementary lipid-wall pixels. Loose water therefore has the actual interior volume and the membrane has the completed wall's repeating-unit scale. DNA and its envelope compose the nucleus; its installed layer uses the same pixels and size as the loose nucleus.

The two arm receivers own visible, disjoint bone-and-tendon regions that together form one arm. Their muscle spaces are empty initially. The independent front/back muscles and radius/ulna mineral windows retain their original master coordinates on a common 1560 × 3376 canvas, centred at (780, 1688). Fittings can be installed independently without changing the other region. The base drawing retains a few short source annotation arrows; these are part of the interactive specimen, not the background.

All hearing states are mechanical composites of stable constituent artwork, cropped without rescaling after assembly. The cochlea, located hair-cell enlargement and its source-drawn locator persist through vibration-sensitive, sound-receiving, inner-ear-with-pathways and final ear states. Outer ear, drum, ossicles and pathway constituents likewise retain their dimensions. The digestion family reuses its selected material illustrations: chains versus monomers and physical fat dispersion versus chemical breakdown remain distinct.

[export-art.py](export-art.py) records the complete producer: extraction, masks, compositing and registration, with no newly code-drawn anatomy. [extraction.json](extraction.json) records source crops, masks, registered canvases and constituent offsets. [art-map.json](art-map.json) supplies presentation metadata. Exact original imagegen requests remain in [prompts](prompts/), selected original drawings in [masters](masters/), and playable exports in [assets](assets/). This refresh reused those built-in-imagegen drawings and made no new generation request.

Regenerate and check:

```sh
uv run --with pillow python projects/anatomy-study/art-study/farout-lecture-notes/export-art.py
node projects/anatomy-study/art-study/integrate-art.ts projects/anatomy-study/art-study/farout-lecture-notes/art-map.json
node projects/anatomy-study/art-study/checks/verify-semantics.ts projects/anatomy-study/art-study/farout-lecture-notes/anatomy.md
npm run lint -- projects/anatomy-study/art-study/farout-lecture-notes/anatomy.md
```

## Verification and limits

Semantic comparison: **equivalent**, no differing fields. Native lint: **0 errors, 6 unchanged warnings**, 29 chapters and 156 combinations. Inventory inspection found nonempty artwork for all 33 identities, including both arm receivers. Source inspection covered blank backgrounds, shared cell scale, visible arm anatomy and independent fittings, and hearing-part retention.

Browser drags, reload and complete all-icon chapter comparison panels are coordinated centrally. Source inspection does not establish browser usability, blind recognition or human preference. Small source arrows remain within the arm specimen, and tiny molecular/hair-cell marks depend on inspection enlargement; the candidate remains a comparison study rather than adopted production artwork. The current contact sheet contains the coordinator's four complete chapter panels, with every icon and fitted state.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
