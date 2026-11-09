# ![A brick-red paper pinwheel](../story/icon.png) The Next Box
background: ![White instruction page](../story/assets/backgrounds/white.svg)

Paper, wheels, string and light. Open a box and make something.

## `c01` Something that moves
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Pinwheel](../story/assets/items/pinwheel.webp)

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
  - icon: ![Dotted paper folding diagram](../story/assets/actions/fold.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)
- `pw-flip` (center 130px, 216px)
  - icon: ![Outline diagram of turning a sheet over](../story/assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)

**Items**
- `pw-fold` Fold
- `pw-flip` Flip
- `pw-paper` Paper
  - icon: ![Prepared paper square](../story/assets/items/pw-paper.webp) (center 358px, 830px)

  ---

  The paper sheet is already cut along four diagonals, stopping short of the centre. Curl the four pierced corners inward; keep the uncut centre whole.
- `pw-hub` Hub
  - icon: ![Teal hub](../story/assets/items/pw-hub.webp) (center 140px, 460px)

  ---

  A hollow snap-in hub holds the folded corners together. Its centre is a bearing for the axle.
- `pw-axle` Axle
  - icon: ![Axle and spacer](../story/assets/items/pw-axle.webp) (center 470px, 460px)

  ---

  A blunt axle with a built-in spacer and retaining tip. The hub turns around the axle; the spacer keeps the paper clear of the handle.
- `pw-handle` Handle
  - icon: ![Wooden handle with an open axle clip](../story/assets/items/pw-handle.webp) (center 690px, 820px)

  ---

  The prepared clip snaps over the axle's rear post. Two small mounting holes remain near the foot of the handle.
- `pw-one-blade` Paper
  - icon: ![Paper with one folded corner](../story/assets/items/pw-one-blade.webp)
- `pw-two-blades` Paper
  - icon: ![Paper with two folded corners](../story/assets/items/pw-two-blades.webp)
- `pw-three-blades` Paper
  - icon: ![Paper with three folded corners](../story/assets/items/pw-three-blades.webp)
- `pw-loose-rotor` Blades
  - icon: ![Folded paper](../story/assets/items/pw-loose-rotor.webp)
- `pw-folded-rotor` Blades
  - icon: ![Blades with hub](../story/assets/items/pw-folded-rotor.webp)
- `pw-rear-rotor` Blades
  - icon: ![Back of the blades](../story/assets/items/pw-rear-rotor.webp)
- `pw-bearing-rotor` Blades
  - icon: ![Blades on their axle](../story/assets/items/pw-bearing-rotor.webp)
- `pw-mounted` Pinwheel
  - icon: ![Back of the pinwheel](../story/assets/items/pw-mounted.webp)
- `pinwheel` Pinwheel
  - icon: ![Pinwheel](../story/assets/items/pinwheel.webp)
  - animation: ![Working toy](../story/assets/animations/pinwheel-working.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Sail](../story/assets/items/wr-sail.webp)

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
  - icon: ![Mast](../story/assets/items/wr-mast-wood.webp)
- `wr-mast-foot` Mast
  - icon: ![Mast](../story/assets/items/wr-mast-foot.webp)
- `wr-mast-joint` Mast
  - icon: ![Mast](../story/assets/items/wr-mast-joint.webp)
- `wr-mast-joint-foot` Mast
  - icon: ![Mast](../story/assets/items/wr-mast-joint-foot.webp)
- `wr-frame` Mast
  - icon: ![Mast](../story/assets/items/wr-frame.webp)
- `wr-ready` Mast
  - icon: ![Mast](../story/assets/items/wr-ready.webp)
- `wr-frame-sail` Sail
  - icon: ![Sail](../story/assets/items/wr-frame-sail.webp)
- `wr-sail` Sail
  - icon: ![Sail](../story/assets/items/wr-sail.webp)
  - from chapter `c-racer-body` icon: ![Sail](../story/assets/items/wr-sail-carried.webp)
- `wr-connector` Connector
  - icon: ![Connector](../story/assets/items/wr-connector.webp)

  ---

  Two offset sockets keep the wooden rods from crossing through each other. Flexible ribs grip both rods.
- `wr-crossbar` Crossbar
  - icon: ![Crossbar](../story/assets/items/wr-crossbar.webp)

  ---

  A short wooden rod that supports the bottom of the sail.
- `wr-foot` Foot
  - icon: ![Foot](../story/assets/items/wr-foot.webp)

  ---

  The mast pushes into the top socket. The split legs underneath will snap into the chassis.
- `wr-sailcloth` Sail
  - icon: ![Sail](../story/assets/items/wr-sailcloth.webp)

  ---

  Three small open clips are attached to the cloth. They press onto the mast and crossbar.
- `wr-crossbar-joint` Crossbar
  - icon: ![Crossbar](../story/assets/items/wr-crossbar-joint.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Wind racer](../story/assets/items/wind-racer.webp)

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
  - icon: ![Turn the chassis over](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `wr-chassis-top` Chassis
  - icon: ![Chassis](../story/assets/items/wr-chassis-top.webp)
- `wr-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-chassis.webp)
- `wr-front-bearing-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-front-bearing-chassis.webp)
- `wr-rear-bearing-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-rear-bearing-chassis.webp)
- `wr-bearing-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-bearing-chassis.webp)
- `wr-front-rolling-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-front-rolling-chassis.webp)
- `wr-rear-rolling-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-rear-rolling-chassis.webp)
- `wr-front-wheel-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-front-wheel-chassis.webp)
- `wr-rear-wheel-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-rear-wheel-chassis.webp)
- `wr-rolling-chassis` Chassis
  - icon: ![Chassis](../story/assets/items/wr-rolling-chassis.webp)
- `wr-upright` Chassis
  - icon: ![Chassis](../story/assets/items/wr-upright.webp)
- `wind-racer` Wind racer
  - icon: ![Wind racer](../story/assets/items/wind-racer.webp)
  - animation: ![Working toy](../story/assets/animations/wind-racer-working.webp)

  ---

  The wheels turn together with each straw axle inside the bearings. Outdoors, moving air can push against the sail.
- `wr-flip` Flip
- `wr-front-bearing` Bearing
  - icon: ![Bearing](../story/assets/items/wr-bearing.webp)

  ---

  An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.
- `wr-front-axle` Front straw
  - icon: ![Front straw](../story/assets/items/wr-straw.webp)

  ---

  A stiff hollow plastic axle. Push one wheel onto each end.
- `wr-front-one-wheel` Front axle
  - icon: ![Front axle](../story/assets/items/wr-one-wheel.webp)
- `wr-front-wheels` Front wheels
  - icon: ![Front wheels](../story/assets/items/wr-wheels.webp)
- `wr-rear-bearing` Bearing
  - icon: ![Bearing](../story/assets/items/wr-bearing.webp)

  ---

  An open bearing clips beneath the chassis. Its spring lips let the axle snap into the channel.
- `wr-rear-axle` Rear straw
  - icon: ![Rear straw](../story/assets/items/wr-straw.webp)

  ---

  A stiff hollow plastic axle. Push one wheel onto each end.
- `wr-rear-one-wheel` Rear axle
  - icon: ![Rear axle](../story/assets/items/wr-one-wheel.webp)
- `wr-rear-wheels` Rear wheels
  - icon: ![Rear wheels](../story/assets/items/wr-wheels.webp)
- `wr-wheel-1` Wheel
  - icon: ![Wheel](../story/assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-2` Wheel
  - icon: ![Wheel](../story/assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-3` Wheel
  - icon: ![Wheel](../story/assets/items/wr-wheel.webp)

  ---

  The wheel has a blind centre socket and an integral spacer. Any wheel fits either straw.
- `wr-wheel-4` Wheel
  - icon: ![Wheel](../story/assets/items/wr-wheel.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Pinball table](../story/assets/items/pinball-table.webp)

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
  - icon: ![Tray](../story/assets/items/bf-pb-tray.webp)

  ---

  Prepared plywood with rail slots, flipper holes and integral carrying handles.
- `bf-pb-left-rail` Left rail
  - icon: ![Left rail](../story/assets/items/bf-pb-left-rail.webp)
- `bf-pb-rail-1` Table
  - icon: ![Table](../story/assets/items/bf-pb-rail-1.webp)
- `bf-pb-right-rail` Right rail
  - icon: ![Right rail](../story/assets/items/bf-pb-right-rail.webp)
- `bf-pb-rail-2` Table
  - icon: ![Table](../story/assets/items/bf-pb-rail-2.webp)
- `bf-pb-top-rail` Top rail
  - icon: ![Top rail](../story/assets/items/bf-pb-top-rail.webp)
- `bf-pb-rail-3` Table
  - icon: ![Table](../story/assets/items/bf-pb-rail-3.webp)
- `bf-pb-lane` Lane rail
  - icon: ![Lane rail](../story/assets/items/bf-pb-lane.webp)
- `bf-pb-rail-4` Table
  - icon: ![Table](../story/assets/items/bf-pb-rail-4.webp)
- `bf-pb-left-lip` Left return
  - icon: ![Left return](../story/assets/items/bf-pb-left-lip.webp)
- `bf-pb-rail-5` Table
  - icon: ![Table](../story/assets/items/bf-pb-rail-5.webp)
- `bf-pb-right-lip` Right return
  - icon: ![Right return](../story/assets/items/bf-pb-right-lip.webp)
- `bf-pb-rail-6` Table
  - icon: ![Table](../story/assets/items/bf-pb-rail-6.webp)
- `bf-pb-cup` Marble cup
  - icon: ![Marble cup](../story/assets/items/bf-pb-cup.webp)
- `bf-pb-rimmed` Table
  - icon: ![Table](../story/assets/items/bf-pb-rimmed.webp)

**Combinations**
- `bf-pb-left-rail` [consume] + `bf-pb-tray` [transform] -> `bf-pb-rail-1`
- `bf-pb-right-rail` [consume] + `bf-pb-rail-1` [transform] -> `bf-pb-rail-2`
- `bf-pb-top-rail` [consume] + `bf-pb-rail-2` [transform] -> `bf-pb-rail-3`
- `bf-pb-lane` [consume] + `bf-pb-rail-3` [transform] -> `bf-pb-rail-4`
- `bf-pb-left-lip` [consume] + `bf-pb-rail-4` [transform] -> `bf-pb-rail-5`
- `bf-pb-right-lip` [consume] + `bf-pb-rail-5` [transform] -> `bf-pb-rail-6`
- `bf-pb-cup` [consume] + `bf-pb-rail-6` [transform] -> `bf-pb-rimmed`


## `bf-pb-flippers` Two flippers
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Pinball table](../story/assets/items/pinball-table.webp)

**Goals**
- Flip the Table -- `bf-pb-under`
- next: Fit the Pivot plate -- `bf-pb-plated-under`
- next: Fit the Support -- `bf-pb-supported-under`
- next: Flip the Table upright -- `bf-pb-upright`
- next: Snap on the Left paddle -- `bf-pb-left`
- next: Snap on the Right paddle -- `bf-pb-flipped`

