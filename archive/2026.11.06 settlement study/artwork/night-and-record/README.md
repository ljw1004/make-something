# Settlement artwork refinements

Selected built-in imagegen edits; exact prompts and input references are retained beside each master. Original input images remain available as edit references. The too-close v2 ending master is retained because it was a reference for the approved v3 composition; v4 preserves that composition with a quieter palette. The [story brief](../../../../stories/settlement/design-brief.md) owns current visual intent.

| Runtime asset under `stories/settlement/assets/` | Change | Reproduce from repository root |
|---|---|---|
| `icons/pond-water-v3.png` | Lighter, level reflective water close to the rim, distinct from empty blue glaze; 288×224 RGBA. | `uv run --with pillow python 'archive/2026.11.06 settlement study/artwork/night-and-record/export.py'` |
| `icons/encyclopedia-v3.png` | Printed botanical illustration without tape or a pasted leaf; matching wood covers and sewn binding; 640×426 RGBA. | Same command. |
| `backgrounds/settlement-record-v4.webp` | Medium-wide view of the full table, chair and a moderate patch of floor in the familiar room, with matching printed spread; 780×1688, softened ochre palette, slightly richer than the original room; no additional cream treatment. | Same command. |
| `backgrounds/astronomy-night-v2.webp` | Dark ground and sea, moonlight, stars and a small lighthouse light; 780×1688, 22% cream once. | `node 'archive/2026.11.06 settlement study/artwork/night-and-record/export-astronomy.mjs'` |
| `icons/stove-base-v2.png`, `icons/cooking-stove.png` | Bare stove keeps its natural 224×224 canvas; the complete stove with pot uses 224×320, preserving the stove body scale. Padded component layers are export intermediates. | `uv run --with pillow python 'archive/2026.11.06 settlement study/artwork/night-and-record/export-stove.py'` |

Plant returns to the existing `icons/plant.png` at 224×224. The binding-table target is authored in the manuscript as a 320×213 background-pixel rectangle centred at (330,430), exactly matching the binding boards; the book's tabletop position is unchanged.

See [references.json](references.json), the matching `.prompt.txt` files, [astronomy metadata](astronomy-night-v2.metadata.json) and [stove request](stove-pot-v3.request.json) for generation provenance. No CLI/API image-generation fallback was used. Browser captures and verification scripts are disposable; concise results belong in [outcomes](../../outcomes.md).
