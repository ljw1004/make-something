# Anatomy background artwork

The [frontispiece](../../../../stories/anatomy/assets/cover.webp) crops a single tall anatomical figure with broad shoulders, a fading diaphragm and a faint lower-body echo at the same scale. The [composition study](torso-study/README.md) records the alternatives, full unfaded artwork, export and independent Terra reviews. The [shared chapter paper](../../../../stories/anatomy/assets/chapter-paper.webp) is unprinted matte ivory. Both use the same aspect ratio as the Cookbook and Settlement covers.

The built-in ImageGen tool produced the [chapter paper master](chapter-paper.png). The chapter paper retains the 1560-pixel width of the original artwork canvas, so the authored coordinates remain registered at the same scale.

Export the chapter paper from this directory.

```sh
cwebp -quiet -q 87 -m 6 -crop 116 0 744 1610 -resize 1560 3376 chapter-paper.png -o ../../../../stories/anatomy/assets/chapter-paper.webp
```

The [paired arm engravings](paired-arm-plates.png), [spacing pass](paired-arm-layout.png) and [paired arm master](paired-arm-frontispiece.png) record the preceding cover. The [earlier cover](frontispiece.png), [initial paper](ivory-paper.png) and [initial placement](cover-layout.png) record the preceding shoulder-and-hand composition.

## Generation requests

### Matched arm studies

```text
Use case: scientific-educational
Asset: a single calm portrait frontispiece for an interactive anatomy book. This image is the background behind separately rendered catalogue text.
Image 1 supplies the very light warm-ivory paper tone and subtle grain. Images 2 and 3 supply the historical anatomy engraving technique, selective madder wash and believable forms. Create a new composition.
Draw one naturally extended human right arm twice as a pair of comparative anatomical plates. Show the same arm from shoulder through fingertips in both, from the same oblique view, at the same apparent scale, with shoulder at left and relaxed fingers pointing mostly right. The arm stays close to horizontal with a very slight bend at the elbow. In the upper plate show the softly hatched superficial muscles and tendons. In the lower plate show the corresponding bones in precisely the same pose and proportions, with a matching fine etched line weight and a little muted grey-brown wash. Each complete study is a single silhouette with its shoulder, elbow, wrist, and hand connected. The matched studies should immediately read as one deliberate diptych organized around the title area.
Use a tall narrow vertical canvas for crop to 780x1688. Absolute placement requirements: center the upper engraving at x=50%, y=21%. Center the lower engraving at x=50%, y=84%. Make BOTH engravings about 50% of the original canvas width and no more than 12% of its overall height, with identical visual weight. Keep the whole center from 31% through 77% of height nearly plain paper across the full width for multiple lines of game text, and leave the lowest 9% empty for footer links. Make large generous margins, airy drawing, and restrained pigment the defining look. The paper is pale neutral ivory, not amber or yellow.
Treat it like one late nineteenth-century book plate, spare, quietly elegant, light sepia etched contours, fine selectively visible hatching and very faint dusty rose. Full-bleed paper to all edges. No text, numbers, captions, arrows, labels, borders, scenery, ornamental dividers, isolated study fragments, wounds or graphic detail.
```

### Matched study scale and placement

```text
Use case: precise-object-edit
Asset: a tall anatomy poster background with reserved interface areas.
The reference is the edit target. Keep the pale matte ivory paper and both matched antique engravings of the right arm, with the same anatomy, pose, light etched hatching and muted palette. Make only a layout correction. Treat each engraving as a flat printed image and uniformly shrink both to 58% of their present scale. Center the upper one horizontally and vertically at 22% down the poster. Center the lower one horizontally and vertically at 84% down the poster. Keep the taller source canvas and aspect ratio, with the extra space filled by matching original paper. Imagine actually moving and scaling two small pasted illustrations on an otherwise blank sheet.
On a 977 by 1610 reference canvas, the final arm studies must fit strictly inside x=231 to 746, upper art y=260 to 445 and lower art y=1275 to 1440. They should feel like two small whole-arm vignettes floating in an enormous amount of plain paper. The middle and an equally generous footer margin are reserved for user interface copy. No cropping of either arm, no extra illustration marks, no lines, text, headings, borders, glyphs, or graphics added. Preserve the appearance of the two studies and matte texture. Do not fill empty space.
```

### Footer clearance

```text
Use case: precise-object-edit
Asset: anatomy book frontispiece with a clean central title field and footer.
Image 1 is the edit target. Preserve the canvas aspect, paper, all lines, colour, and the exact upper engraving. Keep both the shape and size of the lower engraving. Move only the entire lower bones engraving vertically UP by 87 pixels on the 977 by 1609 canvas. Its new top should be at about y=1127 and its bottom at about y=1265. Its exact horizontal placement stays centered. Blend the paper behind it seamlessly. This is a layout-only correction, as if sliding a printed image up on an archival sheet. It gives the poster more space BELOW the lower engraving for footer text. Keep the middle large and unmarked, maintain the pale neutral paper, and add no text, new lines, decoration or diagrams.
```

