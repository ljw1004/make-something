# Researcher's notebook

[Play all four illustrated chapters](http://127.0.0.1:5173/make-something.html?story=projects/anatomy/art-study/farout-1800-researcher/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

An independent study of only [the supplied researcher reference](../../inspiration/farout-1800-researcher.png) and this theme's own prior masters: sepia pen, fine crosshatching and restrained rose, ochre, lavender and olive washes on warm paper. The modern explanatory composition uses anatomical locators and located enlargements; historical drawing manner is not a historical physiology claim.

[Full production source](anatomy.md). Chapters 1, 4, 8 and 18 cover all **33 required identities and five relevant fitted layers**. The other chapters remain explicitly unillustrated. Narrative, supplies, identities, recipes, fittings and goals match the source story.

The four backgrounds contain **blank paper texture only**. They mechanically repeat and mirror an anatomy-free crop from this theme's own generated page. All depicted anatomy belongs to interactive objects or their fittings. Built-in imagegen made the retained [source masters](source/); [exact original requests](prompts.json) retain their provenance. This refresh reuses those masters through masking, cropping, resizing and compositing, with no new generations, API fallback or code-painted anatomy. The original full-page illustrations are source material, not active backgrounds.

## Reproduction and registration

From the repository root:

```sh
uv run --with pillow python projects/anatomy/art-study/farout-1800-researcher/extract.py
node projects/anatomy/art-study/integrate-art.ts projects/anatomy/art-study/farout-1800-researcher/art-map.json
```

[The producer](extract.py) records every extraction and placement; [registration metadata](registration.json) records the ear state constituents and source bounds. [The art map](art-map.json) covers the required inventory.

**Cell.** Water and lipids are complementary masks of the same generated 384 × 384 membrane bag. The water is its aqueous interior at the finished view and magnification; the lipid supply is the curved repeating bilayer that encloses it. The exported bag retains the original generated image. The nucleus is 138 × 138 both as a portable input and when fitted at (120, 118) on the 384 × 384 bag. Later unselected cell fittings remain neutral.

**Ear.** One 900 × 420 working coordinate system places the outer ear, drum, bones, sensing cochlea and nerve. The actual cochlea and its hair-cell enlargement are split from the same generated specimen, with the locator and fine leaders preserved. Every intermediate and final assembly is a sum of these same constituents. All four stages containing hearing cells retain the same located enlargement, including both legal routes to completed ears. Export crops remove unused canvas without resizing anatomy; loose pieces never expand to fill a standard square. This explicitly replaces the earlier use of independently drawn atlas states.

**Arm.** The scaffold is traced from `source/chapter-4.png`, with future muscle spans removed; its front and back are disjoint visible receiver layers. Their union forms one arm with separate radius/ulna matrix enlargements. Fitted muscle and mineral pixels come from `source/chapter-arm.png`. Both receivers and all four fittings share 1560 × 2340 canvases, centred at background (512, 768), preserving the existing quarter-size registration on the 1024 × 1536 page. Front receiver: centre (290, 450), size 180 × 360 background pixels. Back: centre (458, 450), size 150 × 360. The receiving rectangles remain separate. Both bases omit both future muscle spans, and each owns its complete mineral window, so the later receiver layer cannot hide an earlier fitting. Source alpha checks confirm no opaque overlap between the front fittings and back receiver.

**Digestion.** All eleven food, intermediate and product images remain the theme's own generated atlas exports. Their distinct silhouettes preserve the intended difference between droplet dispersion and molecular cleavage. They require contextual names to identify specific biochemical products.

## Verification and limits

Native story lint: **0 errors, 6 existing author-review warnings**, 29 chapters and 156 combinations. The retained semantic checker reports equivalence across every compared category. Source inspection covered blank backgrounds, cell input/result material continuity, every ear state, and all 16 independent arm fitting subsets. All 33 inventory entries resolve to visible art; the five relevant fitted layers are visible and match their receiver canvas sizes.

This is an informed production check, not a blind recognition study, anatomical expert review or evidence of student learning. The retained generated arm has minor annotation remnants and an illustrative rather than clinical dissection style. The nucleus and inner-ear details use deliberate explanatory magnification. The portable cochlea retains its locator/leader scaffold before hearing cells arrive. Small drum/bone pieces preserve their fitted scale and may rely on labels and normal interaction targets for discovery. The parent study owns complete comparison panels and browser drag/reload verification; source compositing alone does not establish browser usability.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
