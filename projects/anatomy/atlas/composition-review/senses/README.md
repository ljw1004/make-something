# Sensory-organ replacement family

Replacement artwork for Anatomy chapters 7–9, prepared under the active [design brief](../../../design-brief.md). The package does not modify the canonical manuscript. The root integration pass owns adoption and fresh independent review.

`map.json` maps the existing item identities to 26 transparent PNGs. No slots or recipes change. The completed eye uses original identity `name:Eye with optic nerve`; integration reverses the temporary art alias. Paths are relative to `projects/anatomy/anatomy.md`.

## Production

Run `uv run --with pillow python projects/anatomy/atlas/composition-review/senses/produce.py` from the repository root. The script retains all source-pixel extraction masks, crop bounds and scale factors. Anatomical master exports use 0.68 source-pixel scale and a six-pixel transparent margin. Isolated eye parts from the matched sheet use the recorded scale corrections to match the master. The three turning patches and two tilt patches are packed more closely as loose material while preserving their source dimensions and orientations. Finished assemblies remain single paintings rather than mosaics of separate generations.

The eight image-generation requests are preserved verbatim in `prompts.json`; all used the built-in image generator. `ear`, `eye` and `balanceV2` are original generation requests. `eyeParts` references `eye-master.png`; `earEmpty` references `ear-master.png`; `earWindow` references `ear-empty.png` first and `ear-master.png` second. Both `balanceV2Empty` and `balanceV2Unweighted` reference `balance-v2-master.png`. These filenames resolve within `sources/`.

Their selected outputs are:

- `eye-master.png`: oblique continuous eyeball with a real iris annulus, broad retinal cup and attached optic nerve.
- `eye-parts.png`: matched cornea, iris, lens and two broad tissue cups. Their broad surfaces resolve the previous narrow-strip-to-full-cup discontinuity.
- `ear-master.png`: continuous pinna, canal, eardrum, ossicle chain and cochlear dissection with surrounding support.
- `ear-empty.png`: matching receiving tissues without drum, ossicles or sensory epithelium.
- `ear-window.png`: matching empty anatomy with the oval-window boundary made explicit; only its small local window region is used.
- `balance-v2-master.png`: three ampullae with contained cupulae and two separately oriented macular patches inside utricle and saccule.
- `balance-v2-empty.png`: matching chambers with sensory patches omitted.
- `balance-v2-unweighted.png`: matching sensory patches with the mineral granules omitted.
- `mineral-sample.png`: retained prior material sample from `atlas/circulation/assets/tiny-mineral-weights.png`. It represents the mineral substance; individual sample grains are illustratively enlarged, not a count-matched installation diagram.

The hearing-cell input is a representative short physical epithelial strip extracted from its installed spiral ribbon. Synecdoche can represent the rest of the sensory population; it is not a detached enlarged diagram included in the resulting ear. The eardrum and ossicle chain are extracted at their installed dimensions. Cochlear preparations include a visible oval-window receiving boundary; the final ear seats the stapes footplate there.

## Review and integration handoff

The producer inspected all 26 exports on the blank atlas ground and all native construction strips at common playing scale. This is informed self-inspection, not independent acceptance or student evidence. Fresh root-managed reviews accepted eye and ear in round 1 and balance revision 2 in round 2. Temporary sheets and operation packets belong in `runs/anatomy-composition-review/senses/` and are disposable.

The completed eye, ear and balance masters remain available as regional anatomy references. The finale repaints those anatomical relationships within its own body-scale master; this package does not claim that its standalone organ pixels are installed in the final body. Integration applies the original-eye identity through its alias table. Descriptive updates in `description-replacements.json` keep the artwork and existing physical units consistent; no recipe changes are proposed.

Balance revision 2 replaces the initial planar-looking loops and undersized cupulae. Its oblique master shows overlapping, foreshortened duct planes and broad cupulae spanning each ampulla. The repair follows the [UTHealth vestibular chapter](https://nba.uth.tmc.edu/neuroscience/m/s2/chapter10.html) and [Rabbitt et al. on the chamber-spanning cupula](https://pmc.ncbi.nlm.nih.gov/articles/PMC2774407/). Eye and ear assets accepted in the fresh round-1 review remain unchanged. The fresh round-2 chapter-9 review accepted components, composition, the standalone whole and all three operations.