### Previous frontispiece paper

```text
Use case: illustration-story
Asset type: a quiet, nearly plain portrait background for an anatomy atlas game cover.
Create only a single sheet of lightly textured, warm ivory book paper, shown perfectly flat, front-on and edge to edge, as though it were a clean unused page from a well-kept 19th-century anatomical atlas. Give it delicate fine paper grain and very subtle, soft variations in cream and pale honey. The sheet should feel tactile and lightly aged while remaining light and even, especially through the center where dark interface text will sit. Use a tall phone portrait composition, ideally 780:1688. Fill the entire image with continuous paper so it can be cropped to this ratio.
No illustration or drawing of any kind, no objects, no text, no ruled lines, no ornament, no border, no dark corners, no folds, no marks, no strong stains, no book edges, no perspective, no lighting shadows. The whole image is unobtrusive warm ivory paper.
```

### Previous frontispiece layout

```text
Use case: illustration-story
Asset type: understated full-bleed portrait frontispiece for an Anatomy atlas game. The game's title, controls and description will be rendered over it.
Input images: Image 1 is the ivory paper background to preserve. Image 2, the Cookbook cover, is a reference only for the visual hierarchy: quiet paper across the middle and sparse subject artwork at the edges. Image 3 is a reference for the little cell cross-section and its restrained atlas palette.
On the lightly textured ivory paper, draw just two modest anatomical studies. Place a small, lightly engraved cross-section of a cell, including its nucleus, above the center at about 15% of the page height. Draw it with a little dusty blue and rose wash and spare, delicate hatching, no larger than about one quarter of the canvas width. Along the bottom, below 81% of the canvas height, place a single oblique study of the human wrist and hand bones, in warm ivory and soft sepia, with a gentle low-contrast wash. Keep it entirely within the central 70% of the width. The two forms should be recognizable at phone size yet as quiet as the line studies on the Cookbook cover.
Leave the entire middle, from 29% to 78% of the image height, as continuous clean textured ivory paper from left to right, with no marks or silhouettes there. Let paper extend to all four edges. Tall narrow portrait composition for a 780:1688 cover. Make this sparse and serene, as if from a gently worn 19th-century anatomy book. Use fine etched contours with selective understated detail. No text, letters, numbers, captions, border, torso, extra specimens, ornaments, panel divisions, or strong shadows.
```

### Previous frontispiece artwork

```text
Use case: precise-object-edit
Asset type: sparse, text-free frontispiece for a 19th-century anatomy atlas game.
Image 1 is the edit target. Preserve its warm ivory paper, large clean middle, lower engraved wrist-and-finger-bone study, and tall landscape-free poster composition. Image 2 is a historical style reference only for the contour engraving and muted colouring of upper-arm muscle.
Replace only the small round cell study near the top of Image 1 with a restrained anatomical atelier study of one human shoulder and upper arm, a little diagonal and wider than it is tall. Show the recognizable rounded deltoid and long biceps transitioning to a tendon, with the suggestion of the shoulder joint underneath. Make it a small, gently faded sepia engraving with a restrained muted rose wash and selective hatching, with the same quiet treatment as the hand below. No whole torso, no skin wound, no dramatic dark lines. Keep the entire upper drawing above 28% of the page height, roughly 42% of the image width, comfortably away from all edges, like an understated plate at the head of a poster.
Preserve the tall portrait aspect and keep all of the paper from 29% to 76% page height completely unprinted, so the game can place a title and description there. Do not shift, expand, or redraw the hand at the bottom. No lettering, headings, page numbers, arrows, borders, frames, or graphic ornaments.
```

### Chapter paper

```text
Use case: illustration-story
Asset type: shared background stock for the chapter boards of an anatomical atlas game, designed to sit behind interactive engraving cutouts.
Make a blank sheet of matte pale ivory paper, the quiet backdrop of a carefully printed anatomical textbook plate or an educational poster in a doctor's consulting room. Show it directly face-on and full bleed, with a clean, neutral warm-white center and an extremely fine, very low-contrast paper grain. Just enough soft cool-gray and bone undertone to distinguish this from a flat white screen. Keep it nearly uniform and light across the entire sheet so fine marks on separate foreground artwork read clearly, with no gradient, sheen or shadows.
Tall narrow 780:1688 portrait proportions, suitable for cropping if needed. Only the unprinted paper surface. No diagrams, anatomy, figures, marks, symbols, rules, grids, frames, border, headers, footers, typography, blank boxes, stains, scratches, folded corners, page edges, book spine, or objects.
```
