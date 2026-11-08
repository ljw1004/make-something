# ![An orange paper pinwheel](icon.png) A Fair in the Air
background: ![An invitation on the garden workbench](assets/cover.webp)

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
- `pw-fold` (center 130px, 216px)
  - icon: ![Dotted paper folding diagram](assets/actions/fold.svg)
- `pw-flip` (center 390px, 216px)
  - icon: ![Outline diagram of turning a sheet over](assets/actions/flip.svg)

**Items**
- `pw-fold` Fold
- `pw-flip` Flip
- `pw-paper` Paper
  - icon: ![Prepared paper square](assets/items/pw-paper.webp) (center 358px, 830px)

  ---

  The orange sheet is already cut along four diagonals, stopping short of the centre. Curl the four pierced corners inward; keep the uncut centre whole.
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
  - from chapter `c02` icon: ![Pinwheel](assets/items/pinwheel-carried.webp)

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


## `c02` The race to the watering can
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Wind racer](assets/items/wind-racer.webp)

The pinwheel is very good at going round and very bad at going anywhere. Jo lays a little chassis in the bench clips; beyond the door, a chalk lane ends at the watering can.

**Goals**
- Fit a bearing tube to the chassis
  - either: `wr-front-bearing-chassis`
  - or: `wr-rear-bearing-chassis`
- next: Fit the other bearing tube to the chassis -- `wr-bearing-chassis`
- next: Add the wheels to the chassis -- `wr-rolling-chassis`
- next: Clip the sail onto the mast -- `wr-sail`
- next: Fit the sail to the chassis -- `wr-rigged`
- next: Aim the sail with the pinwheel -- `wr-aimed`
- next: Race from the starting gate -- `wind-racer`

**Hotspots**
- `wr-chassis` (center 390px, 500px)
  - icon: ![Light wooden chassis](assets/hotspots/c02--wr-chassis.webp)
- `wr-front-bearing-chassis` (center 390px, 500px)
  - icon: ![Chassis with one bearing tube](assets/hotspots/c02--wr-front-bearing-chassis.webp)
- `wr-rear-bearing-chassis` (center 390px, 500px)
  - icon: ![Chassis with one bearing tube](assets/hotspots/c02--wr-rear-bearing-chassis.webp)
- `wr-bearing-chassis` (center 390px, 500px)
  - icon: ![Chassis with axle bearings](assets/hotspots/c02--wr-bearing-chassis.webp)
- `wr-rolling-chassis` (center 390px, 500px)
  - icon: ![Wheeled chassis](assets/hotspots/c02--wr-rolling-chassis.webp)
- `wr-rigged` (center 390px, 500px)
  - icon: ![Racer in the bench clips](assets/hotspots/c02--wr-rigged.webp)
- `wr-aimed` (center 390px, 500px)
  - icon: ![Racer facing the breeze](assets/hotspots/c02--wr-aimed.webp)

**Items**
- `wr-chassis` Chassis
  - icon: ![Light wooden chassis](assets/items/wr-chassis.webp)

  A prepared board with slots for two axle bearings, a mast socket and the same small mounting holes as the pinwheel handle. It is held in the reusable bench clips.
- `wr-front-bearing` Bearing tube
  - icon: ![Bearing tube](assets/items/wr-bearings.webp)

  ---

  A smooth tube with its connected mounting saddles. The wheel axle turns inside it.
- `wr-rear-bearing` Bearing tube
  - icon: ![Bearing tube](assets/items/wr-bearings.webp)

  ---

  A second matching bearing tube, with its connected mounting saddles.
- `wr-wheelset` Wheels
  - icon: ![Wheels and captive axles](assets/items/wr-wheelset.webp)

  One complete wheel-and-axle unit represents the supplied pair. Two straight axles with four light wheels, spacing collars and soft push-on caps. Each wheel is fixed to its axle; the collars leave a little clearance beside the bearing tubes so both axles turn freely.
- `wr-sailcloth` Sail
  - icon: ![Light sailcloth](assets/items/wr-sailcloth.webp)

  A small triangular sail with reinforced corner loops.
- `wr-mast` Mast
  - icon: ![Mast and crossbar](assets/items/wr-mast.webp)

  A short mast with a crossbar, clips for the sail loops and a split foot that fits the chassis socket.
- `wr-starting-gate` Starting gate
  - icon: ![Portable starting gate](assets/items/wr-starting-gate.webp)

  A light arch with a hand-lifted bar. Put it across the chalk lane to hold the racer still until its sail is facing the wind.
- `wr-front-bearing-chassis` Chassis
  - icon: ![Chassis with one bearing tube](assets/hotspots/c02--wr-front-bearing-chassis.webp)
- `wr-rear-bearing-chassis` Chassis
  - icon: ![Chassis with one bearing tube](assets/hotspots/c02--wr-rear-bearing-chassis.webp)
- `wr-bearing-chassis` Chassis
  - icon: ![Chassis with axle bearings](assets/items/wr-bearing-chassis.webp)
- `wr-rolling-chassis` Chassis
  - icon: ![Wheeled chassis](assets/items/wr-rolling-chassis.webp)
- `wr-sail` Sail
  - icon: ![Sail on its mast](assets/items/wr-sail.webp)

  You clip the sail to the crossbar and mast. The broad surface catches moving air; the wheels will let that push move the whole toy.
- `wr-rigged` Racer
  - icon: ![Racer in the bench clips](assets/items/wr-rigged.webp)
- `wr-aimed` Racer
  - icon: ![Racer facing the breeze](assets/items/wr-aimed.webp)

  You hold the pinwheel beside the sail and turn the racer until both catch the breeze from behind. The pinwheel stays in your hand; it has shown you where the air is going.
- `wind-racer` Wind racer
  - icon: ![Wind racer](assets/items/wind-racer.webp)

  ![Wind racer in the garden](assets/rewards/wind-racer.webp)

  You release the racer from its bench clips, lift it to the garden lane and set it behind the starting bar. Up goes the bar. The racer rolls all the way to the watering can.

  Jo crouches at the finish. “Again. I was definitely a very slow watering can.” Above the fence, your younger neighbour Kit’s fingers appear, then two curious eyes. “Can I try it at the fair?”

  “You can be the first driver,” you say. Kit promises to come back. You lift the racer from the lane for another run.

**Combinations**
- `wr-front-bearing` [consume] + `wr-chassis` [transform] -> `wr-front-bearing-chassis`
- `wr-rear-bearing` [consume] + `wr-chassis` [transform] -> `wr-rear-bearing-chassis`
- `wr-rear-bearing` [consume] + `wr-front-bearing-chassis` [transform] -> `wr-bearing-chassis`
- `wr-front-bearing` [consume] + `wr-rear-bearing-chassis` [transform] -> `wr-bearing-chassis`
- `wr-wheelset` [consume] + `wr-bearing-chassis` [transform] -> `wr-rolling-chassis`
- `wr-sailcloth` [consume] + `wr-mast` [transform] -> `wr-sail`
- `wr-sail` [consume] + `wr-rolling-chassis` [transform] -> `wr-rigged`
- `pinwheel` [preserve] + `wr-rigged` [transform] -> `wr-aimed`
- `wr-starting-gate` [preserve] + `wr-aimed` [transform] -> `wind-racer`


## `c03` A hill for a marble
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pinball table](assets/items/pinball-table.webp)

“Something for a windless day?” says Jo. The shallow tray on the bench could become a marble game—if the marble will come back instead of escaping beneath the shed.

**Goals**
- Fit the rails around the tray -- `pb-rail-frame`
- next: Fit the marble cup to the tray -- `pb-railed`
- next: Clip the tray support underneath the tray -- `pb-sloped`
- next: Fit the spring inside the plunger tube -- `pb-launcher`
- next: Attach the launcher to the tray -- `pb-launcher-table`
- next: Try a marble in the launch lane -- `pb-deadspot`
- next: Add the shim to free the trapped marble -- `pb-return-table`

**Hotspots**
- `pb-tray` (center 390px, 500px)
  - icon: ![Flat game tray](assets/hotspots/c03--pb-tray.webp)
- `pb-rail-frame` (center 390px, 500px)
  - icon: ![Tray with side and lane rails](assets/hotspots/c03--pb-rail-frame.webp)
- `pb-railed` (center 390px, 500px)
  - icon: ![Tray with retaining rails](assets/hotspots/c03--pb-railed.webp)
- `pb-sloped` (center 390px, 500px)
  - icon: ![Sloping game tray](assets/hotspots/c03--pb-sloped.webp)
- `pb-launcher-table` (center 390px, 500px)
  - icon: ![Table with a launch lane](assets/hotspots/c03--pb-launcher-table.webp)
- `pb-deadspot` (center 390px, 500px)
  - icon: ![Table with a corner trap](assets/hotspots/c03--pb-deadspot.webp)
- `pb-return-table` (center 390px, 500px)
  - icon: ![Marble-return table](assets/hotspots/c03--pb-return-table.webp)

**Items**
- `pb-tray` Tray
  - icon: ![Flat game tray](assets/items/pb-tray.webp)

  A light plywood tray with prepared rail slots, launcher holes, two flipper holes and carrying handles cut into its sides. Bench clips hold it while you build.
- `pb-rails` Rails
  - icon: ![Shaped retaining rails](assets/items/pb-rails.webp)

  Six shaped rails are supplied; one is shown: two side rails, a curved top rail, a launch-lane divider and two inward return lips, all with push-fit feet. The lips guide the marble toward the catch apron. A slight low spot behind the left return lip can trap a marble if the tray leans sideways.
- `pb-catch-cup` Marble cup
  - icon: ![Catch apron with marble cup](assets/items/pb-catch-cup.webp)

  One connected front apron with side rims, a marble cup and locating bridges. It fits the player’s end of the tray, where the rails return the marble.
- `pb-rail-frame` Tray
  - icon: ![Tray with side and lane rails](assets/items/pb-rail-frame.webp)
- `pb-wedge` Tray support
  - icon: ![Sloping tray support](assets/items/pb-wedge.webp)

  A broad U-shaped support with locating tongues and two spring clips that hook over the tray’s rear edge. Its side runners and rising far crosspiece hold a gentle slope toward the player; openings leave the carrying handles and finger buttons accessible.
- `pb-plunger-tube` Plunger tube
  - icon: ![Launcher tube and plunger](assets/items/pb-plunger-tube.webp)

  A launcher tube with a removable rear bearing cap and pull handle for fitting the spring, and a soft-tipped plunger retained in use. Its open end fits the table’s side lane. A clamp screw and captive sliding nut secure the adjustable travel stop within its marked limits; it begins at the gentle setting.
- `pb-spring` Spring
  - icon: ![Gentle launcher spring](assets/items/pb-spring.webp)

  A short, low-force spring that fits inside the tube around its captive plunger. The tube encloses it in use.
- `pb-marble` Marble
  - icon: ![Game marble](assets/items/pb-marble.webp)

  A large marble for the enclosed table. After each test it returns to the catch apron or to your hand.
- `pb-shim` Shim
  - icon: ![Thin levelling shim](assets/items/pb-shim.webp)

  A broad thin shim for the low corner under the table, with a clip to hold it in place.
- `pb-railed` Tray
  - icon: ![Tray with retaining rails](assets/items/pb-railed.webp)
- `pb-sloped` Tray
  - icon: ![Sloping game tray](assets/items/pb-sloped.webp)
- `pb-launcher` Launcher
  - icon: ![Enclosed marble launcher](assets/items/pb-launcher.webp)

  Pulling the handle squeezes the spring. Letting go makes it push the plunger forward. Its stop limits the push, and the spring stays inside the tube.
- `pb-launcher-table` Table
  - icon: ![Table with a launch lane](assets/items/pb-launcher-table.webp)
- `pb-deadspot` Table
  - icon: ![Table with a corner trap](assets/items/pb-deadspot.webp)

  The marble travels up the divided side lane and rolls back, but settles in the low pocket behind the left return lip. The tray leans sideways as well as downhill; the small dip is now lower than its way out.
- `pb-return-table` Table
  - icon: ![Marble-return table](assets/items/pb-return-table.webp)

  The shim lifts the low corner until the pocket slopes toward the apron. You roll the marble again: it passes the return lip and drops into the catch cup. Jo tries the launcher and gets the same result.

  “A good machine for giving you back your own marble,” she says. “Can we persuade it to do anything on the way?”

**Combinations**
- `pb-rails` [consume] + `pb-tray` [transform] -> `pb-rail-frame`
- `pb-catch-cup` [consume] + `pb-rail-frame` [transform] -> `pb-railed`
- `pb-wedge` [consume] + `pb-railed` [transform] -> `pb-sloped`
- `pb-spring` [consume] + `pb-plunger-tube` [transform] -> `pb-launcher`
- `pb-launcher` [consume] + `pb-sloped` [transform] -> `pb-launcher-table`
- `pb-marble` [preserve] + `pb-launcher-table` [transform] -> `pb-deadspot`
- `pb-shim` [consume] + `pb-deadspot` [transform] -> `pb-return-table`


## `c04` One more go
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pinball table](assets/items/pinball-table.webp)

You leave the marble table in its clips and bring over the flipper parts. Jo puts a chair at the player’s end. “Testing equipment,” she says, sitting down.

**Goals**
- Fit the flipper blades to the pivot plate -- `pb-flippers`
- next: Mount the flippers on the table -- `pb-flipper-table`
- next: Add the target arches to the table -- `pb-arched-table`
- next: Clip on the score wheel -- `pb-target-table`
- next: Launch the marble at the targets -- `pb-short-launch`
- next: Use the screwdriver to adjust the launcher stop -- `pb-tuned`
- next: Launch the marble again and play -- `pinball-table`

**Hotspots**
- `pb-return-table` (center 390px, 500px)
  - icon: ![Marble-return table](assets/hotspots/c04--pb-return-table.webp)
- `pb-flipper-table` (center 390px, 500px)
  - icon: ![Table with working flippers](assets/hotspots/c04--pb-flipper-table.webp)
- `pb-arched-table` (center 390px, 500px)
  - icon: ![Table with three target arches](assets/hotspots/c04--pb-arched-table.webp)
- `pb-target-table` (center 390px, 500px)
  - icon: ![Pinball table with three targets](assets/hotspots/c04--pb-target-table.webp)
- `pb-short-launch` (center 390px, 500px)
  - icon: ![Pinball table on its gentle setting](assets/hotspots/c04--pb-short-launch.webp)
- `pb-tuned` (center 390px, 500px)
  - icon: ![Pinball table with a longer launch](assets/hotspots/c04--pb-tuned.webp)

**Items**
- `work-screwdriver` Screwdriver
  - icon: ![Stubby screwdriver](assets/items/work-screwdriver.webp)

  Fits the captive screws on the workshop clamps and prepared toy fittings. It stays a tool.
- `pb-pivot-plate` Pivot plate
  - icon: ![Flipper pivot plate](assets/items/pb-pivot-plate.webp)

  An under-table plate with two captive pivot posts, finger buttons and soft return loops. The posts fit the prepared flipper holes.
- `pb-flipper-blades` Flipper blades
  - icon: ![Two flipper blades](assets/items/pb-flipper-blades.webp)

  One blade represents the mirrored pair. A left and right paddle, each with a socket for its pivot post. The short end connects to the finger button; the long end bats the marble.
- `pb-targets` Target arches
  - icon: ![Three target arches](assets/items/pb-targets.webp)

  Three matching arches are supplied; one is shown. Wide clip-in arches with different markings. A marble can roll through each arch without leaving the table.
- `pb-score-wheel` Score wheel
  - icon: ![Manual score wheel on its rail](assets/items/pb-score-wheel.webp)

  A numbered wheel already pivoted on a short edge rail. Clip the rail onto the table, then turn the wheel by hand after a successful shot.
- `pb-arched-table` Table
  - icon: ![Table with three target arches](assets/items/pb-arched-table.webp)
- `pb-flippers` Flippers
  - icon: ![Button-operated flippers](assets/items/pb-flippers.webp)

  Pressing a short button end swings a longer paddle across the table. The soft loop brings each paddle back when you let go.
- `pb-flipper-table` Table
  - icon: ![Table with working flippers](assets/items/pb-flipper-table.webp)
- `pb-target-table` Table
  - icon: ![Pinball table with three targets](assets/items/pb-target-table.webp)
- `pb-short-launch` Table
  - icon: ![Pinball table on its gentle setting](assets/items/pb-short-launch.webp)

  The gentle launch sends the marble back to your flippers for shots at the lower arches. You try for the top arch too. The launcher’s adjustable stop offers a longer launch for that shot.
- `pb-tuned` Table
  - icon: ![Pinball table with a longer launch](assets/items/pb-tuned.webp)

  You move the captive stop within its marked range. The spring can compress a little farther, while the plunger stays enclosed and its push remains gentle.

- `pinball-table` Pinball table
  - icon: ![Pinball table](assets/items/pinball-table.webp)

  ![Pinball table in the garden](assets/rewards/pinball-table.webp)

  The marble reaches the top arch, rolls back and takes a flipper shot through the middle. Jo gets the bottom arch on her turn. You have not made the marble stronger; you have given its push somewhere useful to go. You turn the score wheel one place for each arch. Jo tries to count the watering can as a bonus target. It is nowhere near the table.

  You put the marble in its catch cup, release the bench clips and lift the table by its built-in handles onto the garden trestle. Jo carries the chair. The first stall already has a queue of one.

**Combinations**
- `pb-flipper-blades` [consume] + `pb-pivot-plate` [transform] -> `pb-flippers`
- `pb-flippers` [consume] + `pb-return-table` [transform] -> `pb-flipper-table`
- `pb-targets` [consume] + `pb-flipper-table` [transform] -> `pb-arched-table`
- `pb-score-wheel` [consume] + `pb-arched-table` [transform] -> `pb-target-table`
- `pb-marble` [preserve] + `pb-target-table` [transform] -> `pb-short-launch`
- `work-screwdriver` [preserve] + `pb-short-launch` [transform] -> `pb-tuned`
- `pb-marble` [preserve] + `pb-tuned` [transform] -> `pinball-table`


## `c05` Round and up
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Crank dragon](assets/items/crank-dragon.webp)

A paper dragon would make a good fairground announcer. A dragon that waved would be better; first you need a machine that turns going round into going up and down.

**Goals**
- Fit the bearing frames to the base -- `cd-bearings`
- next: Slide the crankshaft through the bearing frames -- `cd-crank-frame`
- next: Fit the cam to the crankshaft -- `cd-cam-frame`
- next: Fit the follower into the guide and close its cover -- `cd-guided-follower`
- next: Mount the follower above the cam -- `cd-lifter`
- next: Add the spring to keep the follower on the cam
  - either: `cd-sprung-lifter`
  - or: `cd-working-lifter`
- next: Turn the crank handle and watch the follower rise and fall -- `cd-working-lifter`

**Hotspots**
- `cd-base` (center 390px, 500px)
  - icon: ![Dragon mechanism base](assets/hotspots/c05--cd-base.webp)
