# Consecutive playable artwork samples

The user found blank icons after advancing from chapter 1. The comparison linked to full manuscripts whose illustrated chapters were 1, 4, 8 and 18. Earlier checkpoint-based verification proved those selected chapters could be played individually; it did not verify the ordinary comparison experience. This was a delivery error.

Each of the thirteen themes now has a generated `sample.md`: cell boundary → bones and muscles → hearing → digestion → a short ending. Gallery and study play links open these samples. Full `anatomy.md` editions remain unchanged as production sources, including the fully illustrated Star Trek book. Separate sample URLs avoid resuming old full-book progress. Contact sheets retain original chapter numbers and have been rebuilt from the consecutive sample captures.

The [builder](../../art-study/checks/build-samples.ts) retains selected goals, recipes, artwork and five relevant fittings. It removes the three later cell fittings and associated conditional descriptions/name change, and supplies muscle cells directly in the arm chapter instead of requiring omitted chapter 3. It adjusts the arm introduction and adds a clear sample ending. The [shared brief](../../design-brief.md#selected-artwork-1800s-anatomical-atlas) owns this delivery scope.

Verification:

- All thirteen samples pass native lint with **zero errors and zero warnings**. Each has 33 identities, 21 recipes, four playable chapters and one ending. Native reference completion takes 16 combinations; the browser route uses 17 to inspect the optional saliva intermediate.
- All thirteen samples pass **continuous browser play at 390×844**: 52 chapter completions, normal Continue transitions, completed-state reloads and arrivals at the ending. No debugger jumps are used. Every starting item/hotspot has an image; image decoding and page-error checks pass. This directly covers the reported failure. Existing artwork had prior checks at short-phone and desktop sizes; those are not claimed as new continuous sample runs.
- Builder assertions preserve every selected goal, default/effective icon, recipe and relevant fitting against each full source edition. The original source hash remains `d6920c636ce31af51a80b341237c1ba3375d29daf23b71834aeb2eae8ff63229`.
- All thirteen gallery play links resolve to the five-section sample manuscripts; following the first link opens the normal player. The regenerated gallery images and linked local artifacts load successfully.

Reproduce with `node projects/anatomy/art-study/checks/build-samples.ts`, native lint/analysis on `*/sample.md`, and `node projects/anatomy/art-study/checks/capture.mjs --sample THEME...`. Rebuild requested sheets with `uv run --with pillow python projects/anatomy/art-study/contact-sheets.py`; `--gallery-only` updates links without captures. Raw verification captures under `runs/anatomy-sample-flow/` are removed after consolidation. No engine/application behavior, artwork generation, publication or access settings changed.
