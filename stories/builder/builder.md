# ![A brick-red paper pinwheel](icon.png) A Fair in the Air
background: ![White instruction page](assets/backgrounds/white.svg)

Build toys that move, draw and shine—then make a little garden fair do something impossible.

## `c01` Something that moves
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pinwheel](assets/items/pinwheel.webp)

**Goals**
- Fold the first corner inward -- `pw-one-blade`
- next: Fold the second corner inward -- `pw-two-blades`
- next: Fold the third corner inward -- `pw-three-blades`
- next: Fold the last corner inward -- `pw-loose-rotor`
- next: Fit the hub to the blades -- `pw-folded-rotor`
- next: Flip the blades over -- `pw-rear-rotor`
- next: Fit the axle into the back of the hub -- `pw-bearing-rotor`
- next: Clip the handle onto the axle -- `pw-mounted`
- next: Flip the pinwheel to the front -- `pinwheel`

**Hotspots**
- `pw-fold` (center 390px, 216px)
  - icon: ![Dotted paper folding diagram](assets/actions/fold.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)
- `pw-flip` (center 130px, 216px)
  - icon: ![Outline diagram of turning a sheet over](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `pw-fold` Fold
- `pw-flip` Flip
- `pw-paper` Paper
  - icon: ![Prepared paper square](assets/items/pw-paper.webp) (center 358px, 830px)

  {A flat brick-red square. Fine diagonal lines run inward from its corners; round holes sit near the corners and centre.}

  ---

  The paper sheet is already cut along four diagonals, stopping short of the centre. Curl the four pierced corners inward; keep the uncut centre whole.
- `pw-hub` Hub
  - icon: ![Teal hub](assets/items/pw-hub.webp) (center 140px, 460px)

  {A green round cap with four small dark holes on its face and a slotted stem behind it.}

  ---

  A hollow snap-in hub holds the folded corners together. Its centre is a bearing for the axle.
- `pw-axle` Axle
  - icon: ![Axle and spacer](assets/items/pw-axle.webp) (center 470px, 460px)

  {A thin black pin extends from a cream ring and green stepped stem ending in a round cap.}

  ---

  A blunt axle with a built-in spacer and retaining tip. The hub turns around the axle; the spacer keeps the paper clear of the handle.
- `pw-handle` Handle
  - icon: ![Wooden handle with an open axle clip](assets/items/pw-handle.webp) (center 690px, 820px)

  {A long narrow wooden handle with a green open hook at one end and small dark holes near each end.}

  ---

  The prepared clip snaps over the axle's rear post. Two small mounting holes remain near the foot of the handle.
- `pw-one-blade` Paper
  - icon: ![Paper with one folded corner](assets/items/pw-one-blade.webp)

  {One red corner curls inward, leaving an open notch at the upper right and a holed tip near the centre.}
- `pw-two-blades` Paper
  - icon: ![Paper with two folded corners](assets/items/pw-two-blades.webp)

  {Two curled red folds meet near the centre. The lower half still has two flat corners.}
- `pw-three-blades` Paper
  - icon: ![Paper with three folded corners](assets/items/pw-three-blades.webp)

  {Three curled folds meet near the centre; one flat lower-right corner with a round hole remains.}
- `pw-loose-rotor` Blades
  - icon: ![Folded paper](assets/items/pw-loose-rotor.webp)

  {Four curled red blades surround a small dark hole at the centre.}
- `pw-folded-rotor` Blades
  - icon: ![Blades with hub](assets/items/pw-folded-rotor.webp)

  {Four curled red blades meet beneath a small green round cap.}
- `pw-rear-rotor` Blades
  - icon: ![Back of the blades](assets/items/pw-rear-rotor.webp)

  {The pale-red back of the four blades, with a short green tip at the centre.}
- `pw-bearing-rotor` Blades
  - icon: ![Blades on their axle](assets/items/pw-bearing-rotor.webp)

  {On the back of the red blades, a cream ring and short green stem project from the centre.}
- `pw-mounted` Pinwheel
  - icon: ![Back of the pinwheel](assets/items/pw-mounted.webp)

  {The wooden handle extends down from the back of the red blades, beneath the green centre fitting.}
- `pinwheel` Pinwheel
  - icon: ![Pinwheel](assets/items/pinwheel.webp)

  {Four curled red blades surround a green centre cap. A long wooden handle extends below.}

  ---

  Four curved paper blades catch the breeze. The paper and hub turn together around the axle while the handle stays still.

**Combinations**
- `pw-paper` [transform] @ `pw-fold` -> `pw-one-blade` (tutorial)
- `pw-one-blade` [transform] @ `pw-fold` -> `pw-two-blades`
- `pw-two-blades` [transform] @ `pw-fold` -> `pw-three-blades`
- `pw-three-blades` [transform] @ `pw-fold` -> `pw-loose-rotor`
- `pw-hub` [consume] + `pw-loose-rotor` [transform] -> `pw-folded-rotor`
- `pw-folded-rotor` [transform] @ `pw-flip` -> `pw-rear-rotor`
- `pw-axle` [consume] + `pw-rear-rotor` [transform] -> `pw-bearing-rotor`
- `pw-handle` [consume] + `pw-bearing-rotor` [transform] -> `pw-mounted`
- `pw-mounted` [transform] @ `pw-flip` -> `pinwheel`


## `c02` A sail
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Completed sail](assets/items/wr-sail.webp)

**Goals**
- Fit the connector to the mast
  - either: `wr-mast-joint`
  - or: `wr-mast-joint-foot`
  - or: `wr-frame`
  - or: `wr-ready`
  - or: `wr-frame-sail`
  - or: `wr-sail`
- next: Fit the crossbar into the connector
  - either: `wr-frame`
  - or: `wr-ready`
  - or: `wr-frame-sail`
  - or: `wr-sail`
- next: Push the foot onto the mast
  - either: `wr-mast-foot`
  - or: `wr-mast-joint-foot`
  - or: `wr-ready`
  - or: `wr-sail`
- next: Clip the sail onto the mast -- `wr-sail`

**Items**
- `wr-mast-wood` Mast
  - icon: ![Mast](assets/items/wr-mast-wood.webp)

  {A long, slim tan rod lying diagonally.}
- `wr-mast-foot` Mast
  - icon: ![Mast](assets/items/wr-mast-foot.webp)

  {A long tan rod ends in a green socket with split legs.}
- `wr-mast-joint` Mast
  - icon: ![Mast](assets/items/wr-mast-joint.webp)

  {A long tan rod passes through a green block. A round side opening remains visible in the block.}
- `wr-mast-joint-foot` Mast
  - icon: ![Mast](assets/items/wr-mast-joint-foot.webp)

  {The long tan rod has a green block partway along it and a green split fitting at its lower end.}
- `wr-frame` Mast
  - icon: ![Mast](assets/items/wr-frame.webp)

  {A long tan rod and shorter crosspiece meet at a green block.}
- `wr-ready` Mast
  - icon: ![Mast](assets/items/wr-ready.webp)

  {The crossed tan rods meet at a green block. A green split fitting sits at the end of the longer rod.}
- `wr-frame-sail` Sail
  - icon: ![Sail](assets/items/wr-frame-sail.webp)

  {A cream triangular sail spans the tan frame, with a long bare rod extending below it.}
- `wr-sail` Sail
  - icon: ![Sail](assets/items/wr-sail.webp)
  - from chapter `c-racer-body` icon: ![Sail](assets/items/wr-sail-carried.webp)

  {A cream triangular sail sits on a tan frame, above a long tan rod ending in a green split fitting.}
- `wr-connector` Connector
  - icon: ![Connector](assets/items/wr-connector.webp)

  {A green block with round openings on two different faces.}

  ---

  Two offset sockets keep the wooden rods from crossing through each other. Flexible ribs grip both rods.
- `wr-crossbar` Crossbar
  - icon: ![Crossbar](assets/items/wr-crossbar.webp)

  {A short tan rod with a round end, lying diagonally.}

  ---

  A short wooden rod that supports the bottom of the sail.
- `wr-foot` Foot
  - icon: ![Foot](assets/items/wr-foot.webp)

  {A green round socket with a pale inner rim and two long split legs below.}

  ---

  The mast pushes into the top socket. The split legs underneath will snap into the chassis.
- `wr-sailcloth` Sail
  - icon: ![Sail](assets/items/wr-sailcloth.webp)

  {A cream triangular sail edged in green, with small open green clips at its corners.}

  ---

  Three small open clips are attached to the cloth. They press onto the mast and crossbar.
- `wr-crossbar-joint` Crossbar
  - icon: ![Crossbar](assets/items/wr-crossbar-joint.webp)

  {A short tan rod passes through a green block; a round opening faces upward.}

**Combinations**
- `wr-foot` [consume] + `wr-mast-wood` [transform] -> `wr-mast-foot`
- `wr-foot` [consume] + `wr-mast-joint` [transform] -> `wr-mast-joint-foot`
- `wr-foot` [consume] + `wr-frame` [transform] -> `wr-ready`
- `wr-foot` [consume] + `wr-frame-sail` [transform] -> `wr-sail`
- `wr-connector` [consume] + `wr-mast-wood` [transform] -> `wr-mast-joint`
- `wr-connector` [consume] + `wr-mast-foot` [transform] -> `wr-mast-joint-foot`
- `wr-crossbar` [consume] + `wr-mast-joint` [transform] -> `wr-frame`
- `wr-crossbar` [consume] + `wr-mast-joint-foot` [transform] -> `wr-ready`
- `wr-sailcloth` [consume] + `wr-frame` [transform] -> `wr-frame-sail`
- `wr-sailcloth` [consume] + `wr-ready` [transform] -> `wr-sail`
- `wr-connector` [consume] + `wr-crossbar` [transform] -> `wr-crossbar-joint`
- `wr-crossbar-joint` [consume] + `wr-mast-wood` [transform] -> `wr-frame`
- `wr-crossbar-joint` [consume] + `wr-mast-foot` [transform] -> `wr-ready`


## `c-racer-body` Wheels for the sail
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Wind racer](assets/items/wind-racer.webp)

**Goals**
- Flip the chassis over -- `wr-chassis`
- next: Push a wheel onto the front straw -- `wr-front-one-wheel`
- next: Push another wheel onto the front axle -- `wr-front-wheels`
- next: Push a wheel onto the rear straw -- `wr-rear-one-wheel`
- next: Push another wheel onto the rear axle -- `wr-rear-wheels`
- next: Fit a bearing to the chassis
  - either: `wr-front-bearing-chassis`
  - or: `wr-rear-bearing-chassis`
  - or: `wr-bearing-chassis`
  - or: `wr-front-rolling-chassis`
  - or: `wr-rear-rolling-chassis`
  - or: `wr-front-wheel-chassis`
  - or: `wr-rear-wheel-chassis`
  - or: `wr-rolling-chassis`
- next: Fit the other bearing
  - either: `wr-bearing-chassis`
  - or: `wr-front-wheel-chassis`
  - or: `wr-rear-wheel-chassis`
  - or: `wr-rolling-chassis`
- next: Snap wheels into a bearing
  - either: `wr-front-rolling-chassis`
  - or: `wr-rear-rolling-chassis`
  - or: `wr-front-wheel-chassis`
  - or: `wr-rear-wheel-chassis`
  - or: `wr-rolling-chassis`
- next: Snap on the other wheels -- `wr-rolling-chassis`
- next: Flip the chassis upright -- `wr-upright`
- next: Fit the sail to the chassis -- `wind-racer`

**Hotspots**
- `wr-flip` (center 390px, 216px)
  - icon: ![Turn the chassis over](assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `wr-chassis-top` Chassis
  - icon: ![Chassis](assets/items/wr-chassis-top.webp)

  {A flat tan rectangular board with four small rectangular holes and a green ring around its central round hole.}
- `wr-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-chassis.webp)

  {The other face of the tan board has green square outlines around its four rectangular holes and a plain central round hole.}
- `wr-front-bearing-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-front-bearing-chassis.webp)

  {A green channel lies across the right-hand end of the tan board. The other end still shows two square outlines.}
- `wr-rear-bearing-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-rear-bearing-chassis.webp)

  {A green channel lies across the left-hand end of the tan board. The other end still shows two square outlines.}
- `wr-bearing-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-bearing-chassis.webp)

  {Two green channels lie across opposite ends of the tan board.}
- `wr-front-rolling-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-front-rolling-chassis.webp)

  {A pair of red wheels and a green channel cross the right-hand end of the tan board; the opposite end is bare.}
- `wr-rear-rolling-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-rear-rolling-chassis.webp)

  {A pair of red wheels and a green channel cross the left-hand end of the tan board; the opposite end is bare.}
- `wr-front-wheel-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-front-wheel-chassis.webp)

  {The tan board has two green channels; a red wheel sits at each end of the right-hand channel.}
- `wr-rear-wheel-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-rear-wheel-chassis.webp)

  {The tan board has two green channels; a red wheel sits at each end of the left-hand channel.}
- `wr-rolling-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-rolling-chassis.webp)

  {Four red wheels sit beside two green channels across the exposed underside of the tan board.}
- `wr-upright` Chassis
  - icon: ![Chassis](assets/items/wr-upright.webp)

  {The tan board sits above four red wheels. Small green fittings and the green ring around the centre hole are visible on top.}
- `wind-racer` Wind racer
  - icon: ![Wind racer](assets/items/wind-racer.webp)

  {A cream triangular sail rises above a tan rectangular chassis with four red wheels.}

  ---

  The wheels turn together with each straw axle inside the bearings. Outdoors, moving air can push against the sail.
- `wr-flip` Flip
- `wr-front-bearing` Bearing
  - icon: ![Bearing](assets/items/wr-bearing.webp)

  {A long green open channel with two raised clip fittings.}

  ---

  An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.
- `wr-front-axle` Front straw
  - icon: ![Front straw](assets/items/wr-straw.webp)

  {A thin dark tube lying diagonally, with a round opening at its nearer end.}

  ---

  A stiff hollow plastic axle. Push one wheel onto each end.
- `wr-front-one-wheel` Front axle
  - icon: ![Front axle](assets/items/wr-one-wheel.webp)

  {One red wheel sits on the end of a long dark axle; its other end is bare.}
- `wr-front-wheels` Front wheels
  - icon: ![Front wheels](assets/items/wr-wheels.webp)

  {Two red wheels sit at opposite ends of one dark axle.}
- `wr-rear-bearing` Bearing
  - icon: ![Bearing](assets/items/wr-bearing.webp)

  {A long green open channel with two raised clip fittings.}

  ---

  An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.
- `wr-rear-axle` Rear straw
  - icon: ![Rear straw](assets/items/wr-straw.webp)

  {A thin dark tube lying diagonally, with a round opening at its nearer end.}

  ---

  A stiff hollow plastic axle. Push one wheel onto each end.
- `wr-rear-one-wheel` Rear axle
  - icon: ![Rear axle](assets/items/wr-one-wheel.webp)

  {One red wheel sits on the end of a long dark axle; its other end is bare.}
- `wr-rear-wheels` Rear wheels
  - icon: ![Rear wheels](assets/items/wr-wheels.webp)

  {Two red wheels sit at opposite ends of one dark axle.}
- `wr-wheel-1` Wheel
  - icon: ![Wheel](assets/items/wr-wheel.webp)

  {A thick brick-red wheel with a pale round centre.}

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-2` Wheel
  - icon: ![Wheel](assets/items/wr-wheel.webp)

  {A thick brick-red wheel with a pale round centre.}

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-3` Wheel
  - icon: ![Wheel](assets/items/wr-wheel.webp)

  {A thick brick-red wheel with a pale round centre.}

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-4` Wheel
  - icon: ![Wheel](assets/items/wr-wheel.webp)

  {A thick brick-red wheel with a pale round centre.}

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.

**Combinations**
- `wr-chassis-top` [transform] @ `wr-flip` -> `wr-chassis`
- `wr-wheel-1` [consume] + `wr-front-axle` [transform] -> `wr-front-one-wheel`
- `wr-wheel-1` [consume] + `wr-front-one-wheel` [transform] -> `wr-front-wheels`
- `wr-wheel-2` [consume] + `wr-front-axle` [transform] -> `wr-front-one-wheel`
- `wr-wheel-2` [consume] + `wr-front-one-wheel` [transform] -> `wr-front-wheels`
- `wr-wheel-3` [consume] + `wr-front-axle` [transform] -> `wr-front-one-wheel`
- `wr-wheel-3` [consume] + `wr-front-one-wheel` [transform] -> `wr-front-wheels`
- `wr-wheel-4` [consume] + `wr-front-axle` [transform] -> `wr-front-one-wheel`
- `wr-wheel-4` [consume] + `wr-front-one-wheel` [transform] -> `wr-front-wheels`
- `wr-wheel-1` [consume] + `wr-rear-axle` [transform] -> `wr-rear-one-wheel`
- `wr-wheel-1` [consume] + `wr-rear-one-wheel` [transform] -> `wr-rear-wheels`
- `wr-wheel-2` [consume] + `wr-rear-axle` [transform] -> `wr-rear-one-wheel`
- `wr-wheel-2` [consume] + `wr-rear-one-wheel` [transform] -> `wr-rear-wheels`
- `wr-wheel-3` [consume] + `wr-rear-axle` [transform] -> `wr-rear-one-wheel`
- `wr-wheel-3` [consume] + `wr-rear-one-wheel` [transform] -> `wr-rear-wheels`
- `wr-wheel-4` [consume] + `wr-rear-axle` [transform] -> `wr-rear-one-wheel`
- `wr-wheel-4` [consume] + `wr-rear-one-wheel` [transform] -> `wr-rear-wheels`
- `wr-front-bearing` [consume] + `wr-chassis` [transform] -> `wr-front-bearing-chassis`
- `wr-rear-bearing` [consume] + `wr-chassis` [transform] -> `wr-rear-bearing-chassis`
- `wr-front-bearing` [consume] + `wr-rear-bearing-chassis` [transform] -> `wr-bearing-chassis`
- `wr-rear-wheels` [consume] + `wr-rear-bearing-chassis` [transform] -> `wr-rear-rolling-chassis`
- `wr-front-bearing` [consume] + `wr-rear-rolling-chassis` [transform] -> `wr-rear-wheel-chassis`
- `wr-front-wheels` [consume] + `wr-front-bearing-chassis` [transform] -> `wr-front-rolling-chassis`
- `wr-rear-bearing` [consume] + `wr-front-bearing-chassis` [transform] -> `wr-bearing-chassis`
- `wr-front-wheels` [consume] + `wr-bearing-chassis` [transform] -> `wr-front-wheel-chassis`
- `wr-rear-wheels` [consume] + `wr-bearing-chassis` [transform] -> `wr-rear-wheel-chassis`
- `wr-front-wheels` [consume] + `wr-rear-wheel-chassis` [transform] -> `wr-rolling-chassis`
- `wr-rear-bearing` [consume] + `wr-front-rolling-chassis` [transform] -> `wr-front-wheel-chassis`
- `wr-rear-wheels` [consume] + `wr-front-wheel-chassis` [transform] -> `wr-rolling-chassis`
- `wr-rolling-chassis` [transform] @ `wr-flip` -> `wr-upright`
- `wr-sail` [consume] + `wr-upright` [transform] -> `wind-racer`

## `bf-pb-rails` A marble table
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pinball table](assets/items/pinball-table.webp)

**Goals**
- Fit the Left rail -- `bf-pb-rail-1`
- next: Fit the Right rail -- `bf-pb-rail-2`
- next: Fit the Top rail -- `bf-pb-rail-3`
- next: Fit the Lane rail -- `bf-pb-rail-4`
- next: Fit the Left return -- `bf-pb-rail-5`
- next: Fit the Right return -- `bf-pb-rail-6`
- next: Fit the Marble cup -- `bf-pb-rimmed`

**Items**
- `bf-pb-tray` Tray
  - icon: ![Tray](assets/items/bf-pb-tray.webp)

  {A long flat tan board with small holes, slots and a shallow notch across its nearer end.}

  ---

  Prepared plywood with rail slots, flipper holes and integral carrying handles.
- `bf-pb-left-rail` Left rail
  - icon: ![Left rail](assets/items/bf-pb-left-rail.webp)

  {A long straight green rail with small projecting feet along its lower edge.}