- `cd-bearings` (center 390px, 500px)
  - icon: ![Base with shaft bearings](assets/hotspots/c05--cd-bearings.webp)
- `cd-crank-frame` (center 390px, 500px)
  - icon: ![Frame with a turning crankshaft](assets/hotspots/c05--cd-crank-frame.webp)
- `cd-cam-frame` (center 390px, 500px)
  - icon: ![Crankshaft with an off-centre cam](assets/hotspots/c05--cd-cam-frame.webp)
- `cd-lifter` (center 390px, 500px)
  - icon: ![Cam beneath a guided follower](assets/hotspots/c05--cd-lifter.webp)
- `cd-lost-contact` (center 390px, 500px)
  - icon: ![Follower losing the cam](assets/hotspots/c05--cd-lost-contact.webp)
- `cd-sprung-lifter` (center 390px, 500px)
  - icon: ![Lifter with its spring fitted](assets/hotspots/c05--cd-sprung-lifter.webp)
- `cd-working-lifter` (center 390px, 500px)
  - icon: ![Reliable cam lifter](assets/hotspots/c05--cd-working-lifter.webp)

**Items**
- `cd-base` Base
  - icon: ![Dragon mechanism base](assets/items/cd-base.webp)

  A small wooden base held in the bench clips, with prepared holes for bearing frames, a guide and the dragon’s body, plus a parking clip for the removable crank handle. The later cam-change kit includes its own spare-cam clip.
- `cd-bearing-frames` Bearing frames
  - icon: ![Two bearing frames](assets/items/cd-bearing-frames.webp)

  Two matching frames are supplied; one is shown. Upright frames with smooth shaft holes and captive mounting screws. Both holes sit at the same height.
- `cd-shaft` Crankshaft
  - icon: ![Crankshaft](assets/items/cd-shaft.webp)

  A straight shaft with a flat-sided crank fitting, collars and a capped end. The collars keep it from sliding sideways in its bearings.
- `cd-cam` Cam
  - icon: ![Off-centre cam](assets/items/cd-cam.webp)

  A smooth round disc whose axle hole sits away from its centre. A split hub fixes it to the crankshaft.
- `cd-follower` Follower
  - icon: ![Follower rod](assets/items/cd-follower.webp)

  A light rod with a broad, smooth foot and a short crosshead with a prepared hole for two independently pivoting wing rods.
- `cd-guide` Guide
  - icon: ![Open follower guide and cover](assets/items/cd-guide.webp)

  A short guide with a mounting foot and removable snap-on front cover. Fit the follower through the open front, then snap the cover into the side-wall pockets before fixing the guide foot to the base. The square passage lets the rod slide up and down while keeping it over the cam. A keeper pin fits the follower’s service hole at maximum lift, supporting it while the shaft is removed; the pin normally parks in its clip on the base.
- `cd-return-spring` Spring
  - icon: ![Light follower spring](assets/items/cd-return-spring.webp)

  A soft tension spring with hooks for the guide bracket and follower collar. It pulls the follower foot gently toward the cam.
- `cd-crank-key` Crank handle
  - icon: ![Removable crank handle](assets/items/cd-crank-key.webp)

  A broad hand crank with a matching flat-sided socket and releasable retaining clip. It can be taken off the shaft and used again.
- `cd-bearings` Base
  - icon: ![Base with shaft bearings](assets/items/cd-bearings.webp)
- `cd-crank-frame` Frame
  - icon: ![Frame with a turning crankshaft](assets/items/cd-crank-frame.webp)
- `cd-cam-frame` Frame
  - icon: ![Crankshaft with an off-centre cam](assets/items/cd-cam-frame.webp)

  As the shaft turns, the far edge of the off-centre disc rises and falls. A centred disc would turn without making that change of height.
- `cd-guided-follower` Follower
  - icon: ![Follower in its guide](assets/items/cd-guided-follower.webp)
- `cd-lifter` Lifter
  - icon: ![Cam beneath a guided follower](assets/items/cd-lifter.webp)
- `cd-lost-contact` Lifter
  - icon: ![Follower losing the cam](assets/items/cd-lost-contact.webp)

  You turn the crank. The cam lifts the rod, but the light rod sometimes hangs in its guide as the cam drops away. Its foot loses contact.
- `cd-sprung-lifter` Lifter
  - icon: ![Lifter with its spring fitted](assets/items/cd-sprung-lifter.webp)

  The spring can be fitted before testing. Turn the crank to compare its light pull with a brief unhooked run.
- `cd-working-lifter` Lifter
  - icon: ![Reliable cam lifter](assets/items/cd-working-lifter.webp)

  You compare the follower with and without the spring’s pull, stopping before unhooking or rehooking it. Without the pull, the light follower sometimes hangs; with it, the foot follows every fall. The spring keeps the foot gently against the cam. You turn the crank again: round becomes up, down, up, down, without the rod wandering off sideways.

**Combinations**
- `cd-bearing-frames` [consume] + `cd-base` [transform] -> `cd-bearings`
- `cd-shaft` [consume] + `cd-bearings` [transform] -> `cd-crank-frame`
- `cd-cam` [consume] + `cd-crank-frame` [transform] -> `cd-cam-frame`
- `cd-follower` [transform] + `cd-guide` [consume] -> `cd-guided-follower`
- `cd-guided-follower` [consume] + `cd-cam-frame` [transform] -> `cd-lifter`
- `cd-crank-key` [preserve] + `cd-lifter` [transform] -> `cd-lost-contact`
- `cd-return-spring` [consume] + `cd-lost-contact` [transform] -> `cd-working-lifter`
- `cd-return-spring` [consume] + `cd-lifter` [transform] -> `cd-sprung-lifter`
- `cd-crank-key` [preserve] + `cd-sprung-lifter` [transform] -> `cd-working-lifter`


## `c06` The dragon says hello
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Crank dragon](assets/items/crank-dragon.webp)

First give the dragon one wave with the original cam, then exchange cams and compare its greeting. Jo brings the dragon’s cut-out pieces, including a very small pair of spectacles. “No lenses,” she says. “But it looks as though it has strong opinions about turnips.”

**Goals**
- Fit the hinge pins to the wings -- `cd-hinged-wings`
- next: Attach the wings to the body -- `cd-winged-dragon`
- next: Attach the tail to the body -- `cd-jointed-dragon`
- next: Mount the dragon on the lifter -- `cd-mounted-dragon`
- next: Fit the wing links to the follower -- `cd-linked-dragon`
- next: Turn the crank handle to make the dragon wave -- `cd-first-wave`
- next: Try the two-humped cam -- `cd-double-wave`
- next: Turn the crank handle for the dragon’s new wave -- `crank-dragon`

**Hotspots**
- `cd-working-lifter` (center 390px, 500px)
  - icon: ![Reliable cam lifter](assets/hotspots/c06--cd-working-lifter.webp)
- `cd-mounted-dragon` (center 390px, 500px)
  - icon: ![Dragon body on the mechanism](assets/hotspots/c06--cd-mounted-dragon.webp)
- `cd-linked-dragon` (center 390px, 500px)
  - icon: ![Dragon linked to its follower](assets/hotspots/c06--cd-linked-dragon.webp)
- `cd-first-wave` (center 390px, 500px)
  - icon: ![Dragon giving one wave](assets/hotspots/c06--cd-first-wave.webp)
- `cd-double-wave` (center 390px, 500px)
  - icon: ![Dragon with a second greeting](assets/hotspots/c06--cd-double-wave.webp)

**Items**
- `cd-cutouts` Body
  - icon: ![Dragon body cut-out](assets/items/cd-cutouts.webp)

  A stiff card body with its lightweight paper back scales already attached, prepared shoulder and tail holes, and folded base tabs. The scales leave the linkage clear; spectacles are already drawn on the body.
- `cd-hinge-pins` Hinge pins
  - icon: ![Soft wing-hinge pins](assets/items/cd-hinge-pins.webp)

  One complete hinge fitting represents the pair. Two broad-headed split pins for the wing pivots. Each carries its spacing collar and smooth washer, which keep the card clear of the body and let it turn freely.
- `cd-wings` Wings
  - icon: ![Two wing cut-outs](assets/items/cd-wings.webp)

  One wing represents the mirrored pair. A mirrored pair of light card wings, each with a prepared shoulder hole and an integral drive tab near its root.
- `cd-tail` Tail
  - icon: ![Dragon tail with captive pin](assets/items/cd-tail.webp)

  A decorative card tail with its own broad-headed pin and washer retained in the attachment hole.
- `cd-hinged-wings` Wings
  - icon: ![Wings with their hinge pins](assets/items/cd-hinged-wings.webp)

  Both wings are prepared; one is shown. Each wing has a pin, collar and washer in its shoulder hole. The retainers can be opened again to pass the pins through the body.
- `cd-winged-dragon` Dragon
  - icon: ![Dragon body with hinged wings](assets/items/cd-winged-dragon.webp)

  The two wings turn freely on the body’s shoulder holes. Their roots remain clear for the follower links.
- `cd-linkage` Wing links
  - icon: ![Wing-to-follower links](assets/items/cd-linkage.webp)

  One link represents the pair. Two separate short rods with pivot holes at both ends, a shared crosshead pin, spacers and a retainer. Fit this connection after mounting the dragon: its two ends need the wing roots and the follower’s crosshead in their final positions. Each rod can then change its angle as its wing turns.
- `cd-double-cam` Two-humped cam
  - icon: ![Two-humped greeting cam](assets/items/cd-double-cam.webp)

  An exchangeable cam with two rounded rises and falls around its edge, the same shaft fitting and the same maximum lift as the first cam. Its package includes a clip for parking the original cam. To exchange them, stop the mechanism, open the hub and end collar, and withdraw the shaft through its bearings.
- `cd-first-wave` Dragon
  - icon: ![Dragon giving one wave](assets/items/cd-first-wave.webp)

  One turn gives one rise and fall of the wings. Jo answers with one slow wave. Behind her you notice an old drawing labelled **A fair in the air**, with tiny stalls balanced on an empty outline.

  “I drew that when I was about your age,” she says. “I could make the stalls. I never worked out where to put them.”
- `cd-double-wave` Dragon
  - icon: ![Dragon with a second greeting](assets/items/cd-double-wave.webp)

  You stop with the follower raised and fit its keeper pin. Loosen the hub and collar, park the end cap, and withdraw the shaft to exchange the cams. Slide the shaft back, secure the fittings and remove the keeper before turning again. The original cam parks in its clip. Two rounded rises now wait under the follower. Everything is secure for the comparison test.
- `cd-jointed-dragon` Dragon
  - icon: ![Jointed card dragon](assets/items/cd-jointed-dragon.webp)
- `cd-mounted-dragon` Dragon
  - icon: ![Dragon body on the mechanism](assets/items/cd-mounted-dragon.webp)
- `cd-linked-dragon` Dragon
  - icon: ![Dragon linked to its follower](assets/items/cd-linked-dragon.webp)

  The body stays still on its base. When the follower rises, the two rods push the wing roots. Each rod pivots independently while its wing turns about the shoulder hinge.
- `crank-dragon` Crank dragon
  - icon: ![Crank dragon](assets/items/crank-dragon.webp)

  ![Crank dragon in the garden](assets/rewards/crank-dragon.webp)

  You turn the handle: wave-wave, pause, wave-wave. “That one’s for Kit,” you say. The first cam stays in its clip, ready for another workshop afternoon.

  You release the base and lift the dragon from the bench, with the spare cam and removable handle parked in their clips. It can perform on any flat table; its little mounting holes remain clear.

**Combinations**
- `cd-hinge-pins` [consume] + `cd-wings` [transform] -> `cd-hinged-wings`
- `cd-hinged-wings` [consume] + `cd-cutouts` [transform] -> `cd-winged-dragon`
- `cd-tail` [consume] + `cd-winged-dragon` [transform] -> `cd-jointed-dragon`
- `cd-jointed-dragon` [consume] + `cd-working-lifter` [transform] -> `cd-mounted-dragon`
- `cd-linkage` [consume] + `cd-mounted-dragon` [transform] -> `cd-linked-dragon`
- `cd-crank-key` [preserve] + `cd-linked-dragon` [transform] -> `cd-first-wave`
- `cd-double-cam` [consume] + `cd-first-wave` [transform] -> `cd-double-wave`
- `cd-crank-key` [preserve] + `cd-double-wave` [transform] -> `crank-dragon`


## `c07` A look over the hedge
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Periscope](assets/items/periscope.webp)

Jo’s hat vanishes behind the tall garden screen. Her voice remains. “Can your next invention find out whether I am still in it?”

**Goals**
- Stick the lining inside the tube net -- `pe-lined`
- next: Fold the tube net with the folding tool -- `pe-tube`
- next: Fit the upper mirror -- `pe-upper`
- next: Fit the lower mirror -- `pe-both`
- next: Fit the window shades -- `pe-baffled`
- next: Use the periscope to spot Jo’s hat -- `periscope`

**Hotspots**
- `pe-net` (center 390px, 500px)
  - icon: ![Periscope tube net](assets/hotspots/c07--pe-net.webp)
- `pe-lined` (center 390px, 500px)
  - icon: ![Periscope net with a dark lining](assets/hotspots/c07--pe-lined.webp)
- `pe-tube` (center 390px, 500px)
  - icon: ![Folded periscope tube](assets/hotspots/c07--pe-tube.webp)
- `pe-upper` (center 390px, 500px)
  - icon: ![Tube with an upper mirror](assets/hotspots/c07--pe-upper.webp)
- `pe-both` (center 390px, 500px)
  - icon: ![Tube with two facing mirrors](assets/hotspots/c07--pe-both.webp)
- `pe-baffled` (center 390px, 500px)
  - icon: ![Periscope with shaded windows](assets/hotspots/c07--pe-baffled.webp)

**Items**
- `pe-net` Tube net
  - icon: ![Periscope tube net](assets/items/pe-net.webp)

  A stiff card net held flat in the bench clips. It has scored folds, prepared peel-and-stick fastening tabs, opposite end windows and prepared mirror ledges at forty-five degrees.
- `pe-lining` Lining
  - icon: ![Dark inner lining](assets/items/pe-lining.webp)

  Four lining panels are supplied, two shorter to leave the windows clear; one panel is shown. Self-adhesive dark paper cut to the inside faces. It absorbs stray light instead of reflecting it around the tube.
- `pe-folder` Folding tool
  - icon: ![Smooth folding tool](assets/items/pe-folder.webp)

  A blunt tool for pressing the prepared card creases and fastening tabs.
- `pe-upper-mirror` Upper mirror
  - icon: ![Upper mirror and clip](assets/items/pe-upper-mirror.webp)

  A small unbreakable mirror on a clip that fits the top ledge. Its reflecting face looks down the tube and out of the upper window.
- `pe-lower-mirror` Lower mirror
  - icon: ![Lower mirror and clip](assets/items/pe-lower-mirror.webp)

  A matching mirror for the lower ledge. Its reflecting face looks up the tube and toward the eyepiece; the two mirror surfaces will be parallel.
- `pe-baffles` Window shades
  - icon: ![Two window shades](assets/items/pe-baffles.webp)

  Two matching dark window shades are supplied; one is shown. Their short sleeves frame the two openings without blocking the mirrors.
- `pe-hat` Jo’s hat
  - icon: ![Jo’s striped hat](assets/items/pe-hat.webp)

  A large floppy hat with a bright stripe. Jo will hold it above the screen while you look through the lower window.
- `pe-lined` Tube net
  - icon: ![Periscope net with a dark lining](assets/items/pe-lined.webp)
- `pe-tube` Tube
  - icon: ![Folded periscope tube](assets/items/pe-tube.webp)
- `pe-upper` Tube
  - icon: ![Tube with an upper mirror](assets/items/pe-upper.webp)
- `pe-both` Tube
  - icon: ![Tube with two facing mirrors](assets/items/pe-both.webp)

  Light from the upper window reflects down the tube, then off the lower mirror toward your eye. The pair lets you look from a different height.
- `pe-baffled` Periscope
  - icon: ![Periscope with shaded windows](assets/items/pe-baffled.webp)
- `periscope` Periscope
  - icon: ![Periscope](assets/items/periscope.webp)

  ![Periscope in the garden](assets/rewards/periscope.webp)

  You release the bench clips and lift the tube to the screen. Jo’s hat appears in the lower window; when she moves it left, you see it move left. The hat dips, and her eyes replace it.

  “You found the person too.” You turn toward the pinball stall and see that over the screen as well, with both feet still on the ground.

**Combinations**
- `pe-lining` [consume] + `pe-net` [transform] -> `pe-lined`
- `pe-folder` [preserve] + `pe-lined` [transform] -> `pe-tube`
- `pe-upper-mirror` [consume] + `pe-tube` [transform] -> `pe-upper`
- `pe-lower-mirror` [consume] + `pe-upper` [transform] -> `pe-both`
- `pe-baffles` [consume] + `pe-both` [transform] -> `pe-baffled`
- `pe-hat` [preserve] + `pe-baffled` [transform] -> `periscope`


## `c08` A pocket full of fireworks
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Kaleidoscope](assets/items/kaleidoscope.webp)

Two mirrors let you look round a corner. Three long mirrors might do something stranger; Jo spreads a few coloured pieces beside a little turning drum.

**Goals**
- Arrange the mirror strips around the triangle former -- `ka-triangle`
- next: Tape the mirror triangle together -- `ka-prism`
- next: Slide the mirror triangle into the viewing tube -- `ka-eye`
- next: Put the coloured pieces into the colour cell -- `ka-colour-drum`
- next: Fit the colour cell to the viewing tube -- `ka-drum-scope`
- next: Fit the light cover over the colour cell -- `ka-sealed`
- next: Hold it toward the lantern and turn -- `kaleidoscope`

**Hotspots**
- `ka-strips` (center 390px, 500px)
  - icon: ![Three long mirror strips](assets/hotspots/c08--ka-strips.webp)
- `ka-triangle` (center 390px, 500px)
  - icon: ![Three mirrors in a triangle](assets/hotspots/c08--ka-triangle.webp)
- `ka-prism` (center 390px, 500px)
  - icon: ![Bound mirror triangle](assets/hotspots/c08--ka-prism.webp)
- `ka-eye` (center 390px, 500px)
  - icon: ![Mirror tube with an eyepiece](assets/hotspots/c08--ka-eye.webp)
- `ka-drum-scope` (center 390px, 500px)
  - icon: ![Mirror tube with a rotating colour drum](assets/hotspots/c08--ka-drum-scope.webp)
- `ka-sealed` (center 390px, 500px)
  - icon: ![Kaleidoscope ready for light](assets/hotspots/c08--ka-sealed.webp)

**Items**
- `ka-strips` Mirror strips
  - icon: ![Three long mirror strips](assets/items/ka-strips.webp)

  Three equal unbreakable mirror strips held in the bench’s folding cradle, reflecting faces upward.
- `ka-former` Triangle former
  - icon: ![Triangular folding former](assets/items/ka-former.webp)

  A smooth triangular tool with three equal sides. It holds the mirrors with their reflecting faces inward while you close their long edges.
