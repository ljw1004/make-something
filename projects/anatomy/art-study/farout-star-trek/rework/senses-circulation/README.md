# Hearing through breathing — selected production package

This package supplies all **78 identities first declared in chapters 8–14**, including every intermediate, plus all **four registered Breathing apparatus fittings**, including the arm and lymph fittings used in chapter 28. `map.json` uses exact parsed identities and paths relative to the Star Trek edition. It does not change manuscript semantics.

The governing contract is [production.md](../production.md). The built-in imagegen tool generated the seven selected atlases in `sources/`; [prompts.json](prompts.json) retains the exact seven requests. Every call used `transparent_background: true`. The supplied [reference](../../../../inspiration/farout-star-trek.png) informed cyan contours, coral/violet tissues, ivory bones and restrained gold nerves. Sources were copied from the imagegen output directory into this package.

`produce.py` reproduces crops, alpha cleanup, anatomical color masks and registered compositing. It draws only small circulation/locator annotations; all anatomical structures are generated raster pixels. Run from the repository with:

```sh
uv run --with pillow --with numpy python projects/anatomy/art-study/farout-star-trek/rework/senses-circulation/produce.py
```

Ear components, sensory enlargements, blood constituents, vessel walls, lung populations and chest components retain their material identity and magnification when combined. The heart halves are divided from one completed cutaway. Lung capillary and elastic-fibre masks derive from matching generated populations. Enlargements are explicit in the generated anatomy; the installed thoracic lungs omit their enlarged air-sac inset. The blood oxygen supply retains a faint cell locator around the small material forms rather than a large symbolic oxygen token.

The initial source chest base and overlays use **1000 × 1100 pixels**. The final integrated edition overrides these with the matching **1000 × 940** chapter-14 geometry and **500 × 470** chapter-28 base in the [skin/finale package](../skin-finale/README.md). `assets/chest-complete-reference.png` is a composition source for the finale package, not an additional gameplay identity. The shared arm is copied from `skin-finale/assets/arm-assembly.png` before that package's final export reduction. The shared lymph source is copied from `defense-digestion/sources/16-lymph.png`; its selected neck junction retains the same valved green route entering a blue vein. Original requests for these two shared sources remain in their owning packages.

Production inspection covered every export at one-quarter intrinsic scale on navy and light grounds, plus all 16 chest base/slot combinations. The exact inventory check found no missing or extra owned identities; every slot matches its base canvas. Corrections removed a neighboring blood-cell crop fragment, kept microscopic air-sac enlargement outside installed chest anatomy, aligned the ear/nerve family, and retained the same anatomical parts across alternative assemblies. Inspection composites are disposable scratch under `runs/anatomy-star-rework/`.

Limits: this is production inspection, not student recognition or medical validation. Very small eardrums/ossicles preserve their relation to the ear, and oxygen/elastic-fibre details are intentionally fine; the selected navy ground supports them better than the light comparison. The central-circuit and coronary/body-vessel views are explanatory located diagrams rather than one continuous same-scale dissection. Browser integration and drag/slot verification belong to the coordinating pass.

## Final assembly source handoff

`produce-final.py` derives a **298 × 220** chest source from the initial 1000 × 1100 canvas. These intermediate images and `finale-presentations.json` remain production inputs/history; the coordinator does not use that map for runtime presentation. The skin/finale package embeds the chest source within a 500 × 470 frame, fits both arms at full-body scale, replaces the heart/lung group with the intact connected reference below, and owns the current early/final geometry. Its `chapter14-presentations.json` and `finale-presentations.json` are the runtime overrides.

## Connected-heart correction

The later production review replaced the chapter 12 atlas juxtaposition with `sources/heart-connected-final.png`, a single connected heart/pulmonary-vessel master. `heart-connected-request.json` records the built-in edit of the earlier atlas; `heart-connected-count-request.json` records the targeted correction to two returning veins per lung. Both used true transparency. The intermediate connected source is retained because it is the exact second edit's input.

Every heart half and pulmonary network now comes from complementary masks of this one master. Recombining them restores the same continuous arterial/venous pixels. Coronary inputs are complementary masks of one enlarged muscle strip; the result no longer duplicates ghost hearts. The body route remains a separately located vessel-wall/exchange view with directional annotations. `heart-pulmonary-connected-reference.png` supplies the organ-only connected construction for downstream chest integration.

The same correction isolates one complete representative eardrum membrane, removes neighboring cochlear-locator fragments from the coil and sensory inset, and masks the adjacent red-cell crescent from the iron/amino-acid enlargement. Revised pieces and assemblies were inspected at source and player size; independent acceptance remains with the coordinating review. The chapter 14 geometry repair is owned by the finale package, which has been given the connected reference so the new vascular joins persist in its chest composition.

The final hearing correction uses the foreground oval from the eardrum atlas as one complete representative membrane. That exact single membrane appears in the loose input and each local ear assembly, matching the one depicted canal; the rear oval is excluded by a traced source silhouette. Full-size and quarter-size inspection covered all affected hearing stages.
