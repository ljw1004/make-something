# ![A brick-red paper pinwheel](../../stories/builder/icon.png) A Fair in the Air
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)

Build toys that move, draw and shine—then make a little garden fair do something impossible.

## `c01` Something that moves
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Pinwheel](../../stories/builder/assets/items/pinwheel.webp)

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
  - icon: ![Dotted paper folding diagram](../../stories/builder/assets/actions/fold.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)
- `pw-flip` (center 130px, 216px)
  - icon: ![Outline diagram of turning a sheet over](../../stories/builder/assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `pw-fold` Fold
- `pw-flip` Flip
- `pw-paper` Paper
  - icon: ![Prepared paper square](../../stories/builder/assets/items/pw-paper.webp) (center 358px, 830px)

  ---

  The paper sheet is already cut along four diagonals, stopping short of the centre. Curl the four pierced corners inward; keep the uncut centre whole.
- `pw-hub` Hub
  - icon: ![Teal hub](../../stories/builder/assets/items/pw-hub.webp) (center 140px, 460px)

  ---

  A hollow snap-in hub holds the folded corners together. Its centre is a bearing for the axle.
- `pw-axle` Axle
  - icon: ![Axle and spacer](../../stories/builder/assets/items/pw-axle.webp) (center 470px, 460px)

  ---

  A blunt axle with a built-in spacer and retaining tip. The hub turns around the axle; the spacer keeps the paper clear of the handle.
- `pw-handle` Handle
  - icon: ![Wooden handle with an open axle clip](../../stories/builder/assets/items/pw-handle.webp) (center 690px, 820px)

  ---

  The prepared clip snaps over the axle's rear post. Two small mounting holes remain near the foot of the handle.
- `pw-one-blade` Paper
  - icon: ![Paper with one folded corner](../../stories/builder/assets/items/pw-one-blade.webp)
- `pw-two-blades` Paper
  - icon: ![Paper with two folded corners](../../stories/builder/assets/items/pw-two-blades.webp)
- `pw-three-blades` Paper
  - icon: ![Paper with three folded corners](../../stories/builder/assets/items/pw-three-blades.webp)
- `pw-loose-rotor` Blades
  - icon: ![Folded paper](../../stories/builder/assets/items/pw-loose-rotor.webp)
- `pw-folded-rotor` Blades
  - icon: ![Blades with hub](../../stories/builder/assets/items/pw-folded-rotor.webp)
- `pw-rear-rotor` Blades
  - icon: ![Back of the blades](../../stories/builder/assets/items/pw-rear-rotor.webp)
- `pw-bearing-rotor` Blades
  - icon: ![Blades on their axle](../../stories/builder/assets/items/pw-bearing-rotor.webp)
- `pw-mounted` Pinwheel
  - icon: ![Back of the pinwheel](../../stories/builder/assets/items/pw-mounted.webp)
- `pinwheel` Pinwheel
  - icon: ![Pinwheel](../../stories/builder/assets/items/pinwheel.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Completed sail](../../stories/builder/assets/items/wr-sail.webp)

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
  - icon: ![Mast](../../stories/builder/assets/items/wr-mast-wood.webp)
- `wr-mast-foot` Mast
  - icon: ![Mast](../../stories/builder/assets/items/wr-mast-foot.webp)
- `wr-mast-joint` Mast
  - icon: ![Mast](../../stories/builder/assets/items/wr-mast-joint.webp)
- `wr-mast-joint-foot` Mast
  - icon: ![Mast](../../stories/builder/assets/items/wr-mast-joint-foot.webp)
- `wr-frame` Mast
  - icon: ![Mast](../../stories/builder/assets/items/wr-frame.webp)
- `wr-ready` Mast
  - icon: ![Mast](../../stories/builder/assets/items/wr-ready.webp)
- `wr-frame-sail` Sail
  - icon: ![Sail](../../stories/builder/assets/items/wr-frame-sail.webp)
- `wr-sail` Sail
  - icon: ![Sail](../../stories/builder/assets/items/wr-sail.webp)
  - from chapter `c-racer-body` icon: ![Sail](../../stories/builder/assets/items/wr-sail-carried.webp)
- `wr-connector` Connector
  - icon: ![Connector](../../stories/builder/assets/items/wr-connector.webp)

  ---

  Two offset sockets keep the wooden rods from crossing through each other. Flexible ribs grip both rods.
- `wr-crossbar` Crossbar
  - icon: ![Crossbar](../../stories/builder/assets/items/wr-crossbar.webp)

  ---

  A short wooden rod that supports the bottom of the sail.
- `wr-foot` Foot
  - icon: ![Foot](../../stories/builder/assets/items/wr-foot.webp)

  ---

  The mast pushes into the top socket. The split legs underneath will snap into the chassis.
- `wr-sailcloth` Sail
  - icon: ![Sail](../../stories/builder/assets/items/wr-sailcloth.webp)

  ---

  Three small open clips are attached to the cloth. They press onto the mast and crossbar.
- `wr-crossbar-joint` Crossbar
  - icon: ![Crossbar](../../stories/builder/assets/items/wr-crossbar-joint.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Wind racer](../../stories/builder/assets/items/wind-racer.webp)

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
  - icon: ![Turn the chassis over](../../stories/builder/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `wr-chassis-top` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-chassis-top.webp)
- `wr-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-chassis.webp)
- `wr-front-bearing-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-front-bearing-chassis.webp)
- `wr-rear-bearing-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-rear-bearing-chassis.webp)
- `wr-bearing-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-bearing-chassis.webp)
- `wr-front-rolling-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-front-rolling-chassis.webp)
- `wr-rear-rolling-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-rear-rolling-chassis.webp)
- `wr-front-wheel-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-front-wheel-chassis.webp)
- `wr-rear-wheel-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-rear-wheel-chassis.webp)
- `wr-rolling-chassis` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-rolling-chassis.webp)
- `wr-upright` Chassis
  - icon: ![Chassis](../../stories/builder/assets/items/wr-upright.webp)
- `wind-racer` Wind racer
  - icon: ![Wind racer](../../stories/builder/assets/items/wind-racer.webp)

  ---

  The wheels turn together with each straw axle inside the bearings. Outdoors, moving air can push against the sail.
- `wr-flip` Flip
- `wr-front-bearing` Bearing
  - icon: ![Bearing](../../stories/builder/assets/items/wr-bearing.webp)

  ---

  An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.
- `wr-front-axle` Front straw
  - icon: ![Front straw](../../stories/builder/assets/items/wr-straw.webp)

  ---

  A stiff hollow plastic axle. Push one wheel onto each end.
- `wr-front-one-wheel` Front axle
  - icon: ![Front axle](../../stories/builder/assets/items/wr-one-wheel.webp)
- `wr-front-wheels` Front wheels
  - icon: ![Front wheels](../../stories/builder/assets/items/wr-wheels.webp)
- `wr-rear-bearing` Bearing
  - icon: ![Bearing](../../stories/builder/assets/items/wr-bearing.webp)

  ---

  An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.
- `wr-rear-axle` Rear straw
  - icon: ![Rear straw](../../stories/builder/assets/items/wr-straw.webp)

  ---

  A stiff hollow plastic axle. Push one wheel onto each end.
- `wr-rear-one-wheel` Rear axle
  - icon: ![Rear axle](../../stories/builder/assets/items/wr-one-wheel.webp)
- `wr-rear-wheels` Rear wheels
  - icon: ![Rear wheels](../../stories/builder/assets/items/wr-wheels.webp)