- `ka-tape` Tape
  - icon: ![Flexible binding tape](assets/items/ka-tape.webp)

  A prepared strip of tough tape for the outside seams of the mirror triangle. Nothing covers the reflecting faces.
- `ka-tube` Viewing tube
  - icon: ![Protective outer tube](assets/items/ka-tube.webp)

  A light tube with padded mirror supports, a rotating front collar and a fitted dark eyecap with a small central viewing hole.
- `ka-chips` Coloured pieces
  - icon: ![Coloured translucent shapes](assets/items/ka-chips.webp)

  Three translucent pieces: a green triangle, an amber crescent and a blue disc. The triangle represents the supplied set. Leave room in the cell for all three to tumble.
- `ka-cell` Colour cell
  - icon: ![Clear lidded colour cell](assets/items/ka-cell.webp)

  A shallow clear cell with a snap lid and a rim that fits the tube’s rotating collar. Its depth leaves space for the coloured pieces to move.
- `ka-diffuser` Light cover
  - icon: ![Milky light cover](assets/items/ka-diffuser.webp)

  A translucent cover for the front of the colour cell. It spreads light behind the loose pieces.
- `work-lantern` Lantern
  - icon: ![Diffused battery lantern](assets/items/work-lantern.webp)

  A small enclosed low-voltage lantern with its battery fitted and a broad milky light face. Its light is gentle enough for viewing the toys.
- `ka-triangle` Mirror triangle
  - icon: ![Three mirrors in a triangle](assets/items/ka-triangle.webp)

  Each mirror reflects the other mirrors as well as what is at the end. Those reflections can repeat a small view into a much larger pattern.
- `ka-prism` Mirror triangle
  - icon: ![Bound mirror triangle](assets/items/ka-prism.webp)
- `ka-eye` Viewing tube
  - icon: ![Mirror tube with an eyepiece](assets/items/ka-eye.webp)
- `ka-colour-drum` Colour cell
  - icon: ![Colour drum with loose shapes](assets/items/ka-colour-drum.webp)

  You close the lid with space around the shapes. Tilt the drum and they slide; packing it full would stop the changing pattern.
- `ka-drum-scope` Kaleidoscope
  - icon: ![Mirror tube with a rotating colour drum](assets/items/ka-drum-scope.webp)
- `ka-sealed` Kaleidoscope
  - icon: ![Kaleidoscope ready for light](assets/items/ka-sealed.webp)
- `kaleidoscope` Kaleidoscope
  - icon: ![Kaleidoscope](assets/items/kaleidoscope.webp)

  ![Kaleidoscope in the garden](assets/rewards/kaleidoscope.webp)

  You lift the finished tube from the cradle and aim its covered end toward the lantern. Three little shapes become a crowd of green triangles, amber curls and blue dots. Turn the drum, and the whole pattern tumbles into a new arrangement.

  Jo takes a turn. For once, she says nothing at all.

**Combinations**
- `ka-former` [preserve] + `ka-strips` [transform] -> `ka-triangle`
- `ka-tape` [consume] + `ka-triangle` [transform] -> `ka-prism`
- `ka-tube` [consume] + `ka-prism` [transform] -> `ka-eye`
- `ka-chips` [consume] + `ka-cell` [transform] -> `ka-colour-drum`
- `ka-colour-drum` [consume] + `ka-eye` [transform] -> `ka-drum-scope`
- `ka-diffuser` [consume] + `ka-drum-scope` [transform] -> `ka-sealed`
- `work-lantern` [preserve] + `ka-sealed` [transform] -> `kaleidoscope`


## `c09` The tall thing that must not wobble
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Lifting crane](assets/items/lifting-crane.webp)

Jo lifts a basket onto the fair’s little stage. “A crane could do this,” you say. She lowers the basket again. “Then it can have my job. Start with somewhere solid to stand.”

**Goals**
- Fix the uprights to the base -- `lc-mast`
- next: Fit the braces to the uprights -- `lc-braced`
- next: Fit the boom to the mast -- `lc-boom-frame`
- next: Add the stay to support the boom -- `lc-stayed`
- next: Fit the pulley wheel into the pulley fork -- `lc-pulley-block`
- next: Mount the pulley block at the boom tip -- `lc-pulley-frame`
- next: Fit the feet to the base -- `lc-wide-frame`

**Hotspots**
- `lc-base` (center 390px, 500px)
  - icon: ![Crane base board](assets/hotspots/c09--lc-base.webp)
- `lc-mast` (center 390px, 500px)
  - icon: ![Base with an upright mast](assets/hotspots/c09--lc-mast.webp)
- `lc-braced` (center 390px, 500px)
  - icon: ![Mast with triangular braces](assets/hotspots/c09--lc-braced.webp)
- `lc-boom-frame` (center 390px, 500px)
  - icon: ![Crane frame with a hinged boom](assets/hotspots/c09--lc-boom-frame.webp)
- `lc-stayed` (center 390px, 500px)
  - icon: ![Crane boom held by its stay](assets/hotspots/c09--lc-stayed.webp)
- `lc-pulley-frame` (center 390px, 500px)
  - icon: ![Crane frame with a tip pulley](assets/hotspots/c09--lc-pulley-frame.webp)
- `lc-wide-frame` (center 390px, 500px)
  - icon: ![Braced crane with spreading feet](assets/hotspots/c09--lc-wide-frame.webp)

**Items**
- `lc-base` Base
  - icon: ![Crane base board](assets/items/lc-base.webp)

  A wide base board held in the bench clips. It has prepared mast sockets, winch holes and sockets for spreading feet.
- `lc-uprights` Uprights
  - icon: ![Mast uprights and crosspiece](assets/items/lc-uprights.webp)

  Two upright beams joined by a crosspiece, with captive mounting screws and a prepared top hinge.
- `lc-braces` Braces
  - icon: ![Diagonal mast braces](assets/items/lc-braces.webp)

  One complete brace represents the matching pair. Two stiff diagonal struts with captive end fasteners. They join the mast to the base to make triangles.
- `lc-boom` Boom
  - icon: ![Light crane boom](assets/items/lc-boom.webp)

  A hollow beam with a root hinge, a captive broad-headed hinge pin and soft retaining cap, a tip clevis socket and an eye for its support stay.
- `lc-stay` Stay
  - icon: ![Boom support stay](assets/items/lc-stay.webp)

  A fixed-length cord with captive hooks for the mast top and boom eye. It holds the boom above the work area.
- `lc-pulley-wheel` Pulley wheel
  - icon: ![Grooved pulley wheel](assets/items/lc-pulley-wheel.webp)

  A smooth wheel with a deep rope groove and a prepared axle hole.
- `lc-clevis` Pulley fork
  - icon: ![Pulley fork and axle](assets/items/lc-clevis.webp)

  A small fork with a captive blunt axle, retaining cap and a mounting foot for the boom tip.
- `lc-feet` Feet
  - icon: ![Spreading crane feet](assets/items/lc-feet.webp)

  One outrigger represents the matching pair. Two broad folding feet with locking clips. They widen the base in the direction the boom reaches.
- `lc-mast` Mast
  - icon: ![Base with an upright mast](assets/items/lc-mast.webp)
- `lc-braced` Mast
  - icon: ![Mast with triangular braces](assets/items/lc-braced.webp)

  A rectangular frame can lean into a diamond. The diagonal braces hold the corners apart, so sideways force cannot change the angles so easily.
- `lc-boom-frame` Crane
  - icon: ![Crane frame with a hinged boom](assets/items/lc-boom-frame.webp)
- `lc-stayed` Crane
  - icon: ![Crane boom held by its stay](assets/items/lc-stayed.webp)
- `lc-pulley-block` Pulley block
  - icon: ![Pulley in its fork](assets/items/lc-pulley-block.webp)

  The rope will run over the wheel instead of scraping around the end of the boom. This single fixed pulley changes the pull’s direction; it does not halve the weight.
- `lc-pulley-frame` Crane
  - icon: ![Crane frame with a tip pulley](assets/items/lc-pulley-frame.webp)
- `lc-wide-frame` Crane
  - icon: ![Braced crane with spreading feet](assets/items/lc-wide-frame.webp)

  The feet make a wider patch of ground to stand on. Jo nudges the mast gently; its triangles hold their shape.

  “The basket is being patient,” she says. “I am nearly as good at it.”

**Combinations**
- `lc-uprights` [consume] + `lc-base` [transform] -> `lc-mast`
- `lc-braces` [consume] + `lc-mast` [transform] -> `lc-braced`
- `lc-boom` [consume] + `lc-braced` [transform] -> `lc-boom-frame`
- `lc-stay` [consume] + `lc-boom-frame` [transform] -> `lc-stayed`
- `lc-pulley-wheel` [transform] + `lc-clevis` [consume] -> `lc-pulley-block`
- `lc-pulley-block` [consume] + `lc-stayed` [transform] -> `lc-pulley-frame`
- `lc-feet` [consume] + `lc-pulley-frame` [transform] -> `lc-wide-frame`


## `c10` Please hold
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Lifting crane](assets/items/lifting-crane.webp)

The frame can stand up. Now the crane must lift a load, keep it there, and bring it down without flinging it into Jo’s tomatoes.

**Goals**
- Fit the crank to the winch drum -- `lc-winch`
- next: Mount the winch on the crane -- `lc-winch-frame`
- next: Thread the rope over the pulley -- `lc-rigged`
- next: Add ballast to steady the crane
  - either: `lc-ballasted-unproven`
  - or: `lc-pawl-ballasted-unproven`
  - or: `lc-balanced`
  - or: `lc-ratchet-frame`
- next: Lift the test weight a little above the bench
  - either: `lc-tipping`
  - or: `lc-pawl-tipping`
  - or: `lc-balanced`
  - or: `lc-ratchet-frame`
- next: Fit the pawl to stop the drum unwinding
  - either: `lc-pawl-rigged`
  - or: `lc-pawl-tipping`
  - or: `lc-pawl-ballasted-unproven`
  - or: `lc-ratchet-frame`
- next: Lift the basket, hold it, then lower it gently -- `lifting-crane`

**Hotspots**
- `lc-wide-frame` (center 390px, 500px)
  - icon: ![Braced crane with spreading feet](assets/hotspots/c10--lc-wide-frame.webp)
- `lc-winch-frame` (center 390px, 500px)
  - icon: ![Crane with a hand winch](assets/hotspots/c10--lc-winch-frame.webp)
- `lc-rigged` (center 390px, 500px)
  - icon: ![Crane with a lifting line](assets/hotspots/c10--lc-rigged.webp)
- `lc-tipping` (center 390px, 500px)
  - icon: ![Crane lifting at its back feet](assets/hotspots/c10--lc-tipping.webp)
- `lc-balanced` (center 390px, 500px)
  - icon: ![Crane with rear ballast](assets/hotspots/c10--lc-balanced.webp)
- `lc-ratchet-frame` (center 390px, 500px)
  - icon: ![Crane with a holding pawl](assets/hotspots/c10--lc-ratchet-frame.webp)
- `lc-pawl-rigged` (center 390px, 500px)
  - icon: ![Rigged crane with holding pawl](assets/hotspots/c10--lc-pawl-rigged.webp)
- `lc-pawl-tipping` (center 390px, 500px)
  - icon: ![Stiff crane beginning to tip](assets/hotspots/c10--lc-pawl-tipping.webp)
- `lc-ballasted-unproven` (center 390px, 500px)
  - icon: ![Ballasted crane ready for a test](assets/hotspots/c10--lc-ballasted-unproven.webp)
- `lc-pawl-ballasted-unproven` (center 390px, 500px)
  - icon: ![Ballasted holding crane ready for a test](assets/hotspots/c10--lc-pawl-ballasted-unproven.webp)

**Items**
- `lc-drum` Winch drum
  - icon: ![Winding drum and bearing bracket](assets/items/lc-drum.webp)

  A small drum on a shaft with two bearing brackets, rope anchor and captive mounting screws.
- `lc-crank-wheel` Crank
  - icon: ![Crank and toothed ratchet wheel](assets/items/lc-crank-wheel.webp)

  A long hand crank and toothed wheel with a spacer, washer and end screw. Their matching sockets fit the drum shaft; the end screw keeps the stack in place. The wheel can later accept a holding pawl.
- `lc-rope` Rope
  - icon: ![Lifting cord and closed hook](assets/items/lc-rope.webp)

  A soft cord with a closed snap hook at one end and an anchor loop at the other. It fits the drum and pulley groove.
- `lc-test-load` Test weight
  - icon: ![Small padded test weight](assets/items/lc-test-load.webp)

  A light, soft-edged weight with a lifting loop. Jo keeps a hand beside it during the first low lift; it returns to the bench after the test.
- `lc-ballast` Ballast
  - icon: ![Rear ballast block](assets/items/lc-ballast.webp)

  A low block with a captive clip for the back of the crane base. Its weight opposes the forward turning effect of the load.
- `lc-pawl` Pawl
  - icon: ![Holding pawl and release lever](assets/items/lc-pawl.webp)

  A pivoted pawl, light spring and hand lever on a foot with captive screws and nuts that attach beside the toothed wheel. It lets the drum turn while lifting and catches when it tries to unwind.
- `lc-basket` Basket
  - icon: ![Small cargo basket](assets/items/lc-basket.webp)

  A shallow basket with a lifting loop and a handful of light wooden play blocks already inside.
- `lc-winch` Winch
  - icon: ![Hand winch](assets/items/lc-winch.webp)

  The crank turns the drum, winding in cord. A longer crank gives your hand more turning effect, although your hand travels farther for each drum turn.
- `lc-winch-frame` Crane
  - icon: ![Crane with a hand winch](assets/items/lc-winch-frame.webp)
- `lc-rigged` Crane
  - icon: ![Crane with a lifting line](assets/items/lc-rigged.webp)
- `lc-tipping` Crane
  - icon: ![Crane lifting at its back feet](assets/items/lc-tipping.webp)

  You loosen the bench clips for a low test, keeping a hand beside the load. As the weight rises, the back feet begin to lift. You lower it immediately and secure the base again.

  The frame has stayed stiff. The whole crane is trying to tip.
- `lc-balanced` Crane
  - icon: ![Crane with rear ballast](assets/items/lc-balanced.webp)

  The block sits low behind the mast. You loosen the clips again and repeat the supported low lift, then lower the test weight: this time all the feet stay on the bench.
- `lc-pawl-rigged` Crane
  - icon: ![Rigged crane with holding pawl](assets/items/lc-pawl-rigged.webp)

  The holding pawl fits beside the drum before the test. It can stop the rope unwinding, but it cannot stop the whole crane tipping.
- `lc-ballasted-unproven` Crane
  - icon: ![Ballasted crane ready for a test](assets/items/lc-ballasted-unproven.webp)

  You put the block behind the mast before lifting anything. A sensible prediction: the rear weight should oppose the load's forward turning effect. Now try the padded weight to check it.
- `lc-pawl-ballasted-unproven` Crane
  - icon: ![Ballasted holding crane ready for a test](assets/items/lc-pawl-ballasted-unproven.webp)

  Rear ballast and holding pawl are both fitted. One balances the whole crane; the other catches the drum. The low test will check them together.
- `lc-pawl-tipping` Crane
  - icon: ![Stiff crane beginning to tip](assets/items/lc-pawl-tipping.webp)

  You release the bench clips and make the supported low test. The drum holds its rope, but the rear feet start to lift. You lower the weight at once: holding a load and balancing it are different jobs.
- `lc-ratchet-frame` Crane
  - icon: ![Crane with a holding pawl](assets/items/lc-ratchet-frame.webp)

  With the rear ballast fitted and the clips released, the supported low lift leaves every foot down. The pawl clicks over the teeth while you wind in. If you stop turning, it catches a tooth instead of letting the drum unwind. To lower, hold the crank before easing the release lever.
- `lifting-crane` Crane
  - icon: ![Lifting crane](assets/items/lifting-crane.webp)

  ![Lifting crane in the garden](assets/rewards/lifting-crane.webp)

  You hook the basket, raise it just above the miniature stage and stop cranking. The pawl holds. Jo slides the small stage underneath the hanging basket. With the crank in your hand, you ease the lever and lower the basket onto it.

  “A delivery service,” says Jo, moving one play block into place. You bring the basket back to the base and lift the complete crane to its garden stall.

**Combinations**
- `lc-crank-wheel` [consume] + `lc-drum` [transform] -> `lc-winch`
- `lc-winch` [consume] + `lc-wide-frame` [transform] -> `lc-winch-frame`
- `lc-rope` [consume] + `lc-winch-frame` [transform] -> `lc-rigged`
- `lc-test-load` [preserve] + `lc-rigged` [transform] -> `lc-tipping`
- `lc-ballast` [consume] + `lc-tipping` [transform] -> `lc-balanced`
- `lc-pawl` [consume] + `lc-balanced` [transform] -> `lc-ratchet-frame`
- `lc-pawl` [consume] + `lc-rigged` [transform] -> `lc-pawl-rigged`
- `lc-test-load` [preserve] + `lc-pawl-rigged` [transform] -> `lc-pawl-tipping`
- `lc-ballast` [consume] + `lc-pawl-tipping` [transform] -> `lc-ratchet-frame`
- `lc-ballast` [consume] + `lc-rigged` [transform] -> `lc-ballasted-unproven`
- `lc-test-load` [preserve] + `lc-ballasted-unproven` [transform] -> `lc-balanced`
- `lc-ballast` [consume] + `lc-pawl-rigged` [transform] -> `lc-pawl-ballasted-unproven`
- `lc-test-load` [preserve] + `lc-pawl-ballasted-unproven` [transform] -> `lc-ratchet-frame`
- `lc-basket` [consume] + `lc-ratchet-frame` [transform] -> `lifting-crane`


## `c11` A motor makes a wiggle
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![String-wave machine](assets/items/wave-machine.webp)

On the third afternoon, the dragon waves because you keep turning its handle. Jo sets a little motor on the bench. “This one will keep turning for us. What could we make that is interesting to watch?” You stretch a bright cord between your hands.

**Goals**
- Mount the motor on the base -- `wm-motor-frame`
- next: Fit the cord driver beside the motor -- `wm-driver-frame`
- next: Loop the belt over the pulleys -- `wm-belt-frame`
- next: Attach the cord to the cord driver -- `wm-cord-frame`
- next: Add the spring to tension the cord -- `wm-tensioned`
- next: Fit the guard over the moving drive -- `wm-guarded`
- next: Connect the speed controller and watch the cord -- `wm-running`

**Hotspots**
- `wm-base` (center 390px, 500px)
  - icon: ![Long wave-machine base](assets/hotspots/c11--wm-base.webp)
- `wm-motor-frame` (center 390px, 500px)
  - icon: ![Wave frame with a motor](assets/hotspots/c11--wm-motor-frame.webp)
- `wm-driver-frame` (center 390px, 500px)
  - icon: ![Wave frame with an eccentric driver](assets/hotspots/c11--wm-driver-frame.webp)
