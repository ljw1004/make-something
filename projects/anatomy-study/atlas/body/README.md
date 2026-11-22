# Later anatomy: selected 1800s atlas artwork

Physical specimen artwork for the original chapters 19–28, governed by the [production brief](../production-brief.md) and [story design brief](../../../../contrib/anatomy/design-brief.md).

`map.json` supplies 91 identities and 16 registered fitted layers. It includes the final head sensory fittings and a common chest registration that accommodates the later arm and lymph fittings. The final body mechanically reuses the built intestinal, urinary, chest, arm and nervous structures. Its skin covering was generated against that actual assembled pose, then opened as a continuous cutaway. No anatomical content lives in a background.

All painted source specimens were generated with the builtin image-generation tool. `sources/*.request.txt` retain the exact requests beside the selected PNG masters. The supplied `classic2.jpeg` and `classic3.jpeg` references were visually inspected; no earlier comparative artwork was transferred. The matched wound plate was used as a shape and placement reference; runtime wound stages preserve the actual construction pixels instead of replacing the whole section.

Rebuild after the opening, circulation and arm-food packages exist:

```sh
uv run --with pillow --with numpy --with scipy python projects/anatomy-study/atlas/body/produce.py
```

`produce.py` extracts and cleans transparent source crops, registers physical layers and emits the map. `finale.py` supplies the shared-package regional composition. Mechanical operations are cropping, resizing, mirroring, alpha cleanup, masking existing pixels and compositing. No anatomical drawing is synthesized in Python.

`description-replacements.json` records the exact-source physical-description corrections sent to the central story integrator. `inventory.json` records the original chapter identities used for this package assignment. They are production inputs, not separate story specifications.

All identities and every registered partial assembly were inspected over ivory. Temporary inspection sheets are written to ignored `runs/anatomy-atlas/`. Independent informed visual review and full browser progression are performed centrally; source coverage alone is not a claim that those checks passed.
