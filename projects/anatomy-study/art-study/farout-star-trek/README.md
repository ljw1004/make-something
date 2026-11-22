# Star Trek: build the textbook page

[Play all four illustrated chapters](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/farout-star-trek/sample.md): cell boundary → bones and muscles → hearing → digestion. This sample plays consecutively and ends after digestion. Chapter numbers on the contact sheet refer to the original full book.

The revised full-book trial for the [Anatomy design brief](../../../../contrib/anatomy/design-brief.md), using the supplied [Star Trek inspiration](../../inspiration/farout-star-trek.png): translucent cyan contours, violet/coral tissue, ivory skeleton and gold details on midnight blue.

- [Play the revised book](http://127.0.0.1:5173/index.html?story=projects/anatomy-study/art-study/farout-star-trek/anatomy.md).
- [Compare starting pieces and completed constructions in all 28 chapters](http://127.0.0.1:5173/projects/anatomy-study/art-study/farout-star-trek/review.html).
- [Complete contact sheet](all-chapters.jpg), [four-chapter comparison](contact-sheet.jpg), and [verification record](../../art-review/2026.11.14_21.49.10/report.md).

Every playable chapter has artwork: **254 identities and 26 compound fittings**. The background is a blank technical grid. Anatomy belongs to movable pieces and fixed receiving objects. Constituents are derived from their assembled families: water occupies the membrane bag's interior, lipid sections retain its bilayer detail, organelles retain their fitted dimensions, and partial constructions retain earlier additions. Located enlargements travel with the object. Later whole-body appearances use explicit chapter presentation metadata.

This replaces the initial four-chapter Star Trek candidate. The original manuscript and the other twelve directions remain unchanged. Five named objects receive explicit internal IDs in this illustrated copy to support later appearances; their visible names and canonical gameplay remain unchanged. The [semantic check](rework/verify-semantics.ts) applies the recorded identity aliases before comparing every chapter, goal, supply, recipe, reading and fate.

## Production

The [production contract](rework/production.md) and four packages retain selected built-in imagegen masters, exact requests, mechanical extraction scripts, registration records and complete asset maps:

- [Opening: chapters 1–7](rework/opening/README.md).
- [Senses and circulation: chapters 8–14](rework/senses-circulation/README.md).
- [Defense and digestion: chapters 15–21](rework/defense-digestion/README.md).
- [Skin and finale: chapters 22–28](rework/skin-finale/README.md).

Run each package's producer, then integrate and verify from the repository root:

```sh
node projects/anatomy-study/art-study/farout-star-trek/rework/integrate.ts
node projects/anatomy-study/art-study/farout-star-trek/rework/verify-semantics.ts projects/anatomy-study/art-study/farout-star-trek/anatomy.md
npm run lint -- projects/anatomy-study/art-study/farout-star-trek/anatomy.md
node projects/anatomy-study/art-study/farout-star-trek/rework/check-player.mjs
uv run --with pillow python projects/anatomy-study/art-study/farout-star-trek/rework/make-sheets.py
```

The browser check requires the local dev server. `WIDTH` and `HEIGHT` select the viewport; optional chapter numbers select targeted checks. Browser captures are disposable scratch under `runs/`; the sheet builder retains the requested comparison deliverables here. This is an artwork trial, with informed visual and browser checks rather than student recognition or medical validation.

The former root-level `sources/`, `assets/`, `produce.py`, `art-map.json` and `registration.json` retain provenance for the initial four-chapter comparison referenced by its historical review. They are superseded and are not used by the current manuscript. Rebuild this edition with `rework/integrate.ts`, not the initial study exporter.