- `wr-wheel-1` Wheel
  - icon: ![Wheel](../../stories/builder/assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-2` Wheel
  - icon: ![Wheel](../../stories/builder/assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-3` Wheel
  - icon: ![Wheel](../../stories/builder/assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-4` Wheel
  - icon: ![Wheel](../../stories/builder/assets/items/wr-wheel.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Pinball table](../../stories/builder/assets/items/pinball-table.webp)

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
  - icon: ![Tray](../../stories/builder/assets/items/bf-pb-tray.webp)

  ---

  Prepared plywood with rail slots, flipper holes and integral carrying handles.
- `bf-pb-left-rail` Left rail
  - icon: ![Left rail](../../stories/builder/assets/items/bf-pb-left-rail.webp)
- `bf-pb-rail-1` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-rail-1.webp)
- `bf-pb-right-rail` Right rail
  - icon: ![Right rail](../../stories/builder/assets/items/bf-pb-right-rail.webp)
- `bf-pb-rail-2` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-rail-2.webp)
- `bf-pb-top-rail` Top rail
  - icon: ![Top rail](../../stories/builder/assets/items/bf-pb-top-rail.webp)
- `bf-pb-rail-3` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-rail-3.webp)
- `bf-pb-lane` Lane rail
  - icon: ![Lane rail](../../stories/builder/assets/items/bf-pb-lane.webp)
- `bf-pb-rail-4` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-rail-4.webp)
- `bf-pb-left-lip` Left return
  - icon: ![Left return](../../stories/builder/assets/items/bf-pb-left-lip.webp)
- `bf-pb-rail-5` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-rail-5.webp)
- `bf-pb-right-lip` Right return
  - icon: ![Right return](../../stories/builder/assets/items/bf-pb-right-lip.webp)
- `bf-pb-rail-6` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-rail-6.webp)
- `bf-pb-cup` Marble cup
  - icon: ![Marble cup](../../stories/builder/assets/items/bf-pb-cup.webp)
- `bf-pb-rimmed` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-rimmed.webp)

**Combinations**
- `bf-pb-left-rail` [consume] + `bf-pb-tray` [transform] -> `bf-pb-rail-1`
- `bf-pb-right-rail` [consume] + `bf-pb-rail-1` [transform] -> `bf-pb-rail-2`
- `bf-pb-top-rail` [consume] + `bf-pb-rail-2` [transform] -> `bf-pb-rail-3`
- `bf-pb-lane` [consume] + `bf-pb-rail-3` [transform] -> `bf-pb-rail-4`
- `bf-pb-left-lip` [consume] + `bf-pb-rail-4` [transform] -> `bf-pb-rail-5`
- `bf-pb-right-lip` [consume] + `bf-pb-rail-5` [transform] -> `bf-pb-rail-6`
- `bf-pb-cup` [consume] + `bf-pb-rail-6` [transform] -> `bf-pb-rimmed`


## `bf-pb-flippers` Two flippers
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Pinball table](../../stories/builder/assets/items/pinball-table.webp)

**Goals**
- Flip the Table -- `bf-pb-under`
- next: Fit the Pivot plate -- `bf-pb-plated-under`
- next: Fit the Support -- `bf-pb-supported-under`
- next: Flip the Table upright -- `bf-pb-upright`
- next: Fit the Left paddle -- `bf-pb-left`
- next: Fit the Right paddle -- `bf-pb-flipped`

**Hotspots**
- `bf-pb-flip` (center 130px, 216px)
  - icon: ![Flip](../../stories/builder/assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `bf-pb-rimmed` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-rimmed.webp)
- `bf-pb-flip` Flip
  - icon: ![Flip](../../stories/builder/assets/actions/flip.svg)
- `bf-pb-under` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-under.webp)
- `bf-pb-plate` Pivot plate
  - icon: ![Pivot plate](../../stories/builder/assets/items/bf-pb-plate.webp)

  ---

  One connected plate with retained spindles, finger buttons, keyed paddle fittings and return loops. Install beneath the tray before adding the paddles from above.
- `bf-pb-plated-under` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-plated-under.webp)
- `bf-pb-support` Support
  - icon: ![Support](../../stories/builder/assets/items/bf-pb-support.webp)

  ---

  One connected U-shaped support with locating tongues and retaining clips. It slopes the table towards its marble cup without tilting sideways.
- `bf-pb-supported-under` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-supported-under.webp)
- `bf-pb-upright` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-upright.webp)
- `bf-pb-left-paddle` Left paddle
  - icon: ![Left paddle](../../stories/builder/assets/items/bf-pb-left-paddle.webp)
- `bf-pb-left` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-left.webp)
- `bf-pb-right-paddle` Right paddle
  - icon: ![Right paddle](../../stories/builder/assets/items/bf-pb-right-paddle.webp)
- `bf-pb-flipped` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-flipped.webp)

**Combinations**
- `bf-pb-rimmed` [transform] @ `bf-pb-flip` -> `bf-pb-under`
- `bf-pb-plate` [consume] + `bf-pb-under` [transform] -> `bf-pb-plated-under`
- `bf-pb-support` [consume] + `bf-pb-plated-under` [transform] -> `bf-pb-supported-under`
- `bf-pb-supported-under` [transform] @ `bf-pb-flip` -> `bf-pb-upright`
- `bf-pb-left-paddle` [consume] + `bf-pb-upright` [transform] -> `bf-pb-left`
- `bf-pb-right-paddle` [consume] + `bf-pb-left` [transform] -> `bf-pb-flipped`


## `bf-pb-targets` One more go
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Pinball table](../../stories/builder/assets/items/pinball-table.webp)

**Goals**
- Fit the Spring inside the Launcher body -- `bf-pb-launcher`
- next: Fit the Launcher -- `bf-pb-launched`
- next: Fit the Lower arch -- `bf-pb-target-1`
- next: Fit the Middle arch -- `bf-pb-target-2`
- next: Fit the Upper arch -- `bf-pb-target-3`
- next: Fit the Score wheel -- `bf-pb-scored`
- next: Put the Marble in its cup -- `pinball-table`

**Items**
- `bf-pb-barrel` Launcher body
  - icon: ![Launcher body](../../stories/builder/assets/items/bf-pb-barrel.webp)

  ---

  A clear enclosing barrel with retained plunger and removable rear cap. Open the cap to fit the spring, then refit it; the spring remains visible and enclosed.
- `bf-pb-spring` Spring
  - icon: ![Spring](../../stories/builder/assets/items/bf-pb-spring.webp)
- `bf-pb-launcher` Launcher
  - icon: ![Launcher](../../stories/builder/assets/items/bf-pb-launcher.webp)
- `bf-pb-flipped` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-flipped.webp)
- `bf-pb-launched` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-launched.webp)
- `bf-pb-arch-low` Lower arch
  - icon: ![Lower arch](../../stories/builder/assets/items/bf-pb-arch-low.webp)
- `bf-pb-target-1` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-target-1.webp)
- `bf-pb-arch-mid` Middle arch
  - icon: ![Middle arch](../../stories/builder/assets/items/bf-pb-arch-mid.webp)
- `bf-pb-target-2` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-target-2.webp)
- `bf-pb-arch-high` Upper arch
  - icon: ![Upper arch](../../stories/builder/assets/items/bf-pb-arch-high.webp)
- `bf-pb-target-3` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-target-3.webp)
- `bf-pb-score` Score wheel
  - icon: ![Score wheel](../../stories/builder/assets/items/bf-pb-score.webp)
- `bf-pb-scored` Table
  - icon: ![Table](../../stories/builder/assets/items/bf-pb-scored.webp)
- `bf-pb-marble` Marble
  - icon: ![Marble](../../stories/builder/assets/items/bf-pb-marble.webp)
- `pinball-table` Pinball table
  - icon: ![Pinball table](../../stories/builder/assets/items/pinball-table.webp)

**Combinations**
- `bf-pb-spring` [consume] + `bf-pb-barrel` [transform] -> `bf-pb-launcher`
- `bf-pb-launcher` [consume] + `bf-pb-flipped` [transform] -> `bf-pb-launched`
- `bf-pb-arch-low` [consume] + `bf-pb-launched` [transform] -> `bf-pb-target-1`
- `bf-pb-arch-mid` [consume] + `bf-pb-target-1` [transform] -> `bf-pb-target-2`
- `bf-pb-arch-high` [consume] + `bf-pb-target-2` [transform] -> `bf-pb-target-3`
- `bf-pb-score` [consume] + `bf-pb-target-3` [transform] -> `bf-pb-scored`
- `bf-pb-marble` [consume] + `bf-pb-scored` [transform] -> `pinball-table`

## `bf-cd-crank` Round and round
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Crank dragon](../../stories/builder/assets/items/crank-dragon.webp)

**Goals**
- Fit the Front bearing -- `bf-cd-bearing-1`
- next: Fit the Rear bearing -- `bf-cd-bearings`
- next: Slide the Shaft through the bearings -- `bf-cd-shafted`
- next: Fit the Cam to the Shaft -- `bf-cd-cammed`
- next: Fit the Crank -- `bf-cd-cranked`

**Items**
- `bf-cd-base` Base
  - icon: ![Base](../../stories/builder/assets/items/bf-cd-base.webp)
- `bf-cd-front-bearing` Front bearing
  - icon: ![Front bearing](../../stories/builder/assets/items/bf-cd-front-bearing.webp)
- `bf-cd-bearing-1` Frame
  - icon: ![Frame](../../stories/builder/assets/items/bf-cd-bearing-1.webp)
- `bf-cd-rear-bearing` Rear bearing
  - icon: ![Rear bearing](../../stories/builder/assets/items/bf-cd-rear-bearing.webp)
- `bf-cd-bearings` Frame
  - icon: ![Frame](../../stories/builder/assets/items/bf-cd-bearings.webp)
- `bf-cd-shaft` Shaft
  - icon: ![Shaft](../../stories/builder/assets/items/bf-cd-shaft.webp)
- `bf-cd-shafted` Frame
  - icon: ![Frame](../../stories/builder/assets/items/bf-cd-shafted.webp)
- `bf-cd-cam` Cam
  - icon: ![Cam](../../stories/builder/assets/items/bf-cd-cam.webp)

  ---

  The shaft hole sits off centre. Turning the round disc raises and lowers the broad follower foot.
- `bf-cd-cammed` Frame
  - icon: ![Frame](../../stories/builder/assets/items/bf-cd-cammed.webp)
- `bf-cd-handle` Crank
  - icon: ![Crank](../../stories/builder/assets/items/bf-cd-handle.webp)
- `bf-cd-cranked` Frame
  - icon: ![Frame](../../stories/builder/assets/items/bf-cd-cranked.webp)

**Combinations**
- `bf-cd-front-bearing` [consume] + `bf-cd-base` [transform] -> `bf-cd-bearing-1`
- `bf-cd-rear-bearing` [consume] + `bf-cd-bearing-1` [transform] -> `bf-cd-bearings`
- `bf-cd-shaft` [consume] + `bf-cd-bearings` [transform] -> `bf-cd-shafted`
- `bf-cd-cam` [consume] + `bf-cd-shafted` [transform] -> `bf-cd-cammed`
- `bf-cd-handle` [consume] + `bf-cd-cammed` [transform] -> `bf-cd-cranked`


## `bf-cd-lift` Round becomes up
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Crank dragon](../../stories/builder/assets/items/crank-dragon.webp)

**Goals**
- Slide the Follower into the Guide -- `bf-cd-open-follower`
- next: Snap on the Cover -- `bf-cd-guided`
- next: Mount the Follower above the Cam -- `bf-cd-mounted`
- next: Hook on the Spring -- `bf-cd-lifter`

**Items**
- `bf-cd-guide` Guide
  - icon: ![Guide](../../stories/builder/assets/items/bf-cd-guide.webp)

  ---

  An open square channel with a mounting foot and spring anchor. The separate cover closes around the follower; its broad foot never has to pass through the narrow channel.
- `bf-cd-follower` Follower
  - icon: ![Follower](../../stories/builder/assets/items/bf-cd-follower.webp)

  ---

  A sliding rod with a broad cam foot, spring collar and retained crosshead pin for two independently pivoting links.
- `bf-cd-open-follower` Follower
  - icon: ![Follower](../../stories/builder/assets/items/bf-cd-open-follower.webp)
- `bf-cd-cover` Cover
  - icon: ![Cover](../../stories/builder/assets/items/bf-cd-cover.webp)
- `bf-cd-guided` Follower
  - icon: ![Follower](../../stories/builder/assets/items/bf-cd-guided.webp)
- `bf-cd-cranked` Frame
  - icon: ![Frame](../../stories/builder/assets/items/bf-cd-cranked.webp)
- `bf-cd-mounted` Lifter
  - icon: ![Lifter](../../stories/builder/assets/items/bf-cd-mounted.webp)
- `bf-cd-spring` Spring
  - icon: ![Spring](../../stories/builder/assets/items/bf-cd-spring.webp)
- `bf-cd-lifter` Lifter
  - icon: ![Lifter](../../stories/builder/assets/items/bf-cd-lifter.webp)

**Combinations**
- `bf-cd-follower` [consume] + `bf-cd-guide` [transform] -> `bf-cd-open-follower`
- `bf-cd-cover` [consume] + `bf-cd-open-follower` [transform] -> `bf-cd-guided`
- `bf-cd-guided` [consume] + `bf-cd-cranked` [transform] -> `bf-cd-mounted`
- `bf-cd-spring` [consume] + `bf-cd-mounted` [transform] -> `bf-cd-lifter`


## `bf-cd-dragon` The dragon
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Crank dragon](../../stories/builder/assets/items/crank-dragon.webp)

**Goals**
- Attach the Left wing -- `bf-cd-body-left`
- next: Attach the Right wing -- `bf-cd-winged`
- next: Attach the Tail -- `bf-cd-bodied`
- next: Mount the Dragon on the Lifter -- `bf-cd-mounted-body`
- next: Fit the Left link -- `bf-cd-linked-left`
- next: Fit the Right link -- `crank-dragon`

**Items**
- `bf-cd-body` Body
  - icon: ![Body](../../stories/builder/assets/items/bf-cd-body.webp)
- `bf-cd-left-wing` Left wing
  - icon: ![Left wing](../../stories/builder/assets/items/bf-cd-left-wing.webp)

  ---

  One card wing with its own retained hinge pin, spacer and washer.
- `bf-cd-body-left` Body
  - icon: ![Body](../../stories/builder/assets/items/bf-cd-body-left.webp)
- `bf-cd-right-wing` Right wing
  - icon: ![Right wing](../../stories/builder/assets/items/bf-cd-right-wing.webp)

  ---

  One card wing with its own retained hinge pin, spacer and washer.
- `bf-cd-winged` Body
  - icon: ![Body](../../stories/builder/assets/items/bf-cd-winged.webp)
- `bf-cd-tail` Tail
  - icon: ![Tail](../../stories/builder/assets/items/bf-cd-tail.webp)
- `bf-cd-bodied` Dragon
  - icon: ![Dragon](../../stories/builder/assets/items/bf-cd-bodied.webp)
- `bf-cd-lifter` Lifter
  - icon: ![Lifter](../../stories/builder/assets/items/bf-cd-lifter.webp)
- `bf-cd-mounted-body` Dragon
  - icon: ![Dragon](../../stories/builder/assets/items/bf-cd-mounted-body.webp)
- `bf-cd-left-link` Left link
  - icon: ![Left link](../../stories/builder/assets/items/bf-cd-left-link.webp)

  ---

  One rigid 55 mm link with pivot eyes. It fits the wing pin and the shared follower pin.
- `bf-cd-linked-left` Dragon
  - icon: ![Dragon](../../stories/builder/assets/items/bf-cd-linked-left.webp)
- `bf-cd-right-link` Right link
  - icon: ![Right link](../../stories/builder/assets/items/bf-cd-right-link.webp)

  ---

  One rigid 55 mm link with pivot eyes. It pivots independently beside the other link.
- `crank-dragon` Crank dragon
  - icon: ![Crank dragon](../../stories/builder/assets/items/crank-dragon.webp)

**Combinations**
- `bf-cd-left-wing` [consume] + `bf-cd-body` [transform] -> `bf-cd-body-left`
- `bf-cd-right-wing` [consume] + `bf-cd-body-left` [transform] -> `bf-cd-winged`
- `bf-cd-tail` [consume] + `bf-cd-winged` [transform] -> `bf-cd-bodied`
- `bf-cd-bodied` [consume] + `bf-cd-lifter` [transform] -> `bf-cd-mounted-body`
- `bf-cd-left-link` [consume] + `bf-cd-mounted-body` [transform] -> `bf-cd-linked-left`
- `bf-cd-right-link` [consume] + `bf-cd-linked-left` [transform] -> `crank-dragon`

## `bf-pe-build` A look over the hedge
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Periscope](../../stories/builder/assets/items/periscope.webp)

**Goals**
- Fold the first side -- `bf-pe-fold-1`
- next: Fold the second side -- `bf-pe-fold-2`
- next: Fold and close the long seam -- `bf-pe-tube`
- next: Fit the Upper mirror -- `bf-pe-upper-fit`
- next: Fit the Lower mirror -- `bf-pe-mirrored`
- next: Fold the bottom closed -- `bf-pe-bottom`
- next: Fold the top closed -- `bf-pe-closed`
- next: Fit the Top shade -- `bf-pe-shaded`
- next: Fit the Eye shade -- `periscope`

**Hotspots**
- `bf-pe-fold` (center 130px, 216px)
  - icon: ![Fold](../../stories/builder/assets/actions/fold.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `bf-pe-net` Tube net
  - icon: ![Tube net](../../stories/builder/assets/items/bf-pe-net.webp)

  ---

  One scored card net with dark inner faces, two end flaps, mirror ledges and prepared adhesive seam tabs. The end flaps stay open while you fit the mirrors.
- `bf-pe-fold` Fold
  - icon: ![Fold](../../stories/builder/assets/actions/fold.svg)
- `bf-pe-fold-1` Tube
  - icon: ![Tube](../../stories/builder/assets/items/bf-pe-fold-1.webp)
- `bf-pe-fold-2` Tube
  - icon: ![Tube](../../stories/builder/assets/items/bf-pe-fold-2.webp)
- `bf-pe-tube` Tube
  - icon: ![Tube](../../stories/builder/assets/items/bf-pe-tube.webp)
- `bf-pe-upper` Upper mirror
  - icon: ![Upper mirror](../../stories/builder/assets/items/bf-pe-upper.webp)

  ---

  An unbreakable mirror with retained edge clips. It seats on the upper forty-five-degree ledges.
- `bf-pe-upper-fit` Tube
  - icon: ![Tube](../../stories/builder/assets/items/bf-pe-upper-fit.webp)
- `bf-pe-lower` Lower mirror
  - icon: ![Lower mirror](../../stories/builder/assets/items/bf-pe-lower.webp)

  ---

  A matching mirror in retained clips. Its reflecting face remains parallel to the upper mirror, redirecting the light towards your eye.
- `bf-pe-mirrored` Tube
  - icon: ![Tube](../../stories/builder/assets/items/bf-pe-mirrored.webp)
- `bf-pe-bottom` Tube
  - icon: ![Tube](../../stories/builder/assets/items/bf-pe-bottom.webp)
- `bf-pe-closed` Tube
  - icon: ![Tube](../../stories/builder/assets/items/bf-pe-closed.webp)
- `bf-pe-top-shade` Top shade
  - icon: ![Top shade](../../stories/builder/assets/items/bf-pe-top-shade.webp)
- `bf-pe-shaded` Tube
  - icon: ![Tube](../../stories/builder/assets/items/bf-pe-shaded.webp)
- `bf-pe-eye-shade` Eye shade
  - icon: ![Eye shade](../../stories/builder/assets/items/bf-pe-eye-shade.webp)
- `periscope` Periscope
  - icon: ![Periscope](../../stories/builder/assets/items/periscope.webp)

**Combinations**
- `bf-pe-net` [transform] @ `bf-pe-fold` -> `bf-pe-fold-1`
- `bf-pe-fold-1` [transform] @ `bf-pe-fold` -> `bf-pe-fold-2`
- `bf-pe-fold-2` [transform] @ `bf-pe-fold` -> `bf-pe-tube`
- `bf-pe-upper` [consume] + `bf-pe-tube` [transform] -> `bf-pe-upper-fit`
- `bf-pe-lower` [consume] + `bf-pe-upper-fit` [transform] -> `bf-pe-mirrored`
- `bf-pe-mirrored` [transform] @ `bf-pe-fold` -> `bf-pe-bottom`
- `bf-pe-bottom` [transform] @ `bf-pe-fold` -> `bf-pe-closed`
- `bf-pe-top-shade` [consume] + `bf-pe-closed` [transform] -> `bf-pe-shaded`
- `bf-pe-eye-shade` [consume] + `bf-pe-shaded` [transform] -> `periscope`

## `bf-ka-mirrors` Three mirrors
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Kaleidoscope](../../stories/builder/assets/items/kaleidoscope.webp)

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
  - icon: ![Fold](../../stories/builder/assets/actions/fold.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `bf-ka-backing` Backing
  - icon: ![Backing](../../stories/builder/assets/items/bf-ka-backing.webp)

  ---

  One continuous scored binding sheet. Its three adhesive panels hold the mirror backs; the flexible seams become hinges.
- `bf-ka-mirror-1` Mirror
  - icon: ![Mirror](../../stories/builder/assets/items/bf-ka-mirror-1.webp)
- `bf-ka-mirrors-1` Mirrors
  - icon: ![Mirrors](../../stories/builder/assets/items/bf-ka-mirrors-1.webp)
- `bf-ka-mirror-2` Mirror
  - icon: ![Mirror](../../stories/builder/assets/items/bf-ka-mirror-2.webp)
- `bf-ka-mirrors-2` Mirrors
  - icon: ![Mirrors](../../stories/builder/assets/items/bf-ka-mirrors-2.webp)
- `bf-ka-mirror-3` Mirror
  - icon: ![Mirror](../../stories/builder/assets/items/bf-ka-mirror-3.webp)
- `bf-ka-mirrors-3` Mirrors
  - icon: ![Mirrors](../../stories/builder/assets/items/bf-ka-mirrors-3.webp)
- `bf-ka-fold` Fold
  - icon: ![Fold](../../stories/builder/assets/actions/fold.svg)
- `bf-ka-prism` Mirror triangle
  - icon: ![Mirror triangle](../../stories/builder/assets/items/bf-ka-prism.webp)
- `bf-ka-tube` Viewing tube
  - icon: ![Viewing tube](../../stories/builder/assets/items/bf-ka-tube.webp)

  ---

  A prepared protective tube with a dark eyecap, padded mirror supports and a retained turning collar.
- `bf-ka-viewer` Viewing tube
  - icon: ![Viewing tube](../../stories/builder/assets/items/bf-ka-viewer.webp)
- `bf-ka-only-2` Mirrors
  - icon: ![Mirrors](../../stories/builder/assets/items/bf-ka-only-2.webp)
- `bf-ka-only-3` Mirrors
  - icon: ![Mirrors](../../stories/builder/assets/items/bf-ka-only-3.webp)
- `bf-ka-pair-13` Mirrors
  - icon: ![Mirrors](../../stories/builder/assets/items/bf-ka-pair-13.webp)
- `bf-ka-pair-23` Mirrors
  - icon: ![Mirrors](../../stories/builder/assets/items/bf-ka-pair-23.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Kaleidoscope](../../stories/builder/assets/items/kaleidoscope.webp)

**Goals**
- Put the Triangle in the Colour cell -- `bf-ka-colour-1`
- next: Add the Crescent -- `bf-ka-colour-2`
- next: Add the Disc -- `bf-ka-colour-3`
- next: Snap on the Clear lid -- `bf-ka-lidded`
- next: Fit the Light cover -- `bf-ka-covered`
- next: Fit the Colour cell to the Viewing tube -- `kaleidoscope`

**Items**
- `bf-ka-cell` Colour cell
  - icon: ![Colour cell](../../stories/builder/assets/items/bf-ka-cell.webp)

  ---

  A connected clear-bottomed cell with a rotating collar fitting. Its separate snap lid leaves space for the coloured pieces to tumble.
- `bf-ka-triangle` Triangle
  - icon: ![Triangle](../../stories/builder/assets/items/bf-ka-triangle.webp)
- `bf-ka-colour-1` Colour cell
  - icon: ![Colour cell](../../stories/builder/assets/items/bf-ka-colour-1.webp)
- `bf-ka-crescent` Crescent
  - icon: ![Crescent](../../stories/builder/assets/items/bf-ka-crescent.webp)
- `bf-ka-colour-2` Colour cell
  - icon: ![Colour cell](../../stories/builder/assets/items/bf-ka-colour-2.webp)
- `bf-ka-disc` Disc
  - icon: ![Disc](../../stories/builder/assets/items/bf-ka-disc.webp)
- `bf-ka-colour-3` Colour cell
  - icon: ![Colour cell](../../stories/builder/assets/items/bf-ka-colour-3.webp)
- `bf-ka-lid` Clear lid
  - icon: ![Clear lid](../../stories/builder/assets/items/bf-ka-lid.webp)
- `bf-ka-lidded` Colour cell
  - icon: ![Colour cell](../../stories/builder/assets/items/bf-ka-lidded.webp)
- `bf-ka-diffuser` Light cover
  - icon: ![Light cover](../../stories/builder/assets/items/bf-ka-diffuser.webp)
- `bf-ka-covered` Colour cell
  - icon: ![Colour cell](../../stories/builder/assets/items/bf-ka-covered.webp)
- `bf-ka-viewer` Viewing tube
  - icon: ![Viewing tube](../../stories/builder/assets/items/bf-ka-viewer.webp)
- `kaleidoscope` Kaleidoscope
  - icon: ![Kaleidoscope](../../stories/builder/assets/items/kaleidoscope.webp)

**Combinations**
- `bf-ka-triangle` [consume] + `bf-ka-cell` [transform] -> `bf-ka-colour-1`
- `bf-ka-crescent` [consume] + `bf-ka-colour-1` [transform] -> `bf-ka-colour-2`
- `bf-ka-disc` [consume] + `bf-ka-colour-2` [transform] -> `bf-ka-colour-3`
- `bf-ka-lid` [consume] + `bf-ka-colour-3` [transform] -> `bf-ka-lidded`
- `bf-ka-diffuser` [consume] + `bf-ka-lidded` [transform] -> `bf-ka-covered`
- `bf-ka-covered` [consume] + `bf-ka-viewer` [transform] -> `kaleidoscope`

## `c-gantry-frame` A lifting frame
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Gantry](../../stories/builder/assets/items/gh-mounted.webp)

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
  - icon: ![Base](../../stories/builder/assets/items/gh-base.webp)
- `gh-side-1` Side frame
  - icon: ![Side frame](../../stories/builder/assets/items/gh-side-1.webp)

  ---

  A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.

- `gh-side-2` Side frame
  - icon: ![Side frame](../../stories/builder/assets/items/gh-side-2.webp)

  ---

  A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.

- `gh-crossbeam` Beam
  - icon: ![Beam](../../stories/builder/assets/items/gh-crossbeam.webp)

  ---

  The beam has two end sockets and separate sockets underneath for the pulley forks.

- `gh-one-side` Frame
  - icon: ![Frame](../../stories/builder/assets/items/gh-one-side.webp)
- `gh-two-sides` Frame
  - icon: ![Frame](../../stories/builder/assets/items/gh-two-sides.webp)
- `gh-frame` Frame
  - icon: ![Frame](../../stories/builder/assets/items/gh-frame.webp)
- `gh-drum` Winch
  - icon: ![Winch](../../stories/builder/assets/items/gh-drum.webp)

  ---

  The winch drum comes with its axle, two bearing cheeks and captive base fasteners.

- `gh-ratchet` Ratchet
  - icon: ![Ratchet](../../stories/builder/assets/items/gh-ratchet.webp)
- `gh-crank` Crank
  - icon: ![Crank](../../stories/builder/assets/items/gh-crank.webp)
- `gh-ratchet-winch` Winch
  - icon: ![Winch](../../stories/builder/assets/items/gh-ratchet-winch.webp)
- `gh-crank-winch` Winch
  - icon: ![Winch](../../stories/builder/assets/items/gh-crank-winch.webp)
- `gh-winch` Winch
  - icon: ![Winch](../../stories/builder/assets/items/gh-winch.webp)
- `gh-mounted` Gantry
  - icon: ![Gantry](../../stories/builder/assets/items/gh-mounted.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Gantry hoist](../../stories/builder/assets/items/gantry-hoist.webp)

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
  - icon: ![Side fork](../../stories/builder/assets/items/gh-side-fork.webp)

  ---

  An open pulley bracket with a split snap axle and a mounting peg. Press a pulley over the tapered axle tip before mounting the bracket.

- `gh-side-pulley` Pulley unit
  - icon: ![Pulley unit](../../stories/builder/assets/items/gh-side-pulley.webp)
- `gh-drop-fork` Drop fork
  - icon: ![Drop fork](../../stories/builder/assets/items/gh-drop-fork.webp)

  ---

  An open pulley bracket with a split snap axle and a mounting peg. Press a pulley over the tapered axle tip before mounting the bracket.

- `gh-drop-pulley` Pulley unit
  - icon: ![Pulley unit](../../stories/builder/assets/items/gh-drop-pulley.webp)
- `gh-pulley-1` Pulley
  - icon: ![Pulley](../../stories/builder/assets/items/gh-pulley-1.webp)

  ---

  A grooved pulley that turns on either fork axle. The split axle tip retains it.

- `gh-pulley-2` Pulley
  - icon: ![Pulley](../../stories/builder/assets/items/gh-pulley-2.webp)

  ---

  A grooved pulley that turns on either fork axle. The split axle tip retains it.

- `gh-pawl` Pawl
  - icon: ![Pawl](../../stories/builder/assets/items/gh-pawl.webp)

  ---

  A spring pawl and its connected mounting foot. Its tooth rests in the ratchet so the drum cannot freely unwind.

- `gh-rope` Rope and hook
  - icon: ![Rope and hook](../../stories/builder/assets/items/gh-rope.webp)

  ---

  One continuous cord, already tied to its hook. Fasten its free end to the drum and thread it over the two pulleys.

- `gh-basket` Basket
  - icon: ![Basket](../../stories/builder/assets/items/gh-basket.webp)

  ---

  A small rigid basket with a connected lifting handle. It hangs directly on the hook.

- `gh-fitted-1` Gantry
  - icon: ![Gantry](../../stories/builder/assets/items/gh-fitted-1.webp)
- `gh-fitted-2` Gantry
  - icon: ![Gantry](../../stories/builder/assets/items/gh-fitted-2.webp)
- `gh-fitted-3` Gantry
  - icon: ![Gantry](../../stories/builder/assets/items/gh-fitted-3.webp)
- `gh-fitted-4` Gantry
  - icon: ![Gantry](../../stories/builder/assets/items/gh-fitted-4.webp)
- `gh-fitted-5` Gantry
  - icon: ![Gantry](../../stories/builder/assets/items/gh-fitted-5.webp)
- `gh-fitted-6` Gantry
  - icon: ![Gantry](../../stories/builder/assets/items/gh-fitted-6.webp)
- `gh-fitted-7` Gantry
  - icon: ![Gantry](../../stories/builder/assets/items/gh-fitted-7.webp)
- `gh-roped` Hoist
  - icon: ![Hoist](../../stories/builder/assets/items/gh-roped.webp)
- `gantry-hoist` Gantry hoist
  - icon: ![Gantry hoist](../../stories/builder/assets/items/gantry-hoist.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Carousel](../../stories/builder/assets/items/ca-platform.webp)

**Goals**
- Fit the spindle
  - either: `ca-spindle-base`
  - or: `ca-drive-base`
- next: Fit the motor -- `ca-drive-base`
- next: Loop the belt around both pulleys -- `ca-belted`
- next: Clip the guard over the drive
  - either: `ca-guarded`
  - or: `ca-ready`
- next: Plug in the battery -- `ca-ready`
- next: Fit the deck onto the spindle -- `ca-platform`

**Items**
- `ca-base` Base
  - icon: ![Base](../../stories/builder/assets/items/ca-base.webp)

  ---

  A broad prepared base with sockets for the bearing, motor and battery. The motor and controller are matching low-voltage modules.

- `ca-spindle` Spindle
  - icon: ![Spindle](../../stories/builder/assets/items/ca-spindle.webp)

  ---

  A vertical spindle and pulley retained inside a bearing block. The square upper end drives the deck.

- `ca-motor` Motor
  - icon: ![Motor](../../stories/builder/assets/items/ca-motor.webp)

  ---

  A small enclosed geared motor, its pulley, retaining strap, mounting foot and plugged lead form one supplied module.

- `ca-belt` Belt
  - icon: ![Belt](../../stories/builder/assets/items/ca-belt.webp)
- `ca-guard` Guard
  - icon: ![Guard](../../stories/builder/assets/items/ca-guard.webp)

  ---

  A clear cover with a real shaft opening, cable opening and attached snap feet.

- `ca-battery` Battery and dial
  - icon: ![Battery and dial](../../stories/builder/assets/items/ca-battery.webp)

  ---

  The battery holder, switch and speed dial share one case. Its connected lead plugs into the motor.

- `ca-deck` Deck
  - icon: ![Deck](../../stories/builder/assets/items/ca-deck.webp)

  ---

  A round deck with a central drive socket and three prepared pole sockets.

- `ca-spindle-base` Base
  - icon: ![Base](../../stories/builder/assets/items/ca-spindle-base.webp)
- `ca-motor-base` Base
  - icon: ![Base](../../stories/builder/assets/items/ca-motor-base.webp)
- `ca-drive-base` Base
  - icon: ![Base](../../stories/builder/assets/items/ca-drive-base.webp)
- `ca-belted` Base
  - icon: ![Base](../../stories/builder/assets/items/ca-belted.webp)
- `ca-guarded` Base
  - icon: ![Base](../../stories/builder/assets/items/ca-guarded.webp)
- `ca-wired` Base
  - icon: ![Base](../../stories/builder/assets/items/ca-wired.webp)
- `ca-ready` Base
  - icon: ![Base](../../stories/builder/assets/items/ca-ready.webp)
- `ca-platform` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-platform.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Electric carousel](../../stories/builder/assets/items/electric-carousel.webp)

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
  - icon: ![Red horse](../../stories/builder/assets/items/ca-horse-1.webp)

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-1` Pole
  - icon: ![Pole](../../stories/builder/assets/items/ca-pole-1.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-1` Red horse
  - icon: ![Red horse](../../stories/builder/assets/items/ca-rider-1.webp)
- `ca-horse-2` Green horse
  - icon: ![Green horse](../../stories/builder/assets/items/ca-horse-2.webp)

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-2` Pole
  - icon: ![Pole](../../stories/builder/assets/items/ca-pole-2.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-2` Green horse
  - icon: ![Green horse](../../stories/builder/assets/items/ca-rider-2.webp)
- `ca-horse-3` Cream horse
  - icon: ![Cream horse](../../stories/builder/assets/items/ca-horse-3.webp)

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-3` Pole
  - icon: ![Pole](../../stories/builder/assets/items/ca-pole-3.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-3` Cream horse
  - icon: ![Cream horse](../../stories/builder/assets/items/ca-rider-3.webp)
- `ca-horses-1` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-horses-1.webp)
- `ca-horses-2` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-horses-2.webp)
- `ca-horses-3` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-horses-3.webp)
- `ca-horses-4` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-horses-4.webp)
- `ca-horses-5` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-horses-5.webp)
- `ca-horses-6` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-horses-6.webp)
- `ca-horses-7` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-horses-7.webp)
- `ca-roofpost` Roof post
  - icon: ![Roof post](../../stories/builder/assets/items/ca-roofpost.webp)
- `ca-canopy` Canopy
  - icon: ![Canopy](../../stories/builder/assets/items/ca-canopy.webp)

  ---

  A small moulded canopy with a centre socket. It sits high enough to leave the horses visible.

- `ca-posted` Carousel
  - icon: ![Carousel](../../stories/builder/assets/items/ca-posted.webp)
- `electric-carousel` Electric carousel
  - icon: ![Electric carousel](../../stories/builder/assets/items/electric-carousel.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Claw](../../stories/builder/assets/items/cl-mechanical.webp)

**Goals**
- Fit a pad to the left jaw
  - either: `cl-padded-jaw-1`
  - or: `cl-mech-1`
  - or: `cl-mech-3`
  - or: `cl-mech-5`
  - or: `cl-mech-7`
  - or: `cl-mech-13`
  - or: `cl-mech-15`
  - or: `cl-mech-23`
  - or: `cl-mechanical`
- next: Fit the left jaw
  - either: `cl-mech-1`
  - or: `cl-mech-3`
  - or: `cl-mech-5`
  - or: `cl-mech-7`
  - or: `cl-mech-13`
  - or: `cl-mech-15`
  - or: `cl-mech-23`
  - or: `cl-mechanical`
- next: Fit the other pad
  - either: `cl-padded-jaw-2`
  - or: `cl-mech-2`
  - or: `cl-mech-3`
  - or: `cl-mech-6`
  - or: `cl-mech-7`
  - or: `cl-mech-15`
  - or: `cl-mech-22`
  - or: `cl-mech-23`
  - or: `cl-mechanical`
- next: Fit the right jaw
  - either: `cl-mech-2`
  - or: `cl-mech-3`
  - or: `cl-mech-6`
  - or: `cl-mech-7`
  - or: `cl-mech-15`
  - or: `cl-mech-22`
  - or: `cl-mech-23`
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
  - or: `cl-mechanical`
- next: Snap a link onto the left pins
  - either: `cl-mech-13`
  - or: `cl-mech-15`
  - or: `cl-mechanical`
- next: Fit the other link
  - either: `cl-mech-22`
  - or: `cl-mech-23`
  - or: `cl-mechanical`

**Items**
- `cl-base` Palm
  - icon: ![Palm](../../stories/builder/assets/items/cl-base.webp)

  ---

  A broad prepared palm with pivot holes and a fixed return-band hook. The jaws reach just beyond its front edge.

- `cl-jaw-1` Left jaw
  - icon: ![Left jaw](../../stories/builder/assets/items/cl-jaw-1.webp)

  ---

  A single jaw with captive pivot and link pins. Its left-facing shape matches the left side of the palm.

- `cl-jaw-2` Right jaw
  - icon: ![Right jaw](../../stories/builder/assets/items/cl-jaw-2.webp)

  ---

  The reflected right jaw has its own captive pins.

- `cl-slider` Slider
  - icon: ![Slider](../../stories/builder/assets/items/cl-slider.webp)

  ---

  One retained sliding shoe inside its guide, including travel stops and the moving return-band hook.

- `cl-link-1` Link
  - icon: ![Link](../../stories/builder/assets/items/cl-link-1.webp)

  ---

  A rigid 52 mm link with split eyes that snap sideways onto the captive pins. Either link fits either side.

- `cl-link-2` Link
  - icon: ![Link](../../stories/builder/assets/items/cl-link-2.webp)

  ---

  A rigid 52 mm link with split eyes. Either link fits either side.

- `cl-pad-1` Pad
  - icon: ![Pad](../../stories/builder/assets/items/cl-pad-1.webp)

  ---

  One soft pad for the inside face of a jaw. Either pad fits either jaw.

- `cl-pad-2` Pad
  - icon: ![Pad](../../stories/builder/assets/items/cl-pad-2.webp)

  ---

  One soft pad. Either pad fits either jaw.

- `cl-padded-jaw-1` Jaw
  - icon: ![Jaw](../../stories/builder/assets/items/cl-padded-jaw-1.webp)
- `cl-padded-jaw-2` Jaw
  - icon: ![Jaw](../../stories/builder/assets/items/cl-padded-jaw-2.webp)
- `cl-mech-1` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-1.webp)
- `cl-mech-2` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-2.webp)
- `cl-mech-3` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-3.webp)
- `cl-mech-4` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-4.webp)
- `cl-mech-5` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-5.webp)
- `cl-mech-6` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-6.webp)
- `cl-mech-7` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-7.webp)
- `cl-mech-13` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-13.webp)
- `cl-mech-15` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-15.webp)
- `cl-mech-22` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-22.webp)
- `cl-mech-23` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mech-23.webp)
- `cl-mechanical` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-mechanical.webp)

**Combinations**
- `cl-pad-1` [consume] + `cl-jaw-1` [transform] -> `cl-padded-jaw-1`
- `cl-pad-2` [consume] + `cl-jaw-1` [transform] -> `cl-padded-jaw-1`
- `cl-pad-1` [consume] + `cl-jaw-2` [transform] -> `cl-padded-jaw-2`
- `cl-pad-2` [consume] + `cl-jaw-2` [transform] -> `cl-padded-jaw-2`
- `cl-padded-jaw-1` [consume] + `cl-base` [transform] -> `cl-mech-1`
- `cl-padded-jaw-2` [consume] + `cl-base` [transform] -> `cl-mech-2`
- `cl-slider` [consume] + `cl-base` [transform] -> `cl-mech-4`
- `cl-padded-jaw-2` [consume] + `cl-mech-1` [transform] -> `cl-mech-3`
- `cl-slider` [consume] + `cl-mech-1` [transform] -> `cl-mech-5`
- `cl-padded-jaw-1` [consume] + `cl-mech-2` [transform] -> `cl-mech-3`
- `cl-slider` [consume] + `cl-mech-2` [transform] -> `cl-mech-6`
- `cl-slider` [consume] + `cl-mech-3` [transform] -> `cl-mech-7`
- `cl-padded-jaw-1` [consume] + `cl-mech-4` [transform] -> `cl-mech-5`
- `cl-padded-jaw-2` [consume] + `cl-mech-4` [transform] -> `cl-mech-6`
- `cl-padded-jaw-2` [consume] + `cl-mech-5` [transform] -> `cl-mech-7`
- `cl-link-1` [consume] + `cl-mech-5` [transform] -> `cl-mech-13`
- `cl-link-2` [consume] + `cl-mech-5` [transform] -> `cl-mech-13`
- `cl-padded-jaw-1` [consume] + `cl-mech-6` [transform] -> `cl-mech-7`
- `cl-link-1` [consume] + `cl-mech-6` [transform] -> `cl-mech-22`
- `cl-link-2` [consume] + `cl-mech-6` [transform] -> `cl-mech-22`
- `cl-link-1` [consume] + `cl-mech-7` [transform] -> `cl-mech-15`
- `cl-link-2` [consume] + `cl-mech-7` [transform] -> `cl-mech-15`
- `cl-padded-jaw-2` [consume] + `cl-mech-13` [transform] -> `cl-mech-15`
- `cl-link-1` [consume] + `cl-mech-15` [transform] -> `cl-mechanical`
- `cl-link-2` [consume] + `cl-mech-15` [transform] -> `cl-mechanical`
- `cl-padded-jaw-1` [consume] + `cl-mech-22` [transform] -> `cl-mech-23`
- `cl-link-1` [consume] + `cl-mech-23` [transform] -> `cl-mechanical`
- `cl-link-2` [consume] + `cl-mech-23` [transform] -> `cl-mechanical`

## `c-claw-air` Syringes and a hose
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Pneumatic claw](../../stories/builder/assets/items/pneumatic-claw.webp)

**Goals**
- Snap the rear cup onto the syringe
  - either: `cl-rear-supported`
  - or: `cl-supported-output`
- next: Fit the front cup -- `cl-supported-output`
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
  - icon: ![Output syringe](../../stories/builder/assets/items/cl-output.webp)

  ---

  A prepared needleless syringe. Its rigid piston and stem move inside a real hollow barrel.

- `cl-rear-cup` Rear cup
  - icon: ![Rear cup](../../stories/builder/assets/items/cl-rear-cup.webp)

  ---

  A single snap cup with an attached soft retaining strap and captive mounting pins.

- `cl-front-cup` Front cup
  - icon: ![Front cup](../../stories/builder/assets/items/cl-front-cup.webp)

  ---

  The other snap cup has its own attached strap and captive pins.

- `cl-clip` Plunger clip
  - icon: ![Plunger clip](../../stories/builder/assets/items/cl-clip.webp)

  ---

  A connected clip that plugs into the slider and captures the syringe thumb flange.

- `cl-band` Return band
  - icon: ![Return band](../../stories/builder/assets/items/cl-band.webp)

  ---

  One soft elastic loop. Its two hook brackets are already attached to the palm and slider.

- `cl-input` Hand syringe
  - icon: ![Hand syringe](../../stories/builder/assets/items/cl-input.webp)

  ---

  A second prepared needleless syringe. It stays beside the claw, joined by the flexible hose.

- `cl-tube` Air hose
  - icon: ![Air hose](../../stories/builder/assets/items/cl-tube.webp)

  ---

  One continuous flexible hose with an open end for each syringe nozzle.

- `cl-rear-supported` Syringe
  - icon: ![Syringe](../../stories/builder/assets/items/cl-rear-supported.webp)
- `cl-front-supported` Syringe
  - icon: ![Syringe](../../stories/builder/assets/items/cl-front-supported.webp)
- `cl-supported-output` Syringe
  - icon: ![Syringe](../../stories/builder/assets/items/cl-supported-output.webp)
- `cl-air-1` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-air-1.webp)
- `cl-air-3` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-air-3.webp)
- `cl-air-4` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-air-4.webp)
- `cl-air-5` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-air-5.webp)
- `cl-air-7` Claw
  - icon: ![Claw](../../stories/builder/assets/items/cl-air-7.webp)
- `cl-controller` Hand syringe
  - icon: ![Hand syringe](../../stories/builder/assets/items/cl-controller.webp)
- `pneumatic-claw` Pneumatic claw
  - icon: ![Pneumatic claw](../../stories/builder/assets/items/pneumatic-claw.webp)

  ---

  Pushing the hand syringe moves air through the hose into the output syringe. The output plunger moves the slider; the two rigid links turn the jaws. The elastic loop opens them as the plunger returns. The drawings show the available mechanism travel, not a measured grip force.


**Combinations**
- `cl-rear-cup` [consume] + `cl-output` [transform] -> `cl-rear-supported`
- `cl-front-cup` [consume] + `cl-output` [transform] -> `cl-front-supported`
- `cl-front-cup` [consume] + `cl-rear-supported` [transform] -> `cl-supported-output`
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

## `bf-film-build` A tiny picture show
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Animation drum](../../stories/builder/assets/items/animation-drum.webp)

**Goals**
- Cut the marked viewing slits -- `bf-film-cut`
- next: Roll the Drum wall -- `bf-film-rolled`
- next: Tape the seam -- `bf-film-seamed`
- next: Fit the Floor into the tabs -- `bf-film-shell`
- next: Fit the Turntable to the Base -- `bf-film-turntable`
- next: Fit the Drum onto the Turntable -- `bf-film-standing`
- next: Roll the Picture strip -- `bf-film-loop`
- next: Fit the Picture ring inside the Drum -- `animation-drum`

**Hotspots**
- `bf-film-cut-process` (center 130px, 216px)
  - icon: ![Cut](../../stories/builder/assets/actions/cut.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)
- `bf-film-roll-process` (center 390px, 216px)
  - icon: ![Roll](../../stories/builder/assets/actions/roll.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-film-wall` Drum wall
  - icon: ![Drum wall](../../stories/builder/assets/items/bf-film-wall.webp)

  ---

  One card strip with twelve marked slots and integral floor tabs. Cut down to the stopping line; the lower band stays continuous.
- `bf-film-cut-process` Cut
  - icon: ![Cut](../../stories/builder/assets/actions/cut.svg)
- `bf-film-cut` Drum wall
  - icon: ![Drum wall](../../stories/builder/assets/items/bf-film-cut.webp)
- `bf-film-roll-process` Roll
  - icon: ![Roll](../../stories/builder/assets/actions/roll.svg)
- `bf-film-rolled` Drum
  - icon: ![Drum](../../stories/builder/assets/items/bf-film-rolled.webp)
- `bf-film-tape` Tape
  - icon: ![Tape](../../stories/builder/assets/items/bf-film-tape.webp)
- `bf-film-seamed` Drum
  - icon: ![Drum](../../stories/builder/assets/items/bf-film-seamed.webp)
- `bf-film-floor` Floor
  - icon: ![Floor](../../stories/builder/assets/items/bf-film-floor.webp)
- `bf-film-shell` Drum
  - icon: ![Drum](../../stories/builder/assets/items/bf-film-shell.webp)
- `bf-film-base` Base
  - icon: ![Base](../../stories/builder/assets/items/bf-film-base.webp)
- `bf-film-bearing` Turntable
  - icon: ![Turntable](../../stories/builder/assets/items/bf-film-bearing.webp)

  ---

  One retained spindle, sleeve bearing and platform. The spindle stays fixed in the base while the platform turns.
- `bf-film-turntable` Base
  - icon: ![Base](../../stories/builder/assets/items/bf-film-turntable.webp)
- `bf-film-standing` Drum
  - icon: ![Drum](../../stories/builder/assets/items/bf-film-standing.webp)
- `bf-film-strip` Picture strip
  - icon: ![Picture strip](../../stories/builder/assets/items/bf-film-strip.webp)

  ---

  A printed sequence of twelve fish pictures, one per viewing slit, with a prepared adhesive overlap. The pictures face inward when rolled.
- `bf-film-loop` Picture ring
  - icon: ![Picture ring](../../stories/builder/assets/items/bf-film-loop.webp)
- `animation-drum` Animation drum
  - icon: ![Animation drum](../../stories/builder/assets/items/animation-drum.webp)

  ---

  Looking through the slits gives brief separated glimpses of successive pictures, with darkness between them.

**Combinations**
- `bf-film-wall` [transform] @ `bf-film-cut-process` -> `bf-film-cut`
- `bf-film-cut` [transform] @ `bf-film-roll-process` -> `bf-film-rolled`
- `bf-film-tape` [consume] + `bf-film-rolled` [transform] -> `bf-film-seamed`
- `bf-film-floor` [consume] + `bf-film-seamed` [transform] -> `bf-film-shell`
- `bf-film-bearing` [consume] + `bf-film-base` [transform] -> `bf-film-turntable`
- `bf-film-turntable` [consume] + `bf-film-shell` [transform] -> `bf-film-standing`
- `bf-film-strip` [transform] @ `bf-film-roll-process` -> `bf-film-loop`
- `bf-film-loop` [consume] + `bf-film-standing` [transform] -> `animation-drum`

## `c-rover-drive` Two wheels, two motors
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Build reference](../../stories/builder/assets/items/rv-mounted.webp)

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
  - icon: ![Flip](../../stories/builder/assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `rv-deck` Deck
  - icon: ![Deck](../../stories/builder/assets/items/rv-deck.webp)

  ---

  The prepared deck includes the pen guides, captive caps, return spring and hand-operated lift cam. The drawing carriage is fitted later.
- `rv-motor-a` Left motor
  - icon: ![Left motor](../../stories/builder/assets/items/rv-motor-a.webp)

  ---

  An enclosed slow gearmotor, mounting flange and attached lead. Its output shaft drives one wheel.
- `rv-motor-b` Right motor
  - icon: ![Right motor](../../stories/builder/assets/items/rv-motor-b.webp)

  ---

  An enclosed slow gearmotor, mounting flange and attached lead. Its output shaft drives one wheel.
- `rv-wheel-a` Wheel
  - icon: ![Wheel](../../stories/builder/assets/items/rv-wheel.webp)

  ---

  Either wheel fits either geared motor. Its retained centre fastener locks the hub to the flat-sided shaft.
- `rv-wheel-b` Wheel
  - icon: ![Wheel](../../stories/builder/assets/items/rv-wheel.webp)

  ---

  Either wheel fits either geared motor. Its retained centre fastener locks the hub to the flat-sided shaft.
- `rv-caster` Caster
  - icon: ![Caster](../../stories/builder/assets/items/rv-caster.webp)

  ---

  The free-turning ball supports the third corner.
- `rv-pack` Battery pack
  - icon: ![Battery pack](../../stories/builder/assets/items/rv-pack.webp)

  ---

  An enclosed compatible low-voltage pack with cells already fitted.
- `rv-receiver` Receiver
  - icon: ![Receiver](../../stories/builder/assets/items/rv-receiver.webp)

  ---

  The supplied receiver and motor driver control the wheels independently. Its matching ready-to-use remote needs no construction here.
- `rv-under` Deck
  - icon: ![Deck](../../stories/builder/assets/items/rv-under.webp)
- `rv-drive-a` Left drive
  - icon: ![Left drive](../../stories/builder/assets/items/rv-drive-a.webp)
- `rv-drive-b` Right drive
  - icon: ![Right drive](../../stories/builder/assets/items/rv-drive-b.webp)
- `rv-deck-01` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-01.webp)
- `rv-deck-02` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-02.webp)
- `rv-deck-03` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-03.webp)
- `rv-deck-04` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-04.webp)
- `rv-deck-05` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-05.webp)
- `rv-deck-06` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-06.webp)
- `rv-deck-07` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-07.webp)
- `rv-deck-08` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-08.webp)
- `rv-deck-09` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-09.webp)
- `rv-deck-10` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-10.webp)
- `rv-deck-11` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-11.webp)
- `rv-deck-12` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-12.webp)
- `rv-deck-13` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-13.webp)
- `rv-deck-14` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-14.webp)
- `rv-deck-15` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-15.webp)
- `rv-deck-16` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-16.webp)
- `rv-deck-17` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-17.webp)
- `rv-deck-18` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-18.webp)
- `rv-deck-19` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-19.webp)
- `rv-deck-20` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-20.webp)
- `rv-deck-21` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-21.webp)
- `rv-deck-22` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-22.webp)
- `rv-deck-23` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-23.webp)
- `rv-deck-24` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-24.webp)
- `rv-deck-25` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-25.webp)
- `rv-deck-26` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-26.webp)
- `rv-deck-27` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-27.webp)
- `rv-deck-28` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-28.webp)
- `rv-deck-29` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-29.webp)
- `rv-deck-30` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-deck-30.webp)
- `rv-mounted` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-mounted.webp)
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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Build reference](../../stories/builder/assets/items/drawing-rover.webp)

