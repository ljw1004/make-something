# One bearing tube at a time

The chapter-two prototype supplies two separate draggable **Bearing tube**
identities. Both reuse the existing connected tube-and-saddles inspection icon.
Either may be fitted first. The positive-X station is the front of the canonical
racer, which travels in positive X; the negative-X station is the rear.

`racer_stages.py` selects one complete 13-mesh bearing unit from the unchanged
canonical `build_racer()` assembly. It adds no parts, moves no vertices and keeps
the original chassis. `verify.py` compares evaluated mesh hashes: both partials
retain the chassis exactly, their added units are disjoint, and their union is
the original two-bearing assembly. These subset checks do not repeat or extend
the original mechanism's physical validation.

The original registered camera and lights are retained. `registration.json`
records the original 960px canvas, crop and uniform scale. The crop was recovered
from the exact five baseline c02 hotspot images at Git revision
`780af8557be813cc83e516e8c243974a0a956df2`, using the previous readability
exporter's alpha threshold, six-pixel padding and 248px family limit. Applying
it reproduced every pixel of all five current live hotspot images before the
new states were introduced. Existing production images are not regenerated.

```sh
python3 -m venv runs/builder-chapter-one/venv
runs/builder-chapter-one/venv/bin/pip install Pillow==13.0.0
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup \
  --python projects/builder-study/racer-art/render.py -- \
  --output runs/builder-chapter-one/racer/masters
runs/builder-chapter-one/venv/bin/python projects/builder-study/racer-art/export.py \
  --masters runs/builder-chapter-one/racer/masters \
  --output runs/builder-chapter-one/export/hotspots
```

The renderer also makes bare-chassis and complete-bearing proofs for comparison
with the baseline. Those proofs, render manifests and contact sheets remain
scratch. Only the selected new WebPs and these authoring sources are retained.

Selected runtime artwork lives in `stories/builder/assets/`. Review scratch exports before replacing those files; the older study manuscripts preserve their historical source paths.
