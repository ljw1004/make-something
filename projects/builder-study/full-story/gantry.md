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
- `gh-side-1` Side frame
  - icon: ![Side frame](assets/items/gh-side-1.webp)

  ---

  A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.

- `gh-side-2` Side frame
  - icon: ![Side frame](assets/items/gh-side-2.webp)

  ---

  A prepared triangular frame with joined braces and captive foot pegs. Either frame fits either side of the base.

- `gh-crossbeam` Beam
  - icon: ![Beam](assets/items/gh-crossbeam.webp)

  ---

  The beam has two end sockets and separate sockets underneath for the pulley forks.

- `gh-one-side` Frame
  - icon: ![Frame](assets/items/gh-one-side.webp)
- `gh-two-sides` Frame
  - icon: ![Frame](assets/items/gh-two-sides.webp)
- `gh-frame` Frame
  - icon: ![Frame](assets/items/gh-frame.webp)
- `gh-drum` Winch
  - icon: ![Winch](assets/items/gh-drum.webp)

  ---

  The winch drum comes with its axle, two bearing cheeks, captive base fasteners and a sprung cord clamp.

- `gh-ratchet` Ratchet
  - icon: ![Ratchet](assets/items/gh-ratchet.webp)
- `gh-crank` Crank
  - icon: ![Crank](assets/items/gh-crank.webp)
- `gh-ratchet-winch` Winch
  - icon: ![Winch](assets/items/gh-ratchet-winch.webp)
- `gh-crank-winch` Winch
  - icon: ![Winch](assets/items/gh-crank-winch.webp)
- `gh-winch` Winch
  - icon: ![Winch](assets/items/gh-winch.webp)
- `gh-mounted` Gantry
  - icon: ![Gantry](assets/items/gh-mounted.webp)

**Combinations**
- `gh-base` [transform] + `gh-side-1` [consume] -> `gh-one-side`
- `gh-base` [transform] + `gh-side-2` [consume] -> `gh-one-side`
- `gh-one-side` [transform] + `gh-side-1` [consume] -> `gh-two-sides`
- `gh-one-side` [transform] + `gh-side-2` [consume] -> `gh-two-sides`
- `gh-two-sides` [transform] + `gh-crossbeam` [consume] -> `gh-frame`
- `gh-drum` [transform] + `gh-ratchet` [consume] -> `gh-ratchet-winch`
- `gh-drum` [transform] + `gh-crank` [consume] -> `gh-crank-winch`
- `gh-ratchet-winch` [transform] + `gh-crank` [consume] -> `gh-winch`
- `gh-crank-winch` [transform] + `gh-ratchet` [consume] -> `gh-winch`
- `gh-frame` [transform] + `gh-winch` [consume] -> `gh-mounted`

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

  ---

  An open pulley bracket with a split snap axle and a barbed mounting stem. Press a pulley over the axle tip, then push the stem through the beam until its head opens above the wood.

- `gh-side-pulley` Pulley unit
  - icon: ![Pulley unit](assets/items/gh-side-pulley.webp)
- `gh-drop-fork` Drop fork
  - icon: ![Drop fork](assets/items/gh-drop-fork.webp)

  ---

  An open pulley bracket with a split snap axle and a barbed mounting stem. Press a pulley over the axle tip, then push the stem through the beam until its head opens above the wood.

- `gh-drop-pulley` Pulley unit
  - icon: ![Pulley unit](assets/items/gh-drop-pulley.webp)
- `gh-pulley-1` Pulley
  - icon: ![Pulley](assets/items/gh-pulley-1.webp)

  ---

  A grooved pulley that turns on either fork axle. The split axle tip retains it.

- `gh-pulley-2` Pulley
  - icon: ![Pulley](assets/items/gh-pulley-2.webp)

  ---

  A grooved pulley that turns on either fork axle. The split axle tip retains it.

- `gh-pawl` Pawl
  - icon: ![Pawl](assets/items/gh-pawl.webp)

  ---

  A spring pawl and its connected mounting foot. Its tooth rests in the ratchet so the drum cannot freely unwind.

- `gh-rope` Rope and hook
  - icon: ![Rope and hook](assets/items/gh-rope.webp)

  ---

  One continuous cord, already tied to its hook. Push its free end under the drum’s prepared spring clamp, wind one turn, then thread it over the two pulleys.

- `gh-basket` Basket
  - icon: ![Basket](assets/items/gh-basket.webp)

  ---

  A small rigid basket with a connected lifting handle. It hangs directly on the hook.

- `gh-fitted-1` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-1.webp)
- `gh-fitted-2` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-2.webp)
- `gh-fitted-3` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-3.webp)
- `gh-fitted-4` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-4.webp)
- `gh-fitted-5` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-5.webp)
- `gh-fitted-6` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-6.webp)
- `gh-fitted-7` Gantry
  - icon: ![Gantry](assets/items/gh-fitted-7.webp)
- `gh-roped` Hoist
  - icon: ![Hoist](assets/items/gh-roped.webp)
- `gantry-hoist` Gantry hoist
  - icon: ![Gantry hoist](assets/items/gantry-hoist.webp)

  ---

  Two fixed pulleys guide the cord; they change its direction without multiplying the lifting force. Turning the crank winds the drum. The pawl holds the drum between turns.


**Combinations**
- `gh-side-fork` [transform] + `gh-pulley-1` [consume] -> `gh-side-pulley`
- `gh-side-fork` [transform] + `gh-pulley-2` [consume] -> `gh-side-pulley`
- `gh-drop-fork` [transform] + `gh-pulley-1` [consume] -> `gh-drop-pulley`
- `gh-drop-fork` [transform] + `gh-pulley-2` [consume] -> `gh-drop-pulley`
- `gh-mounted` [transform] + `gh-side-pulley` [consume] -> `gh-fitted-1`
- `gh-mounted` [transform] + `gh-drop-pulley` [consume] -> `gh-fitted-2`
- `gh-mounted` [transform] + `gh-pawl` [consume] -> `gh-fitted-4`
- `gh-fitted-1` [transform] + `gh-drop-pulley` [consume] -> `gh-fitted-3`
- `gh-fitted-1` [transform] + `gh-pawl` [consume] -> `gh-fitted-5`
- `gh-fitted-2` [transform] + `gh-side-pulley` [consume] -> `gh-fitted-3`
- `gh-fitted-2` [transform] + `gh-pawl` [consume] -> `gh-fitted-6`
- `gh-fitted-3` [transform] + `gh-pawl` [consume] -> `gh-fitted-7`
- `gh-fitted-4` [transform] + `gh-side-pulley` [consume] -> `gh-fitted-5`
- `gh-fitted-4` [transform] + `gh-drop-pulley` [consume] -> `gh-fitted-6`
- `gh-fitted-5` [transform] + `gh-drop-pulley` [consume] -> `gh-fitted-7`
- `gh-fitted-6` [transform] + `gh-side-pulley` [consume] -> `gh-fitted-7`
- `gh-fitted-7` [transform] + `gh-rope` [consume] -> `gh-roped`
- `gh-roped` [transform] + `gh-basket` [consume] -> `gantry-hoist`