**Hotspots**
- `bf-pb-flip` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-pb-rimmed` Table
  - icon: ![Table](../story/assets/items/bf-pb-rimmed.webp)
- `bf-pb-flip` Flip
  - icon: ![Flip](../story/assets/actions/flip.svg)
- `bf-pb-under` Table
  - icon: ![Table](../story/assets/items/bf-pb-under.webp)
- `bf-pb-plate` Pivot plate
  - icon: ![Pivot plate](../story/assets/items/bf-pb-plate.webp)

  ---

  A plate with retained spindles, finger buttons and return loops. The shoulders pass through the prepared tray clearances. Captive screws enter the tray’s threaded receivers from beneath.
- `bf-pb-plated-under` Table
  - icon: ![Table](../story/assets/items/bf-pb-plated-under.webp)
- `bf-pb-support` Support
  - icon: ![Support](../story/assets/items/bf-pb-support.webp)

  ---

  One connected U-shaped support with locating tongues and retaining clips. It slopes the table towards its marble cup without tilting sideways.
- `bf-pb-supported-under` Table
  - icon: ![Table](../story/assets/items/bf-pb-supported-under.webp)
- `bf-pb-upright` Table
  - icon: ![Table](../story/assets/items/bf-pb-upright.webp)
- `bf-pb-left-paddle` Left paddle
  - icon: ![Left paddle](../story/assets/items/bf-pb-left-paddle.webp)

  ---

  One polymer paddle with an open keyed snap socket. Its flexible mouth clips sideways around the spindle neck between the retaining shoulders.
- `bf-pb-left` Table
  - icon: ![Table](../story/assets/items/bf-pb-left.webp)
- `bf-pb-right-paddle` Right paddle
  - icon: ![Right paddle](../story/assets/items/bf-pb-right-paddle.webp)

  ---

  One polymer paddle with an open keyed snap socket. Its flexible mouth clips sideways around the spindle neck between the retaining shoulders.
- `bf-pb-flipped` Table
  - icon: ![Table](../story/assets/items/bf-pb-flipped.webp)

**Combinations**
- `bf-pb-rimmed` [transform] @ `bf-pb-flip` -> `bf-pb-under`
- `bf-pb-plate` [consume] + `bf-pb-under` [transform] -> `bf-pb-plated-under`
- `bf-pb-support` [consume] + `bf-pb-plated-under` [transform] -> `bf-pb-supported-under`
- `bf-pb-supported-under` [transform] @ `bf-pb-flip` -> `bf-pb-upright`
- `bf-pb-left-paddle` [consume] + `bf-pb-upright` [transform] -> `bf-pb-left`
- `bf-pb-right-paddle` [consume] + `bf-pb-left` [transform] -> `bf-pb-flipped`


## `bf-pb-launcher-build` A spring launcher
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Pinball table](../story/assets/items/pinball-table.webp)

**Goals**
- Slide the Spring onto the Plunger rod -- `bf-pb-sprung-rod`
- next: Fit the Plunger tip -- `bf-pb-tipped`
- next: Lower the Plunger into the Launcher cradle -- `bf-pb-open-launcher`
- next: Clip on the Launcher cover -- `bf-pb-launcher`
- next: Fit the Launcher to the Table -- `bf-pb-launched`

**Items**
- `bf-pb-rod` Plunger rod
  - icon: ![Plunger rod](../story/assets/items/bf-pb-rod.webp)

  ---

  A six-millimetre plunger rod with a fitted pull handle and an open front end for threading the spring.
- `bf-pb-spring` Spring
  - icon: ![Spring](../story/assets/items/bf-pb-spring.webp)
- `bf-pb-sprung-rod` Plunger
  - icon: ![Plunger](../story/assets/items/bf-pb-sprung-rod.webp)
- `bf-pb-tip` Plunger tip
  - icon: ![Plunger tip](../story/assets/items/bf-pb-tip.webp)

  ---

  A soft striking tip and piston with a blind gripping socket for the rod.
- `bf-pb-tipped` Plunger
  - icon: ![Plunger](../story/assets/items/bf-pb-tipped.webp)
- `bf-pb-barrel` Launcher cradle
  - icon: ![Launcher cradle](../story/assets/items/bf-pb-barrel.webp)

  ---

  An open-topped cradle with half-round end guides, mounting feet and a travel stop. The assembled plunger lowers through its open top.
- `bf-pb-open-launcher` Launcher
  - icon: ![Launcher](../story/assets/items/bf-pb-open-launcher.webp)
- `bf-pb-cover` Launcher cover
  - icon: ![Launcher cover](../story/assets/items/bf-pb-cover.webp)

  ---

  A clear upper shell with matching half-guides and flexible retaining clips. Closing it captures the plunger and encloses the spring.
- `bf-pb-launcher` Launcher
  - icon: ![Launcher](../story/assets/items/bf-pb-launcher.webp)
- `bf-pb-flipped` Table
  - icon: ![Table](../story/assets/items/bf-pb-flipped.webp)
- `bf-pb-launched` Table
  - icon: ![Table](../story/assets/items/bf-pb-launched.webp)

**Combinations**
- `bf-pb-spring` [consume] + `bf-pb-rod` [transform] -> `bf-pb-sprung-rod`
- `bf-pb-tip` [consume] + `bf-pb-sprung-rod` [transform] -> `bf-pb-tipped`
- `bf-pb-barrel` [consume] + `bf-pb-tipped` [transform] -> `bf-pb-open-launcher`
- `bf-pb-cover` [consume] + `bf-pb-open-launcher` [transform] -> `bf-pb-launcher`
- `bf-pb-launcher` [consume] + `bf-pb-flipped` [transform] -> `bf-pb-launched`


## `bf-pb-targets` One more go
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Pinball table](../story/assets/items/pinball-table.webp)

**Goals**
- Fit the Lower arch -- `bf-pb-target-1`
- next: Fit the Middle arch -- `bf-pb-target-2`
- next: Fit the Upper arch -- `bf-pb-target-3`
- next: Turn the Table toward the Score wheel -- `bf-pb-score-facing`
- next: Fit the Score wheel -- `bf-pb-scored`
- next: Put the Marble in its cup -- `pinball-table`

**Hotspots**
- `bf-pb-score-flip` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-pb-launched` Table
  - icon: ![Table](../story/assets/items/bf-pb-launched.webp)
- `bf-pb-arch-low` Lower arch
  - icon: ![Lower arch](../story/assets/items/bf-pb-arch-low.webp)
- `bf-pb-target-1` Table
  - icon: ![Table](../story/assets/items/bf-pb-target-1.webp)
- `bf-pb-arch-mid` Middle arch
  - icon: ![Middle arch](../story/assets/items/bf-pb-arch-mid.webp)
- `bf-pb-target-2` Table
  - icon: ![Table](../story/assets/items/bf-pb-target-2.webp)
- `bf-pb-arch-high` Upper arch
  - icon: ![Upper arch](../story/assets/items/bf-pb-arch-high.webp)
- `bf-pb-target-3` Table
  - icon: ![Table](../story/assets/items/bf-pb-target-3.webp)
- `bf-pb-score-flip` Flip
  - icon: ![Flip](../story/assets/actions/flip.svg)
- `bf-pb-score-facing` Table
  - icon: ![Table](../story/assets/items/bf-pb-score-facing.webp)
- `bf-pb-score` Score wheel
  - icon: ![Score wheel](../story/assets/items/bf-pb-score.webp)
- `bf-pb-scored` Table
  - icon: ![Table](../story/assets/items/bf-pb-scored.webp)
- `bf-pb-marble` Marble
  - icon: ![Marble](../story/assets/items/bf-pb-marble.webp)
- `pinball-table` Pinball table
  - icon: ![Pinball table](../story/assets/items/pinball-table.webp)
  - animation: ![Working toy](../story/assets/animations/pinball-table-working.webp)

**Combinations**
- `bf-pb-arch-low` [consume] + `bf-pb-launched` [transform] -> `bf-pb-target-1`
- `bf-pb-arch-mid` [consume] + `bf-pb-target-1` [transform] -> `bf-pb-target-2`
- `bf-pb-arch-high` [consume] + `bf-pb-target-2` [transform] -> `bf-pb-target-3`
- `bf-pb-target-3` [transform] @ `bf-pb-score-flip` -> `bf-pb-score-facing`
- `bf-pb-score` [consume] + `bf-pb-score-facing` [transform] -> `bf-pb-scored`
- `bf-pb-marble` [consume] + `bf-pb-scored` [transform] -> `pinball-table`

## `bf-cd-crank` Round and round
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Crank dragon](../story/assets/items/crank-dragon.webp)

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
- `bf-cd-flip` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-cd-shaft` Shaft
  - icon: ![Shaft](../story/assets/items/bf-cd-shaft.webp)

  ---

  A plain six-millimetre shaft, supplied without its collars. The cam and bearings slide on before the separate collars retain the shaft.
- `bf-cd-cam` Cam
  - icon: ![Cam](../story/assets/items/bf-cd-cam.webp)

  ---

  The shaft hole sits off centre. Turning the round disc raises and lowers the broad follower foot.
- `bf-cd-cammed` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-cammed.webp)
- `bf-cd-front-bearing` Front bearing
  - icon: ![Front bearing](../story/assets/items/bf-cd-front-bearing.webp)
- `bf-cd-bearing-1` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-bearing-1.webp)
- `bf-cd-rear-bearing` Rear bearing
  - icon: ![Rear bearing](../story/assets/items/bf-cd-rear-bearing.webp)
- `bf-cd-bearings` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-bearings.webp)
- `bf-cd-front-collar` Front collar
  - icon: ![Front collar](../story/assets/items/bf-cd-front-collar.webp)
- `bf-cd-front-retained` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-front-retained.webp)
- `bf-cd-flip` Flip
  - icon: ![Flip](../story/assets/actions/flip.svg)
- `bf-cd-rear-facing` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-rear-facing.webp)
- `bf-cd-rear-collar` Rear collar
  - icon: ![Rear collar](../story/assets/items/bf-cd-rear-collar.webp)
- `bf-cd-retained-rear` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-retained-rear.webp)
- `bf-cd-retained` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-retained.webp)
- `bf-cd-handle` Crank
  - icon: ![Crank](../story/assets/items/bf-cd-handle.webp)

  ---

  A D-shaped socket fits the matching shaft end. Its separate retaining clip enters the aligned cross holes after the crank is fitted.
- `bf-cd-cranked` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-cranked.webp)
- `bf-cd-crank-clip` Crank clip
  - icon: ![Crank clip](../story/assets/items/bf-cd-crank-clip.webp)

  ---

  One spring-wire clip. Its straight leg passes through the aligned crank and shaft holes; the curved leg grips outside the socket.
- `bf-cd-clipped` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-clipped.webp)
- `bf-cd-base` Base
  - icon: ![Base](../story/assets/items/bf-cd-base.webp)
- `bf-cd-frame` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-frame.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Crank dragon](../story/assets/items/crank-dragon.webp)

**Goals**
- Slide the Follower into the Guide -- `bf-cd-open-follower`
- next: Snap on the Cover -- `bf-cd-guided`
- next: Mount the Follower above the Cam -- `bf-cd-mounted`
- next: Hook on the Spring -- `bf-cd-lifter`

**Items**
- `bf-cd-guide` Guide
  - icon: ![Guide](../story/assets/items/bf-cd-guide.webp)

  ---

  An open square channel with a mounting foot and spring anchor. The separate cover closes around the follower; its broad foot never has to pass through the narrow channel.
- `bf-cd-follower` Follower
  - icon: ![Follower](../story/assets/items/bf-cd-follower.webp)

  ---

  A sliding rod with a broad cam foot, spring collar and retained crosshead pin for two independently pivoting links.
- `bf-cd-open-follower` Follower
  - icon: ![Follower](../story/assets/items/bf-cd-open-follower.webp)
- `bf-cd-cover` Cover
  - icon: ![Cover](../story/assets/items/bf-cd-cover.webp)
- `bf-cd-guided` Follower
  - icon: ![Follower](../story/assets/items/bf-cd-guided.webp)
- `bf-cd-frame` Frame
  - icon: ![Frame](../story/assets/items/bf-cd-frame.webp)
- `bf-cd-mounted` Lifter
  - icon: ![Lifter](../story/assets/items/bf-cd-mounted.webp)
- `bf-cd-spring` Spring
  - icon: ![Spring](../story/assets/items/bf-cd-spring.webp)
- `bf-cd-lifter` Lifter
  - icon: ![Lifter](../story/assets/items/bf-cd-lifter.webp)

**Combinations**
- `bf-cd-follower` [consume] + `bf-cd-guide` [transform] -> `bf-cd-open-follower`
- `bf-cd-cover` [consume] + `bf-cd-open-follower` [transform] -> `bf-cd-guided`
- `bf-cd-guided` [consume] + `bf-cd-frame` [transform] -> `bf-cd-mounted`
- `bf-cd-spring` [consume] + `bf-cd-mounted` [transform] -> `bf-cd-lifter`


## `bf-cd-dragon` The dragon
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Crank dragon](../story/assets/items/crank-dragon.webp)

**Goals**
- Attach the Left wing -- `bf-cd-body-left`
- next: Attach the Right wing -- `bf-cd-winged`
- next: Flip the Body to its back -- `bf-cd-winged-rear`
- next: Attach the Tail -- `bf-cd-bodied-rear`
- next: Flip the Body to its front -- `bf-cd-bodied`
- next: Mount the Dragon on the Lifter -- `bf-cd-mounted-body`
- next: Fit the Left link -- `bf-cd-linked-left`
- next: Fit the Right link -- `crank-dragon`

**Hotspots**
- `bf-cd-body-flip` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-cd-body` Body
  - icon: ![Body](../story/assets/items/bf-cd-body.webp)
- `bf-cd-left-wing` Left wing
  - icon: ![Left wing](../story/assets/items/bf-cd-left-wing.webp)

  ---

  One card wing with a prepared split snap pin and spacer. The two tapered tips compress through the body hole and reopen behind it.
