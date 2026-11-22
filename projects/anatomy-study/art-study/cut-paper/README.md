# Contemporary cut-paper scientific atlas

[Play all four illustrated chapters](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/cut-paper/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

Comparison candidate for original chapters 1, 4, 8 and 18, under the single [Anatomy design brief](../../../../contrib/anatomy/design-brief.md). The complete manuscript retains the original narrative and mechanics. [Full production source](anatomy.md).

## Visual intent and coverage

Layered matte ivory, coral, sage, teal and mustard paper gives membranes, tissue planes and cutaways physical edges without heavy contours. Shallow shadows separate the layers. The original supplied `digestion3.jpeg`, `muscle-fiber.jpeg` and `ear.jpeg` informed the earlier direction's explanatory layout, rather than its rendering style. This refresh uses only this direction's own source masters; no other candidate was inspected.

The selected chapters include all **33 comparison identities**, the **five relevant fittings**, and every compound partial state: the empty/fitted opening cell and all sixteen combinations of the four independent arm fittings. The [state catalogue](state-catalog.json) lists the exported states for comparison-panel production. Every chapter background is blank paper, with **no anatomy, labels, diagrams or finished examples**. All anatomy belongs to interactive item or receiver artwork.

Water is the pale aqueous volume mechanically separated from the membrane-bag master. Lipids are its complementary membrane material at the same repeating-unit scale. Their composition reconstructs the bag; neither is an enlarged molecular symbol. DNA and its nuclear envelope use the same generated pieces as the resulting nucleus and its fitted appearance.

The hearing family is composed from one registered set of six components. The outer ear, drum, bone chain, cochlea, sensory enlargement and hearing pathway retain their pixels and magnification through every relevant stage. Exporting crops each stage's current geometry without resizing its components. The located sensory enlargement remains attached to the cochlear region at the same position and size. These are explanatory views, not literal shared scales between the whole ear and its tissue enlargement.

Chapter 4 has one shared skeleton divided into complementary alpha partitions between the two visibly anatomical receivers. Both use the same 1560 × 2340 origin. Each receiver also owns its bone window, with independent muscle and mineral layers. Fitting one does not replace the other. Muscle overlays include enlarged tissue and cell-fusion details; bone windows retain cells, collagen and a vessel. Unselected chapters remain explicitly unillustrated using neutral metadata.

## Sources and reproduction

All anatomical raster artwork was made with the built-in `image_gen` tool. The five original selected outputs remain in `masters/`; their exact requests remain in `prompts.json` and `arm-prompt.txt`. The original tool copies were produced under `/Users/ljw/.codex/generated_images/01a1dd62-72e6-7280-9afc-902afdc9f189/`.

The refresh additionally retains `masters/arm-skeleton-transparent.png`, an imagegen extraction of this direction's own original skeleton. [Exact extraction request](refresh-request.txt). Built-in source: `/Users/ljw/.codex/generated_images/01a1dde4-97f6-7553-962a-5af0d23c14ff/exec-473cda6b-c603-4610-bf6f-99a73b1c2cde.png`. Its input is reproducible as crop `[519,8,1016,761]` of `masters/background-atlas.png`.

[extract.py](extract.py) performs mechanical cropping, proportional sizing, complementary masks, alpha composition, arm registration and annotation. It does not draw replacement anatomy. [registration.json](registration.json) records the source crops, component sizes, common origins and per-stage hearing crops. The four blank backgrounds use a clean paper crop of the retained background atlas; the original diagrams are not used as scenery.

```sh
uv run --with pillow python projects/anatomy-study/art-study/cut-paper/extract.py
node projects/anatomy-study/art-study/cut-paper/integrate.mjs
npm run lint -- projects/anatomy-study/art-study/cut-paper/anatomy.md
node projects/anatomy-study/art-study/checks/verify-semantics.ts projects/anatomy-study/art-study/cut-paper/anatomy.md
```

The integration script reads the original manuscript and adds presentation metadata only. It does not modify the source story or application.

## Verification and limits

2026-11-14 refresh: native lint passed with **0 errors, 6 unchanged author-review warnings**, 29 chapters and 156 explicit combinations. The warnings concern mixed fates in later unillustrated chapters. Strict parser comparison reported **`equivalent: true`**, including prose, goals, identities/readings/slots, recipes, dispositions and tutorials. All 254 manuscript identities have default metadata, and slot overlays retain their owner's dimensions.

The coordinator owns browser drags, reload checks and complete chapter comparison panels. The arm is a constructed explanatory projection, rather than a measured anatomical reconstruction; precise muscle insertion readability remains a visual-review limitation. The generated hearing pathway includes a small schematic brain locator. No claim is made about human preference, student understanding or browser verification from this local production check.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