**Goals**
- Connect the switch harness -- `rv-wired`
- next: Fit a guard
  - either: `rv-one-guard-a`
  - or: `rv-one-guard-b`
  - or: `rv-guarded`
- next: Fit the other guard -- `rv-guarded`
- next: Flip the rover upright -- `rv-upright`
- next: Clip the pen into its carriage -- `rv-pen-carriage`
- next: Slide the carriage onto the guides -- `drawing-rover`

**Hotspots**
- `rv-flip-pen` (center 130px, 216px)
  - icon: ![Flip](../../stories/builder/assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `rv-harness` Switch harness
  - icon: ![Switch harness](../../stories/builder/assets/items/rv-harness.webp)

  ---

  A connected fused harness and switch. Fit with the power off and connect the parked battery and motor plugs to their matching sockets.
- `rv-guard-a` Guard
  - icon: ![Guard](../../stories/builder/assets/items/rv-guard-a.webp)

  ---

  One hollow snap-on guard. Its open shaft slot and split cable channel fit around the already attached wheel and lead.
- `rv-guard-b` Guard
  - icon: ![Guard](../../stories/builder/assets/items/rv-guard-b.webp)

  ---

  One hollow snap-on guard, fitted independently on the other drive.
- `rv-pen` Pen
  - icon: ![Pen](../../stories/builder/assets/items/rv-pen.webp)

  ---

  A felt-tip pen with its cap removed.
- `rv-clip` Pen carriage
  - icon: ![Pen carriage](../../stories/builder/assets/items/rv-clip.webp)

  ---

  One connected bridge, spring clip and follower shoe. The deck already carries the guides and lift lever.
- `rv-wired` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-wired.webp)
- `rv-one-guard-a` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-one-guard-a.webp)
- `rv-one-guard-b` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-one-guard-b.webp)
- `rv-guarded` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-guarded.webp)
- `rv-upright` Rover
  - icon: ![Rover](../../stories/builder/assets/items/rv-upright.webp)
