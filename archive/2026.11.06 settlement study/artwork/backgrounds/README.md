# Settlement background artwork

Selected production artwork for the 9 November 2026 festival, studio and science revision. All six images were produced with the built-in `image_gen` tool. Four remain in use; the final room is now the closer, richer `settlement-record-v4.webp` in [night-and-record](../night-and-record/), and the user preferred the original wall-hearth kitchen (`25.webp`) for chapter 13, with the hearth remaining scenery rather than a hotspot. The generated cooking room is retained as an unused alternate. Each `.prompt.txt` is the exact submitted prompt; each `.master.png` is the selected untreated output. The original generated cache files were left in place.

| Output in `stories/settlement/assets/backgrounds/` | Reference input | Intended scene |
|---|---|---|
| `art-studio.webp` | `stories/settlement/assets/backgrounds/25.webp` | Late-autumn daylight studio, shared by the arts and mechanical-work chapters. |
| `binding-studio.webp` | `art-studio.master.png` in this folder | The same studio from the opposite side, with a clear workbench and bowl oil lamp; dark outside. |
| `weather-beach.webp` | `stories/settlement/assets/backgrounds/22.webp` | Existing beach geography at late-autumn twilight, before the night-sky chapter. |
| `cooking-room.webp` | `stories/settlement/assets/backgrounds/25.webp` | Unused alternate with the wall hearth removed; chapter 13 uses the original `25.webp` by user preference. |
| `waterworks.webp` | `stories/settlement/assets/backgrounds/14.webp` | Shared riverside courtyard before installation of washing and drinking-water equipment. |
| `settlement-record.webp` | `art-studio.master.png` in this folder | Superseded composition, retained as the reference input for `settlement-record-v4.webp`; modest cottage room with the completed record. |

The selected masters are 853×1844. Run `node 'archive/2026.11.06 settlement study/artwork/backgrounds/export.mjs'` from the repository root to reproduce the 780×1688 WebP runtime images. Export applies the design brief's 22% warm cream (`#fffaf0`) once, directly to the untreated master, and makes no additional colour adjustment. The negligible aspect-ratio adjustment preserves the established scene coordinate frame. Reuse the single studio runtime image rather than keeping an identical mechanical-workshop copy.

The images were inspected at full size and together at their intended portrait framing. The rooms retain the game's irregular carved marks, timber/plaster construction and generous uncluttered play area. The studio views retain the brush jars, substantial workbench, window and empty frame; the binding view changes position and lighting. The cooking room no longer paints an active hearth, and the water courtyard does not pre-build the player's facilities. The beach retains its coast and distant lighthouse while changing to dusk; the revised astronomy background in [night-and-record](../night-and-record/) supplies the following night. The ending shows an ordinary handmade volume in a small settlement room.

In `binding-studio.webp`, `(330px, 465px)` is a clear working point on the actual tabletop, to the right of the lamp. Use a transparent registered receiver rather than drawing a second table over it. Existing early backgrounds depict warm growing-season daylight and ripe fruit, so this revision does not claim that they establish a literal spring-to-autumn calendar. Existing festival backgrounds already progress from an undecorated square to canopy and bandstand and were retained.

All six first candidates were selected after inspection; no rejected production variants are retained. Temporary contact sheets and geometry checks belong in ignored `runs/` and are disposable.