- `bf-pb-rail-1` Table
  - icon: ![Table](assets/items/bf-pb-rail-1.webp)

  {One straight green rail runs along the left side of the tan board.}
- `bf-pb-right-rail` Right rail
  - icon: ![Right rail](assets/items/bf-pb-right-rail.webp)

  {A long straight green rail with small projecting feet along its lower edge.}
- `bf-pb-rail-2` Table
  - icon: ![Table](assets/items/bf-pb-rail-2.webp)

  {Straight green rails run along both long sides of the tan board.}
- `bf-pb-top-rail` Top rail
  - icon: ![Top rail](assets/items/bf-pb-top-rail.webp)

  {A broad curved green rail with small feet beneath it.}
- `bf-pb-rail-3` Table
  - icon: ![Table](assets/items/bf-pb-rail-3.webp)

  {A curved green rail joins the two side rails around the far end of the tan board.}
- `bf-pb-lane` Lane rail
  - icon: ![Lane rail](assets/items/bf-pb-lane.webp)

  {A long thin green rail with a short bent tip and small feet underneath.}
- `bf-pb-rail-4` Table
  - icon: ![Table](assets/items/bf-pb-rail-4.webp)

  {A second narrow green rail forms a long lane inside the board’s right-hand edge.}
- `bf-pb-left-lip` Left return
  - icon: ![Left return](assets/items/bf-pb-left-lip.webp)

  {A short green rail bends through a broad curve, with small feet beneath it.}
- `bf-pb-rail-5` Table
  - icon: ![Table](assets/items/bf-pb-rail-5.webp)

  {The left rail curves inward near the front of the board.}
- `bf-pb-right-lip` Right return
  - icon: ![Right return](assets/items/bf-pb-right-lip.webp)

  {A short green rail has one angled end and small feet underneath.}
- `bf-pb-rail-6` Table
  - icon: ![Table](assets/items/bf-pb-rail-6.webp)

  {Both front rail ends turn inward, leaving a gap between them.}
- `bf-pb-cup` Marble cup
  - icon: ![Marble cup](assets/items/bf-pb-cup.webp)

  {A green shallow tray has raised edge rails and a round recessed cup near its centre.}
- `bf-pb-rimmed` Table
  - icon: ![Table](assets/items/bf-pb-rimmed.webp)

  {A small green tray and round cup extend from the gap at the front of the railed board.}

**Combinations**
- `bf-pb-left-rail` [consume] + `bf-pb-tray` [transform] -> `bf-pb-rail-1`
- `bf-pb-right-rail` [consume] + `bf-pb-rail-1` [transform] -> `bf-pb-rail-2`
- `bf-pb-top-rail` [consume] + `bf-pb-rail-2` [transform] -> `bf-pb-rail-3`
- `bf-pb-lane` [consume] + `bf-pb-rail-3` [transform] -> `bf-pb-rail-4`
- `bf-pb-left-lip` [consume] + `bf-pb-rail-4` [transform] -> `bf-pb-rail-5`
- `bf-pb-right-lip` [consume] + `bf-pb-rail-5` [transform] -> `bf-pb-rail-6`
- `bf-pb-cup` [consume] + `bf-pb-rail-6` [transform] -> `bf-pb-rimmed`


## `bf-pb-flippers` Two flippers
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pinball table](assets/items/pinball-table.webp)

**Goals**
- Flip the Table -- `bf-pb-under`
- next: Fit the Pivot plate -- `bf-pb-plated-under`
- next: Fit the Support -- `bf-pb-supported-under`
- next: Flip the Table upright -- `bf-pb-upright`
- next: Snap on the Left paddle -- `bf-pb-left`
- next: Snap on the Right paddle -- `bf-pb-flipped`

**Hotspots**
- `bf-pb-flip` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `bf-pb-rimmed` Table
  - icon: ![Table](assets/items/bf-pb-rimmed.webp)

  {A small green tray and round cup extend from the gap at the front of the railed board.}
- `bf-pb-flip` Flip
  - icon: ![Flip](assets/actions/flip.svg)
- `bf-pb-under` Table
  - icon: ![Table](assets/items/bf-pb-under.webp)

  {The underside of the tan board faces up, showing slots, small holes and two narrow wooden strips; the green cup projects behind its far edge.}
- `bf-pb-plate` Pivot plate
  - icon: ![Pivot plate](assets/items/bf-pb-plate.webp)

  {A flat green rectangular plate carries black upright pins and small red paddles at its sides.}

  ---

  A plate with retained spindles, finger buttons and return loops. The shoulders pass through the prepared tray clearances. Captive screws enter the tray’s threaded receivers from beneath.
- `bf-pb-plated-under` Table
  - icon: ![Table](assets/items/bf-pb-plated-under.webp)

  {A green rectangular plate with black pins and red side fittings lies across the exposed underside of the board.}
- `bf-pb-support` Support
  - icon: ![Support](assets/items/bf-pb-support.webp)

  {A tan U-shaped stand has two long slotted arms and a taller connecting back.}

  ---

  One connected U-shaped support with locating tongues and retaining clips. It slopes the table towards its marble cup without tilting sideways.
- `bf-pb-supported-under` Table
  - icon: ![Table](assets/items/bf-pb-supported-under.webp)

  {A tan U-shaped stand surrounds the underside of the board, beside the fitted green plate.}
- `bf-pb-upright` Table
  - icon: ![Table](assets/items/bf-pb-upright.webp)

  {The railed table stands upright on its tan support, with two exposed dark pivot pins near the front.}
- `bf-pb-left-paddle` Left paddle
  - icon: ![Left paddle](assets/items/bf-pb-left-paddle.webp)

  {A long flat red paddle narrows toward one end and has a socket near its broad rounded end.}

  ---

  One polymer paddle with an open keyed snap socket. Its flexible mouth clips sideways around the spindle neck between the retaining shoulders.
- `bf-pb-left` Table
  - icon: ![Table](assets/items/bf-pb-left.webp)

  {One red paddle sits on the left front pivot; the right pivot remains bare.}
- `bf-pb-right-paddle` Right paddle
  - icon: ![Right paddle](assets/items/bf-pb-right-paddle.webp)

  {A long flat red paddle narrows toward one end and has a socket near its broad rounded end.}

  ---

  One polymer paddle with an open keyed snap socket. Its flexible mouth clips sideways around the spindle neck between the retaining shoulders.
- `bf-pb-flipped` Table
  - icon: ![Table](assets/items/bf-pb-flipped.webp)

  {Two red paddles angle inward near the front gap of the railed table.}

**Combinations**
- `bf-pb-rimmed` [transform] @ `bf-pb-flip` -> `bf-pb-under`
- `bf-pb-plate` [consume] + `bf-pb-under` [transform] -> `bf-pb-plated-under`
- `bf-pb-support` [consume] + `bf-pb-plated-under` [transform] -> `bf-pb-supported-under`
- `bf-pb-supported-under` [transform] @ `bf-pb-flip` -> `bf-pb-upright`
- `bf-pb-left-paddle` [consume] + `bf-pb-upright` [transform] -> `bf-pb-left`
- `bf-pb-right-paddle` [consume] + `bf-pb-left` [transform] -> `bf-pb-flipped`


## `bf-pb-launcher-build` A spring launcher
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pinball table](assets/items/pinball-table.webp)

**Goals**
- Slide the Spring onto the Plunger rod -- `bf-pb-sprung-rod`
- next: Fit the Plunger tip -- `bf-pb-tipped`
- next: Lower the Plunger into the Launcher cradle -- `bf-pb-open-launcher`
- next: Clip on the Launcher cover -- `bf-pb-launcher`
- next: Fit the Launcher to the Table -- `bf-pb-launched`

**Items**
- `bf-pb-rod` Plunger rod
  - icon: ![Plunger rod](assets/items/bf-pb-rod.webp)

  {A long charcoal rod ends in a red crosspiece forming a T handle.}

  ---

  A six-millimetre plunger rod with a fitted pull handle and an open front end for threading the spring.
- `bf-pb-spring` Spring
  - icon: ![Spring](assets/items/bf-pb-spring.webp)

  {A thick black coil with open ends, lying diagonally.}
- `bf-pb-sprung-rod` Plunger
  - icon: ![Plunger](assets/items/bf-pb-sprung-rod.webp)

  {A black coil surrounds the far end of the charcoal rod; its red T handle remains exposed.}
- `bf-pb-tip` Plunger tip
  - icon: ![Plunger tip](assets/items/bf-pb-tip.webp)

  {A stepped red round cap with a central round hole.}

  ---

  A soft striking tip and piston with a blind gripping socket for the rod.
- `bf-pb-tipped` Plunger
  - icon: ![Plunger](assets/items/bf-pb-tipped.webp)

  {A red round cap sits beyond the coil at the far end of the charcoal rod and T handle.}
- `bf-pb-barrel` Launcher cradle
  - icon: ![Launcher cradle](assets/items/bf-pb-barrel.webp)

  {An open grey half-tube sits at one end of a long green rail, with a red upright fitting at the other end.}

  ---

  An open-topped cradle with half-round end guides, mounting feet and a travel stop. The assembled plunger lowers through its open top.
- `bf-pb-open-launcher` Launcher
  - icon: ![Launcher](assets/items/bf-pb-open-launcher.webp)

  {The coil and capped rod lie inside the open grey half-tube on the green rail; the T handle extends from the front.}
- `bf-pb-cover` Launcher cover
  - icon: ![Launcher cover](assets/items/bf-pb-cover.webp)

  {A grey half-cylinder has black end rims and green clips hanging from its sides.}

  ---

  A clear upper shell with matching half-guides and flexible retaining clips. Closing it captures the plunger and encloses the spring.
- `bf-pb-launcher` Launcher
  - icon: ![Launcher](assets/items/bf-pb-launcher.webp)

  {A grey cylindrical cover surrounds the coil, with green side clips; the charcoal rod and red T handle extend from its front.}
- `bf-pb-flipped` Table
  - icon: ![Table](assets/items/bf-pb-flipped.webp)

  {Two red paddles angle inward near the front gap of the railed table.}
- `bf-pb-launched` Table
  - icon: ![Table](assets/items/bf-pb-launched.webp)

  {The covered launcher sits beside the table’s right-hand lane, with its red T handle projecting from the front.}

**Combinations**
- `bf-pb-spring` [consume] + `bf-pb-rod` [transform] -> `bf-pb-sprung-rod`
- `bf-pb-tip` [consume] + `bf-pb-sprung-rod` [transform] -> `bf-pb-tipped`
- `bf-pb-barrel` [consume] + `bf-pb-tipped` [transform] -> `bf-pb-open-launcher`
- `bf-pb-cover` [consume] + `bf-pb-open-launcher` [transform] -> `bf-pb-launcher`
- `bf-pb-launcher` [consume] + `bf-pb-flipped` [transform] -> `bf-pb-launched`


## `bf-pb-targets` One more go
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pinball table](assets/items/pinball-table.webp)

**Goals**
- Fit the Lower arch -- `bf-pb-target-1`
- next: Fit the Middle arch -- `bf-pb-target-2`
- next: Fit the Upper arch -- `bf-pb-target-3`
- next: Fit the Score wheel -- `bf-pb-scored`
- next: Put the Marble in its cup -- `pinball-table`

**Items**
- `bf-pb-launched` Table
  - icon: ![Table](assets/items/bf-pb-launched.webp)

  {The covered launcher sits beside the table’s right-hand lane, with its red T handle projecting from the front.}
- `bf-pb-arch-low` Lower arch
  - icon: ![Lower arch](assets/items/bf-pb-arch-low.webp)

  {A green rectangular arch with one red dot on its top bar and round pegs below its two legs.}
- `bf-pb-target-1` Table
  - icon: ![Table](assets/items/bf-pb-target-1.webp)

  {One small green arch stands on the board above the two red paddles.}
- `bf-pb-arch-mid` Middle arch
  - icon: ![Middle arch](assets/items/bf-pb-arch-mid.webp)

  {A green rectangular arch with two red dots on its top bar and round pegs below its two legs.}
- `bf-pb-target-2` Table
  - icon: ![Table](assets/items/bf-pb-target-2.webp)

  {Two small green arches stand at different positions on the board above the red paddles.}
- `bf-pb-arch-high` Upper arch
  - icon: ![Upper arch](assets/items/bf-pb-arch-high.webp)

  {A green rectangular arch with three red dots on its top bar and round pegs below its two legs.}
- `bf-pb-target-3` Table
  - icon: ![Table](assets/items/bf-pb-target-3.webp)

  {Three small green arches stand in a staggered line along the board.}
- `bf-pb-score` Score wheel
  - icon: ![Score wheel](assets/items/bf-pb-score.webp)

  {A red wheel sits on a green support above a tan rail with green clips underneath.}
- `bf-pb-scored` Table
  - icon: ![Table](assets/items/bf-pb-scored.webp)

  {A red wheel on a tan rail rises outside the table’s left edge, beside the three green arches.}
- `bf-pb-marble` Marble
  - icon: ![Marble](assets/items/bf-pb-marble.webp)

  {One red ball.}
- `pinball-table` Pinball table
  - icon: ![Pinball table](assets/items/pinball-table.webp)

  {The railed table has two red paddles, three green arches, a side launcher and red wheel. A small red ball sits in the green cup at the front.}

**Combinations**
- `bf-pb-arch-low` [consume] + `bf-pb-launched` [transform] -> `bf-pb-target-1`
- `bf-pb-arch-mid` [consume] + `bf-pb-target-1` [transform] -> `bf-pb-target-2`
- `bf-pb-arch-high` [consume] + `bf-pb-target-2` [transform] -> `bf-pb-target-3`
- `bf-pb-score` [consume] + `bf-pb-target-3` [transform] -> `bf-pb-scored`
- `bf-pb-marble` [consume] + `bf-pb-scored` [transform] -> `pinball-table`

## `bf-cd-crank` Round and round
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Crank dragon](assets/items/crank-dragon.webp)

**Goals**
- Slide the Cam onto the Shaft -- `bf-cd-cammed`
- next: Fit the Front bearing -- `bf-cd-bearing-1`
- next: Fit the Rear bearing -- `bf-cd-bearings`
- next: Fit the Front collar -- `bf-cd-front-retained`
- next: Flip to the back of the bearings -- `bf-cd-rear-facing`
- next: Fit the Rear collar -- `bf-cd-retained-rear`
- next: Flip back to the front -- `bf-cd-retained`
- next: Fit the Crank -- `bf-cd-cranked`
- next: Secure the Crank with its clip -- `bf-cd-clipped`
- next: Mount the bearings on the Base -- `bf-cd-frame`

**Hotspots**
- `bf-cd-flip` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `bf-cd-shaft` Shaft
  - icon: ![Shaft](assets/items/bf-cd-shaft.webp)

  {A long thin charcoal rod lying diagonally.}

  ---

  A plain six-millimetre shaft, supplied without its collars. The cam and bearings slide on before the separate collars retain the shaft.
- `bf-cd-cam` Cam
  - icon: ![Cam](assets/items/bf-cd-cam.webp)

  {A red circular disc with a short split socket below the centre of its face.}

  ---

  The shaft hole sits off centre. Turning the round disc raises and lowers the broad follower foot.
- `bf-cd-cammed` Frame
  - icon: ![Frame](assets/items/bf-cd-cammed.webp)

  {A charcoal shaft passes through the off-centre socket of a red disc.}
- `bf-cd-front-bearing` Front bearing
  - icon: ![Front bearing](assets/items/bf-cd-front-bearing.webp)

  {A green rectangular frame with two legs, a round hole through its top bar and two black pins beneath its foot.}
- `bf-cd-bearing-1` Frame
  - icon: ![Frame](assets/items/bf-cd-bearing-1.webp)

  {The charcoal shaft passes through one green frame in front of the red disc.}
- `bf-cd-rear-bearing` Rear bearing
  - icon: ![Rear bearing](assets/items/bf-cd-rear-bearing.webp)

  {A green rectangular frame with two legs, a round hole through its top bar and two black pins beneath its foot.}
- `bf-cd-bearings` Frame
  - icon: ![Frame](assets/items/bf-cd-bearings.webp)

  {A red disc sits on a charcoal shaft between two green frames; the near end of the shaft is bare.}
- `bf-cd-front-collar` Front collar
  - icon: ![Front collar](assets/items/bf-cd-front-collar.webp)

  {A thick green ring with a split side and small holes around its rim.}
- `bf-cd-front-retained` Frame
  - icon: ![Frame](assets/items/bf-cd-front-retained.webp)

  {A green ring surrounds the shaft just outside the nearer green frame. The red disc sits between the two frames.}
- `bf-cd-flip` Flip
  - icon: ![Flip](assets/actions/flip.svg)
- `bf-cd-rear-facing` Frame
  - icon: ![Frame](assets/items/bf-cd-rear-facing.webp)

  {From the other side, the plain back of the red disc faces us between two green frames. A bare charcoal shaft projects from the nearer frame.}
- `bf-cd-rear-collar` Rear collar
  - icon: ![Rear collar](assets/items/bf-cd-rear-collar.webp)

  {A thick green ring with a split side and small holes around its rim.}
- `bf-cd-retained-rear` Frame
  - icon: ![Frame](assets/items/bf-cd-retained-rear.webp)

  {From the back, a green ring now surrounds the projecting shaft beside the nearer frame.}
- `bf-cd-retained` Frame
  - icon: ![Frame](assets/items/bf-cd-retained.webp)

  {From the front again, a red disc sits between two green frames. A green ring surrounds the exposed front shaft.}
- `bf-cd-handle` Crank
  - icon: ![Crank](assets/items/bf-cd-handle.webp)

  {A green cylindrical grip attached to a short red arm.}

  ---

  A D-shaped socket fits the matching shaft end. Its separate retaining clip enters the aligned cross holes after the crank is fitted.
- `bf-cd-cranked` Frame
  - icon: ![Frame](assets/items/bf-cd-cranked.webp)

  {A green cylindrical grip and short red arm extend from the front of the two green frames and red disc.}
- `bf-cd-crank-clip` Crank clip
  - icon: ![Crank clip](assets/items/bf-cd-crank-clip.webp)

  {One thin black wire bent into a narrow open loop with two unequal ends.}

  ---

  One spring-wire clip. Its straight leg passes through the aligned crank and shaft holes; the curved leg grips outside the socket.
- `bf-cd-clipped` Frame
  - icon: ![Frame](assets/items/bf-cd-clipped.webp)

  {The green grip and red arm remain on the shaft; a small dark wire loop is visible beside the red socket.}
- `bf-cd-base` Base
  - icon: ![Base](assets/items/bf-cd-base.webp)

  {A flat tan rectangular board with small round holes.}
- `bf-cd-frame` Frame
  - icon: ![Frame](assets/items/bf-cd-frame.webp)

  {Two green frames hold a red disc and green crank above a broad tan board.}

**Combinations**
- `bf-cd-cam` [consume] + `bf-cd-shaft` [transform] -> `bf-cd-cammed`
- `bf-cd-front-bearing` [consume] + `bf-cd-cammed` [transform] -> `bf-cd-bearing-1`
- `bf-cd-rear-bearing` [consume] + `bf-cd-bearing-1` [transform] -> `bf-cd-bearings`
- `bf-cd-front-collar` [consume] + `bf-cd-bearings` [transform] -> `bf-cd-front-retained`
- `bf-cd-front-retained` [transform] @ `bf-cd-flip` -> `bf-cd-rear-facing`
- `bf-cd-rear-collar` [consume] + `bf-cd-rear-facing` [transform] -> `bf-cd-retained-rear`
- `bf-cd-retained-rear` [transform] @ `bf-cd-flip` -> `bf-cd-retained`
- `bf-cd-handle` [consume] + `bf-cd-retained` [transform] -> `bf-cd-cranked`
- `bf-cd-crank-clip` [consume] + `bf-cd-cranked` [transform] -> `bf-cd-clipped`
- `bf-cd-base` [consume] + `bf-cd-clipped` [transform] -> `bf-cd-frame`


## `bf-cd-lift` Round becomes up
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Crank dragon](assets/items/crank-dragon.webp)