- `rv-pen-carriage` Pen carriage
  - icon: ![Pen carriage](../../stories/builder/assets/items/rv-pen-carriage.webp)
- `drawing-rover` Drawing rover
  - icon: ![Drawing rover](../../stories/builder/assets/items/drawing-rover.webp)

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
- `rv-pen-carriage` [consume] + `rv-upright` [transform] -> `drawing-rover`

## `c-projector-box` A box of stars
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Build reference](../../stories/builder/assets/items/pj-wheel-box.webp)

**Goals**
- Fit the reflector inside the box -- `pj-lined`
- next: Fit the lamp -- `pj-lamped`
- next: Connect the battery pack -- `pj-powered`
- next: Punch stars around the disc -- `pj-stars`
- next: Fit the disc to the spindle -- `pj-wheel`
- next: Mount the star wheel in the box -- `pj-wheel-box`

**Hotspots**
- `pj-punch` (center 130px, 216px)
  - icon: ![Punch](../../stories/builder/assets/actions/punch.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `pj-box` Box
  - icon: ![Box](../../stories/builder/assets/items/pj-box.webp)

  ---

  An open prepared box with a fixed internal aperture and spindle mounting positions. Its lid is a separate part.
- `pj-liner` Reflector
  - icon: ![Reflector](../../stories/builder/assets/items/pj-liner.webp)

  ---

  One folded U-shaped reflector joins its floor and side faces. It leaves the electrical contacts clear.
- `pj-lamp` Lamp
  - icon: ![Lamp](../../stories/builder/assets/items/pj-lamp.webp)

  ---

  A cool-running diffused LED module, holder, current-limiting resistor and attached lead.
- `pj-battery` Battery pack
  - icon: ![Battery pack](../../stories/builder/assets/items/pj-battery.webp)

  ---

  An enclosed compatible switched low-voltage pack with its connected holder and fused lead. Connect with the switch off.
- `pj-card` Card disc
  - icon: ![Card disc](../../stories/builder/assets/items/pj-card.webp)

  ---

  The flat-sided centre hole matches the spindle.
- `pj-spindle` Spindle
  - icon: ![Spindle](../../stories/builder/assets/items/pj-spindle.webp)

  ---

  A shaft retained in its two bushed supports, with captive collars and fasteners. It is one prepared mechanism.
- `pj-lined` Projector
  - icon: ![Projector](../../stories/builder/assets/items/pj-lined.webp)
- `pj-lamped` Projector
  - icon: ![Projector](../../stories/builder/assets/items/pj-lamped.webp)
- `pj-powered` Projector
  - icon: ![Projector](../../stories/builder/assets/items/pj-powered.webp)
- `pj-stars` Star disc
  - icon: ![Star disc](../../stories/builder/assets/items/pj-stars.webp)
- `pj-wheel` Star wheel
  - icon: ![Star wheel](../../stories/builder/assets/items/pj-wheel.webp)
- `pj-wheel-box` Projector
  - icon: ![Projector](../../stories/builder/assets/items/pj-wheel-box.webp)
- `pj-punch` Punch

**Combinations**
- `pj-card` [transform] @ `pj-punch` -> `pj-stars`
- `pj-stars` [consume] + `pj-spindle` [transform] -> `pj-wheel`
- `pj-liner` [consume] + `pj-box` [transform] -> `pj-lined`
- `pj-lamp` [consume] + `pj-lined` [transform] -> `pj-lamped`
- `pj-battery` [consume] + `pj-lamped` [transform] -> `pj-powered`
- `pj-wheel` [consume] + `pj-powered` [transform] -> `pj-wheel-box`


## `c-projector-lens` Bring the stars into focus
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Build reference](../../stories/builder/assets/items/star-projector.webp)

