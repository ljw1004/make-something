# FAROUT FUN — independent Anatomy art candidate

[Play all four illustrated chapters](http://127.0.0.1:5173/make-something.html?story=projects/anatomy-study/art-study/farout-fun/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

The sole external drawing reference is [the supplied FAROUT FUN image](../../inspiration/farout-fun.png). Its fibrous torn-paper construction, coral, violet, gold and cobalt inform this candidate. This revision reuses only this candidate's own selected anatomy sources. It remains a comparison candidate, not an adopted production style.

[Open the full manuscript](anatomy.md). Chapters **1, 4, 8 and 18** cover all **33 comparison identities and five relevant fitted layers**. Other chapters retain neutral placeholders. Narrative, identities, supplies, goals, recipes, fates and compound slots are unchanged.

## Source art and reproduction

`sources/blank-paper.png` is the new selected built-in image-generation output; [refresh-prompt.json](refresh-prompt.json) retains its exact request and reference path. All four chapter backgrounds use that same blank cream sheet with a cobalt paper edge. No anatomical content, labels or diagrams are baked into those backgrounds.

The four inherited anatomy masters (`cell-parts.png`, `hearing-parts.png`, `digestion-parts.png`, `arm-master.png`) remain selected. The former illustrated background atlas is retained as an inherited source but is no longer used. [prompts.json](prompts.json) contains its original request. **Provenance limit:** the inherited folder did not contain exact generation requests for the four anatomy masters; this revision does not invent them.

[produce.py](produce.py) records the mechanical extraction, alpha masks, resampling and registration. Reproduce with:

```sh
uv run --with pillow --with numpy --with scipy python projects/anatomy-study/art-study/farout-fun/produce.py
node projects/anatomy-study/art-study/integrate-art.ts projects/anatomy-study/art-study/farout-fun/art-map.json
```

Water is a cropped aqueous interior of the actual bag drawing; the lipid supply is a curved section of that drawing's bilayer, with the same repeating-unit size. Neither is independently enlarged. DNA and the nuclear envelope are now the exact components of the constructed nucleus. The 184-pixel nucleus is fitted at `(158,150)` on the bag's 520-pixel canvas. Future cell fittings outside this comparison remain neutral overlays.

All twelve hearing identities are compositions from six canonical raster components. Each component is scaled once before composition. Intermediate and completed states are cropped to their actual bounds without rescaling their content. [hearing-registration.json](hearing-registration.json) records each state's selected components and crop in the common 820 × 540 coordinate system. The hair-cell detail and extracted cream locator wedge remain identical in the sensitive inner ear, sound-receiving ear, inner ear with pathways and finished ear. Standalone hearing cells use that same enlarged detail. No final atlas cell can replace or shrink the earlier assembly.

The arm uses one master and one 480 × 1240 registration canvas. Complementary front/back receiver layers each contain visible bone and tendon anatomy; together they form one arm. Both fixed receivers share background centre `(390,630)`, with separate front/back hitboxes. Biceps, triceps and the two mineral windows are independently extracted from the same master and retain its registration. Their independent slot layers support all sixteen arm fitting combinations without painting anatomy into the page or replacing the whole receiver. The free muscle-cell and mineral supplies remain representative tissue/material samples rather than literal full-arm quantities.

The eleven digestion identities retain the candidate's original paper-collage illustrations. Their molecules are explanatory enlargements on small paper samples; they are not a literal common physical scale with food portions. No new code-drawn anatomical illustration was substituted.

## Verification outcome

Native story lint: **0 errors, 6 mixed-fate warnings**, concerning unchanged later skin/body assembly semantics. The semantic checker reports **equivalent**, including chapter text, supplies, goals, items, slots, recipes and fates (29 chapters; 156 explicit combinations).

Artist inspection covered the new blank master, aqueous and membrane cutouts composited over cream, completed hearing composition, its retained enlargement, nucleus components and registered arm layers. The coordinator supplies complete comparison panels and actual browser interaction/reload checks. No independent student recognition or enjoyment claim is made. The generated anatomy is a simplified educational illustration, not a medically validated spatial model.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