- `bf-cd-body-left` Body
  - icon: ![Body](../story/assets/items/bf-cd-body-left.webp)
- `bf-cd-right-wing` Right wing
  - icon: ![Right wing](../story/assets/items/bf-cd-right-wing.webp)

  ---

  One card wing with a prepared split snap pin and spacer. The two tapered tips compress through the body hole and reopen behind it.
- `bf-cd-winged` Body
  - icon: ![Body](../story/assets/items/bf-cd-winged.webp)
- `bf-cd-body-flip` Flip
  - icon: ![Flip](../story/assets/actions/flip.svg)
- `bf-cd-winged-rear` Body
  - icon: ![Body](../story/assets/items/bf-cd-winged-rear.webp)
- `bf-cd-tail` Tail
  - icon: ![Tail](../story/assets/items/bf-cd-tail.webp)

  ---

  The tail carries a split snap pin. Its tapered tip passes through the body hole before its flexible barbs reopen.
- `bf-cd-bodied-rear` Body
  - icon: ![Body](../story/assets/items/bf-cd-bodied-rear.webp)
- `bf-cd-bodied` Dragon
  - icon: ![Dragon](../story/assets/items/bf-cd-bodied.webp)
- `bf-cd-lifter` Lifter
  - icon: ![Lifter](../story/assets/items/bf-cd-lifter.webp)
- `bf-cd-mounted-body` Dragon
  - icon: ![Dragon](../story/assets/items/bf-cd-mounted-body.webp)
- `bf-cd-left-link` Left link
  - icon: ![Left link](../story/assets/items/bf-cd-left-link.webp)

  ---

  One rigid 55 mm polymer link with two open snap eyes. Fit both eyes sideways over the exposed pin necks; their heads stay in place.
- `bf-cd-linked-left` Dragon
  - icon: ![Dragon](../story/assets/items/bf-cd-linked-left.webp)
- `bf-cd-right-link` Right link
  - icon: ![Right link](../story/assets/items/bf-cd-right-link.webp)

  ---

  One rigid 55 mm polymer link with two open snap eyes. It pivots independently beside the other link.
- `crank-dragon` Crank dragon
  - icon: ![Crank dragon](../story/assets/items/crank-dragon.webp)
  - animation: ![Working toy](../story/assets/animations/crank-dragon-working.webp)

**Combinations**
- `bf-cd-left-wing` [consume] + `bf-cd-body` [transform] -> `bf-cd-body-left`
- `bf-cd-right-wing` [consume] + `bf-cd-body-left` [transform] -> `bf-cd-winged`
- `bf-cd-winged` [transform] @ `bf-cd-body-flip` -> `bf-cd-winged-rear`
- `bf-cd-tail` [consume] + `bf-cd-winged-rear` [transform] -> `bf-cd-bodied-rear`
- `bf-cd-bodied-rear` [transform] @ `bf-cd-body-flip` -> `bf-cd-bodied`
- `bf-cd-bodied` [consume] + `bf-cd-lifter` [transform] -> `bf-cd-mounted-body`
- `bf-cd-left-link` [consume] + `bf-cd-mounted-body` [transform] -> `bf-cd-linked-left`
- `bf-cd-right-link` [consume] + `bf-cd-linked-left` [transform] -> `crank-dragon`

## `c-gantry-frame` A lifting frame
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Gantry](../story/assets/items/gh-mounted.webp)

**Goals**
- Fit a side frame -- `gh-one-side`
- next: Fit the other side frame -- `gh-two-sides`
- next: Join the frames with the beam -- `gh-frame`
- next: Fit the ratchet to the winch
  - either: `gh-ratchet-winch`
  - or: `gh-winch`
- next: Turn the winch toward its crank end
  - either: `gh-rear-drum`
  - or: `gh-rear-ratchet-winch`
- next: Fit the crank
  - either: `gh-crank-winch`
  - or: `gh-rear-winch`
- next: Turn the winch back toward the ratchet
  - either: `gh-front-crank-winch`
  - or: `gh-winch`
- next: Mount the winch -- `gh-mounted`

**Hotspots**
- `gh-winch-flip` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `gh-base` Base
  - icon: ![Base](../story/assets/items/gh-base.webp)
- `gh-side-1` Side frame
  - icon: ![Side frame](../story/assets/items/gh-side-1.webp)

  ---

  A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.

- `gh-side-2` Side frame
  - icon: ![Side frame](../story/assets/items/gh-side-2.webp)

  ---

  A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.

- `gh-crossbeam` Beam
  - icon: ![Beam](../story/assets/items/gh-crossbeam.webp)

  ---

  The beam has two end sockets and separate sockets underneath for the pulley forks.

- `gh-one-side` Frame
  - icon: ![Frame](../story/assets/items/gh-one-side.webp)
- `gh-two-sides` Frame
  - icon: ![Frame](../story/assets/items/gh-two-sides.webp)
- `gh-frame` Frame
  - icon: ![Frame](../story/assets/items/gh-frame.webp)
- `gh-drum` Winch
  - icon: ![Winch](../story/assets/items/gh-drum.webp)

  ---

  The winch drum comes with its axle, two bearing cheeks, captive base fasteners and a sprung cord clamp.

- `gh-ratchet` Ratchet
  - icon: ![Ratchet](../story/assets/items/gh-ratchet.webp)
- `gh-crank` Crank
  - icon: ![Crank](../story/assets/items/gh-crank.webp)
- `gh-ratchet-winch` Winch
  - icon: ![Winch](../story/assets/items/gh-ratchet-winch.webp)
- `gh-crank-winch` Winch
  - icon: ![Winch](../story/assets/items/gh-crank-winch.webp)
- `gh-winch` Winch
  - icon: ![Winch](../story/assets/items/gh-winch.webp)
- `gh-rear-drum` Winch
  - icon: ![Winch](../story/assets/items/gh-rear-drum.webp)
- `gh-rear-ratchet-winch` Winch
  - icon: ![Winch](../story/assets/items/gh-rear-ratchet-winch.webp)
- `gh-rear-winch` Winch
  - icon: ![Winch](../story/assets/items/gh-rear-winch.webp)
- `gh-front-crank-winch` Winch
  - icon: ![Winch](../story/assets/items/gh-front-crank-winch.webp)
- `gh-mounted` Gantry
  - icon: ![Gantry](../story/assets/items/gh-mounted.webp)
- `gh-winch-flip` Flip

**Combinations**
- `gh-side-1` [consume] + `gh-base` [transform] -> `gh-one-side`
- `gh-side-2` [consume] + `gh-base` [transform] -> `gh-one-side`
- `gh-side-1` [consume] + `gh-one-side` [transform] -> `gh-two-sides`
- `gh-side-2` [consume] + `gh-one-side` [transform] -> `gh-two-sides`
- `gh-crossbeam` [consume] + `gh-two-sides` [transform] -> `gh-frame`
- `gh-ratchet` [consume] + `gh-drum` [transform] -> `gh-ratchet-winch`
- `gh-ratchet` [consume] + `gh-front-crank-winch` [transform] -> `gh-winch`
- `gh-drum` [transform] @ `gh-winch-flip` -> `gh-rear-drum`
- `gh-ratchet-winch` [transform] @ `gh-winch-flip` -> `gh-rear-ratchet-winch`
- `gh-crank` [consume] + `gh-rear-drum` [transform] -> `gh-crank-winch`
- `gh-crank` [consume] + `gh-rear-ratchet-winch` [transform] -> `gh-rear-winch`
- `gh-crank-winch` [transform] @ `gh-winch-flip` -> `gh-front-crank-winch`
- `gh-rear-winch` [transform] @ `gh-winch-flip` -> `gh-winch`
- `gh-winch` [consume] + `gh-frame` [transform] -> `gh-mounted`

## `c-gantry-rope` Over the beam
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Gantry hoist](../story/assets/items/gantry-hoist.webp)

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
  - icon: ![Side fork](../story/assets/items/gh-side-fork.webp)

  ---

  An open pulley bracket with a split snap axle and a barbed mounting stem. Press a pulley over the axle tip, then push the stem through the beam until its head opens above the wood.

- `gh-side-pulley` Pulley unit
  - icon: ![Pulley unit](../story/assets/items/gh-side-pulley.webp)
- `gh-drop-fork` Drop fork
  - icon: ![Drop fork](../story/assets/items/gh-drop-fork.webp)

  ---

  An open pulley bracket with a split snap axle and a barbed mounting stem. Press a pulley over the axle tip, then push the stem through the beam until its head opens above the wood.

- `gh-drop-pulley` Pulley unit
  - icon: ![Pulley unit](../story/assets/items/gh-drop-pulley.webp)
- `gh-pulley-1` Pulley
  - icon: ![Pulley](../story/assets/items/gh-pulley-1.webp)

  ---

  A grooved pulley that turns on either fork axle. The split axle tip retains it.

- `gh-pulley-2` Pulley
  - icon: ![Pulley](../story/assets/items/gh-pulley-2.webp)

  ---

  A grooved pulley that turns on either fork axle. The split axle tip retains it.

- `gh-pawl` Pawl
  - icon: ![Pawl](../story/assets/items/gh-pawl.webp)

  ---

  A spring pawl and its connected mounting foot. Its tooth rests in the ratchet so the drum cannot freely unwind.

- `gh-rope` Rope and hook
  - icon: ![Rope and hook](../story/assets/items/gh-rope.webp)

  ---

  One continuous cord, already tied to its hook. Push its free end under the drum’s prepared spring clamp, wind one turn, then thread it over the two pulleys.

- `gh-basket` Basket
  - icon: ![Basket](../story/assets/items/gh-basket.webp)

  ---

  A small rigid basket with a connected lifting handle. It hangs directly on the hook.

- `gh-fitted-1` Gantry
  - icon: ![Gantry](../story/assets/items/gh-fitted-1.webp)
- `gh-fitted-2` Gantry
  - icon: ![Gantry](../story/assets/items/gh-fitted-2.webp)
- `gh-fitted-3` Gantry
  - icon: ![Gantry](../story/assets/items/gh-fitted-3.webp)
- `gh-fitted-4` Gantry
  - icon: ![Gantry](../story/assets/items/gh-fitted-4.webp)
- `gh-fitted-5` Gantry
  - icon: ![Gantry](../story/assets/items/gh-fitted-5.webp)
- `gh-fitted-6` Gantry
  - icon: ![Gantry](../story/assets/items/gh-fitted-6.webp)
- `gh-fitted-7` Gantry
  - icon: ![Gantry](../story/assets/items/gh-fitted-7.webp)
- `gh-roped` Hoist
  - icon: ![Hoist](../story/assets/items/gh-roped.webp)
- `gantry-hoist` Gantry hoist
  - icon: ![Gantry hoist](../story/assets/items/gantry-hoist.webp)
  - animation: ![Working toy](../story/assets/animations/gantry-hoist-working.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Carousel](../story/assets/items/ca-platform.webp)

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
  - icon: ![Base](../story/assets/items/ca-base.webp)

  ---

  A broad prepared base with sockets for the bearing, motor and battery. The motor and controller are matching low-voltage modules.

- `ca-spindle` Spindle
  - icon: ![Spindle](../story/assets/items/ca-spindle.webp)

  ---

  A vertical spindle and pulley retained inside a bearing block. The square upper end drives the deck; a shoulder supports its hub above the guard.

- `ca-motor` Motor
  - icon: ![Motor](../story/assets/items/ca-motor.webp)

  ---

  A small enclosed geared motor, its pulley, retaining strap, mounting foot and plugged lead form one supplied module.

- `ca-belt` Belt
  - icon: ![Belt](../story/assets/items/ca-belt.webp)
- `ca-guard` Guard
  - icon: ![Guard](../story/assets/items/ca-guard.webp)

  ---

  A clear cover with a real shaft opening, cable opening and attached locating feet.

- `ca-battery` Battery and dial
  - icon: ![Battery and dial](../story/assets/items/ca-battery.webp)

  ---

  The battery holder, switch and speed dial share one case. Its connected lead plugs into the motor.

- `ca-deck` Deck
  - icon: ![Deck](../story/assets/items/ca-deck.webp)

  ---

  A round deck with a central drive socket and three prepared pole sockets.

- `ca-spindle-base` Base
  - icon: ![Base](../story/assets/items/ca-spindle-base.webp)
- `ca-motor-base` Base
  - icon: ![Base](../story/assets/items/ca-motor-base.webp)
- `ca-drive-base` Base
  - icon: ![Base](../story/assets/items/ca-drive-base.webp)