**Goals**
- Fit the lens into its holder -- `pj-focus`
- next: Fit the holder to the box -- `pj-focused`
- next: Fit the hood around the lens -- `pj-hooded`
- next: Fit the handle to the spindle -- `pj-handled`
- next: Close the box with its lid -- `star-projector`

**Items**
- `pj-lens` Lens
  - icon: ![Lens](../../stories/builder/assets/items/pj-lens.webp)

  ---

  A single convex lens forms an inverted image of the lit holes.
- `pj-holder` Lens holder
  - icon: ![Lens holder](../../stories/builder/assets/items/pj-holder.webp)

  ---

  A connected sliding carriage retained on its rails. Move it along the rails to focus.
- `pj-hood` Hood
  - icon: ![Hood](../../stories/builder/assets/items/pj-hood.webp)

  ---

  The dark tube surrounds the lens without covering its clear aperture.
- `pj-handle` Handle
  - icon: ![Handle](../../stories/builder/assets/items/pj-handle.webp)

  ---

  The handwheel has a real belt groove behind its grip. It can be turned by hand now and driven by a belt later.
- `pj-lid` Lid
  - icon: ![Lid](../../stories/builder/assets/items/pj-lid.webp)

  ---

  One rigid lid with its integral locating rim. Fit it after the internal parts.