**Goals**
- Slide the Follower into the Guide -- `bf-cd-open-follower`
- next: Snap on the Cover -- `bf-cd-guided`
- next: Mount the Follower above the Cam -- `bf-cd-mounted`
- next: Hook on the Spring -- `bf-cd-lifter`

**Items**
- `bf-cd-guide` Guide
  - icon: ![Guide](assets/items/bf-cd-guide.webp)

  {A tall tan post on a small foot, with an open green frame at the top.}

  ---

  An open square channel with a mounting foot and spring anchor. The separate cover closes around the follower; its broad foot never has to pass through the narrow channel.
- `bf-cd-follower` Follower
  - icon: ![Follower](assets/items/bf-cd-follower.webp)

  {A thin red upright with a broad flat foot, a small crosspiece near its top and a black pin across its upper end.}

  ---

  A sliding rod with a broad cam foot, spring collar and retained crosshead pin for two independently pivoting links.
- `bf-cd-open-follower` Follower
  - icon: ![Follower](assets/items/bf-cd-open-follower.webp)

  {A red upright runs beside a tall tan post, through an open green frame; its broad red foot projects sideways.}
- `bf-cd-cover` Cover
  - icon: ![Cover](assets/items/bf-cd-cover.webp)

  {A flat green rectangular plate with short projecting tabs behind it.}
- `bf-cd-guided` Follower
  - icon: ![Follower](assets/items/bf-cd-guided.webp)

  {A green plate closes the front of the frame around the red upright on the tan post.}
- `bf-cd-frame` Frame
  - icon: ![Frame](assets/items/bf-cd-frame.webp)

  {Two green frames hold a red disc and green crank above a broad tan board.}
- `bf-cd-mounted` Lifter
  - icon: ![Lifter](assets/items/bf-cd-mounted.webp)

  {The tan post rises behind the red disc, with the broad red foot just above the disc and a cross-pin at the top.}
- `bf-cd-spring` Spring
  - icon: ![Spring](assets/items/bf-cd-spring.webp)

  {A black coil with an open curved hook at each end.}
- `bf-cd-lifter` Lifter
  - icon: ![Lifter](assets/items/bf-cd-lifter.webp)

  {A thin black coil runs beside the red upright between its upper crosspiece and the green guide frame.}

**Combinations**
- `bf-cd-follower` [consume] + `bf-cd-guide` [transform] -> `bf-cd-open-follower`
- `bf-cd-cover` [consume] + `bf-cd-open-follower` [transform] -> `bf-cd-guided`
- `bf-cd-guided` [consume] + `bf-cd-frame` [transform] -> `bf-cd-mounted`
- `bf-cd-spring` [consume] + `bf-cd-mounted` [transform] -> `bf-cd-lifter`


## `bf-cd-dragon` The dragon
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Crank dragon](assets/items/crank-dragon.webp)

**Goals**
- Attach the Left wing -- `bf-cd-body-left`
- next: Attach the Right wing -- `bf-cd-winged`
- next: Attach the Tail -- `bf-cd-bodied`
- next: Mount the Dragon on the Lifter -- `bf-cd-mounted-body`
- next: Fit the Left link -- `bf-cd-linked-left`
- next: Fit the Right link -- `crank-dragon`

**Items**
- `bf-cd-body` Body
  - icon: ![Body](assets/items/bf-cd-body.webp)

  {A flat green dragon with a smiling face, red neck spikes and two long legs ending in small feet.}
- `bf-cd-left-wing` Left wing
  - icon: ![Left wing](assets/items/bf-cd-left-wing.webp)

  {A pointed red wing with dark ribs and a short tan peg across its lower end.}

  ---

  One card wing with a prepared split snap pin and spacer. The two tapered tips compress through the body hole and reopen behind it.
- `bf-cd-body-left` Body
  - icon: ![Body](assets/items/bf-cd-body-left.webp)

  {The flat green dragon has one raised red wing; its other shoulder remains bare.}
- `bf-cd-right-wing` Right wing
  - icon: ![Right wing](assets/items/bf-cd-right-wing.webp)

  {A pointed red wing with dark ribs and a short tan peg across its lower end.}

  ---

  One card wing with a prepared split snap pin and spacer. The two tapered tips compress through the body hole and reopen behind it.
- `bf-cd-winged` Body
  - icon: ![Body](assets/items/bf-cd-winged.webp)

  {Two pointed red wings rise from the green dragon’s shoulders.}
- `bf-cd-tail` Tail
  - icon: ![Tail](assets/items/bf-cd-tail.webp)

  {A flat green tail with an upturned tip and a small round fitting at its other end.}

  ---

  The tail carries a split snap pin. Its tapered tip passes through the body hole before its flexible barbs reopen.
- `bf-cd-bodied` Dragon
  - icon: ![Dragon](assets/items/bf-cd-bodied.webp)

  {The green dragon has two raised red wings and an upturned green tail.}
- `bf-cd-lifter` Lifter
  - icon: ![Lifter](assets/items/bf-cd-lifter.webp)

  {A thin black coil runs beside the red upright between its upper crosspiece and the green guide frame.}
- `bf-cd-mounted-body` Dragon
  - icon: ![Dragon](assets/items/bf-cd-mounted-body.webp)

  {The green dragon stands on the tan board around the upright mechanism and red disc. Its two wings have bare lower pins.}
- `bf-cd-left-link` Left link
  - icon: ![Left link](assets/items/bf-cd-left-link.webp)

  {A narrow green bar with an open circular eye at each end.}

  ---

  One rigid 55 mm polymer link with two open snap eyes. Fit both eyes sideways over the exposed pin necks; their heads stay in place.
- `bf-cd-linked-left` Dragon
  - icon: ![Dragon](assets/items/bf-cd-linked-left.webp)

  {One green bar runs from the left wing’s lower pin to the central red upright; the right wing’s lower pin remains bare.}
- `bf-cd-right-link` Right link
  - icon: ![Right link](assets/items/bf-cd-right-link.webp)

  {A narrow green bar with an open circular eye at each end.}

  ---

  One rigid 55 mm polymer link with two open snap eyes. It pivots independently beside the other link.
- `crank-dragon` Crank dragon
  - icon: ![Crank dragon](assets/items/crank-dragon.webp)

  {The green dragon stands above a red disc and green crank on a tan board. Two short green bars connect its red wings to the central upright.}

**Combinations**
- `bf-cd-left-wing` [consume] + `bf-cd-body` [transform] -> `bf-cd-body-left`
- `bf-cd-right-wing` [consume] + `bf-cd-body-left` [transform] -> `bf-cd-winged`
- `bf-cd-tail` [consume] + `bf-cd-winged` [transform] -> `bf-cd-bodied`
- `bf-cd-bodied` [consume] + `bf-cd-lifter` [transform] -> `bf-cd-mounted-body`
- `bf-cd-left-link` [consume] + `bf-cd-mounted-body` [transform] -> `bf-cd-linked-left`
- `bf-cd-right-link` [consume] + `bf-cd-linked-left` [transform] -> `crank-dragon`

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

  {A flat tan sheet divided into four long panels, with square openings and longer end flaps.}

  ---

  One scored card net with dark inner faces, two end flaps, mirror ledges and prepared adhesive seam tabs. The end flaps stay open while you fit the mirrors.
- `bf-pe-fold` Fold
  - icon: ![Fold](assets/actions/fold.svg)
- `bf-pe-fold-1` Tube
  - icon: ![Tube](assets/items/bf-pe-fold-1.webp)

  {One long side panel of the tan sheet folds away from the others; the lower square opening remains visible.}
- `bf-pe-fold-2` Tube
  - icon: ![Tube](assets/items/bf-pe-fold-2.webp)

  {The folded tan panels surround a dark narrow channel, with a long open side and projecting end flaps.}
- `bf-pe-tube` Tube
  - icon: ![Tube](assets/items/bf-pe-tube.webp)

  {A tall tan square tube with a dark lower opening and flat flaps projecting above and below.}
- `bf-pe-flip` Flip
  - icon: ![Flip](assets/actions/flip.svg)
- `bf-pe-rear` Tube
  - icon: ![Tube](assets/items/bf-pe-rear.webp)

  {The other face of the tan tube has its dark square opening at the upper end. Its top flap still stands upright.}
- `bf-pe-upper` Upper mirror
  - icon: ![Upper mirror](assets/items/bf-pe-upper.webp)

  {A silver rectangular plate held along two opposite edges by green strips.}

  ---

  An unbreakable mirror with retained edge clips. It seats on the upper forty-five-degree ledges.
- `bf-pe-upper-fit` Tube
  - icon: ![Tube](assets/items/bf-pe-upper-fit.webp)

  {A pale angled edge and green side strips appear inside the upper opening; the top flap still stands upright.}
- `bf-pe-top-closed` Tube
  - icon: ![Tube](assets/items/bf-pe-top-closed.webp)

  {The top of the tan tube is now closed flat above the dark upper opening.}
- `bf-pe-top-shade` Top shade
  - icon: ![Top shade](assets/items/bf-pe-top-shade.webp)

  {A thick black square frame with a stepped edge around its open centre.}

  ---

  One stepped window hood. Its narrow neck enters the opening while its prepared adhesive flange rests on the card outside.
- `bf-pe-shaded` Tube
  - icon: ![Tube](assets/items/bf-pe-shaded.webp)

  {A thick black square rim projects around the upper opening of the tan tube.}
- `bf-pe-front` Tube
  - icon: ![Tube](assets/items/bf-pe-front.webp)

  {The tan tube is turned to its lower opening again. A black rim peeks from behind the top, and the bottom flap hangs down.}
- `bf-pe-lower` Lower mirror
  - icon: ![Lower mirror](assets/items/bf-pe-lower.webp)

  {A silver rectangular plate held along two opposite edges by green strips.}

  ---

  A matching mirror in retained clips. Its reflecting face remains parallel to the upper mirror, redirecting the light towards your eye.
- `bf-pe-mirrored` Tube
  - icon: ![Tube](assets/items/bf-pe-mirrored.webp)

  {A bright angled plate fills the lower opening, with a green strip along its side; the bottom flap still hangs down.}
- `bf-pe-closed` Tube
  - icon: ![Tube](assets/items/bf-pe-closed.webp)

  {The bottom flap is folded flat beneath the bright angled plate in the lower opening.}
- `bf-pe-eye-shade` Eye shade
  - icon: ![Eye shade](assets/items/bf-pe-eye-shade.webp)

  {A thick black square frame with a stepped edge around its open centre.}

  ---

  A matching stepped hood for the lower window, with prepared adhesive on its outer flange.
- `periscope` Periscope
  - icon: ![Periscope](assets/items/periscope.webp)

  {A tall tan square tube has a black rim around its lower silver opening, with a small black edge peeking out behind its upper end.}

**Combinations**
- `bf-pe-net` [transform] @ `bf-pe-fold` -> `bf-pe-fold-1`
- `bf-pe-fold-1` [transform] @ `bf-pe-fold` -> `bf-pe-fold-2`
- `bf-pe-fold-2` [transform] @ `bf-pe-fold` -> `bf-pe-tube`
- `bf-pe-tube` [transform] @ `bf-pe-flip` -> `bf-pe-rear`
- `bf-pe-upper` [consume] + `bf-pe-rear` [transform] -> `bf-pe-upper-fit`
- `bf-pe-upper-fit` [transform] @ `bf-pe-fold` -> `bf-pe-top-closed`
- `bf-pe-top-shade` [consume] + `bf-pe-top-closed` [transform] -> `bf-pe-shaded`
- `bf-pe-shaded` [transform] @ `bf-pe-flip` -> `bf-pe-front`
- `bf-pe-lower` [consume] + `bf-pe-front` [transform] -> `bf-pe-mirrored`
- `bf-pe-mirrored` [transform] @ `bf-pe-fold` -> `bf-pe-closed`
- `bf-pe-eye-shade` [consume] + `bf-pe-closed` [transform] -> `periscope`

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

  {A flat tan rectangular sheet.}

  ---

  One continuous scored binding sheet. Its three adhesive panels hold the mirror backs; the flexible seams become hinges.
- `bf-ka-mirror-1` Mirror
  - icon: ![Mirror](assets/items/bf-ka-mirror-1.webp)

  {One long thin silver rectangular strip.}
- `bf-ka-mirrors-1` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-mirrors-1.webp)

  {One silver strip covers the left part of the tan backing; the rest is bare.}
- `bf-ka-mirror-2` Mirror
  - icon: ![Mirror](assets/items/bf-ka-mirror-2.webp)

  {One long thin silver rectangular strip.}
- `bf-ka-mirrors-2` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-mirrors-2.webp)

  {Two silver strips lie side by side on the tan backing, with a bare tan panel at the right.}
- `bf-ka-mirror-3` Mirror
  - icon: ![Mirror](assets/items/bf-ka-mirror-3.webp)

  {One long thin silver rectangular strip.}
- `bf-ka-mirrors-3` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-mirrors-3.webp)

  {Three silver strips cover the tan backing, separated by narrow tan lines.}
- `bf-ka-fold` Fold
  - icon: ![Fold](assets/actions/fold.svg)
- `bf-ka-prism` Mirror triangle
  - icon: ![Mirror triangle](assets/items/bf-ka-prism.webp)

  {The tan sheet forms a long triangular tube with a triangular opening at its nearer end.}
- `bf-ka-tube` Viewing tube
  - icon: ![Viewing tube](assets/items/bf-ka-tube.webp)

  {A tan cylindrical tube with a green rim around its open nearer end.}

  ---

  A prepared protective tube with a dark eyecap, padded mirror supports and a retained turning collar.
- `bf-ka-viewer` Viewing tube
  - icon: ![Viewing tube](assets/items/bf-ka-viewer.webp)

  {A triangular opening is visible inside the green-rimmed end of the tan tube.}
- `bf-ka-only-2` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-only-2.webp)

  {One silver strip runs down the middle of the tan backing, with bare tan panels on both sides.}
- `bf-ka-only-3` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-only-3.webp)

  {One silver strip covers the right part of the tan backing; the left two panels are bare.}
- `bf-ka-pair-13` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-pair-13.webp)

  {Two silver strips flank one bare tan panel in the middle of the backing.}
- `bf-ka-pair-23` Mirrors
  - icon: ![Mirrors](assets/items/bf-ka-pair-23.webp)

  {Two silver strips cover the middle and right panels of the backing; the left panel is bare.}

**Combinations**
- `bf-ka-mirror-1` [consume] + `bf-ka-backing` [transform] -> `bf-ka-mirrors-1`
- `bf-ka-mirror-2` [consume] + `bf-ka-mirrors-1` [transform] -> `bf-ka-mirrors-2`
- `bf-ka-mirror-3` [consume] + `bf-ka-mirrors-2` [transform] -> `bf-ka-mirrors-3`
- `bf-ka-mirrors-3` [transform] @ `bf-ka-fold` -> `bf-ka-prism`
- `bf-ka-tube` [consume] + `bf-ka-prism` [transform] -> `bf-ka-viewer`
- `bf-ka-mirror-2` [consume] + `bf-ka-backing` [transform] -> `bf-ka-only-2`
- `bf-ka-mirror-3` [consume] + `bf-ka-backing` [transform] -> `bf-ka-only-3`
- `bf-ka-mirror-3` [consume] + `bf-ka-mirrors-1` [transform] -> `bf-ka-pair-13`
- `bf-ka-mirror-1` [consume] + `bf-ka-only-2` [transform] -> `bf-ka-mirrors-2`
- `bf-ka-mirror-3` [consume] + `bf-ka-only-2` [transform] -> `bf-ka-pair-23`
- `bf-ka-mirror-1` [consume] + `bf-ka-only-3` [transform] -> `bf-ka-pair-13`
- `bf-ka-mirror-2` [consume] + `bf-ka-only-3` [transform] -> `bf-ka-pair-23`
- `bf-ka-mirror-2` [consume] + `bf-ka-pair-13` [transform] -> `bf-ka-mirrors-3`
- `bf-ka-mirror-1` [consume] + `bf-ka-pair-23` [transform] -> `bf-ka-mirrors-3`


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

  {A broad red circular rim around a dark grey bottom.}

  ---

  A connected clear-bottomed cell with a rotating collar fitting. Its separate snap lid leaves space for the coloured pieces to tumble.
- `bf-ka-triangle` Triangle
  - icon: ![Triangle](assets/items/bf-ka-triangle.webp)

  {One thick green triangle.}
- `bf-ka-colour-1` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-colour-1.webp)

  {One small green triangle lies inside the red-rimmed round cell.}
- `bf-ka-crescent` Crescent
  - icon: ![Crescent](assets/items/bf-ka-crescent.webp)

  {One thick yellow crescent.}
- `bf-ka-colour-2` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-colour-2.webp)

  {A green triangle and yellow crescent lie inside the red-rimmed round cell.}
- `bf-ka-disc` Disc
  - icon: ![Disc](assets/items/bf-ka-disc.webp)

  {One thick blue disc.}
- `bf-ka-colour-3` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-colour-3.webp)

  {A green triangle, yellow crescent and blue disc lie inside the red-rimmed round cell.}
- `bf-ka-lid` Clear lid
  - icon: ![Clear lid](assets/items/bf-ka-lid.webp)

  {A grey circular plate with three small red tabs around its edge.}
- `bf-ka-lidded` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-lidded.webp)

  {The three coloured shapes appear faintly beneath a grey circular lid with three small red edge tabs.}
- `bf-ka-diffuser` Light cover
  - icon: ![Light cover](assets/items/bf-ka-diffuser.webp)

  {A pale round plate with a cream edge.}
- `bf-ka-covered` Colour cell
  - icon: ![Colour cell](assets/items/bf-ka-covered.webp)

  {A pale circular cover fills the front of the red-rimmed cell.}
- `bf-ka-viewer` Viewing tube
  - icon: ![Viewing tube](assets/items/bf-ka-viewer.webp)

  {A triangular opening is visible inside the green-rimmed end of the tan tube.}
- `kaleidoscope` Kaleidoscope
  - icon: ![Kaleidoscope](assets/items/kaleidoscope.webp)

  {A long tan tube ends in green and red rings around a pale circular cover.}

**Combinations**
- `bf-ka-triangle` [consume] + `bf-ka-cell` [transform] -> `bf-ka-colour-1`
- `bf-ka-crescent` [consume] + `bf-ka-colour-1` [transform] -> `bf-ka-colour-2`
- `bf-ka-disc` [consume] + `bf-ka-colour-2` [transform] -> `bf-ka-colour-3`
- `bf-ka-lid` [consume] + `bf-ka-colour-3` [transform] -> `bf-ka-lidded`
- `bf-ka-diffuser` [consume] + `bf-ka-lidded` [transform] -> `bf-ka-covered`
- `bf-ka-covered` [consume] + `bf-ka-viewer` [transform] -> `kaleidoscope`

## `c-gantry-frame` A lifting frame
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Gantry](assets/items/gh-mounted.webp)

**Goals**
- Fit a side frame -- `gh-one-side`
- next: Fit the other side frame -- `gh-two-sides`
- next: Join the frames with the beam -- `gh-frame`
- next: Fit the ratchet to the winch
  - either: `gh-ratchet-winch`
  - or: `gh-winch`
- next: Fit the crank -- `gh-winch`
- next: Mount the winch -- `gh-mounted`

**Items**
- `gh-base` Base
  - icon: ![Base](assets/items/gh-base.webp)

  {A flat tan rectangular board with small round holes.}
- `gh-side-1` Side frame
  - icon: ![Side frame](assets/items/gh-side-1.webp)

  {A tall triangular tan frame with a crossbar near its feet and short black pins projecting from its corners.}

  ---

  A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.

- `gh-side-2` Side frame
  - icon: ![Side frame](assets/items/gh-side-2.webp)

  {A tall triangular tan frame with a crossbar near its feet and short black pins projecting from its corners.}

  ---

  A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.

- `gh-crossbeam` Beam
  - icon: ![Beam](assets/items/gh-crossbeam.webp)

  {A long square tan beam with small round holes along one face.}

  ---

  The beam has two end sockets and separate sockets underneath for the pulley forks.

- `gh-one-side` Frame
  - icon: ![Frame](assets/items/gh-one-side.webp)

  {One triangular tan frame stands at the left end of the rectangular base.}
