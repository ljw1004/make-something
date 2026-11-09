# Independent sail and racer

`build.py` is the canonical dimensioned model for the two racer chapters. It
uses metre coordinates, Z up, with the front axle at positive X. All stages
select parts of that model. Turning the chassis over applies a rigid half-turn;
no fitting rescales or bends an existing part. The chassis starts upright, turns over for the bearings and wheel units, then turns upright for the sail. Flat printed locating marks distinguish its two faces. The flat material palette lives
in `../materials.py`; there are no texture maps.

`author.py` produces the c02 sail chapter and c-racer-body chassis chapter in
an explicitly named draft, plus the component map `construction-plan.json`. The pinwheel
stays independent. Thirteen sail recipes and thirty-one chassis recipes support
independent fitting orders and interchangeable wheels; completion takes four
and eleven actions respectively. `../tools/verify-racer-graph.mjs` exhausts their
legal assembly orders using the shared engine, including terminal leftovers.

Each of the two straws receives two individual wheels. The wheel sockets have
integral spacers and gripping ribs. Open bearing channels accept those complete
units from underneath; the saddles clip into actual chassis slots. The axles
rotate inside the bearings. Each bearing icon is one connected factory fitting,
with its channel and saddles, never two separated tubes represented as one.
Integral tapered noses guide the saddle and foot locking legs inward during
insertion; square rear shoulders retain the fitted part.

The mast and crossbar are separate wooden rods. Offset sockets in the connector
keep them from intersecting. The foot grips the mast and snaps through the
chassis hole. Three open clips are attached to the sail; small integral tabs
keep the cloth clear of the connector while preserving the clips' spring
sections. These are nominal geometry and prescribed fitting paths, not tested
manufacturing specifications or a simulation of real elastic forces.

`render.py` makes disposable transparent masters with two CPU threads. Mast
states share a camera and scale, as do underside chassis states. Loose parts
have inspection views, often diagonal. The Flip and completed-racer views expose
the newly relevant structure. `export.py` uses `display-settings.json` for loose
part caps, assembly scales and the smaller carried sail. It preserves a common
physical scale within each additive family while cropping each current state tightly.
Three through-holes in each connected wheel make its rotation visible in the
completed toy's loop. Labels and touch targets remain
engine-owned; visible materials are opaque and actual openings transparent.

Run from the repository root with a Pillow-enabled Python:

```sh
python3 projects/builder-study/racer-art/author.py --output runs/builder-racer/opening-draft.md
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup \
  --python projects/builder-study/racer-art/render.py -- \
  --output runs/builder-racer/masters
runs/builder-racer/venv/bin/python projects/builder-study/racer-art/export.py \
  --masters runs/builder-racer/masters --output runs/builder-racer/assets/items
node projects/builder-study/tools/verify-racer-graph.mjs \
  runs/builder-racer/opening-draft.md
```

Inspect exports in the real browser before promotion. Selected artwork lives
only in `stories/builder/assets/items/`; masters, manifests, captures and detailed
geometry reports are scratch. The [evaluation record](../racer-evaluation.md)
retains review instructions, concise outcomes and evidence limits. The previous
fixed-racer adapters and registration are superseded; Git history retains them.
