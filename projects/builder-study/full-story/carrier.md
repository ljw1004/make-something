## `c-lift-frame` The impossible part
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Build reference](assets/items/fc-lift-frame.webp)

Jo sets down a violet tile. “This part is invented: power makes it lift.”

**Goals**
- Fit an arch to the deck -- `fc-one-arch`
- next: Fit the second arch -- `fc-arches`
- next: Clip the cradle across the arches -- `fc-top`
- next: Seat the lift tile -- `fc-tiled`
- next: Flip the frame over -- `fc-inverted`
- next: Fit the battery underneath -- `fc-powered`
- next: Flip the frame upright -- `fc-upright`
- next: Fit the lift control -- `fc-lift-frame`

**Hotspots**
- `fc-flip-lift` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `fc-deck` Deck
  - icon: ![Deck](assets/items/fc-deck.webp)

  ---

  A 400 × 300 mm prepared plywood deck. The mounting holes and wire passages are already cut.
- `fc-arch-a` Arch
  - icon: ![Arch](assets/items/fc-arch-a.webp)

  ---

  One connected rigid arch with two feet and captive bolts.
- `fc-arch-b` Arch
  - icon: ![Arch](assets/items/fc-arch-b.webp)

  ---

  A second identical connected arch. Either arch fits either side of the deck.
- `fc-cradle` Tile cradle
  - icon: ![Tile cradle](assets/items/fc-cradle.webp)

  ---

  One connected top cradle. Four integral saddles clip over the arches; its padded rails receive the tile.
- `fc-tile` Lift tile
  - icon: ![Lift tile](assets/items/fc-tile.webp)

  ---

  This powered lift tile is explicitly fictional. Its limited force points upward while current flows. It makes no energy and carries no person.
- `fc-battery` Battery pack
  - icon: ![Battery pack](assets/items/fc-battery.webp)

  ---

  A compatible enclosed battery in its integral retained bracket. It mounts below the deck, keeping weight low.
- `fc-control` Lift control
  - icon: ![Lift control](assets/items/fc-control.webp)

  ---

  A prepared controller and latching stop button in one pod with a connected fused harness. Keep power off while fitting it.
- `fc-one-arch` Frame
  - icon: ![Frame](assets/items/fc-one-arch.webp)
- `fc-arches` Frame
  - icon: ![Frame](assets/items/fc-arches.webp)
- `fc-top` Frame
  - icon: ![Frame](assets/items/fc-top.webp)
- `fc-tiled` Frame
  - icon: ![Frame](assets/items/fc-tiled.webp)
- `fc-inverted` Frame
  - icon: ![Frame](assets/items/fc-inverted.webp)
- `fc-powered` Frame
  - icon: ![Frame](assets/items/fc-powered.webp)
- `fc-upright` Frame
  - icon: ![Frame](assets/items/fc-upright.webp)
- `fc-lift-frame` Frame
  - icon: ![Frame](assets/items/fc-lift-frame.webp)
- `fc-flip-lift` Flip

**Combinations**
- `fc-arch-a` [consume] + `fc-deck` [transform] -> `fc-one-arch`
- `fc-arch-a` [consume] + `fc-one-arch` [transform] -> `fc-arches`
- `fc-arch-b` [consume] + `fc-deck` [transform] -> `fc-one-arch`
- `fc-arch-b` [consume] + `fc-one-arch` [transform] -> `fc-arches`
- `fc-cradle` [consume] + `fc-arches` [transform] -> `fc-top`
- `fc-tile` [consume] + `fc-top` [transform] -> `fc-tiled`
- `fc-tiled` [transform] @ `fc-flip-lift` -> `fc-inverted`
- `fc-battery` [consume] + `fc-inverted` [transform] -> `fc-powered`
- `fc-powered` [transform] @ `fc-flip-lift` -> `fc-upright`
- `fc-control` [consume] + `fc-upright` [transform] -> `fc-lift-frame`


## `c-lift-projector` Stars aboard
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Build reference](assets/items/fc-powered-show.webp)

**Goals**
- Fit the projector dock -- `fc-docked`
- next: Press your projector onto the dock -- `fc-projector-aboard`
- next: Fit the small pulley to the motor -- `fc-drive`
- next: Mount the drive motor -- `fc-motor-mounted`
- next: Loop the belt around both pulleys -- `fc-belted`
- next: Flip to the underside -- `fc-drive-under`
- next: Fit the Motor supply -- `fc-supply-under`
- next: Flip the Frame upright -- `fc-powered-show`

**Hotspots**
- `fc-flip-drive` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `star-projector` Star projector
  - from chapter `c-lift-projector` icon: ![Star projector](assets/items/fc-projector-carried.webp)