- `gh-two-sides` Frame
  - icon: ![Frame](assets/items/gh-two-sides.webp)

  {Two triangular tan frames stand at opposite ends of the rectangular base; their tops are unjoined.}
- `gh-frame` Frame
  - icon: ![Frame](assets/items/gh-frame.webp)

  {A long tan beam joins the tops of the two triangular frames above the rectangular base.}
- `gh-drum` Winch
  - icon: ![Winch](assets/items/gh-drum.webp)

  {A tan spool with red end discs sits in a green stand, with black square-ended shafts projecting from both sides.}

  ---

  The winch drum comes with its axle, two bearing cheeks, captive base fasteners and a sprung cord clamp.

- `gh-ratchet` Ratchet
  - icon: ![Ratchet](assets/items/gh-ratchet.webp)

  {A red toothed disc with a square centre hole.}
- `gh-crank` Crank
  - icon: ![Crank](assets/items/gh-crank.webp)

  {A straight red arm with a square hole near one end and a green cylindrical grip at the other.}
- `gh-ratchet-winch` Winch
  - icon: ![Winch](assets/items/gh-ratchet-winch.webp)

  {A red toothed disc sits outside the near green support of the tan spool.}
- `gh-crank-winch` Winch
  - icon: ![Winch](assets/items/gh-crank-winch.webp)

  {A tall red arm and green grip rise behind the tan spool; the nearer shaft remains bare.}
- `gh-winch` Winch
  - icon: ![Winch](assets/items/gh-winch.webp)

  {The tan spool has a red toothed disc on its near side and a tall red crank with green grip behind it.}
- `gh-mounted` Gantry
  - icon: ![Gantry](assets/items/gh-mounted.webp)

  {The red-and-green winch sits on the left side of the broad tan frame’s base.}

**Combinations**
- `gh-side-1` [consume] + `gh-base` [transform] -> `gh-one-side`
- `gh-side-2` [consume] + `gh-base` [transform] -> `gh-one-side`
- `gh-side-1` [consume] + `gh-one-side` [transform] -> `gh-two-sides`
- `gh-side-2` [consume] + `gh-one-side` [transform] -> `gh-two-sides`
- `gh-crossbeam` [consume] + `gh-two-sides` [transform] -> `gh-frame`
- `gh-ratchet` [consume] + `gh-drum` [transform] -> `gh-ratchet-winch`
- `gh-crank` [consume] + `gh-drum` [transform] -> `gh-crank-winch`
- `gh-crank` [consume] + `gh-ratchet-winch` [transform] -> `gh-winch`
- `gh-ratchet` [consume] + `gh-crank-winch` [transform] -> `gh-winch`
- `gh-winch` [consume] + `gh-frame` [transform] -> `gh-mounted`

## `c-gantry-rope` Over the beam
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Gantry hoist](assets/items/gantry-hoist.webp)

**Goals**
- Fit a pulley into the side fork -- `gh-side-pulley`
- next: Fit the other pulley into its fork -- `gh-drop-pulley`
- next: Mount the side pulley
  - either: `gh-fitted-1`
  - or: `gh-fitted-3`
  - or: `gh-fitted-5`
  - or: `gh-fitted-7`
- next: Mount the drop pulley
  - either: `gh-fitted-2`
  - or: `gh-fitted-3`
  - or: `gh-fitted-6`
  - or: `gh-fitted-7`
- next: Fit the pawl
  - either: `gh-fitted-4`
  - or: `gh-fitted-5`
  - or: `gh-fitted-6`
  - or: `gh-fitted-7`
- next: Thread the rope over both pulleys -- `gh-roped`
- next: Hang the basket on the hook -- `gantry-hoist`

**Items**
- `gh-side-fork` Side fork
  - icon: ![Side fork](assets/items/gh-side-fork.webp)

  {A green right-angled bracket has a short horizontal green pin and a long black split pin above.}

  ---

  An open pulley bracket with a split snap axle and a barbed mounting stem. Press a pulley over the axle tip, then push the stem through the beam until its head opens above the wood.

- `gh-side-pulley` Pulley unit
  - icon: ![Pulley unit](assets/items/gh-side-pulley.webp)

  {A red grooved wheel sits on the green bracket’s horizontal pin, below its long black top pin.}
- `gh-drop-fork` Drop fork
  - icon: ![Drop fork](assets/items/gh-drop-fork.webp)

  {A green right-angled bracket has a short horizontal green pin and a long black split pin above.}

  ---

  An open pulley bracket with a split snap axle and a barbed mounting stem. Press a pulley over the axle tip, then push the stem through the beam until its head opens above the wood.

- `gh-drop-pulley` Pulley unit
  - icon: ![Pulley unit](assets/items/gh-drop-pulley.webp)

  {A red grooved wheel sits on the green bracket’s horizontal pin, below its long black top pin.}
- `gh-pulley-1` Pulley
  - icon: ![Pulley](assets/items/gh-pulley-1.webp)

  {A thick red wheel with a groove around its rim and a round centre hole.}

  ---

  A grooved pulley that turns on either fork axle. The split axle tip retains it.

- `gh-pulley-2` Pulley
  - icon: ![Pulley](assets/items/gh-pulley-2.webp)

  {A thick red wheel with a groove around its rim and a round centre hole.}

  ---

  A grooved pulley that turns on either fork axle. The split axle tip retains it.

- `gh-pawl` Pawl
  - icon: ![Pawl](assets/items/gh-pawl.webp)

  {A bent black lever rises from a green block and ends in a broad angled tip.}

  ---

  A spring pawl and its connected mounting foot. Its tooth rests in the ratchet so the drum cannot freely unwind.

- `gh-rope` Rope and hook
  - icon: ![Rope and hook](assets/items/gh-rope.webp)

  {A black cord lies in a loose spiral, with a curved hook joined at its outer end.}

  ---

  One continuous cord, already tied to its hook. Push its free end under the drum’s prepared spring clamp, wind one turn, then thread it over the two pulleys.

- `gh-basket` Basket
  - icon: ![Basket](assets/items/gh-basket.webp)

  {A square green open box has a tan floor, dark lower band and a tall black handle.}

  ---

  A small rigid basket with a connected lifting handle. It hangs directly on the hook.

- `gh-fitted-1` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-1.webp)

  {One red pulley hangs beneath the left end of the tan top beam, above the winch.}
- `gh-fitted-2` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-2.webp)

  {One red pulley hangs near the middle of the tan top beam; the winch sits below at the left.}
- `gh-fitted-3` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-3.webp)

  {Two red pulleys hang beneath the tan top beam, one at its left end and one near the middle.}
- `gh-fitted-4` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-4.webp)

  {A small green block and dark lever stand beside the winch’s red toothed disc; the top beam is bare.}
- `gh-fitted-5` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-5.webp)

  {A dark lever stands beside the winch, and one red pulley hangs beneath the left end of the top beam.}
- `gh-fitted-6` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-6.webp)

  {A dark lever stands beside the winch, and one red pulley hangs near the middle of the top beam.}
- `gh-fitted-7` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-7.webp)

  {A dark lever stands beside the winch, below two red pulleys on the top beam.}
- `gh-roped` Hoist
  - icon: ![Hoist](assets/items/gh-roped.webp)

  {A thin black cord rises from the winch, crosses the two overhead red pulleys and hangs down to a hook.}
- `gantry-hoist` Gantry hoist
  - icon: ![Gantry hoist](assets/items/gantry-hoist.webp)

  {A green basket hangs from the black hook and cord between the tan frame’s legs, beneath two red pulleys.}

  ---

  Two fixed pulleys guide the cord; they change its direction without multiplying the lifting force. Turning the crank winds the drum. The pawl holds the drum between turns.


**Combinations**
- `gh-pulley-1` [consume] + `gh-side-fork` [transform] -> `gh-side-pulley`
- `gh-pulley-2` [consume] + `gh-side-fork` [transform] -> `gh-side-pulley`
- `gh-pulley-1` [consume] + `gh-drop-fork` [transform] -> `gh-drop-pulley`
- `gh-pulley-2` [consume] + `gh-drop-fork` [transform] -> `gh-drop-pulley`
- `gh-side-pulley` [consume] + `gh-mounted` [transform] -> `gh-fitted-1`
- `gh-drop-pulley` [consume] + `gh-mounted` [transform] -> `gh-fitted-2`
- `gh-pawl` [consume] + `gh-mounted` [transform] -> `gh-fitted-4`
- `gh-drop-pulley` [consume] + `gh-fitted-1` [transform] -> `gh-fitted-3`
- `gh-pawl` [consume] + `gh-fitted-1` [transform] -> `gh-fitted-5`
- `gh-side-pulley` [consume] + `gh-fitted-2` [transform] -> `gh-fitted-3`
- `gh-pawl` [consume] + `gh-fitted-2` [transform] -> `gh-fitted-6`
- `gh-pawl` [consume] + `gh-fitted-3` [transform] -> `gh-fitted-7`
- `gh-side-pulley` [consume] + `gh-fitted-4` [transform] -> `gh-fitted-5`
- `gh-drop-pulley` [consume] + `gh-fitted-4` [transform] -> `gh-fitted-6`
- `gh-drop-pulley` [consume] + `gh-fitted-5` [transform] -> `gh-fitted-7`
- `gh-side-pulley` [consume] + `gh-fitted-6` [transform] -> `gh-fitted-7`
- `gh-rope` [consume] + `gh-fitted-7` [transform] -> `gh-roped`
- `gh-basket` [consume] + `gh-roped` [transform] -> `gantry-hoist`

## `c-carousel-drive` A turning deck
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Carousel](assets/items/ca-platform.webp)

**Goals**
- Fit the spindle
  - either: `ca-spindle-base`
  - or: `ca-drive-base`
- next: Fit the motor -- `ca-drive-base`
- next: Loop the belt around both pulleys -- `ca-belted`
- next: Set the guard over the drive
  - either: `ca-guarded`
  - or: `ca-ready`
- next: Plug in the battery -- `ca-ready`
- next: Fit the deck onto the spindle -- `ca-platform`

**Items**
- `ca-base` Base
  - icon: ![Base](assets/items/ca-base.webp)

  {A thick tan circular base with a central hole, small round holes and square recesses.}

  ---

  A broad prepared base with sockets for the bearing, motor and battery. The motor and controller are matching low-voltage modules.

- `ca-spindle` Spindle
  - icon: ![Spindle](assets/items/ca-spindle.webp)

  {A broad green grooved disc sits above a square green support; a short black shaft projects from its centre.}

  ---

  A vertical spindle and pulley retained inside a bearing block. The square upper end drives the deck; a shoulder supports its hub above the guard.

- `ca-motor` Motor
  - icon: ![Motor](assets/items/ca-motor.webp)

  {A black cylindrical motor sits on a green foot, with a red pulley above and a short black lead ending in a green plug.}

  ---

  A small enclosed geared motor, its pulley, retaining strap, mounting foot and plugged lead form one supplied module.

- `ca-belt` Belt
  - icon: ![Belt](assets/items/ca-belt.webp)

  {One thin black loop with a broad rounded end and a narrower end.}
- `ca-guard` Guard
  - icon: ![Guard](assets/items/ca-guard.webp)

  {A dark translucent box-shaped cover has a small top hole, green corner feet and an opening at its lower edge.}

  ---

  A clear cover with a real shaft opening, cable opening and attached locating feet.

- `ca-battery` Battery and dial
  - icon: ![Battery and dial](assets/items/ca-battery.webp)

  {A green rectangular box has a black switch and red round knob on top.}

  ---

  The battery holder, switch and speed dial share one case. Its connected lead plugs into the motor.

- `ca-deck` Deck
  - icon: ![Deck](assets/items/ca-deck.webp)

  {A thin tan circular disc with a central hole and three smaller holes around it.}

  ---

  A round deck with a central drive socket and three prepared pole sockets.

- `ca-spindle-base` Base
  - icon: ![Base](assets/items/ca-spindle-base.webp)

  {The green pulley and square support stand in the middle of the tan circular base.}
- `ca-motor-base` Base
  - icon: ![Base](assets/items/ca-motor-base.webp)

  {The black motor with its red pulley stands near the left edge of the tan base; its lead and green plug lie beside it.}
- `ca-drive-base` Base
  - icon: ![Base](assets/items/ca-drive-base.webp)

  {The black motor and red pulley stand beside the broad green pulley on the tan base.}
- `ca-belted` Base
  - icon: ![Base](assets/items/ca-belted.webp)

  {A thin black belt spans the small red pulley and the large green pulley.}
- `ca-guarded` Base
  - icon: ![Base](assets/items/ca-guarded.webp)

  {A dark translucent cover surrounds the motor and green pulley; their outlines remain visible through its sides.}
- `ca-wired` Base
  - icon: ![Base](assets/items/ca-wired.webp)

  {A green box with a black switch and red knob sits in front of the two pulleys and their black belt.}
- `ca-ready` Base
  - icon: ![Base](assets/items/ca-ready.webp)

  {The dark translucent cover encloses the pulleys, with the green control box outside at the front.}
- `ca-platform` Carousel
  - icon: ![Carousel](assets/items/ca-platform.webp)

  {A tan circular deck sits above the covered pulleys and lower round base; the green control box projects at the front.}

**Combinations**
- `ca-spindle` [consume] + `ca-base` [transform] -> `ca-spindle-base`
- `ca-motor` [consume] + `ca-base` [transform] -> `ca-motor-base`
- `ca-motor` [consume] + `ca-spindle-base` [transform] -> `ca-drive-base`
- `ca-spindle` [consume] + `ca-motor-base` [transform] -> `ca-drive-base`
- `ca-belt` [consume] + `ca-drive-base` [transform] -> `ca-belted`
- `ca-guard` [consume] + `ca-belted` [transform] -> `ca-guarded`
- `ca-battery` [consume] + `ca-belted` [transform] -> `ca-wired`
- `ca-battery` [consume] + `ca-guarded` [transform] -> `ca-ready`
- `ca-guard` [consume] + `ca-wired` [transform] -> `ca-ready`
- `ca-deck` [consume] + `ca-ready` [transform] -> `ca-platform`

## `c-carousel-horses` Three horses
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Electric carousel](assets/items/electric-carousel.webp)

**Goals**
- Fit a pole through the red horse -- `ca-rider-1`
- next: Fit the red horse onto the deck
  - either: `ca-horses-1`
  - or: `ca-horses-3`
  - or: `ca-horses-5`
  - or: `ca-horses-7`
- next: Fit a pole through the green horse -- `ca-rider-2`
- next: Fit the green horse onto the deck
  - either: `ca-horses-2`
  - or: `ca-horses-3`
  - or: `ca-horses-6`
  - or: `ca-horses-7`
- next: Fit a pole through the cream horse -- `ca-rider-3`
- next: Fit the cream horse onto the deck
  - either: `ca-horses-4`
  - or: `ca-horses-5`
  - or: `ca-horses-6`
  - or: `ca-horses-7`
- next: Fit the roof post -- `ca-posted`
- next: Fit the canopy -- `electric-carousel`

**Items**
- `ca-horse-1` Red horse
  - icon: ![Red horse](assets/items/ca-horse-1.webp)

  {A small blocky red horse has a round hole in its back.}

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-1` Pole
  - icon: ![Pole](assets/items/ca-pole-1.webp)

  {A thin black upright rod has two small green rings around its lower half.}

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-1` Red horse
  - icon: ![Red horse](assets/items/ca-rider-1.webp)

  {A black pole passes through the red horse, with a green ring below it.}
- `ca-horse-2` Green horse
  - icon: ![Green horse](assets/items/ca-horse-2.webp)

  {A small blocky green horse has a round hole in its back.}

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-2` Pole
  - icon: ![Pole](assets/items/ca-pole-2.webp)

  {A thin black upright rod has two small green rings around its lower half.}

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-2` Green horse
  - icon: ![Green horse](assets/items/ca-rider-2.webp)

  {A black pole passes through the green horse, with a green ring below it.}
- `ca-horse-3` Cream horse
  - icon: ![Cream horse](assets/items/ca-horse-3.webp)

  {A small blocky cream horse has a round hole in its back.}

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-3` Pole
  - icon: ![Pole](assets/items/ca-pole-3.webp)

  {A thin black upright rod has two small green rings around its lower half.}

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-3` Cream horse
  - icon: ![Cream horse](assets/items/ca-rider-3.webp)

  {A black pole passes through the cream horse, with a green ring below it.}
- `ca-horses-1` Carousel
  - icon: ![Carousel](assets/items/ca-horses-1.webp)

  {One red horse stands on a black pole at the right side of the tan upper deck.}
- `ca-horses-2` Carousel
  - icon: ![Carousel](assets/items/ca-horses-2.webp)

  {One green horse stands on a black pole near the back of the tan upper deck.}
- `ca-horses-3` Carousel
  - icon: ![Carousel](assets/items/ca-horses-3.webp)

  {A red horse at the right and a green horse at the back stand on black poles above the deck.}
- `ca-horses-4` Carousel
  - icon: ![Carousel](assets/items/ca-horses-4.webp)

  {One cream horse stands on a black pole at the left front of the tan upper deck.}
- `ca-horses-5` Carousel
  - icon: ![Carousel](assets/items/ca-horses-5.webp)

  {Cream and red horses stand on black poles at opposite sides of the tan upper deck.}
- `ca-horses-6` Carousel
  - icon: ![Carousel](assets/items/ca-horses-6.webp)

  {Cream and green horses stand on black poles at the left front and back of the upper deck.}
- `ca-horses-7` Carousel
  - icon: ![Carousel](assets/items/ca-horses-7.webp)

  {Cream, green and red horses stand on three black poles around the tan upper deck.}
- `ca-roofpost` Roof post
  - icon: ![Roof post](assets/items/ca-roofpost.webp)

  {A long tan upright rod has a short green fitting around its lower end.}
- `ca-canopy` Canopy
  - icon: ![Canopy](assets/items/ca-canopy.webp)

  {A shallow red circular canopy has a small green cap at its centre.}

  ---

  A small moulded canopy with a centre socket. It sits high enough to leave the horses visible.

- `ca-posted` Carousel
  - icon: ![Carousel](assets/items/ca-posted.webp)

  {A tall tan post rises from the centre of the deck between the three horses.}
- `electric-carousel` Electric carousel
  - icon: ![Electric carousel](assets/items/electric-carousel.webp)

  {A broad red canopy on a tan central post shelters three coloured horses on black poles, above two tan circular levels and a green control box.}

  ---

  The small motor pulley drives the larger spindle pulley through the belt. All three horses turn with the deck. The roof, poles and horses keep their actual sizes throughout the build.


**Combinations**
- `ca-pole-1` [consume] + `ca-horse-1` [transform] -> `ca-rider-1`
- `ca-pole-2` [consume] + `ca-horse-1` [transform] -> `ca-rider-1`
- `ca-pole-3` [consume] + `ca-horse-1` [transform] -> `ca-rider-1`
- `ca-pole-1` [consume] + `ca-horse-2` [transform] -> `ca-rider-2`
- `ca-pole-2` [consume] + `ca-horse-2` [transform] -> `ca-rider-2`
- `ca-pole-3` [consume] + `ca-horse-2` [transform] -> `ca-rider-2`
- `ca-pole-1` [consume] + `ca-horse-3` [transform] -> `ca-rider-3`
- `ca-pole-2` [consume] + `ca-horse-3` [transform] -> `ca-rider-3`
- `ca-pole-3` [consume] + `ca-horse-3` [transform] -> `ca-rider-3`
- `ca-rider-1` [consume] + `ca-platform` [transform] -> `ca-horses-1`
- `ca-rider-2` [consume] + `ca-platform` [transform] -> `ca-horses-2`
- `ca-rider-3` [consume] + `ca-platform` [transform] -> `ca-horses-4`
- `ca-rider-2` [consume] + `ca-horses-1` [transform] -> `ca-horses-3`
- `ca-rider-3` [consume] + `ca-horses-1` [transform] -> `ca-horses-5`
- `ca-rider-1` [consume] + `ca-horses-2` [transform] -> `ca-horses-3`
- `ca-rider-3` [consume] + `ca-horses-2` [transform] -> `ca-horses-6`
- `ca-rider-3` [consume] + `ca-horses-3` [transform] -> `ca-horses-7`
- `ca-rider-1` [consume] + `ca-horses-4` [transform] -> `ca-horses-5`
- `ca-rider-2` [consume] + `ca-horses-4` [transform] -> `ca-horses-6`
- `ca-rider-2` [consume] + `ca-horses-5` [transform] -> `ca-horses-7`
- `ca-rider-1` [consume] + `ca-horses-6` [transform] -> `ca-horses-7`
- `ca-roofpost` [consume] + `ca-horses-7` [transform] -> `ca-posted`
- `ca-canopy` [consume] + `ca-posted` [transform] -> `electric-carousel`

