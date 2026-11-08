## `c-spinner-drive` Two pulleys
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Drive](assets/items/sp-drive-ready.webp)

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
  - icon: ![Base](assets/items/sp-base.webp)
- `sp-motor` Motor
  - icon: ![Motor](assets/items/sp-motor.webp)
- `sp-bearing` Spindle
  - icon: ![Spindle](assets/items/sp-bearing.webp)
- `sp-motor-pulley` Small pulley
  - icon: ![Small pulley](assets/items/sp-motor-pulley.webp)
- `sp-driven-pulley` Large pulley
  - icon: ![Large pulley](assets/items/sp-driven-pulley.webp)
- `sp-belt` Belt
  - icon: ![Belt](assets/items/sp-belt.webp)
- `sp-guard` Guard
  - icon: ![Guard](assets/items/sp-guard.webp)
- `sp-wheel` Wheel
  - icon: ![Wheel](assets/items/sp-wheel.webp)
- `sp-collar` Collar
  - icon: ![Collar](assets/items/sp-collar.webp)
- `sp-motor-unit` Motor
  - icon: ![Motor](assets/items/sp-motor-unit.webp)
- `sp-bearing-unit` Spindle
  - icon: ![Spindle](assets/items/sp-bearing-unit.webp)
- `sp-drive-2` Base
  - icon: ![Base](assets/items/sp-drive-2.webp)
- `sp-drive-10` Base
  - icon: ![Base](assets/items/sp-drive-10.webp)
- `sp-drive-1` Base
  - icon: ![Base](assets/items/sp-drive-1.webp)
- `sp-drive-3` Base
  - icon: ![Base](assets/items/sp-drive-3.webp)
- `sp-drive-11` Base
  - icon: ![Base](assets/items/sp-drive-11.webp)
- `sp-drive-5` Base
  - icon: ![Base](assets/items/sp-drive-5.webp)
- `sp-drive-7` Base
  - icon: ![Base](assets/items/sp-drive-7.webp)
- `sp-drive` Base
  - icon: ![Base](assets/items/sp-drive.webp)
- `sp-belted` Drive
  - icon: ![Drive](assets/items/sp-belted.webp)
- `sp-guarded` Drive
  - icon: ![Drive](assets/items/sp-guarded.webp)
- `sp-wheeled` Drive
  - icon: ![Drive](assets/items/sp-wheeled.webp)
- `sp-drive-ready` Drive
  - icon: ![Drive](assets/items/sp-drive-ready.webp)

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
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![String spinner](assets/items/ribbon-spinner.webp)

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
- next: Thread the loop over the wheel -- `ribbon-spinner`

**Items**
- `sp-battery` Battery
  - icon: ![Battery](assets/items/sp-battery.webp)
- `sp-switch` Switch
  - icon: ![Switch](assets/items/sp-switch.webp)
- `sp-fork` Fork
  - icon: ![Fork](assets/items/sp-fork.webp)
- `sp-string` String
  - icon: ![String](assets/items/sp-string.webp)
- `sp-joiner` Joiner
  - icon: ![Joiner](assets/items/sp-joiner.webp)
- `sp-string-loop` Loop
  - icon: ![Loop](assets/items/sp-string-loop.webp)
- `sp-fitted-1` Spinner
  - icon: ![Spinner](assets/items/sp-fitted-1.webp)
- `sp-fitted-2` Spinner
  - icon: ![Spinner](assets/items/sp-fitted-2.webp)
- `sp-fitted-3` Spinner
  - icon: ![Spinner](assets/items/sp-fitted-3.webp)
- `sp-fitted-4` Spinner
  - icon: ![Spinner](assets/items/sp-fitted-4.webp)
- `sp-fitted-5` Spinner
  - icon: ![Spinner](assets/items/sp-fitted-5.webp)
- `sp-fitted-6` Spinner
  - icon: ![Spinner](assets/items/sp-fitted-6.webp)
- `sp-fitted-7` Spinner
  - icon: ![Spinner](assets/items/sp-fitted-7.webp)
- `ribbon-spinner` String spinner
  - icon: ![String spinner](assets/items/ribbon-spinner.webp)

**Combinations**
- `sp-joiner` [consume] + `sp-string` [transform] -> `sp-string-loop`
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
- `sp-string-loop` [consume] + `sp-fitted-7` [transform] -> `ribbon-spinner`