- `pj-focus` Lens holder
  - icon: ![Lens holder](../../stories/builder/assets/items/pj-focus.webp)
- `pj-focused` Projector
  - icon: ![Projector](../../stories/builder/assets/items/pj-focused.webp)
- `pj-hooded` Projector
  - icon: ![Projector](../../stories/builder/assets/items/pj-hooded.webp)
- `pj-handled` Projector
  - icon: ![Projector](../../stories/builder/assets/items/pj-handled.webp)
- `star-projector` Star projector
  - icon: ![Star projector](../../stories/builder/assets/items/star-projector.webp)

  ---

  Turning the disc brings new holes past the fixed aperture. Sliding the lens brings their projected image into focus. The optical model uses one ideal thin lens; brightness and real component tolerances are not measured.

**Combinations**
- `pj-lens` [consume] + `pj-holder` [transform] -> `pj-focus`
- `pj-focus` [consume] + `pj-wheel-box` [transform] -> `pj-focused`
- `pj-hood` [consume] + `pj-focused` [transform] -> `pj-hooded`
- `pj-handle` [consume] + `pj-hooded` [transform] -> `pj-handled`
- `pj-lid` [consume] + `pj-handled` [transform] -> `star-projector`

## `c-lift-frame` The impossible part
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Build reference](../../stories/builder/assets/items/fc-lift-frame.webp)

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
  - icon: ![Flip](../../stories/builder/assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `fc-deck` Deck
  - icon: ![Deck](../../stories/builder/assets/items/fc-deck.webp)

  ---

  A 400 × 300 mm prepared plywood deck. The mounting holes and wire passages are already cut.
- `fc-arch-a` Arch
  - icon: ![Arch](../../stories/builder/assets/items/fc-arch-a.webp)

  ---

  One connected rigid arch with two feet and captive bolts.
- `fc-arch-b` Arch
  - icon: ![Arch](../../stories/builder/assets/items/fc-arch-b.webp)

  ---

  A second identical connected arch. Either arch fits either side of the deck.
- `fc-cradle` Tile cradle
  - icon: ![Tile cradle](../../stories/builder/assets/items/fc-cradle.webp)

  ---

  One connected top cradle. Four integral saddles clip over the arches; its padded rails receive the tile.
- `fc-tile` Lift tile
  - icon: ![Lift tile](../../stories/builder/assets/items/fc-tile.webp)

  ---

  This powered lift tile is explicitly fictional. Its limited force points upward while current flows. It makes no energy and carries no person.
- `fc-battery` Battery pack
  - icon: ![Battery pack](../../stories/builder/assets/items/fc-battery.webp)

  ---

  A compatible enclosed battery in its integral retained bracket. It mounts below the deck, keeping weight low.
- `fc-control` Lift control
  - icon: ![Lift control](../../stories/builder/assets/items/fc-control.webp)

  ---

  A prepared controller and latching stop button in one pod with a connected fused harness. Keep power off while fitting it.
- `fc-one-arch` Frame
  - icon: ![Frame](../../stories/builder/assets/items/fc-one-arch.webp)
- `fc-arches` Frame
  - icon: ![Frame](../../stories/builder/assets/items/fc-arches.webp)
- `fc-top` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-top.webp)
- `fc-tiled` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-tiled.webp)
- `fc-inverted` Frame
  - icon: ![Frame](../../stories/builder/assets/items/fc-inverted.webp)