## `c-claw-jaws` A small claw
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Claw](assets/items/cl-mechanical.webp)

**Goals**
- Fit the left jaw
  - either: `cl-mech-1`
  - or: `cl-mech-3`
  - or: `cl-mech-5`
  - or: `cl-mech-7`
  - or: `cl-mech-13`
  - or: `cl-mech-15`
  - or: `cl-mech-23`
  - or: `cl-mech-31`
  - or: `cl-mech-33`
  - or: `cl-mech-35`
  - or: `cl-mech-37`
  - or: `cl-mech-39`
  - or: `cl-mech-45`
  - or: `cl-mech-47`
  - or: `cl-mech-55`
  - or: `cl-mech-63`
  - or: `cl-mech-67`
  - or: `cl-mech-71`
  - or: `cl-mech-79`
  - or: `cl-mech-87`
  - or: `cl-mech-95`
  - or: `cl-mech-99`
  - or: `cl-mech-103`
  - or: `cl-mech-111`
  - or: `cl-mech-119`
  - or: `cl-mechanical`
- next: Fit the right jaw
  - either: `cl-mech-2`
  - or: `cl-mech-3`
  - or: `cl-mech-6`
  - or: `cl-mech-7`
  - or: `cl-mech-15`
  - or: `cl-mech-22`
  - or: `cl-mech-23`
  - or: `cl-mech-31`
  - or: `cl-mech-35`
  - or: `cl-mech-39`
  - or: `cl-mech-47`
  - or: `cl-mech-55`
  - or: `cl-mech-63`
  - or: `cl-mech-66`
  - or: `cl-mech-67`
  - or: `cl-mech-70`
  - or: `cl-mech-71`
  - or: `cl-mech-79`
  - or: `cl-mech-86`
  - or: `cl-mech-87`
  - or: `cl-mech-95`
  - or: `cl-mech-99`
  - or: `cl-mech-103`
  - or: `cl-mech-111`
  - or: `cl-mech-119`
  - or: `cl-mechanical`
- next: Fit the slider
  - either: `cl-mech-4`
  - or: `cl-mech-5`
  - or: `cl-mech-6`
  - or: `cl-mech-7`
  - or: `cl-mech-13`
  - or: `cl-mech-15`
  - or: `cl-mech-22`
  - or: `cl-mech-23`
  - or: `cl-mech-31`
  - or: `cl-mech-37`
  - or: `cl-mech-39`
  - or: `cl-mech-45`
  - or: `cl-mech-47`
  - or: `cl-mech-55`
  - or: `cl-mech-63`
  - or: `cl-mech-70`
  - or: `cl-mech-71`
  - or: `cl-mech-79`
  - or: `cl-mech-86`
  - or: `cl-mech-87`
  - or: `cl-mech-95`
  - or: `cl-mech-103`
  - or: `cl-mech-111`
  - or: `cl-mech-119`
  - or: `cl-mechanical`
- next: Snap a link onto the left pins
  - either: `cl-mech-13`
  - or: `cl-mech-15`
  - or: `cl-mech-31`
  - or: `cl-mech-45`
  - or: `cl-mech-47`
  - or: `cl-mech-63`
  - or: `cl-mech-79`
  - or: `cl-mech-95`
  - or: `cl-mech-111`
  - or: `cl-mechanical`
- next: Fit the other link
  - either: `cl-mech-22`
  - or: `cl-mech-23`
  - or: `cl-mech-31`
  - or: `cl-mech-55`
  - or: `cl-mech-63`
  - or: `cl-mech-86`
  - or: `cl-mech-87`
  - or: `cl-mech-95`
  - or: `cl-mech-119`
  - or: `cl-mechanical`
- next: Fit a pad to the left jaw
  - either: `cl-mech-33`
  - or: `cl-mech-35`
  - or: `cl-mech-37`
  - or: `cl-mech-39`
  - or: `cl-mech-45`
  - or: `cl-mech-47`
  - or: `cl-mech-55`
  - or: `cl-mech-63`
  - or: `cl-mech-99`
  - or: `cl-mech-103`
  - or: `cl-mech-111`
  - or: `cl-mech-119`
  - or: `cl-mechanical`
- next: Fit the other pad
  - either: `cl-mech-66`
  - or: `cl-mech-67`
  - or: `cl-mech-70`
  - or: `cl-mech-71`
  - or: `cl-mech-79`
  - or: `cl-mech-86`
  - or: `cl-mech-87`
  - or: `cl-mech-95`
  - or: `cl-mech-99`
  - or: `cl-mech-103`
  - or: `cl-mech-111`
  - or: `cl-mech-119`
  - or: `cl-mechanical`

**Items**
- `cl-base` Palm
  - icon: ![Palm](assets/items/cl-base.webp)

  {A tan rectangular board has a small green fitting near one end, a raised tan strip near the other and several small holes.}

  ---

  A broad prepared palm with pivot holes and a fixed return-band hook. The jaws reach just beyond its front edge.

- `cl-jaw-1` Left jaw
  - icon: ![Left jaw](assets/items/cl-jaw-1.webp)

  {A long bent tan jaw has a hooked tip, a red-rimmed middle hole and a short green-and-black pin near its other end.}

  ---

  A single jaw with captive pivot and link pins. Its left-facing shape matches the left side of the palm.

- `cl-jaw-2` Right jaw
  - icon: ![Right jaw](assets/items/cl-jaw-2.webp)

  {A long bent tan jaw has a hooked tip, a red-rimmed middle hole and a short green-and-black pin near its other end.}

  ---

  The reflected right jaw has its own captive pins.

- `cl-slider` Slider
  - icon: ![Slider](assets/items/cl-slider.webp)

  {A green rectangular frame surrounds a red sliding piece and supports a tall green bracket.}

  ---

  One retained sliding shoe inside its guide, including travel stops and the moving return-band hook.

- `cl-link-1` Link
  - icon: ![Link](assets/items/cl-link-1.webp)

  {A slim red bar ends in two open circular eyes.}

  ---

  A rigid 52 mm link with split eyes that snap sideways onto the captive pins. Either link fits either side.

- `cl-link-2` Link
  - icon: ![Link](assets/items/cl-link-2.webp)

  {A slim red bar ends in two open circular eyes.}

  ---

  A rigid 52 mm link with split eyes. Either link fits either side.

- `cl-pad-1` Pad
  - icon: ![Pad](assets/items/cl-pad-1.webp)

  {A thick black rectangular block with a green top.}

  ---

  One soft pad for the inside face of a jaw. Either pad fits either jaw.

- `cl-pad-2` Pad
  - icon: ![Pad](assets/items/cl-pad-2.webp)

  {A thick black rectangular block with a green top.}

  ---

  One soft pad. Either pad fits either jaw.

- `cl-mech-1` Claw
  - icon: ![Claw](assets/items/cl-mech-1.webp)

  {One tan hooked jaw extends from the upper right side of the board.}
- `cl-mech-2` Claw
  - icon: ![Claw](assets/items/cl-mech-2.webp)

  {One tan hooked jaw extends from the lower right side of the board.}
- `cl-mech-3` Claw
  - icon: ![Claw](assets/items/cl-mech-3.webp)

  {Two tan hooked jaws spread to the right of the board.}
- `cl-mech-4` Claw
  - icon: ![Claw](assets/items/cl-mech-4.webp)

  {A raised green bracket sits near the middle.}
- `cl-mech-5` Claw
  - icon: ![Claw](assets/items/cl-mech-5.webp)

  {One tan hooked jaw extends from the upper right side of the board. A raised green bracket sits near the middle.}
- `cl-mech-6` Claw
  - icon: ![Claw](assets/items/cl-mech-6.webp)

  {One tan hooked jaw extends from the lower right side of the board. A raised green bracket sits near the middle.}
- `cl-mech-7` Claw
  - icon: ![Claw](assets/items/cl-mech-7.webp)

  {Two tan hooked jaws spread to the right of the board. A raised green bracket sits near the middle.}
- `cl-mech-13` Claw
  - icon: ![Claw](assets/items/cl-mech-13.webp)

  {One tan hooked jaw extends from the upper right side of the board. One red bar joins the central green bracket to the upper jaw.}
- `cl-mech-15` Claw
  - icon: ![Claw](assets/items/cl-mech-15.webp)

  {Two tan hooked jaws spread to the right of the board. One red bar joins the central green bracket to the upper jaw.}
- `cl-mech-22` Claw
  - icon: ![Claw](assets/items/cl-mech-22.webp)

  {One tan hooked jaw extends from the lower right side of the board. One red bar joins the central green bracket to the lower jaw.}
- `cl-mech-23` Claw
  - icon: ![Claw](assets/items/cl-mech-23.webp)

  {Two tan hooked jaws spread to the right of the board. One red bar joins the central green bracket to the lower jaw.}
- `cl-mech-31` Claw
  - icon: ![Claw](assets/items/cl-mech-31.webp)

  {Two tan hooked jaws spread to the right of the board. Two red bars join the central green bracket to the jaws.}
- `cl-mech-33` Claw
  - icon: ![Claw](assets/items/cl-mech-33.webp)

  {One tan hooked jaw extends from the upper right side of the board. A dark green-topped pad covers the upper jaw tip.}
- `cl-mech-35` Claw
  - icon: ![Claw](assets/items/cl-mech-35.webp)

  {Two tan hooked jaws spread to the right of the board. A dark green-topped pad covers the upper jaw tip.}
- `cl-mech-37` Claw
  - icon: ![Claw](assets/items/cl-mech-37.webp)

  {One tan hooked jaw extends from the upper right side of the board. A raised green bracket sits near the middle. A dark green-topped pad covers the upper jaw tip.}
- `cl-mech-39` Claw
  - icon: ![Claw](assets/items/cl-mech-39.webp)

  {Two tan hooked jaws spread to the right of the board. A raised green bracket sits near the middle. A dark green-topped pad covers the upper jaw tip.}
- `cl-mech-45` Claw
  - icon: ![Claw](assets/items/cl-mech-45.webp)

  {One tan hooked jaw extends from the upper right side of the board. One red bar joins the central green bracket to the upper jaw. A dark green-topped pad covers the upper jaw tip.}
- `cl-mech-47` Claw
  - icon: ![Claw](assets/items/cl-mech-47.webp)

  {Two tan hooked jaws spread to the right of the board. One red bar joins the central green bracket to the upper jaw. A dark green-topped pad covers the upper jaw tip.}
- `cl-mech-55` Claw
  - icon: ![Claw](assets/items/cl-mech-55.webp)

  {Two tan hooked jaws spread to the right of the board. One red bar joins the central green bracket to the lower jaw. A dark green-topped pad covers the upper jaw tip.}
- `cl-mech-63` Claw
  - icon: ![Claw](assets/items/cl-mech-63.webp)

  {Two tan hooked jaws spread to the right of the board. Two red bars join the central green bracket to the jaws. A dark green-topped pad covers the upper jaw tip.}
- `cl-mech-66` Claw
  - icon: ![Claw](assets/items/cl-mech-66.webp)

  {One tan hooked jaw extends from the lower right side of the board. A dark green-topped pad covers the lower jaw tip.}
- `cl-mech-67` Claw
  - icon: ![Claw](assets/items/cl-mech-67.webp)

  {Two tan hooked jaws spread to the right of the board. A dark green-topped pad covers the lower jaw tip.}
- `cl-mech-70` Claw
  - icon: ![Claw](assets/items/cl-mech-70.webp)

  {One tan hooked jaw extends from the lower right side of the board. A raised green bracket sits near the middle. A dark green-topped pad covers the lower jaw tip.}
- `cl-mech-71` Claw
  - icon: ![Claw](assets/items/cl-mech-71.webp)

  {Two tan hooked jaws spread to the right of the board. A raised green bracket sits near the middle. A dark green-topped pad covers the lower jaw tip.}
- `cl-mech-79` Claw
  - icon: ![Claw](assets/items/cl-mech-79.webp)

  {Two tan hooked jaws spread to the right of the board. One red bar joins the central green bracket to the upper jaw. A dark green-topped pad covers the lower jaw tip.}
- `cl-mech-86` Claw
  - icon: ![Claw](assets/items/cl-mech-86.webp)

  {One tan hooked jaw extends from the lower right side of the board. One red bar joins the central green bracket to the lower jaw. A dark green-topped pad covers the lower jaw tip.}
- `cl-mech-87` Claw
  - icon: ![Claw](assets/items/cl-mech-87.webp)

  {Two tan hooked jaws spread to the right of the board. One red bar joins the central green bracket to the lower jaw. A dark green-topped pad covers the lower jaw tip.}
- `cl-mech-95` Claw
  - icon: ![Claw](assets/items/cl-mech-95.webp)

  {Two tan hooked jaws spread to the right of the board. Two red bars join the central green bracket to the jaws. A dark green-topped pad covers the lower jaw tip.}
- `cl-mech-99` Claw
  - icon: ![Claw](assets/items/cl-mech-99.webp)

  {Two tan hooked jaws spread to the right of the board. Dark green-topped pads cover both jaw tips.}
- `cl-mech-103` Claw
  - icon: ![Claw](assets/items/cl-mech-103.webp)

  {Two tan hooked jaws spread to the right of the board. A raised green bracket sits near the middle. Dark green-topped pads cover both jaw tips.}
- `cl-mech-111` Claw
  - icon: ![Claw](assets/items/cl-mech-111.webp)

  {Two tan hooked jaws spread to the right of the board. One red bar joins the central green bracket to the upper jaw. Dark green-topped pads cover both jaw tips.}
- `cl-mech-119` Claw
  - icon: ![Claw](assets/items/cl-mech-119.webp)

  {Two tan hooked jaws spread to the right of the board. One red bar joins the central green bracket to the lower jaw. Dark green-topped pads cover both jaw tips.}
- `cl-mechanical` Claw
  - icon: ![Claw](assets/items/cl-mechanical.webp)

  {Two tan hooked jaws spread to the right of the board. Two red bars join the central green bracket to the jaws. Dark green-topped pads cover both jaw tips.}

**Combinations**
- `cl-jaw-1` [consume] + `cl-base` [transform] -> `cl-mech-1`
- `cl-jaw-2` [consume] + `cl-base` [transform] -> `cl-mech-2`
- `cl-slider` [consume] + `cl-base` [transform] -> `cl-mech-4`
- `cl-jaw-2` [consume] + `cl-mech-1` [transform] -> `cl-mech-3`
- `cl-slider` [consume] + `cl-mech-1` [transform] -> `cl-mech-5`
- `cl-pad-1` [consume] + `cl-mech-1` [transform] -> `cl-mech-33`
- `cl-pad-2` [consume] + `cl-mech-1` [transform] -> `cl-mech-33`
- `cl-jaw-1` [consume] + `cl-mech-2` [transform] -> `cl-mech-3`
- `cl-slider` [consume] + `cl-mech-2` [transform] -> `cl-mech-6`
- `cl-pad-1` [consume] + `cl-mech-2` [transform] -> `cl-mech-66`
- `cl-pad-2` [consume] + `cl-mech-2` [transform] -> `cl-mech-66`
- `cl-slider` [consume] + `cl-mech-3` [transform] -> `cl-mech-7`
- `cl-pad-1` [consume] + `cl-mech-3` [transform] -> `cl-mech-35`
- `cl-pad-2` [consume] + `cl-mech-3` [transform] -> `cl-mech-35`
- `cl-jaw-1` [consume] + `cl-mech-4` [transform] -> `cl-mech-5`
- `cl-jaw-2` [consume] + `cl-mech-4` [transform] -> `cl-mech-6`
- `cl-jaw-2` [consume] + `cl-mech-5` [transform] -> `cl-mech-7`
- `cl-link-1` [consume] + `cl-mech-5` [transform] -> `cl-mech-13`
- `cl-link-2` [consume] + `cl-mech-5` [transform] -> `cl-mech-13`
- `cl-pad-1` [consume] + `cl-mech-5` [transform] -> `cl-mech-37`
- `cl-pad-2` [consume] + `cl-mech-5` [transform] -> `cl-mech-37`
- `cl-jaw-1` [consume] + `cl-mech-6` [transform] -> `cl-mech-7`
- `cl-link-1` [consume] + `cl-mech-6` [transform] -> `cl-mech-22`
- `cl-link-2` [consume] + `cl-mech-6` [transform] -> `cl-mech-22`
- `cl-pad-1` [consume] + `cl-mech-6` [transform] -> `cl-mech-70`
- `cl-pad-2` [consume] + `cl-mech-6` [transform] -> `cl-mech-70`
- `cl-link-1` [consume] + `cl-mech-7` [transform] -> `cl-mech-15`
- `cl-link-2` [consume] + `cl-mech-7` [transform] -> `cl-mech-15`
- `cl-pad-1` [consume] + `cl-mech-7` [transform] -> `cl-mech-39`
- `cl-pad-2` [consume] + `cl-mech-7` [transform] -> `cl-mech-39`
- `cl-jaw-2` [consume] + `cl-mech-13` [transform] -> `cl-mech-15`
- `cl-pad-1` [consume] + `cl-mech-13` [transform] -> `cl-mech-45`
- `cl-pad-2` [consume] + `cl-mech-13` [transform] -> `cl-mech-45`
- `cl-link-1` [consume] + `cl-mech-15` [transform] -> `cl-mech-31`
- `cl-link-2` [consume] + `cl-mech-15` [transform] -> `cl-mech-31`
- `cl-pad-1` [consume] + `cl-mech-15` [transform] -> `cl-mech-47`
- `cl-pad-2` [consume] + `cl-mech-15` [transform] -> `cl-mech-47`
- `cl-jaw-1` [consume] + `cl-mech-22` [transform] -> `cl-mech-23`
- `cl-pad-1` [consume] + `cl-mech-22` [transform] -> `cl-mech-86`
- `cl-pad-2` [consume] + `cl-mech-22` [transform] -> `cl-mech-86`
- `cl-link-1` [consume] + `cl-mech-23` [transform] -> `cl-mech-31`
- `cl-link-2` [consume] + `cl-mech-23` [transform] -> `cl-mech-31`
- `cl-pad-1` [consume] + `cl-mech-23` [transform] -> `cl-mech-55`
- `cl-pad-2` [consume] + `cl-mech-23` [transform] -> `cl-mech-55`
- `cl-pad-1` [consume] + `cl-mech-31` [transform] -> `cl-mech-63`
- `cl-pad-2` [consume] + `cl-mech-31` [transform] -> `cl-mech-63`
- `cl-jaw-2` [consume] + `cl-mech-33` [transform] -> `cl-mech-35`
- `cl-slider` [consume] + `cl-mech-33` [transform] -> `cl-mech-37`
- `cl-slider` [consume] + `cl-mech-35` [transform] -> `cl-mech-39`
- `cl-pad-1` [consume] + `cl-mech-35` [transform] -> `cl-mech-99`
- `cl-pad-2` [consume] + `cl-mech-35` [transform] -> `cl-mech-99`
- `cl-jaw-2` [consume] + `cl-mech-37` [transform] -> `cl-mech-39`
- `cl-link-1` [consume] + `cl-mech-37` [transform] -> `cl-mech-45`
- `cl-link-2` [consume] + `cl-mech-37` [transform] -> `cl-mech-45`
- `cl-link-1` [consume] + `cl-mech-39` [transform] -> `cl-mech-47`
- `cl-link-2` [consume] + `cl-mech-39` [transform] -> `cl-mech-47`
- `cl-pad-1` [consume] + `cl-mech-39` [transform] -> `cl-mech-103`
- `cl-pad-2` [consume] + `cl-mech-39` [transform] -> `cl-mech-103`
- `cl-jaw-2` [consume] + `cl-mech-45` [transform] -> `cl-mech-47`
- `cl-link-1` [consume] + `cl-mech-47` [transform] -> `cl-mech-63`
- `cl-link-2` [consume] + `cl-mech-47` [transform] -> `cl-mech-63`
- `cl-pad-1` [consume] + `cl-mech-47` [transform] -> `cl-mech-111`
- `cl-pad-2` [consume] + `cl-mech-47` [transform] -> `cl-mech-111`
- `cl-link-1` [consume] + `cl-mech-55` [transform] -> `cl-mech-63`
- `cl-link-2` [consume] + `cl-mech-55` [transform] -> `cl-mech-63`
- `cl-pad-1` [consume] + `cl-mech-55` [transform] -> `cl-mech-119`
- `cl-pad-2` [consume] + `cl-mech-55` [transform] -> `cl-mech-119`
- `cl-pad-1` [consume] + `cl-mech-63` [transform] -> `cl-mechanical`
- `cl-pad-2` [consume] + `cl-mech-63` [transform] -> `cl-mechanical`
- `cl-jaw-1` [consume] + `cl-mech-66` [transform] -> `cl-mech-67`
- `cl-slider` [consume] + `cl-mech-66` [transform] -> `cl-mech-70`
- `cl-slider` [consume] + `cl-mech-67` [transform] -> `cl-mech-71`
- `cl-pad-1` [consume] + `cl-mech-67` [transform] -> `cl-mech-99`
- `cl-pad-2` [consume] + `cl-mech-67` [transform] -> `cl-mech-99`
- `cl-jaw-1` [consume] + `cl-mech-70` [transform] -> `cl-mech-71`
- `cl-link-1` [consume] + `cl-mech-70` [transform] -> `cl-mech-86`
- `cl-link-2` [consume] + `cl-mech-70` [transform] -> `cl-mech-86`
- `cl-link-1` [consume] + `cl-mech-71` [transform] -> `cl-mech-79`
- `cl-link-2` [consume] + `cl-mech-71` [transform] -> `cl-mech-79`
- `cl-pad-1` [consume] + `cl-mech-71` [transform] -> `cl-mech-103`
- `cl-pad-2` [consume] + `cl-mech-71` [transform] -> `cl-mech-103`
- `cl-link-1` [consume] + `cl-mech-79` [transform] -> `cl-mech-95`
- `cl-link-2` [consume] + `cl-mech-79` [transform] -> `cl-mech-95`
- `cl-pad-1` [consume] + `cl-mech-79` [transform] -> `cl-mech-111`
- `cl-pad-2` [consume] + `cl-mech-79` [transform] -> `cl-mech-111`
- `cl-jaw-1` [consume] + `cl-mech-86` [transform] -> `cl-mech-87`
- `cl-link-1` [consume] + `cl-mech-87` [transform] -> `cl-mech-95`
- `cl-link-2` [consume] + `cl-mech-87` [transform] -> `cl-mech-95`
- `cl-pad-1` [consume] + `cl-mech-87` [transform] -> `cl-mech-119`
- `cl-pad-2` [consume] + `cl-mech-87` [transform] -> `cl-mech-119`
- `cl-pad-1` [consume] + `cl-mech-95` [transform] -> `cl-mechanical`
- `cl-pad-2` [consume] + `cl-mech-95` [transform] -> `cl-mechanical`
- `cl-slider` [consume] + `cl-mech-99` [transform] -> `cl-mech-103`
- `cl-link-1` [consume] + `cl-mech-103` [transform] -> `cl-mech-111`
- `cl-link-2` [consume] + `cl-mech-103` [transform] -> `cl-mech-111`
- `cl-link-1` [consume] + `cl-mech-111` [transform] -> `cl-mechanical`
- `cl-link-2` [consume] + `cl-mech-111` [transform] -> `cl-mechanical`
- `cl-link-1` [consume] + `cl-mech-119` [transform] -> `cl-mechanical`
- `cl-link-2` [consume] + `cl-mech-119` [transform] -> `cl-mechanical`

