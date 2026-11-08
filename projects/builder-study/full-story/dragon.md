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

  ---

  A plain six-millimetre shaft, supplied without its collars. The cam and bearings slide on before the separate collars retain the shaft.
- `bf-cd-cam` Cam
  - icon: ![Cam](assets/items/bf-cd-cam.webp)

  ---

  The shaft hole sits off centre. Turning the round disc raises and lowers the broad follower foot.
- `bf-cd-cammed` Frame
  - icon: ![Frame](assets/items/bf-cd-cammed.webp)
- `bf-cd-front-bearing` Front bearing
  - icon: ![Front bearing](assets/items/bf-cd-front-bearing.webp)
- `bf-cd-bearing-1` Frame
  - icon: ![Frame](assets/items/bf-cd-bearing-1.webp)
- `bf-cd-rear-bearing` Rear bearing
  - icon: ![Rear bearing](assets/items/bf-cd-rear-bearing.webp)
- `bf-cd-bearings` Frame
  - icon: ![Frame](assets/items/bf-cd-bearings.webp)
- `bf-cd-front-collar` Front collar
  - icon: ![Front collar](assets/items/bf-cd-front-collar.webp)
- `bf-cd-front-retained` Frame
  - icon: ![Frame](assets/items/bf-cd-front-retained.webp)
- `bf-cd-flip` Flip
  - icon: ![Flip](assets/actions/flip.svg)
- `bf-cd-rear-facing` Frame
  - icon: ![Frame](assets/items/bf-cd-rear-facing.webp)
- `bf-cd-rear-collar` Rear collar
  - icon: ![Rear collar](assets/items/bf-cd-rear-collar.webp)
- `bf-cd-retained-rear` Frame
  - icon: ![Frame](assets/items/bf-cd-retained-rear.webp)
- `bf-cd-retained` Frame
  - icon: ![Frame](assets/items/bf-cd-retained.webp)
- `bf-cd-handle` Crank
  - icon: ![Crank](assets/items/bf-cd-handle.webp)

  ---

  A D-shaped socket fits the matching shaft end. Its separate retaining clip enters the aligned cross holes after the crank is fitted.
- `bf-cd-cranked` Frame
  - icon: ![Frame](assets/items/bf-cd-cranked.webp)
- `bf-cd-crank-clip` Crank clip
  - icon: ![Crank clip](assets/items/bf-cd-crank-clip.webp)

  ---

  One spring-wire clip. Its straight leg passes through the aligned crank and shaft holes; the curved leg grips outside the socket.
- `bf-cd-clipped` Frame
  - icon: ![Frame](assets/items/bf-cd-clipped.webp)
- `bf-cd-base` Base
  - icon: ![Base](assets/items/bf-cd-base.webp)
- `bf-cd-frame` Frame
  - icon: ![Frame](assets/items/bf-cd-frame.webp)

**Combinations**
- `bf-cd-shaft` [transform] + `bf-cd-cam` [consume] -> `bf-cd-cammed`
- `bf-cd-cammed` [transform] + `bf-cd-front-bearing` [consume] -> `bf-cd-bearing-1`
- `bf-cd-bearing-1` [transform] + `bf-cd-rear-bearing` [consume] -> `bf-cd-bearings`
- `bf-cd-bearings` [transform] + `bf-cd-front-collar` [consume] -> `bf-cd-front-retained`
- `bf-cd-front-retained` [transform] @ `bf-cd-flip` -> `bf-cd-rear-facing`
- `bf-cd-rear-facing` [transform] + `bf-cd-rear-collar` [consume] -> `bf-cd-retained-rear`
- `bf-cd-retained-rear` [transform] @ `bf-cd-flip` -> `bf-cd-retained`
- `bf-cd-retained` [transform] + `bf-cd-handle` [consume] -> `bf-cd-cranked`
- `bf-cd-cranked` [transform] + `bf-cd-crank-clip` [consume] -> `bf-cd-clipped`
- `bf-cd-clipped` [transform] + `bf-cd-base` [consume] -> `bf-cd-frame`


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

  ---

  An open square channel with a mounting foot and spring anchor. The separate cover closes around the follower; its broad foot never has to pass through the narrow channel.