- `fc-powered` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-powered.webp)
- `fc-upright` Frame
  - icon: ![Frame](../../stories/builder/assets/items/fc-upright.webp)
- `fc-lift-frame` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-lift-frame.webp)
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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Build reference](../../stories/builder/assets/items/fc-powered-show.webp)

**Goals**
- Fit the projector dock -- `fc-docked`
- next: Fit your projector to the dock -- `fc-projector-aboard`
- next: Fit the small pulley to the motor -- `fc-drive`
- next: Mount the drive motor -- `fc-motor-mounted`
- next: Loop the belt around both pulleys -- `fc-belted`
- next: Connect the motor supply -- `fc-powered-show`

**Items**
- `star-projector` Star projector
  - from chapter `c-lift-projector` icon: ![Star projector](../../stories/builder/assets/items/fc-projector-carried.webp)
- `fc-dock` Projector dock
  - icon: ![Projector dock](../../stories/builder/assets/items/fc-dock.webp)

  ---

  One connected projector dock, with four captive mounting studs matching the original box.
- `fc-motor` Gearmotor
  - icon: ![Gearmotor](../../stories/builder/assets/items/fc-motor.webp)

  ---

  An enclosed slow gearmotor with its integral pedestal and lead. The shaft is parallel to the projector spindle.
