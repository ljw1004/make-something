## `bf-pe-build` A look over the hedge
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Periscope](assets/items/periscope.webp)

**Goals**
- Fold the first side -- `bf-pe-fold-1`
- next: Fold the second side -- `bf-pe-fold-2`
- next: Fold and close the long seam -- `bf-pe-tube`
- next: Flip to the upper opening -- `bf-pe-rear`
- next: Fit the Upper mirror -- `bf-pe-upper-fit`
- next: Fold the top closed -- `bf-pe-top-closed`
- next: Fit the Top shade -- `bf-pe-shaded`
- next: Flip to the lower opening -- `bf-pe-front`
- next: Fit the Lower mirror -- `bf-pe-mirrored`
- next: Fold the bottom closed -- `bf-pe-closed`
- next: Fit the Eye shade -- `periscope`

**Hotspots**
- `bf-pe-flip` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)
- `bf-pe-fold` (center 390px, 216px)
  - icon: ![Fold](assets/actions/fold.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-pe-net` Tube net
  - icon: ![Tube net](assets/items/bf-pe-net.webp)

  ---

  One scored card net with dark inner faces, two end flaps, mirror ledges and prepared adhesive seam tabs. The end flaps stay open while you fit the mirrors.
- `bf-pe-fold` Fold
  - icon: ![Fold](assets/actions/fold.svg)
- `bf-pe-fold-1` Tube
  - icon: ![Tube](assets/items/bf-pe-fold-1.webp)
- `bf-pe-fold-2` Tube
  - icon: ![Tube](assets/items/bf-pe-fold-2.webp)
- `bf-pe-tube` Tube
  - icon: ![Tube](assets/items/bf-pe-tube.webp)
- `bf-pe-flip` Flip
  - icon: ![Flip](assets/actions/flip.svg)
- `bf-pe-rear` Tube
  - icon: ![Tube](assets/items/bf-pe-rear.webp)
- `bf-pe-upper` Upper mirror
  - icon: ![Upper mirror](assets/items/bf-pe-upper.webp)

  ---

  An unbreakable mirror with retained edge clips. It seats on the upper forty-five-degree ledges.
- `bf-pe-upper-fit` Tube
  - icon: ![Tube](assets/items/bf-pe-upper-fit.webp)
- `bf-pe-top-closed` Tube
  - icon: ![Tube](assets/items/bf-pe-top-closed.webp)
- `bf-pe-top-shade` Top shade
  - icon: ![Top shade](assets/items/bf-pe-top-shade.webp)

  ---

  One stepped window hood. Its narrow neck enters the opening while its prepared adhesive flange rests on the card outside.
- `bf-pe-shaded` Tube
  - icon: ![Tube](assets/items/bf-pe-shaded.webp)
- `bf-pe-front` Tube
  - icon: ![Tube](assets/items/bf-pe-front.webp)
- `bf-pe-lower` Lower mirror
  - icon: ![Lower mirror](assets/items/bf-pe-lower.webp)

  ---

  A matching mirror in retained clips. Its reflecting face remains parallel to the upper mirror, redirecting the light towards your eye.
- `bf-pe-mirrored` Tube
  - icon: ![Tube](assets/items/bf-pe-mirrored.webp)
- `bf-pe-closed` Tube
  - icon: ![Tube](assets/items/bf-pe-closed.webp)
- `bf-pe-eye-shade` Eye shade
  - icon: ![Eye shade](assets/items/bf-pe-eye-shade.webp)

  ---

  A matching stepped hood for the lower window, with prepared adhesive on its outer flange.
- `periscope` Periscope
  - icon: ![Periscope](assets/items/periscope.webp)

**Combinations**
- `bf-pe-net` [transform] @ `bf-pe-fold` -> `bf-pe-fold-1`
- `bf-pe-fold-1` [transform] @ `bf-pe-fold` -> `bf-pe-fold-2`
- `bf-pe-fold-2` [transform] @ `bf-pe-fold` -> `bf-pe-tube`
- `bf-pe-tube` [transform] @ `bf-pe-flip` -> `bf-pe-rear`
- `bf-pe-rear` [transform] + `bf-pe-upper` [consume] -> `bf-pe-upper-fit`
- `bf-pe-upper-fit` [transform] @ `bf-pe-fold` -> `bf-pe-top-closed`
- `bf-pe-top-closed` [transform] + `bf-pe-top-shade` [consume] -> `bf-pe-shaded`
- `bf-pe-shaded` [transform] @ `bf-pe-flip` -> `bf-pe-front`
- `bf-pe-front` [transform] + `bf-pe-lower` [consume] -> `bf-pe-mirrored`
- `bf-pe-mirrored` [transform] @ `bf-pe-fold` -> `bf-pe-closed`
- `bf-pe-closed` [transform] + `bf-pe-eye-shade` [consume] -> `periscope`