- `ca-belted` Base
  - icon: ![Base](../story/assets/items/ca-belted.webp)
- `ca-guarded` Base
  - icon: ![Base](../story/assets/items/ca-guarded.webp)
- `ca-wired` Base
  - icon: ![Base](../story/assets/items/ca-wired.webp)
- `ca-ready` Base
  - icon: ![Base](../story/assets/items/ca-ready.webp)
- `ca-platform` Carousel
  - icon: ![Carousel](../story/assets/items/ca-platform.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Electric carousel](../story/assets/items/electric-carousel.webp)

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
  - icon: ![Red horse](../story/assets/items/ca-horse-1.webp)

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-1` Pole
  - icon: ![Pole](../story/assets/items/ca-pole-1.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-1` Red horse
  - icon: ![Red horse](../story/assets/items/ca-rider-1.webp)
- `ca-horse-2` Green horse
  - icon: ![Green horse](../story/assets/items/ca-horse-2.webp)

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-2` Pole
  - icon: ![Pole](../story/assets/items/ca-pole-2.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-2` Green horse
  - icon: ![Green horse](../story/assets/items/ca-rider-2.webp)
- `ca-horse-3` Cream horse
  - icon: ![Cream horse](../story/assets/items/ca-horse-3.webp)

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-3` Pole
  - icon: ![Pole](../story/assets/items/ca-pole-3.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-3` Cream horse
  - icon: ![Cream horse](../story/assets/items/ca-rider-3.webp)
- `ca-horses-1` Carousel
  - icon: ![Carousel](../story/assets/items/ca-horses-1.webp)
- `ca-horses-2` Carousel
  - icon: ![Carousel](../story/assets/items/ca-horses-2.webp)
- `ca-horses-3` Carousel
  - icon: ![Carousel](../story/assets/items/ca-horses-3.webp)
- `ca-horses-4` Carousel
  - icon: ![Carousel](../story/assets/items/ca-horses-4.webp)
- `ca-horses-5` Carousel
  - icon: ![Carousel](../story/assets/items/ca-horses-5.webp)
- `ca-horses-6` Carousel
  - icon: ![Carousel](../story/assets/items/ca-horses-6.webp)
- `ca-horses-7` Carousel
  - icon: ![Carousel](../story/assets/items/ca-horses-7.webp)
- `ca-roofpost` Roof post
  - icon: ![Roof post](../story/assets/items/ca-roofpost.webp)
- `ca-canopy` Canopy
  - icon: ![Canopy](../story/assets/items/ca-canopy.webp)

  ---

  A small moulded canopy with a centre socket. It sits high enough to leave the horses visible.

- `ca-posted` Carousel
  - icon: ![Carousel](../story/assets/items/ca-posted.webp)
- `electric-carousel` Electric carousel
  - icon: ![Electric carousel](../story/assets/items/electric-carousel.webp)
  - animation: ![Working toy](../story/assets/animations/electric-carousel-working.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Claw](../story/assets/items/cl-mechanical.webp)

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
  - icon: ![Palm](../story/assets/items/cl-base.webp)

  ---

  A broad prepared palm with pivot holes and a fixed return-band hook. The jaws reach just beyond its front edge.

- `cl-jaw-1` Left jaw
  - icon: ![Left jaw](../story/assets/items/cl-jaw-1.webp)

  ---

  A single jaw with captive pivot and link pins. Its left-facing shape matches the left side of the palm.

- `cl-jaw-2` Right jaw
  - icon: ![Right jaw](../story/assets/items/cl-jaw-2.webp)

  ---

  The reflected right jaw has its own captive pins.

- `cl-slider` Slider
  - icon: ![Slider](../story/assets/items/cl-slider.webp)

  ---

  One retained sliding shoe inside its guide, including travel stops and the moving return-band hook.

- `cl-link-1` Link
  - icon: ![Link](../story/assets/items/cl-link-1.webp)

  ---

  A rigid 52 mm link with split eyes that snap sideways onto the captive pins. Either link fits either side.

- `cl-link-2` Link
  - icon: ![Link](../story/assets/items/cl-link-2.webp)

  ---

  A rigid 52 mm link with split eyes. Either link fits either side.

- `cl-pad-1` Pad
  - icon: ![Pad](../story/assets/items/cl-pad-1.webp)

  ---

  One soft pad for the inside face of a jaw. Either pad fits either jaw.

- `cl-pad-2` Pad
  - icon: ![Pad](../story/assets/items/cl-pad-2.webp)

  ---

  One soft pad. Either pad fits either jaw.

- `cl-mech-1` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-1.webp)
- `cl-mech-2` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-2.webp)
- `cl-mech-3` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-3.webp)
- `cl-mech-4` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-4.webp)
- `cl-mech-5` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-5.webp)
- `cl-mech-6` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-6.webp)
- `cl-mech-7` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-7.webp)
- `cl-mech-13` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-13.webp)
- `cl-mech-15` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-15.webp)
- `cl-mech-22` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-22.webp)
- `cl-mech-23` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-23.webp)
- `cl-mech-31` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-31.webp)
- `cl-mech-33` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-33.webp)
- `cl-mech-35` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-35.webp)
- `cl-mech-37` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-37.webp)
- `cl-mech-39` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-39.webp)
- `cl-mech-45` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-45.webp)
- `cl-mech-47` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-47.webp)
- `cl-mech-55` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-55.webp)
- `cl-mech-63` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-63.webp)
- `cl-mech-66` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-66.webp)
- `cl-mech-67` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-67.webp)
- `cl-mech-70` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-70.webp)
- `cl-mech-71` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-71.webp)
- `cl-mech-79` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-79.webp)
- `cl-mech-86` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-86.webp)
- `cl-mech-87` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-87.webp)
- `cl-mech-95` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-95.webp)
- `cl-mech-99` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-99.webp)
- `cl-mech-103` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-103.webp)
- `cl-mech-111` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-111.webp)
- `cl-mech-119` Claw
  - icon: ![Claw](../story/assets/items/cl-mech-119.webp)
- `cl-mechanical` Claw
  - icon: ![Claw](../story/assets/items/cl-mechanical.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Pneumatic claw](../story/assets/items/pneumatic-claw.webp)

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
  - icon: ![Output syringe](../story/assets/items/cl-output.webp)

  ---

  A prepared needleless syringe. Its rigid piston and stem move inside a real hollow barrel.

- `cl-rear-cup` Cup
  - icon: ![Cup](../story/assets/items/cl-rear-cup.webp)

  ---

  Either identical cup fits either barrel seat. Slide the first over the nozzle to the farther seat, then slide the other onto the nearer seat. Each has a soft retaining strap and captive mounting pins.

- `cl-front-cup` Cup
  - icon: ![Cup](../story/assets/items/cl-front-cup.webp)

  ---

  Either identical cup fits either barrel seat. Slide the first over the nozzle to the farther seat, then slide the other onto the nearer seat. Each has a soft retaining strap and captive mounting pins.

- `cl-clip` Plunger clip
  - icon: ![Plunger clip](../story/assets/items/cl-clip.webp)

  ---

  A connected clip that plugs into the slider and captures the syringe thumb flange.

- `cl-band` Return band
  - icon: ![Return band](../story/assets/items/cl-band.webp)

  ---

  One soft elastic loop. Its two hook brackets are already attached to the palm and slider.

- `cl-input` Hand syringe
  - icon: ![Hand syringe](../story/assets/items/cl-input.webp)

  ---

  A second prepared needleless syringe. It stays beside the claw, joined by the flexible hose.

- `cl-tube` Air hose
  - icon: ![Air hose](../story/assets/items/cl-tube.webp)

  ---

  One continuous flexible hose with an open end for each syringe nozzle.

- `cl-front-supported` Syringe
  - icon: ![Syringe](../story/assets/items/cl-front-supported.webp)
- `cl-supported-output` Syringe
  - icon: ![Syringe](../story/assets/items/cl-supported-output.webp)
- `cl-air-1` Claw
  - icon: ![Claw](../story/assets/items/cl-air-1.webp)
- `cl-air-3` Claw
  - icon: ![Claw](../story/assets/items/cl-air-3.webp)
- `cl-air-4` Claw
  - icon: ![Claw](../story/assets/items/cl-air-4.webp)
- `cl-air-5` Claw
  - icon: ![Claw](../story/assets/items/cl-air-5.webp)
- `cl-air-7` Claw
  - icon: ![Claw](../story/assets/items/cl-air-7.webp)
- `cl-controller` Hand syringe
  - icon: ![Hand syringe](../story/assets/items/cl-controller.webp)
- `pneumatic-claw` Pneumatic claw
  - icon: ![Pneumatic claw](../story/assets/items/pneumatic-claw.webp)
  - animation: ![Working toy](../story/assets/animations/pneumatic-claw-working.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Animation drum](../story/assets/items/animation-drum.webp)

**Goals**
- Cut the marked viewing slits -- `bf-film-cut`
- next: Roll the Drum wall -- `bf-film-rolled`
- next: Tape the seam -- `bf-film-seamed`

**Hotspots**
- `bf-film-cut-process` (center 130px, 216px)
  - icon: ![Cut](../story/assets/actions/cut.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)
- `bf-film-roll-process` (center 390px, 216px)
  - icon: ![Roll](../story/assets/actions/roll.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-film-wall` Drum wall
  - icon: ![Drum wall](../story/assets/items/bf-film-wall.webp)

  ---

  One card strip with twelve marked slots and scored floor tabs. Their tips stay straight until the floor is seated. Cut down to the stopping line; the lower band stays continuous.
- `bf-film-cut-process` Cut
  - icon: ![Cut](../story/assets/actions/cut.svg)
- `bf-film-cut` Drum wall
  - icon: ![Drum wall](../story/assets/items/bf-film-cut.webp)
- `bf-film-roll-process` Roll
  - icon: ![Roll](../story/assets/actions/roll.svg)
- `bf-film-rolled` Drum
  - icon: ![Drum](../story/assets/items/bf-film-rolled.webp)
- `bf-film-tape` Tape
  - icon: ![Tape](../story/assets/items/bf-film-tape.webp)
- `bf-film-seamed` Drum
  - icon: ![Drum](../story/assets/items/bf-film-seamed.webp)

**Combinations**
- `bf-film-wall` [transform] @ `bf-film-cut-process` -> `bf-film-cut`
- `bf-film-cut` [transform] @ `bf-film-roll-process` -> `bf-film-rolled`
- `bf-film-tape` [consume] + `bf-film-rolled` [transform] -> `bf-film-seamed`


## `bf-film-floor-build` A turning drum
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Animation drum](../story/assets/items/animation-drum.webp)

**Goals**
- Flip the Drum over -- `bf-film-under`
- next: Fold the scored tabs inward -- `bf-film-prepared`
- next: Slide the Floor over the straight tips -- `bf-film-seated`
- next: Fold the tabs under the Floor -- `bf-film-shell`
- next: Fit the Turntable to the Base -- `bf-film-turntable`
- next: Flip the Base over -- `bf-film-inverted-base`
- next: Fit the Base beneath the Drum -- `bf-film-mounted-under`
- next: Flip the Drum upright -- `bf-film-standing`

**Hotspots**
- `bf-film-flip-process` (center 130px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)
- `bf-film-fold-process` (center 390px, 216px)
  - icon: ![Fold](../story/assets/actions/fold.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-film-seamed` Drum
  - icon: ![Drum](../story/assets/items/bf-film-seamed.webp)
- `bf-film-flip-process` Flip
  - icon: ![Flip](../story/assets/actions/flip.svg)
- `bf-film-under` Drum
  - icon: ![Drum](../story/assets/items/bf-film-under.webp)
- `bf-film-fold-process` Fold
  - icon: ![Fold](../story/assets/actions/fold.svg)
- `bf-film-prepared` Drum
  - icon: ![Drum](../story/assets/items/bf-film-prepared.webp)
- `bf-film-floor` Floor
  - icon: ![Floor](../story/assets/items/bf-film-floor.webp)

  ---

  A 178.8 mm disc, smaller than the wall opening, with twelve slots for the straight tabs. Fold the tips underneath only after inserting it.
- `bf-film-seated` Drum
  - icon: ![Drum](../story/assets/items/bf-film-seated.webp)
- `bf-film-shell` Drum
  - icon: ![Drum](../story/assets/items/bf-film-shell.webp)
- `bf-film-base` Base
  - icon: ![Base](../story/assets/items/bf-film-base.webp)
- `bf-film-bearing` Turntable
  - icon: ![Turntable](../story/assets/items/bf-film-bearing.webp)

  ---

  One retained spindle, sleeve bearing and platform. The spindle stays fixed in the base while the platform turns.
- `bf-film-turntable` Base
  - icon: ![Base](../story/assets/items/bf-film-turntable.webp)
- `bf-film-inverted-base` Base
  - icon: ![Base](../story/assets/items/bf-film-inverted-base.webp)
- `bf-film-mounted-under` Drum
  - icon: ![Drum](../story/assets/items/bf-film-mounted-under.webp)
- `bf-film-standing` Drum
  - icon: ![Drum](../story/assets/items/bf-film-standing.webp)

**Combinations**
- `bf-film-seamed` [transform] @ `bf-film-flip-process` -> `bf-film-under`
- `bf-film-under` [transform] @ `bf-film-fold-process` -> `bf-film-prepared`
- `bf-film-floor` [consume] + `bf-film-prepared` [transform] -> `bf-film-seated`
- `bf-film-seated` [transform] @ `bf-film-fold-process` -> `bf-film-shell`
- `bf-film-bearing` [consume] + `bf-film-base` [transform] -> `bf-film-turntable`
- `bf-film-turntable` [transform] @ `bf-film-flip-process` -> `bf-film-inverted-base`
- `bf-film-inverted-base` [consume] + `bf-film-shell` [transform] -> `bf-film-mounted-under`
- `bf-film-mounted-under` [transform] @ `bf-film-flip-process` -> `bf-film-standing`


## `bf-film-pictures` A tiny picture show
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Animation drum](../story/assets/items/animation-drum.webp)