- `bf-cd-follower` Follower
  - icon: ![Follower](assets/items/bf-cd-follower.webp)

  ---

  A sliding rod with a broad cam foot, spring collar and retained crosshead pin for two independently pivoting links.
- `bf-cd-open-follower` Follower
  - icon: ![Follower](assets/items/bf-cd-open-follower.webp)
- `bf-cd-cover` Cover
  - icon: ![Cover](assets/items/bf-cd-cover.webp)
- `bf-cd-guided` Follower
  - icon: ![Follower](assets/items/bf-cd-guided.webp)
- `bf-cd-frame` Frame
  - icon: ![Frame](assets/items/bf-cd-frame.webp)
- `bf-cd-mounted` Lifter
  - icon: ![Lifter](assets/items/bf-cd-mounted.webp)
- `bf-cd-spring` Spring
  - icon: ![Spring](assets/items/bf-cd-spring.webp)
- `bf-cd-lifter` Lifter
  - icon: ![Lifter](assets/items/bf-cd-lifter.webp)

**Combinations**
- `bf-cd-guide` [transform] + `bf-cd-follower` [consume] -> `bf-cd-open-follower`
- `bf-cd-open-follower` [transform] + `bf-cd-cover` [consume] -> `bf-cd-guided`
- `bf-cd-frame` [transform] + `bf-cd-guided` [consume] -> `bf-cd-mounted`
- `bf-cd-mounted` [transform] + `bf-cd-spring` [consume] -> `bf-cd-lifter`


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
- `bf-cd-left-wing` Left wing
  - icon: ![Left wing](assets/items/bf-cd-left-wing.webp)

  ---

  One card wing with a prepared split snap pin and spacer. The two tapered tips compress through the body hole and reopen behind it.
- `bf-cd-body-left` Body
  - icon: ![Body](assets/items/bf-cd-body-left.webp)
- `bf-cd-right-wing` Right wing
  - icon: ![Right wing](assets/items/bf-cd-right-wing.webp)

  ---

  One card wing with a prepared split snap pin and spacer. The two tapered tips compress through the body hole and reopen behind it.
- `bf-cd-winged` Body
  - icon: ![Body](assets/items/bf-cd-winged.webp)
- `bf-cd-tail` Tail
  - icon: ![Tail](assets/items/bf-cd-tail.webp)

  ---

  The tail carries a split snap pin. Its tapered tip passes through the body hole before its flexible barbs reopen.
- `bf-cd-bodied` Dragon
  - icon: ![Dragon](assets/items/bf-cd-bodied.webp)
- `bf-cd-lifter` Lifter
  - icon: ![Lifter](assets/items/bf-cd-lifter.webp)
- `bf-cd-mounted-body` Dragon
  - icon: ![Dragon](assets/items/bf-cd-mounted-body.webp)
- `bf-cd-left-link` Left link
  - icon: ![Left link](assets/items/bf-cd-left-link.webp)

  ---

  One rigid 55 mm polymer link with two open snap eyes. Fit both eyes sideways over the exposed pin necks; their heads stay in place.
- `bf-cd-linked-left` Dragon
  - icon: ![Dragon](assets/items/bf-cd-linked-left.webp)
- `bf-cd-right-link` Right link
  - icon: ![Right link](assets/items/bf-cd-right-link.webp)

  ---

  One rigid 55 mm polymer link with two open snap eyes. It pivots independently beside the other link.
- `crank-dragon` Crank dragon
  - icon: ![Crank dragon](assets/items/crank-dragon.webp)

**Combinations**
- `bf-cd-body` [transform] + `bf-cd-left-wing` [consume] -> `bf-cd-body-left`
- `bf-cd-body-left` [transform] + `bf-cd-right-wing` [consume] -> `bf-cd-winged`
- `bf-cd-winged` [transform] + `bf-cd-tail` [consume] -> `bf-cd-bodied`
- `bf-cd-lifter` [transform] + `bf-cd-bodied` [consume] -> `bf-cd-mounted-body`
- `bf-cd-mounted-body` [transform] + `bf-cd-left-link` [consume] -> `bf-cd-linked-left`
- `bf-cd-linked-left` [transform] + `bf-cd-right-link` [consume] -> `crank-dragon`