- `fc-dock` Projector dock
  - icon: ![Projector dock](assets/items/fc-dock.webp)

  ---

  One connected projector dock. Four feet bear on the deck and two recessed captive screws fasten it down. Four split snap studs pass through the original mounting holes; their flexible heads spring out above the box collars to retain the unchanged projector.
- `fc-motor` Gearmotor
  - icon: ![Gearmotor](assets/items/fc-motor.webp)

  ---

  An enclosed slow gearmotor with its integral pedestal and lead. The shaft is parallel to the projector spindle.
- `fc-pulley` Small pulley
  - icon: ![Small pulley](assets/items/fc-pulley.webp)

  ---

  One small pulley with a captive screw that clamps onto the motor shaft flat.
- `fc-belt` Belt
  - icon: ![Belt](assets/items/fc-belt.webp)

  ---

  One continuous soft belt. Its small pulley drives the larger grooved handwheel more slowly.
- `fc-motor-pack` Motor supply
  - icon: ![Motor supply](assets/items/fc-motor-pack.webp)

  ---

  An enclosed low-voltage motor supply with its own switch, lead and integral mounting bracket. The lamp keeps its original supply; the lift has a separate circuit.
- `fc-docked` Frame
  - icon: ![Frame](assets/items/fc-docked.webp)
- `fc-projector-aboard` Frame
  - icon: ![Frame](assets/items/fc-projector-aboard.webp)
- `fc-drive` Drive motor
  - icon: ![Drive motor](assets/items/fc-drive.webp)
- `fc-motor-mounted` Frame
  - icon: ![Frame](assets/items/fc-motor-mounted.webp)
- `fc-belted` Frame
  - icon: ![Frame](assets/items/fc-belted.webp)
- `fc-drive-under` Frame
  - icon: ![Frame](assets/items/fc-drive-under.webp)
- `fc-supply-under` Frame
  - icon: ![Frame](assets/items/fc-supply-under.webp)
- `fc-powered-show` Frame
  - icon: ![Frame](assets/items/fc-powered-show.webp)
- `fc-flip-drive` Flip

**Combinations**
- `fc-dock` [consume] + `fc-lift-frame` [transform] -> `fc-docked`
- `star-projector` [consume] + `fc-docked` [transform] -> `fc-projector-aboard`
- `fc-pulley` [consume] + `fc-motor` [transform] -> `fc-drive`
- `fc-drive` [consume] + `fc-projector-aboard` [transform] -> `fc-motor-mounted`
- `fc-belt` [consume] + `fc-motor-mounted` [transform] -> `fc-belted`
- `fc-belted` [transform] @ `fc-flip-drive` -> `fc-drive-under`
- `fc-motor-pack` [consume] + `fc-drive-under` [transform] -> `fc-supply-under`
- `fc-supply-under` [transform] @ `fc-flip-drive` -> `fc-powered-show`


## `c-whale-shape` A whale takes shape
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Build reference](assets/items/fc-whale.webp)

**Goals**
- Fit the Front side -- `fc-near-side`
- next: Turn to the back -- `fc-side-rear`
- next: Fit the Back side -- `fc-sided`
- next: Fit the Tail -- `fc-tailed`
- next: Fit the Back fin -- `fc-one-fin-b`
- next: Turn to the front -- `fc-fin-front`
- next: Fit the Front fin -- `fc-whale`

**Hotspots**
- `fc-flip-shell` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `fc-side-a` Front side
  - icon: ![Front side](assets/items/fc-side-a.webp)

  ---

  One cut whale side panel with its mounting tabs. Its top edge stays below the projector beam.
- `fc-side-b` Back side
  - icon: ![Back side](assets/items/fc-side-b.webp)

  ---

  A second whale side panel, fitted separately.
- `fc-tail` Tail
  - icon: ![Tail](assets/items/fc-tail.webp)

  ---

  One continuous fixed tail with its prepared root fitting. It does not steer or provide lift.
- `fc-fin-a` Front fin
  - icon: ![Front fin](assets/items/fc-fin-a.webp)

  ---

  One fixed fin with two integral mushroom studs and a captive centre screw. The keyhole entries sit below the deck. With the screw retracted, pass the heads through the wide openings and lower the fin into the narrow slots. Tighten the screw to retain it during flips. It gives the whale its shape, not lift.
- `fc-fin-b` Back fin
  - icon: ![Back fin](assets/items/fc-fin-b.webp)

  ---

  The other fixed fin.
- `fc-near-side` Whale
  - icon: ![Whale](assets/items/fc-near-side.webp)
- `fc-side-rear` Whale
  - icon: ![Whale](assets/items/fc-side-rear.webp)
- `fc-sided` Whale
  - icon: ![Whale](assets/items/fc-sided.webp)
- `fc-tailed` Whale
  - icon: ![Whale](assets/items/fc-tailed.webp)
- `fc-one-fin-b` Whale
  - icon: ![Whale](assets/items/fc-one-fin-b.webp)
