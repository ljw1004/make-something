# Farout watercolor — Anatomy comparison candidate

[Play all four illustrated chapters](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/farout-watercolor/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

Illustrates original chapters **1, 4, 8 and 18**, including all 33 identities in the comparison inventory and the five relevant fitted layers. The complete [manuscript](anatomy.md) preserves the source story's gameplay and narrative. Other chapters remain explicitly unillustrated. This is an unpublished comparison candidate governed by the [Anatomy design brief](../../../../contrib/anatomy/design-brief.md).

The sole style reference is [the supplied watercolor drawing](../../inspiration/farout-watercolor.png): translucent lavender, coral and ochre washes, fine plum contours and pooling pigment. The refresh reuses only this theme's selected generated masters. The exact built-in imagegen requests remain in [prompts.json](sources/prompts.json) and [additional-prompts.json](sources/additional-prompts.json); no new generation was required. All four selected originals remain in `sources/`.

All four backgrounds are blank textured paper, sampled exclusively from empty portions of the existing background master. There are no headings, anatomy, labels or completed examples in the backgrounds. All anatomy belongs to interactive items and fittings.

The membrane bag supplies the exact pixels for its aqueous interior and lipid wall. The water is a blue interior volume; the membrane supply retains the result's repeating-unit size. A shared DNA drawing and envelope compose the nucleus, and that same nucleus is registered inside the bag. The complete cell and its overlays share a 440×360 canvas.

The twelve ear identities are mechanically assembled from one set of painted components. Outer ear, drum, ossicles, cochlea, located hair-cell enlargement and hearing pathway retain their native output magnification through every applicable intermediate and final. Current assemblies are cropped without resizing their contents. The hair-cell locator and enlargement persist in Sound-receiving ears, Inner ears with hearing pathways and Ears.

Both arm receivers visibly depict the same single anatomical arm at the same position. All four independent fitting overlays and both bases share an 820×1230 canvas, centred at (800,1330) on the 1560×3376 chapter sheet. Transparent fitting regions in **both** receiver bases include every exported fitting pixel, including resampling edges, so a later receiver cannot obscure an earlier fitting. Tendons remain in the base; muscle tissue and mineral appear independently. Each fitted tissue carries a located enlargement using the exact standalone supply pixels at the same size.

[produce.py](produce.py) retains the mechanical atlas extraction, masks, crops, resizing, annotation leaders and registration. It draws no anatomical substitutes. [registration.json](sources/registration.json) records source bounds, cell geometry, ear assembly positions, arm masks, located details and blank-paper sampling. Regenerate exports and the presentation-only manuscript:

```sh
uv run --with pillow python projects/anatomy-study/art-study/farout-watercolor/produce.py
node projects/anatomy-study/art-study/integrate-art.ts projects/anatomy-study/art-study/farout-watercolor/art-map.json
```

Refresh verification, 14 November 2026: semantic checker reports **equivalent: true**; native story lint reports **0 errors, 6 warnings**, across 29 chapters and 156 combinations. The six warnings concern unchanged mixed fates in later unillustrated chapters. Inventory coverage is 33/33 identities; the five selected-chapter fittings exist. Pixel checks confirm zero alpha overlap between either arm base and every fitting. Completed arm, cell extraction and ear-stage composites were visually inspected. The coordinator owns final browser drag/reload checks and complete chapter comparison panels.

Limits: the arm is an explanatory cutaway. The tissue and mineral insets deliberately change magnification and are located by leaders. Hearing uses one representative ear for the plural identities. The cochlear source has an idealized cutaway, and its unfitted state retains the small locator mark. Digestion retains the selected painted instructional icons, including simplified molecular representations. These production checks do not establish student comprehension or human preference.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
