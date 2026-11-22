# Farout Cozy — Anatomy art candidate

[Play all four illustrated chapters](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/farout-cozy/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

Full production source: [anatomy.md](anatomy.md). Illustrated original chapters: **1, 4, 8 and 18**. The governing story intent remains the [Anatomy design brief](../../../../stories/anatomy/design-brief.md); this is an independent comparison candidate, not an adopted production style.

The sole style reference was [the supplied Farout Cozy image](../../inspiration/farout-cozy.png), inspected directly. Transparent watercolor washes, warm paper, fine brown drawing and lavender anatomy inform this interpretation. No other artist's work was consulted.

## Selected production and refresh

Four original built-in `image_gen.imagegen` generations remain selected in [sources](sources/): background, cell/arm, hearing and digestion atlases. [prompts.json](prompts.json) preserves their exact original requests and the refresh instruction. This refresh uses their existing raster pixels through deterministic cropping, masking, resizing and compositing; it makes no new generated or code-drawn anatomy.

[export.py](export.py) owns extraction and registration. [registration.json](registration.json) records the common hearing canvas, constituent positions, stage membership and cell/arm registration. Rebuild with:

```sh
uv run --with pillow python projects/anatomy-study/art-study/farout-cozy/export.py
node projects/anatomy-study/art-study/integrate-art.ts projects/anatomy-study/art-study/farout-cozy/art-map.json
```

All four runtime backgrounds are **780 × 1688 blank textured paper**, tiled from one anatomy-free region of the selected source. All anatomical content is interactive. There are **33 selected item mappings and five relevant fittings**, matching the shared comparison inventory. Unselected chapters and unrelated slots retain neutral placeholders without added supplies.

The water input is a region of the actual bag's aqueous volume. The lipid input is a curved bilayer section extracted from that same bag, preserving repeating-unit magnification. DNA and the nuclear envelope are composed into the nucleus from the same constituent pixels, and that nucleus is installed without resizing. The water sample depicts a selected volume rather than an exact volumetric accounting of the final bag.

Every hearing assembly now composites the same outer ear, drum, ossicles, cochlea, hair-cell enlargement and nerve pixels at fixed canonical coordinates. Export only crops transparent margins: existing parts never grow or shrink between stages. The pointed hair-cell enlargement persists in every state after those cells are installed. Its magnification is a located explanatory exception; it does not claim the cells are cochlea-sized. Original separately generated completed hearing pictures are retained only as unused regions within the selected source atlas.

The arm has been extracted from the former painted background into two complementary, registered receiver layers. Their union shows one arm, including the hand; their disjoint base pixels avoid covering an already fitted addition belonging to the other owner. The four independent muscle/mineral overlays preserve all **16** fitting combinations. The cell has two chapter-one states, without and with its nucleus. Muscle overlays retain their generated tendon tips and use the source arm's tendon trajectories. Mineral occupies the two bone windows. The arm's soft watercolor extraction remains slightly irregular at very fine edges; it is an explanatory cutaway, not a surgical model.

## Verification outcome and limits

Native lint: **0 errors, 6 reviewed warnings**, 29 chapters and 156 authored combinations. The warnings concern existing mixed-fate uses of Skin segment, Skin with a cleared wound, Lower body, Breathing apparatus, Nervous system model and Skin covering; this presentation-only copy retains those roles.

The shared semantic comparison reports **equivalent: true**, including chapter supplies, narrative, goals, item identities, recipes, fates and compound slots. Source inspection checked the bag family, complete hearing assembly, and the arm with its four fittings. The stable geometry is now a compositing invariant, rather than a claim that independent generated stages match. Digestion retains its original complete eleven-icon family; its symbolic molecular representations are not a common literal physical scale with food portions.

Browser drag/reload verification and the requested complete comparison panels are handled centrally by the coordinator. This production pass does not establish student recognition, learning or enjoyment. Temporary inspection artifacts remain under ignored `runs/anatomy-style-refresh/farout-cozy/` until the coordinator finishes review; they are disposable.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