**Goals**
- Roll the Picture strip -- `bf-film-loop`
- next: Fit the Picture ring inside the Drum -- `animation-drum`

**Hotspots**
- `bf-film-picture-roll` (center 390px, 216px)
  - icon: ![Roll](../story/assets/actions/roll.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `bf-film-strip` Picture strip
  - icon: ![Picture strip](../story/assets/items/bf-film-strip.webp)

  ---

  A printed sequence of twelve fish pictures, one per viewing slit, with a prepared adhesive overlap. The pictures face inward when rolled.
- `bf-film-picture-roll` Roll
  - icon: ![Roll](../story/assets/actions/roll.svg)
- `bf-film-loop` Picture ring
  - icon: ![Picture ring](../story/assets/items/bf-film-loop.webp)
- `bf-film-standing` Drum
  - icon: ![Drum](../story/assets/items/bf-film-standing.webp)
- `animation-drum` Animation drum
  - icon: ![Animation drum](../story/assets/items/animation-drum.webp)
  - animation: ![Working toy](../story/assets/animations/animation-drum-working.webp)

  ---

  Looking through the slits gives brief separated glimpses of successive pictures, with darkness between them.

**Combinations**
- `bf-film-strip` [transform] @ `bf-film-picture-roll` -> `bf-film-loop`
- `bf-film-loop` [consume] + `bf-film-standing` [transform] -> `animation-drum`

## `c-rover-drive` Two wheels, two motors
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Rover](../story/assets/items/rv-mounted.webp)

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
- `rv-flip-build` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `rv-deck` Deck
  - icon: ![Deck](../story/assets/items/rv-deck.webp)

  ---

  The prepared deck includes two bare pen guide rods and a hand-operated lift cam. Fit the carriage, then its return spring and connected guide cap.
- `rv-motor-a` Left motor
  - icon: ![Left motor](../story/assets/items/rv-motor-a.webp)

  ---

  An enclosed slow gearmotor, mounting flange and attached lead. Its output shaft drives one wheel.
- `rv-motor-b` Right motor
  - icon: ![Right motor](../story/assets/items/rv-motor-b.webp)

  ---

  An enclosed slow gearmotor, mounting flange and attached lead. Its output shaft drives one wheel.
- `rv-wheel-a` Wheel
  - icon: ![Wheel](../story/assets/items/rv-wheel.webp)

  ---

  Either wheel fits either geared motor. Its retained centre fastener locks the hub to the flat-sided shaft.
- `rv-wheel-b` Wheel
  - icon: ![Wheel](../story/assets/items/rv-wheel.webp)

  ---

  Either wheel fits either geared motor. Its retained centre fastener locks the hub to the flat-sided shaft.
- `rv-caster` Caster
  - icon: ![Caster](../story/assets/items/rv-caster.webp)

  ---

  The free-turning ball supports the third corner.
- `rv-pack` Battery pack
  - icon: ![Battery pack](../story/assets/items/rv-pack.webp)

  ---

  An enclosed compatible low-voltage pack with cells already fitted.
- `rv-receiver` Receiver
  - icon: ![Receiver](../story/assets/items/rv-receiver.webp)

  ---

  The supplied receiver and motor driver control the wheels independently. Its matching ready-to-use remote needs no construction here.
- `rv-under` Deck
  - icon: ![Deck](../story/assets/items/rv-under.webp)
- `rv-drive-a` Left drive
  - icon: ![Left drive](../story/assets/items/rv-drive-a.webp)
- `rv-drive-b` Right drive
  - icon: ![Right drive](../story/assets/items/rv-drive-b.webp)
- `rv-deck-01` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-01.webp)
- `rv-deck-02` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-02.webp)
- `rv-deck-03` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-03.webp)
- `rv-deck-04` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-04.webp)
- `rv-deck-05` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-05.webp)
- `rv-deck-06` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-06.webp)
- `rv-deck-07` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-07.webp)
- `rv-deck-08` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-08.webp)
- `rv-deck-09` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-09.webp)
- `rv-deck-10` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-10.webp)
- `rv-deck-11` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-11.webp)
- `rv-deck-12` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-12.webp)
- `rv-deck-13` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-13.webp)
- `rv-deck-14` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-14.webp)
- `rv-deck-15` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-15.webp)
- `rv-deck-16` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-16.webp)
- `rv-deck-17` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-17.webp)
- `rv-deck-18` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-18.webp)
- `rv-deck-19` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-19.webp)
- `rv-deck-20` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-20.webp)
- `rv-deck-21` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-21.webp)
- `rv-deck-22` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-22.webp)
- `rv-deck-23` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-23.webp)
- `rv-deck-24` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-24.webp)
- `rv-deck-25` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-25.webp)
- `rv-deck-26` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-26.webp)
- `rv-deck-27` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-27.webp)
- `rv-deck-28` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-28.webp)
- `rv-deck-29` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-29.webp)
- `rv-deck-30` Rover
  - icon: ![Rover](../story/assets/items/rv-deck-30.webp)
- `rv-mounted` Rover
  - icon: ![Rover](../story/assets/items/rv-mounted.webp)
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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Drawing rover](../story/assets/items/drawing-rover.webp)

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
- `rv-flip-pen` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `rv-harness` Switch harness
  - icon: ![Switch harness](../story/assets/items/rv-harness.webp)

  ---

  A connected fused harness and switch. Fit with the power off and connect the parked battery and motor plugs to their matching sockets.
- `rv-guard-a` Guard
  - icon: ![Guard](../story/assets/items/rv-guard-a.webp)

  ---

  One hollow snap-on guard. Its open shaft slot and split cable channel fit around the already attached wheel and lead.
- `rv-guard-b` Guard
  - icon: ![Guard](../story/assets/items/rv-guard-b.webp)

  ---

  One hollow snap-on guard, fitted independently on the other drive.
- `rv-pen` Pen
  - icon: ![Pen](../story/assets/items/rv-pen.webp)

  ---

  A felt-tip pen with its cap removed.
- `rv-clip` Pen carriage
  - icon: ![Pen carriage](../story/assets/items/rv-clip.webp)

  ---

  One connected bridge, spring clip and follower shoe. The deck already carries the guides and lift lever.
- `rv-spring` Return spring
  - icon: ![Return spring](../story/assets/items/rv-spring.webp)

  ---

  One compression spring slides down the near guide rod after the carriage. The guide cap retains its upper end.
- `rv-cap` Guide cap
  - icon: ![Guide cap](../story/assets/items/rv-cap.webp)

  ---

  One connected bridge with two soft lined sockets. Press it onto the two bare guide ends to retain the carriage and compress its return spring.
- `rv-wired` Rover
  - icon: ![Rover](../story/assets/items/rv-wired.webp)
- `rv-one-guard-a` Rover
  - icon: ![Rover](../story/assets/items/rv-one-guard-a.webp)
- `rv-one-guard-b` Rover
  - icon: ![Rover](../story/assets/items/rv-one-guard-b.webp)
- `rv-guarded` Rover
  - icon: ![Rover](../story/assets/items/rv-guarded.webp)
- `rv-upright` Rover
  - icon: ![Rover](../story/assets/items/rv-upright.webp)
- `rv-pen-carriage` Pen carriage
  - icon: ![Pen carriage](../story/assets/items/rv-pen-carriage.webp)
- `rv-pen-fitted` Rover
  - icon: ![Rover](../story/assets/items/rv-pen-fitted.webp)
- `rv-sprung` Rover
  - icon: ![Rover](../story/assets/items/rv-sprung.webp)
- `drawing-rover` Drawing rover
  - icon: ![Drawing rover](../story/assets/items/drawing-rover.webp)
  - animation: ![Working toy](../story/assets/animations/drawing-rover-working.webp)

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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Projector](../story/assets/items/pj-wheel-box.webp)

**Goals**
- Fit the reflector inside the box -- `pj-lined`
- next: Punch stars around the disc -- `pj-stars`
- next: Slide the disc onto the spindle -- `pj-disc-shaft`
- next: Fit the disc collar -- `pj-wheel`
- next: Turn the star wheel to its loading side -- `pj-wheel-loading`
- next: Lower the star wheel into the bearings -- `pj-loaded`
- next: Turn the box toward the lamp seat -- `pj-lamp-facing`
- next: Fit the lamp -- `pj-lamped`
- next: Connect the battery pack -- `pj-wheel-box`

**Hotspots**
- `pj-punch` (center 130px, 216px)
  - icon: ![Punch](../story/assets/actions/punch.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)
- `pj-flip` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `pj-box` Box
  - icon: ![Box](../story/assets/items/pj-box.webp)

  ---

  An open prepared box with two upward-opening bearing cradles. Prepared loading slots let the complete star wheel lower into them; the lid closes those slots and retains the shaft.
- `pj-liner` Reflector
  - icon: ![Reflector](../story/assets/items/pj-liner.webp)

  ---

  One folded U-shaped reflector joins its floor and side faces. It leaves the electrical contacts clear.
- `pj-lamp` Lamp
  - icon: ![Lamp](../story/assets/items/pj-lamp.webp)

  ---

  A cool-running diffused LED module, holder, current-limiting resistor and attached lead.
- `pj-battery` Battery pack
  - icon: ![Battery pack](../story/assets/items/pj-battery.webp)

  ---

  An enclosed compatible switched low-voltage pack with its connected holder and fused lead. Connect with the switch off.
- `pj-card` Card disc
  - icon: ![Card disc](../story/assets/items/pj-card.webp)

  ---

  The flat-sided centre hole matches the spindle.
- `pj-spindle` Spindle
  - icon: ![Spindle](../story/assets/items/pj-spindle.webp)

  ---

  The flat continues from the free front end to the disc seat. Slide the disc along it until it reaches the fixed rear shoulder. The two rear flanges locate the shaft in its bearing.
- `pj-collar` Disc collar
  - icon: ![Disc collar](../story/assets/items/pj-collar.webp)

  ---

  Slide this flat-sided collar along the same free end, then tighten its captive screw against the shaft flat. It holds the disc against the fixed shoulder.
- `pj-lined` Projector
  - icon: ![Projector](../story/assets/items/pj-lined.webp)
- `pj-loaded` Projector
  - icon: ![Projector](../story/assets/items/pj-loaded.webp)
- `pj-lamp-facing` Projector
  - icon: ![Projector](../story/assets/items/pj-lamp-facing.webp)
- `pj-lamped` Projector
  - icon: ![Projector](../story/assets/items/pj-lamped.webp)
- `pj-stars` Star disc
  - icon: ![Star disc](../story/assets/items/pj-stars.webp)
- `pj-disc-shaft` Star wheel
  - icon: ![Star wheel](../story/assets/items/pj-disc-shaft.webp)
- `pj-wheel` Star wheel
  - icon: ![Star wheel](../story/assets/items/pj-wheel.webp)
- `pj-wheel-loading` Star wheel
  - icon: ![Star wheel](../story/assets/items/pj-wheel-loading.webp)