## `c-claw-air` Syringes and a hose
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pneumatic claw](assets/items/pneumatic-claw.webp)

**Goals**
- Slide either cup to the farther seat
  - either: `cl-front-supported`
  - or: `cl-supported-output`
- next: Fit the other cup behind it -- `cl-supported-output`
- next: Fit the plunger clip
  - either: `cl-air-1`
  - or: `cl-air-3`
  - or: `cl-air-5`
  - or: `cl-air-7`
- next: Fit the syringe into the claw
  - either: `cl-air-3`
  - or: `cl-air-7`
- next: Loop the return band over its hooks
  - either: `cl-air-4`
  - or: `cl-air-5`
  - or: `cl-air-7`
- next: Push the hose onto the hand syringe -- `cl-controller`
- next: Connect the hose to the claw -- `pneumatic-claw`

**Items**
- `cl-output` Output syringe
  - icon: ![Output syringe](assets/items/cl-output.webp)

  {A transparent blue-grey syringe has a green rim, red plunger and round red thumb plate.}

  ---

  A prepared needleless syringe. Its rigid piston and stem move inside a real hollow barrel.

- `cl-rear-cup` Cup
  - icon: ![Cup](assets/items/cl-rear-cup.webp)

  {A green upright has a semicircular recess, red curved retaining band and two black pins below.}

  ---

  Either identical cup fits either barrel seat. Slide the first over the nozzle to the farther seat, then slide the other onto the nearer seat. Each has a soft retaining strap and captive mounting pins.

- `cl-front-cup` Cup
  - icon: ![Cup](assets/items/cl-front-cup.webp)

  {A green upright has a semicircular recess, red curved retaining band and two black pins below.}

  ---

  Either identical cup fits either barrel seat. Slide the first over the nozzle to the farther seat, then slide the other onto the nearer seat. Each has a soft retaining strap and captive mounting pins.

- `cl-clip` Plunger clip
  - icon: ![Plunger clip](assets/items/cl-clip.webp)

  {A green clip has two open rectangular end fittings joined by a flat middle strip.}

  ---

  A connected clip that plugs into the slider and captures the syringe thumb flange.

- `cl-band` Return band
  - icon: ![Return band](assets/items/cl-band.webp)

  {One long narrow dark loop with rounded ends.}

  ---

  One soft elastic loop. Its two hook brackets are already attached to the palm and slider.

- `cl-input` Hand syringe
  - icon: ![Hand syringe](assets/items/cl-input.webp)

  {A transparent blue-grey syringe has a red band around its barrel, a green rim and an extended red plunger.}

  ---

  A second prepared needleless syringe. It stays beside the claw, joined by the flexible hose.

- `cl-tube` Air hose
  - icon: ![Air hose](assets/items/cl-tube.webp)

  {A short blue-green tube curves into a broad U.}

  ---

  One continuous flexible hose with an open end for each syringe nozzle.

- `cl-front-supported` Syringe
  - icon: ![Syringe](assets/items/cl-front-supported.webp)

  {A green upright stands beside the syringe barrel, with a red band around it near the plunger end.}
- `cl-supported-output` Syringe
  - icon: ![Syringe](assets/items/cl-supported-output.webp)

  {Two green uprights and red bands hold opposite ends of the syringe barrel.}
- `cl-air-1` Claw
  - icon: ![Claw](assets/items/cl-air-1.webp)

  {The two-jawed mechanism has a small upright green clip on its central bracket; both jaw tips have dark pads.}
- `cl-air-3` Claw
  - icon: ![Claw](assets/items/cl-air-3.webp)

  {A syringe on two green supports lies along the right end of the board, behind the central bracket and two padded jaws.}
- `cl-air-4` Claw
  - icon: ![Claw](assets/items/cl-air-4.webp)

  {A dark loop stretches from the small right green fitting to the central bracket, beside the two padded jaws.}
- `cl-air-5` Claw
  - icon: ![Claw](assets/items/cl-air-5.webp)

  {The central bracket has an upright green clip and a dark loop extending right; two padded jaws spread to the left.}
- `cl-air-7` Claw
  - icon: ![Claw](assets/items/cl-air-7.webp)

  {A supported syringe, upright green clip and dark loop sit behind the two padded jaws on the tan board.}
- `cl-controller` Hand syringe
  - icon: ![Hand syringe](assets/items/cl-controller.webp)

  {A blue-green hose curves from the small end of the syringe; its red plunger extends from the other end.}
- `pneumatic-claw` Pneumatic claw
  - icon: ![Pneumatic claw](assets/items/pneumatic-claw.webp)

  {Two padded wooden jaws and red links sit on a tan board. A supported syringe connects by a curved blue-green hose to a second syringe beside the board.}

  ---

  Pushing the hand syringe moves air through the hose into the output syringe. The output plunger moves the slider; the two rigid links turn the jaws. The elastic loop opens them as the plunger returns. The drawings show the available mechanism travel, not a measured grip force.


**Combinations**
- `cl-front-cup` [consume] + `cl-output` [transform] -> `cl-front-supported`
- `cl-rear-cup` [consume] + `cl-output` [transform] -> `cl-front-supported`
- `cl-front-cup` [consume] + `cl-front-supported` [transform] -> `cl-supported-output`
- `cl-rear-cup` [consume] + `cl-front-supported` [transform] -> `cl-supported-output`
- `cl-clip` [consume] + `cl-mechanical` [transform] -> `cl-air-1`
- `cl-band` [consume] + `cl-mechanical` [transform] -> `cl-air-4`
- `cl-supported-output` [consume] + `cl-air-1` [transform] -> `cl-air-3`
- `cl-band` [consume] + `cl-air-1` [transform] -> `cl-air-5`
- `cl-band` [consume] + `cl-air-3` [transform] -> `cl-air-7`
- `cl-clip` [consume] + `cl-air-4` [transform] -> `cl-air-5`
- `cl-supported-output` [consume] + `cl-air-5` [transform] -> `cl-air-7`
- `cl-tube` [consume] + `cl-input` [transform] -> `cl-controller`
- `cl-controller` [consume] + `cl-air-7` [transform] -> `pneumatic-claw`

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

  {A long black card strip with fine pale vertical marks, a horizontal line and small tabs along its lower edge.}

  ---

  One card strip with twelve marked slots and scored floor tabs. Their tips stay straight until the floor is seated. Cut down to the stopping line; the lower band stays continuous.
- `bf-film-cut-process` Cut
  - icon: ![Cut](assets/actions/cut.svg)
- `bf-film-cut` Drum wall
  - icon: ![Drum wall](assets/items/bf-film-cut.webp)

  {The black strip has narrow open slits descending from its upper edge; its lower band remains joined.}
- `bf-film-roll-process` Roll
  - icon: ![Roll](assets/actions/roll.svg)
- `bf-film-rolled` Drum
  - icon: ![Drum](assets/items/bf-film-rolled.webp)

  {The black strip forms an open cylinder with narrow upper slits and small tabs pointing down from its bottom.}
- `bf-film-tape` Tape
  - icon: ![Tape](assets/items/bf-film-tape.webp)

  {One narrow flat green strip.}
- `bf-film-seamed` Drum
  - icon: ![Drum](assets/items/bf-film-seamed.webp)

  {A green strip covers the lower part of the black cylinder’s front seam.}

**Combinations**
- `bf-film-wall` [transform] @ `bf-film-cut-process` -> `bf-film-cut`
- `bf-film-cut` [transform] @ `bf-film-roll-process` -> `bf-film-rolled`
- `bf-film-tape` [consume] + `bf-film-rolled` [transform] -> `bf-film-seamed`


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

  {A green strip covers the lower part of the black cylinder’s front seam.}
- `bf-film-flip-process` Flip
  - icon: ![Flip](assets/actions/flip.svg)
- `bf-film-under` Drum
  - icon: ![Drum](assets/items/bf-film-under.webp)

  {The black cylinder is upside down: its small tabs point upward and the long slits reach the lower edge.}
- `bf-film-fold-process` Fold
  - icon: ![Fold](assets/actions/fold.svg)
- `bf-film-prepared` Drum
  - icon: ![Drum](assets/items/bf-film-prepared.webp)

  {Short dark tabs project around the open upper rim of the upside-down black cylinder.}
- `bf-film-floor` Floor
  - icon: ![Floor](assets/items/bf-film-floor.webp)

  {A thin tan circular disc with small slots around its edge.}

  ---

  A 178.8 mm disc, smaller than the wall opening, with twelve slots for the straight tabs. Fold the tips underneath only after inserting it.
- `bf-film-seated` Drum
  - icon: ![Drum](assets/items/bf-film-seated.webp)

  {A tan circular floor fills the upper opening of the upside-down cylinder; small black tab tips project through its edge slots.}
- `bf-film-shell` Drum
  - icon: ![Drum](assets/items/bf-film-shell.webp)

  {The tan circular floor has small black tabs folded flat around its rim.}
- `bf-film-base` Base
  - icon: ![Base](assets/items/bf-film-base.webp)

  {A thick tan circular disc with a small hole at its centre.}
- `bf-film-bearing` Turntable
  - icon: ![Turntable](assets/items/bf-film-bearing.webp)

  {A broad green disc sits above a narrow green stem, cream ring and projecting black pin.}

  ---

  One retained spindle, sleeve bearing and platform. The spindle stays fixed in the base while the platform turns.
- `bf-film-turntable` Base
  - icon: ![Base](assets/items/bf-film-turntable.webp)

  {The green turntable sits on a narrow stem in the middle of the thick tan circular base.}
- `bf-film-mounted-under` Drum
  - icon: ![Drum](assets/items/bf-film-mounted-under.webp)

  {A smaller tan base sits above the upside-down drum’s floor, with three green pads and a central hole on its exposed face.}
- `bf-film-standing` Drum
  - icon: ![Drum](assets/items/bf-film-standing.webp)

  {The black slit drum stands upright on a round tan base, with green tape along its front seam.}

**Combinations**
- `bf-film-seamed` [transform] @ `bf-film-flip-process` -> `bf-film-under`
- `bf-film-under` [transform] @ `bf-film-fold-process` -> `bf-film-prepared`
- `bf-film-floor` [consume] + `bf-film-prepared` [transform] -> `bf-film-seated`
- `bf-film-seated` [transform] @ `bf-film-fold-process` -> `bf-film-shell`
- `bf-film-bearing` [consume] + `bf-film-base` [transform] -> `bf-film-turntable`
- `bf-film-turntable` [consume] + `bf-film-shell` [transform] -> `bf-film-mounted-under`
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

  {A long pale strip divided into panels, with small red outlined fish in different positions and a green line near one edge.}

  ---

  A printed sequence of twelve fish pictures, one per viewing slit, with a prepared adhesive overlap. The pictures face inward when rolled.
- `bf-film-picture-roll` Roll
  - icon: ![Roll](assets/actions/roll.svg)
- `bf-film-loop` Picture ring
  - icon: ![Picture ring](assets/items/bf-film-loop.webp)

  {The pale picture strip forms an open ring with red outlined fish and a green line around its inner face.}
- `bf-film-standing` Drum
  - icon: ![Drum](assets/items/bf-film-standing.webp)

  {The black slit drum stands upright on a round tan base, with green tape along its front seam.}
- `animation-drum` Animation drum
  - icon: ![Animation drum](assets/items/animation-drum.webp)

  {A pale ring of red outlined fish sits inside the black slit drum, above its round tan base.}

  ---

  Looking through the slits gives brief separated glimpses of successive pictures, with darkness between them.

**Combinations**
- `bf-film-strip` [transform] @ `bf-film-picture-roll` -> `bf-film-loop`
- `bf-film-loop` [consume] + `bf-film-standing` [transform] -> `animation-drum`

## `c-rover-drive` Two wheels, two motors
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Build reference](assets/items/rv-mounted.webp)

**Goals**
- Flip the deck over -- `rv-under`
- next: Fit a wheel to the left motor -- `rv-drive-a`
- next: Fit a wheel to the right motor -- `rv-drive-b`
- next: Fit the left drive to the deck
  - either: `rv-deck-01`
  - or: `rv-deck-03`
  - or: `rv-deck-05`
  - or: `rv-deck-07`
  - or: `rv-deck-09`
  - or: `rv-deck-11`
  - or: `rv-deck-13`
  - or: `rv-deck-15`
  - or: `rv-deck-17`
  - or: `rv-deck-19`
  - or: `rv-deck-21`
  - or: `rv-deck-23`
  - or: `rv-deck-25`
  - or: `rv-deck-27`
  - or: `rv-deck-29`
  - or: `rv-mounted`
- next: Fit the right drive
  - either: `rv-deck-03`
  - or: `rv-deck-07`
  - or: `rv-deck-11`
  - or: `rv-deck-15`
  - or: `rv-deck-19`
  - or: `rv-deck-23`
  - or: `rv-deck-27`
  - or: `rv-mounted`
- next: Fit the caster
  - either: `rv-deck-04`
  - or: `rv-deck-05`
  - or: `rv-deck-06`
  - or: `rv-deck-07`
  - or: `rv-deck-12`
  - or: `rv-deck-13`
  - or: `rv-deck-14`
  - or: `rv-deck-15`
  - or: `rv-deck-20`
  - or: `rv-deck-21`
  - or: `rv-deck-22`
  - or: `rv-deck-23`
  - or: `rv-deck-28`
  - or: `rv-deck-29`
  - or: `rv-deck-30`
  - or: `rv-mounted`
- next: Fit the battery pack
  - either: `rv-deck-08`
  - or: `rv-deck-09`
  - or: `rv-deck-10`
  - or: `rv-deck-11`
  - or: `rv-deck-12`
  - or: `rv-deck-13`
  - or: `rv-deck-14`
  - or: `rv-deck-15`
  - or: `rv-deck-24`
  - or: `rv-deck-25`
  - or: `rv-deck-26`
  - or: `rv-deck-27`
  - or: `rv-deck-28`
  - or: `rv-deck-29`
  - or: `rv-deck-30`
  - or: `rv-mounted`
- next: Fit the receiver -- `rv-mounted`

**Hotspots**
- `rv-flip-build` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `rv-deck` Deck
  - icon: ![Deck](assets/items/rv-deck.webp)

  {A tan rectangular board has two tall dark rods, small green fittings and a short red lever near its centre.}

  ---

  The prepared deck includes two bare pen guide rods and a hand-operated lift cam. Fit the carriage, then its return spring and connected guide cap.
- `rv-motor-a` Left motor
  - icon: ![Left motor](assets/items/rv-motor-a.webp)

  {A green box has a flat mounting plate, two black screws, a projecting dark shaft and a red lead ending in a dark plug.}

  ---

  An enclosed slow gearmotor, mounting flange and attached lead. Its output shaft drives one wheel.
- `rv-motor-b` Right motor
  - icon: ![Right motor](assets/items/rv-motor-b.webp)

  {A green box has a flat mounting plate and two black screws; a short red lead and dark plug run along its side.}

  ---

  An enclosed slow gearmotor, mounting flange and attached lead. Its output shaft drives one wheel.
- `rv-wheel-a` Wheel
  - icon: ![Wheel](assets/items/rv-wheel.webp)

  {A thick black wheel has eight red spokes and a green centre cap.}

  ---

  Either wheel fits either geared motor. Its retained centre fastener locks the hub to the flat-sided shaft.
- `rv-wheel-b` Wheel
  - icon: ![Wheel](assets/items/rv-wheel.webp)

  {A thick black wheel has eight red spokes and a green centre cap.}

  ---

  Either wheel fits either geared motor. Its retained centre fastener locks the hub to the flat-sided shaft.
- `rv-caster` Caster
  - icon: ![Caster](assets/items/rv-caster.webp)

  {A green rounded foot hangs below a short stem and square mounting plate with two black screws.}

  ---

  The free-turning ball supports the third corner.
- `rv-pack` Battery pack
  - icon: ![Battery pack](assets/items/rv-pack.webp)

  {A flat green box has two black mounting screws and a long red lead ending in a dark plug.}

  ---

  An enclosed compatible low-voltage pack with cells already fitted.
- `rv-receiver` Receiver
  - icon: ![Receiver](assets/items/rv-receiver.webp)

  {A green rectangular box has two black mounting screws and a small red mark on its top plate.}

  ---

  The supplied receiver and motor driver control the wheels independently. Its matching ready-to-use remote needs no construction here.
