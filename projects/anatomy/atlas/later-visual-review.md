# Later atlas visual review

Fresh informed model review begun 15 November 2026, approximately 00:35 PST, by `atlas_review_later`. The reviewer did not produce these assets. Instructions: [production brief](production-brief.md), [active design brief](../design-brief.md), and [icon review guidance](../../../docs/icon-guide.md). Supplied context included item identities, manuscript descriptions, maps, producers, and the classic2/classic3 references. This is neither blind recognition nor evidence of human comprehension.

## Scope and method

Reviewed the initial circulation exports for chapters 9–17 and body exports for chapters 19–27, before repairs prompted by this review. Every mapped item in those ranges was inspected on ivory at source pixels / 4, preserving relative size. Inspected all four chest partials, all four urinary partials, all four skin partials, and all eight wound partials. Read `circulation/produce.py`, `body/produce.py` and both maps. Diagnostic sheets and scripts are disposable under `runs/anatomy-atlas/later-review/`. Root owns browser progression checks. Chapter 28 remains pending until its producer declares exports ready.

## Initial outcome: change required

The restrained engraving, naturalistic contours and rose/sage/ochre palette support the selected atlas direction. Most material and cellular items depict their present contents without purpose badges, former ingredients or detached inset diagrams. Lung construction and gut-wall layers retain a coherent physical family. The following concrete defects prevent accepting these versions:

- **Detached venous return:** `capillaries-and-venous-return.png` and `body-blood-vessel-network.png` leave a visible gap between the blue capillary outlet and the added vein.
- **Lining floats in the lumen:** `arterial-vessels.png` and `thin-walled-veins.png` place a wavy strip across the open vessel rather than against its inner wall.
- **Heart/route scale and joins:** `heart-and-two-routes.png` and `heart-with-connected-vessels.png` place a disproportionately large heart over the body-wide vessel tree, reaching from chest toward thighs. Pulmonary trunks do not visibly join the heart outlets. Their partial route states inherit the problem.
- **Chest clipping:** the fitted diaphragm ends on the bottom edge of the common 1400-pixel canvas with a straight crop. The common canvas needs room for the complete addition.
- **Urinary registration:** fitted ureter upper ends meet the lower kidney silhouettes while the existing inward-facing yellow outlet stubs remain separate.
- **Sweat outlet incomplete:** the fitted duct stops within the outer cell layer instead of reaching the visible skin surface, contrary to the supplied outlet description.
- **Invisible clearing transition:** `skin-with-a-cleared-wound.png` is pixel-identical to `skin-with-a-reinforced-clot.png`; the described fragment clearance and engulfed remains are absent.
- **Sprout fitting:** the fitted capillary is a mask of pre-existing vessels, not the supplied branching sprout. At playing size its contribution is effectively invisible; the prescribed new branch meeting another vessel is not established.
- **Extraction contamination:** pale floating fragments appear above `tiny-capillary-tubes.png`; below `insulin-in-blood.png`, `glucagon-in-blood.png`, `muscle-fibres-beside-a-blood-vessel.png` and `protein-messengers-from-the-wound.png` (also reused by `clot-clearing-enzymes.png`); and beside `rf-worn-red-cells.png` and `rf-recovered-iron.png`.

All reviewed compound overlays match their base canvas dimensions. Stable anatomy remains registered across the inspected partials; wound surface closure and supporting fibres visibly contribute within the original cut. These technical successes do not resolve the defects above. Repaired versions require a different fresh reviewer under the icon guide; this record describes the initial versions, not their subsequent acceptance.

## First chapter 28 inspection — 15 November 2026, approximately 00:45 PST

The producer confirmed that the first-reviewed finale version included the refreshed diaphragm, continuous eye, and skin generated against the assembled pose. The reviewer had not previously seen chapter 28 art. Repaired chapters 9–27 were not re-reviewed. Inspected all sixteen chest fitting subsets, all four lower-body subsets, all four head/sensory subsets, both skin states, the four regional completions, and `trunk-and-limbs`, `body-beneath-the-skin`, and `body`. Images were alpha-composited over ivory at source/4; two native-resolution diagnostic details checked the midriff and forearm opening. Reviewed `body/finale.py` and current chapter 28 descriptions.

**Outcome: change required.**

- The chest and abdomen leave a visible ivory/transparency gap beneath the diaphragm, retained in all three whole-body stages including the final cutaway. The regions do not visibly meet at matching edges. This is a specimen continuity failure, not transparent-RGB display noise.
- The all-fitted lower-body compound paints urinary organs after the gut, whereas `lower-complete` and subsequent whole-body exports paint gut after urinary organs. Kidneys and bladder visible in the fitted regional state disappear behind the gut during the join. Use consistent physical occlusion across the same assembly family.
- The chest lymph layer uses an isolated cropped lymph tree without the already built neck-vein junction required by the chapter's supplied description. Its upper trunk does not visibly meet a vein.
- The lower-region gut crops away the upper food pipe; `finale.py` supplies no continuation through chest/head, despite the chapter's explicit continuity requirement.

No duplicated head, brain, kidneys or digestive tract, detached magnification inset, or purpose badge was found in this version. Sensory fittings remain inside the existing head and retain registration. The forearm inspection opening receives a small local skin segment; its reduced scale is appropriate to the body-scale handoff. The skin follows the assembled pose and the completed body is readable as one figure at 275 × 550 display pixels, subject to the midriff defect above. All four compound families have correctly matching overlay/base canvas dimensions. These are informed visual observations, not human recognition or browser interaction evidence. A different fresh reviewer must evaluate any revised finale.