- `fc-fin-front` Whale
  - icon: ![Whale](assets/items/fc-fin-front.webp)
- `fc-whale` Whale
  - icon: ![Whale](assets/items/fc-whale.webp)
- `fc-flip-shell` Flip

**Combinations**
- `fc-side-a` [consume] + `fc-powered-show` [transform] -> `fc-near-side`
- `fc-near-side` [transform] @ `fc-flip-shell` -> `fc-side-rear`
- `fc-side-b` [consume] + `fc-side-rear` [transform] -> `fc-sided`
- `fc-tail` [consume] + `fc-sided` [transform] -> `fc-tailed`
- `fc-fin-b` [consume] + `fc-tailed` [transform] -> `fc-one-fin-b`
- `fc-one-fin-b` [transform] @ `fc-flip-shell` -> `fc-fin-front`
- `fc-fin-a` [consume] + `fc-fin-front` [transform] -> `fc-whale`


## `c-whale-finish` Ready for the fair
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Build reference](assets/items/flying-whale.webp)

**Goals**
- Flip the whale over -- `fc-whale-under`
- next: Fit a landing skid
  - either: `fc-one-skid-a`
  - or: `fc-one-skid-b`
  - or: `fc-skids`
- next: Fit the other skid -- `fc-skids`
- next: Fit the weight rail -- `fc-railed`
- next: Fit the weight through the wide slot -- `fc-weighted`
- next: Flip the whale upright -- `fc-standing`
- next: Fit the clear drive guard -- `flying-whale`

**Hotspots**
- `fc-flip-feet` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `fc-skid-a` Landing skid
  - icon: ![Landing skid](assets/items/fc-skid-a.webp)

  ---

  One connected landing skid with two upright legs and captive deck bolts.
- `fc-skid-b` Landing skid
  - icon: ![Landing skid](assets/items/fc-skid-b.webp)

  ---

  A second landing skid. Their feet reach below the batteries and trim weight.
- `fc-rail` Weight rail
  - icon: ![Weight rail](assets/items/fc-rail.webp)

  ---

  One slotted rail with integral mounting ears, closed travel ends and a wide keyhole entry near the right end. The weight shoe enters through that opening from below.
- `fc-weight` Counterweight
  - icon: ![Counterweight](assets/items/fc-weight.webp)

  ---

  A single sliding weight with a captive shoe, vertical clamp screw and washer. Raise the shoe through the wide rail entry, slide into the narrow track, then tighten the screw to clamp the rail between shoe and pad.
- `fc-guard` Guard
  - icon: ![Guard](assets/items/fc-guard.webp)

  ---

  One hollow clear hood, open underneath and at the rear. Lower it over the drive, then tighten the captive screws on its exposed side feet. It encloses the belt and hand grip without covering the lens.
- `fc-whale-under` Whale
  - icon: ![Whale](assets/items/fc-whale-under.webp)
- `fc-one-skid-a` Whale
  - icon: ![Whale](assets/items/fc-one-skid-a.webp)
- `fc-one-skid-b` Whale
  - icon: ![Whale](assets/items/fc-one-skid-b.webp)
- `fc-skids` Whale
  - icon: ![Whale](assets/items/fc-skids.webp)
- `fc-railed` Whale
  - icon: ![Whale](assets/items/fc-railed.webp)
- `fc-weighted` Whale
  - icon: ![Whale](assets/items/fc-weighted.webp)
- `fc-standing` Whale
  - icon: ![Whale](assets/items/fc-standing.webp)
- `flying-whale` Whale
  - icon: ![Whale](assets/items/flying-whale.webp)

  ---

  The real projector, motor, belt, batteries, arches and counterweight retain their ordinary jobs. Only the violet lift tile is fictional. The exposed rail lets the weight move opposite a heavier end while the machine is supported and disconnected. This is a dimensioned story model, not a manufactured flying toy.
- `fc-flip-feet` Flip

**Combinations**
- `fc-whale` [transform] @ `fc-flip-feet` -> `fc-whale-under`
- `fc-skid-a` [consume] + `fc-whale-under` [transform] -> `fc-one-skid-a`
- `fc-skid-b` [consume] + `fc-one-skid-a` [transform] -> `fc-skids`
- `fc-skid-b` [consume] + `fc-whale-under` [transform] -> `fc-one-skid-b`
- `fc-skid-a` [consume] + `fc-one-skid-b` [transform] -> `fc-skids`
- `fc-rail` [consume] + `fc-skids` [transform] -> `fc-railed`
- `fc-weight` [consume] + `fc-railed` [transform] -> `fc-weighted`
- `fc-weighted` [transform] @ `fc-flip-feet` -> `fc-standing`
- `fc-guard` [consume] + `fc-standing` [transform] -> `flying-whale`
