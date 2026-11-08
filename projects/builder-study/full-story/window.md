## `c-window-foot` A broad foot
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Window base](assets/items/wn-foot-ready.webp)

**Goals**
- Fit a foot
  - either: `wn-one-foot`
  - or: `wn-right-foot`
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
  - icon: ![Base](assets/items/wn-base.webp)
- `wn-foot-1` Left foot
  - icon: ![Left foot](assets/items/wn-foot-1.webp)
- `wn-foot-2` Right foot
  - icon: ![Right foot](assets/items/wn-foot-2.webp)
- `wn-battery` Battery
  - icon: ![Battery](assets/items/wn-battery.webp)
- `wn-switch` Switch
  - icon: ![Switch](assets/items/wn-switch.webp)
- `wn-block` Block
  - icon: ![Block](assets/items/wn-block.webp)
- `wn-sill` Sill
  - icon: ![Sill](assets/items/wn-sill.webp)
- `wn-one-foot` Base
  - icon: ![Base](assets/items/wn-one-foot.webp)
- `wn-right-foot` Base
  - icon: ![Base](assets/items/wn-right-foot.webp)
- `wn-two-feet` Base
  - icon: ![Base](assets/items/wn-two-feet.webp)
- `wn-fitted-1` Window base
  - icon: ![Window base](assets/items/wn-fitted-1.webp)
- `wn-fitted-2` Window base
  - icon: ![Window base](assets/items/wn-fitted-2.webp)
- `wn-fitted-3` Window base
  - icon: ![Window base](assets/items/wn-fitted-3.webp)
- `wn-fitted-4` Window base
  - icon: ![Window base](assets/items/wn-fitted-4.webp)
- `wn-fitted-5` Window base
  - icon: ![Window base](assets/items/wn-fitted-5.webp)
- `wn-fitted-6` Window base
  - icon: ![Window base](assets/items/wn-fitted-6.webp)
- `wn-fitted-7` Window base
  - icon: ![Window base](assets/items/wn-fitted-7.webp)
- `wn-fitted-8` Window base
  - icon: ![Window base](assets/items/wn-fitted-8.webp)
- `wn-fitted-9` Window base
  - icon: ![Window base](assets/items/wn-fitted-9.webp)
- `wn-fitted-10` Window base
  - icon: ![Window base](assets/items/wn-fitted-10.webp)
- `wn-fitted-11` Window base
  - icon: ![Window base](assets/items/wn-fitted-11.webp)
- `wn-fitted-12` Window base
  - icon: ![Window base](assets/items/wn-fitted-12.webp)
- `wn-fitted-13` Window base
  - icon: ![Window base](assets/items/wn-fitted-13.webp)
- `wn-fitted-14` Window base
  - icon: ![Window base](assets/items/wn-fitted-14.webp)
- `wn-foot-ready` Window base
  - icon: ![Window base](assets/items/wn-foot-ready.webp)
  - from chapter `c-window-frame` icon: ![Window base](assets/items/wn-base-carried.webp)

**Combinations**
- `wn-foot-1` [consume] + `wn-base` [transform] -> `wn-one-foot`
- `wn-foot-2` [consume] + `wn-base` [transform] -> `wn-right-foot`
- `wn-foot-2` [consume] + `wn-one-foot` [transform] -> `wn-two-feet`
- `wn-foot-1` [consume] + `wn-right-foot` [transform] -> `wn-two-feet`
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
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Window](assets/items/open-window.webp)

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
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `wn-upright-1` Upright
  - icon: ![Upright](assets/items/wn-upright-1.webp)
- `wn-upright-2` Upright
  - icon: ![Upright](assets/items/wn-upright-2.webp)
- `wn-top` Crossbar
  - icon: ![Crossbar](assets/items/wn-top.webp)
- `wn-strut-1` Strut
  - icon: ![Strut](assets/items/wn-strut-1.webp)
- `wn-strut-2` Strut
  - icon: ![Strut](assets/items/wn-strut-2.webp)
- `wn-lead` Lead
  - icon: ![Lead](assets/items/wn-lead.webp)
- `wn-one-upright` Window
  - icon: ![Window](assets/items/wn-one-upright.webp)
- `wn-uprights` Window
  - icon: ![Window](assets/items/wn-uprights.webp)
- `wn-frame` Window
  - icon: ![Window](assets/items/wn-frame.webp)
- `wn-back` Window
  - icon: ![Window](assets/items/wn-back.webp)
- `wn-one-strut` Window
  - icon: ![Window](assets/items/wn-one-strut.webp)
- `wn-braced-back` Window
  - icon: ![Window](assets/items/wn-braced-back.webp)
- `wn-braced` Window
  - icon: ![Window](assets/items/wn-braced.webp)
- `open-window` Window
  - icon: ![Window](assets/items/open-window.webp)
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