- `wm-belt-frame` (center 390px, 500px)
  - icon: ![Wave frame with a belt drive](assets/hotspots/c11--wm-belt-frame.webp)
- `wm-cord-frame` (center 390px, 500px)
  - icon: ![Wave frame with a loose cord](assets/hotspots/c11--wm-cord-frame.webp)
- `wm-tensioned` (center 390px, 500px)
  - icon: ![Wave frame with a tensioned cord](assets/hotspots/c11--wm-tensioned.webp)
- `wm-guarded` (center 390px, 500px)
  - icon: ![Guarded string-wave machine](assets/hotspots/c11--wm-guarded.webp)
- `wm-running` (center 390px, 500px)
  - icon: ![Cord with a travelling wiggle](assets/hotspots/c11--wm-running.webp)

**Items**
- `wm-controller` Speed controller
  - icon: ![Battery and speed controller](assets/items/wm-controller.webp)

  A compatible enclosed low-voltage battery holder with cells fitted, an on-off switch, speed dial and keyed plug. Its clips fit the base; start with the switch off.
- `wm-running` Wave machine
  - icon: ![Cord with a travelling wiggle](assets/items/wm-running.webp)

  You plug in the controller, turn it on and slowly increase the speed. The peg keeps shaking one end; a disturbance travels along the cord and reflects from the far end.
- `wm-base` Base
  - icon: ![Long wave-machine base](assets/items/wm-base.webp)

  A light base with two fitted end posts, held in the bench clips. One post carries a cord anchor and tension screw; the other supports the driver bearing. A hollow wooden soundbox with a thin top is already clipped to the base, and soft isolation pads are fitted beneath its feet. Prepared holes take the motor cradle; small clips park the removable bridge and pick.
- `wm-mounted-motor` Motor
  - icon: ![Motor secured in its cradle](assets/items/wm-mounted-motor.webp)

  An ordinary compatible low-voltage motor with a capped drive pulley and insulated plug lead. Its fitted cradle has a retaining strap, captive screws and soft isolation mounts, holding the motor clear of the wooden base. No battery is connected.
- `wm-driver` Cord driver
  - icon: ![Eccentric cord driver](assets/items/wm-driver.webp)

  A small pulley wheel on its own bearing, with a captive swivel peg a little off centre. The swivel lets the cord move without twisting up.
- `wm-belt` Belt
  - icon: ![Soft drive belt](assets/items/wm-belt.webp)

  A short rubber belt sized for the motor pulley and driver pulley. It will run behind a cover.
- `wm-cord` Cord
  - icon: ![Bright flexible cord](assets/items/wm-cord.webp)

  A long, light nylon cord with prepared end loops. One loop fits the driver swivel, the other the tension spring.
- `wm-spring` Spring
  - icon: ![Cord tension spring](assets/items/wm-spring.webp)

  A small extension spring with closed end hooks. It links the cord to the adjustable post and keeps a steady pull on it.
- `wm-guard` Guard
  - icon: ![Clear drive guard](assets/items/wm-guard.webp)

  A transparent snap-on cover for the motor pulleys and belt, with a smooth opening for the moving cord and a slot for the electrical plug.
- `wm-motor-frame` Wave machine
  - icon: ![Wave frame with a motor](assets/items/wm-motor-frame.webp)
- `wm-driver-frame` Wave machine
  - icon: ![Wave frame with an eccentric driver](assets/items/wm-driver-frame.webp)

  The swivel peg follows a small circle instead of sitting at the axle centre. It will keep disturbing one end of the cord while the far end stays anchored.
- `wm-belt-frame` Wave machine
  - icon: ![Wave frame with a belt drive](assets/items/wm-belt-frame.webp)
- `wm-cord-frame` Wave machine
  - icon: ![Wave frame with a loose cord](assets/items/wm-cord-frame.webp)
- `wm-tensioned` Wave machine
  - icon: ![Wave frame with a tensioned cord](assets/items/wm-tensioned.webp)
- `wm-guarded` Wave machine
  - icon: ![Guarded string-wave machine](assets/items/wm-guarded.webp)

  The clear cover keeps fingers away from the belt and pulleys. Through it you can still trace the movement: motor, belt, off-centre peg, cord. The motor remains disconnected until its controller arrives.

**Combinations**
- `wm-mounted-motor` [consume] + `wm-base` [transform] -> `wm-motor-frame`
- `wm-driver` [consume] + `wm-motor-frame` [transform] -> `wm-driver-frame`
- `wm-belt` [consume] + `wm-driver-frame` [transform] -> `wm-belt-frame`
- `wm-cord` [consume] + `wm-belt-frame` [transform] -> `wm-cord-frame`
- `wm-spring` [consume] + `wm-cord-frame` [transform] -> `wm-tensioned`
- `wm-guard` [consume] + `wm-tensioned` [transform] -> `wm-guarded`



- `wm-controller` [consume] + `wm-guarded` [transform] -> `wm-running`

## `c12` Watch it. Hear it.
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![String-wave machine](assets/items/wave-machine.webp)

The cord is already dancing. Jo folds a tiny paper rider. “Does the cord travel with the wiggle?” You stop the motor before fitting anything to the cord or base, and restart it for each observation.

**Goals**
- Clip the paper rider onto the cord -- `wm-marked`
- next: Use the tension key to find a standing wave -- `wm-looping`
- next: Slide the bridge under the stopped cord -- `wm-bridged`
- next: Pluck the cord with the pick -- `wave-machine`

**Hotspots**
- `wm-running` (center 390px, 500px)
  - icon: ![Cord with a travelling wiggle](assets/hotspots/c12--wm-running.webp)
- `wm-marked` (center 390px, 500px)
  - icon: ![Wave cord with a paper rider](assets/hotspots/c12--wm-marked.webp)
- `wm-looping` (center 390px, 500px)
  - icon: ![Cord making two broad loops](assets/hotspots/c12--wm-looping.webp)
- `wm-bridged` (center 390px, 500px)
  - icon: ![Cord resting on a movable bridge](assets/hotspots/c12--wm-bridged.webp)

**Items**
- `wm-rider` Paper rider
  - icon: ![Light paper rider](assets/items/wm-rider.webp)

  A tiny folded paper flag with a loose soft clip. It can mark one place on the cord without holding it still.
- `wm-tension-key` Tension key
  - icon: ![Tension-adjusting key](assets/items/wm-tension-key.webp)

  A blunt key for the post’s captive adjustment screw. Small turns change the cord’s tension; the marked limits keep the spring within its working stretch.
- `wm-bridge` Bridge
  - icon: ![Movable string bridge](assets/items/wm-bridge.webp)

  A smooth, low wooden bridge with a shallow cord notch. It rests on the soundbox and can slide along the cord to change the length free to vibrate. First tune the unobstructed cord into two broad loops; this extra contact will interrupt that pattern.
- `wm-pick` Pick
  - icon: ![Soft plectrum](assets/items/wm-pick.webp)

  A broad flexible pick for plucking the cord with the motor switched off.
- `wm-marked` Wave machine
  - icon: ![Wave cord with a paper rider](assets/items/wm-marked.webp)

  With the drive running again, the rider bobs around its own place while the disturbance travels past it. A wave can move along the cord without carrying that piece of cord all the way to the other end.
- `wm-looping` Wave machine
  - icon: ![Cord making two broad loops](assets/items/wm-looping.webp)

  You adjust the tension a little at a time and tune the speed. At one setting, two broad loops keep their places, separated by a nearly still point. Disturbances travelling in opposite directions are meeting in a repeating pattern.
- `wm-bridged` Wave machine
  - icon: ![Cord resting on a movable bridge](assets/items/wm-bridged.webp)

  With the drive stopped, you release the bench clips and set the machine freely on its soft feet. Fit the bridge to give the cord another firm contact point: moving it changes the vibrating length and the wave pattern. The bridge passes vibration into the soundbox; the soft feet reduce buzz transmitted to the table.

- `wave-machine` Wave machine
  - icon: ![String-wave machine](assets/items/wave-machine.webp)

  ![String-wave machine in the garden](assets/rewards/wave-machine.webp)

  With the drive off, you tighten the cord within its marked range and pluck it. The soundbox makes the twang easier to hear. Slide the bridge to leave a shorter vibrating length and pluck again: the note rises.

  You lift the complete machine into the garden, with its pick in the parking clip. Restore the earlier tension and speed, park the bridge, and the broad dancing loops return. Jo listens from the pinball chair while you switch the motor off and try a two-note tune.

**Combinations**
- `wm-rider` [consume] + `wm-running` [transform] -> `wm-marked`
- `wm-tension-key` [preserve] + `wm-marked` [transform] -> `wm-looping`
- `wm-bridge` [consume] + `wm-looping` [transform] -> `wm-bridged`
- `wm-pick` [preserve] + `wm-bridged` [transform] -> `wave-machine`


## `c-air-1` A hand at the far end
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pneumatic grabber](assets/items/pneumatic-grabber.webp)

Kit has left a note through the fence: **Can there be a game where you pick things up without touching them?** You set a long light handle on the bench. Jo supplies two wooden jaws. “We could borrow a crab’s idea.”

**Goals**
- Pivot the jaws onto the beam -- `air-jawed`
- next: Fit the slider to the beam -- `air-guided`
- next: Fit the jaw links between the jaws and slider -- `air-linked`
- next: Seat the output syringe in the syringe cradle -- `air-mounted-syringe`
- next: Fit the plunger clip to the slider -- `air-clip-ready`
- next: Mount the output syringe and connect its plunger -- `air-actuated`
- next: Add the return band to open the jaws -- `air-sprung`
- next: Close the jaws around the test block -- `air-hand-grabber`

**Hotspots**
- `air-beam` (center 390px, 500px)
  - icon: ![Grabber beam](assets/hotspots/c-air-1--air-beam.webp)
- `air-jawed` (center 390px, 500px)
  - icon: ![Beam with hinged jaws](assets/hotspots/c-air-1--air-jawed.webp)
- `air-guided` (center 390px, 500px)
  - icon: ![Grabber with a guided slider](assets/hotspots/c-air-1--air-guided.webp)
- `air-linked` (center 390px, 500px)
  - icon: ![Grabber with linked jaws](assets/hotspots/c-air-1--air-linked.webp)
- `air-clip-ready` (center 390px, 500px)
  - icon: ![Grabber with plunger-end clip](assets/hotspots/c-air-1--air-clip-ready.webp)
- `air-actuated` (center 390px, 500px)
  - icon: ![Grabber with an output syringe](assets/hotspots/c-air-1--air-actuated.webp)
- `air-sprung` (center 390px, 500px)
  - icon: ![Grabber with a return band](assets/hotspots/c-air-1--air-sprung.webp)
- `air-hand-grabber` (center 390px, 500px)
  - icon: ![Grabber working by hand](assets/hotspots/c-air-1--air-hand-grabber.webp)

**Items**
- `air-beam` Beam
  - icon: ![Grabber beam](assets/items/air-beam.webp)

  A light wooden beam with a handgrip, prepared jaw pivots at its far end and holes for a slider guide and syringe cradle. Bench clips hold it while you build.
- `air-jaws` Jaws
  - icon: ![Two crab-shaped jaws](assets/items/air-jaws.webp)

  One jaw represents the mirrored pair. Two short wooden levers with rounded gripping ends, hinge washers and captive pivot pins. Their short rear arms will connect to a sliding crosshead.
- `air-slider` Slider
  - icon: ![Slider and straight guide](assets/items/air-slider.webp)

  A smooth crosshead with two link holes, a straight guide rail and captive mounting clips. It moves along the beam without twisting sideways.
- `air-links` Jaw links
  - icon: ![Two separate jaw links](assets/items/air-links.webp)

  One complete link represents the pair. Two short rods with a pivot at each end. They connect the crosshead to the short rear arms of the jaws. Moving the slider forward spreads those rear arms and brings the gripping ends together.
- `air-output-syringe` Output syringe
  - icon: ![Needleless output syringe](assets/items/air-output-syringe.webp)

  A smooth-moving toy syringe with no needle and no liquid. Its plunger starts almost fully in; air entering its nozzle can push the plunger out.
- `air-cradle` Syringe cradle
  - icon: ![Paired syringe-barrel cups](assets/items/air-cradle.webp)

  The strapped rear cup represents the two supplied cups. Two shaped barrel cups with matching captive mounting fasteners. The rear cup has a soft retaining strap bonded to it. Together they support the syringe with its nozzle toward the handle and its plunger toward the jaws.
- `air-plunger-clip` Plunger clip
  - icon: ![Plunger-end clip](assets/items/air-plunger-clip.webp)

  A connected pair of C-shaped jaws on a bridge and central support. It fits the sliding crosshead and captures the broad thumb pad of the output plunger.
- `air-clip-ready` Grabber
  - icon: ![Grabber with plunger-end clip](assets/items/air-clip-ready.webp)
- `air-return-band` Return band
  - icon: ![Light return band](assets/items/air-return-band.webp)

  A soft elastic loop with prepared anchor hooks and a broad peel-and-stick foot for the fixed hook. It pulls the slider back, opening the jaws and returning the output plunger into its barrel.
- `air-test-block` Test block
  - icon: ![Light wooden test block](assets/items/air-test-block.webp)

  A small smooth block to grip and release. It returns to the table after each test.
- `air-jawed` Grabber
  - icon: ![Beam with hinged jaws](assets/items/air-jawed.webp)
- `air-guided` Grabber
  - icon: ![Grabber with a guided slider](assets/items/air-guided.webp)
- `air-linked` Grabber
  - icon: ![Grabber with linked jaws](assets/items/air-linked.webp)

  Slide the crosshead forward and the two links change their angles separately. The short arms spread; the long jaw tips close. As the jaws turn, each link swings on both its pivots.
- `air-mounted-syringe` Output syringe
  - icon: ![Output syringe in its cradle](assets/items/air-mounted-syringe.webp)
- `air-actuated` Grabber
  - icon: ![Grabber with an output syringe](assets/items/air-actuated.webp)
- `air-sprung` Grabber
  - icon: ![Grabber with a return band](assets/items/air-sprung.webp)
- `air-hand-grabber` Grabber
  - icon: ![Grabber working by hand](assets/items/air-hand-grabber.webp)

  You move the crosshead forward with a fingertip. The jaws close around the block. Let go, and the band draws the slider back: the jaws open and the block drops gently onto the bench.

  “Good crab,” says Jo. “Now we need to tell it what to do from the other end.”

**Combinations**
- `air-jaws` [consume] + `air-beam` [transform] -> `air-jawed`
- `air-slider` [consume] + `air-jawed` [transform] -> `air-guided`
- `air-links` [consume] + `air-guided` [transform] -> `air-linked`
- `air-output-syringe` [transform] + `air-cradle` [consume] -> `air-mounted-syringe`
- `air-plunger-clip` [consume] + `air-linked` [transform] -> `air-clip-ready`
- `air-mounted-syringe` [consume] + `air-clip-ready` [transform] -> `air-actuated`
- `air-return-band` [consume] + `air-actuated` [transform] -> `air-sprung`
- `air-test-block` [preserve] + `air-sprung` [transform] -> `air-hand-grabber`

## `c-air-2` A squeeze travels
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Pneumatic grabber](assets/items/pneumatic-grabber.webp)

The jaws wait at the far end of their beam. Jo holds up a length of clear tube. “There will be something inside this,” she says. “Even when it looks empty.”

**Goals**
- Connect the tube to the hand syringe -- `air-control-line`
- next: Connect the tube’s other end to the grabber -- `air-connected`
- next: Squeeze the hand syringe to grip the test block -- `air-squeezing`
- next: Stick the grip pads onto the jaws -- `air-padded`
- next: Fit the syringe holders around the hand syringe -- `air-held`
- next: Fit the tube clips along the beam -- `air-routed`
- next: Pick up the pear with a squeeze -- `pneumatic-grabber`

**Hotspots**
- `air-hand-grabber` (center 390px, 500px)
  - icon: ![Grabber working by hand](assets/hotspots/c-air-2--air-hand-grabber.webp)
- `air-connected` (center 390px, 500px)
  - icon: ![Grabber with an air line](assets/hotspots/c-air-2--air-connected.webp)
- `air-squeezing` (center 390px, 500px)
  - icon: ![Grabber closing from a distance](assets/hotspots/c-air-2--air-squeezing.webp)
- `air-padded` (center 390px, 500px)
  - icon: ![Grabber with soft gripping pads](assets/hotspots/c-air-2--air-padded.webp)
- `air-held` (center 390px, 500px)
  - icon: ![Grabber with supported hand syringe](assets/hotspots/c-air-2--air-held.webp)
- `air-routed` (center 390px, 500px)
  - icon: ![Grabber with a secured air line](assets/hotspots/c-air-2--air-routed.webp)

**Items**
- `air-control-syringe` Hand syringe
  - icon: ![Needleless hand syringe](assets/items/air-control-syringe.webp)

  A matching smooth-moving toy syringe with a broad thumb pad. Its plunger is drawn out to the marked starting line, holding air ready to push through the tube.
- `air-tube` Tube
  - icon: ![Flexible air tube](assets/items/air-tube.webp)

  A clear tube long enough to run from the jaws to the handgrip. Its snug push-fit ends match the two syringe nozzles; it contains air, not water.
- `air-grip-pads` Grip pads
  - icon: ![Soft jaw pads](assets/items/air-grip-pads.webp)

  One pad represents the matching pair. Two thin rubbery pads with peel-off backs. Their surfaces grip a light object without needing a hard squeeze.
- `air-tube-clips` Tube clips
  - icon: ![Air-tube clips](assets/items/air-tube-clips.webp)

  One clip represents the pair. Two gentle C-clips on peel-and-stick feet hold the tube along the beam without flattening it. Leave a loose loop beside the hand syringe.
- `air-hand-holders` Syringe holders
  - icon: ![Hand-syringe holders](assets/items/air-hand-holders.webp)

  One holder represents the supplied pair. A pair of strapped holders with feet shaped for the beam and handgrip. They support the hand syringe while leaving its plunger free for your thumb.
- `air-held` Grabber
  - icon: ![Grabber with supported hand syringe](assets/items/air-held.webp)
- `air-fruit-game` Pear
  - icon: ![Sponge pear](assets/items/air-fruit-game.webp)

  A soft, light pretend pear. Put it beyond easy finger reach, then bring it back with the grabber. Jo has a collecting cup ready in the garden.
- `air-control-line` Hand syringe
  - icon: ![Hand syringe with an air tube](assets/items/air-control-line.webp)
- `air-connected` Grabber
  - icon: ![Grabber with an air line](assets/items/air-connected.webp)

  You fit the tube to the output syringe’s nozzle. Both connections are snug, and the air is enclosed between the two plungers.
- `air-squeezing` Grabber
  - icon: ![Grabber closing from a distance](assets/items/air-squeezing.webp)

  You press the hand syringe. The trapped air compresses a little, then pushes the far plunger out against the return band. The jaws close around the block. The squeeze feels springy; the two plungers do not copy each other’s travel exactly.

  Ease your thumb and let the hand plunger move back: the band opens the jaws. Your hand supplied the push; the air carried it along the tube.
