# Settlement production artwork

Selected production artwork for the harvest-festival, studio and encyclopedia revision. The [story brief](../../../stories/settlement/design-brief.md) owns visual intent. All new illustration was made with the built-in imagegen tool; the runtime files live under `stories/settlement/assets/`. No API/CLI image-generation fallback was used.

- [Backgrounds](backgrounds/README.md): six new scenes, exact prompts, references, selected masters and reproducible 22% cream export. The studio serves two chapters.
- [Object requests](seasonal-icons/requests.json): thirteen selected object illustrations, including corrected vessel, press and washstand states. Original icons are preserved.
- [Workshop requests](seasonal-icons/workshop-requests.json) and [registration](seasonal-icons/workshop-export.json): unfuelled forge, open stove, fitted pot and standalone iron pot. The Plant enlargement was rejected; the manuscript again uses the original 224×224 art.
- [Printed-page orientation](presentation-requests.json): the selected upright sheet edit, exact prompt and reference inputs; its runtime is `printed-pages-v3.png`, also used by the art fitting in the encyclopedia.
- [Binding requests](binding-requests.json): two final illustrations and the necessary reference generation. The unfinished state is two separate lined boards; the final volume is visibly sewn. The earlier connected-board reference is retained because it was an input to both selected generations, not as runtime art.
- [Night and final-room refinements](night-and-record/): selected masters, exact prompts and exports for the filled pond bowl, night-lit coast, printed encyclopedia, reframed final room and pot above the stove. The noninteractive final room retains full-strength colour; the playable coast receives 22% cream once.
- [Binding export](export-binding.py): reproducible sizing and transparent padding of the seven existing loose records into two shallow fans. The 640×426 base and overlays have a 160×106.5 display footprint. Records fit in any order; overlay stacking remains fixed so the assembled appearance does not depend on action order. No miniature subject bundles are created during earlier chapters.

Generation prompts are preserved verbatim in their request files. Selected full-resolution masters are retained here, without duplicate copies of runtime exports. Review sheets, browser captures, rejected generations and test inputs are temporary verification material and are removed after concise findings are recorded in [outcomes](../outcomes.md).
