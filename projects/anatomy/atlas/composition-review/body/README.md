# Anatomy composition repairs: later tissues and body

This package repairs concrete composition failures in chapters 19–26. It leaves the original `atlas/body` package intact. The active [design brief](../../../design-brief.md) and [icon guide](../../../../../docs/icon-guide.md) govern its anatomical units, naturalistic engraving, and present-state illustrations. Chapter 27 passed review unchanged; chapter 28 is owned by the separate finale package.

| Chapters | Selected repair |
| --- | --- |
| 19 | Continuous epithelial covering, connective villus cores, supplied capillary meshes, and a local collecting venule that drains onward into larger intestinal and portal veins. |
| 20 | Matched muscle fibres with exposed intracellular compartments and glycogen stored inside them; hormone samples use the repaired shared Blood master. |
| 21 | Corresponding whole-colon wall layers, a blind cecal pouch, and a continuous ileocecal junction; molecular fermentation products are an explicitly enlarged sample. |
| 22 | Separate recovery-tube and vascular lumens; coherent kidney, ureter, and bladder anatomy with registered drainage fittings. |
| 23 | Matched gut-wall lumen views before and after water joins blood; the fitting changes fluid inside the vessel. |
| 24 | Corresponding epidermal and dermal layers, intercellular lipid seams, continuous sweat duct, and nerves entering through the cut boundary. Vessel-free dermis contains irregular collagen without vascular scaffolds. |
| 25–26 | Corresponding wound, platelet plug, reinforced clot, cleared wound, repair, and healed states. Crossing fibrin threads persist until clot removal. New cells, collagen, and capillary growth occupy the wound at the installed tissue scale; the loose branch has one free tip that joins its receiving vessel when fitted. |

The built-in image-generation tool painted the selected masters in [sources](sources/). Exact generation and edit requests accompany each selected source. Rejected generations and diagnostic strips remain disposable scratch under `runs/anatomy-composition-review/`. Only selected production sources, necessary edit inputs and exports belong here. `sources/muscle-storage-reference.png` preserves the exact muscle-repair input: the former metabolism master’s `(0,470,1536,1024)` crop, verified pixel-identical. `muscle-storage-v2-provenance.json` records the request, reference base, crop and selected output without changing the exact prompt. The capillary pair’s two-stage edit retains its former closed-loop reference and first generated pair under `sources/references/`; `capillary-growth-provenance.json` maps both exact request sections to those inputs and the selected final output. These reference images do not supply current runtime anatomy.

[produce.py](produce.py), [skin.py](skin.py), and [wounds.py](wounds.py) crop, mask, resize, and register painted source anatomy. They do not draw anatomical strokes. Within the intestinal family the common factor is 1.6; the muscle pair uses 0.53, colon layers 1.7, digestive pair 1.3, and healthy skin 0.72. Urinary fittings retain a common 696 × 1044 canvas, water fitting 640 × 975, healthy skin fittings 1043 × 782, and wound fittings 950 × 620. The six wound states normalize the generated cells to that shared specimen size. Mask transitions preserve existing white cells when fitting wound repairs.

[map.json](map.json) contains 48 selected identity exports and eight registered slot layers. [changes.json](changes.json) records approved local semantic and physical-description changes; the coordinating author integrates the canonical manuscript. The shared Blood source dependency is `../blood/sources/whole.png`, resized to 900 × 600 with the same alpha threshold as its owner package.

Run `uv run --with pillow python projects/anatomy/atlas/composition-review/body/produce.py` to reproduce the runtime exports. Paths, nonempty alpha, and slot/owner dimensions have been checked; actual-scale operations and white-background composites have been inspected. Independent composition review accepted chapters 19–26, with the final wound continuity correction accepted in round 11. The coordinating review record owns final outcomes. This package makes no learning or enjoyment claim.

Anatomical grounding: [OpenStax, small and large intestines](https://openstax.org/books/anatomy-and-physiology-2e/pages/23-5-the-small-and-large-intestines), especially the villus capillary bed and subsequent intestinal-to-portal drainage.
