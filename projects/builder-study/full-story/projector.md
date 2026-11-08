## `c-projector-box` A box of stars
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Projector](assets/items/pj-wheel-box.webp)

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
  - icon: ![Punch](assets/actions/punch.svg)
  - hitbox: (center 130px, 216px) (size 236px, 248px)
- `pj-flip` (center 390px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `pj-box` Box
  - icon: ![Box](assets/items/pj-box.webp)

  ---

  An open prepared box with two upward-opening bearing cradles. Prepared loading slots let the complete star wheel lower into them; the lid closes those slots and retains the shaft.
- `pj-liner` Reflector
  - icon: ![Reflector](assets/items/pj-liner.webp)

  ---

  One folded U-shaped reflector joins its floor and side faces. It leaves the electrical contacts clear.
- `pj-lamp` Lamp
  - icon: ![Lamp](assets/items/pj-lamp.webp)

  ---

  A cool-running diffused LED module, holder, current-limiting resistor and attached lead.
- `pj-battery` Battery pack
  - icon: ![Battery pack](assets/items/pj-battery.webp)

  ---

  An enclosed compatible switched low-voltage pack with its connected holder and fused lead. Connect with the switch off.
- `pj-card` Card disc
  - icon: ![Card disc](assets/items/pj-card.webp)

  ---

  The flat-sided centre hole matches the spindle.
- `pj-spindle` Spindle
  - icon: ![Spindle](assets/items/pj-spindle.webp)

  ---

  The flat continues from the free front end to the disc seat. Slide the disc along it until it reaches the fixed rear shoulder. The two rear flanges locate the shaft in its bearing.
- `pj-collar` Disc collar
  - icon: ![Disc collar](assets/items/pj-collar.webp)

  ---

  Slide this flat-sided collar along the same free end, then tighten its captive screw against the shaft flat. It holds the disc against the fixed shoulder.
- `pj-lined` Projector
  - icon: ![Projector](assets/items/pj-lined.webp)
- `pj-loaded` Projector
  - icon: ![Projector](assets/items/pj-loaded.webp)
- `pj-lamp-facing` Projector
  - icon: ![Projector](assets/items/pj-lamp-facing.webp)
- `pj-lamped` Projector
  - icon: ![Projector](assets/items/pj-lamped.webp)
- `pj-stars` Star disc
  - icon: ![Star disc](assets/items/pj-stars.webp)
- `pj-disc-shaft` Star wheel
  - icon: ![Star wheel](assets/items/pj-disc-shaft.webp)
- `pj-wheel` Star wheel
  - icon: ![Star wheel](assets/items/pj-wheel.webp)
- `pj-wheel-loading` Star wheel
  - icon: ![Star wheel](assets/items/pj-wheel-loading.webp)
- `pj-wheel-box` Projector
  - icon: ![Projector](assets/items/pj-wheel-box.webp)
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
background: ![White instruction page](assets/backgrounds/white.svg)
reference: ![Star projector](assets/items/star-projector.webp)

**Goals**
- Close the box with its lid -- `pj-closed`
- next: Turn the box toward the lens opening -- `pj-front-closed`
- next: Fit the lens into its holder -- `pj-focus`
- next: Fit the holder to the box -- `pj-focused`
- next: Fit the hood around the lens -- `pj-hooded`
- next: Fit the handle to the spindle -- `star-projector`

**Hotspots**
- `pj-flip` (center 390px, 216px)
  - icon: ![Flip](assets/actions/flip.svg)
  - hitbox: (center 390px, 216px) (size 236px, 248px)

**Items**
- `pj-lens` Lens
  - icon: ![Lens](assets/items/pj-lens.webp)

  ---

  A single convex lens forms an inverted image of the lit holes.
- `pj-holder` Lens holder
  - icon: ![Lens holder](assets/items/pj-holder.webp)

  ---

  A connected sliding carriage retained on its rails. Move it along the rails to focus.
- `pj-hood` Hood
  - icon: ![Hood](assets/items/pj-hood.webp)

  ---

  The dark tube surrounds the lens without covering its clear aperture.
- `pj-handle` Handle
  - icon: ![Handle](assets/items/pj-handle.webp)

  ---

  The handwheel has a real belt groove behind its grip. It can be turned by hand now and driven by a belt later.
- `pj-lid` Lid
  - icon: ![Lid](assets/items/pj-lid.webp)

  ---

  One connected lid with locating tabs, shaft retainers and two downward tongues. The inner tongue carries the real projection window. Fit the lid before the external lens rails, which pass through its prepared openings.
- `pj-closed` Projector
  - icon: ![Projector](assets/items/pj-closed.webp)
- `pj-front-closed` Projector
  - icon: ![Projector](assets/items/pj-front-closed.webp)
- `pj-focus` Lens holder
  - icon: ![Lens holder](assets/items/pj-focus.webp)
- `pj-focused` Projector
  - icon: ![Projector](assets/items/pj-focused.webp)
- `pj-hooded` Projector
  - icon: ![Projector](assets/items/pj-hooded.webp)
- `star-projector` Star projector
  - icon: ![Star projector](assets/items/star-projector.webp)

  ---

  Turning the disc brings new holes past the fixed aperture. Sliding the lens brings their projected image into focus. The optical model uses one ideal thin lens; brightness and real component tolerances are not measured.

**Combinations**
- `pj-lens` [consume] + `pj-holder` [transform] -> `pj-focus`
- `pj-lid` [consume] + `pj-wheel-box` [transform] -> `pj-closed`
- `pj-closed` [transform] @ `pj-flip` -> `pj-front-closed`
- `pj-focus` [consume] + `pj-front-closed` [transform] -> `pj-focused`
- `pj-hood` [consume] + `pj-focused` [transform] -> `pj-hooded`
- `pj-handle` [consume] + `pj-hooded` [transform] -> `star-projector`
