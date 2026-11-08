# Chapter-one pinwheel artwork

This source implements the chapter-one movable-workpiece prototype. It imports
the original Builder paper's dimensions and hole factory from
`archive/2026.11.07 builder study/art/wind_toys.py`; the frozen source is unchanged.
The paper is a 160mm square, 0.25mm thick, with four prepared diagonal incisions
ending at its 24mm central web. The front is orange and the reverse a warmer
orange. Hole positions and paper length survive folding. Each fold follows an
exact 180-degree semicircle of radius half its tip height, then continues as a
horizontal plane. The four tip planes are separated by 0.35mm, leaving 0.10mm
between their 0.25mm sheets. A fixed-length bend followed by sloping tips was
rejected because those tip planes intersected each other.

The sequence has nine operations: fold each of the four prepared corners, add
the hub, turn it over, insert the axle, attach the handle, and turn the complete
pinwheel back. `pinwheel.py` supplies the canonical geometry for all states and
supplies. `fold_stages.py` adds the three partially folded states without changing
the frozen base model: upper-right, upper-left, then lower-left corners are
folded; the fourth operation folds the lower-right corner into the original
fully folded state.
Only the fold changes paper geometry. Adding a part only enables that part's
owned meshes. Flips select real cameras on the opposite side of the same model.

The new front-fitting hub has a 24mm teal face and a hollow 6mm stem. Its tapered
rear lips enter the prepared 6.4mm paper holes and capture the web. A slit in the
rear stem permits the nominal plastic tongues to flex. The rear-inserted axle
has a continuous 3mm shaft, a bonded smooth spacer, a mounting post and a split
pair of tapered retaining barbs. The tip snaps into an annular pocket inside the hub's closed
front. The hub has 0.3mm radial clearance around the shaft and a nominal 0.5mm
gap ahead of the axle's spacer. The wooden handle's attached side-entry C-clip
fits its rear post; the clip's side opening makes the authored assembly path
possible after the axle has already been installed.

These are ideal nominal dimensions, not a manufactured toy specification.
Plastic flexure, snap forces, material strength, paper recovery, friction and
wind torque are not simulated. `checks()` reports authored dimensions and the
paper endpoint check; it is not an independent validation. Mechanical
review must inspect evaluated meshes and insertion paths as well as these
numbers.

`verify.py` checks the actual evaluated meshes against prescribed insertion
poses. Hub tongues rotate inward by 5.3 degrees with a 2.2mm slot; their complete
radial envelope fits the paper holes and the two halves remain separated.
The axle's two barbs rotate inward by 4.8 degrees with a 1.5mm split; their
envelope fits the hub's bore without the halves crossing. These simple tongue
poses establish geometric space, without modelling stress or elastic recovery.
The handle clip's nominal mouth needs a total 0.333mm opening to admit its post.
The same check rejects folded-sheet crossings away from the shared web seams
and verifies that all five addition/flip transitions retain the exact evaluated
meshes already present.

Loose hardware uses larger inspection magnification. Front paper states share
one crop and scale, as do the two rear rotor states. Adding the long handle
zooms out to a whole-object view; no part changes its physical dimensions.
The front/rear workpiece drawings have a 320px visible long dimension at the
390px reference viewport, completed pinwheels 400px, the handle 270px, the hub
132px and the axle 145px. `pinwheel-carried.webp` uses the same finished geometry
at 184px for later chapters. All sizes are set in `export.py` and include a
separate three-pixel transparent margin.

The partial-fold adapter uses each blade's exact existing flat or folded mesh,
including its actual hole cutter. `verify_folds.py` compares all evaluated blade
meshes with those two baselines and checks partial-stage crossings. Its checks
are still-picture geometry checks; they do not validate the entire moving fold.
`render_folds.py` uses the same front camera, lights and selected render settings.
`export_folds.py` reads the selected base export's crop and applies exactly that
crop and pixel scale to each new state, rejecting any drawing outside it.

Run from the repository root, using a Pillow-enabled Python for the exporter:

```sh
python3 -m venv runs/builder-chapter-one/venv
runs/builder-chapter-one/venv/bin/pip install Pillow==13.0.0
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup \
  --python projects/builder-study/chapter-one-art/render.py -- \
  --output runs/builder-chapter-one/masters --samples 24
runs/builder-chapter-one/venv/bin/python \
  projects/builder-study/chapter-one-art/export.py \
  --masters runs/builder-chapter-one/masters \
  --output runs/builder-chapter-one/export/items
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup \
  --python projects/builder-study/chapter-one-art/render_folds.py -- \
  --output runs/builder-chapter-one/fold-masters
runs/builder-chapter-one/venv/bin/python \
  projects/builder-study/chapter-one-art/export_folds.py \
  --masters runs/builder-chapter-one/fold-masters \
  --baseline-masters runs/builder-chapter-one/masters \
  --output runs/builder-chapter-one/export/items
```

Rendering uses two CPU threads. Masters, source hashes, crop manifests and
review packets belong in ignored scratch space; retain these source files and
the selected runtime WebPs. Source hashes in a completed batch bind the files
that remained unchanged for that batch, not a stronger claim about prior
candidate runs.

Selected runtime artwork lives in `stories/builder/assets/`. Review scratch exports before replacing those files; the older study manuscripts preserve their historical source paths.

Display sizing is read by `export.py` from `production-settings.json`. Broad
paper and blade stages share a 184px inspection scale; hub and axle inspections
are 96px and 112px. The 270px handle and 400px finished pinwheel remain large,
with a 280px carried pinwheel for chapter 2. These sizes change only the export
magnification, never the model or the consistent crop within an additive group.
The opening browser checker (`../tools/verify-opening.mjs`) now follows both
chapters through the completed racer using emulated touch input at phone sizes.
