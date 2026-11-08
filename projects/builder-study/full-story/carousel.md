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

  ---

  A broad prepared base with sockets for the bearing, motor and battery. The motor and controller are matching low-voltage modules.

- `ca-spindle` Spindle
  - icon: ![Spindle](assets/items/ca-spindle.webp)

  ---

  A vertical spindle and pulley retained inside a bearing block. The square upper end drives the deck; a shoulder supports its hub above the guard.

- `ca-motor` Motor
  - icon: ![Motor](assets/items/ca-motor.webp)

  ---

  A small enclosed geared motor, its pulley, retaining strap, mounting foot and plugged lead form one supplied module.

- `ca-belt` Belt
  - icon: ![Belt](assets/items/ca-belt.webp)
- `ca-guard` Guard
  - icon: ![Guard](assets/items/ca-guard.webp)

  ---

  A clear cover with a real shaft opening, cable opening and attached locating feet.

- `ca-battery` Battery and dial
  - icon: ![Battery and dial](assets/items/ca-battery.webp)

  ---

  The battery holder, switch and speed dial share one case. Its connected lead plugs into the motor.

- `ca-deck` Deck
  - icon: ![Deck](assets/items/ca-deck.webp)

  ---

  A round deck with a central drive socket and three prepared pole sockets.

- `ca-spindle-base` Base
  - icon: ![Base](assets/items/ca-spindle-base.webp)
- `ca-motor-base` Base
  - icon: ![Base](assets/items/ca-motor-base.webp)
- `ca-drive-base` Base
  - icon: ![Base](assets/items/ca-drive-base.webp)
- `ca-belted` Base
  - icon: ![Base](assets/items/ca-belted.webp)
- `ca-guarded` Base
  - icon: ![Base](assets/items/ca-guarded.webp)
- `ca-wired` Base
  - icon: ![Base](assets/items/ca-wired.webp)
- `ca-ready` Base
  - icon: ![Base](assets/items/ca-ready.webp)
- `ca-platform` Carousel
  - icon: ![Carousel](assets/items/ca-platform.webp)

**Combinations**
- `ca-base` [transform] + `ca-spindle` [consume] -> `ca-spindle-base`
- `ca-base` [transform] + `ca-motor` [consume] -> `ca-motor-base`
- `ca-spindle-base` [transform] + `ca-motor` [consume] -> `ca-drive-base`
- `ca-motor-base` [transform] + `ca-spindle` [consume] -> `ca-drive-base`
- `ca-drive-base` [transform] + `ca-belt` [consume] -> `ca-belted`
- `ca-belted` [transform] + `ca-guard` [consume] -> `ca-guarded`
- `ca-belted` [transform] + `ca-battery` [consume] -> `ca-wired`
- `ca-guarded` [transform] + `ca-battery` [consume] -> `ca-ready`
- `ca-wired` [transform] + `ca-guard` [consume] -> `ca-ready`
- `ca-ready` [transform] + `ca-deck` [consume] -> `ca-platform`

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

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-1` Pole
  - icon: ![Pole](assets/items/ca-pole-1.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-1` Red horse
  - icon: ![Red horse](assets/items/ca-rider-1.webp)
- `ca-horse-2` Green horse
  - icon: ![Green horse](assets/items/ca-horse-2.webp)

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-2` Pole
  - icon: ![Pole](assets/items/ca-pole-2.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-2` Green horse
  - icon: ![Green horse](assets/items/ca-rider-2.webp)
- `ca-horse-3` Cream horse
  - icon: ![Cream horse](assets/items/ca-horse-3.webp)

  ---

  A single connected horse with a through socket in its back. Any of the three poles fits it.

- `ca-pole-3` Pole
  - icon: ![Pole](assets/items/ca-pole-3.webp)

  ---

  A straight pole with a lower mounting peg and a shoulder that supports the horse. Any pole fits any horse.

