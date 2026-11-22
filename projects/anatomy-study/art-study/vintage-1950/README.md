# 1950s wall chart — independent artwork study

[Play all four illustrated chapters](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/vintage-1950/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

[Full production source](anatomy.md). The illustrated comparison chapters are **1, 4, 8 and 18**. Other chapters retain neutral placeholders.

The independent references are [vintage1](../../inspiration/vintage1.jpeg) and [vintage2](../../inspiration/vintage2.jpeg): opaque gouache, lithographic modelling, warm ivory paper, dusty teal, ochre and vermilion. The [Anatomy design brief](../../../../stories/anatomy/design-brief.md) governs this candidate. No other candidate's artwork was consulted for this revision.

All four backgrounds are completely blank ivory sheets, 780 × 1688. All scientific content belongs to interactive artwork. The complete comparison family covers **33 identities and five relevant fitted overlays**. The original three selected atlases remain the sources for the portable family. The opening water and lipid strip are mechanically extracted from the same membrane-bag painting, preserving its exact repeating-unit magnification and aqueous material. The standalone nucleus and fitted nucleus share one export size. Hearing composites retain a located, explicitly captioned tissue enlargement, alongside the macroscopic ear or coil.

The arm is one skeleton, extracted into a transparent selected master with built-in image generation. Its front receiver owns the skeleton and radius window; its back receiver owns the ulna window and supplied rear tendon scaffold. Both use the same registered 1560 × 3376 canvas, with independent receiving rectangles. Four independently composited overlays add biceps, triceps and mineral in their respective bone windows. Mineral never covers the joint or tendon. All sixteen fitting combinations were inspected at the 390px playing scale; the cell and hearing families were also inspected at quarter-size.

The [original exact requests](sources/prompts.json), [transparent-arm edit request](sources/refresh-request.json), selected masters, [original atlas extraction](sources/extraction.json), and [revision registration](sources/refresh-extraction.json) preserve provenance. Original scene paintings are retained source material; they are **not runtime backgrounds**. Reproduce the exports and full manuscript copy from the repository root:

```sh
uv run --with pillow python projects/anatomy-study/art-study/vintage-1950/sources/export.py
uv run --with pillow python projects/anatomy-study/art-study/vintage-1950/sources/refresh.py
node projects/anatomy-study/art-study/vintage-1950/sources/integrate.mjs
```

The [integrator](sources/integrate.mjs) copies the original manuscript and adds presentation metadata. Verification on 14 November 2026: semantic checker reports exact equivalence; native lint reports **zero errors and six existing mixed-fate warnings** in unselected later chapters. The coordinator owns browser drag/reload checks and the four complete chapter comparison panels. Scratch visual checks live only under `runs/anatomy-style-refresh/vintage-1950/`.

This is a style-comparison candidate. Generated anatomical detail remains a simplified teaching illustration, especially local ear tissue and muscle attachment shape; it is not evidence of student comprehension. The smallest ear parts depend on their adjacent item names at phone scale. The located tissue enlargement intentionally changes magnification; whole-ear components retain a common macroscopic family. Later placeholder slots are intentionally unillustrated and outside this four-chapter delivery.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
