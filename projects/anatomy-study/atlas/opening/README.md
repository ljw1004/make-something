# Opening atlas artwork

Production sources and mechanically derived cutouts for chapters 1–3 and 5–8. The [production contract](../production-brief.md) governs these assets; the [story brief](../../../../stories/anatomy/design-brief.md) owns the visual intent. Exact generation requests accompany their selected masters in `sources/`.

The nuclear envelope study preserves two porous double-wall cutaways. The frontal shell is selected because its cavity leaves the tangled DNA clearly visible.

The repaired eye uses one continuous whole-organ master. Front states and loose optical/retinal parts are mechanically selected from that same image; the final result does not acquire a detached magnification. The source plate remains a necessary generation reference. Registered cell and neuron layers retain their base canvas dimensions; the whole cell is deliberately larger than loose molecule samples.

Rebuild with `uv run --with pillow --with numpy --with scipy python projects/anatomy-study/atlas/opening/build.py`. The script writes only runtime exports, the map and a disposable informed-inspection montage under `runs/anatomy-atlas/`.
