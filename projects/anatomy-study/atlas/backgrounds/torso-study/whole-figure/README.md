# Anatomy whole-figure frontispiece

The user chose the centered neck-and-shoulders crop and asked for a more visible, better proportioned suggestion of the legs. The [unfaded master](unfaded.png) shows the entire continuous anatomical figure from chin to feet, using the [game’s finished body artwork](../../../../../../contrib/anatomy/assets/composition-review/finale/assets/body-beneath-the-skin.png) for the pose and limb proportions. The export crops that standing figure with a consistent scale so the shoulders fill most of the width. The knees and upper calves are visible below the description. The crop ends above the feet.

The built-in ImageGen tool made the [unfaded master](unfaded.png), [first wide-cover fade](first-fade.png) and [final faded master](faded.png). The first fade used the [centered cutaway](../centered-cutaway.png) for its paper and tonal transition. The last pass fades the abdomen earlier and softens the lower echo near the footer.

An independent Terra reviewer examined the unfaded figure and two faded exports as real carousel cards with the title, full subtitle, dots, Continue label and footer. The reviewer found the whole figure convincingly tall and athletic, with substantial thighs and calves and plausible alignment through the knees and ankles. The torso was somewhat elongated and stylized. The first wide-cover fade scored 4/5 for harmony. The revised fade scored 4.5/5, with a quieter transition by the dots and a legible footer. Only the faint tops of the knees appear on a short phone.

Export the [live cover](../../../../../../contrib/anatomy/assets/cover.webp) from this directory.

```sh
cwebp -quiet -q 87 -m 6 -crop 231 0 530 1147 -resize 780 1688 faded.png -o ../../../../../../contrib/anatomy/assets/cover.webp
```

## Generation requests

### Full figure

```text
Use case: scientific-educational
Asset: the full-strength art master for a nineteenth-century anatomy atlas game frontispiece.
Image 1 is the chosen cover. Keep its style, pale matte ivory paper, classic neutral colors and connected frontal rendering of the neck, shoulders, ribs, lungs, heart and diaphragm. Image 2 is a visual reference for the proportions and physical continuity of the same game's full adult body, especially its pelvis, thighs, knees, calves and feet. Its vivid contrast and head treatment are not the style or intended crop.
Draw one continuous, conventionally proportioned adult human figure in a relaxed frontal anatomical stance, from the underside of the chin at the very top edge clear down to both feet. The chin crop is intentional. Exclude facial features. Show the same recognizable thoracic cutaway as Image 1, with an unbroken continuation through the abdomen and muscular pelvis into both legs. Two naturally proportioned thigh muscles start from a broad enough pelvis, kneecaps meet them at realistic positions, calves have their real muscle volume, and ankles narrow gradually into real, grounded, fully visible feet. Both legs point down from the corresponding hip joints with a natural modest stance. Keep enough arm, hip and forearm continuity to show this is one real figure. Hands can hang relaxed to either side of the thighs, with no items or props. The midline pelvis can be treated as a conventional schematic section of bone and muscle, with no exterior genital depiction.
Keep the body narrower than the upper-only cover so the full human proportions fit. Center the figure within the middle 67% of the source width so it can be brought to 780:1688 by trimming sides. On a tall 977 by 1610 source sheet, the lower jaw enters at y=0, the diaphragm arcs near y=435, both hip joint centers are around y=715, kneecaps around y=1080, and the ankles and feet finish around y=1490 to 1520. These are composition guides for coherent adult proportions. Do not hide small or misplaced legs in a fade. The complete anatomy from upper thorax through midsection and legs should be rendered clearly and at the same atlas scale in this first source, with delicate fine etched hatching and restrained madder, warm ivory, and slate on softly textured paper. Keep everything part of the one whole body.
This is the unfaded inspection master. Keep all regions equally legible across the whole figure, including the middle and lower legs. No captions, arrows, labels, numbers, panels, vignette, title, background objects, borders, or interface.
```

### Faded print

```text
Use case: precise-object-edit
Asset: a density-adjusted print of the exact existing tall anatomy engraving.
Image 1 is the sole edit target, a complete 1000 x 1573 atlas figure. Image 2 is only a tonal reference for the quiet ivory transition, not a shape reference. Make a layer-opacity change only. Do not redraw, reposition, resize or reshape any part of Image 1. The chin, shoulder width, ribs, diaphragm, pelvis, knees, calves, ankles and feet must all stay in the exact same places. Keep the paper texture, color, and full image dimensions.
The upper thorax from the top to y=315 remains at full ink. Treat the engraving below this as a line drawing whose ink opacity can be varied by height. Between y=315 and y=560 taper all anatomical lines into the paper very smoothly, with the ribs and diaphragm visible and strong near the beginning of the fade. Around y=500 no distinct abdominal organs should remain. From y=560 to y=855 make essentially clean ivory paper all the way across, without readable anatomy or arms. This broad middle will be a text area after cropping.
Starting at y=865 allow the lower portions of the same upper legs to return slowly. From y=970 onwards let the knees and calves look like a soft but clearly readable faded antique impression, roughly 20% of the density of the original drawing. Preserve all the body geometry from Image 1 exactly, including the wider thighs, full kneecaps and upper calf contours. Fade the edges very lightly so this one continuous figure seems to emerge from the same sheet. The lower body will be cut off partway through the calves in the eventual cover, but keep the whole image including the feet here as the full faded master. It is important that the returned anatomy begins high enough to be visible between y=900 and y=1147. The notes, title and interface will be added separately. Add no lettering, ornaments, borders, new drawings, blurred shapes, filters over the paper, or horizontal seams.
```

### Earlier fade and softer knees

```text
Use case: precise-object-edit
Asset: the finished ink-density adjustment on an existing 1000 x 1573 full-height anatomy plate. The first reference is the edit target. The second reference is useful only for the delicacy of the fade into clean ivory. Make only two changes in ink opacity below the upper chest. Do not change any drawing, size, position, contours, proportions, anatomy, height, width, upper color treatment, or the Cropped chin. The same full figure must remain registered exactly.
First, accelerate and soften the upper fade. The heart, lungs, shoulders and neck from y=0 to y=330 stay as engraved. Let the diaphragm remain visible, then let the supplied engraved lines thin and fade into the pale paper almost completely across y=345–470. In the final image the liver, stomach, and intestinal shapes must be only extremely faint, almost invisible, and all below y=480 should be plain ivory. Current visible detail in the abdomen and arms around y=435–550 should disappear into a natural gradient of faint strokes, like the quieter second reference. Leave the paper especially clear from y=470–850 all the way across. No hard horizontal blur or boundary.
Second, lower the opacity of the knees and upper calf strokes by approximately one third relative to reference Image 1, keeping the leg widths and shapes. Begin their extremely soft, slow return slightly earlier, around y=850, with only a feather-light implication of the lower thighs at first; substantial silhouettes are still faint, not comparable to the upper body. At y=980–1045 keep the kneecaps readable as antique ghost ink, clearly more tangible than the tiny leg traces in Image 2. Then let the calves be a little lighter again from y=1050 to y=1160 so black footer links can sit over them unaided. Keep the quieter lower legs and feet on the inspection master, although the cover export will crop below y=1147.
The design stays one continuous figure emerging from the very same matte paper, with most ink in the upper chest. Preserve the full canvas and exact feature registration. Do not print interface text, dashes, labels, frames, guides, or separators.
```