- `fc-pulley` Small pulley
  - icon: ![Small pulley](../../stories/builder/assets/items/fc-pulley.webp)

  ---

  One small pulley with a captive screw that clamps onto the motor shaft flat.
- `fc-belt` Belt
  - icon: ![Belt](../../stories/builder/assets/items/fc-belt.webp)

  ---

  One continuous soft belt. Its small pulley drives the larger grooved handwheel more slowly.
- `fc-motor-pack` Motor supply
  - icon: ![Motor supply](../../stories/builder/assets/items/fc-motor-pack.webp)

  ---

  An enclosed low-voltage motor supply with its own switch, lead and integral mounting bracket. The lamp keeps its original supply; the lift has a separate circuit.
- `fc-docked` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-docked.webp)
- `fc-projector-aboard` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-projector-aboard.webp)
- `fc-drive` Drive motor
  - icon: ![Drive motor](../../stories/builder/assets/items/fc-drive.webp)
- `fc-motor-mounted` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-motor-mounted.webp)
- `fc-belted` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-belted.webp)
- `fc-powered-show` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-powered-show.webp)

**Combinations**
- `fc-dock` [consume] + `fc-lift-frame` [transform] -> `fc-docked`
- `star-projector` [consume] + `fc-docked` [transform] -> `fc-projector-aboard`
- `fc-pulley` [consume] + `fc-motor` [transform] -> `fc-drive`
- `fc-drive` [consume] + `fc-projector-aboard` [transform] -> `fc-motor-mounted`
- `fc-belt` [consume] + `fc-motor-mounted` [transform] -> `fc-belted`
- `fc-motor-pack` [consume] + `fc-belted` [transform] -> `fc-powered-show`


## `c-whale-shape` A whale takes shape
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Build reference](../../stories/builder/assets/items/fc-whale.webp)

**Goals**
- Fit a whale side
  - either: `fc-near-side`
  - or: `fc-far-side`
  - or: `fc-sided`
- next: Fit the other side -- `fc-sided`
- next: Fit the tail -- `fc-tailed`
- next: Fit a fin
  - either: `fc-one-fin-a`
  - or: `fc-one-fin-b`
  - or: `fc-whale`
- next: Fit the other fin -- `fc-whale`

**Items**
- `fc-side-a` Whale side
  - icon: ![Whale side](../../stories/builder/assets/items/fc-side-a.webp)

  ---

  One cut whale side panel with its mounting tabs. Its top edge stays below the projector beam.
- `fc-side-b` Whale side
  - icon: ![Whale side](../../stories/builder/assets/items/fc-side-b.webp)

  ---

  A second whale side panel, fitted separately.
- `fc-tail` Tail
  - icon: ![Tail](../../stories/builder/assets/items/fc-tail.webp)

  ---

  One continuous fixed tail with its prepared root fitting. It does not steer or provide lift.
- `fc-fin-a` Fin
  - icon: ![Fin](../../stories/builder/assets/items/fc-fin-a.webp)

  ---

  One fixed fin with integral mounting tabs. It gives the whale its shape, not lift.
- `fc-fin-b` Fin
  - icon: ![Fin](../../stories/builder/assets/items/fc-fin-b.webp)

  ---

  The other fixed fin.
- `fc-near-side` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-near-side.webp)
- `fc-far-side` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-far-side.webp)
- `fc-sided` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-sided.webp)
- `fc-tailed` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-tailed.webp)
- `fc-one-fin-a` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-one-fin-a.webp)
- `fc-one-fin-b` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-one-fin-b.webp)
- `fc-whale` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-whale.webp)

**Combinations**
- `fc-side-a` [consume] + `fc-powered-show` [transform] -> `fc-near-side`
- `fc-side-b` [consume] + `fc-powered-show` [transform] -> `fc-far-side`
- `fc-side-b` [consume] + `fc-near-side` [transform] -> `fc-sided`
- `fc-side-a` [consume] + `fc-far-side` [transform] -> `fc-sided`
- `fc-tail` [consume] + `fc-sided` [transform] -> `fc-tailed`
- `fc-fin-a` [consume] + `fc-tailed` [transform] -> `fc-one-fin-a`
- `fc-fin-b` [consume] + `fc-one-fin-a` [transform] -> `fc-whale`
- `fc-fin-b` [consume] + `fc-tailed` [transform] -> `fc-one-fin-b`
- `fc-fin-a` [consume] + `fc-one-fin-b` [transform] -> `fc-whale`


## `c-whale-finish` Ready for the fair
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)
reference: ![Build reference](../../stories/builder/assets/items/flying-whale.webp)

**Goals**
- Flip the whale over -- `fc-whale-under`
- next: Fit a landing skid
  - either: `fc-one-skid-a`
  - or: `fc-one-skid-b`
  - or: `fc-skids`
- next: Fit the other skid -- `fc-skids`
- next: Fit the weight rail -- `fc-railed`
- next: Slide the weight into the rail -- `fc-weighted`
- next: Flip the whale upright -- `fc-standing`
- next: Fit the clear drive guard -- `flying-whale`

**Hotspots**
- `fc-flip-feet` (center 130px, 216px)
  - icon: ![Flip](../../stories/builder/assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `fc-skid-a` Landing skid
  - icon: ![Landing skid](../../stories/builder/assets/items/fc-skid-a.webp)

  ---

  One connected landing skid with two upright legs and captive deck bolts.
- `fc-skid-b` Landing skid
  - icon: ![Landing skid](../../stories/builder/assets/items/fc-skid-b.webp)

  ---

  A second landing skid. Their feet reach below the batteries and trim weight.
- `fc-rail` Weight rail
  - icon: ![Weight rail](../../stories/builder/assets/items/fc-rail.webp)

  ---

  One slotted rail with integral mounting ears and a captive end stop. The weight shoe enters through its open end.
- `fc-weight` Counterweight
  - icon: ![Counterweight](../../stories/builder/assets/items/fc-weight.webp)

  ---

  A single sliding weight with a connected captive shoe and clamping screw. Slide the shoe into the rail before closing its captive end stop.
- `fc-guard` Guard
  - icon: ![Guard](../../stories/builder/assets/items/fc-guard.webp)

  ---

  One hollow clear guard with open rear seating channels and captive screws. It encloses the belt and hand grip without covering the lens.
- `fc-whale-under` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-whale-under.webp)
- `fc-one-skid-a` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-one-skid-a.webp)
- `fc-one-skid-b` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-one-skid-b.webp)
- `fc-skids` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-skids.webp)
- `fc-railed` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-railed.webp)
- `fc-weighted` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/fc-weighted.webp)
- `fc-standing` Whale
  - icon: ![Whale](../../stories/builder/assets/items/fc-standing.webp)
- `flying-whale` Whale carrier
  - icon: ![Whale carrier](../../stories/builder/assets/items/flying-whale.webp)

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
background: ![White instruction page](../../stories/builder/assets/backgrounds/white.svg)

“Can I have a go?”
