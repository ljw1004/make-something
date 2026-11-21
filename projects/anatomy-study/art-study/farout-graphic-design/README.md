# FAROUT GRAPHIC DESIGN — Anatomy comparison candidate

[Play all four illustrated chapters](http://127.0.0.1:5173/make-something.html?story=projects/anatomy-study/art-study/farout-graphic-design/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

Independent interpretation of [farout-graphic-design.png](../../inspiration/farout-graphic-design.png), using only this reference and this theme's earlier generated artwork. Angular anatomical facets, lithographic grain, oxide red, slate blue and cream define the drawing treatment. The [Anatomy brief](../../../../stories/anatomy/design-brief.md) and [common assignment](../artist-instructions.md) govern the work.

[Full production source](anatomy.md). Original chapters **1, 4, 8 and 18** contain all **33 comparison identities**, the registered nucleus and four independent arm fittings. Other chapters retain neutral placeholders. All narrative, supplies, goals, recipes, ingredient fates and compound identities remain unchanged.

## Current construction

All four backgrounds are blank paper, mechanically sampled from an unused margin of this theme's generated arm master. They contain no anatomy, labels or diagrams. Anatomical content belongs to item images and their fitted layers.

The membrane bag, aqueous water volume and lipid strip are extracted from one new generated master at the identical scale. Water is blue fluid volume, without droplet or molecule symbols. The membrane supply retains the bilayer's repeating-unit size. DNA and its envelope keep their sizes when combined; the resulting nucleus keeps that size when installed in the bag.

One arm plate is partitioned between complementary visible front and back receiver layers. The exact existing muscle and mineral pixels restore pale receiving spaces, with four independent overlays and separate radius/ulna windows. Both receiver canvases and all overlays remain 1560 × 3376; their artwork centre remains (780,1688). The shared image is divided at x=716, so the two bases together reproduce one arm, with no pre-painted anatomy on the background. Empty, mineral-only, muscle-only and complete receiver exports are in `assets/states/`.

Hearing is now assembled mechanically from this theme's own generated components. Component dimensions never change between states. The same cochlear cutaway, hair-cell enlargement and triangular locator persist through vibration-sensitive inner ears, sound-receiving ears, inner ears with pathways and the final ears. The digestion atlas retains its recognizable food sources, short starch chains, distinct enzymes, separated products and fat-emulsification sequence.

## Reproduction and sources

Six selected original raster generations are retained in `masters/`, including the new `cell-volume.png`. [prompts.json](prompts.json) preserves the exact built-in imagegen requests and source reference. The new master used the built-in imagegen tool; no CLI image generation or other theme supplied artwork.

[produce.py](produce.py) and [refresh.py](refresh.py) contain mechanical cropping, alpha cleanup, resizing, masks, registration and compositing only. [registration.json](registration.json) records extraction geometry, cell masks, hearing component dimensions/origins and arm partitioning. [art-map.json](art-map.json) provides presentation metadata. [contact-sheet.jpg](contact-sheet.jpg) contains four complete chapter panels: player views show relative scale, while isolated icon details are enlarged for inspection. The coordinator supplies current browser evidence.

```sh
uv run --with pillow python projects/anatomy-study/art-study/farout-graphic-design/produce.py
node projects/anatomy-study/art-study/integrate-art.ts projects/anatomy-study/art-study/farout-graphic-design/art-map.json
npm run lint -- projects/anatomy-study/art-study/farout-graphic-design/anatomy.md
node projects/anatomy-study/art-study/checks/verify-semantics.ts projects/anatomy-study/art-study/farout-graphic-design/anatomy.md
```

## Verification and limits

Refresh verification: **0 lint errors, 6 existing warnings**; semantic comparison **equivalent** across all 29 chapters and 156 combinations. The six warnings concern unchanged mixed ingredient fates in later unillustrated chapters. Raster inspection checked the water/membrane family, installed nucleus, combined arm and persistent hearing enlargement. Current browser interaction and chapter-panel checks belong to the coordinator; earlier browser outcomes do not validate this refresh.

The angular treatment is schematic anatomy. The cell is an explanatory cutaway, not a claim that a membrane enclosure is living. Bilayer units are enlarged consistently to expose construction. The hair-cell inset is an explicitly located enlargement, not literal cochlear scale; food-molecule shapes remain representational rather than structural chemical formulae. The arm's two complementary receivers are parts of one printed plate, retaining paper within their bounds. No independent student-recognition or learning claim is made.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
