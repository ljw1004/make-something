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

  ---

  Prepared plywood with rail slots, flipper holes and integral carrying handles.
- `bf-pb-left-rail` Left rail
  - icon: ![Left rail](assets/items/bf-pb-left-rail.webp)
- `bf-pb-rail-1` Table
  - icon: ![Table](assets/items/bf-pb-rail-1.webp)
- `bf-pb-right-rail` Right rail
  - icon: ![Right rail](assets/items/bf-pb-right-rail.webp)
- `bf-pb-rail-2` Table
  - icon: ![Table](assets/items/bf-pb-rail-2.webp)
- `bf-pb-top-rail` Top rail
  - icon: ![Top rail](assets/items/bf-pb-top-rail.webp)
- `bf-pb-rail-3` Table
  - icon: ![Table](assets/items/bf-pb-rail-3.webp)
- `bf-pb-lane` Lane rail
  - icon: ![Lane rail](assets/items/bf-pb-lane.webp)
- `bf-pb-rail-4` Table
  - icon: ![Table](assets/items/bf-pb-rail-4.webp)
- `bf-pb-left-lip` Left return
  - icon: ![Left return](assets/items/bf-pb-left-lip.webp)
- `bf-pb-rail-5` Table
  - icon: ![Table](assets/items/bf-pb-rail-5.webp)
- `bf-pb-right-lip` Right return
  - icon: ![Right return](assets/items/bf-pb-right-lip.webp)
- `bf-pb-rail-6` Table
  - icon: ![Table](assets/items/bf-pb-rail-6.webp)
- `bf-pb-cup` Marble cup
  - icon: ![Marble cup](assets/items/bf-pb-cup.webp)
- `bf-pb-rimmed` Table
  - icon: ![Table](assets/items/bf-pb-rimmed.webp)

**Combinations**
- `bf-pb-tray` [transform] + `bf-pb-left-rail` [consume] -> `bf-pb-rail-1`
- `bf-pb-rail-1` [transform] + `bf-pb-right-rail` [consume] -> `bf-pb-rail-2`
- `bf-pb-rail-2` [transform] + `bf-pb-top-rail` [consume] -> `bf-pb-rail-3`
- `bf-pb-rail-3` [transform] + `bf-pb-lane` [consume] -> `bf-pb-rail-4`
- `bf-pb-rail-4` [transform] + `bf-pb-left-lip` [consume] -> `bf-pb-rail-5`
- `bf-pb-rail-5` [transform] + `bf-pb-right-lip` [consume] -> `bf-pb-rail-6`
- `bf-pb-rail-6` [transform] + `bf-pb-cup` [consume] -> `bf-pb-rimmed`


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
- `bf-pb-flip` Flip
  - icon: ![Flip](assets/actions/flip.svg)
- `bf-pb-under` Table
  - icon: ![Table](assets/items/bf-pb-under.webp)
- `bf-pb-plate` Pivot plate
  - icon: ![Pivot plate](assets/items/bf-pb-plate.webp)

  ---

  A plate with retained spindles, finger buttons and return loops. The shoulders pass through the prepared tray clearances. Captive screws enter the tray’s threaded receivers from beneath.
- `bf-pb-plated-under` Table
  - icon: ![Table](assets/items/bf-pb-plated-under.webp)
- `bf-pb-support` Support
  - icon: ![Support](assets/items/bf-pb-support.webp)

  ---

  One connected U-shaped support with locating tongues and retaining clips. It slopes the table towards its marble cup without tilting sideways.
- `bf-pb-supported-under` Table
  - icon: ![Table](assets/items/bf-pb-supported-under.webp)
- `bf-pb-upright` Table
  - icon: ![Table](assets/items/bf-pb-upright.webp)
- `bf-pb-left-paddle` Left paddle
  - icon: ![Left paddle](assets/items/bf-pb-left-paddle.webp)

  ---

  One polymer paddle with an open keyed snap socket. Its flexible mouth clips sideways around the spindle neck between the retaining shoulders.
- `bf-pb-left` Table
  - icon: ![Table](assets/items/bf-pb-left.webp)
- `bf-pb-right-paddle` Right paddle
  - icon: ![Right paddle](assets/items/bf-pb-right-paddle.webp)

  ---

  One polymer paddle with an open keyed snap socket. Its flexible mouth clips sideways around the spindle neck between the retaining shoulders.
- `bf-pb-flipped` Table
  - icon: ![Table](assets/items/bf-pb-flipped.webp)