- `pj-wheel-box` Projector
  - icon: ![Projector](../story/assets/items/pj-wheel-box.webp)
- `pj-punch` Punch
- `pj-flip` Flip

**Combinations**
- `pj-card` [transform] @ `pj-punch` -> `pj-stars`
- `pj-stars` [consume] + `pj-spindle` [transform] -> `pj-disc-shaft`
- `pj-collar` [consume] + `pj-disc-shaft` [transform] -> `pj-wheel`
- `pj-wheel` [transform] @ `pj-flip` -> `pj-wheel-loading`
- `pj-loaded` [transform] @ `pj-flip` -> `pj-lamp-facing`
- `pj-liner` [consume] + `pj-box` [transform] -> `pj-lined`
- `pj-wheel-loading` [consume] + `pj-lined` [transform] -> `pj-loaded`
- `pj-lamp` [consume] + `pj-lamp-facing` [transform] -> `pj-lamped`
- `pj-battery` [consume] + `pj-lamped` [transform] -> `pj-wheel-box`


## `c-projector-lens` Bring the stars into focus
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Star projector](../story/assets/items/star-projector.webp)

**Goals**
- Close the box with its lid -- `pj-closed`
- next: Turn the box toward the lens opening -- `pj-front-closed`
- next: Fit the lens into its holder -- `pj-focus`
- next: Fit the holder to the box -- `pj-focused`
- next: Fit the hood around the lens -- `pj-hooded`
- next: Fit the handle to the spindle -- `star-projector`

**Hotspots**
- `pj-flip` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `pj-lens` Lens
  - icon: ![Lens](../story/assets/items/pj-lens.webp)

  ---

  A single convex lens forms an inverted image of the lit holes.
- `pj-holder` Lens holder
  - icon: ![Lens holder](../story/assets/items/pj-holder.webp)

  ---

  A connected sliding carriage retained on its rails. Move it along the rails to focus.
- `pj-hood` Hood
  - icon: ![Hood](../story/assets/items/pj-hood.webp)

  ---

  The dark tube surrounds the lens without covering its clear aperture.
- `pj-handle` Handle
  - icon: ![Handle](../story/assets/items/pj-handle.webp)

  ---

  The handwheel has a real belt groove behind its grip. It can be turned by hand now and driven by a belt later.
- `pj-lid` Lid
  - icon: ![Lid](../story/assets/items/pj-lid.webp)

  ---

  One connected lid with locating tabs, shaft retainers and two downward tongues. The inner tongue carries the real projection window. Fit the lid before the external lens rails, which pass through its prepared openings.
- `pj-closed` Projector
  - icon: ![Projector](../story/assets/items/pj-closed.webp)
- `pj-front-closed` Projector
  - icon: ![Projector](../story/assets/items/pj-front-closed.webp)
- `pj-focus` Lens holder
  - icon: ![Lens holder](../story/assets/items/pj-focus.webp)
- `pj-focused` Projector
  - icon: ![Projector](../story/assets/items/pj-focused.webp)
- `pj-hooded` Projector
  - icon: ![Projector](../story/assets/items/pj-hooded.webp)
- `star-projector` Star projector
  - icon: ![Star projector](../story/assets/items/star-projector.webp)
  - animation: ![Working toy](../story/assets/animations/star-projector-working.webp)

  ---

  Turning the disc brings new holes past the fixed aperture. Sliding the lens brings their projected image into focus. The optical model uses one ideal thin lens; brightness and real component tolerances are not measured.

**Combinations**
- `pj-lens` [consume] + `pj-holder` [transform] -> `pj-focus`
- `pj-lid` [consume] + `pj-wheel-box` [transform] -> `pj-closed`
- `pj-closed` [transform] @ `pj-flip` -> `pj-front-closed`
- `pj-focus` [consume] + `pj-front-closed` [transform] -> `pj-focused`
- `pj-hood` [consume] + `pj-focused` [transform] -> `pj-hooded`
- `pj-handle` [consume] + `pj-hooded` [transform] -> `star-projector`

## `c-window-foot` A broad foot
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Window base](../story/assets/items/wn-foot-ready.webp)

**Goals**
- Fit a foot -- `wn-one-foot`
- next: Fit the other foot -- `wn-two-feet`
- next: Fit the battery
  - either: `wn-fitted-1`
  - or: `wn-fitted-3`
  - or: `wn-fitted-5`
  - or: `wn-fitted-7`
  - or: `wn-fitted-9`
  - or: `wn-fitted-11`
  - or: `wn-fitted-13`
  - or: `wn-foot-ready`
- next: Fit the switch
  - either: `wn-fitted-2`
  - or: `wn-fitted-3`
  - or: `wn-fitted-6`
  - or: `wn-fitted-7`
  - or: `wn-fitted-10`
  - or: `wn-fitted-11`
  - or: `wn-fitted-14`
  - or: `wn-foot-ready`
- next: Fit the block
  - either: `wn-fitted-4`
  - or: `wn-fitted-5`
  - or: `wn-fitted-6`
  - or: `wn-fitted-7`
  - or: `wn-fitted-12`
  - or: `wn-fitted-13`
  - or: `wn-fitted-14`
  - or: `wn-foot-ready`
- next: Fit the sill -- `wn-foot-ready`

**Items**
- `wn-base` Base
  - icon: ![Base](../story/assets/items/wn-base.webp)
- `wn-foot-1` Foot
  - icon: ![Foot](../story/assets/items/wn-foot-1.webp)
- `wn-foot-2` Foot
  - icon: ![Foot](../story/assets/items/wn-foot-2.webp)
- `wn-battery` Battery
  - icon: ![Battery](../story/assets/items/wn-battery.webp)
- `wn-switch` Switch
  - icon: ![Switch](../story/assets/items/wn-switch.webp)
- `wn-block` Block
  - icon: ![Block](../story/assets/items/wn-block.webp)
- `wn-sill` Sill
  - icon: ![Sill](../story/assets/items/wn-sill.webp)
- `wn-one-foot` Base
  - icon: ![Base](../story/assets/items/wn-one-foot.webp)
- `wn-two-feet` Base
  - icon: ![Base](../story/assets/items/wn-two-feet.webp)
- `wn-fitted-1` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-1.webp)
- `wn-fitted-2` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-2.webp)
- `wn-fitted-3` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-3.webp)
- `wn-fitted-4` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-4.webp)
- `wn-fitted-5` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-5.webp)
- `wn-fitted-6` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-6.webp)
- `wn-fitted-7` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-7.webp)
- `wn-fitted-8` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-8.webp)
- `wn-fitted-9` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-9.webp)
- `wn-fitted-10` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-10.webp)
- `wn-fitted-11` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-11.webp)
- `wn-fitted-12` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-12.webp)
- `wn-fitted-13` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-13.webp)
- `wn-fitted-14` Window base
  - icon: ![Window base](../story/assets/items/wn-fitted-14.webp)
- `wn-foot-ready` Window base
  - icon: ![Window base](../story/assets/items/wn-foot-ready.webp)

**Combinations**
- `wn-foot-1` [consume] + `wn-base` [transform] -> `wn-one-foot`
- `wn-foot-1` [consume] + `wn-one-foot` [transform] -> `wn-two-feet`
- `wn-foot-2` [consume] + `wn-base` [transform] -> `wn-one-foot`
- `wn-foot-2` [consume] + `wn-one-foot` [transform] -> `wn-two-feet`
- `wn-battery` [consume] + `wn-two-feet` [transform] -> `wn-fitted-1`
- `wn-switch` [consume] + `wn-two-feet` [transform] -> `wn-fitted-2`
- `wn-block` [consume] + `wn-two-feet` [transform] -> `wn-fitted-4`
- `wn-sill` [consume] + `wn-two-feet` [transform] -> `wn-fitted-8`
- `wn-switch` [consume] + `wn-fitted-1` [transform] -> `wn-fitted-3`
- `wn-block` [consume] + `wn-fitted-1` [transform] -> `wn-fitted-5`
- `wn-sill` [consume] + `wn-fitted-1` [transform] -> `wn-fitted-9`
- `wn-battery` [consume] + `wn-fitted-2` [transform] -> `wn-fitted-3`
- `wn-block` [consume] + `wn-fitted-2` [transform] -> `wn-fitted-6`
- `wn-sill` [consume] + `wn-fitted-2` [transform] -> `wn-fitted-10`
- `wn-block` [consume] + `wn-fitted-3` [transform] -> `wn-fitted-7`
- `wn-sill` [consume] + `wn-fitted-3` [transform] -> `wn-fitted-11`
- `wn-battery` [consume] + `wn-fitted-4` [transform] -> `wn-fitted-5`
- `wn-switch` [consume] + `wn-fitted-4` [transform] -> `wn-fitted-6`
- `wn-sill` [consume] + `wn-fitted-4` [transform] -> `wn-fitted-12`
- `wn-switch` [consume] + `wn-fitted-5` [transform] -> `wn-fitted-7`
- `wn-sill` [consume] + `wn-fitted-5` [transform] -> `wn-fitted-13`
- `wn-battery` [consume] + `wn-fitted-6` [transform] -> `wn-fitted-7`
- `wn-sill` [consume] + `wn-fitted-6` [transform] -> `wn-fitted-14`
- `wn-sill` [consume] + `wn-fitted-7` [transform] -> `wn-foot-ready`
- `wn-battery` [consume] + `wn-fitted-8` [transform] -> `wn-fitted-9`
- `wn-switch` [consume] + `wn-fitted-8` [transform] -> `wn-fitted-10`
- `wn-block` [consume] + `wn-fitted-8` [transform] -> `wn-fitted-12`
- `wn-switch` [consume] + `wn-fitted-9` [transform] -> `wn-fitted-11`
- `wn-block` [consume] + `wn-fitted-9` [transform] -> `wn-fitted-13`
- `wn-battery` [consume] + `wn-fitted-10` [transform] -> `wn-fitted-11`
- `wn-block` [consume] + `wn-fitted-10` [transform] -> `wn-fitted-14`
- `wn-block` [consume] + `wn-fitted-11` [transform] -> `wn-foot-ready`
- `wn-battery` [consume] + `wn-fitted-12` [transform] -> `wn-fitted-13`
- `wn-switch` [consume] + `wn-fitted-12` [transform] -> `wn-fitted-14`
- `wn-switch` [consume] + `wn-fitted-13` [transform] -> `wn-foot-ready`
- `wn-battery` [consume] + `wn-fitted-14` [transform] -> `wn-foot-ready`


## `c-window-frame` An open frame
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Window](../story/assets/items/open-window.webp)

**Goals**
- Fit an upright -- `wn-one-upright`
- next: Fit the other upright -- `wn-uprights`
- next: Join them with the crossbar -- `wn-frame`
- next: Flip the window -- `wn-back`
- next: Fit a strut -- `wn-one-strut`
- next: Fit the other strut -- `wn-braced-back`
- next: Flip the window -- `wn-braced`
- next: Connect the lead -- `open-window`

**Hotspots**
- `wn-flip` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `wn-upright-1` Upright
  - icon: ![Upright](../story/assets/items/wn-upright-1.webp)
- `wn-upright-2` Upright
  - icon: ![Upright](../story/assets/items/wn-upright-2.webp)
- `wn-top` Crossbar
  - icon: ![Crossbar](../story/assets/items/wn-top.webp)
- `wn-strut-1` Strut
  - icon: ![Strut](../story/assets/items/wn-strut-1.webp)
- `wn-strut-2` Strut
  - icon: ![Strut](../story/assets/items/wn-strut-2.webp)
- `wn-lead` Lead
  - icon: ![Lead](../story/assets/items/wn-lead.webp)
- `wn-one-upright` Window
  - icon: ![Window](../story/assets/items/wn-one-upright.webp)
- `wn-uprights` Window
  - icon: ![Window](../story/assets/items/wn-uprights.webp)
- `wn-frame` Window
  - icon: ![Window](../story/assets/items/wn-frame.webp)
- `wn-back` Window
  - icon: ![Window](../story/assets/items/wn-back.webp)
- `wn-one-strut` Window
  - icon: ![Window](../story/assets/items/wn-one-strut.webp)
- `wn-braced-back` Window
  - icon: ![Window](../story/assets/items/wn-braced-back.webp)
- `wn-braced` Window
  - icon: ![Window](../story/assets/items/wn-braced.webp)
- `open-window` Window
  - icon: ![Window](../story/assets/items/open-window.webp)
  - animation: ![Working toy](../story/assets/animations/open-window-working.webp)
- `wn-flip` Flip

