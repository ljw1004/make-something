# Opening constructions, chapters 1–7

Implements the [shared contract](../production.md) for 50 identities and 12 compound fittings. [sources/](sources/) retains the selected imagegen masters and exact requests. [produce.py](produce.py) mechanically crops, masks, resizes and composites their pixels; [map.json](map.json) and [registration.json](registration.json) record runtime assets and fitting geometry.

The membrane bag is one source: lipid sections and the water volume retain its geometry, material and magnification. Cell interiors use actual fitted organelle sizes. The arm is decomposed into two visible skeletal receivers with four independently registered additions. Muscle-cell populations change presentation in chapter 4 to anticipate the fibers they become. The neuron remains continuous beneath separate sleeves and channels. The eye's constituents and intermediates are spatial partitions of one connected eye master; transparent unused extents are cropped without changing anatomical pixel scale. Skull, brain and cord use the same final registration. Later head-scale eye and ear appearances fit the chapter-28 body.

```sh
uv run --with pillow --with numpy python projects/anatomy-study/art-study/farout-star-trek/rework/opening/produce.py
```

The original arm master/request are reused from the initial study. Other opening masters were generated for this rework; the exploded eye atlas remains as the input reference for its selected connected-eye edit. The coordinator's [review record](../../../../art-review/2026.11.14_21.49.10/report.md) records visual and browser verification and its limits.