- `air-padded` Grabber
  - icon: ![Grabber with soft gripping pads](assets/items/air-padded.webp)

  The pads spread the contact and add grip. You try the block again: the jaws can hold it with a gentler squeeze, then let it go cleanly.
- `air-routed` Grabber
  - icon: ![Grabber with a secured air line](assets/items/air-routed.webp)
- `pneumatic-grabber` Grabber
  - icon: ![Pneumatic grabber](assets/items/pneumatic-grabber.webp)

  ![Pneumatic grabber in the garden](assets/rewards/pneumatic-grabber.webp)

  You release the beam from its bench clips and lift it by the handgrip. Reach out, squeeze, bring back the sponge pear, ease your thumb: it drops into Jo’s cup. All the syringe parts and tubing travel with the grabber.

  Jo places the pear a little farther away. “The crab requests a longer lunch break.” You put Kit’s note beside the game. This one has its first player waiting already.

**Combinations**
- `air-tube` [consume] + `air-control-syringe` [transform] -> `air-control-line`
- `air-control-line` [consume] + `air-hand-grabber` [transform] -> `air-connected`
- `air-test-block` [preserve] + `air-connected` [transform] -> `air-squeezing`
- `air-grip-pads` [consume] + `air-squeezing` [transform] -> `air-padded`
- `air-hand-holders` [consume] + `air-padded` [transform] -> `air-held`
- `air-tube-clips` [consume] + `air-held` [transform] -> `air-routed`
- `air-fruit-game` [preserve] + `air-routed` [transform] -> `pneumatic-grabber`

## `c-film-1` A drum for a tiny picture show
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Animation drum](assets/items/animation-drum.webp)

Jo finds a strip of blank picture frames while clearing the bench. You draw a fish in the air with your finger: up, over, splash. “Could we make that happen inside a drum?”

**Goals**
- Cut the viewing slits in the drum wall -- `film-slotted`
- next: Tape the drum wall into a cylinder -- `film-cylinder`
- next: Fit the floor inside the drum -- `film-shell`
- next: Fit the turntable onto the base -- `film-turntable`
- next: Set the drum on the base -- `film-turning-drum`

**Hotspots**
- `film-wall` (center 390px, 500px)
  - icon: ![Marked drum-wall strip](assets/hotspots/c-film-1--film-wall.webp)
- `film-slotted` (center 390px, 500px)
  - icon: ![Drum wall with viewing slits](assets/hotspots/c-film-1--film-slotted.webp)
- `film-cylinder` (center 390px, 500px)
  - icon: ![Dark slotted cylinder](assets/hotspots/c-film-1--film-cylinder.webp)
- `film-shell` (center 390px, 500px)
  - icon: ![Drum with a round floor](assets/hotspots/c-film-1--film-shell.webp)
- `film-turning-drum` (center 390px, 500px)
  - icon: ![Turning picture drum](assets/hotspots/c-film-1--film-turning-drum.webp)

**Items**
- `work-scissors` Scissors
  - icon: ![Round-ended scissors](assets/items/work-scissors.webp)

  The scissors cut paper and thin card. They remain a tool after cutting.
- `film-wall` Drum wall
  - icon: ![Marked drum-wall strip](assets/items/film-wall.webp)

  A stiff dark card strip held flat in the bench clips. Twelve evenly spaced slit outlines start at its top edge; a stopping line keeps their lower ends above the picture area. Its lower edge has prepared floor tabs.
- `film-joining-tape` Tape
  - icon: ![Drum seam tape](assets/items/film-joining-tape.webp)

  A strong self-adhesive strip for joining the wall into a cylinder at its marked seam. It leaves all twelve viewing slits clear.
- `film-floor` Floor
  - icon: ![Round drum floor](assets/items/film-floor.webp)

  A light prepared disc with a centred mounting socket and twelve matching tab slots. It keeps the wall round.
- `film-base` Base
  - icon: ![Broad picture-drum base](assets/items/film-base.webp)

  A stable wooden foot with a prepared upright-axle socket and soft pads beneath it.
- `film-bearing` Turntable
  - icon: ![Spindle and turning platform](assets/items/film-bearing.webp)

  A blunt upright axle, sleeve bearing, spacing washers, retaining cap and a small rotating platform. The axle fixes into the base; the platform turns around it and fits the drum floor’s central socket.
- `film-slotted` Drum wall
  - icon: ![Drum wall with viewing slits](assets/items/film-slotted.webp)
- `film-cylinder` Drum
  - icon: ![Dark slotted cylinder](assets/items/film-cylinder.webp)
- `film-shell` Drum
  - icon: ![Drum with a round floor](assets/items/film-shell.webp)
- `film-turntable` Base
  - icon: ![Picture-drum turntable](assets/items/film-turntable.webp)
- `film-turning-drum` Drum
  - icon: ![Turning picture drum](assets/items/film-turning-drum.webp)

  You seat the floor on the platform and give the rim a gentle push. The drum turns around its upright axle while the broad base stays still. Twelve narrow windows pass your eye, one after another.

  Jo peers through a slit. “An excellent picture show about an empty drum.”

**Combinations**
- `work-scissors` [preserve] + `film-wall` [transform] -> `film-slotted`
- `film-joining-tape` [consume] + `film-slotted` [transform] -> `film-cylinder`
- `film-floor` [consume] + `film-cylinder` [transform] -> `film-shell`
- `film-bearing` [consume] + `film-base` [transform] -> `film-turntable`
- `film-turntable` [consume] + `film-shell` [transform] -> `film-turning-drum`

## `c-film-2` A fish that never gets wet
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Animation drum](assets/items/animation-drum.webp)

The drum is ready for a picture show of its own. Your fish will have a crooked tail, a determined nose and twelve chances to get back into the water.

**Goals**
- Use the pencil to draw four fish poses on the picture strip -- `film-key-poses`
- next: Use the fish stencil to fill the in-between frames -- `film-drawn-strip`
- next: Use the colouring pencils to colour the fish and water -- `film-coloured-strip`
- next: Fit the picture strip inside the drum -- `film-loaded-drum`
- next: Set it by the lantern and watch through the slits -- `animation-drum`

**Hotspots**
- `film-turning-drum` (center 390px, 500px)
  - icon: ![Turning picture drum](assets/hotspots/c-film-2--film-turning-drum.webp)
- `film-loaded-drum` (center 390px, 500px)
  - icon: ![Drum with a leaping-fish strip](assets/hotspots/c-film-2--film-loaded-drum.webp)

**Items**
- `film-blank-strip` Picture strip
  - icon: ![Twelve-frame picture strip](assets/items/film-blank-strip.webp)

  A blank strip divided into twelve equal frames, with a waterline across them and a marked overlap tab. It fits inside the drum below the slits, with one frame per slit interval and pictures facing inward.
- `film-pencil` Pencil
  - icon: ![Drawing pencil](assets/items/film-pencil.webp)

  A soft pencil with an eraser for planning the fish’s positions and adjusting the joining frames.
- `film-fish-stencil` Fish stencil
  - icon: ![Crooked-tail fish stencil](assets/items/film-fish-stencil.webp)

  Your original little fish outline cut into a thin reusable stencil. Move it, turn it and trace it with the pencil so the same fish keeps its shape through the jump.
- `film-colours` Colouring pencils
  - icon: ![Bright colouring pencils](assets/items/film-colours.webp)

  Three colouring pencils are supplied; one is shown. Orange for the fish, blue for the water and yellow for one small fin. The same colours will help each pose look like the same creature.
- `film-key-poses` Picture strip
  - icon: ![Strip with four main fish poses](assets/items/film-key-poses.webp)

  In frame one the nose breaks the water. Frame four catches the fish at the top of its leap; frame seven sends it diving down; frame ten holds the spreading ripples. The empty frames are space for the movements between.
- `film-drawn-strip` Picture strip
  - icon: ![Twelve drawings of one fish](assets/items/film-drawn-strip.webp)

  You trace the in-between poses, changing the fish’s position and angle a little at a time. In the last frame its nose waits just below the waterline, ready to meet the first frame again.
- `film-coloured-strip` Picture strip
  - icon: ![Coloured leaping-fish strip](assets/items/film-coloured-strip.webp)
- `film-loaded-drum` Drum
  - icon: ![Drum with a leaping-fish strip](assets/items/film-loaded-drum.webp)
- `animation-drum` Animation drum
  - icon: ![Animation drum](assets/items/animation-drum.webp)

  ![Animation drum in the garden](assets/rewards/animation-drum.webp)

  You lift the finished base from the bench clips and set it beside the lantern. Look over the rim while it turns: the pictures smear past. Lower your eye to the slits, and the orange fish leaps—splash!—then leaps again.

  Each slit gives a brief glimpse of the next drawing, with darkness between. Those separate views let you see a sequence of poses as movement instead of a continuous blur. Turn the drum the other way and the splash gathers itself into a fish.

  You draw the fish once more with a much wider back. “A whale could carry the little stalls on your old plan.” Jo brings the unfinished drawing down from its shelf and makes room beside it for yours.

**Combinations**
- `film-pencil` [preserve] + `film-blank-strip` [transform] -> `film-key-poses`
- `film-fish-stencil` [preserve] + `film-key-poses` [transform] -> `film-drawn-strip`
- `film-colours` [preserve] + `film-drawn-strip` [transform] -> `film-coloured-strip`
- `film-coloured-strip` [consume] + `film-turning-drum` [transform] -> `film-loaded-drum`
- `work-lantern` [preserve] + `film-loaded-drum` [transform] -> `animation-drum`

## `c13` A robot with somewhere to go
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Drawing rover](assets/items/drawing-rover.webp)

On the fourth afternoon, the fair needs invitations. You could draw every one. Or you could make something that draws and then drives over to deliver it.

Jo produces two small gearmotors. “These turn slowly enough to be useful. A very fast motor would mostly deliver itself into a chair.”

**Goals**
- Fit the wheels to the gearmotors -- `rover-drive-pair`
- next: Mount the wheel drives on the deck -- `rover-deck`[`rover-drive-pair`]
- next: Fit the caster to the deck -- `rover-deck`[`rover-caster`]
- next: Mount the battery pack on the deck -- `rover-deck`[`rover-pack`]
- next: Fit the switch harness to the deck -- `rover-deck`[`rover-switch`]
- next: Mount the receiver on the deck -- `rover-deck`[`rover-radio`]
- next: With power off, connect the leads and fit the gear guards -- `guarded-rover`
- next: Put the batteries into the remote -- `rover-powered-remote`
- next: Use the remote to test the wheels -- `rover-tested`

**Hotspots**
- `rover-deck` (center 390px, 500px)
  - icon: ![Rover deck](assets/hotspots/c13--rover-deck.webp)
- `guarded-rover` (center 390px, 500px)
  - icon: ![Guarded rover](assets/hotspots/c13--guarded-rover.webp)
- `rover-tested` (center 390px, 500px)
  - icon: ![Rover with tested wheel drives](assets/hotspots/c13--rover-tested.webp)

**Items**
- `rover-tested` Rover
  - icon: ![Rover with tested wheel drives](assets/items/rover-tested.webp)

  With its wheels raised in the jig, the rover answers the remote: both wheels forward, one wheel faster, both stopped. The batteries provide the energy; radio carries the instructions. You stop the wheels and leave it on the test stops while fitting the pen.
- `rover-remote` Remote
  - icon: ![Matching remote](assets/items/rover-remote.webp)
- `rover-remote-cells` Batteries
  - icon: ![Remote batteries](assets/items/rover-remote-cells.webp)

  Two matching cells are supplied; one is shown. Fit both into the remote’s marked battery compartment.
- `rover-powered-remote` Remote
  - icon: ![Working remote](assets/items/rover-powered-remote.webp)
- `rover-deck` Rover deck (compound)
  - icon: ![Rover deck](assets/items/rover-deck.webp)
  - slot: Caster, accepts `rover-caster`, icon: ![Ball caster](assets/overlays/rover-deck--rover-caster.webp)
  - slot: Wheel drives, accepts `rover-drive-pair`, icon: ![Wheel drives](assets/overlays/rover-deck--rover-drive-pair.webp)
  - slot: Battery, accepts `rover-pack`, icon: ![Rover battery pack](assets/overlays/rover-deck--rover-pack.webp)
  - slot: Switch harness, accepts `rover-switch`, icon: ![Switch harness](assets/overlays/rover-deck--rover-switch.webp)
  - slot: Receiver, accepts `rover-radio`, icon: ![Receiver and motor driver](assets/overlays/rover-deck--rover-radio.webp)

  A little birch platform held upside down in a bench jig. Its upper face already carries the pen’s guide rods, captive top caps, return spring, and its hand-operated lift lever and cam with their brackets and stops. Separate accessible mounting positions accept the caster, drives and electrical modules in any order. Park each connector beside its module, with the spare lead in a loose coil. Keep the switch off until the complete assembly is ready.
- `rover-deck`[`rover-caster`,`rover-drive-pair`]

  Two driven wheels and a free-turning ball will support the deck. Different wheel speeds will turn it; no steering axle is needed.
- `rover-deck`[`rover-radio`]

  The receiver has two separate motor outputs. Once connected, it will control one wheel independently of the other.
- `rover-caster` Caster
  - icon: ![Ball caster](assets/items/rover-caster.webp)
- `rover-gearmotors` Gearmotors
  - icon: ![Matched gearmotors](assets/items/rover-gearmotors.webp)

  One complete geared motor represents the matching left-and-right pair. Two low-voltage motors, reduction gears, brackets and short leads. One drives each side.
- `rover-wheels` Wheels
  - icon: ![Rubber wheels](assets/items/rover-wheels.webp)

  Two matching rubber wheels with their hubs and retained fasteners; one is shown. Fit one to each gearbox output.
- `rover-drive-pair` Wheel drives
  - icon: ![Wheel drives](assets/items/rover-drive-pair.webp)

  Both geared motors now have wheels fitted; one complete drive represents the pair. Each wheel locks to a gearbox output. Inside the supplied gearboxes, fast motor rotation becomes slower wheel rotation with more turning force.
- `rover-pack` Battery pack
  - icon: ![Rover battery pack](assets/items/rover-pack.webp)

  An enclosed low-voltage holder with matching cells already fitted. Its plug matches the fused switch harness.
- `rover-switch` Switch harness
  - icon: ![Switch harness](assets/items/rover-switch.webp)

  A ready-made fused low-voltage harness with an off switch and matching plugs. Keep it off while connecting the battery, receiver and motor leads; switch on only for the guarded drive test.
- `rover-radio` Receiver
  - icon: ![Receiver and motor driver](assets/items/rover-radio.webp)

  The receiver listens to the matching remote. Its motor driver sends the battery's power to the two motors separately.
- `rover-covers` Gear guards
  - icon: ![Gear guards](assets/items/rover-covers.webp)

  Two matching guards are supplied, one for each side; one is shown. Clip-on covers with open shaft slots, split soft cable grommets and tapered split snap pins. They fit around the installed wheel shafts and connected leads.
- `guarded-rover` Rover
  - icon: ![Guarded rover](assets/items/guarded-rover.webp)

  With power off, you connect the supplied harness, battery and two motor leads, then fit the gear covers. Turn the complete rover upright onto its test stops, with both drive wheels clear. Now it is ready for the remote.

**Combinations**
- `rover-wheels` [consume] + `rover-gearmotors` [transform] -> `rover-drive-pair`
- `rover-covers` [consume] @ `rover-deck`[`rover-caster`,`rover-drive-pair`,`rover-pack`,`rover-switch`,`rover-radio`] [transform] -> `guarded-rover`

- `rover-remote-cells` [consume] + `rover-remote` [transform] -> `rover-powered-remote`
- `rover-powered-remote` [preserve] @ `guarded-rover` [transform] -> `rover-tested`

## `c14` Sign your name badly
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Drawing rover](assets/items/drawing-rover.webp)

A clear patch of patio is waiting for the test-paper roll. You have promised Jo a beautifully written invitation.

“I will also accept a magnificent squiggle,” she says.

**Goals**
- Fit the pen into the pen carriage -- `rover-pen-mount`
- next: Slide the pen carriage onto the rover’s guides -- `rover-pen-deck`
- next: Lay out the paper for a driving test -- `rover-looping`
- next: Use the trim screwdriver to straighten the rover’s path -- `rover-trimmed`
- next: Steer with the remote; lift the pen with its hand lever -- `drawing-rover`

**Hotspots**
- `rover-tested` (center 390px, 500px)
  - icon: ![Rover with tested wheel drives](assets/hotspots/c14--rover-tested.webp)
- `rover-pen-deck` (center 390px, 500px)
  - icon: ![Rover with pen](assets/hotspots/c14--rover-pen-deck.webp)
- `rover-looping` (center 390px, 500px)
  - icon: ![Rover drawing a curve](assets/hotspots/c14--rover-looping.webp)
- `rover-trimmed` (center 390px, 500px)
  - icon: ![Trimmed rover](assets/hotspots/c14--rover-trimmed.webp)

**Items**
- `rover-pen` Pen
  - icon: ![Felt-tip pen](assets/items/rover-pen.webp)
- `rover-pen-clip` Pen carriage
  - icon: ![Sliding pen carriage](assets/items/rover-pen-clip.webp)

  A connected spring clip, sliding bridge and follower shoe. The rover’s deck already carries its guide rods and lift lever; this carriage will slide up and down on the rods.
- `rover-pen-mount` Pen carriage
  - icon: ![Pen in its sliding carriage](assets/items/rover-pen-mount.webp)
- `rover-trim-driver` Trim screwdriver
  - icon: ![Small trim screwdriver](assets/items/rover-trim-driver.webp)
- `rover-paper` Paper
  - icon: ![Test-paper roll](assets/items/rover-paper.webp)
- `rover-pen-deck` Rover
  - icon: ![Rover with pen](assets/items/rover-pen-deck.webp)

  With the rover stopped, you release the captive guide caps, slide the carriage onto the rods, seat its return spring and replace the caps. The deck’s hand lever turns a small cam against the follower shoe, raising the pen between drawings.
- `rover-looping` Rover
  - icon: ![Rover drawing a curve](assets/items/rover-looping.webp)

  You unroll a longer length of paper on the patio, release the rover from its test stops, and drive it onto the sheet. With the pen lowered, you drive a long test line. Both wheels turn, but “straight ahead” draws a gentle curve. One motor is a little quicker. You lift the pen and steer aside to inspect the whole trail. The receiver has a trim adjustment for just this problem.
- `rover-trimmed` Rover
  - icon: ![Trimmed rover](assets/items/rover-trimmed.webp)

  With the rover stopped and its pen raised, you give the trim screw a small turn. You steer to a fresh strip of paper, lower the pen, and drive another long line. Then you lift the pen and park beside the marks. The straighter second line shows how the adjustment has brought the wheel speeds together.