**Combinations**
- `wn-upright-1` [consume] + `wn-foot-ready` [transform] -> `wn-one-upright`
- `wn-upright-1` [consume] + `wn-one-upright` [transform] -> `wn-uprights`
- `wn-upright-2` [consume] + `wn-foot-ready` [transform] -> `wn-one-upright`
- `wn-upright-2` [consume] + `wn-one-upright` [transform] -> `wn-uprights`
- `wn-top` [consume] + `wn-uprights` [transform] -> `wn-frame`
- `wn-frame` [transform] @ `wn-flip` -> `wn-back`
- `wn-strut-1` [consume] + `wn-back` [transform] -> `wn-one-strut`
- `wn-strut-1` [consume] + `wn-one-strut` [transform] -> `wn-braced-back`
- `wn-strut-2` [consume] + `wn-back` [transform] -> `wn-one-strut`
- `wn-strut-2` [consume] + `wn-one-strut` [transform] -> `wn-braced-back`
- `wn-braced-back` [transform] @ `wn-flip` -> `wn-braced`
- `wn-lead` [consume] + `wn-braced` [transform] -> `open-window`

## `c-spinner-drive` Two pulleys
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Drive](../story/assets/items/sp-drive-ready.webp)

**Goals**
- Mount the motor
  - either: `sp-drive-1`
  - or: `sp-drive-3`
  - or: `sp-drive-11`
  - or: `sp-drive-5`
  - or: `sp-drive-7`
  - or: `sp-drive`
- next: Mount the spindle
  - either: `sp-drive-2`
  - or: `sp-drive-10`
  - or: `sp-drive-3`
  - or: `sp-drive-11`
  - or: `sp-drive-7`
  - or: `sp-drive`
- next: Fit the small pulley
  - either: `sp-motor-unit`
  - or: `sp-drive-5`
  - or: `sp-drive-7`
  - or: `sp-drive`
- next: Fit the large pulley -- `sp-drive`
- next: Loop the belt around both pulleys -- `sp-belted`
- next: Fit the guard -- `sp-guarded`
- next: Fit the wheel -- `sp-wheeled`
- next: Fit the collar -- `sp-drive-ready`

**Items**
- `sp-base` Base
  - icon: ![Base](../story/assets/items/sp-base.webp)
- `sp-motor` Motor
  - icon: ![Motor](../story/assets/items/sp-motor.webp)
- `sp-bearing` Spindle
  - icon: ![Spindle](../story/assets/items/sp-bearing.webp)
- `sp-motor-pulley` Small pulley
  - icon: ![Small pulley](../story/assets/items/sp-motor-pulley.webp)
- `sp-driven-pulley` Large pulley
  - icon: ![Large pulley](../story/assets/items/sp-driven-pulley.webp)
- `sp-belt` Belt
  - icon: ![Belt](../story/assets/items/sp-belt.webp)
- `sp-guard` Guard
  - icon: ![Guard](../story/assets/items/sp-guard.webp)
- `sp-wheel` Wheel
  - icon: ![Wheel](../story/assets/items/sp-wheel.webp)
- `sp-collar` Collar
  - icon: ![Collar](../story/assets/items/sp-collar.webp)
- `sp-motor-unit` Motor
  - icon: ![Motor](../story/assets/items/sp-motor-unit.webp)
- `sp-bearing-unit` Spindle
  - icon: ![Spindle](../story/assets/items/sp-bearing-unit.webp)
- `sp-drive-2` Base
  - icon: ![Base](../story/assets/items/sp-drive-2.webp)
- `sp-drive-10` Base
  - icon: ![Base](../story/assets/items/sp-drive-10.webp)
- `sp-drive-1` Base
  - icon: ![Base](../story/assets/items/sp-drive-1.webp)
- `sp-drive-3` Base
  - icon: ![Base](../story/assets/items/sp-drive-3.webp)
- `sp-drive-11` Base
  - icon: ![Base](../story/assets/items/sp-drive-11.webp)
- `sp-drive-5` Base
  - icon: ![Base](../story/assets/items/sp-drive-5.webp)
- `sp-drive-7` Base
  - icon: ![Base](../story/assets/items/sp-drive-7.webp)
- `sp-drive` Base
  - icon: ![Base](../story/assets/items/sp-drive.webp)
- `sp-belted` Drive
  - icon: ![Drive](../story/assets/items/sp-belted.webp)
- `sp-guarded` Drive
  - icon: ![Drive](../story/assets/items/sp-guarded.webp)
- `sp-wheeled` Drive
  - icon: ![Drive](../story/assets/items/sp-wheeled.webp)
- `sp-drive-ready` Drive
  - icon: ![Drive](../story/assets/items/sp-drive-ready.webp)

**Combinations**
- `sp-motor-pulley` [consume] + `sp-motor` [transform] -> `sp-motor-unit`
- `sp-driven-pulley` [consume] + `sp-bearing` [transform] -> `sp-bearing-unit`
- `sp-motor` [consume] + `sp-base` [transform] -> `sp-drive-1`
- `sp-bearing` [consume] + `sp-base` [transform] -> `sp-drive-2`
- `sp-motor-unit` [consume] + `sp-base` [transform] -> `sp-drive-5`
- `sp-bearing-unit` [consume] + `sp-base` [transform] -> `sp-drive-10`
- `sp-motor` [consume] + `sp-drive-2` [transform] -> `sp-drive-3`
- `sp-driven-pulley` [consume] + `sp-drive-2` [transform] -> `sp-drive-10`
- `sp-motor-unit` [consume] + `sp-drive-2` [transform] -> `sp-drive-7`
- `sp-motor` [consume] + `sp-drive-10` [transform] -> `sp-drive-11`
- `sp-motor-unit` [consume] + `sp-drive-10` [transform] -> `sp-drive`
- `sp-bearing` [consume] + `sp-drive-1` [transform] -> `sp-drive-3`
- `sp-motor-pulley` [consume] + `sp-drive-1` [transform] -> `sp-drive-5`
- `sp-bearing-unit` [consume] + `sp-drive-1` [transform] -> `sp-drive-11`
- `sp-motor-pulley` [consume] + `sp-drive-3` [transform] -> `sp-drive-7`
- `sp-driven-pulley` [consume] + `sp-drive-3` [transform] -> `sp-drive-11`
- `sp-motor-pulley` [consume] + `sp-drive-11` [transform] -> `sp-drive`
- `sp-bearing` [consume] + `sp-drive-5` [transform] -> `sp-drive-7`
- `sp-bearing-unit` [consume] + `sp-drive-5` [transform] -> `sp-drive`
- `sp-driven-pulley` [consume] + `sp-drive-7` [transform] -> `sp-drive`
- `sp-belt` [consume] + `sp-drive` [transform] -> `sp-belted`
- `sp-guard` [consume] + `sp-belted` [transform] -> `sp-guarded`
- `sp-wheel` [consume] + `sp-guarded` [transform] -> `sp-wheeled`
- `sp-collar` [consume] + `sp-wheeled` [transform] -> `sp-drive-ready`


## `c-spinner-ribbon` A loop of string
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Ribbon spinner](../story/assets/items/ribbon-spinner.webp)

**Goals**
- Fit the battery
  - either: `sp-fitted-1`
  - or: `sp-fitted-3`
  - or: `sp-fitted-5`
  - or: `sp-fitted-7`
- next: Fit the switch
  - either: `sp-fitted-2`
  - or: `sp-fitted-3`
  - or: `sp-fitted-6`
  - or: `sp-fitted-7`
- next: Fit the fork
  - either: `sp-fitted-4`
  - or: `sp-fitted-5`
  - or: `sp-fitted-6`
  - or: `sp-fitted-7`
- next: Join the ends of the string -- `sp-string-loop`
- next: Thread the loop over the wheel -- `sp-threaded`
- next: Fold the ribbon -- `sp-folded-ribbon`
- next: Fit the clip -- `sp-clipped-ribbon`
- next: Clip the ribbon to the fork -- `ribbon-spinner`

**Hotspots**
- `sp-fold` (center 390px, 216px)
  - icon: ![Fold](../story/assets/actions/fold.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `sp-battery` Battery
  - icon: ![Battery](../story/assets/items/sp-battery.webp)
- `sp-switch` Switch
  - icon: ![Switch](../story/assets/items/sp-switch.webp)
- `sp-fork` Fork
  - icon: ![Fork](../story/assets/items/sp-fork.webp)
- `sp-string` String
  - icon: ![String](../story/assets/items/sp-string.webp)
- `sp-joiner` Joiner
  - icon: ![Joiner](../story/assets/items/sp-joiner.webp)
- `sp-paper` Ribbon
  - icon: ![Ribbon](../story/assets/items/sp-paper.webp)
- `sp-clip` Clip
  - icon: ![Clip](../story/assets/items/sp-clip.webp)
- `sp-string-loop` Loop
  - icon: ![Loop](../story/assets/items/sp-string-loop.webp)
- `sp-folded-ribbon` Ribbon
  - icon: ![Ribbon](../story/assets/items/sp-folded-ribbon.webp)
- `sp-clipped-ribbon` Ribbon
  - icon: ![Ribbon](../story/assets/items/sp-clipped-ribbon.webp)
- `sp-fitted-1` Spinner
  - icon: ![Spinner](../story/assets/items/sp-fitted-1.webp)
- `sp-fitted-2` Spinner
  - icon: ![Spinner](../story/assets/items/sp-fitted-2.webp)
- `sp-fitted-3` Spinner
  - icon: ![Spinner](../story/assets/items/sp-fitted-3.webp)
- `sp-fitted-4` Spinner
  - icon: ![Spinner](../story/assets/items/sp-fitted-4.webp)
- `sp-fitted-5` Spinner
  - icon: ![Spinner](../story/assets/items/sp-fitted-5.webp)
- `sp-fitted-6` Spinner
  - icon: ![Spinner](../story/assets/items/sp-fitted-6.webp)
- `sp-fitted-7` Spinner
  - icon: ![Spinner](../story/assets/items/sp-fitted-7.webp)
- `sp-threaded` Spinner
  - icon: ![Spinner](../story/assets/items/sp-threaded.webp)
- `ribbon-spinner` Ribbon spinner
  - icon: ![Ribbon spinner](../story/assets/items/ribbon-spinner.webp)
  - animation: ![Working toy](../story/assets/animations/ribbon-spinner-working.webp)
- `sp-fold` Fold

**Combinations**
- `sp-joiner` [consume] + `sp-string` [transform] -> `sp-string-loop`
- `sp-paper` [transform] @ `sp-fold` -> `sp-folded-ribbon`
- `sp-clip` [consume] + `sp-folded-ribbon` [transform] -> `sp-clipped-ribbon`
- `sp-battery` [consume] + `sp-drive-ready` [transform] -> `sp-fitted-1`
- `sp-switch` [consume] + `sp-drive-ready` [transform] -> `sp-fitted-2`
- `sp-fork` [consume] + `sp-drive-ready` [transform] -> `sp-fitted-4`
- `sp-switch` [consume] + `sp-fitted-1` [transform] -> `sp-fitted-3`
- `sp-fork` [consume] + `sp-fitted-1` [transform] -> `sp-fitted-5`
- `sp-battery` [consume] + `sp-fitted-2` [transform] -> `sp-fitted-3`
- `sp-fork` [consume] + `sp-fitted-2` [transform] -> `sp-fitted-6`
- `sp-fork` [consume] + `sp-fitted-3` [transform] -> `sp-fitted-7`
- `sp-battery` [consume] + `sp-fitted-4` [transform] -> `sp-fitted-5`
- `sp-switch` [consume] + `sp-fitted-4` [transform] -> `sp-fitted-6`
- `sp-switch` [consume] + `sp-fitted-5` [transform] -> `sp-fitted-7`
- `sp-battery` [consume] + `sp-fitted-6` [transform] -> `sp-fitted-7`
- `sp-string-loop` [consume] + `sp-fitted-7` [transform] -> `sp-threaded`
- `sp-clipped-ribbon` [consume] + `sp-threaded` [transform] -> `ribbon-spinner`

## `c-lift-frame` A wide frame
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Frame](../story/assets/items/fc-lift-frame.webp)

**Goals**
- Fit an arch to the deck -- `fc-one-arch`
- next: Fit the second arch -- `fc-arches`
- next: Clip the cradle across the arches -- `fc-top`
- next: Seat the Tile -- `fc-tiled`
- next: Flip the frame over -- `fc-inverted`
- next: Fit the battery underneath -- `fc-powered`
- next: Flip the frame upright -- `fc-upright`
- next: Fit the Control -- `fc-lift-frame`