- `rv-under` Deck
  - icon: ![Deck](assets/items/rv-under.webp)

  {A bare tan rectangular board has several round holes and a narrow rectangular slot.}
- `rv-drive-a` Left drive
  - icon: ![Left drive](assets/items/rv-drive-a.webp)

  {A black wheel with red spokes sits on the green box’s shaft; its red lead extends from the other side.}
- `rv-drive-b` Right drive
  - icon: ![Right drive](assets/items/rv-drive-b.webp)

  {A black wheel stands behind a green box with two mounting screws and a red side lead.}
- `rv-deck-01` Rover
  - icon: ![Rover](assets/items/rv-deck-01.webp)

  {The tan board carries one black wheel unit on a green mount at its far edge.}
- `rv-deck-02` Rover
  - icon: ![Rover](assets/items/rv-deck-02.webp)

  {The tan board carries one red-spoked black wheel unit on a green mount at its near edge.}
- `rv-deck-03` Rover
  - icon: ![Rover](assets/items/rv-deck-03.webp)

  {The tan board carries two black wheel units on green mounts.}
- `rv-deck-04` Rover
  - icon: ![Rover](assets/items/rv-deck-04.webp)

  {The tan board carries a green round-topped foot at the right.}
- `rv-deck-05` Rover
  - icon: ![Rover](assets/items/rv-deck-05.webp)

  {The tan board carries one black wheel unit on a green mount at its far edge and a green round-topped foot at the right.}
- `rv-deck-06` Rover
  - icon: ![Rover](assets/items/rv-deck-06.webp)

  {The tan board carries one red-spoked black wheel unit on a green mount at its near edge and a green round-topped foot at the right.}
- `rv-deck-07` Rover
  - icon: ![Rover](assets/items/rv-deck-07.webp)

  {The tan board carries two black wheel units on green mounts and a green round-topped foot at the right.}
- `rv-deck-08` Rover
  - icon: ![Rover](assets/items/rv-deck-08.webp)

  {The tan board carries a dark-topped green box near the back.}
- `rv-deck-09` Rover
  - icon: ![Rover](assets/items/rv-deck-09.webp)

  {The tan board carries one black wheel unit on a green mount at its far edge and a dark-topped green box near the back.}
- `rv-deck-10` Rover
  - icon: ![Rover](assets/items/rv-deck-10.webp)

  {The tan board carries one red-spoked black wheel unit on a green mount at its near edge and a dark-topped green box near the back.}
- `rv-deck-11` Rover
  - icon: ![Rover](assets/items/rv-deck-11.webp)

  {The tan board carries two black wheel units on green mounts and a dark-topped green box near the back.}
- `rv-deck-12` Rover
  - icon: ![Rover](assets/items/rv-deck-12.webp)

  {The tan board carries a green round-topped foot at the right and a dark-topped green box near the back.}
- `rv-deck-13` Rover
  - icon: ![Rover](assets/items/rv-deck-13.webp)

  {The tan board carries one black wheel unit on a green mount at its far edge, a green round-topped foot at the right and a dark-topped green box near the back.}
- `rv-deck-14` Rover
  - icon: ![Rover](assets/items/rv-deck-14.webp)

  {The tan board carries one red-spoked black wheel unit on a green mount at its near edge, a green round-topped foot at the right and a dark-topped green box near the back.}
- `rv-deck-15` Rover
  - icon: ![Rover](assets/items/rv-deck-15.webp)

  {The tan board carries two black wheel units on green mounts, a green round-topped foot at the right and a dark-topped green box near the back.}
- `rv-deck-16` Rover
  - icon: ![Rover](assets/items/rv-deck-16.webp)

  {The tan board carries a closed green box near the front.}
- `rv-deck-17` Rover
  - icon: ![Rover](assets/items/rv-deck-17.webp)

  {The tan board carries one black wheel unit on a green mount at its far edge and a closed green box near the front.}
- `rv-deck-18` Rover
  - icon: ![Rover](assets/items/rv-deck-18.webp)

  {The tan board carries one red-spoked black wheel unit on a green mount at its near edge and a closed green box near the front.}
- `rv-deck-19` Rover
  - icon: ![Rover](assets/items/rv-deck-19.webp)

  {The tan board carries two black wheel units on green mounts and a closed green box near the front.}
- `rv-deck-20` Rover
  - icon: ![Rover](assets/items/rv-deck-20.webp)

  {The tan board carries a green round-topped foot at the right and a closed green box near the front.}
- `rv-deck-21` Rover
  - icon: ![Rover](assets/items/rv-deck-21.webp)

  {The tan board carries one black wheel unit on a green mount at its far edge, a green round-topped foot at the right and a closed green box near the front.}
- `rv-deck-22` Rover
  - icon: ![Rover](assets/items/rv-deck-22.webp)

  {The tan board carries one red-spoked black wheel unit on a green mount at its near edge, a green round-topped foot at the right and a closed green box near the front.}
- `rv-deck-23` Rover
  - icon: ![Rover](assets/items/rv-deck-23.webp)

  {The tan board carries two black wheel units on green mounts, a green round-topped foot at the right and a closed green box near the front.}
- `rv-deck-24` Rover
  - icon: ![Rover](assets/items/rv-deck-24.webp)

  {The tan board carries a dark-topped green box near the back and a closed green box near the front.}
- `rv-deck-25` Rover
  - icon: ![Rover](assets/items/rv-deck-25.webp)

  {The tan board carries one black wheel unit on a green mount at its far edge, a dark-topped green box near the back and a closed green box near the front.}
- `rv-deck-26` Rover
  - icon: ![Rover](assets/items/rv-deck-26.webp)

  {The tan board carries one red-spoked black wheel unit on a green mount at its near edge, a dark-topped green box near the back and a closed green box near the front.}
- `rv-deck-27` Rover
  - icon: ![Rover](assets/items/rv-deck-27.webp)

  {The tan board carries two black wheel units on green mounts, a dark-topped green box near the back and a closed green box near the front.}
- `rv-deck-28` Rover
  - icon: ![Rover](assets/items/rv-deck-28.webp)

  {The tan board carries a green round-topped foot at the right, a dark-topped green box near the back and a closed green box near the front.}
- `rv-deck-29` Rover
  - icon: ![Rover](assets/items/rv-deck-29.webp)

  {The tan board carries one black wheel unit on a green mount at its far edge, a green round-topped foot at the right, a dark-topped green box near the back and a closed green box near the front.}
- `rv-deck-30` Rover
  - icon: ![Rover](assets/items/rv-deck-30.webp)

  {The tan board carries one red-spoked black wheel unit on a green mount at its near edge, a green round-topped foot at the right, a dark-topped green box near the back and a closed green box near the front.}
- `rv-mounted` Rover
  - icon: ![Rover](assets/items/rv-mounted.webp)

  {The tan board carries two black wheel units on green mounts, a green round-topped foot at the right, a dark-topped green box near the back and a closed green box near the front.}
- `rv-flip-build` Flip

**Combinations**
- `rv-wheel-a` [consume] + `rv-motor-a` [transform] -> `rv-drive-a`
- `rv-wheel-b` [consume] + `rv-motor-a` [transform] -> `rv-drive-a`
- `rv-wheel-a` [consume] + `rv-motor-b` [transform] -> `rv-drive-b`
- `rv-wheel-b` [consume] + `rv-motor-b` [transform] -> `rv-drive-b`
- `rv-drive-a` [consume] + `rv-under` [transform] -> `rv-deck-01`
- `rv-drive-b` [consume] + `rv-under` [transform] -> `rv-deck-02`
- `rv-caster` [consume] + `rv-under` [transform] -> `rv-deck-04`
- `rv-pack` [consume] + `rv-under` [transform] -> `rv-deck-08`
- `rv-receiver` [consume] + `rv-under` [transform] -> `rv-deck-16`
- `rv-drive-b` [consume] + `rv-deck-01` [transform] -> `rv-deck-03`
- `rv-caster` [consume] + `rv-deck-01` [transform] -> `rv-deck-05`
- `rv-pack` [consume] + `rv-deck-01` [transform] -> `rv-deck-09`
- `rv-receiver` [consume] + `rv-deck-01` [transform] -> `rv-deck-17`
- `rv-drive-a` [consume] + `rv-deck-02` [transform] -> `rv-deck-03`
- `rv-caster` [consume] + `rv-deck-02` [transform] -> `rv-deck-06`
- `rv-pack` [consume] + `rv-deck-02` [transform] -> `rv-deck-10`
- `rv-receiver` [consume] + `rv-deck-02` [transform] -> `rv-deck-18`
- `rv-caster` [consume] + `rv-deck-03` [transform] -> `rv-deck-07`
- `rv-pack` [consume] + `rv-deck-03` [transform] -> `rv-deck-11`
- `rv-receiver` [consume] + `rv-deck-03` [transform] -> `rv-deck-19`
- `rv-drive-a` [consume] + `rv-deck-04` [transform] -> `rv-deck-05`
- `rv-drive-b` [consume] + `rv-deck-04` [transform] -> `rv-deck-06`
- `rv-pack` [consume] + `rv-deck-04` [transform] -> `rv-deck-12`
- `rv-receiver` [consume] + `rv-deck-04` [transform] -> `rv-deck-20`
- `rv-drive-b` [consume] + `rv-deck-05` [transform] -> `rv-deck-07`
- `rv-pack` [consume] + `rv-deck-05` [transform] -> `rv-deck-13`
- `rv-receiver` [consume] + `rv-deck-05` [transform] -> `rv-deck-21`
- `rv-drive-a` [consume] + `rv-deck-06` [transform] -> `rv-deck-07`
- `rv-pack` [consume] + `rv-deck-06` [transform] -> `rv-deck-14`
- `rv-receiver` [consume] + `rv-deck-06` [transform] -> `rv-deck-22`
- `rv-pack` [consume] + `rv-deck-07` [transform] -> `rv-deck-15`
- `rv-receiver` [consume] + `rv-deck-07` [transform] -> `rv-deck-23`
- `rv-drive-a` [consume] + `rv-deck-08` [transform] -> `rv-deck-09`
- `rv-drive-b` [consume] + `rv-deck-08` [transform] -> `rv-deck-10`
- `rv-caster` [consume] + `rv-deck-08` [transform] -> `rv-deck-12`
- `rv-receiver` [consume] + `rv-deck-08` [transform] -> `rv-deck-24`
- `rv-drive-b` [consume] + `rv-deck-09` [transform] -> `rv-deck-11`
- `rv-caster` [consume] + `rv-deck-09` [transform] -> `rv-deck-13`
- `rv-receiver` [consume] + `rv-deck-09` [transform] -> `rv-deck-25`
- `rv-drive-a` [consume] + `rv-deck-10` [transform] -> `rv-deck-11`
- `rv-caster` [consume] + `rv-deck-10` [transform] -> `rv-deck-14`
- `rv-receiver` [consume] + `rv-deck-10` [transform] -> `rv-deck-26`
- `rv-caster` [consume] + `rv-deck-11` [transform] -> `rv-deck-15`
- `rv-receiver` [consume] + `rv-deck-11` [transform] -> `rv-deck-27`
- `rv-drive-a` [consume] + `rv-deck-12` [transform] -> `rv-deck-13`
- `rv-drive-b` [consume] + `rv-deck-12` [transform] -> `rv-deck-14`
- `rv-receiver` [consume] + `rv-deck-12` [transform] -> `rv-deck-28`
- `rv-drive-b` [consume] + `rv-deck-13` [transform] -> `rv-deck-15`
- `rv-receiver` [consume] + `rv-deck-13` [transform] -> `rv-deck-29`
- `rv-drive-a` [consume] + `rv-deck-14` [transform] -> `rv-deck-15`
- `rv-receiver` [consume] + `rv-deck-14` [transform] -> `rv-deck-30`
- `rv-receiver` [consume] + `rv-deck-15` [transform] -> `rv-mounted`
- `rv-drive-a` [consume] + `rv-deck-16` [transform] -> `rv-deck-17`
- `rv-drive-b` [consume] + `rv-deck-16` [transform] -> `rv-deck-18`
- `rv-caster` [consume] + `rv-deck-16` [transform] -> `rv-deck-20`
- `rv-pack` [consume] + `rv-deck-16` [transform] -> `rv-deck-24`
- `rv-drive-b` [consume] + `rv-deck-17` [transform] -> `rv-deck-19`
- `rv-caster` [consume] + `rv-deck-17` [transform] -> `rv-deck-21`
- `rv-pack` [consume] + `rv-deck-17` [transform] -> `rv-deck-25`
- `rv-drive-a` [consume] + `rv-deck-18` [transform] -> `rv-deck-19`
- `rv-caster` [consume] + `rv-deck-18` [transform] -> `rv-deck-22`
- `rv-pack` [consume] + `rv-deck-18` [transform] -> `rv-deck-26`
- `rv-caster` [consume] + `rv-deck-19` [transform] -> `rv-deck-23`
- `rv-pack` [consume] + `rv-deck-19` [transform] -> `rv-deck-27`
- `rv-drive-a` [consume] + `rv-deck-20` [transform] -> `rv-deck-21`
- `rv-drive-b` [consume] + `rv-deck-20` [transform] -> `rv-deck-22`
- `rv-pack` [consume] + `rv-deck-20` [transform] -> `rv-deck-28`
- `rv-drive-b` [consume] + `rv-deck-21` [transform] -> `rv-deck-23`
- `rv-pack` [consume] + `rv-deck-21` [transform] -> `rv-deck-29`
- `rv-drive-a` [consume] + `rv-deck-22` [transform] -> `rv-deck-23`
- `rv-pack` [consume] + `rv-deck-22` [transform] -> `rv-deck-30`
- `rv-pack` [consume] + `rv-deck-23` [transform] -> `rv-mounted`
- `rv-drive-a` [consume] + `rv-deck-24` [transform] -> `rv-deck-25`
- `rv-drive-b` [consume] + `rv-deck-24` [transform] -> `rv-deck-26`
- `rv-caster` [consume] + `rv-deck-24` [transform] -> `rv-deck-28`
- `rv-drive-b` [consume] + `rv-deck-25` [transform] -> `rv-deck-27`
- `rv-caster` [consume] + `rv-deck-25` [transform] -> `rv-deck-29`
- `rv-drive-a` [consume] + `rv-deck-26` [transform] -> `rv-deck-27`
- `rv-caster` [consume] + `rv-deck-26` [transform] -> `rv-deck-30`
- `rv-caster` [consume] + `rv-deck-27` [transform] -> `rv-mounted`
- `rv-drive-a` [consume] + `rv-deck-28` [transform] -> `rv-deck-29`
- `rv-drive-b` [consume] + `rv-deck-28` [transform] -> `rv-deck-30`
- `rv-drive-b` [consume] + `rv-deck-29` [transform] -> `rv-mounted`
- `rv-drive-a` [consume] + `rv-deck-30` [transform] -> `rv-mounted`
- `rv-deck` [transform] @ `rv-flip-build` -> `rv-under`


## `c-rover-pen` A pen for the rover
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Build reference](assets/items/drawing-rover.webp)

**Goals**
- Connect the switch harness -- `rv-wired`
- next: Fit a guard
  - either: `rv-one-guard-a`
  - or: `rv-one-guard-b`
  - or: `rv-guarded`
- next: Fit the other guard -- `rv-guarded`
- next: Flip the rover upright -- `rv-upright`
- next: Clip the pen into its carriage -- `rv-pen-carriage`
- next: Slide the carriage onto the guides -- `rv-pen-fitted`
- next: Slide on the return spring -- `rv-sprung`
- next: Press on the guide cap -- `drawing-rover`

**Hotspots**
- `rv-flip-pen` (center 130px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `rv-harness` Switch harness
  - icon: ![Switch harness](assets/items/rv-harness.webp)

  {A small red box has two black mounting screws, a black upright switch and a bent dark lead ending in a red plug.}

  ---

  A connected fused harness and switch. Fit with the power off and connect the parked battery and motor plugs to their matching sockets.
- `rv-guard-a` Guard
  - icon: ![Guard](assets/items/rv-guard-a.webp)

  {An open cream box-shaped cover has a rounded side opening, a smaller rimmed opening and two red fittings at the top.}

  ---

  One hollow snap-on guard. Its open shaft slot and split cable channel fit around the already attached wheel and lead.
- `rv-guard-b` Guard
  - icon: ![Guard](assets/items/rv-guard-b.webp)

  {An open cream box-shaped cover has rounded and rectangular edge cutouts, with two red fittings at the top.}

  ---

  One hollow snap-on guard, fitted independently on the other drive.
- `rv-pen` Pen
  - icon: ![Pen](assets/items/rv-pen.webp)

  {A long green pen has a dark cap and pointed tip.}

  ---

  A felt-tip pen with its cap removed.
- `rv-clip` Pen carriage
  - icon: ![Pen carriage](assets/items/rv-clip.webp)

  {A green bracket carries a split red circular clip and has a long flat arm projecting sideways.}

  ---

  One connected bridge, spring clip and follower shoe. The deck already carries the guides and lift lever.
- `rv-spring` Return spring
  - icon: ![Return spring](assets/items/rv-spring.webp)

  {A short red coil with open ends.}

  ---

  One compression spring slides down the near guide rod after the carriage. The guide cap retains its upper end.
- `rv-cap` Guide cap
  - icon: ![Guide cap](assets/items/rv-cap.webp)

  {A green rectangular bar has two rounded fittings underneath.}

  ---

  One connected bridge with two soft lined sockets. Press it onto the two bare guide ends to retain the carriage and compress its return spring.
- `rv-wired` Rover
  - icon: ![Rover](assets/items/rv-wired.webp)

  {Two wheel units, a round green caster and two green boxes sit on the tan deck, joined by thin leads and a small red switch box.}
- `rv-one-guard-a` Rover
  - icon: ![Rover](assets/items/rv-one-guard-a.webp)

  {A cream cover surrounds the far wheel’s green box; the nearer wheel’s green box remains exposed.}
- `rv-one-guard-b` Rover
  - icon: ![Rover](assets/items/rv-one-guard-b.webp)

  {A cream cover surrounds the nearer wheel’s green box; the far wheel’s green box remains exposed.}
- `rv-guarded` Rover
  - icon: ![Rover](assets/items/rv-guarded.webp)

  {Cream covers surround both wheel boxes; the green caster, two green boxes and red switch box remain visible between them.}
- `rv-upright` Rover
  - icon: ![Rover](assets/items/rv-upright.webp)

  {The tan board sits above the wheels and green rounded foot. Two dark guide rods, green fittings and a short red lever rise from its top.}
- `rv-pen-carriage` Pen carriage
  - icon: ![Pen carriage](assets/items/rv-pen-carriage.webp)

  {A green pen passes through the red ring of a green bracket, with the bracket’s flat arm projecting sideways.}
- `rv-pen-fitted` Rover
  - icon: ![Rover](assets/items/rv-pen-fitted.webp)

  {The green pen and its bracket stand between the dark guide rods above the wheeled tan board.}
- `rv-sprung` Rover
  - icon: ![Rover](assets/items/rv-sprung.webp)

  {A short red coil surrounds the guide rod beside the green pen.}
- `drawing-rover` Drawing rover
  - icon: ![Drawing rover](assets/items/drawing-rover.webp)

  {A green top bar bridges the two guide rods beside the upright pen, above a tan board on two black wheels and a rounded green foot.}

  ---

  Different wheel speeds steer the rover. The hand lever lifts the pen between strokes. A slight motor mismatch makes a curve; the receiver has a trim screw. These are ordinary mechanisms, not a promise of precise handwriting.
- `rv-flip-pen` Flip

**Combinations**
- `rv-harness` [consume] + `rv-mounted` [transform] -> `rv-wired`
- `rv-guard-a` [consume] + `rv-wired` [transform] -> `rv-one-guard-a`
- `rv-guard-b` [consume] + `rv-one-guard-a` [transform] -> `rv-guarded`
- `rv-guard-b` [consume] + `rv-wired` [transform] -> `rv-one-guard-b`
- `rv-guard-a` [consume] + `rv-one-guard-b` [transform] -> `rv-guarded`
- `rv-guarded` [transform] @ `rv-flip-pen` -> `rv-upright`
- `rv-pen` [consume] + `rv-clip` [transform] -> `rv-pen-carriage`
- `rv-pen-carriage` [consume] + `rv-upright` [transform] -> `rv-pen-fitted`
- `rv-spring` [consume] + `rv-pen-fitted` [transform] -> `rv-sprung`
- `rv-cap` [consume] + `rv-sprung` [transform] -> `drawing-rover`

## `c-projector-box` A box of stars
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Build reference](assets/items/pj-wheel-box.webp)