- `drawing-rover` Rover
  - icon: ![Drawing rover](assets/items/drawing-rover.webp)

  ![Drawing rover in the garden](assets/rewards/drawing-rover.webp)

  The two test lines stay on the paper. You stop the rover and raise its pen with the hand lever, then use the remote to steer to a fresh patch. Stop, lower the lever, and drive a ridiculous looping whale. You stop once more, raise the pen by hand, and park beside the paper. Jo writes **YOU ARE INVITED** inside the whale.

**Combinations**
- `rover-pen` [consume] + `rover-pen-clip` [transform] -> `rover-pen-mount`
- `rover-pen-mount` [consume] @ `rover-tested` [transform] -> `rover-pen-deck`
- `rover-paper` [consume] @ `rover-pen-deck` [transform] -> `rover-looping`
- `rover-trim-driver` [preserve] @ `rover-looping` [transform] -> `rover-trimmed`
- `rover-powered-remote` [preserve] @ `rover-trimmed` [transform] -> `drawing-rover`

## `c15` Put the night in a box
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Star theatre](assets/items/shadow-theatre.webp)

Your paper whale needs stars. Real ones are inconveniently far away.

The next box has a low-power lamp, a turning handle and room for a miniature night sky. First, you need to find out what its shadows actually look like.

**Goals**
- Line the box with the reflector foil -- `theatre-lined`
- next: Fit the lamp inside the box -- `theatre-lit-box`
- next: Connect the battery pack to the lamp -- `theatre-powered-box`
- next: Use the star punch on the card disc -- `theatre-stars`
- next: Fit the star disc onto the disc spindle -- `theatre-shadow-wheel`
- next: Mount the star wheel inside the box -- `theatre-wheel-box`

**Hotspots**
- `theatre-box` (center 390px, 500px)
  - icon: ![Theatre box](assets/hotspots/c15--theatre-box.webp)
- `theatre-lined` (center 390px, 500px)
  - icon: ![Reflective theatre box](assets/hotspots/c15--theatre-lined.webp)
- `theatre-lit-box` (center 390px, 500px)
  - icon: ![Theatre with lamp](assets/hotspots/c15--theatre-lit-box.webp)
- `theatre-powered-box` (center 390px, 500px)
  - icon: ![Powered theatre](assets/hotspots/c15--theatre-powered-box.webp)
- `theatre-wheel-box` (center 390px, 500px)
  - icon: ![Theatre with star wheel](assets/hotspots/c15--theatre-wheel-box.webp)
- `theatre-blurry` (center 390px, 500px)
  - icon: ![Blurry star theatre](assets/hotspots/c15--theatre-blurry.webp)

**Items**
- `theatre-box` Box
  - icon: ![Theatre box](assets/items/theatre-box.webp)

  A prepared box with a removable lid, a projection opening and a fixed internal window. You lay the lid beside it, inside face up, while fitting the parts.
- `theatre-foil` Reflector foil
  - icon: ![Reflective lining](assets/items/theatre-foil.webp)
- `theatre-lamp` Lamp
  - icon: ![LED lamp module](assets/items/theatre-lamp.webp)

  A small cool-running diffused LED module in a holder, with its current-limiting resistor already fitted. It matches the supplied low-voltage battery and later accessory outlet.
- `theatre-power` Battery pack
  - icon: ![Switched lamp supply](assets/items/theatre-power.webp)

  A compatible enclosed low-voltage battery pack with its fused lead and on-off switch already fitted. A pad, side keeper and strap hold the pack. Connect to the lamp with the switch off; turn on for the projection test. Its lead unplugs when the theatre moves onto the whale.
- `theatre-card` Card disc
  - icon: ![Black card disc](assets/items/theatre-card.webp)

  A prepared black card disc with a matching flat-sided central hole.
- `theatre-punch` Star punch
  - icon: ![Star hole punch](assets/items/theatre-punch.webp)

  Slide the card edge into its narrow mouth and press the star-marked button. Each press cuts a little window for the light.
- `theatre-stars` Star disc
  - icon: ![Star disc](assets/items/theatre-stars.webp)
- `theatre-spindle` Disc spindle
  - icon: ![Disc spindle](assets/items/theatre-spindle.webp)

  A six-millimetre spindle with two bushed supports, two flat-sided disc clamping collars with captive locking screws, mounting screws and an exposed shaft end for a detachable handwheel or drive pulley.
- `theatre-shadow-wheel` Star wheel
  - icon: ![Shadow wheel](assets/items/theatre-shadow-wheel.webp)
- `theatre-lined` Box
  - icon: ![Reflective theatre box](assets/items/theatre-lined.webp)

  The bright lining sends some otherwise lost light back toward the star disc. Its foil is kept clear of the electrical contacts. One strip lines the lid; the other two stay along the sides.
- `theatre-lit-box` Box
  - icon: ![Theatre with lamp](assets/items/theatre-lit-box.webp)
- `theatre-powered-box` Box
  - icon: ![Powered theatre](assets/items/theatre-powered-box.webp)
- `theatre-wheel-box` Star box
  - icon: ![Theatre with star wheel](assets/items/theatre-wheel-box.webp)

  The spindle holds the disc between the lamp and the front opening. Light passes through its little holes; turning the disc will move those patches of light.
- `theatre-blurry` Projector
  - icon: ![Blurry star theatre](assets/items/theatre-blurry.webp)

  You replace the lid and switch on the lamp. Pale blobs of light spread across the screen. They are not yet stars.

**Combinations**
- `theatre-foil` [consume] @ `theatre-box` [transform] -> `theatre-lined`
- `theatre-lamp` [consume] @ `theatre-lined` [transform] -> `theatre-lit-box`
- `theatre-power` [consume] @ `theatre-lit-box` [transform] -> `theatre-powered-box`
- `theatre-card` [transform] + `theatre-punch` [preserve] -> `theatre-stars`
- `theatre-stars` [consume] + `theatre-spindle` [transform] -> `theatre-shadow-wheel`
- `theatre-shadow-wheel` [consume] @ `theatre-powered-box` [transform] -> `theatre-wheel-box`

## `c16` The stars come out early
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Star theatre](assets/items/shadow-theatre.webp)

At dusk, you hang a white cloth between the apple trees. Your stars ought to be big enough for everyone to see.

Jo holds the box while you look for a sharp image. “A blurry universe has its charms. Let's try a focused one.”

**Goals**
- Fit the lens into the lens holder -- `theatre-focus`
- next: Mount the lens holder on the star box
  - either: `theatre-focus-ready`
  - or: `theatre-focus-box`
- next: Try the projector on the screen
  - either: `theatre-blurry`
  - or: `theatre-focus-box`
- next: Fit the hood to block stray light -- `theatre-hooded`
- next: Fit and turn the star-wheel handle -- `shadow-theatre`

**Hotspots**
- `theatre-wheel-box` (center 390px, 500px)
  - icon: ![Theatre with star wheel](assets/hotspots/c16--theatre-wheel-box.webp)
- `theatre-blurry` (center 390px, 500px)
  - icon: ![Blurry star theatre](assets/hotspots/c16--theatre-blurry.webp)
- `theatre-focus-box` (center 390px, 500px)
  - icon: ![Projector with focusing lens](assets/hotspots/c16--theatre-focus-box.webp)
- `theatre-focus-ready` (center 390px, 500px)
  - icon: ![Projector ready for its screen](assets/hotspots/c16--theatre-focus-ready.webp)
- `theatre-hooded` (center 390px, 500px)
  - icon: ![Hooded star projector](assets/hotspots/c16--theatre-hooded.webp)
**Items**
- `theatre-lens` Lens
  - icon: ![Convex projection lens](assets/items/theatre-lens.webp)
- `theatre-slider` Lens holder
  - icon: ![Sliding lens holder](assets/items/theatre-slider.webp)

  Its grooved carriage runs on two fixed rails through prepared wall openings. Sliding it a little forward or back brings the image into focus.
- `theatre-focus` Lens holder
  - icon: ![Adjustable lens assembly](assets/items/theatre-focus.webp)
- `theatre-hood` Hood
  - icon: ![Dark lens hood](assets/items/theatre-hood.webp)
- `theatre-handwheel` Star-wheel handle
  - icon: ![Star-wheel handle](assets/items/theatre-handwheel.webp)

  A detachable handwheel with a matching flat-sided socket and retaining clip. Remove it before fitting the belt pulley.
- `theatre-cloth` Screen
  - icon: ![Hanging projection cloth](assets/items/theatre-cloth.webp)
- `theatre-focus-ready` Projector
  - icon: ![Projector ready for its screen](assets/items/theatre-focus-ready.webp)

  With the lens carriage fitted, you replace the lid before trying the screen. Its slider will let you compare a blurry setting with a sharp one.
- `theatre-focus-box` Projector
  - icon: ![Projector with focusing lens](assets/items/theatre-focus-box.webp)

  With the cloth in place, you slide the lens from a blurry setting to a sharp one. Sliding the lens changes where the star disc forms a sharp image. This is a projector: the light passes through the holes, then the lens forms their image on the cloth.
- `theatre-hooded` Projector
  - icon: ![Hooded star projector](assets/items/theatre-hooded.webp)

  The hood catches stray light around the lens. The projected dark spaces become darker, so the stars stand out.
- `shadow-theatre` Projector
  - icon: ![Star theatre](assets/items/shadow-theatre.webp)

  ![Star theatre in the garden](assets/rewards/shadow-theatre.webp)

  You turn the handle. Stars drift across the cloth as new holes move through the light. The image is upside down; for your invented constellations, that is entirely acceptable.

  You put the projector beside the drawing Jo has kept for years. “Your dragon could ride here,” you say, pointing to the front deck. “And this could put stars over everyone.”

  Jo lays the rover’s wobbly whale beside your animation drawing. “Your fish has grown into its new job.”

**Combinations**
- `theatre-cloth` [preserve] @ `theatre-wheel-box` [transform] -> `theatre-blurry`
- `theatre-lens` [consume] + `theatre-slider` [transform] -> `theatre-focus`
- `theatre-focus` [consume] @ `theatre-blurry` [transform] -> `theatre-focus-box`
- `theatre-focus` [consume] @ `theatre-wheel-box` [transform] -> `theatre-focus-ready`
- `theatre-cloth` [preserve] @ `theatre-focus-ready` [transform] -> `theatre-focus-box`
- `theatre-hood` [consume] @ `theatre-focus-box` [transform] -> `theatre-hooded`
- `theatre-handwheel` [consume] @ `theatre-hooded` [transform] -> `shadow-theatre`

## `c17` The thing that should not happen
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Lift test stand](assets/items/lift-ready.webp)

“I could build every part except the flying,” Jo says. “Then my friend sent this.”

Inside a padded tin is a violet tile. **Experimental lift tile. Apply power to lift. Disconnect to stop.**

This part is invented science. Real batteries cannot make a tile ignore gravity. In this workshop, this one can. You still have to find out how much it lifts—and keep hold of it.

**Goals**
- Attach the tether to the test base -- `lift-tethered-base`
- next: Fit the guide posts to the test base -- `lift-guided-base`
- next: Fit the crossbars to the cradle -- `lift-guided-cradle`
- next: Seat the lift tile in its cradle -- `lift-cradled-tile`
- next: Connect the test switch to the battery pack -- `lift-switched-pack`
- next: Slide the lift tile down the guide posts -- `lift-seated`
- next: Fit the top nuts to retain the cradle -- `lift-ready`
- next: Connect the battery pack and test the lift -- `lift-rising`
- next: Add the test weight and compare the lift -- `lift-load-tested`

**Hotspots**
- `lift-base` (center 390px, 500px)
  - icon: ![Test-stand base](assets/hotspots/c17--lift-base.webp)
- `lift-tethered-base` (center 390px, 500px)
  - icon: ![Tethered test base](assets/hotspots/c17--lift-tethered-base.webp)
- `lift-guided-base` (center 390px, 500px)
  - icon: ![Stand with bare guide posts](assets/hotspots/c17--lift-guided-base.webp)
- `lift-seated` (center 390px, 500px)
  - icon: ![Cradled tile on the guide posts](assets/hotspots/c17--lift-seated.webp)
- `lift-ready` (center 390px, 500px)
  - icon: ![Tile in test stand](assets/hotspots/c17--lift-ready.webp)
- `lift-rising` (center 390px, 500px)
  - icon: ![Rising tile stand](assets/hotspots/c17--lift-rising.webp)
- `lift-load-tested` (center 390px, 500px)
  - icon: ![Loaded lift test](assets/hotspots/c17--lift-load-tested.webp)

**Items**
- `lift-base` Test base
  - icon: ![Test-stand base](assets/items/lift-base.webp)
- `lift-posts` Guide posts
  - icon: ![Four bare guide posts](assets/items/lift-posts.webp)

  Four matching guide posts are supplied; one is shown. Fit their lower ends to the test base. Their top threads remain bare until the cradle is on the stand.
- `lift-tether` Tether
  - icon: ![Short safety tether](assets/items/lift-tether.webp)
- `lift-tile` Lift tile
  - icon: ![Experimental lift tile](assets/items/lift-tile.webp)

  A violet tile in a protective rim. In this invented technology its force points upward, even if the tile tilts. The force is limited and lasts only while powered; the tile does not make electricity.
- `lift-pack` Battery pack
  - icon: ![Tile battery pack](assets/items/lift-pack.webp)
- `lift-switch` Test switch
  - icon: ![Spring-return test switch](assets/items/lift-switch.webp)
- `lift-switched-pack` Battery pack
  - icon: ![Hold-to-lift supply](assets/items/lift-switched-pack.webp)
- `lift-cradle` Cradle
  - icon: ![Tile cradle with hanging supports](assets/items/lift-cradle.webp)

  The tile sits in a padded upper frame. Four short rigid supports join it to a lower frame with a battery shelf; the slotted tray fits onto that frame. The weight hangs below the point providing lift. Closed lifting eyes leave room for the crane sling.
- `lift-guide-crossbars` Crossbars
  - icon: ![Two guide crossbars](assets/items/lift-guide-crossbars.webp)

  Two matching crossbars are supplied; one is shown. Each connects its two guide rings and frame clamps. Clamp them to the cradle’s lower frame before sliding the rings onto the posts.
- `lift-post-nuts` Top nuts
  - icon: ![Four guide-post top nuts](assets/items/lift-post-nuts.webp)

  Four matching top nuts are supplied; one is shown. After seating the cradle, fit one to each post to keep its guide rings from sliding off the top.
- `lift-guided-cradle` Cradle
  - icon: ![Cradle with guide crossbars](assets/items/lift-guided-cradle.webp)
- `lift-seated` Lift stand
  - icon: ![Cradled tile on the guide posts](assets/items/lift-seated.webp)
- `lift-cradled-tile` Lift tile
  - icon: ![Cradled lift tile](assets/items/lift-cradled-tile.webp)
- `lift-weight` Test weight
  - icon: ![Test weight](assets/items/lift-weight.webp)
- `lift-tethered-base` Test base
  - icon: ![Tethered test base](assets/items/lift-tethered-base.webp)
- `lift-guided-base` Test stand
  - icon: ![Stand with bare guide posts](assets/items/lift-guided-base.webp)

  The four guide posts are fixed to the tethered base. Keep their tops clear so the cradle’s guide rings can slide down them.
- `lift-ready` Lift stand
  - icon: ![Tile in test stand](assets/items/lift-ready.webp)
- `lift-rising` Lift stand
  - icon: ![Rising tile stand](assets/items/lift-rising.webp)

  You hold the switch. The tile rises until the short tether catches it. Let go, and it settles back onto the padded base. It has no propeller and no balloon. Jo laughs once, very loudly.
- `lift-load-tested` Lift stand
  - icon: ![Loaded lift test](assets/items/lift-load-tested.webp)

  With the weight clipped beneath it, the tile rises more slowly. The battery must now support the tile, the cradle and the extra weight. The test is small; the grin is not.

**Combinations**
- `lift-tether` [consume] @ `lift-base` [transform] -> `lift-tethered-base`
- `lift-posts` [consume] @ `lift-tethered-base` [transform] -> `lift-guided-base`
- `lift-guide-crossbars` [consume] + `lift-cradle` [transform] -> `lift-guided-cradle`
- `lift-tile` [consume] + `lift-guided-cradle` [transform] -> `lift-cradled-tile`
- `lift-switch` [consume] + `lift-pack` [transform] -> `lift-switched-pack`
- `lift-cradled-tile` [consume] @ `lift-guided-base` [transform] -> `lift-seated`
- `lift-post-nuts` [consume] @ `lift-seated` [transform] -> `lift-ready`
- `lift-switched-pack` [consume] @ `lift-ready` [transform] -> `lift-rising`
- `lift-weight` [consume] @ `lift-rising` [transform] -> `lift-load-tested`

## `c18` Up is the easy part
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Balanced lift module](assets/items/balanced-lift.webp)

The tile lifts. A fair also needs to come down where you want it.

You set out a tray, a sliding weight and a control unit that can vary the current. The tile stays on its short tether throughout the experiment.

**Goals**
- Fit the tray to the lift module -- `lift-tray-test`
- next: Put the test load off-centre on the tray -- `lift-tilting-test`
- next: Fit and adjust the counterweight -- `lift-balanced-test`
- next: Connect the lift control -- `lift-variable-test`
- next: Fit and test the emergency stop -- `lift-stop-test`
- next: Fit the lifting sling to the crane -- `lift-supported-module`
- next: Use the crane to lift out the lift module -- `balanced-lift`

**Hotspots**
- `lift-load-tested` (center 390px, 500px)
  - icon: ![Loaded lift test](assets/hotspots/c18--lift-load-tested.webp)
- `lift-tray-test` (center 390px, 500px)
  - icon: ![Tile with load tray](assets/hotspots/c18--lift-tray-test.webp)
- `lift-tilting-test` (center 390px, 500px)
  - icon: ![Tilting lift tray](assets/hotspots/c18--lift-tilting-test.webp)
- `lift-balanced-test` (center 390px, 500px)
  - icon: ![Level lift tray](assets/hotspots/c18--lift-balanced-test.webp)
- `lift-variable-test` (center 390px, 500px)
  - icon: ![Adjustable lift module](assets/hotspots/c18--lift-variable-test.webp)
- `lift-stop-test` (center 390px, 500px)
  - icon: ![Stopped lift module](assets/hotspots/c18--lift-stop-test.webp)

**Items**
- `lift-tray` Tray
  - icon: ![Slotted load tray](assets/items/lift-tray.webp)

  The tray has front and rear counterweight slots, clear passages for the battery holder and four support holes.
- `lift-offset-load` Test load
  - icon: ![Off-centre test block](assets/items/lift-offset-load.webp)
- `lift-slider` Counterweight
  - icon: ![Sliding counterweight](assets/items/lift-slider.webp)

  A shoe runs beneath the slot. Loosen the finger screw to slide the weight, then tighten it to hold the new position. A matching socket accepts the temporary adjustment handle.
- `lift-control` Lift control
  - icon: ![Current controller and replacement harness](assets/items/lift-control.webp)

  The new harness replaces the hold-to-lift test switch. Its dial varies the lift smoothly and its plug accepts a long control lead. Disconnect the battery before changing harnesses.