**Hotspots**
- `fc-flip-lift` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `fc-deck` Deck
  - icon: ![Deck](../story/assets/items/fc-deck.webp)

  ---

  A 400 × 300 mm prepared plywood deck. The mounting holes and wire passages are already cut.
- `fc-arch-a` Arch
  - icon: ![Arch](../story/assets/items/fc-arch-a.webp)

  ---

  One connected rigid arch with two feet and captive bolts.
- `fc-arch-b` Arch
  - icon: ![Arch](../story/assets/items/fc-arch-b.webp)

  ---

  A second identical connected arch. Either arch fits either side of the deck.
- `fc-cradle` Tile cradle
  - icon: ![Tile cradle](../story/assets/items/fc-cradle.webp)

  ---

  One connected top cradle. Four integral saddles clip over the arches; its padded rails receive the tile.
- `fc-tile` Tile
  - icon: ![Tile](../story/assets/items/fc-tile.webp)

  ---

  A flat pink tile with a keyed power socket and retaining holes.
- `fc-battery` Battery pack
  - icon: ![Battery pack](../story/assets/items/fc-battery.webp)

  ---

  A compatible enclosed battery in its integral retained bracket. It mounts below the deck, keeping weight low.
- `fc-control` Control
  - icon: ![Control](../story/assets/items/fc-control.webp)

  ---

  A prepared controller and latching stop button in one pod with a connected fused harness. Keep power off while fitting it.
- `fc-one-arch` Frame
  - icon: ![Frame](../story/assets/items/fc-one-arch.webp)
- `fc-arches` Frame
  - icon: ![Frame](../story/assets/items/fc-arches.webp)
- `fc-top` Frame
  - icon: ![Frame](../story/assets/items/fc-top.webp)
- `fc-tiled` Frame
  - icon: ![Frame](../story/assets/items/fc-tiled.webp)
- `fc-inverted` Frame
  - icon: ![Frame](../story/assets/items/fc-inverted.webp)
- `fc-powered` Frame
  - icon: ![Frame](../story/assets/items/fc-powered.webp)
- `fc-upright` Frame
  - icon: ![Frame](../story/assets/items/fc-upright.webp)
- `fc-lift-frame` Frame
  - icon: ![Frame](../story/assets/items/fc-lift-frame.webp)
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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Frame](../story/assets/items/fc-powered-show.webp)

**Goals**
- Fit the projector dock -- `fc-docked`
- next: Press your projector onto the dock -- `fc-projector-aboard`
- next: Fit the small pulley to the motor -- `fc-drive`
- next: Mount the drive motor -- `fc-motor-mounted`
- next: Loop the belt around both pulleys -- `fc-belted`
- next: Flip to the underside -- `fc-drive-under`
- next: Fit the Battery pack -- `fc-supply-under`
- next: Flip the Frame upright -- `fc-powered-show`

**Hotspots**
- `fc-flip-drive` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `star-projector` Star projector
  - from chapter `c-lift-projector` icon: ![Star projector](../story/assets/items/fc-projector-carried.webp)
  - from chapter `c-lift-projector` animation: none
- `fc-dock` Projector dock
  - icon: ![Projector dock](../story/assets/items/fc-dock.webp)

  ---

  One connected projector dock. Four feet bear on the deck and two recessed captive screws fasten it down. Four split snap studs pass through the original mounting holes; their flexible heads spring out above the box collars to retain the unchanged projector.
- `fc-motor` Gearmotor
  - icon: ![Gearmotor](../story/assets/items/fc-motor.webp)

  ---

  An enclosed slow gearmotor with its integral pedestal and lead. The shaft is parallel to the projector spindle.
- `fc-pulley` Small pulley
  - icon: ![Small pulley](../story/assets/items/fc-pulley.webp)

  ---

  One small pulley with a captive screw that clamps onto the motor shaft flat.
- `fc-belt` Belt
  - icon: ![Belt](../story/assets/items/fc-belt.webp)

  ---

  One continuous soft belt. Its small pulley drives the larger grooved handwheel more slowly.
- `fc-motor-pack` Battery pack
  - icon: ![Battery pack](../story/assets/items/fc-motor-pack.webp)

  ---

  An enclosed low-voltage motor supply with its own switch, lead and integral mounting bracket. The lamp keeps its original supply; the lift has a separate circuit.
- `fc-docked` Frame
  - icon: ![Frame](../story/assets/items/fc-docked.webp)
- `fc-projector-aboard` Frame
  - icon: ![Frame](../story/assets/items/fc-projector-aboard.webp)
- `fc-drive` Drive motor
  - icon: ![Drive motor](../story/assets/items/fc-drive.webp)
- `fc-motor-mounted` Frame
  - icon: ![Frame](../story/assets/items/fc-motor-mounted.webp)
- `fc-belted` Frame
  - icon: ![Frame](../story/assets/items/fc-belted.webp)
- `fc-drive-under` Frame
  - icon: ![Frame](../story/assets/items/fc-drive-under.webp)
- `fc-supply-under` Frame
  - icon: ![Frame](../story/assets/items/fc-supply-under.webp)
- `fc-powered-show` Frame
  - icon: ![Frame](../story/assets/items/fc-powered-show.webp)
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
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Whale](../story/assets/items/fc-whale.webp)

**Goals**
- Fit the Tail -- `fc-tailed`
- next: Fit the Front side -- `fc-near-side`
- next: Turn to the back -- `fc-side-rear`
- next: Fit the Back side -- `fc-sided`
- next: Fit the Back fin -- `fc-one-fin-b`
- next: Turn to the front -- `fc-fin-front`
- next: Fit the Front fin -- `fc-whale`

**Hotspots**
- `fc-flip-shell` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `fc-tail` Tail
  - icon: ![Tail](../story/assets/items/fc-tail.webp)

  ---

  One continuous fixed tail with its prepared root fitting. It does not steer or provide lift.
- `fc-side-a` Front side
  - icon: ![Front side](../story/assets/items/fc-side-a.webp)

  ---

  One cut whale side panel with its mounting tabs. Its top edge stays below the projector beam.
- `fc-side-b` Back side
  - icon: ![Back side](../story/assets/items/fc-side-b.webp)

  ---

  A second whale side panel, fitted separately.
- `fc-fin-a` Front fin
  - icon: ![Front fin](../story/assets/items/fc-fin-a.webp)

  ---

  One fixed fin with two integral mushroom studs and a captive centre screw. The keyhole entries sit below the deck. With the screw retracted, pass the heads through the wide openings and lower the fin into the narrow slots. Tighten the screw to retain it during flips. It gives the whale its shape, not lift.
- `fc-fin-b` Back fin
  - icon: ![Back fin](../story/assets/items/fc-fin-b.webp)

  ---

  The other fixed fin.
- `fc-tailed` Whale
  - icon: ![Whale](../story/assets/items/fc-tailed.webp)
- `fc-near-side` Whale
  - icon: ![Whale](../story/assets/items/fc-near-side.webp)
- `fc-side-rear` Whale
  - icon: ![Whale](../story/assets/items/fc-side-rear.webp)
- `fc-sided` Whale
  - icon: ![Whale](../story/assets/items/fc-sided.webp)
- `fc-one-fin-b` Whale
  - icon: ![Whale](../story/assets/items/fc-one-fin-b.webp)
- `fc-fin-front` Whale
  - icon: ![Whale](../story/assets/items/fc-fin-front.webp)
- `fc-whale` Whale
  - icon: ![Whale](../story/assets/items/fc-whale.webp)
- `fc-flip-shell` Flip

**Combinations**
- `fc-tail` [consume] + `fc-powered-show` [transform] -> `fc-tailed`
- `fc-side-a` [consume] + `fc-tailed` [transform] -> `fc-near-side`
- `fc-near-side` [transform] @ `fc-flip-shell` -> `fc-side-rear`
- `fc-side-b` [consume] + `fc-side-rear` [transform] -> `fc-sided`
- `fc-fin-b` [consume] + `fc-sided` [transform] -> `fc-one-fin-b`
- `fc-one-fin-b` [transform] @ `fc-flip-shell` -> `fc-fin-front`
- `fc-fin-a` [consume] + `fc-fin-front` [transform] -> `fc-whale`


## `c-whale-finish` Landing feet
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Whale](../story/assets/items/fc-guarded.webp)

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
- next: Fit the clear drive guard -- `fc-guarded`

**Hotspots**
- `fc-flip-feet` (center 390px, 216px)
  - icon: ![Flip](../story/assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `fc-skid-a` Landing skid
  - icon: ![Landing skid](../story/assets/items/fc-skid-a.webp)

  ---

  One connected landing skid with two upright legs and captive deck bolts.
- `fc-skid-b` Landing skid
  - icon: ![Landing skid](../story/assets/items/fc-skid-b.webp)

  ---

  A second landing skid. Their feet reach below the batteries and trim weight.
- `fc-rail` Weight rail
  - icon: ![Weight rail](../story/assets/items/fc-rail.webp)

  ---

  One slotted rail with integral mounting ears, closed travel ends and a wide keyhole entry near the right end. The weight shoe enters through that opening from below.
- `fc-weight` Counterweight
  - icon: ![Counterweight](../story/assets/items/fc-weight.webp)

  ---

  A single sliding weight with a captive shoe, vertical clamp screw and washer. Raise the shoe through the wide rail entry, slide into the narrow track, then tighten the screw to clamp the rail between shoe and pad.
- `fc-guard` Guard
  - icon: ![Guard](../story/assets/items/fc-guard.webp)

  ---

  One hollow clear hood, open underneath and at the rear. Lower it over the drive, then tighten the captive screws on its exposed side feet. It encloses the belt and hand grip without covering the lens.
- `fc-whale-under` Whale
  - icon: ![Whale](../story/assets/items/fc-whale-under.webp)
- `fc-one-skid-a` Whale
  - icon: ![Whale](../story/assets/items/fc-one-skid-a.webp)
- `fc-one-skid-b` Whale
  - icon: ![Whale](../story/assets/items/fc-one-skid-b.webp)
- `fc-skids` Whale
  - icon: ![Whale](../story/assets/items/fc-skids.webp)
- `fc-railed` Whale
  - icon: ![Whale](../story/assets/items/fc-railed.webp)
- `fc-weighted` Whale
  - icon: ![Whale](../story/assets/items/fc-weighted.webp)
- `fc-standing` Whale
  - icon: ![Whale](../story/assets/items/fc-standing.webp)
- `fc-guarded` Whale
  - icon: ![Whale](../story/assets/items/fc-guarded.webp)

  ---

  The real projector, motor, belt, batteries, arches and counterweight retain their ordinary jobs. The exposed rail lets the weight move opposite a heavier end while the machine is supported and disconnected.
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
- `fc-guard` [consume] + `fc-standing` [transform] -> `fc-guarded`


## `c-whale-cargo` One more thing
background: ![White instruction page](../story/assets/backgrounds/white.svg)
reference: ![Whale](../story/assets/items/flying-whale.webp)

**Goals**
- Fit the Clip onto the arch -- `fc-clipped`
- next: Slide the Pinwheel into the Clip -- `flying-whale`

**Items**
- `fc-guarded` Whale
  - from chapter `c-whale-cargo` icon: ![Whale](../story/assets/items/fc-cargo-ready.webp)
- `pinwheel` Pinwheel
  - from chapter `c-whale-cargo` icon: ![Pinwheel](../story/assets/items/fc-pinwheel-carried.webp)
  - from chapter `c-whale-cargo` animation: none
- `fc-cargo` Clip
  - icon: ![Clip](../story/assets/items/fc-cargo.webp)

  ---

  A connected socket and open saddle. The saddle clips over the arch; its deep socket receives the wooden pinwheel handle. A captive screw grips the handle.
- `fc-clipped` Whale
  - icon: ![Whale](../story/assets/items/fc-clipped.webp)
- `flying-whale` Whale
  - icon: ![Whale](../story/assets/items/flying-whale.webp)
  - animation: ![Working toy](../story/assets/animations/flying-whale-working.webp)

**Combinations**
- `fc-cargo` [consume] + `fc-guarded` [transform] -> `fc-clipped`
- `pinwheel` [consume] + `fc-clipped` [transform] -> `flying-whale`

## `c-end` The End
background: ![Two makers and an exchanged paper star](../story/assets/backgrounds/ending.webp)
background animation: ![A pinwheel goes across; a paper star comes home](../story/assets/backgrounds/ending-working.webp)
