# Completed-toy working loops

This pipeline uses the [active Builder brief](../../../stories/builder/design-brief.md)
and the existing canonical assemblies. `adapters.py` selects each finished state;
`mechanisms.py` supplies its operating pose. Source geometry remains owned by the
original family factories. No object is rescaled, and rigid members keep their
mesh vertices while their actual shafts, pivots, followers and links move.

Ordinary loops contain 96 frames at 15 fps (6.4 seconds). The projector uses 120
frames (8 seconds) to visit its separate projection screen and return. Frames
sample the half-open interval `[0, 1)`, with no duplicate endpoint pause. The
pinwheel adds a modest camera excursion while its paper and hub rotate around
the fixed axle. Other mechanical views keep their first camera direction.

| Toy | Operating motion |
| --- | --- |
| Pinwheel | Paper and hub rotate together; axle, bearing spacer and handle remain fixed. Boolean cutters follow their owning moving meshes. |
| Wind racer | Two complete straw axles roll a short distance forward and back; wheel angle is distance divided by the actual 30 mm wheel radius. |
| Pinball table | A prescribed marble rally passes through the centre arch and returns to the phased right flipper; the ball stays supported by the actual tray. |
| Crank dragon | Existing eccentric-cam solver drives the follower, spring, two fixed-length links and wings. |
| Gantry hoist | Winch, keyed crank, ratchet and pulley wheels move with the cord. Extra wound cord raises the hook and basket; the spring pawl releases for lowering. |
| Electric carousel | Existing spindle control rotates the deck, roof and horses; motor speed follows the real pulley ratio. |
| Pneumatic claw | Existing non-toggle solver moves both syringes, slider, rigid links, jaws and elastic return. |
| Animation drum | Wall, picture strip, floor and rotating bearing surfaces turn around the fixed spindle and base. |
| Drawing rover | Exact differential-drive circle, with +5/−1 complete wheel turns; the real lowered pen retraces a separate line on the work surface. A modest tracking camera preserves its finished view and keeps the toy centered. |
| Star projector | Disc and handwheel rotate; real punched-hole coordinates supply the inverted thin-lens image on a separate translucent rear-projection diffuser. |
| Flying whale | Powered lift moves the intact loaded carrier; the projector uses the actual belt ratio, and the carried pinwheel turns on its fixed axle. |
| Open window | The authored separate far-side scene introduces a hand and familiar pinwheel through the actual opening. |
| String spinner | The family’s fixed-length loop solver advances the dark cord by one lap, with three driven-wheel and eight motor turns. Pale surface bands and the red joiner travel with the cord; the open wooden fork stays fixed. |

The projector has an explicit cinematic exception to the ordinary alpha-union
crop. Its native image plane is 1.4 m from the box origin. A continuous camera
excursion reveals that separate surface, then returns to a tightly cropped
equivalent of the original finished camera. It uses one fixed raster canvas;
the poster does not reserve the world-space distance to the screen. Toy and
screen intentionally cross the viewport during this move. The camera visits
the rear face of a separate translucent diffuser; the light polygons represent
the transmitted image at the calculated image plane. Projected polygons
represent light and may change shape; they are not extra components attached
to the projector. The rover's line likewise belongs to a use surface.

These are prescribed working demonstrations over dimensioned geometry. They
do not simulate force, friction, wind, restitution, spring stress, air pressure,
motor torque, electrical performance or actual optical brightness. The marble
rally is not a measured trajectory. The drum's rotation shows its slit/picture
construction; it does not claim a 15 fps video reproduces the full perceptual
effect of looking through a physical zoetrope.

## Render and export

Use at most two full Blender render processes at a time; each process fixes its
CPU thread count at two. The batch runner renders its selected families sequentially.
Create an ignored Pillow environment first:

```sh
python3 -m venv runs/builder-next/venv
runs/builder-next/venv/bin/pip install Pillow==13.0.0
runs/builder-next/venv/bin/python projects/builder-study/animation/batch.py \
  --families pinwheel,racer,pinball,dragon,gantry,carousel,claw,drum,rover,projector,carrier,window,spinner \
  --output runs/builder-next/animation/final
```

The default render is transparent Cycles/Standard at 640 square, eight samples
plus denoising, with a separate 1600 square/24-sample frame-zero poster. The
carousel, spinner and whale use 24/48 samples for their clear guards. Export
uses one alpha-union crop for the whole loop, four raster pixels per CSS pixel
for the poster, and a smaller registered animation raster. Spinner exports at
560 px/quality 80 after a display-size encoding comparison; the other loops
use 640 px/quality 82. The static poster
therefore remains the source of display dimensions and the reduced-motion
alternative. The pinwheel keeps its accepted 400 px longest dimension; other
completed toys use their family’s 340–350 px scale. A smaller animated raster
does not change its authored display size.

The WebP duration sequence alternates 66/67 ms to total exactly 6.4 or 8 seconds.
It repeats infinitely. The exporter rejects empty frames, ordinary motion
touching the source canvas, incomplete sequences and source changes during the
render. `--allow-changed-sources` exists only for explicitly disposable previews
and preserves the warning in their manifest. Production renders require frozen
sources; a preview override is not production approval.

Each source manifest records imported source SHA-256 hashes, camera, samples,
render dimensions and the declared evidence limit. Export adds common crop,
poster/animation dimensions, duration, encoding quality and output hashes. Keep
the selected manifests with the production source record; do not retain raw
frames, probe sheets or render logs as permanent evidence. Runtime promotion is
separate from this renderer and writes only reviewed outputs beside the story.

The selected [toy source record](source-record.json) binds all thirteen loops and
their posters to frozen inputs and output hashes. The [ending source record](ending-source-record.json)
binds the separate 390×844, 150-frame, ten-second exchange to its 780×1688 settled
poster. That scene plays once and holds its last frame. Its canonical scene lives
in `../full-story/ending_scene.py`; shared far-side hands and pinwheel geometry live
in `../full-story/future_scene.py`. Passage checks include the whole loaded machine,
Window fittings and fasteners, hands and both work surfaces.

## Verification

`check.py` samples 97 poses, requires actual visible geometry to move and rejects
rigid mesh deformation. It specifically checks paper movement relative to the
toy root and a stationary handle for both the original and carried pinwheel,
so whole-carrier travel cannot conceal a stationary rotor. It creates temporary quarter-cycle
views for informed inspection; these are not source-unexposed recognition tests.
Use `--no-renders` for a lightweight geometry pass while the main render slot is
busy. The declared flexible spinner sleeve and projected light polygons are
excluded from rigid-mesh invariance checks.

`contacts.py` checks the finite-radius pinball against the actual evaluated
surfaces and verifies gantry cord length/hook continuity. `verify_gantry.py`
checks the complete pawl/ratchet profiles; `verify_rover.py` checks ground-contact
velocities for both driven wheels and the free ball caster. Its centered finite
difference avoids amplifying Blender's single-precision transform rounding.
`verify_exports.py` decodes the WebPs to check timing, canvas registration and
alpha margins, and reports seam differences for informed inspection.

Inspect the decoded WebP at playing size, including the seam, transparency,
moving-part attachment and any temporary clipping. The selected-source record
owns output provenance; record concise verification outcomes here without
retaining temporary captures or detailed reports.