- `lift-stop` Emergency stop
  - icon: ![Latching power-cut switch](assets/items/lift-stop.webp)
- `lift-crane-sling` Lifting sling
  - icon: ![Short lifting sling](assets/items/lift-crane-sling.webp)
- `lift-tray-test` Lift module
  - icon: ![Tile with load tray](assets/items/lift-tray-test.webp)
- `lift-tilting-test` Lift module
  - icon: ![Tilting lift tray](assets/items/lift-tilting-test.webp)

  The tray's loaded end dips. Upward force alone does not keep a lopsided load level.
- `lift-balanced-test` Lift module
  - icon: ![Level lift tray](assets/items/lift-balanced-test.webp)

  The counterweight slides away from the heavy end until the tray hangs level. The total load is greater, so it now needs a little more lift.
- `lift-variable-test` Lift module
  - icon: ![Adjustable lift module](assets/items/lift-variable-test.webp)
- `lift-stop-test` Lift module
  - icon: ![Stopped lift module](assets/items/lift-stop-test.webp)

  The big switch cuts the tile's power even while the controller asks for lift. The short tether and padded base keep this a gentle test. With the controller at zero, you disconnect the battery and reset the latched stop before moving the module.
- `lift-supported-module` Crane
  - icon: ![Crane with lifting sling](assets/items/lift-supported-module.webp)

  You unhook its cargo basket and leave that on the bench, then clip the sling to the crane's closed hook.
- `balanced-lift` Lift module
  - icon: ![Balanced lift module](assets/items/balanced-lift.webp)

  ![Balanced lift module in the garden](assets/rewards/balanced-lift.webp)

  The crane takes the weight while you undo the stand's wingnuts. You unclip the guide crossbars and leave them with the stand. The two test blocks stay on the bench, and you centre the counterweight in the front slot for the empty tray. You release the stand tether and lift out one complete module: tile above, tray and battery below, with counterweight, controller and stop switch. The old test switch stays with the stand.

**Combinations**
- `lift-tray` [consume] @ `lift-load-tested` [transform] -> `lift-tray-test`
- `lift-offset-load` [consume] @ `lift-tray-test` [transform] -> `lift-tilting-test`
- `lift-slider` [consume] @ `lift-tilting-test` [transform] -> `lift-balanced-test`
- `lift-control` [consume] @ `lift-balanced-test` [transform] -> `lift-variable-test`
- `lift-stop` [consume] @ `lift-variable-test` [transform] -> `lift-stop-test`
- `lift-crane-sling` [consume] + `lifting-crane` [transform] -> `lift-supported-module`
- `lift-supported-module` [preserve] @ `lift-stop-test` [transform] -> `balanced-lift`

**Items**
**Hotspots**
## `c19` A whale without a sea
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Whale with its lift module](assets/items/whale-lift-fitted.webp)

You put your rover's whale drawing beside Jo's old plan. Hers has more measurements. Yours has a much better smile.

The flying fair will be the size of a large model boat. No passengers. Plenty of room for a dragon.

**Goals**
- Fit the ribs along the keel -- `whale-ribbed`
- next: Fit the top spar through the ribs -- `whale-spined`
- next: Attach the tail to the back of the whale frame -- `whale-tailed`
- next: Fit the deck across the ribs -- `whale-decked`
- next: Join the brace cords with the tensioners -- `whale-braces`
- next: Tension the braces across the whale frame -- `whale-braced-frame`