**Goals**
- Fit the reflector inside the box -- `pj-lined`
- next: Punch stars around the disc -- `pj-stars`
- next: Slide the disc onto the spindle -- `pj-disc-shaft`
- next: Fit the disc collar -- `pj-wheel`
- next: Lower the star wheel into the bearings -- `pj-loaded`
- next: Fit the lamp -- `pj-lamped`
- next: Connect the battery pack -- `pj-wheel-box`

**Hotspots**
- `pj-punch` (center 130px, 216px)
  - icon: ![Punch](assets/actions/punch.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `pj-box` Box
  - icon: ![Box](assets/items/pj-box.webp)

  {An open tan box has a dark upright panel across its interior, several round floor holes and shaped slots in its walls.}

  ---

  An open prepared box with two upward-opening bearing cradles. Prepared loading slots let the complete star wheel lower into them; the lid closes those slots and retains the shaft.
- `pj-liner` Reflector
  - icon: ![Reflector](assets/items/pj-liner.webp)

  {A pale U-shaped liner has a flat bottom, two tall sides and a small round hole.}

  ---

  One folded U-shaped reflector joins its floor and side faces. It leaves the electrical contacts clear.
- `pj-lamp` Lamp
  - icon: ![Lamp](assets/items/pj-lamp.webp)

  {A small green rectangular fitting holds a pale panel and a long thin black lead.}

  ---

  A cool-running diffused LED module, holder, current-limiting resistor and attached lead.
- `pj-battery` Battery pack
  - icon: ![Battery pack](assets/items/pj-battery.webp)

  {A green-sided pack holds two dark rectangular blocks, with a small red button near one top corner.}

  ---

  An enclosed compatible switched low-voltage pack with its connected holder and fused lead. Connect with the switch off.
- `pj-card` Card disc
  - icon: ![Card disc](assets/items/pj-card.webp)

  {A flat dark circular disc with one small centre hole.}

  ---

  The flat-sided centre hole matches the spindle.
- `pj-spindle` Spindle
  - icon: ![Spindle](assets/items/pj-spindle.webp)

  {A long narrow dark shaft has small green and red fittings near one end.}

  ---

  The flat continues from the free front end to the disc seat. Slide the disc along it until it reaches the fixed rear shoulder. The two rear flanges locate the shaft in its bearing.
- `pj-collar` Disc collar
  - icon: ![Disc collar](assets/items/pj-collar.webp)

  {A thick green ring has a large central opening and a smaller hole through its side.}

  ---

  Slide this flat-sided collar along the same free end, then tighten its captive screw against the shaft flat. It holds the disc against the fixed shoulder.
- `pj-lined` Projector
  - icon: ![Projector](assets/items/pj-lined.webp)

  {A broad pale liner covers part of the open tan box’s interior, beside a dark upright panel.}
- `pj-loaded` Projector
  - icon: ![Projector](assets/items/pj-loaded.webp)

  {A long dark shaft projects from the open tan box. A dark circular disc stands across the nearer compartment.}
- `pj-lamped` Projector
  - icon: ![Projector](assets/items/pj-lamped.webp)

  {A small pale rectangle in a green fitting sits beside the disc near the edge of the open box; the long shaft projects above it.}
- `pj-stars` Star disc
  - icon: ![Star disc](assets/items/pj-stars.webp)

  {Many tiny holes circle the outer part of the dark disc, around its small central hole.}
- `pj-disc-shaft` Star wheel
  - icon: ![Star wheel](assets/items/pj-disc-shaft.webp)

  {A dark shaft projects diagonally from the centre of the perforated disc.}
- `pj-wheel` Star wheel
  - icon: ![Star wheel](assets/items/pj-wheel.webp)

  {A small green ring surrounds the shaft where it enters the perforated disc.}
- `pj-wheel-box` Projector
  - icon: ![Projector](assets/items/pj-wheel-box.webp)

  {A dark block with a green edge is visible in the left-hand compartment of the open box, beside the disc and projecting shaft.}
- `pj-punch` Punch

**Combinations**
- `pj-card` [transform] @ `pj-punch` -> `pj-stars`
- `pj-stars` [consume] + `pj-spindle` [transform] -> `pj-disc-shaft`
- `pj-collar` [consume] + `pj-disc-shaft` [transform] -> `pj-wheel`
- `pj-liner` [consume] + `pj-box` [transform] -> `pj-lined`
- `pj-wheel` [consume] + `pj-lined` [transform] -> `pj-loaded`
- `pj-lamp` [consume] + `pj-loaded` [transform] -> `pj-lamped`
- `pj-battery` [consume] + `pj-lamped` [transform] -> `pj-wheel-box`


## `c-projector-lens` Bring the stars into focus
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Build reference](assets/items/star-projector.webp)

**Goals**
- Close the box with its lid -- `pj-closed`
- next: Fit the lens into its holder -- `pj-focus`
- next: Fit the holder to the box -- `pj-focused`
- next: Fit the hood around the lens -- `pj-hooded`
- next: Fit the handle to the spindle -- `star-projector`

**Items**
- `pj-lens` Lens
  - icon: ![Lens](assets/items/pj-lens.webp)

  {A pale blue-grey circular lens with a thin darker rim.}

  ---

  A single convex lens forms an inverted image of the lit holes.
- `pj-holder` Lens holder
  - icon: ![Lens holder](assets/items/pj-holder.webp)

  {A green ring stands on a small green frame between two red blocks.}

  ---

  A connected sliding carriage retained on its rails. Move it along the rails to focus.
- `pj-hood` Hood
  - icon: ![Hood](assets/items/pj-hood.webp)

  {A short black hollow tube has a stepped outer rim.}

  ---

  The dark tube surrounds the lens without covering its clear aperture.
- `pj-handle` Handle
  - icon: ![Handle](assets/items/pj-handle.webp)

  {A red wheel has a centre hole, a groove around its rim and a short green grip on its face.}

  ---

  The handwheel has a real belt groove behind its grip. It can be turned by hand now and driven by a belt later.
- `pj-lid` Lid
  - icon: ![Lid](assets/items/pj-lid.webp)

  {A flat tan lid has a narrow top slot and a shaped vertical tab hanging underneath.}

  ---

  One connected lid with locating tabs, shaft retainers and two downward tongues. The inner tongue carries the real projection window. Fit the lid before the external lens rails, which pass through its prepared openings.
- `pj-closed` Projector
  - icon: ![Projector](assets/items/pj-closed.webp)

  {A flat tan lid closes the box; its shaped front opening and projecting shaft remain exposed.}
- `pj-focus` Lens holder
  - icon: ![Lens holder](assets/items/pj-focus.webp)

  {A pale circular lens fills the green ring on the small green-and-red frame.}
- `pj-focused` Projector
  - icon: ![Projector](assets/items/pj-focused.webp)

  {The green-and-red lens frame sits around the front opening of the closed tan box.}
- `pj-hooded` Projector
  - icon: ![Projector](assets/items/pj-hooded.webp)

  {A short black tube projects from the green lens frame on the front of the box.}
- `star-projector` Star projector
  - icon: ![Star projector](assets/items/star-projector.webp)

  {A tan box has a black lens hood in a green-and-red frame. Below it, a long shaft ends in a red wheel with a small green grip.}

  ---

  Turning the disc brings new holes past the fixed aperture. Sliding the lens brings their projected image into focus. The optical model uses one ideal thin lens; brightness and real component tolerances are not measured.

**Combinations**
- `pj-lens` [consume] + `pj-holder` [transform] -> `pj-focus`
- `pj-lid` [consume] + `pj-wheel-box` [transform] -> `pj-closed`
- `pj-focus` [consume] + `pj-closed` [transform] -> `pj-focused`
- `pj-hood` [consume] + `pj-focused` [transform] -> `pj-hooded`
- `pj-handle` [consume] + `pj-hooded` [transform] -> `star-projector`

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

  {A broad flat tan rectangular board with small holes and a rectangular opening near one corner.}

  ---

  A 400 × 300 mm prepared plywood deck. The mounting holes and wire passages are already cut.
- `fc-arch-a` Arch
  - icon: ![Arch](assets/items/fc-arch-a.webp)

  {Two slim tan uprights joined by a tan crossbar, with green feet at their lower ends.}

  ---

  One connected rigid arch with two feet and captive bolts.
- `fc-arch-b` Arch
  - icon: ![Arch](assets/items/fc-arch-b.webp)

  {Two slim tan uprights joined by a tan crossbar, with green feet at their lower ends.}

  ---

  A second identical connected arch. Either arch fits either side of the deck.
- `fc-cradle` Tile cradle
  - icon: ![Tile cradle](assets/items/fc-cradle.webp)

  {An open green rectangular frame with projecting ends and small raised tabs.}

  ---

  One connected top cradle. Four integral saddles clip over the arches; its padded rails receive the tile.
- `fc-tile` Lift tile
  - icon: ![Lift tile](assets/items/fc-tile.webp)

  {A thick flat purple square.}

  ---

  This powered lift tile is explicitly fictional. Its limited force points upward while current flows. It makes no energy and carries no person.
- `fc-battery` Battery pack
  - icon: ![Battery pack](assets/items/fc-battery.webp)

  {A black rectangular box beneath a flat green top, with a thin dark lead beside it.}

  ---

  A compatible enclosed battery in its integral retained bracket. It mounts below the deck, keeping weight low.
- `fc-control` Lift control
  - icon: ![Lift control](assets/items/fc-control.webp)

  {A green box with two red buttons and thin dark leads; one lead rises far above the box.}

  ---

  A prepared controller and latching stop button in one pod with a connected fused harness. Keep power off while fitting it.
- `fc-one-arch` Frame
  - icon: ![Frame](assets/items/fc-one-arch.webp)

  {One tall tan arch stands along the far edge of a broad tan board, on two green feet.}
- `fc-arches` Frame
  - icon: ![Frame](assets/items/fc-arches.webp)

  {Two tall tan arches stand at opposite ends of a broad tan board, on four green feet.}
- `fc-top` Frame
  - icon: ![Frame](assets/items/fc-top.webp)

  {A green rectangular frame spans the tops of two tan arches above a broad tan board.}
- `fc-tiled` Frame
  - icon: ![Frame](assets/items/fc-tiled.webp)

  {A purple square rests in the green frame at the top of the tan arches.}
- `fc-inverted` Frame
  - icon: ![Frame](assets/items/fc-inverted.webp)

  {The construction is upside down: the broad tan board is on top and the purple square is below the arches.}
- `fc-powered` Frame
  - icon: ![Frame](assets/items/fc-powered.webp)

  {A black box on a green plate sits on the upward-facing tan board. The purple square is below.}
- `fc-upright` Frame
  - icon: ![Frame](assets/items/fc-upright.webp)

  {The tan board is below the arches again, with a purple square in the green frame above.}
- `fc-lift-frame` Frame
  - icon: ![Frame](assets/items/fc-lift-frame.webp)

  {A green box with two red buttons sits at the right of the tan board, beneath the purple-topped frame.}
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

  {An open green rectangular frame with black corner fittings and small dark pins on top.}

  ---

  One connected projector dock. Four feet bear on the deck and two recessed captive screws fasten it down. Four split snap studs pass through the original mounting holes; their flexible heads spring out above the box collars to retain the unchanged projector.
- `fc-motor` Gearmotor
  - icon: ![Gearmotor](assets/items/fc-motor.webp)

  {A black cylinder sits on a tall green pedestal. A dark shaft projects from its front and a thin lead extends behind.}

  ---

  An enclosed slow gearmotor with its integral pedestal and lead. The shaft is parallel to the projector spindle.
- `fc-pulley` Small pulley
  - icon: ![Small pulley](assets/items/fc-pulley.webp)

  {A thick red wheel with a groove around its edge and a round hole through its centre.}

  ---

  One small pulley with a captive screw that clamps onto the motor shaft flat.
- `fc-belt` Belt
  - icon: ![Belt](assets/items/fc-belt.webp)

  {One thin black loop, long and narrow with rounded ends.}

  ---

  One continuous soft belt. Its small pulley drives the larger grooved handwheel more slowly.
- `fc-motor-pack` Motor supply
  - icon: ![Motor supply](assets/items/fc-motor-pack.webp)

  {A small black rectangular box beneath a green top, with a fine dark lead extending beside it.}

  ---

  An enclosed low-voltage motor supply with its own switch, lead and integral mounting bracket. The lamp keeps its original supply; the lift has a separate circuit.
- `fc-docked` Frame
  - icon: ![Frame](assets/items/fc-docked.webp)

  {An open green rectangular frame sits on the tan board beside the green two-button box.}
- `fc-projector-aboard` Frame
  - icon: ![Frame](assets/items/fc-projector-aboard.webp)

  {A tan box stands in the frame beneath the purple square. Its front has a round dark lens fitting and a projecting red wheel.}
- `fc-drive` Drive motor
  - icon: ![Drive motor](assets/items/fc-drive.webp)

  {A small red grooved wheel surrounds the projecting shaft of a black cylinder on a green pedestal.}
- `fc-motor-mounted` Frame
  - icon: ![Frame](assets/items/fc-motor-mounted.webp)

  {The black cylinder on its green pedestal stands at the front right of the tan box, with its small red wheel facing outward.}
- `fc-belted` Frame
  - icon: ![Frame](assets/items/fc-belted.webp)

  {A thin dark belt stretches between the large red wheel on the tan box and the smaller wheel on the green pedestal.}
- `fc-drive-under` Frame
  - icon: ![Frame](assets/items/fc-drive-under.webp)

  {The construction is upside down. A black box on a green plate sits on the upward-facing board; the tan box and purple square are below.}
- `fc-supply-under` Frame
  - icon: ![Frame](assets/items/fc-supply-under.webp)

  {Two black boxes on green plates sit beside one another on the upward-facing board. The smaller box has a small coloured button on top.}
- `fc-powered-show` Frame
  - icon: ![Frame](assets/items/fc-powered-show.webp)

  {The tan box, two red wheels and dark belt sit beneath the purple-topped frame. A fine dark lead lies beside the right-hand controls.}
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

  {A long green panel with pointed ends, two keyhole-shaped openings and small fittings near its upper edge.}

  ---

  One cut whale side panel with its mounting tabs. Its top edge stays below the projector beam.
- `fc-side-b` Back side
  - icon: ![Back side](assets/items/fc-side-b.webp)

  {A long green panel with pointed ends, two keyhole-shaped openings and small projecting fittings near its upper edge.}

  ---

  A second whale side panel, fitted separately.
- `fc-tail` Tail
  - icon: ![Tail](assets/items/fc-tail.webp)

  {A flat red forked tail joined to a green rectangular socket.}

  ---

  One continuous fixed tail with its prepared root fitting. It does not steer or provide lift.
- `fc-fin-a` Front fin
  - icon: ![Front fin](assets/items/fc-fin-a.webp)

  {A broad red fin with a thick upper edge and two small green round fittings behind it.}

  ---

  One fixed fin with two integral mushroom studs and a captive centre screw. The keyhole entries sit below the deck. With the screw retracted, pass the heads through the wide openings and lower the fin into the narrow slots. Tighten the screw to retain it during flips. It gives the whale its shape, not lift.
- `fc-fin-b` Back fin
  - icon: ![Back fin](assets/items/fc-fin-b.webp)

  {A thin red fin seen almost edge-on, with two green round fittings along one edge.}

  ---

  The other fixed fin.
- `fc-near-side` Whale
  - icon: ![Whale](assets/items/fc-near-side.webp)

  {A long green panel with two keyhole-shaped openings covers the near edge of the tan board, below the wheels and belt.}
- `fc-side-rear` Whale
  - icon: ![Whale](assets/items/fc-side-rear.webp)

  {The plain tan back of the box faces us beneath the purple square. The two-button green control is at the left, and a green panel runs along the far board edge.}
- `fc-sided` Whale
  - icon: ![Whale](assets/items/fc-sided.webp)

  {Green panels line both long edges of the tan board; the near panel has two keyhole-shaped openings.}
- `fc-tailed` Whale
  - icon: ![Whale](assets/items/fc-tailed.webp)

  {From the back, a red forked tail projects to the left of the green-sided construction. The plain tan box face is visible beneath the purple square.}
- `fc-one-fin-b` Whale
  - icon: ![Whale](assets/items/fc-one-fin-b.webp)

  {A red fin projects from the nearer green panel, below the plain back of the tan box. The red forked tail extends to the left.}
- `fc-fin-front` Whale
  - icon: ![Whale](assets/items/fc-fin-front.webp)

  {The tan box’s lens fitting, red wheels and belt face us. The near green panel has two pale openings; a red forked tail extends to the right.}
- `fc-whale` Whale
  - icon: ![Whale](assets/items/fc-whale.webp)

  {A red fin projects from the near green side panel, below the wheels and belt. A red forked tail extends from the right end.}
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

  {A long tan bar joined to two short green uprights with flat green ends.}

  ---

  One connected landing skid with two upright legs and captive deck bolts.
- `fc-skid-b` Landing skid
  - icon: ![Landing skid](assets/items/fc-skid-b.webp)

  {A long tan bar joined to two short green uprights with flat green ends.}

  ---

  A second landing skid. Their feet reach below the batteries and trim weight.
- `fc-rail` Weight rail
  - icon: ![Weight rail](assets/items/fc-rail.webp)

  {A long green channel with an upright fitting at each end and a small red end piece.}

  ---

  One slotted rail with integral mounting ears, closed travel ends and a wide keyhole entry near the right end. The weight shoe enters through that opening from below.
- `fc-weight` Counterweight
  - icon: ![Counterweight](assets/items/fc-weight.webp)

  {A black rectangular block with a cream top and a raised green fitting.}

  ---

  A single sliding weight with a captive shoe, vertical clamp screw and washer. Raise the shoe through the wide rail entry, slide into the narrow track, then tighten the screw to clamp the rail between shoe and pad.
- `fc-guard` Guard
  - icon: ![Guard](assets/items/fc-guard.webp)

  {A long grey translucent cover with an open lower edge and green feet at its ends.}

  ---

  One hollow clear hood, open underneath and at the rear. Lower it over the drive, then tighten the captive screws on its exposed side feet. It encloses the belt and hand grip without covering the lens.
- `fc-whale-under` Whale
  - icon: ![Whale](assets/items/fc-whale-under.webp)

  {The whale-shaped construction is upside down. Black boxes and thin leads are visible on the upward-facing tan board; the purple square is below.}
- `fc-one-skid-a` Whale
  - icon: ![Whale](assets/items/fc-one-skid-a.webp)

  {On the upside-down construction, a long tan bar stands on two short green supports along the far side of the board.}
- `fc-one-skid-b` Whale
  - icon: ![Whale](assets/items/fc-one-skid-b.webp)

  {On the upside-down construction, a long tan bar stands on two short green supports along the near side of the board.}
- `fc-skids` Whale
  - icon: ![Whale](assets/items/fc-skids.webp)

  {Two long tan bars stand on green supports along opposite sides of the upward-facing board.}
- `fc-railed` Whale
  - icon: ![Whale](assets/items/fc-railed.webp)

  {A long green channel crosses the upward-facing board between the two raised tan bars.}
- `fc-weighted` Whale
  - icon: ![Whale](assets/items/fc-weighted.webp)

  {A small dark block with a red round fitting sits on the green channel between the raised tan bars.}
- `fc-standing` Whale
  - icon: ![Whale](assets/items/fc-standing.webp)

  {The whale-shaped construction stands upright on two tan bars. The purple square is above the tan box, wheels and belt.}
- `flying-whale` Whale
  - icon: ![Whale](assets/items/flying-whale.webp)

  {A grey translucent cover encloses the front wheels and belt. The green-sided machine has a red fin and forked tail, tan skids and a purple square above.}

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

## `c-end` The End
background: ![White instruction page](assets/backgrounds/white.svg)

“Can I have a go?”
