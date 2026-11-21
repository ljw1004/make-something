# Defense and digestion production

This package implements the [shared production contract](../production.md) for the 67 identities first declared in chapters 15–21. It supplies transparent anatomical objects for the coordinator's blank navy sheet; it does not modify the manuscript, app, background or another package.

- [map.json](map.json) maps every exact parsed identity to an export and supplies the lymph-node receiver in chapter 17 and both pancreatic receivers in chapter 20. This range owns no compound slots.
- [assets/](assets/) contains the 67 production PNGs.
- [sources/](sources/) retains selected generated masters and the source inputs needed for their precise isolation/correction edits.
- [prompts.json](prompts.json) retains every exact request. All generation used the built-in imagegen tool with transparency requested, informed by the supplied Star Trek drawing reference.
- [produce.py](produce.py) records inspected crop bounds, sizes, masks, registration and composition. Reproduce with `uv run --with pillow python projects/anatomy-study/art-study/farout-star-trek/rework/defense-digestion/produce.py` from the repository root.

The source-to-prompt correspondence is `15-airway`→`15`, `16-lymph`→`16`, `17-immune`→`17`, `18-food`→`18`, `19-villi`→`19`, `20-storage`→`20`, `21-organs`→`21`, `21-microbes`→`21micro`, `21-upper`→`21upper`, `21-colon`→`21colon`, and `20-storage-final`→`20rings`. The last three are edits of the respective completed masters. The storage correction retained registered anatomy but introduced background alpha; extraction restores the original storage master's anatomical alpha rather than retaining the added haze.

The airway family retains the same four ciliated cells as its mucus layer gains particles. Lymph entry and neck return use separate tissue and junction closeups with an attached locator. Digestive glucose rings and amino-acid beads keep their dimensions when chains separate; saliva, bile and fat samples are spatial fluid volumes. The same glucose-ring shape is retained in blood and branched intracellular stores. Colon mucus, epithelium, supporting tissue and partial assemblies are masks of one completed slab on one registration canvas. Upper tract and colon are isolation edits of the finished organ master, preserving the organ positions and their assembly scale. The colon's attached cutaway shows the wall at an explicitly enlarged detail scale.

The circulation producer was given `16-lymph.png` and the lymph junction design for its chest fitting. The finale producer was given `21-organs.png` and the completed tract export for its lower-body fitting. Those receiving packages own their final registration.

## Production check

All 67 inventory identities are present, all mapped files decode as RGBA, and three fixed receivers have scene positions and hitboxes. All eight original atlases and three selected edit outputs were inspected at source resolution. All exports were inspected at one-quarter intrinsic size on navy and light grounds; corrected atlas bounds exclude neighboring sprites. Revised immune supplies, storage rings, transparent mattes and tract isolation received a further focused check. Both legal colon-wall orders retain exactly the same tissue pixels; there are no compound overlays in this package. Disposable inspection sheets were kept under ignored `runs/` and removed after recording this outcome.

This is informed production QA, not a student recognition study or medical validation. Fine subcellular structures are schematic; small molecular supplies rely on their item names alongside the art. The coordinator owns whole-story/browser layout validation, including receiver positions and fitting continuity in the chest and final body.
