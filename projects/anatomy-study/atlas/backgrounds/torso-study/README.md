# Anatomy frontispiece composition study

The brief was a single anatomical figure that fades near the diaphragm so the carousel bar and subtitle have space. The upright upper figure of the 1651 *Leviathan* supplied a compositional reference. [Pitts Theology Library scan](https://digital.pitts.emory.edu/s/digital-collections/item/14393)

The [whole-figure follow-up](whole-figure/README.md) extends the selected centered cutaway idea into a wide crop of one continuous figure. It includes the full unfaded master, current export and independent follow-up judgments.

An independent Terra reviewer inspected the real carousel with the full subtitle, title bar, dots, Continue label and footer. The comparison included phone, short phone and desktop layouts. The phone render with enlarged type approximated the supplied screenshot.

| Candidate | Harmony | Reviewer’s judgment |
|---|---:|---|
| [Three-quarter cutaway](three-quarter-cutaway.webp) | 2.5/5 | The engraving is attractive, but the tight crop cuts into the head and shoulders. The diaphragm meets the bar while still prominent, and the dots sit over busy detail. |
| [Frontal muscle study](frontal-muscle-study.webp) | 3/5 | The face makes the figure feel human. The broad chest fills the upper card so the bar meets it abruptly, and the blank lower field feels separate. |
| [Centered cutaway](centered-cutaway.webp) | 4/5 | The centered anatomy and smooth fade leave the title, subtitle and footer clear. The faint legs give continuity. The reviewer found the chin crop abrupt. |
| [Complete anatomical figure](complete-figure.webp) | 4.5/5 | The complete head unifies the figure, and the restrained return of the legs balances the page. The subtitle and footer remain clear. The dots cross the lower ribs on a short phone, where the bar meets some visible anatomy and the controls stay legible. |

The user chose the centered cutaway after seeing both renders. They found that the face drew attention away from the anatomy. The review scores record one independent visual judgment.

## Artwork and export

Built-in ImageGen produced the [three-quarter master](three-quarter-cutaway.png), [frontal muscle master](frontal-muscle-study.png), [centered cutaway master](centered-cutaway.png) and [complete figure master](anatomical-figure.png). The inputs included the [earlier thorax](earlier-thorax.png), [matte paper](../chapter-paper.png), [supplied shoulder plate](../../../inspiration/classic3.jpeg) and [scaled Leviathan scan](leviathan-reference.jpg). The complete figure used the centered cutaway and frontal muscle masters as references.

The WebP files use a horizontal crop to the 780 × 1688 cover dimensions. The three first-round masters have a 1610-pixel source height. The complete figure master has a 1609-pixel source height. Export the first centered cutaway from this directory.

```sh
cwebp -quiet -q 87 -m 6 -crop 116 0 744 1610 -resize 780 1688 centered-cutaway.png -o centered-cutaway.webp
```

## Generation requests

### Three-quarter cutaway

```text
Use case: illustration-story
Asset: a quiet portrait frontispiece for a classic illustrated atlas of human anatomy.
Image 1 is a style and subject reference for its earlier thorax, with fine colour engraving and heart between the lungs. Image 2 supplies the new light, neutral paper tone. Draw a new composition.
A single large, connected classical anatomical bust emerges from the top of this page. From the visible lower jaw and full neck at the top, the shoulders and upper chest fill the upper third. Use a gentle three-quarter view like the reference, placing the heart visually near center and the shoulder and neck muscles around it, with readable lung contours, curved rib edges and delicate hints of blue veins. Preserve the gravity and elegance of a 19th-century plate, reframed to be a book cover. Moderate desaturated madder, bone ivory and slate. Make a wide, quiet silhouette at the shoulders and one coherent body mass, not a cluster of organs.
The diaphragm lies at about 41% page height. From 29% down, let the ink itself thin progressively into broken dry hatching and then vanish into the page. Finish this soft, irregular fade fully by 43%. The anatomy never has a hard lower cut edge. Below that the paper is quiet and empty to the bottom. This is the background art behind a real portrait mobile game catalogue card. Final aspect is 780:1688. The art will be center-cropped horizontally to that narrow portrait ratio if needed, so compose anatomy inside the central 70% of your source width. The game's title bar spans the image at 47% height; dots sit just above it and a black, multi-line description sits directly below. Do not draw any of those interface elements. Through 42–77% height the paper must read as a single quiet nearly white field, with no dark lines behind the words. The footer links occupy the bottom; give them clean paper. An unprinted, very pale matte ivory paper with fine soft grain extends edge to edge. No typography, captions, rules, frame, inset specimens, detached limbs, pools of blood, surgery, theatrical injury, glow, or page edges.
```

### Frontal muscle study

```text
Use case: illustration-story
Asset: a portrait anatomy game frontispiece in antique copperplate style.
Image 1, the 1651 Leviathan frontispiece, is a reference ONLY for its axial balance, the calm upright figure rising in the upper register and the transition into the title field below. Image 2 supplies the historical anatomy illustration technique. Image 3 supplies pale neutral ivory paper.
Make a single centered, front-facing adult anatomical figure, noble and composed like a classical print. A calm human face is visible near the top, from upper brow to chin, with the strongest established lines in the neck and shoulders just below. The upper chest is a sober atlas study of the collarbones and superficial pectoral and shoulder muscles, with broad open planes, a little restrained madder, and finely engraved warm charcoal lines. Give the figure believable head and shoulder proportions and quiet dignity. No crown, landscape, heraldry or props. Set the subject in the upper 40 percent, with shoulder width commanding the field but ample breathing room at either side. Below the ribs, the engraved marks progressively become sparse and faint in an organic dissolve into the warm-white paper. The implied diaphragm is near 44% height, where the anatomy vanishes; the midriff and lower page resolve entirely into lightly textured paper. A harmonious old book syntax, feels like one picture. No split anatomical halves. This is the background art behind a real portrait mobile game catalogue card. Final aspect is 780:1688. The art will be center-cropped horizontally to that narrow portrait ratio if needed, so compose anatomy inside the central 70% of your source width. The game's title bar spans the image at 47% height; dots sit just above it and a black, multi-line description sits directly below. Do not draw any of those interface elements. Through 42–77% height the paper must read as a single quiet nearly white field, with no dark lines behind the words. The footer links occupy the bottom; give them clean paper. An unprinted, very pale matte ivory paper with fine soft grain extends edge to edge. No typography, captions, rules, frame, inset specimens, detached limbs, pools of blood, surgery, theatrical injury, glow, or page edges.
```

### Centered cutaway

```text
Use case: illustration-story
Asset: a portrait historical anatomical game frontispiece with a suggestion of the whole body.
Image 1 references the earlier engraved neck and thorax, Image 2 references the broad upper figure on a book frontispiece, Image 3 supplies the matte paper.
One front-facing anatomical figure on one axis, neck and shoulders at the top. The lower jaw may be just visible at the top, and the upper thorax offers a clean, restrained engraving of collarbones, ribs and the heart between muted lungs. Use the naturalistic 19th-century pen and subdued rose-gray wash of an anatomy atlas. The dome of the diaphragm tapers into open paper at about 40% page height. Fade the image with soft thinning strokes along its own contour, from the upper abdominal plane into the sheet. The center where title and body text sit is pale paper; along the outer contour only, each hip is merely implied by exceptionally faint broken graphite lines. As a very subtle low watermark between 78 and 89% page height, let that same figure continue into two light, sketchy suggestions of the lower legs, centered on the same axis and at continuous body scale. They are an echo, with almost no tonal weight, as though the figure emerges and recedes through the ink; do not make a new sharply defined specimen or panel. Fade these lines again before the footer. If any central contour remains, make it the faintest warm-paper-colored phantom. This is the background art behind a real portrait mobile game catalogue card. Final aspect is 780:1688. The art will be center-cropped horizontally to that narrow portrait ratio if needed, so compose anatomy inside the central 70% of your source width. The game's title bar spans the image at 47% height; dots sit just above it and a black, multi-line description sits directly below. Do not draw any of those interface elements. Through 42–77% height the paper must read as a single quiet nearly white field, with no dark lines behind the words. The footer links occupy the bottom; give them clean paper. An unprinted, very pale matte ivory paper with fine soft grain extends edge to edge. No typography, captions, rules, frame, inset specimens, detached limbs, pools of blood, surgery, theatrical injury, glow, or page edges.
```

### Complete anatomical figure

```text
Use case: precise-object-edit
Asset: anatomy atlas frontispiece for a portrait game catalogue. Image 1 is the edit target. Image 2 is a reference only for the dignity of a complete face and traditional engraved treatment.
Correct the top crop in Image 1 by completing the SAME centered anatomical figure with a complete calmly posed human head above the neck. Show the entire head and a small amount of ivory paper above the hair. Give the face and hair subtle warm graphite shading, calmer and lighter than the thorax, with a natural neutral gaze. Keep the anatomical neck, shoulder muscles, ribs, heart and lungs recognizably the same beautiful coordinated plate as in Image 1. This is one embodied atlas figure. Head roughly one third of the shoulder breadth or a little less, accurately human.
Re-compose the upper engraving a little smaller to accommodate the full head while preserving the lower part of the page. In the 977 x 1610 source canvas, center the figure horizontally. Have the top of the head at about y=35, chin near y=205, clavicles around y=285, the diaphragm around y=550, and all distinct anatomy gone by y=675. Keep roughly 610px of shoulder width, with the quiet silhouette comfortably inside the center 72% of the page. Let fine hatch marks and thin muted rose ink recede unevenly into matte paper from the rib edges downward, mostly gone by 41% height. The design must feel like it fades into the space where a real title bar sits at 47% height. Keep the whole text area completely pale, the very faint existing suggestion of legs in Image 1, and the light neutral paper throughout. No additional elements, no new strong marks in the lower half, no labels, panels, titles, decorations, or hard horizontal fade boundary. Match the nineteenth-century engraving and moderate contrast of Image 1, with the whole head at its modest proportion, no dramatic pose.
```