**Hotspots**
- `whale-keel` (center 390px, 500px)
  - icon: ![Whale keel](assets/hotspots/c19--whale-keel.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-ribbed` (center 390px, 500px)
  - icon: ![Ribbed whale frame](assets/hotspots/c19--whale-ribbed.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-spined` (center 390px, 500px)
  - icon: ![Whale frame with upper spar](assets/hotspots/c19--whale-spined.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-tailed` (center 390px, 500px)
  - icon: ![Tailed whale frame](assets/hotspots/c19--whale-tailed.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-decked` (center 390px, 500px)
  - icon: ![Whale frame with deck](assets/hotspots/c19--whale-decked.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-braced-frame` (center 390px, 500px)
  - icon: ![Braced whale frame](assets/hotspots/c19--whale-braced-frame.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)

**Items**
- `whale-keel` Keel
  - icon: ![Whale keel](assets/items/whale-keel.webp)

  A long light wooden spine, clamped flat in the building jig.
- `whale-ribs` Ribs
  - icon: ![Slotted ribs](assets/items/whale-ribs.webp)

  Eight numbered ribs are shaped for their places along the keel; the drawing shows one central rib. One rib takes a stiff detour around the service opening. A strong frame should still leave room to reach its workings.
- `whale-top-spar` Top spar
  - icon: ![Upper spar](assets/items/whale-top-spar.webp)
- `whale-tail` Tail
  - icon: ![Light whale tail](assets/items/whale-tail.webp)

  Two light panels joined to a rigid root that slots into the keel. It is a fixed tail, not a steering mechanism.
- `whale-deck` Deck
  - icon: ![Slatted fair deck](assets/items/whale-deck.webp)

  A light prepared deck on two crosspieces, with mounting holes for the attractions.
- `whale-brace-cord` Brace cords
  - icon: ![Measured brace cords](assets/items/whale-brace-cord.webp)

  Sixteen measured cord lengths form eight short-and-long pairs; one length is shown. Each pair will join through a tensioner to make a diagonal brace.
- `whale-tensioners` Tensioners
  - icon: ![Brace tensioners](assets/items/whale-tensioners.webp)

  Eight matching tensioners are supplied; one is shown. Each joins a pair of cord lengths and adjusts the finished brace.
- `whale-braces` Braces
  - icon: ![Adjustable diagonal braces](assets/items/whale-braces.webp)

  Eight complete diagonal braces are ready; one is shown. Each has two cord runs joined by its tensioner and end loops for the ribs. Fit the full set across the frame’s two sides.
- `whale-ribbed` Whale frame
  - icon: ![Ribbed whale frame](assets/items/whale-ribbed.webp)
- `whale-spined` Whale frame
  - icon: ![Whale frame with upper spar](assets/items/whale-spined.webp)
- `whale-tailed` Whale frame
  - icon: ![Tailed whale frame](assets/items/whale-tailed.webp)
- `whale-decked` Whale frame
  - icon: ![Whale frame with deck](assets/items/whale-decked.webp)

  The deck spreads each attraction’s weight across several ribs. It is a platform with a route for forces to reach the frame, not a loose floor resting on paper.
- `whale-braced-frame` Whale frame
  - icon: ![Braced whale frame](assets/items/whale-braced-frame.webp)

  The diagonal cords stop the rectangles leaning into diamonds. You can see straight through the whale and still recognize it.

**Combinations**
- `whale-ribs` [consume] @ `whale-keel` [transform] -> `whale-ribbed`
- `whale-top-spar` [consume] @ `whale-ribbed` [transform] -> `whale-spined`
- `whale-tail` [consume] @ `whale-spined` [transform] -> `whale-tailed`
- `whale-deck` [consume] @ `whale-tailed` [transform] -> `whale-decked`
- `whale-brace-cord` [consume] + `whale-tensioners` [transform] -> `whale-braces`
- `whale-braces` [consume] @ `whale-decked` [transform] -> `whale-braced-frame`

## `c20` Leave room for the workings
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Whale with its lift module](assets/items/whale-lift-fitted.webp)

You could wrap the whole whale beautifully and discover afterwards that its switch was inside.

Work from the hatch side. Fit the lift module while the ribs are open, then add the skin and service hatch. The useful bits will stay reachable. The small detail view shows where the outside stop button fits.

**Goals**
- Fit the extension struts to the lift module -- `lift-extended`
- next: Reconnect the lift module with the harness extension -- `lift-reconnected`
- next: Fit the fork saddles against the top spar -- `whale-mounted`
- next: Seat the lift module beneath the fork saddles -- `whale-lift-resting`
- next: Secure the lift module with the retaining straps -- `whale-lift-inside`
- next: Fit the skin around the whale frame -- `whale-skinned`
- next: Fit the hatch -- `whale-hatched`
- next: Fit the button guide -- `whale-stop-guided`
- next: Slide the stop button’s pushrod through the button guide -- `whale-lift-fitted`

**Hotspots**
- `whale-braced-frame` (center 390px, 500px)
  - icon: ![Braced whale frame](assets/hotspots/c20--whale-braced-frame.webp)
- `whale-skinned` (center 390px, 500px)
  - icon: ![Paper-skinned whale](assets/hotspots/c20--whale-skinned.webp)
- `whale-hatched` (center 390px, 500px)
  - icon: ![Whale with service hatch](assets/hotspots/c20--whale-hatched.webp)
- `whale-lift-resting` (center 390px, 500px)
  - icon: ![Lift module seated beneath the whale forks](assets/hotspots/c20--whale-lift-resting.webp)
- `whale-mounted` (center 390px, 500px)
  - icon: ![Whale with supporting forks](assets/hotspots/c20--whale-mounted.webp)
- `whale-stop-guided` (center 390px, 500px)
  - icon: ![Whale with stop-button guide](assets/hotspots/c20--whale-stop-guided.webp)
- `whale-lift-fitted` (center 390px, 500px)
  - icon: ![Whale with outside stop button](assets/hotspots/c20--whale-lift-fitted.webp)

**Items**
- `whale-skin` Skin
  - icon: ![Cut translucent paper skin](assets/items/whale-skin.webp)

  Light blue panels with two stiffened fins already attached and an opening over the service bay. The fin rods and panel tabs clip directly to the ribs. The fins give the whale its silhouette; they make no lift. A prepared cable grommet beside the service opening lets the two insulated ground leads leave without catching in the closed hatch.
- `whale-hatch` Hatch
  - icon: ![Hinged service hatch](assets/items/whale-hatch.webp)

  A light surround with its hinged paper door, rib brackets and latch already attached. It opens over the controller and counterweight; the outside stop guide fits beside it.
- `whale-module-mount` Extension struts
  - icon: ![Four lift-extension struts](assets/items/whale-module-mount.webp)

  Four complete extension struts are supplied; one is shown. Each extension strut has a locking sleeve and captive cross-pins. With the complete lift module supported and disconnected, fit them between its original short supports and lower frame. Move the same counterweight to the marked rear tray slot; Jo keeps the module supported while you work.
- `whale-stop-extension` Stop button
  - icon: ![Outside stop button and pushrod](assets/items/whale-stop-extension.webp)

  A red exterior button joined to its pushrod. Slide the rod through the fitted guide to meet the lift module’s stop switch.
- `whale-harness-extension` Harness extension
  - icon: ![Lift-module harness extension](assets/items/whale-harness-extension.webp)

  A measured insulated lead with two inline connectors. It bridges the gap between the original controller lead and tile lead without stretching either. Keep the battery disconnected while fitting it.
- `whale-forks` Fork saddles
  - icon: ![Paired supporting forks](assets/items/whale-forks.webp)

  One complete fork represents the pair. Two rigid U-shaped fork saddles, each with two legs and a crosshead. The crossheads bear against the whale’s upper spar while their feet receive the lift cradle.
- `whale-retaining-straps` Retaining straps
  - icon: ![Module retaining straps](assets/items/whale-retaining-straps.webp)

  One strap represents the pair. Two prepared retaining straps, each one continuous piece. They retain the original upper cradle against the fork saddles after the module is seated.
- `whale-stop-guide` Button guide
  - icon: ![Stop-button guide bracket](assets/items/whale-stop-guide.webp)

  A pushrod guide with its support flange and rib bracket. It mounts beside the hatch, keeping the button’s pushrod lined up with the module’s stop switch.
- `lift-extended` Lift module
  - icon: ![Lift module with extended supports](assets/items/lift-extended.webp)

  The original supports keep their lengths; the four extra struts bridge the gap to the lower frame. The same battery and counterweight remain on the lower tray, with the counterweight in its marked rear slot. The short electrical leads now need their extension.
- `lift-reconnected` Lift module
  - icon: ![Extended lift module with connected harness](assets/items/lift-reconnected.webp)

  The added lead joins both original connectors without pulling on either. The complete module remains supported and disconnected while Jo helps fit it beneath the fork saddles.
- `whale-lift-resting` Whale
  - icon: ![Lift module seated beneath the whale forks](assets/items/whale-lift-resting.webp)

  The tile cradle meets the forks beneath the upper spar; the battery and counterweight hang low. Jo keeps the assembly supported while you fit the retaining straps.
- `whale-stop-guided` Whale
  - icon: ![Whale with stop-button guide](assets/items/whale-stop-guided.webp)
- `whale-skinned` Whale
  - icon: ![Paper-skinned whale](assets/items/whale-skinned.webp)

  The blue panels bow into a belly. Light shines through the two fins. A frame for carrying things has become a whale.

  “It looks as if it is waiting for the sea,” says Jo. You point upward.
- `whale-hatched` Whale
  - icon: ![Whale with service hatch](assets/items/whale-hatched.webp)

  The hatch opens over the controller and counterweight. Closing it finishes the shape without sealing away the things you will need to adjust.
- `whale-mounted` Whale frame
  - icon: ![Whale with supporting forks](assets/items/whale-mounted.webp)

  The two fork crossheads bear against the upper spar. Jo supports them while the prepared lift cradle is seated beneath their feet.
- `whale-lift-inside` Whale
  - icon: ![Whale carrying lift module](assets/items/whale-lift-inside.webp)
- `whale-lift-fitted` Whale
  - icon: ![Whale with outside stop button](assets/items/whale-lift-fitted.webp)

  The violet tile is secured beneath the upper spar, above the fair deck. Its battery and counterweight sit low in the service bay, so the whale's weight hangs below the lift. A pushrod links the red exterior button to the module's stop switch.

**Hotspots**
- `whale-lift-inside` (center 390px, 500px)
  - icon: ![Whale carrying lift module](assets/hotspots/c20--whale-lift-inside.webp)

**Combinations**
- `whale-module-mount` [consume] + `balanced-lift` [transform] -> `lift-extended`
- `whale-harness-extension` [consume] + `lift-extended` [transform] -> `lift-reconnected`
- `whale-forks` [consume] @ `whale-braced-frame` [transform] -> `whale-mounted`
- `lift-reconnected` [consume] @ `whale-mounted` [transform] -> `whale-lift-resting`
- `whale-retaining-straps` [consume] @ `whale-lift-resting` [transform] -> `whale-lift-inside`
- `whale-skin` [consume] @ `whale-lift-inside` [transform] -> `whale-skinned`
- `whale-hatch` [consume] @ `whale-skinned` [transform] -> `whale-hatched`
- `whale-stop-guide` [consume] @ `whale-hatched` [transform] -> `whale-stop-guided`
- `whale-stop-extension` [consume] @ `whale-stop-guided` [transform] -> `whale-lift-fitted`

## `c21` The dragon gets a ticket
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Working fair whale](assets/items/whale-running-fair.webp)

The dragon fits the front deck. It has been practising its wave all afternoon.

The star theatre will ride behind it. Every ordinary part still has a job; the strange tile only holds the whole thing up.

**Goals**
- Fit the dragon bracket to the deck -- `whale-dragon-seat`
- next: Secure the crank dragon on the dragon bracket -- `whale-dragon-aboard`
- next: Fit the projector bracket to the deck -- `whale-theatre-seat`
- next: Secure the projector on the projector bracket -- `whale-theatre-aboard`
- next: Fit the switch dock beneath the deck -- `whale-switch-docked`
- next: Fit the accessory supply and connect the projector’s lamp -- `whale-loaded`

**Hotspots**
- `whale-lift-fitted` (center 390px, 500px)
  - icon: ![Whale with outside stop button](assets/hotspots/c21--whale-lift-fitted.webp)
- `whale-dragon-seat` (center 390px, 500px)
  - icon: ![Whale with dragon mount](assets/hotspots/c21--whale-dragon-seat.webp)
- `whale-dragon-aboard` (center 390px, 500px)
  - icon: ![Whale with dragon aboard](assets/hotspots/c21--whale-dragon-aboard.webp)
- `whale-theatre-seat` (center 390px, 500px)
  - icon: ![Whale with theatre mount](assets/hotspots/c21--whale-theatre-seat.webp)
- `whale-theatre-aboard` (center 390px, 500px)
  - icon: ![Whale with both attractions](assets/hotspots/c21--whale-theatre-aboard.webp)
- `whale-switch-docked` (center 390px, 500px)
  - icon: ![Whale with an accessory-switch dock](assets/hotspots/c21--whale-switch-docked.webp)
- `whale-loaded` (center 390px, 500px)
  - icon: ![Loaded fair whale](assets/hotspots/c21--whale-loaded.webp)

**Items**
- `fair-dragon-bracket` Dragon bracket
  - icon: ![Dragon mounting sections](assets/items/fair-dragon-bracket.webp)

  Four shaped mounting sections with four captive pins form two matching pairs. One long section is shown. The long and short sections leave room for the crosspiece; their cable clips leave the flat-sided crank fitting clear.
- `fair-theatre-bracket` Projector bracket
  - icon: ![Theatre mounting spreaders](assets/items/fair-theatre-bracket.webp)

  Two matching mounting spreaders are supplied; one is shown. Their captive locking pins and cable clips hold the theatre level, with its spindle parallel to the motor shaft. Aim by placing the screen across the light path.
- `fair-switch-dock` Switch dock
  - icon: ![Accessory-switch parking dock](assets/items/fair-switch-dock.webp)

  A small teal parking plate on a short support arm. It mounts under the deck to hold the wired accessory switch.
- `fair-power-divider` Accessory supply
  - icon: ![Fused accessory supply](assets/items/fair-power-divider.webp)

  A separate compatible battery pack with two fused, switched low-voltage outlets and matching lamp and motor connectors. With both supplies off, disconnect and remove the theatre’s old battery before connecting its lamp here. Its shelf and straps hold the new pack, and its clipped lamp cable passes through the prepared deck and theatre-floor openings. The lift tile keeps its own supply.
- `whale-dragon-seat` Whale
  - icon: ![Whale with dragon mount](assets/items/whale-dragon-seat.webp)
- `whale-dragon-aboard` Whale
  - icon: ![Whale with dragon aboard](assets/items/whale-dragon-aboard.webp)

  The same mounting holes from the little bench toy fit the deck bracket. Its follower, both pivoting links and the spare cam all come aboard with it. Jo checks that the wings can still complete their sweep.
- `whale-theatre-seat` Whale
  - icon: ![Whale with theatre mount](assets/items/whale-theatre-seat.webp)
- `whale-theatre-aboard` Whale
  - icon: ![Whale with both attractions](assets/items/whale-theatre-aboard.webp)

  The projector sits behind the dragon, with its lens pointing clear of the wings. The two attractions need their own space to work, not just enough space to fit. With both supplies off, Jo opens the service hatch. Keep it open while you fit the parking dock and connect the accessory supply underneath the deck.
- `whale-switch-docked` Whale
  - icon: ![Whale with an accessory-switch dock](assets/items/whale-switch-docked.webp)
- `whale-loaded` Whale
  - icon: ![Loaded fair whale](assets/items/whale-loaded.webp)

  The dragon's crank fitting and the theatre's spindle still turn freely. Their hand handles are parked in the workshop. The bracket clips hold wires away from both; a motor will need an actual connection to each shaft.

**Hotspots**
**Combinations**
- `fair-dragon-bracket` [consume] @ `whale-lift-fitted` [transform] -> `whale-dragon-seat`
- `crank-dragon` [consume] @ `whale-dragon-seat` [transform] -> `whale-dragon-aboard`
- `fair-theatre-bracket` [consume] @ `whale-dragon-aboard` [transform] -> `whale-theatre-seat`
- `shadow-theatre` [consume] @ `whale-theatre-seat` [transform] -> `whale-theatre-aboard`
- `fair-switch-dock` [consume] @ `whale-theatre-aboard` [transform] -> `whale-switch-docked`
- `fair-power-divider` [consume] @ `whale-switch-docked` [transform] -> `whale-loaded`

## `c22` Who turns the handles?
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Working fair whale](assets/items/whale-running-fair.webp)

Jo closes the service hatch. You hold up a hand underneath the whale.

“Excellent,” says Jo. “Now imagine it another metre higher.”

The handles need a slow motor. The dragon and the stars want different speeds.

**Goals**
- Mount the drive motor -- `whale-motor-fitted`
- next: Fit the crank coupler between the motor and dragon -- `whale-dragon-driven`
- next: Fit the reduction drive for the projector -- `whale-theatre-driven`
- next: Fit the drive guard -- `whale-drive-guarded`
- next: Use the accessory switch to run the attractions -- `whale-running-fair`

**Hotspots**
- `whale-loaded` (center 390px, 500px)
  - icon: ![Loaded fair whale](assets/hotspots/c22--whale-loaded.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-motor-fitted` (center 390px, 500px)
  - icon: ![Whale with accessory motor](assets/hotspots/c22--whale-motor-fitted.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-dragon-driven` (center 390px, 500px)
  - icon: ![Motor-driven dragon whale](assets/hotspots/c22--whale-dragon-driven.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-theatre-driven` (center 390px, 500px)
  - icon: ![Whale with slower star wheel](assets/hotspots/c22--whale-theatre-driven.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)
- `whale-drive-guarded` (center 390px, 500px)
  - icon: ![Guarded fair drive](assets/hotspots/c22--whale-drive-guarded.webp)
  - hitbox: (center 390.000px, 500.264px) (size 518.138px, 384.782px)

**Items**
- `fair-mounted-motor` Drive motor
  - icon: ![Clutched motor assembly](assets/items/fair-mounted-motor.webp)

  A slow gearmotor in a bracket, with a slip clutch and an extended keyed output. The small belt pulley fits behind the flexible dragon coupler on the same shaft. The prepared saddle has an open channel for its attached lead: lower the motor and lead into place together. Its plug matches the accessory supply; connect with both switches off.
- `fair-dragon-coupler` Crank coupler
  - icon: ![Flexible crank coupler](assets/items/fair-dragon-coupler.webp)

  A short flexible coupling with flat pressure shoes and captive clamp screws at both ends. Tightened against the shaft flats, the shoes carry the turning force and hold the coupling in place. Release the screws to draw the shoes clear and slide the coupling along the round shaft.
- `fair-reduction` Reduction drive
  - icon: ![Reducing belt-drive set](assets/items/fair-reduction.webp)

  A small pulley for the motor shaft, a larger pulley for the theatre spindle, and their matching soft belt. With power off, release both coupling shoes, slide the coupler off the motor shaft and park it farther along the dragon’s shaft. Fit the small keyed pulley and tighten its retaining screw, then restore the coupler and tighten both shoes. The large flat-sided pulley, spacers and cross-pin replace the theatre handwheel. The mounted shafts stay parallel; the larger pulley turns more slowly.
- `fair-guard` Drive guard
  - icon: ![Clear drive cover](assets/items/fair-guard.webp)

  A prepared clear hood with open rear channels for the ribs, braces and supports, two deck lugs, and guided captive screws. With power off, draw both screws back to their stops. Slide the hood rearward until its guide tubes seat against the deck lugs, then tighten the screws. The hood encloses the belt and turning shafts while fitting around the stationary motor case.
- `fair-accessory-switch` Accessory switch
  - icon: ![Wired accessory master switch](assets/items/fair-accessory-switch.webp)

  A removable low-voltage wired switch with a matching plug. It docks below the deck for the bench test, then plugs into the garden panel’s extension lead. It controls only the accessory supply.
- `whale-motor-fitted` Whale
  - icon: ![Whale with accessory motor](assets/items/whale-motor-fitted.webp)
- `whale-dragon-driven` Whale
  - icon: ![Motor-driven dragon whale](assets/items/whale-dragon-driven.webp)
- `whale-theatre-driven` Whale
  - icon: ![Whale with slower star wheel](assets/items/whale-theatre-driven.webp)

  The small pulley pulls the belt past the large pulley. The large pulley takes longer to go round, so the stars drift while the dragon waves briskly.
- `whale-drive-guarded` Whale
  - icon: ![Guarded fair drive](assets/items/whale-drive-guarded.webp)
- `whale-running-fair` Whale
  - icon: ![Working fair whale](assets/items/whale-running-fair.webp)

  One switch: the dragon gives two wing-waves per turn, and stars crawl over the workshop wall. The clutch slips gently if you hold the dragon still. You switch everything off before the lifting test.

**Combinations**
- `fair-mounted-motor` [consume] @ `whale-loaded` [transform] -> `whale-motor-fitted`
- `fair-dragon-coupler` [consume] @ `whale-motor-fitted` [transform] -> `whale-dragon-driven`
- `fair-reduction` [consume] @ `whale-dragon-driven` [transform] -> `whale-theatre-driven`
- `fair-guard` [consume] @ `whale-theatre-driven` [transform] -> `whale-drive-guarded`
- `fair-accessory-switch` [preserve] @ `whale-drive-guarded` [transform] -> `whale-running-fair`

**Items**
## `c23` The first flight is ten centimetres
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Tethered flying fair](assets/items/whale-garden-ready.webp)

The whale is complete enough to be dangerous to its own paper nose. So its first flight will stay within ten centimetres of a padded landing cradle.

The two attractions have moved the weight. The balance that worked for an empty tray will not do.

**Goals**
- Clip on the test tether -- `whale-short-tethered`
- next: Set the whale in the landing cradle -- `whale-ready-low`
- next: Connect the lift lead for a low test -- `whale-nose-down`
- next: Land and adjust the counterweight with the counterweight handle -- `whale-trimmed`
- next: Use the bubble level to test a level hover -- `whale-hovering-low`
- next: Land, fit the stop cord’s lever, then hover and pull the cord -- `whale-low-tested`

**Hotspots**
- `whale-running-fair` (center 390px, 480px)
  - icon: ![Working fair whale](assets/hotspots/c23--whale-running-fair.webp)
- `whale-short-tethered` (center 390px, 480px)
  - icon: ![Whale on low tether](assets/hotspots/c23--whale-short-tethered.webp)
- `whale-ready-low` (center 390px, 480px)
  - icon: ![Whale resting in its cradle](assets/hotspots/c23--whale-ready-low.webp)
- `whale-nose-down` (center 390px, 480px)
  - icon: ![Nose-heavy hovering whale](assets/hotspots/c23--whale-nose-down.webp)
- `whale-trimmed` (center 390px, 480px)
  - icon: ![Rebalanced fair whale](assets/hotspots/c23--whale-trimmed.webp)
- `whale-hovering-low` (center 390px, 480px)
  - icon: ![Level low-hovering whale](assets/hotspots/c23--whale-hovering-low.webp)

**Items**
- `flight-short-tether` Test tether
  - icon: ![Low test tether](assets/items/flight-short-tether.webp)

  A short line with a frame clip and weighted anchor, limiting this first lift to ten centimetres.
- `flight-mat` Landing cradle
  - icon: ![Padded landing cradle](assets/items/flight-mat.webp)

  A broad padded tray with two crossbars, thick felt where the keel rests and side braces that splay out clear of the hull. The tray catches the short emergency-stop test.
- `flight-control-lead` Lift lead
  - icon: ![Long lift-control lead](assets/items/flight-control-lead.webp)

  Jo lays its spare length in a broad loose loop on the ground, clear of the landing cradle. The same lead will reach the whale at full height.
- `flight-trim-handle` Counterweight handle
  - icon: ![Counterweight adjustment handle](assets/items/flight-trim-handle.webp)

  First lower the whale into its cradle, turn the lift control to zero and disconnect the battery. Then open the hatch to reach the counterweight. Fit the handle, make the loaded whale’s adjustment, then withdraw it before closing the hatch. For the full tray adjustment or a change between its slots, remove the handle and move the weight by hand with the supported module outside the skin.
- `flight-level` Bubble level
  - icon: ![Bubble level](assets/items/flight-level.webp)
- `flight-stop-cord` Stop cord
  - icon: ![Stop cord with pivoted lever](assets/items/flight-stop-cord.webp)

  A bracket and right-angle lever fit beside the exterior stop button. Pulling the cord turns the lever and presses the button. A return spring brings the lever back when released.
- `whale-short-tethered` Whale
  - icon: ![Whale on low tether](assets/items/whale-short-tethered.webp)
- `whale-ready-low` Whale
  - icon: ![Whale resting in its cradle](assets/items/whale-ready-low.webp)

  The keel settles into the felt-lined cradle while the fins and tail stay clear. Even an impossible flying machine needs somewhere ordinary to land.
- `whale-nose-down` Whale
  - icon: ![Nose-heavy hovering whale](assets/items/whale-nose-down.webp)

  Just clear of the cradle, the dragon end dips. The lift works, but the fair's weight is uneven. Jo steadies the line while you reach for the dial.
- `whale-trimmed` Whale
  - icon: ![Rebalanced fair whale](assets/items/whale-trimmed.webp)

  Back in the cradle, with the power off, you use the handle to slide the counterweight away from the dragon end. Jo watches through the open hatch. “Let’s ask it again.”
- `whale-hovering-low` Whale
  - icon: ![Level low-hovering whale](assets/items/whale-hovering-low.webp)

  Handle out; hatch shut. You reconnect the battery and raise the current. The bubble sits between its marks. The whale lifts evenly, its short tether taut. The ordinary counterweight has solved a problem the extraordinary tile could not.
- `whale-low-tested` Whale
  - icon: ![Low-tested whale](assets/items/whale-low-tested.webp)

  You lower the whale into the cradle, set the controller to zero and disconnect the battery. With Jo supporting the hull, you fit the stop-cord bracket beside the exterior button and check that its pivoted lever presses it freely. You reconnect the battery and repeat the low hover above the cradle. Pulling the cord presses the exterior stop button and cuts lift immediately. The whale drops the short test distance into the padded cradle. This emergency stop is different from a landing: to land gently, you turn the current down gradually. With the controller at zero and the battery disconnected, you reset the latched stop for the next flight.

**Combinations**
- `flight-short-tether` [consume] @ `whale-running-fair` [transform] -> `whale-short-tethered`
- `flight-mat` [consume] @ `whale-short-tethered` [transform] -> `whale-ready-low`
- `flight-control-lead` [consume] @ `whale-ready-low` [transform] -> `whale-nose-down`
- `flight-trim-handle` [preserve] @ `whale-nose-down` [transform] -> `whale-trimmed`
- `flight-level` [preserve] @ `whale-trimmed` [transform] -> `whale-hovering-low`
- `flight-stop-cord` [consume] @ `whale-hovering-low` [transform] -> `whale-low-tested`

## `c24` A place to come home
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Tethered flying fair](assets/items/whale-garden-ready.webp)

The garden has a tree, a fence and a great many places where you do not want a paper whale.

You choose the clear patch beside the cloth screen. Three separate tether lines will limit height and stop the whale turning away from its audience. Jo will handle the lines while you lower it into its cradle.

**Goals**
- Fit the garden tethers -- `whale-garden-tethered`
- next: Set the screen stand in the projector’s light path -- `whale-aimed`
- next: Connect the control panel -- `whale-garden-ready`

**Hotspots**
- `whale-low-tested` (center 390px, 480px)
  - icon: ![Low-tested whale](assets/hotspots/c24--whale-low-tested.webp)
- `whale-garden-tethered` (center 390px, 480px)
  - icon: ![Whale on garden tether](assets/hotspots/c24--whale-garden-tethered.webp)
- `whale-aimed` (center 390px, 480px)
  - icon: ![Whale aimed at garden screen](assets/hotspots/c24--whale-aimed.webp)

**Items**
- `flight-long-tether` Garden tethers
  - icon: ![Three-line garden tether rig](assets/items/flight-long-tether.webp)

  Three complete tether units are supplied; one is shown. Each measured line joins a weighted ground anchor to a frame clip. Replace the short test line with all three. At full height they are taut: they limit drift and turning as well as height, and stay below the branches.
- `flight-screen-stand` Screen stand
  - icon: ![Adjustable garden-screen stand](assets/items/flight-screen-stand.webp)

  A broad-footed stand for the existing cloth screen. Its telescoping posts and captive clips let you place the cloth squarely across the projector’s sideways light path without tilting the belt-driven theatre.
- `flight-rehearsal-remote` Control panel
  - icon: ![Tether-side control panel](assets/items/flight-rehearsal-remote.webp)

  The panel includes a long low-voltage accessory extension lead and a socket for the same wired accessory master switch, plus the lift-control connection. The two supplies remain electrically separate. Jo lays the two leads and the separate stop cord in their own loose loops, leaving enough length for the rise and keeping the controls within reach.
- `whale-garden-tethered` Whale
  - icon: ![Whale on garden tether](assets/items/whale-garden-tethered.webp)

  Three separate lines run from the frame to broad weighted anchors around the landing place. They limit both its height and its wanderings; none crosses the projector’s light path. You leave the whale resting in its cradle while fitting the screen.
- `whale-aimed` Whale
  - icon: ![Whale aimed at garden screen](assets/items/whale-aimed.webp)

  You fit the cloth to its stand beside the clear flight space. Jo measures the projector’s height at full tether length, and you raise the screen to meet it. The theatre stays level with its motor, so the belt remains straight.
- `whale-garden-ready` Whale
  - icon: ![Garden-ready flying fair](assets/items/whale-garden-ready.webp)

  With the whale still in its cradle, you find the lift dial with one hand and the accessory switch with the other. The separate red stop cord stays within reach. You check the three lines and the clear path to the cloth. Jo takes the handling lines. The complete airborne show can wait until the guests are here.

**Combinations**
- `flight-long-tether` [consume] @ `whale-low-tested` [transform] -> `whale-garden-tethered`
- `flight-screen-stand` [consume] @ `whale-garden-tethered` [transform] -> `whale-aimed`
- `flight-rehearsal-remote` [consume] @ `whale-aimed` [transform] -> `whale-garden-ready`

## `c25` Can I have a go?
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Tethered flying fair](assets/items/whale-garden-ready.webp)

The gate clicks. Kit has brought biscuits and the very serious cardboard hat.

Kit takes the promised first turn with the wind racer, then uses the crab grabber to fetch a sponge pear. “This is exactly the ridiculous game I wanted.”

The pinball marble clicks past its arches. Somebody looks through the periscope; somebody else is still turning the kaleidoscope. A paper rider dances on the wave machine. Fish leap round and round inside the animation drum.

“One last invitation,” you tell the rover. Jo stands at the whale's control panel, trying to look as if this happens every Saturday.

**Goals**
- Have the rover draw on the banner -- `fair-written-banner`
- next: Hang the banner on the landing cradle -- `fair-bannered`
- next: Use the accessory switch to start the dragon and projector -- `fair-whale-alight`
- next: Use the lift key and open the flying fair -- `fair-in-the-air`

**Hotspots**
- `whale-garden-ready` (center 390px, 480px)
  - icon: ![Garden-ready flying fair](assets/hotspots/c25--whale-garden-ready.webp)
- `fair-bannered` (center 390px, 480px)
  - icon: ![Whale with welcome banner](assets/hotspots/c25--fair-bannered.webp)
- `fair-whale-alight` (center 390px, 480px)
  - icon: ![Whale with its attractions running](assets/hotspots/c25--fair-whale-alight.webp)
- `fair-in-the-air` (center 390px, 480px)
  - icon: ![A fair in the air](assets/hotspots/c25--fair-in-the-air.webp)

**Items**
- `fair-bannered` Whale
  - icon: ![Whale with welcome banner](assets/items/fair-bannered.webp)

  You hang the banner along the front of the grounded cradle, clear of the fins and tether lines. The two controls are ready beside it.
- `fair-rover-paper` Banner
  - icon: ![Long welcome banner](assets/items/fair-rover-paper.webp)
- `fair-written-banner` Banner
  - icon: ![Rover-drawn welcome banner](assets/items/fair-written-banner.webp)

  The rover makes the border in glorious loops. You write WELCOME in the middle. Kit adds a whale with a cardboard hat.
- `fair-start-key` Lift key
  - icon: ![Lift-control key](assets/items/fair-start-key.webp)

  The removable key enables the ground controller. Turn its dial up gradually; the separate red stop cord remains reachable.
- `fair-whale-alight` Whale
  - icon: ![Whale with its attractions running](assets/items/fair-whale-alight.webp)

  You turn on the accessory supply. The dragon waves; the star disc turns inside its lamp-lit box. Now for the part of Jo's drawing that never worked.
- `fair-in-the-air` Flying fair
  - icon: ![A fair in the air](assets/items/fair-in-the-air.webp)

  ![A fair in the air in the garden](assets/rewards/fair-in-the-air.webp)

  The whale lifts clear of its cradle. Stars climb onto the waiting cloth. Its three tethers tighten. The little dragon waves above the garden, beneath a sky it has brought along itself.

  Kit looks up. Then at the control panel.

  “Can I have a go?”

  You make room beside you. “Start with the dragon.” Jo is laughing, looking from the whale to her old drawing and back again. “Mine never got off the paper.”

**Combinations**
- `drawing-rover` [preserve] + `fair-rover-paper` [transform] -> `fair-written-banner`
- `fair-written-banner` [consume] @ `whale-garden-ready` [transform] -> `fair-bannered`
- `fair-accessory-switch` [preserve] @ `fair-bannered` [transform] -> `fair-whale-alight`
- `fair-start-key` [preserve] @ `fair-whale-alight` [transform] -> `fair-in-the-air`

## `c26` Yours to make
background: ![White instruction page](assets/backgrounds/white.svg)

The fair runs until the last biscuit disappears. Then you turn down the lift while Jo guides the lines, switch off both supplies, and leave the whale sleeping in its cradle.

The rover is parked beside its very bad whale drawing. The dragon has stopped mid-wave. Inside its frame, you can still follow every link back to the cam.

The lift tile belongs to this story. The other mechanisms are real ideas to explore—with suitable materials, tools and help.

On the bench is an empty box. You have already started looking at it differently.