- `ca-rider-3` Cream horse
  - icon: ![Cream horse](assets/items/ca-rider-3.webp)
- `ca-horses-1` Carousel
  - icon: ![Carousel](assets/items/ca-horses-1.webp)
- `ca-horses-2` Carousel
  - icon: ![Carousel](assets/items/ca-horses-2.webp)
- `ca-horses-3` Carousel
  - icon: ![Carousel](assets/items/ca-horses-3.webp)
- `ca-horses-4` Carousel
  - icon: ![Carousel](assets/items/ca-horses-4.webp)
- `ca-horses-5` Carousel
  - icon: ![Carousel](assets/items/ca-horses-5.webp)
- `ca-horses-6` Carousel
  - icon: ![Carousel](assets/items/ca-horses-6.webp)
- `ca-horses-7` Carousel
  - icon: ![Carousel](assets/items/ca-horses-7.webp)
- `ca-roofpost` Roof post
  - icon: ![Roof post](assets/items/ca-roofpost.webp)
- `ca-canopy` Canopy
  - icon: ![Canopy](assets/items/ca-canopy.webp)

  ---

  A small moulded canopy with a centre socket. It sits high enough to leave the horses visible.

- `ca-posted` Carousel
  - icon: ![Carousel](assets/items/ca-posted.webp)
- `electric-carousel` Electric carousel
  - icon: ![Electric carousel](assets/items/electric-carousel.webp)

  ---

  The small motor pulley drives the larger spindle pulley through the belt. All three horses turn with the deck. The roof, poles and horses keep their actual sizes throughout the build.


**Combinations**
- `ca-horse-1` [transform] + `ca-pole-1` [consume] -> `ca-rider-1`
- `ca-horse-1` [transform] + `ca-pole-2` [consume] -> `ca-rider-1`
- `ca-horse-1` [transform] + `ca-pole-3` [consume] -> `ca-rider-1`
- `ca-horse-2` [transform] + `ca-pole-1` [consume] -> `ca-rider-2`
- `ca-horse-2` [transform] + `ca-pole-2` [consume] -> `ca-rider-2`
- `ca-horse-2` [transform] + `ca-pole-3` [consume] -> `ca-rider-2`
- `ca-horse-3` [transform] + `ca-pole-1` [consume] -> `ca-rider-3`
- `ca-horse-3` [transform] + `ca-pole-2` [consume] -> `ca-rider-3`
- `ca-horse-3` [transform] + `ca-pole-3` [consume] -> `ca-rider-3`
- `ca-platform` [transform] + `ca-rider-1` [consume] -> `ca-horses-1`
- `ca-platform` [transform] + `ca-rider-2` [consume] -> `ca-horses-2`
- `ca-platform` [transform] + `ca-rider-3` [consume] -> `ca-horses-4`
- `ca-horses-1` [transform] + `ca-rider-2` [consume] -> `ca-horses-3`
- `ca-horses-1` [transform] + `ca-rider-3` [consume] -> `ca-horses-5`
- `ca-horses-2` [transform] + `ca-rider-1` [consume] -> `ca-horses-3`
- `ca-horses-2` [transform] + `ca-rider-3` [consume] -> `ca-horses-6`
- `ca-horses-3` [transform] + `ca-rider-3` [consume] -> `ca-horses-7`
- `ca-horses-4` [transform] + `ca-rider-1` [consume] -> `ca-horses-5`
- `ca-horses-4` [transform] + `ca-rider-2` [consume] -> `ca-horses-6`
- `ca-horses-5` [transform] + `ca-rider-2` [consume] -> `ca-horses-7`
- `ca-horses-6` [transform] + `ca-rider-1` [consume] -> `ca-horses-7`
- `ca-horses-7` [transform] + `ca-roofpost` [consume] -> `ca-posted`
- `ca-posted` [transform] + `ca-canopy` [consume] -> `electric-carousel`
