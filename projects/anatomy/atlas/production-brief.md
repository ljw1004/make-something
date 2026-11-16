# Anatomy — selected 1800s atlas production

Governed by [the single design brief](../design-brief.md) and [icon guide](../../../docs/icon-guide.md). This is the selected full-book direction, replacing the comparative selection phase.

Use fine naturalistic engraving, believable anatomical contours, restrained rose/madder/sage/ochre washes and warm ivory paper, matching `../art-study/classic-1800/` and supplied `../inspiration/classic2.jpeg`, `classic3.jpeg`. Inspect those images. Preserve modern explanatory scale and the successful large specimen views. No glossy cartoons, faceted geometry or holographic glow.

## Physical objects, never explanatory badges

Every movable, fixed or fitted image shows what that thing physically IS in its current state. Do not include former reagents, future products, target substrates, organ locators, arrows, labels, captions, surrounding mini diagrams or purpose symbols. Enzymes are enzyme molecules alone; bile is actual bile liquid; small fat droplets are droplets alone. A combined result includes a reagent only if it physically remains inside/attached to it. No detached zoom circles, magnifying windows or repeated anatomical parts in any result. If a small part was visible while supplied, it may become naturally small within the finished construction. Cutaways through one continuous specimen are welcome.

Use the same physical geometry within an assembly family. Compose from same masters/constituents so additions are recognizable. Material supply samples may stand for sufficient quantity, but cannot advertise what they will form. Blank backgrounds only; all anatomy belongs to runtime objects.

Apply the icon guide's [synecdoche allowance and composition review](../../../docs/icon-guide.md#review-the-construction-not-just-the-cutouts). A single representative can become numerous instances where growth or organization makes that useful. Exact pixel reuse does not compensate for an unnatural whole; redraw a coherent specimen and its physically meaningful parts when necessary. The current independent review loop and selected replacements live in [composition-review](composition-review/README.md).

## Deliverable contract

Packages live in `atlas/PACKAGE/`, with selected builtin-generated source masters and exact requests in `sources/`, runtime transparent PNGs in `assets/`, reproducible mechanical extraction/composition script and concise README. Temporary diagnostic sheets stay in ignored `runs/anatomy-atlas/`. Do not edit canonical manuscript or other packages. Do not reuse inappropriate prior atlas icons just to fill inventory.

Each package emits `map.json`: `itemIcons` mapping parser identity (id:... or name:...) to paths relative to projects/anatomy/anatomy.md (atlas/PACKAGE/assets/...), `slotIcons` mapping compound owner identity to {accepted identity:path}, `hotspots` mapping original chapter number string to {identity:{center:[x,y], icon?:path, hitbox?:{center:[x,y],size:[w,h]}}}, optional `placements` mapping identity to [x,y] initial image centers, optional `presentations` mapping identity to [{chapter:chapter-id,path:path}] for later scale. Use original source parser keys, not invented aliases. Root integrates.

Default page is a plain ivory 1560×2340 canvas. Typical main specimens should occupy roughly 700–1300 source pixels (175–325 CSS pixels); small loose physical pieces typically 160–480 source pixels. Follow natural relative scale within each assembly; never square-normalize everything. Keep ordinary supplies clear of receivers and goal area. For fixed models center about [780,1050], with enough space for reagents below. Overlay PNGs must exactly match their base canvas. Fixed states retain shared registration. Movable states should crop to present anatomy without rescaling their parts.

Use builtin imagegen for all new painting; mechanical cropping, alpha cleanup, registration and compositing of generated parts are allowed. Generate related physical families from common specimens. Inspect all outputs and registered partials. Distinguish batch coverage from fresh recognition testing. Full progression and final image loading will be checked centrally.
