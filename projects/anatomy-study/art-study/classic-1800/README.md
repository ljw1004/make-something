# Classic 1800s anatomical atlas

[Play all four illustrated chapters](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/classic-1800/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

Independent chapter 1, 4, 8 and 18 study under the [Anatomy design brief](../../../../stories/anatomy/design-brief.md). The supplied [classic2](../../inspiration/classic2.jpeg) and [classic3](../../inspiration/classic3.jpeg) informed fine parallel engraving, anatomical contours, rose madder muscle, sage accents and restrained paper colour. These references were inspected directly; other artists' themes were not consulted.

[Full production source](anatomy.md).

All four selected backgrounds are **plain ivory, without anatomy or text**. Every anatomical illustration belongs to an interactive item or fitting. The copied manuscript retains the original narrative, identities, supplies, recipes, fates, goals and compound slots. Unselected chapters retain neutral backgrounds and placeholder artwork for their unillustrated items. Three later cell fittings remain transparent registered placeholders because those chapters are outside this comparison.

The selected chapters cover all 33 identities in the shared [comparison inventory](../checks/comparison-inventory.json), with the nucleus and four independent arm fittings.

## Production and material continuity

The opening family was rebuilt from [cell-material-master.png](sources/cell-material-master.png), generated with the built-in imagegen tool. Its [exact request](sources/refresh-request.json) is retained. A membrane strip and aqueous volume are extracted from the empty cell at the same magnification; the water is its enclosed volume, not a droplet emblem. DNA, envelope and nucleus are extracted from the same smaller nuclear cutaway. The fitted nucleus preserves their scale. Cropping supplies does not normalize their dimensions to equal squares.

The earlier selected arm, ear and digestion generations remain the sources for those chapters. [Original requests](sources/prompts.json) preserve their provenance. Ear exports use individually recorded factors to keep small eardrums and ossicles proportionate to their receiving assemblies. Digestion exports keep glucose units and amino-acid beads approximately consistent across chained and separated appearances. Those drawings include deliberate molecular explanatory views, distinct from the macroscopic food specimens.

The muscle-cell supply preserves three separately nucleated precursor cells. Its enlarged cellular view and the arm's tissue view express the story's change from precursor populations to organized muscle; it is not a whole detached biceps passed off as cells. The mineral supply samples the mineralized matrix from a bone window at that window's scale.

[build.py](sources/build.py) mechanically extracts, masks, crops, resizes and registers the selected raster artwork, creates the plain backgrounds and inserts presentation metadata into a fresh copy of the source manuscript:

```sh
uv run --with pillow python projects/anatomy-study/art-study/classic-1800/sources/build.py
node --experimental-strip-types projects/anatomy-study/art-study/checks/verify-semantics.ts projects/anatomy-study/art-study/classic-1800/anatomy.md
npm run lint -- projects/anatomy-study/art-study/classic-1800/anatomy.md
```

The old illustrated background sources are retained as superseded production history; the producer does not use them. The current `contact-sheet.jpg` contains the coordinator's four refreshed chapter panels with complete icon inventories.

## Registered constructions

The front and back bases are complementary pieces of **one** arm on the same 1560 × 2340 canvas, centred at `(780,1170)`. Both are interactive fixed regions with separate receiving hitboxes. Together they carry the shared bones, joint, tendons, labels, leaders and pale receiving regions. None of this anatomy is in the background. The four disjoint overlays restore biceps, triceps, radius-window mineral and ulna-window mineral independently; neither declaration order nor fitting order covers another fitted region. The bone windows are located enlargements of different bones.

The cell and its nucleus fitting share a 640 × 640 registered canvas. [registration.json](sources/registration.json) records source crops, masks, common canvases, factors and arm placement. The producer is authoritative for the exact extraction operations.

## Verification and limits

On 14 November 2026, the semantic checker found no differences from the original across chapters, items, readings, goals, recipes or tutorials. Native lint passed with **zero errors and six existing mixed-fate warnings** in later, unillustrated chapters. Mechanical checks confirmed four exactly uniform backgrounds, matching base/overlay dimensions and disjoint arm masks. Informed visual inspection covered the exported families, both cell states and all sixteen arm partial states. Browser routes, four complete comparison panels, real dragging and reload checks are coordinated separately.

Fine engraved lines and small eardrums require actual-size inspection. The generated nuclear boundary is an explanatory double-ring approximation, not a detailed ultrastructural diagram. The mineral sample shows deposited mineral within matrix rather than isolated crystals. Ear pictures use one representative side for plural item names. This is comparative artwork, not scientific peer review or evidence of student comprehension; no fresh blind recognition trial is claimed.

Central comparison review rebuilt the hearing stages from the retained component pixels, preserving the located sensory enlargement through both alternative assembly routes and the final ear.

Current browser verification and the complete chapter panels are recorded in the [consolidated refresh review](../../art-review/2026.11.14_22.26.04/report.md). Temporary review captures were removed after consolidation.
