# Builder: assembly goals

The v21 candidate replaces distant chapter goals with 170 concrete instructions across all 29 playable chapters. Each chapter uses one `next:` chain, so the player sees one current instruction. The last instruction keeps the chapter’s finished-machine use or experiment. This responds to the user’s request for goals that function like construction-guide steps.

The underlying recipes remain available in their original orders. Completed hidden goals latch immediately, so an early subassembly or rover fitting stays credited. Disjunctive witnesses preserve the cam’s test/spring routes, the crane’s ballast/test/pawl routes, and the projector’s lens/screen routes. The rover’s five slot milestones remain independently bankable; the chain suggests an order without requiring it.

## Verification

Checks used the live `stories/builder/builder.md` as the baseline and `builder-v21.md` as the candidate. Disposable scripts and output were placed in `runs/builder-readability/goals`.

- Removing each Goals section gives byte-identical story text. All 181 recipes, item definitions, slots, chapter supplies and hotspots also compare equal after normalizing registry insertion order.
- Fast semantic lint reports zero errors and the existing intentional rover mixed-fates warning.
- Both checkpoint witnesses finish in 170 combinations. Replaying all 321 baseline actions in v21 preserves inventory identities, token statuses, chapter membership, installed slots and chapter-completion results after every action. At most one goal is visible.
- For each of the 29 playable chapters, exhaustive traversal of current-board combinations from its baseline checkpoint compared old/new inventories, retirement, legal action sets, completion and visible-goal count: 349 states and 576 edges, with no unfinished terminal state. This includes both cam experiment routes, all four crane branches, both projector routes and the rover installation state graph.

These are structural checks, not evidence of player enjoyment. Traversal covers current-board combinations from the baseline checkpoint for each chapter; it does not enumerate every historical scrollback or preceding-chapter history. Goal dependency ordering may change initial positions, which these comparisons deliberately exclude. Browser layout and independent editorial review remain separate checks.

## Final v22 author source

The v21 manuscript remains frozen. The v22 candidate applies the explicit [assembly split plan](art-readability-2026.11.07/assembly-splits.json): 24 new identities and twelve additional physical operations, for **193 recipes and 182 guided goals**. Chapter changes are c03 (catch apron), c04 (score wheel), c06 (wings and tail), c-air-1 (plunger clip), c-air-2 (hand-syringe holders), c17 (guide crossbars and retaining nuts), and c20 (lift extensions, harness, forks, retention and stop guide). Chapters c13/c14 clarify that the rover deck supplies its fixed pen mechanism and the loose carriage supplies the moving piece; those chapters gain no recipes. The same sponge pear is used throughout its garden reward, with Jo’s collecting cup in the setting.

All 40 representative supplies/subassemblies selected in `part-presentations.json` state their actual quantity and that one drawing represents the set. Counts were checked against the canonical source and the part-audit author: eight whale ribs, eight braces/tensioners, sixteen cord runs, three complete garden tethers, four bare lift-guide posts, two crossbars and four retaining nuts. Periscope wording describes its actual two window shades. No repeated identical fitting gained an extra action.

The new module preparation and fork fitting remain independent until installation. Existing cam, crane and projector alternatives and all five independent rover fittings remain unchanged. Exact authored recipes and the new identity set match the split plan; compound acceptance is unchanged.

The final checkpoint completes with 182 combinations and replays all 342 actions. Exhaustive current-board traversal from each of its 29 chapter checkpoints covers 371 states, 610 edges and all 193 recipes. Every terminal state is complete, every state displays at most one current instruction, and all 34 terminal branches replay the remaining canonical route to the ending. Both cam routes, all four crane branches and both projector routes remain reachable. Chapter starts contain at most ten available items, including the revised lift chapter.

Fast semantic lint reports zero errors and the intentional rover mixed-fates warning. The final deep semantic check retains the existing 20,000-state fixed-item verification limit; exhaustive whole-history retirement and peak-count verification remains incomplete. These checks do not substitute for visual review, actual browser checks or fresh playtests. The wording pass is not a fresh player trial.

Frozen author-source SHA-256: `7765d2cf7f25a3e3b0ad271d219f7b313614f2f801292aaf904b0982f70d249d`. The archived catalogue tool rebuilt `runs/builder-readability/catalogue-v22.json`: 364 artwork identities and 181 supplied parts/tool groups. Exported art metadata is outside this source freeze.

## Instruction review and v23

A fresh manuscript-only reviewer inspected all 182 instructions in the frozen v22, without author notes or earlier reviews. It found no selection dead end, but identified naming and operation mismatches. V23 adopts eleven specific goal corrections and two related result-text corrections: use actual part names, fit the follower through its open guide, distinguish the colour-cell lid from its light cover, connect the rover leads before guarding, lift its pen by hand, compare the added lift load without claiming a measured limit, fit the projector handle, position the screen, and land before attaching and testing the emergency-stop lever. The existing coupler-removal sequence remains explicit because the selected shaft assembly requires that access; it adds no game operation.

The v23 parser comparison preserves the complete recipes, goal conditions/operators/chains, item identities, slots and chapter supplies. Fast semantic lint reports zero errors. Its source hash is `6716dcab1f61a4a9cf3017dc9e9b72b1587a04eb0985ef77133c3d60ac4a1a79`. A separate fresh instruction review and targeted new player trials follow; no earlier editorial acceptance is inferred for the revised words.

The second fresh reviewer inspected every v23 instruction and passed the manuscript-level guidance, with no unresolved selection blocker or material padding. V24 adopts its small follow-ups: the crane lifts above the bench, the grounded whale is named as resting in its cradle, the first blurry projection is static until a handle is fitted, and the goal uses the supplied cam's “two-humped” wording. These are wording/state-name changes. Actual progressive display, artwork and touch interaction remain separate checks.

The exported candidate's full pointer route exposed overlapping invisible touch areas around the two narrow pencils. The visible drawings were separate, but the smaller canvas did not reserve the engine's whole 44px receiving area during arrival layout. Portable exports now reserve at least 44px in each canvas dimension around the already enlarged visible drawing. This padding is an interaction/layout fix; the visible scale-family bounds still measure actual ink. It requires a new browser route, not an inference from the prior layout.


## V25–v26 and visual destinations

V25 separates the real accessory-switch parking dock from its power supply: the dock is fitted under the deck before the accessory supply is connected. Its prepared support arm and plate are one connected part. Source inspection also established that the dragon mounting supply contains four sections in two matching pairs; one actual long section is shown, with quantity and captive pins stated. V26 adds 29 chapter-local reference pictures. Connected chapters share a finished target where useful; the lift test stand has its own target. These pictures are presentation metadata and add no game identities or operations.

The final source has 194 recipes, 183 successive goals, 366 artwork identities and 182 primitive supplies. A full checkpoint replays all 343 actions, including 183 combinations. Exhaustive current-board traversal from each chapter checkpoint covers 372 states, 611 edges and all 194 recipes. All 34 terminal branches complete and replay the remaining route to the ending; no state exposes more than one current instruction. The explicit split plan still matches every authored recipe change and new identity, and the rover's compound acceptance is unchanged. The 29 references are present only in the construction chapters. These checks have the same whole-history and human-evidence limits described above.

V27 makes access visible and explicit: work from the whale's hatch side, open the service hatch after securing the projector, keep it open for the dock and accessory supply, and close it at the next chapter's start. It changes three prose passages and no recipe, goal condition, identity, quantity or reference selection. The same exhaustive chapter traversal and complete replay pass for V27.
