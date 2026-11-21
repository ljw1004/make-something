# Nervous-system replacement family

Replacement artwork for Anatomy chapter 6 under the active [design brief](../../../../../stories/anatomy/design-brief.md). The selected family is **posterior revision 4**, with corrected lower-root routing and a naturally prepared nerve receiving site. Fresh independent round-13 review accepted every criterion and operation with no remaining issues. Root integration owns canonical adoption. No recipes change. `map.json` supplies eleven transparent PNGs under original item IDs; `description-replacements.json` supplies viewpoint descriptions.

Run `uv run --with pillow python projects/anatomy-study/atlas/composition-review/nervous/produce.py`.

## Selected sources

The built-in image-generation sources retain one registered 1024×1536 posterior view. Exact requests are in `edit-requests.json` and `lower-route-requests.json`.

- `whole-posterior-v3.png` supplies the accepted upper whole. `tissue-posterior-v3.png` supplies its brain and the selected sensory/motor/common nerve junction.
- `lower-routes-reference-v4.png` is the exact first lower-route correction used by the subsequent local bone-channel edit. It remains a necessary selected production input, although it does not directly supply runtime artwork. `lower-route-requests.json` records the input/output chain with paths relative to its `sources` reference base.
- `lower-routes-whole-v4.png` corrects descending lumbar and sacral roots. Distinct bundles peel laterally to exits; two paired sacral routes enter visible foramina through locally dissected channels. Only a thin central filum continues to the tip. The producer adopts the lower region below y1060 with a five-pixel blend, retaining the original upper geometry. The old registered outer silhouette removes generated background haze outside the specimen.
- `whole-registered-v4.png` retains that cleaned composite as the exact reference supplied to subsequent edits.
- `receiver-v4.png` removes the selected large nerve from that whole and supplies natural short rootlet ends, continuous canal tissue and the exposed lateral bone boundary. It replaces the earlier rectangular erased patch.
- `bones-v4.png` removes nervous tissue from the registered whole, leaving matching empty protective bones and lower exits.
- `prepared-tissue-v4.png` isolates the matching brain, cord and lower roots from the prepared receiver. Its cord supplies the loose specimen; no broad rectangular mask removes its nerves.
- `whole-windows-v2.png` and its request are retained solely as a required reference input for the selected finale body-master generation. They do not supply current chapter-6 art.

The posterior skull window, opened vertebral arches and midline cord share one viewpoint. The selected right junction has a sensory ganglion, motor-root union and common outgoing trunk. Its approximately 220 source-pixel width becomes roughly 45 CSS pixels at the uniform 0.85 export scale and normal four-to-one chapter background scale. There is no separate enlarged inset.

Bone separates at source y350, while brainstem and cord separate at y310; the protected cord retains its short exposed upper tip. Final installed views retain generated bone occlusion rather than overlaying every isolated root on the column. The selected nerve's two inputs are complementary tissue regions of the same junction. Exports have six-pixel transparent margins; alpha below 12 is discarded.

## Verification limits

Fresh round-7 review accepted the components and upper arrangement but found lower roots converging into a terminal tassel and a rectangular prepared site. Revision 4 addresses those two findings. The producer inspected the loose, empty, protected, central and completed states together on a light background. This is self-inspection, not independent acceptance or student evidence. The subsequent fresh independent round-13 review accepted components, composition, the standalone whole and every operation, with no remaining issues. This visual judgment does not establish student learning outcomes.

Unsuccessful sources and disposable previews belong under `runs/anatomy-composition-review/nervous/`. The finale now has its own integrated anatomy; unused head/whole handoff exports are no longer retained in this package.
