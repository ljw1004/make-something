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

  ---

  The paper sheet is already cut along four diagonals, stopping short of the centre. Curl the four pierced corners inward; keep the uncut centre whole.
- `pw-hub` Hub
  - icon: ![Teal hub](assets/items/pw-hub.webp) (center 140px, 460px)

  ---

  A hollow snap-in hub holds the folded corners together. Its centre is a bearing for the axle.
- `pw-axle` Axle
  - icon: ![Axle and spacer](assets/items/pw-axle.webp) (center 470px, 460px)

  ---

  A blunt axle with a built-in spacer and retaining tip. The hub turns around the axle; the spacer keeps the paper clear of the handle.
- `pw-handle` Handle
  - icon: ![Wooden handle with an open axle clip](assets/items/pw-handle.webp) (center 690px, 820px)

  ---

  The prepared clip snaps over the axle's rear post. Two small mounting holes remain near the foot of the handle.
- `pw-one-blade` Paper
  - icon: ![Paper with one folded corner](assets/items/pw-one-blade.webp)
- `pw-two-blades` Paper
  - icon: ![Paper with two folded corners](assets/items/pw-two-blades.webp)
- `pw-three-blades` Paper
  - icon: ![Paper with three folded corners](assets/items/pw-three-blades.webp)
- `pw-loose-rotor` Blades
  - icon: ![Folded paper](assets/items/pw-loose-rotor.webp)
- `pw-folded-rotor` Blades
  - icon: ![Blades with hub](assets/items/pw-folded-rotor.webp)
- `pw-rear-rotor` Blades
  - icon: ![Back of the blades](assets/items/pw-rear-rotor.webp)
- `pw-bearing-rotor` Blades
  - icon: ![Blades on their axle](assets/items/pw-bearing-rotor.webp)
- `pw-mounted` Pinwheel
  - icon: ![Back of the pinwheel](assets/items/pw-mounted.webp)
- `pinwheel` Pinwheel
  - icon: ![Pinwheel](assets/items/pinwheel.webp)

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
- `wr-mast-foot` Mast
  - icon: ![Mast](assets/items/wr-mast-foot.webp)
- `wr-mast-joint` Mast
  - icon: ![Mast](assets/items/wr-mast-joint.webp)
- `wr-mast-joint-foot` Mast
  - icon: ![Mast](assets/items/wr-mast-joint-foot.webp)
- `wr-frame` Mast
  - icon: ![Mast](assets/items/wr-frame.webp)
- `wr-ready` Mast
  - icon: ![Mast](assets/items/wr-ready.webp)
- `wr-frame-sail` Sail
  - icon: ![Sail](assets/items/wr-frame-sail.webp)
- `wr-sail` Sail
  - icon: ![Sail](assets/items/wr-sail.webp)
  - from chapter `c-racer-body` icon: ![Sail](assets/items/wr-sail-carried.webp)
- `wr-connector` Connector
  - icon: ![Connector](assets/items/wr-connector.webp)

  ---

  Two offset sockets keep the wooden rods from crossing through each other. Flexible ribs grip both rods.
- `wr-crossbar` Crossbar
  - icon: ![Crossbar](assets/items/wr-crossbar.webp)

  ---

  A short wooden rod that supports the bottom of the sail.
- `wr-foot` Foot
  - icon: ![Foot](assets/items/wr-foot.webp)

  ---

  The mast pushes into the top socket. The split legs underneath will snap into the chassis.
- `wr-sailcloth` Sail
  - icon: ![Sail](assets/items/wr-sailcloth.webp)

  ---

  Three small open clips are attached to the cloth. They press onto the mast and crossbar.
- `wr-crossbar-joint` Crossbar
  - icon: ![Crossbar](assets/items/wr-crossbar-joint.webp)

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
- `wr-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-chassis.webp)
- `wr-front-bearing-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-front-bearing-chassis.webp)
- `wr-rear-bearing-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-rear-bearing-chassis.webp)
- `wr-bearing-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-bearing-chassis.webp)
- `wr-front-rolling-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-front-rolling-chassis.webp)
- `wr-rear-rolling-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-rear-rolling-chassis.webp)
- `wr-front-wheel-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-front-wheel-chassis.webp)
- `wr-rear-wheel-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-rear-wheel-chassis.webp)
- `wr-rolling-chassis` Chassis
  - icon: ![Chassis](assets/items/wr-rolling-chassis.webp)
- `wr-upright` Chassis
  - icon: ![Chassis](assets/items/wr-upright.webp)
- `wind-racer` Wind racer
  - icon: ![Wind racer](assets/items/wind-racer.webp)

  ---

  The wheels turn together with each straw axle inside the bearings. Outdoors, moving air can push against the sail.
- `wr-flip` Flip
- `wr-front-bearing` Bearing
  - icon: ![Bearing](assets/items/wr-bearing.webp)

  ---

  An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.
- `wr-front-axle` Front straw
  - icon: ![Front straw](assets/items/wr-straw.webp)

  ---

  A stiff hollow plastic axle. Push one wheel onto each end.
- `wr-front-one-wheel` Front axle
  - icon: ![Front axle](assets/items/wr-one-wheel.webp)
- `wr-front-wheels` Front wheels
  - icon: ![Front wheels](assets/items/wr-wheels.webp)
- `wr-rear-bearing` Bearing
  - icon: ![Bearing](assets/items/wr-bearing.webp)

  ---

  An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.
- `wr-rear-axle` Rear straw
  - icon: ![Rear straw](assets/items/wr-straw.webp)

  ---

  A stiff hollow plastic axle. Push one wheel onto each end.
- `wr-rear-one-wheel` Rear axle
  - icon: ![Rear axle](assets/items/wr-one-wheel.webp)
- `wr-rear-wheels` Rear wheels
  - icon: ![Rear wheels](assets/items/wr-wheels.webp)
- `wr-wheel-1` Wheel
  - icon: ![Wheel](assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-2` Wheel
  - icon: ![Wheel](assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-3` Wheel
  - icon: ![Wheel](assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-4` Wheel
  - icon: ![Wheel](assets/items/wr-wheel.webp)

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
