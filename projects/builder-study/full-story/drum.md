## `bf-film-build` A slit drum
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Animation drum](assets/items/animation-drum.webp)

**Goals**
- Cut the marked viewing slits -- `bf-film-cut`
- next: Roll the Drum wall -- `bf-film-rolled`
- next: Tape the seam -- `bf-film-seamed`

**Hotspots**
- `bf-film-cut-process` (center 130px, 216px)
  - icon: ![Cut](assets/actions/cut.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)
- `bf-film-roll-process` (center 390px, 216px)
  - icon: ![Roll](assets/actions/roll.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-film-wall` Drum wall
  - icon: ![Drum wall](assets/items/bf-film-wall.webp)

  ---

  One card strip with twelve marked slots and scored floor tabs. Their tips stay straight until the floor is seated. Cut down to the stopping line; the lower band stays continuous.
- `bf-film-cut-process` Cut
  - icon: ![Cut](assets/actions/cut.svg)
- `bf-film-cut` Drum wall
  - icon: ![Drum wall](assets/items/bf-film-cut.webp)
- `bf-film-roll-process` Roll
  - icon: ![Roll](assets/actions/roll.svg)
- `bf-film-rolled` Drum
  - icon: ![Drum](assets/items/bf-film-rolled.webp)
- `bf-film-tape` Tape
  - icon: ![Tape](assets/items/bf-film-tape.webp)
- `bf-film-seamed` Drum
  - icon: ![Drum](assets/items/bf-film-seamed.webp)

**Combinations**
- `bf-film-wall` [transform] @ `bf-film-cut-process` -> `bf-film-cut`
- `bf-film-cut` [transform] @ `bf-film-roll-process` -> `bf-film-rolled`
- `bf-film-rolled` [transform] + `bf-film-tape` [consume] -> `bf-film-seamed`


## `bf-film-floor-build` A turning drum
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Animation drum](assets/items/animation-drum.webp)

**Goals**
- Flip the Drum over -- `bf-film-under`
- next: Fold the scored tabs inward -- `bf-film-prepared`
- next: Slide the Floor over the straight tips -- `bf-film-seated`
- next: Fold the tabs under the Floor -- `bf-film-shell`
- next: Fit the Turntable to the Base -- `bf-film-turntable`
- next: Fit the Base beneath the Drum -- `bf-film-mounted-under`
- next: Flip the Drum upright -- `bf-film-standing`

**Hotspots**
- `bf-film-flip-process` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)
- `bf-film-fold-process` (center 390px, 216px)
  - icon: ![Fold](assets/actions/fold.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-film-seamed` Drum
  - icon: ![Drum](assets/items/bf-film-seamed.webp)
- `bf-film-flip-process` Flip
  - icon: ![Flip](assets/actions/flip.svg)
- `bf-film-under` Drum
  - icon: ![Drum](assets/items/bf-film-under.webp)
- `bf-film-fold-process` Fold
  - icon: ![Fold](assets/actions/fold.svg)
- `bf-film-prepared` Drum
  - icon: ![Drum](assets/items/bf-film-prepared.webp)
- `bf-film-floor` Floor
  - icon: ![Floor](assets/items/bf-film-floor.webp)

  ---

  A 178.8 mm disc, smaller than the wall opening, with twelve slots for the straight tabs. Fold the tips underneath only after inserting it.
- `bf-film-seated` Drum
  - icon: ![Drum](assets/items/bf-film-seated.webp)
- `bf-film-shell` Drum
  - icon: ![Drum](assets/items/bf-film-shell.webp)
- `bf-film-base` Base
  - icon: ![Base](assets/items/bf-film-base.webp)
- `bf-film-bearing` Turntable
  - icon: ![Turntable](assets/items/bf-film-bearing.webp)

  ---

  One retained spindle, sleeve bearing and platform. The spindle stays fixed in the base while the platform turns.
- `bf-film-turntable` Base
  - icon: ![Base](assets/items/bf-film-turntable.webp)
- `bf-film-mounted-under` Drum
  - icon: ![Drum](assets/items/bf-film-mounted-under.webp)
- `bf-film-standing` Drum
  - icon: ![Drum](assets/items/bf-film-standing.webp)

**Combinations**
- `bf-film-seamed` [transform] @ `bf-film-flip-process` -> `bf-film-under`
- `bf-film-under` [transform] @ `bf-film-fold-process` -> `bf-film-prepared`
- `bf-film-prepared` [transform] + `bf-film-floor` [consume] -> `bf-film-seated`
- `bf-film-seated` [transform] @ `bf-film-fold-process` -> `bf-film-shell`
- `bf-film-base` [transform] + `bf-film-bearing` [consume] -> `bf-film-turntable`
- `bf-film-shell` [transform] + `bf-film-turntable` [consume] -> `bf-film-mounted-under`
- `bf-film-mounted-under` [transform] @ `bf-film-flip-process` -> `bf-film-standing`


## `bf-film-pictures` A tiny picture show
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Animation drum](assets/items/animation-drum.webp)

**Goals**
- Roll the Picture strip -- `bf-film-loop`
- next: Fit the Picture ring inside the Drum -- `animation-drum`

**Hotspots**
- `bf-film-picture-roll` (center 130px, 216px)
  - icon: ![Roll](assets/actions/roll.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `bf-film-strip` Picture strip
  - icon: ![Picture strip](assets/items/bf-film-strip.webp)

  ---

  A printed sequence of twelve fish pictures, one per viewing slit, with a prepared adhesive overlap. The pictures face inward when rolled.
- `bf-film-picture-roll` Roll
  - icon: ![Roll](assets/actions/roll.svg)
- `bf-film-loop` Picture ring
  - icon: ![Picture ring](assets/items/bf-film-loop.webp)
- `bf-film-standing` Drum
  - icon: ![Drum](assets/items/bf-film-standing.webp)
- `animation-drum` Animation drum
  - icon: ![Animation drum](assets/items/animation-drum.webp)

  ---

  Looking through the slits gives brief separated glimpses of successive pictures, with darkness between them.

**Combinations**
- `bf-film-strip` [transform] @ `bf-film-picture-roll` -> `bf-film-loop`
- `bf-film-standing` [transform] + `bf-film-loop` [consume] -> `animation-drum`
