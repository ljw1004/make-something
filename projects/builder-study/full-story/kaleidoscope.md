## `bf-ka-mirrors` Three mirrors
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Kaleidoscope](assets/items/kaleidoscope.webp)

**Goals**
- Fit a Mirror to the Backing
  - either: `bf-ka-mirrors-1`
  - or: `bf-ka-only-2`
  - or: `bf-ka-only-3`
- next: Fit another Mirror
  - either: `bf-ka-mirrors-2`
  - or: `bf-ka-pair-13`
  - or: `bf-ka-pair-23`
- next: Fit the last Mirror -- `bf-ka-mirrors-3`
- next: Fold the mirrors into a triangle -- `bf-ka-prism`
- next: Slide the triangle into the Viewing tube -- `bf-ka-viewer`

**Hotspots**
- `bf-ka-fold` (center 130px, 216px)
  - icon: ![Fold](assets/actions/fold.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `bf-ka-backing` Backing
  - icon: ![Backing](assets/items/bf-ka-backing.webp)

  ---

  One continuous scored binding sheet. Its three adhesive panels hold the mirror backs; the flexible seams become hinges.
- `bf-ka-mirror-1` Mirror
  - icon: ![Mirror](assets/items/bf-ka-mirror-1.webp)
- `bf-ka-mirrors-1` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-mirrors-1.webp)
- `bf-ka-mirror-2` Mirror
  - icon: ![Mirror](assets/items/bf-ka-mirror-2.webp)
- `bf-ka-mirrors-2` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-mirrors-2.webp)
- `bf-ka-mirror-3` Mirror
  - icon: ![Mirror](assets/items/bf-ka-mirror-3.webp)
- `bf-ka-mirrors-3` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-mirrors-3.webp)
- `bf-ka-fold` Fold
  - icon: ![Fold](assets/actions/fold.svg)
- `bf-ka-prism` Mirror triangle
  - icon: ![Mirror triangle](assets/items/bf-ka-prism.webp)
- `bf-ka-tube` Viewing tube
  - icon: ![Viewing tube](assets/items/bf-ka-tube.webp)

  ---

  A prepared protective tube with a dark eyecap, padded mirror supports and a retained turning collar.
- `bf-ka-viewer` Viewing tube
  - icon: ![Viewing tube](assets/items/bf-ka-viewer.webp)
- `bf-ka-only-2` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-only-2.webp)
- `bf-ka-only-3` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-only-3.webp)
- `bf-ka-pair-13` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-pair-13.webp)
- `bf-ka-pair-23` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-pair-23.webp)

**Combinations**
- `bf-ka-backing` [transform] + `bf-ka-mirror-1` [consume] -> `bf-ka-mirrors-1`
- `bf-ka-mirrors-1` [transform] + `bf-ka-mirror-2` [consume] -> `bf-ka-mirrors-2`
- `bf-ka-mirrors-2` [transform] + `bf-ka-mirror-3` [consume] -> `bf-ka-mirrors-3`
- `bf-ka-mirrors-3` [transform] @ `bf-ka-fold` -> `bf-ka-prism`
- `bf-ka-prism` [transform] + `bf-ka-tube` [consume] -> `bf-ka-viewer`
- `bf-ka-backing` [transform] + `bf-ka-mirror-2` [consume] -> `bf-ka-only-2`
- `bf-ka-backing` [transform] + `bf-ka-mirror-3` [consume] -> `bf-ka-only-3`
- `bf-ka-mirrors-1` [transform] + `bf-ka-mirror-3` [consume] -> `bf-ka-pair-13`
- `bf-ka-only-2` [transform] + `bf-ka-mirror-1` [consume] -> `bf-ka-mirrors-2`
- `bf-ka-only-2` [transform] + `bf-ka-mirror-3` [consume] -> `bf-ka-pair-23`
- `bf-ka-only-3` [transform] + `bf-ka-mirror-1` [consume] -> `bf-ka-pair-13`
- `bf-ka-only-3` [transform] + `bf-ka-mirror-2` [consume] -> `bf-ka-pair-23`
- `bf-ka-pair-13` [transform] + `bf-ka-mirror-2` [consume] -> `bf-ka-mirrors-3`
- `bf-ka-pair-23` [transform] + `bf-ka-mirror-1` [consume] -> `bf-ka-mirrors-3`


## `bf-ka-colours` A pocket full of colours
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Kaleidoscope](assets/items/kaleidoscope.webp)

**Goals**
- Put the Triangle in the Colour cell -- `bf-ka-colour-1`
- next: Add the Crescent -- `bf-ka-colour-2`
- next: Add the Disc -- `bf-ka-colour-3`
- next: Snap on the Clear lid -- `bf-ka-lidded`
- next: Fit the Light cover -- `bf-ka-covered`
- next: Fit the Colour cell to the Viewing tube -- `kaleidoscope`

**Items**
- `bf-ka-cell` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-cell.webp)

  ---

  A connected clear-bottomed cell with a rotating collar fitting. Its separate snap lid leaves space for the coloured pieces to tumble.
- `bf-ka-triangle` Triangle
  - icon: ![Triangle](assets/items/bf-ka-triangle.webp)
- `bf-ka-colour-1` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-colour-1.webp)
- `bf-ka-crescent` Crescent
  - icon: ![Crescent](assets/items/bf-ka-crescent.webp)
- `bf-ka-colour-2` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-colour-2.webp)
- `bf-ka-disc` Disc
  - icon: ![Disc](assets/items/bf-ka-disc.webp)
- `bf-ka-colour-3` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-colour-3.webp)
- `bf-ka-lid` Clear lid
  - icon: ![Clear lid](assets/items/bf-ka-lid.webp)
- `bf-ka-lidded` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-lidded.webp)
- `bf-ka-diffuser` Light cover
  - icon: ![Light cover](assets/items/bf-ka-diffuser.webp)
- `bf-ka-covered` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-covered.webp)
- `bf-ka-viewer` Viewing tube
  - icon: ![Viewing tube](assets/items/bf-ka-viewer.webp)
- `kaleidoscope` Kaleidoscope
  - icon: ![Kaleidoscope](assets/items/kaleidoscope.webp)

**Combinations**
- `bf-ka-cell` [transform] + `bf-ka-triangle` [consume] -> `bf-ka-colour-1`
- `bf-ka-colour-1` [transform] + `bf-ka-crescent` [consume] -> `bf-ka-colour-2`
- `bf-ka-colour-2` [transform] + `bf-ka-disc` [consume] -> `bf-ka-colour-3`
- `bf-ka-colour-3` [transform] + `bf-ka-lid` [consume] -> `bf-ka-lidded`
- `bf-ka-lidded` [transform] + `bf-ka-diffuser` [consume] -> `bf-ka-covered`
- `bf-ka-viewer` [transform] + `bf-ka-covered` [consume] -> `kaleidoscope`
