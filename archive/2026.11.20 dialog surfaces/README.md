# Dialog surfaces

The [contact sheet](contact-sheet.png) shows three repeats across and two down for each 144 × 144 px texture at the size used in play. Mars uses a flat 1 × 1 px image. The [story format](../../docs/story-format-spec.md#specification) and [UX](../../docs/ux.md#goals-and-readings) own the adopted syntax and player behavior.

## Production artwork

The six textures use the built-in ImageGen tool. Production crops were resized, recolored, and blended across the horizontal and vertical joins, then encoded as lossless WebP. The Mars surface uses flat stone gray (`#eef1f4`). The least contrast measured against black across the decoded images was 15.6 to 1, on the Settlement tile.

| Runtime asset | Material from the generation request |
| --- | --- |
| [Anatomy](../../stories/anatomy/assets/dialogs.webp) | light ivory cotton paper from a nineteenth-century anatomical atlas, extremely fine and softly pressed grain, fairly neutral white ivory |
| [Cookbook](../../stories/cookbook/assets/dialogs.webp) | warm pale butter-ivory cold-pressed watercolor paper from a well-kept illustrated kitchen notebook, soft nearly invisible tooth, gentle creamy yellow |
| [Creation](../../stories/creation/assets/dialogs.webp) | pale cool blue-white paper with a delicate diffuse blue-gray watercolor granulation, reminiscent of the sky palette of a creation myth, essentially still a white surface |
| [History of Ideas](../../stories/ideas/assets/dialogs.webp) | pale celadon-gray gray-green cotton book paper from a historian’s working folio, faint short paper fibers with very little contrast |
| [Mission to Mars](../../stories/mars/assets/dialogs.png) | pale cool stone-gray matte expedition log stock, clean utilitarian archival synthetic paper, barely visible fine grain, almost flat and cool white |
| [Settlement](../../stories/settlement/assets/dialogs.webp) | pale oatmeal unbleached rag paper for colored woodcut printing, subtle natural fiber texture, predominantly a very light pale biscuit cream |
| [Theology](../../stories/theology/assets/dialogs.webp) | very light biscuit-ivory vellum from a historical manuscript, quiet warm-gold undertone and faint even vellum grain, minimal warm honey |

Each generation used the following request, with the lowercase manuscript name and corresponding material above. Mars’s generated texture was a trial before the flat fill was selected.

> Generate one opaque full-bleed square seamless repeating raster texture tile for the {story} story's reading dialogs, specifically {material}. Intended for black text drawn on top. It should read as a single extremely light surface with only quiet near-microscopic variation. Fine organic texture density even edge to edge, matching opposite edges for continuous horizontal and vertical repeat. Flat scanned orthographic illumination, no directional light, no vignetting, no gradients, no border, no folds, no stains, no strong fibers, no speckles, no illustrations, no text, no labels, no layout. This is the texture alone.
