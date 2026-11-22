# Anatomy — complete 1800s atlas

The [study manuscript](../anatomy.md) records the selected illustrated edition added to the [catalogue](../../../contrib/anatomy/anatomy.md). Both follow the [design brief](../../../contrib/anatomy/design-brief.md). The edition includes 28 playable chapters and an epilogue. The [chapter-by-chapter composition revision](composition-review/README.md) uses a fresh independent reviewer for every chapter and every revision. Its [outcomes](composition-review/outcomes.md) supersede the earlier broad visual review below.

- [Play the study manuscript](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/anatomy.md).
- [Review all chapters and their complete icon inventories](http://127.0.0.1:5173/projects/anatomy-study/atlas/review.html).
- [Complete chapter contact sheet](all-chapters.jpg).
- [Frontispiece and chapter background sources for the catalogue edition](backgrounds/README.md).
- [Nuclear envelope candidates](nuclear-envelope-studies.jpg).
- [Combination changes and scientific grounding](story-changes.md).

All anatomy on the chapter boards belongs to interactive objects. The study chapter backgrounds are blank ivory paper. Fine naturalistic engraving, restrained washes and continuous cutaways follow the selected 1800s direction. The [present-state rule](../../../docs/icon-guide.md#depict-the-present-physical-object) excludes purpose/history symbols, detached enlargements and duplicate diagrams. The nuclear envelope source retains two porous double-wall candidates; the frontal cutaway is selected to expose the tangled DNA.

## Production

Four packages share the [production contract](production-brief.md): [opening](opening/README.md), [arm and digestion](arm-food/README.md), [circulation](circulation/README.md), and [body and finale](body/README.md). Each retains exact built-in image-generation requests, selected masters, mechanical crop/composition scripts, runtime cutouts and a `map.json`. Existing comparison studies and supplied inspiration remain intact.

Replacement specimen families live together under [composition-review](composition-review/README.md). The integrator applies them after the original packages. A representative single cell can stand for a population; the chapter reviews distinguish that allowed convention from disconnected anatomy or incompatible physical scales. Chapter 3 reuses the completed cell, and chapter 4 now develops bone-building cells before matrix production and mineralization.

`integrate.ts` applies package artwork to the study manuscript and preserves its recipes. It is repeatable and supplies explicit IDs only where chapter-dependent artwork requires them. `identity-aliases.json` records those presentation aliases. `coverage.json` records the integrated item and fitting counts. Producers need Pillow. The opening producer also uses NumPy and SciPy for mechanical fragment cleanup.

With the local development server running:

```sh
node projects/anatomy-study/atlas/integrate.ts
npm run lint -- projects/anatomy-study/anatomy.md
node projects/anatomy-study/atlas/check-player.mjs
node projects/anatomy-study/atlas/composition-review/prepare.ts round-N
uv run --with pillow python projects/anatomy-study/atlas/composition-review/render.py runs/anatomy-composition-review/round-N
uv run --with pillow python projects/anatomy-study/atlas/make-sheets.py runs/anatomy-composition-review/round-N
node projects/anatomy-study/atlas/check-gallery.mjs
```

The browser check follows ordinary drags and Continue controls consecutively through the book, checks every chapter's visible artwork and saves/reloads completed progress. Optional chapter numbers use developer checkpoints for focused repairs. `WIDTH` and `HEIGHT` select a verification viewport. Choose a new unused round name. The sheet exporter requires packets whose manuscript and artwork match the current files; it retains the construction lists and all ingredient/result strips in the gallery. Captures and detailed outcomes stay disposable under `runs/anatomy-atlas/`; only requested sheets and concise review outcomes are retained here.

## Current verification

The current edition has **257 illustrated identities, 23 fitted layers and 147 authored/implicit recipes**. Its native completion route uses **132 combination/fitting actions** across 28 playable chapters and the epilogue. The gallery includes 28 complete inventory sheets, their construction lists and 132 ingredient/result strips.

The [composition loop](composition-review/README.md) completed **86 reviews in 86 distinct fresh conversations**. Every chapter now has an accepted independent review of its components, composition and standalone anatomy. Revised image families were sent to new reviewers; producers did not supply their own acceptance. The final pixel/operation comparison matches accepted versions for **all 28 chapters**, including later changes to shared assets. The [concise outcomes](composition-review/outcomes.md) retain the initial findings, adopted repairs, current criteria and version hashes.

Native progression completes. Lint reports **zero errors and seven warnings**: six reviewed mixed-fate hints and the 20,000-state fixed-item analysis limit. This is not exhaustive fixed-state verification.

The final graphical run completed **all 28 chapters consecutively at 390×844**, using ordinary drags and chapter transitions, a save/reload after every chapter, and the epilogue. All 132 actions passed with no missing images or browser exceptions. Focused chapter-6 and chapter-28 routes also passed at 390×740 and 1280×900; the finale’s last layout revision was rechecked at both sizes. Its taller blank sheet keeps the starting components clear of the goals. The gallery’s 28 panels, 132 recipe illustrations and 165 local links load without broken images or browser errors.

The remaining minor review note is chapter 17: individual antibodies occupy only a few pixels at phone scale. Its material and binding geometry passed; the enlarged inventory remains available for inspection. These are technical and informed model reviews, not student learning, unaided recognition or independent medical certification. Raw packets, reviewer answers, captures and logs are disposable; selected art, exact requests, requested sheets and concise outcomes remain.

Final manuscript SHA-256: `39a0b968aec2270faf02da4d452718bfa753a0fc07f33833c66df75f21479a1e`.

## Previous-edition verification

The following record applies only to the manuscript hash at the end of this section. The subsequent independent chapter review found substantial composition defects despite these technical passes. It must not be read as acceptance of the current revision or as proof that technical registration establishes natural anatomy.

The native reference route completes. Lint has six reviewed mixed-fate hints and a fixed-state analysis bound warning; the 20,000-state analysis limit prevents a claim of exhaustive fixed-state verification. The final illustrated manuscript passes lint with **zero errors**. The native route reaches the epilogue with 130 combinations and one placement.

The ordinary graphical player completed **all 28 chapters consecutively at 390×844**, including the epilogue transition, artwork loading and a save/reload at every completed chapter. Eight additional focused routes passed at 390×740 and 1280×900: 36 final chapter checks and 186 successful pointer operations in total. No broken images or browser exceptions remained. The gallery loads its 28 chapter panels and all local links. An early test-harness race at the final transition was corrected by waiting for the chapter's normal Begin control after asset loading; no application change was needed.

Independent informed visual reviews caught and led to repairs in eye/ear/nerve joins, stray crops, vessel linings, heart/diaphragm registration, kidney drainage, visible wound changes, and final-body continuity, scale and occlusion. Revised artwork received fresh reviewers. The [opening/arm/digestion and final-layer review](visual-review.md), [later-family review](later-visual-review.md), [first repair review](repair-review.md), and [final body review](final-body-review.md) retain their scoped outcomes and version limits. The final accepted checks leave no reported visual blocker. Earlier failures remain recorded as earlier versions, not current unresolved defects.

These are technical and informed composition checks, not student learning, unaided recognition or independent medical validation. Small details naturally become small in the final body: the construction chapters retain their larger inspection scale, and no detached magnifying inset is added.

Verified manuscript SHA-256: `6ba7ec40066ea9038f339d26d2d1fa88a50b6976dc8d7932136496a955211398`.
