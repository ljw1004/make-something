# Independent artist assignment

This records the common assignment for the thirteen-theme comparison. The coordinator supplies each artist's reference image(s), theme name and exclusive output directory separately. The [Anatomy design brief](../design-brief.md) remains the single governing story brief; this is a production assignment, not another story or UX specification.

Read the repository instructions and README, the [icon guide](../../../docs/icon-guide.md), [story specification](../../../docs/story-format-spec.md), [authoring guide](../../../docs/story-authoring.md), relevant [engineering](../../../docs/engineering.md) and [UX](../../../docs/ux.md) guidance, the design brief and [source manuscript](../anatomy.md).

## Independence and art

- Inspect the assigned original reference images directly. Do not inspect another artist's theme, generated images, notes or prompts. Develop the visual interpretation independently.
- The shared audience is grades 9–10. The shared intellectual approach is modern textbook/medical-poster illustration: clear hierarchy, located enlargements, and purposeful changes of scale within a harmonious whole. Anatomical structures need not share literal scale. Historical and farout directions change the drawing aesthetic while retaining this explanatory approach.
- Cover original chapters **1, 4, 8 and 18**: cell boundary, bones/muscles, hearing and digestion. Produce plain, ruled or subtly textured blank-sheet backgrounds, plus all portable inputs, intermediate results, completed results, fixed regions and fitted layers needed in those chapters. Backgrounds must contain NO anatomy, diagrams, labels or finished examples. All content belongs to interactive objects.
- Use the built-in image-generation tool, following `/Users/ljw/.codex/skills/.system/imagegen/SKILL.md`. Use generated raster artwork rather than code-drawn stand-ins. Generated atlases and mechanical cropping, resizing, masking and registration are appropriate. `uv run --with pillow python` is available for mechanical processing.
- Plan backward from each completed construction. Constituents must retain the material, viewpoint and anatomical magnification they have in the result. Water is the aqueous volume that fills the bag, not a droplet symbol beside giant molecules; lipids are membrane material at the same repeating-unit scale as the resulting wall. Derive compatible parts and partial states from one generated master where useful. Located enlargements belong to the object. Never independently normalize every part to the same square.
- Chapter 4 shows one arm, with independent front/back muscle and mineral fittings. Plan the artwork in context so muscles meet their tendons and mineral belongs to its bone window. Preserve independent partial states and align all fitted layers. The opening cell also needs a registered nucleus fitting.

## Deliverables and integration

- Work only in the assigned theme directory. Retain the selected original generations, exported assets, exact requests, source references, registration/extraction information and any mechanical production script.
- Copy the full `anatomy.md` into that directory and link its own assets. Preserve narrative, item identities, chapter supplies, goals, recipes, fates and compound slots. Add presentation metadata only.
- Keep unselected chapters explicitly unillustrated, with neutral placeholders. The original placeholder is `../../placeholder.svg` relative to a theme manuscript. Follow the specification's requirement for default portable icons and slot overlays once a manuscript uses icons; do not introduce extra supplies while adding those declarations.
- Original unillustrated backgrounds are 1×1 pixels. Globally positioned primitives are checked against every chapter that may supply them; either omit their starting centres or provide correctly sized neutral draft backgrounds where needed. Hotspot hitbox metadata uses a direct child `- hitbox:` bullet.
- Do not edit the original manuscript, application, shared documents or another theme. Do not start additional agents. A theme is a comparison candidate, not an adopted production style.
- An optional shared [presentation exporter](integrate-art.ts) can create the copied manuscript from your own `art-map.json`. Its `ArtMap` type documents the mapping. It contains no style choices or other artist's assets. You may instead use your own producer; either route must pass the semantic comparison.

## Verification and handoff

The ordinary development server is already available at `http://127.0.0.1:5173`. Run `npm run lint -- YOUR_COPY` and compare gameplay with the original using the retained `projects/anatomy/art-study/checks/verify-semantics.ts` checker. Preserve a concise final outcome and material limitations, not raw logs.

The coordinator captures four chapter views, checks real drags and reload, and assembles four chapter comparison panels per theme. Each panel includes the playable composition AND all relevant inputs, intermediate/result icons and fitted states, so the user can inspect the complete art family. The artist should prioritize artwork, manuscript integration, provenance and lint, then report completion promptly so another independent artist can start. Raw browser proofs and disposable intermediate generations belong in ignored `runs/`.

## Playable comparison delivery

The gallery must link to each theme’s `sample.md`, generated with [checks/build-samples.ts](checks/build-samples.ts). This excerpt plays original chapters 1, 4, 8 and 18 consecutively, then ends. Keep `anatomy.md` as the full production source. Verify normal Continue progression through the entire sample with `checks/capture.mjs --sample THEME...`; checkpoint jumps alone cannot verify this delivery.