**Combinations**
- `bf-pb-rimmed` [transform] @ `bf-pb-flip` -> `bf-pb-under`
- `bf-pb-under` [transform] + `bf-pb-plate` [consume] -> `bf-pb-plated-under`
- `bf-pb-plated-under` [transform] + `bf-pb-support` [consume] -> `bf-pb-supported-under`
- `bf-pb-supported-under` [transform] @ `bf-pb-flip` -> `bf-pb-upright`
- `bf-pb-upright` [transform] + `bf-pb-left-paddle` [consume] -> `bf-pb-left`
- `bf-pb-left` [transform] + `bf-pb-right-paddle` [consume] -> `bf-pb-flipped`


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

  ---

  A six-millimetre plunger rod with a fitted pull handle and an open front end for threading the spring.
- `bf-pb-spring` Spring
  - icon: ![Spring](assets/items/bf-pb-spring.webp)
- `bf-pb-sprung-rod` Plunger
  - icon: ![Plunger](assets/items/bf-pb-sprung-rod.webp)
- `bf-pb-tip` Plunger tip
  - icon: ![Plunger tip](assets/items/bf-pb-tip.webp)

  ---

  A soft striking tip and piston with a blind gripping socket for the rod.
- `bf-pb-tipped` Plunger
  - icon: ![Plunger](assets/items/bf-pb-tipped.webp)
- `bf-pb-barrel` Launcher cradle
  - icon: ![Launcher cradle](assets/items/bf-pb-barrel.webp)

  ---

  An open-topped cradle with half-round end guides, mounting feet and a travel stop. The assembled plunger lowers through its open top.
- `bf-pb-open-launcher` Launcher
  - icon: ![Launcher](assets/items/bf-pb-open-launcher.webp)
- `bf-pb-cover` Launcher cover
  - icon: ![Launcher cover](assets/items/bf-pb-cover.webp)

  ---

  A clear upper shell with matching half-guides and flexible retaining clips. Closing it captures the plunger and encloses the spring.
- `bf-pb-launcher` Launcher
  - icon: ![Launcher](assets/items/bf-pb-launcher.webp)
- `bf-pb-flipped` Table
  - icon: ![Table](assets/items/bf-pb-flipped.webp)
- `bf-pb-launched` Table
  - icon: ![Table](assets/items/bf-pb-launched.webp)

**Combinations**
- `bf-pb-rod` [transform] + `bf-pb-spring` [consume] -> `bf-pb-sprung-rod`
- `bf-pb-sprung-rod` [transform] + `bf-pb-tip` [consume] -> `bf-pb-tipped`
- `bf-pb-tipped` [transform] + `bf-pb-barrel` [consume] -> `bf-pb-open-launcher`
- `bf-pb-open-launcher` [transform] + `bf-pb-cover` [consume] -> `bf-pb-launcher`
- `bf-pb-flipped` [transform] + `bf-pb-launcher` [consume] -> `bf-pb-launched`


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
- `bf-pb-arch-low` Lower arch
  - icon: ![Lower arch](assets/items/bf-pb-arch-low.webp)
- `bf-pb-target-1` Table
  - icon: ![Table](assets/items/bf-pb-target-1.webp)
- `bf-pb-arch-mid` Middle arch
  - icon: ![Middle arch](assets/items/bf-pb-arch-mid.webp)
- `bf-pb-target-2` Table
  - icon: ![Table](assets/items/bf-pb-target-2.webp)
- `bf-pb-arch-high` Upper arch
  - icon: ![Upper arch](assets/items/bf-pb-arch-high.webp)
- `bf-pb-target-3` Table
  - icon: ![Table](assets/items/bf-pb-target-3.webp)
- `bf-pb-score` Score wheel
  - icon: ![Score wheel](assets/items/bf-pb-score.webp)
- `bf-pb-scored` Table
  - icon: ![Table](assets/items/bf-pb-scored.webp)
- `bf-pb-marble` Marble
  - icon: ![Marble](assets/items/bf-pb-marble.webp)
- `pinball-table` Pinball table
  - icon: ![Pinball table](assets/items/pinball-table.webp)

**Combinations**
- `bf-pb-launched` [transform] + `bf-pb-arch-low` [consume] -> `bf-pb-target-1`
- `bf-pb-target-1` [transform] + `bf-pb-arch-mid` [consume] -> `bf-pb-target-2`
- `bf-pb-target-2` [transform] + `bf-pb-arch-high` [consume] -> `bf-pb-target-3`
- `bf-pb-target-3` [transform] + `bf-pb-score` [consume] -> `bf-pb-scored`
- `bf-pb-scored` [transform] + `bf-pb-marble` [consume] -> `pinball-table`
