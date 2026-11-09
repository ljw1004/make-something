# Full Builder revision — working production sources

The [live brief](../../story/design-brief.md) is the single design authority.
This directory holds the replacement family manuscripts and their dimensioned models.
Review the actual compositions before producing the final art. The earlier opening
remains independently authored in `chapter-one-art/` and `racer-art/`.

## Family interface

Each family has `NAME.md` (chapter sections only, relative `assets/` paths) and
`NAME.py` (Blender geometry). Use unique item/chapter IDs. Every build stays movable;
only actual processes are hotspots. No automatic routine prose or result notices.
Place optional physical explanations after `---`. Repeated components are literal
individual supplies, with sensible interchangeable or independent assembly orders.

The model module exports:

- `PLAN`: mapping each illustrated identity to `{parts: [physical part keys], group:
  "shared-camera-and-magnification-family", css: visibleLongestCssPixels, image: optionalFilename}`.
  One image may serve physically identical supplies. Export variants have their own
  illustrated identity. Add any additional pose metadata needed by the family.
- `build()`: returns at least `{root, parts}`, where parts maps physical ownership
  keys to Blender objects. Every supplied drawable is one connected part or retained
  mechanism; no separated piles, loose unowned lids or test scenery.
- `stage(model, identity)`: reset the complete model pose, show exactly PLAN's parts,
  then return `{location, target, scale, roll: optionalRadians}` for an orthographic
  camera. Reject unknown identities. Keep physical dimensions fixed. Shared viewing
  groups must also share camera and scale; explicit flips use a distinct group.

Use the shared flat palette in `../materials.py` before creating materials. Import
reusable archived geometry helpers without editing their historical sources. New
source changes belong here. Preserve real insertion paths, mechanical clearances
and useful motion controls. The [working-loop pipeline](../animation/README.md)
uses those same models; no texture maps are needed.

Typical display dimensions: broad workpieces 190–270 CSS px, compact loose parts
75–125 px, slender diagonal parts 110–180 px, subassemblies 150–250 px, completed
objects 320–360 px. These are starting points, verified in the browser. Rendered
openings remain transparent; materials keep their real opacity. Framing may change
between inspection, work and completed views; fitted parts never resize physically.

Each page uses `assets/backgrounds/white.svg` and a picture reference to its actual
build target, with a short object-name caption. A single process is centered at
(390px,216px). Two processes use (130px,216px) and (390px,216px), with a 236×248
background-pixel hitbox; the reference occupies the right third. The opening
pinwheel has Flip first and Fold second. Use each page's
own process IDs, declared as Items. The background is 780px wide; image export is
four image pixels per CSS pixel at the 390px reference width.

Models, routes and source instructions are retained. All renders, proofs, logs,
reviewer inputs and detailed verification output belong under ignored `runs/`.
Only accepted runtime images are promoted beside the story. The full revised
manuscript, fresh playtests and concise evaluation outcomes remain in this study.

## Reproduce a candidate

Regenerate a family's fragment from its Python route declarations. The three retained early
families use `python3 projects/builder-study/full-story/early_author.py`; each other
family writes its own fragment when run with ordinary Python. These commands do
not render or publish. `opening.md` contains the current independent opening;
the racer author accepts an explicit scratch output path when revising it.
Periscope and kaleidoscope sources remain for the earlier numbered drafts; they
are excluded from the current authoring and assembly commands.

Assemble into a new version, preserving versions used by retained playtests:

```sh
python3 projects/builder-study/full-story/assemble.py --output projects/builder-study/builder-vNN.md
node projects/builder-study/tools/verify-full-graph.mjs projects/builder-study/builder-vNN.md runs/builder-full/graph.json
```

`captions.json` owns the literal descriptions of exported pictures. After a fresh
image-only audit, pass `--captions projects/builder-study/full-story/captions.json`
to the assembler. It inserts `{...}` item passages and requires coverage of every
primary WebP item image. Review carried image variants against the same passage
too. Caption files must be flat JSON objects mapping image IDs directly to
nonempty strings; nested reviewer envelopes are rejected rather than silently
leaving older descriptions in place. Keep only current primary-image keys in the
production map. The shared engine preserves these passages for text players; the browser
omits them according to the [format rule](../../../../docs/story-format-spec.md#specification).
Do not derive captions from model metadata or use them to supply hidden joints,
functions, motion or future instructions. `contact_sheet.py` produces disposable
review sheets from actual exported images, optionally at their natural CSS size.

Pass `--motion-captions projects/builder-study/full-story/motion-captions.json`
after the working loops and final exchange have received their own literal visual
audit. The assembler requires a description for every selected animation. These
alt descriptions become separate text-player motion observations; they never
change the still goal picture's description. New result observations let fast
players receive the visible change even on a chapter's last action.

Review insertion paths and motion before rendering. For each frozen family:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup -t 2 --python-exit-code 1 \
  --python projects/builder-study/full-story/verify_additions.py -- \
  --family pinball --output runs/builder-full/pinball-additions.json
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup -t 2 --python-exit-code 1 \
  --python projects/builder-study/full-story/render.py -- \
  --family pinball --output runs/builder-full/pinball-masters
runs/builder-full/venv/bin/python projects/builder-study/full-story/export.py \
  --family pinball --masters runs/builder-full/pinball-masters \
  --output runs/builder-full/preview/assets/items
```

The selected exports use Pillow 13.0.0. Recreate the ignored environment with
`python3 -m venv runs/builder-full/venv`, then
`runs/builder-full/venv/bin/pip install Pillow==13.0.0`. Renders use two CPU threads, transparent Standard
colour output at exposure −2.75, 1280px and 24 samples. Render and export complete
groups together to determine their common physical magnification, then tightly
crop each stage to the geometry present in that stage. A small
pilot render is an inspection input, not a production manifest. Every production
manifest must contain the expected images and unchanging source hashes; Blender
can print a Python exception without returning a failing process exit code.

`verify_additions.py` compares evaluated meshes, material assignments, ownership
and cameras. Existing components must remain unchanged during a fitting. A common
rigid settling movement is diagnosed but still fails the additive-fitting check;
an access-changing turn belongs in an explicit process action.
Folds and flips are explicit process recipes, assessed separately. This check does
not prove insertion paths, retention forces, collision-free motion or legibility.

Preview with all candidate assets staged under `runs/`, then use
`tools/verify-full-browser.mjs` (relative to the study) to replay the complete route
through actual pointer events. It captures each state for inspection, checks
minimum hit areas, enlarged process margins, reference presentation, chapter
reloads and missing images. Keep those captures temporary. Promotion includes
only referenced accepted assets, the manuscript and its updated source record.
