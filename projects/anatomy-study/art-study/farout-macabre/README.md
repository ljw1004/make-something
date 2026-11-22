# Farout macabre — Anatomy art candidate

[Play all four illustrated chapters](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/farout-macabre/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

[Full source manuscript](anatomy.md): original chapters **1, 4, 8 and 18**, with all **33 comparison identities**, the **five relevant fitting layers**, and independently exported partial states. Other chapters retain neutral placeholders. This is a comparison candidate, not the adopted production style.

The sole external visual reference is the user's [invented macabre image](../../inspiration/farout-macabre.png), inspected directly. The theme keeps its dark umber cabinet atmosphere, luminous ivory structures, crimson tissue and amber highlights. No other candidate's art, prompts or notes were consulted.

The selected originals and [exact generation requests](sources/prompts.json) remain in [sources](sources/). They were produced with the **built-in imagegen tool**. This revision mechanically reuses those same originals; it makes no new generation request. Original background paintings are retained as provenance, but their anatomical compositions are no longer used as backgrounds. The scientific and narrative source is the unchanged Anatomy manuscript and its [single design brief](../../../../stories/anatomy/design-brief.md).

[produce.py](produce.py) owns extraction, masking, registration and exports. [extraction.json](extraction.json) records source bounds and registration; [art-map.json](art-map.json) owns manuscript presentation links. Every selected chapter now has a blank textured surface sampled exclusively from an anatomy-free lower strip of the original arm master. All anatomy is interactive artwork.

- **Cell:** water is the aqueous volume cropped from the membrane bag, and lipids are two sections of that bag's actual membrane wall, preserving the repeating-unit scale. The same envelope and DNA pixels compose the portable nucleus and its registered fitting. `assets/cell-with-nucleus.png` exposes the fitted state for comparison.
- **Arm:** complementary front/back masks divide the single generated arm into two visibly anatomical receivers on one shared canvas. Each retains its bone and tendon structure; the four original muscle/mineral fittings remain independently registered. Mineral restores its own bone window and located enlargement. Each receiver has `muscle`, `mineral` and `complete` state exports, named `assets/arm-{front,back}-{state}.png`; both base states are separate assets. The anatomical painting is no longer baked into the surface.
- **Hearing:** all twelve identities are built from six fixed components at one registered scale. The same outer ear, drum, ossicles, cochlea, hair-cell detail and hearing pathway pixels persist across the additive sequence. The located enlargement remains visible in vibration-sensitive inner ears, sound-receiving ears, inner ears with hearing pathways and the final ears. Tight cropping changes each object's extent without rescaling its contents.
- **Digestion:** all eleven supplied/intermediate/result identities retain this candidate's selected raster artwork.

Reproduce from the repository root:

```sh
uv run --with pillow python projects/anatomy-study/art-study/farout-macabre/produce.py
node projects/anatomy-study/art-study/integrate-art.ts projects/anatomy-study/art-study/farout-macabre/art-map.json
node projects/anatomy-study/art-study/checks/verify-semantics.ts projects/anatomy-study/art-study/farout-macabre/anatomy.md
npm run lint -- projects/anatomy-study/art-study/farout-macabre/anatomy.md
```

Verification: semantic comparison passes with chapters, supplies, goals, recipes, fates, slots, narrative and tutorials unchanged. Native lint passes with **0 errors and 6 reviewed mixed-fates warnings** from unchanged later skin/whole-body recipes. Coverage checks find all 33 nonempty mapped identities and all five nonempty, size-matched relevant fitting layers. The coordinator owns browser drag/reload checks, routes and four all-icon comparison panels.

Limits: these are explanatory painted sections with deliberately enlarged membrane units and sensory detail, not anatomically dimensional meshes. The arm receivers partition one drawing and are not separate front/back camera views. Hearing pathways use a representative brain silhouette; the located sensory detail is a teaching enlargement. Digestion includes schematic molecular representations. Export inspection and continuity checks do not establish human recognition, preference or learning efficacy.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
