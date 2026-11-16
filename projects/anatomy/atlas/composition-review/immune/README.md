# Airway and immune-response replacement family

Artwork for Anatomy chapters 15 and 17 under the active [design brief](../../../design-brief.md). `map.json` supplies fifteen replacement item assets plus positions for the two mutually exclusive fixed node states. The canonical manuscript is not edited here. Root integration applies the concrete chapter-17 changes in `changes.json` and checks fixed-state retirement; `description-replacements.json` describes the supplied pictures.

## Selected sources and production

Run `uv run --with pillow python projects/anatomy/atlas/composition-review/immune/produce.py`.

- `sources/phagocytes.png` is the root-generated three-state master: an empty macrophage, the same cell containing intact rods in a bounded phagosome, and the cell containing fragmented remains in that compartment. The compartment is visibly separate from the nucleus. All three retain the same source scale. Each state is extracted from its 724-pixel panel.
- `sources/airway.png` is the root-generated coherent mucus-covered ciliated epithelium. `airway-bare.png` is its matching built-in edit without mucus. The mucus supply follows the original surface plane; trapping adds actual dust and rod cutouts under a faint copy of the existing translucent gel, without drawing any anatomy in code.
- `sources/nodes.png` is the root-generated two-state lymph-node master. Each half retains the same 971×809 registration canvas. The responding state contains embedded populations and enlarged germinal centres, rather than giant independent cells overlaid on the organ.
- `sources/bacteria-extracted.png` contains three rods extracted from the intact-bacteria phagosome at their source dimensions. The same rods supply both bacterial items and the coating result, so coating and engulfment do not resize them.
- `sources/antibody.png` is a selected painted protein cutout from a built-in coating trial. The trial placed stems against bacteria, so its complete coating was rejected. Production rotates the selected protein and registers an actual binding-arm tip to each bacterial surface; no free glyphs remain. Loose proteins use the same dimensions as bound proteins.
- `sources/dust-sample.png` preserves only the three dust grains from the existing `atlas/circulation/assets/inhaled-particles-and-bacteria.png`.

Root generation requests are retained beside their sources. Exact additional requests and material-extraction provenance are in `edit-requests.json`. `airwayBare` uses `sources/airway.png`; `antibodySourceTrial` uses `sources/bacteria-extracted.png`, and only the selected antibody cutout survives from that rejected complete coating. `mucusClean` uses the former isolated mucus export mechanically extracted from `sources/airway.png`; the selected replacement is `sources/mucus-clean.png`, registered to the same source-plane bounds below. The producer records cell-panel bounds, mucus masks, shared bacterial registration, antibody contact points and scale factors. Different microscopic subjects have separate established illustrative magnifications; each construction preserves its own input-to-result scale. Molecular and material samples represent populations rather than literal counts.

## Integration and verification limits

Chapter 17 replaces the fixed Living lymph node with fixed Responding lymph node at the same position. An activated lymphocyte contributes to that growing population; the responding node persists while amino acids produce antibodies. The engulfing white cell transforms into its digestive state. These changes preserve five combinations and remove the old organ/cell overlay.

The producer inspected all fifteen exports and the coated-bacteria contact geometry at enlarged and playing sizes. Root integration owns lint and native review. Independent fresh review accepted chapter 17 in round 4 and chapter 15’s clean-mucus repair in round 7, with no remaining issues. Temporary previews and the rejected full coating trial remain under `runs/anatomy-composition-review/immune/`.

The earlier chapter-15 review accepted the phagocyte family but found ciliary fragments in the two isolated mucus sheets. A targeted built-in edit (`sources/mucus-clean.png`, exact request in `edit-requests.json`) replaces that contaminated edge with fluid alone. Its alpha bounds are registered back to the original 2027×214 source-plane rectangle at (81,119). Both isolated mucus exports use this clean sheet; cilia remain exclusively rooted in the epithelial artwork. Chapter 17's accepted artwork is unchanged.
