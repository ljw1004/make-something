# Undissection working notes

**Current direction:** the user rejected the kidney-centred prototype below as far too advanced and authorized a new grades 8–10 organ/system story. See [School-level reset](#school-level-reset). Earlier findings remain historical evidence about a different manuscript; the active brief and narrative arc now describe *Lift a glass*.

## Method and scope

Started 2026-11-11. User requested source research, repeated three-variant brainstorming with blind review, narrative and combination review, and iterative Terra `--fast` playtests. Gameplay only. This is a development study, not an accepted catalogue story or a learning-effectiveness experiment.

Fresh reviewers receive only the current assigned artifact and the applicable criteria. They do not receive the author's preferred answer, previous reviews or this log. Concept comparisons ask for a ranking, a concrete promising action, a concrete failure mode and a reject-all option. Raw inputs and outputs are disposable under `runs/undissection/`; this file retains assignments, decisions and limits. Player/grader deliverables follow the repository's separate retention rule.

## Source preparation

Completed source preparation: 23 complete OpenStax sections (92,841 whitespace-delimited words, including metadata, exercises and MathML; 377 glossary definitions), original CNXML plus derived HTML/Markdown, pinned to a publisher snapshot explicitly licensed CC BY 4.0. Full local texts are ignored and deletable; copyrighted textbook/workbook references have original study notes instead of full reproductions. The source index records exactly what was read and saved, including access failures and known source inaccuracies. The downloaded edition predates the publisher's later licence change.

## Concept round 1

Two fresh independent reviewers received only Round 1 A/B/C, the grade 10–12 audience, combination format, text-only constraint and worthwhile/hook criteria. Both ranked **B > C > A**. They identified selective filtration/recovery and the distinction between gut contents and internal environment as promising enacted insights. Both warned that four tissue families could support arbitrary organ lookup, a generic regulation tile could conceal the actual causal chain, and walking could be declared before its supporting physiology existed.

Decision: carry boundary/exchange reasoning forward, keep a familiar bodily consequence as the payoff, and compare concrete sequences rather than declare B accepted. The suggested human studies and animated quantities were not performed; current evidence is concept criticism only. Round 2 explicitly respects the existing engine's text consequences rather than presuming a numerical simulation.

## Concept round 2

Two new blind reviewers received D/E/F alone with the same audience and the actual binary/text engine limits. Both ranked **E > F > D**. Selective recovery offered a stronger enacted reversal than simply attaching three organ interfaces to circulation. Both identified the cost of cooling and the limits of conservation as a possible continuation. They warned against water being actively pumped, dry weather being treated as the cause of dehydration, and heart-plus-vessels construction being an entry fee to an interesting later chapter.

Decision: compare a compact water-balance episode, a cooling-led episode and a broader whole-body arc before committing scope. Do not add timers, quantities, blocked-combination feedback or human-study claims that the existing test does not provide. Keep the user's broader undissection ambition visible, while testing the smallest complete arc that can earn expansion.

## Concept round 3 and scope decision

Two new blind reviewers received only G/H/I and the common audience/engine constraints. Both ranked **G > H > I**. They valued filtration → recovery → conditional conservation → replacement as a causal arc. They cautioned that specialised starter parts do not amount to constructing a whole body, that a supplied intestine attached to a body could be an administrative fitting, and that the ADH pathway could become a vocabulary gate. The proposed human comparisons were not conducted.

Adopt **G, A glass of water**, as a small complete episode before broader anatomy. Preserve the larger “few → many → one body” ambition as an expansion hypothesis, not an achieved result. Four connected systems can reveal interdependence without paying an entrance fee of familiar heart/artery fittings. The current prototype still has to earn those connections through play.

## Narrative review assignment

Fresh reviewers receive the current narrative arc, active brief and standing authoring criteria, without concept rankings or this history. Ask whether the questions and player actions drive the next chapter, whether the ending depends on earlier work, and where an apparently meaningful construction is only a label. Separate factual mechanism review from narrative judgment.

### Outcomes and adopted changes

The narrative reviewer retained the conservation-versus-replacement hook but did not endorse four chapters on outline evidence alone. It asked for a quick filtration reversal, a bridge from fixed recovery to variable water needs, distinct contributions from gradient and permeability, and an ending where absorption changes the existing feedback response automatically. It identified the counterfactual test: would a ready-made kidney make the ending equally understandable and satisfying?

The independent physiology reviewer found no premise blocker, conditional on preserving circulation, distinct blood/tubular paths, ordinary proximal recovery before ADH adjustment, a maintained gradient, hypothalamic synthesis versus posterior-pituitary release, evaporative cooling and a modest deficit. Adopted these constraints in the 15-combination draft. A supplied circulation remains the same identity through its early perfusion and later convergence. The finale changes the internal condition; it does not ask the player to switch off ADH or declare perfect recovery after one glass.

The current draft uses a single plain one-pixel SVG for the parser's required image fields. All playable items are text. No anatomical artwork, icon design or graphics evaluation was performed.

## Combination and authenticity reviews

Fresh reviewers saw the first complete 15-recipe manuscript and active brief, without the earlier reviews. The gameplay reviewer retained the glucose/recovery opening and conservation-limit payoff. Adopted: name the gradient-producing input as its loop/vessel assembly; avoid a second circulation hookup that only changes viewing scale; give the intestinal-wall construction an immediate crossing-versus-transport explanation; narrow the hypothalamus primitive so the posterior pituitary adds its release site. The independent authenticity reviewer found the scoped physiology defensible and flagged physical identity in the gradient input and the intestinal wall apparently becoming water. The revised latter result retains the absorbing wall before it joins the body. Added the verified primary reference for anticipatory drinking signals and qualified volume effects as increasingly important with larger losses.

A separate fresh reader received only the public chapter-two scene, goals and six item names (compatibility hints omitted for this isolated probe). First it chose to connect the recovering renal unit directly to the loop, while acknowledging uncertainty about the accompanying vessels. Only after that answer did it receive the proposed loop-plus-vessels pair; it predicted establishing/preserving the gradient and distinguished the still-needed adjustable wall. Adopted the plausible first choice as an alternative assembly order, rather than blocking it for a preferred sequence. This probe supports local intelligibility, not sustained enjoyment.

The resulting pre-playtest draft has **16 authored recipes, 14 required combinations, four playable chapters and one ending**. There are two equivalent orders for the loop/vessel assembly. The additional route replaces the removed redundant circulation hookup; no extra completion steps were added for score or length.

## Baseline Terra fast campaign

[Report](playtests/2026.11.11_02.29.14/report.md), manuscript SHA-256 `f1119215e9cc890ac03de515e534b4c04e3d0a8ced452f550db39d1d2efbcde0`. Three fresh Terra Medium players per chapter, twelve fresh Terra Medium graders and four fresh Terra Medium chapter synthesizers. The adapter actually selected `gpt-6.1-terra`, effort `medium`. All twelve records completed and passed frozen-engine replay/grade validation. Three external worker slots ran the dependency pipeline; final report assembly occurred immediately after the last synthesis. Additional guidance and model/timing metadata are retained in each chapter report. No continuous human or detailed-mode test was performed.

```text
Chapter  Title                                  Fun           Worthwhile  Hook
1        What a filter lets through             not measured  2/3         medium (3)
2        The same kidney, a different output    not measured  4/5         low (1), medium (2)
3        Cooling costs water                    not measured  3/3         low (1), medium (2)
4        A drink reaches the cells              not measured  1.7/3       low (3)
```

The lower-half worthwhile screen selects chapters 1 and 4; the no-high-hook screen selects all four. Chapter 3's full worthwhile count does not establish a compelling game: all three players found the connection to the kidney predictable, while valuing what its explanation taught. Across the campaign, the glucose reversal, gradient-plus-permeability distinction, conservation limit and changed renal response to a drink were valued. Repeated fittings and missing mechanism explanations weakened interest. Normal compatible-pair hints are part of the game; these findings do not justify hiding them or manufacturing puzzles.

### Revision hypothesis

1. Bundle the initial filter/tubule plumbing so the first action immediately reveals useful glucose entering filtrate. Preserve the separate blood and tubular routes in the supplied assembly.
2. Bundle the loop/vessel preparation into one concrete countercurrent assembly, and explain how unequal limb permeability, salt transport and accompanying blood flow maintain a gradient when it joins the earlier renal unit. Remove one low-value fitting, rather than multiply specialist labels.
3. Keep the valued cooling/conservation passage. Offer a choice between dry and humid warm settings with unreplaced sweat loss. The choice must alter evaporative cooling while preserving the common water deficit, giving the environment an actual physiological role rather than introducing an arbitrary fork.
4. Bundle the intestinal lining/capillaries and spend the remaining actions on absorption and its consequence. Explain solute transport and osmotic water movement, addressing the missing mechanism rather than simply repeating that water crosses.
5. Remove the empty ending chapter. Structural analysis showed that it cleared the final body from the current board (zero items at that chapter), contrary to the intended convergence. The final result should remain the single body; no extra victory object or action is needed.

Run fresh narrative and authenticity-director reviews, then retest all four affected chapters with identical guidance, model, effort and mode. This is a test of less preparatory work plus more substantial relationships, not an attempt to inflate a decision score. If hooks remain weak, retain that finding and do not expand anatomy coverage to conceal it.

### Independent director review and revision 1

Fresh story and authenticity directors received only the current baseline manuscript, active brief and relevant standing/source guidance, not the results above. The story director independently recommended compressing preparatory assemblies, retaining the gradient/permeability construction and the conservation-limit turn, and returning the final response to the initial glucose-recovery thread. It considered the initial filter/tubule orientation defensible; the actual unanimous reports of low value were the reason to bundle it anyway. The authenticity director found no essential inaccuracy and requested that the loop/vessel gradient be stated as depending on established tubular and blood flow. The revision includes that condition.

Revision 1 has 13 authored recipes and 11 required actions across four playable chapters. It starts with three items, peaks at five along the debugger route, and ends on one body. The earlier alternate loop-fitting order disappears with the bundled preparation; the new dry/humid alternatives change the resulting condition. The hormone-release branch remains separately constructible because its connection to the kidney received positive local value, despite the director's optional suggestion to bundle it too. The ending explicitly keeps glucose recovery and waste excretion operating while extra water conservation eases.

## Revision 1: all-chapter retest

[Report](playtests/2026.11.11_02.41.16/report.md), SHA-256 `8baff46cadae24e33f5943d4e3473377b6516305e3ee05646f42884ee0316268`. Same guidance, mode, model, effort, three-player design and independent grading/synthesis as baseline. All twelve playthroughs completed and verified. These are new participants, not returning players experiencing improvement.

```text
Chapter  Title                                  Fun before    Fun after     Worthwhile before  Worthwhile after
1        What a filter lets through             not measured  not measured  2/3                2/2
2        The same kidney, a different output    not measured  not measured  4/5                4/4
3        Cooling costs water                    not measured  not measured  3/3                2.7/3
4        A drink reaches the cells              not measured  not measured  1.7/3              2/2
```

The three preparatory cuts reduced the completion route from 14 to 11 actions. The credited-action counts for chapters 1 and 2 stayed the same; their fractions improved because low-value work was removed, not because more value was demonstrated. Chapter 4's explicit mechanism explanation received credit from all three players. Chapter 3 fell slightly on the broad worthwhile measure despite the new environmental choice; one player found the skin/kidney hookup repetitive. Preserve that contrary result.

Two players chose the humid walk to test limited evaporation; one chose the dry walk and predicted cooling. All three graders credited that choice as meaningful in the fast diagnostic. This is evidence of one reasoned comparison opportunity, not a human-fun result or a substantial replay loop. Hook was medium for all players in chapters 1–3, and low/medium (2 low, 1 medium) in chapter 4. **No high hook was reported.**

Chapter 4 trials used the debugger's dry-route checkpoint history. They did not continue the chapter 3 participants' chosen paths. The humid branch's convergence was checked by the shared-engine replay and factual reviewers, not by a continuous player experiencing that branch through the drink.

## Final director reviews and focused ending retest

Two fresh directors saw the revised manuscript and active brief, without playtest scores, history or earlier criticism. The narrative director recommended **retain as a small teaching prototype; do not expand as-is**. It valued interdependence and the limits of conservation but judged the weather fork an authored observation rather than a substantial replay hook. It requested a concrete change in urine output in the final result. The authenticity director found no factual blockers across all 13 recipes, including both environmental paths and convergence; it cautioned that “Regulated kidney” includes a brain-to-kidney relationship whose separate locations must remain clear in any future representation. No artwork is authorized here.

Adopted the final-output clarification: as extra recovery eases, more water can leave as urine and the urine becomes less concentrated than during the strongest conservation response. Retested chapter 4 only with three new players, graders and a new synthesizer; other chapters were unchanged.

[Focused report](playtests/2026.11.11_02.46.52/report.md), final manuscript SHA-256 `04b834d57f51b19663a0262620fca34a66298dc03c296a57050e64e2c60dda30`.

```text
Chapter  Title                       Fun before    Fun after     Worthwhile before  Worthwhile after
4        A drink reaches the cells   not measured  not measured  2/2                2/2
```

Before is revision 1; after is the focused final run. Hook remained low/medium (2 low, 1 medium). The clarification improved explicitness, not the measured hook verdict. Players still found the whole-body response useful while describing a prescribed action followed by a substantial explanation. Across all three campaigns there were **27 actual chapter playthroughs, 27 fresh independent grades and nine fresh chapter syntheses**, all Terra Medium, with 81 accepted gameplay actions in total. These totals describe separate local trials, never a continuous 81-action story.

## Current judgment and stopping point

The worthwhile **subject** is established enough for a small prototype: useful substances must be recovered after filtration; a gradient and a permeable route do different jobs; cooling costs water and depends on the environment; conservation cannot replace a loss; absorption changes the response of the same body. The combinations make some relationships concrete, especially the glucose reversal, gradient/permeability construction and environmental choice.

The **hook remains unproven and weak in these AI reports**. Strong credited-learning counts coexist with low or conditional desire to continue. Much of the reward still comes from the explanations; do not infer that this format has an advantage over an equally good illustrated reading. The target age group, retained learning, cumulative attachment, browser dragging and human enjoyment were not evaluated. Fast-mode Fun is not measured.

Retain this small complete episode as a reviewable development result. Do not expand into a full anatomy catalogue, add more regulation chains, commission art or promote it to the published catalogue on this evidence. The larger undissection idea remains interesting, but this particular construction pattern has not earned that expansion. A human reading/playing this compact draft would supply more useful direction than another round of optimizing its AI scores.

## Final verification and retention

- `npm run lint -- projects/undissection/undissection.md --details`: zero errors, zero warnings on the final version.
- `npm run analyze -- projects/undissection/undissection.md --json --details`: complete legal route, 25 items (13 primitive, 12 derived), 13 authored recipes, 11 completion actions, four playable chapters; starting boards 3, 5, 5, 3 and route peaks no higher than 5. The draft is deliberately much smaller than Cookbook/Settlement; count comparisons do not establish quality.
- Explicit shared-engine replays selected each of the dry and humid branches. Both completed in 11 combinations with exactly one available item on the final current board: **Body responding to a drink**. This checks the two defined paths, not every possible action ordering.
- A Chromium smoke check opened the local draft at a 390 × 844 viewport, entered through Start/Begin and found the opening items; HTTP 200, no page errors. It was not a visual-design, geometry or human-usability evaluation. The existing development server was left alone.
- All 27 actual sessions and independent grades passed frozen-runtime replay, protocol coverage and arithmetic validation. Report syntheses preserve original graders' classifications; mean worthwhile counts and aggregate hook labels were checked against the attributed details. Run reports were mechanically assembled from marked chapter syntheses.
- Local source conversions retain publisher attribution, licence, source URLs and checksums. Full downloads remain ignored and deletable under `sources/local/`. No copyrighted textbook/workbook was retained in full. Selected response arrays and chapter/run reports stay with the project; disposable sessions, prompts, intermediate grades, logs and analysis dumps are removed after verification.

No application code, production story, shared UX rule, published host or artwork set changed. This active project is not ready for promotion or archiving as an accepted story.


## School-level reset

The user judged the renal story far beyond the desired audience, then authorized a new attempt for grades 8–10. This is a replacement of the active manuscript, brief and arc, not a claim that simpler wording makes the renal mechanisms suitable. Earlier scores above apply only to that superseded draft. The current project remains active; no catalogue promotion or graphics is authorized.

### Concepts and scope

Two fresh blind reviewers compared three new candidates: **A, Lift a glass**; **B, Keep going**; **C, From a sandwich to a hand**. They received only the candidate sketches, audience and format constraints. Rankings were A > C > B and C > A > B. A supplied the strongest immediate action, opposing muscular pulls; C supplied a clearer convergence of food, air and blood. Both doubted whether a claimed continuation of activity could be earned by a text-only engine, and whether kidneys and temperature regulation belonged in a single reach.

Adopt A's mechanical opening and C's supply connection. Put sensory control before the supply chapters, so the brain is not a final life switch. Omit renal and temperature detours. The resulting fourteen-combination arc uses bones, muscles, nerves, eyes, lungs, heart, blood vessels, stomach and small intestine. It ends with one body lifting a glass. It models selected relationships and supporting assemblies, not exhaustive human anatomy or resurrection.

A separate source/scope reviewer grounded the organ-system level in NGSS MS-LS1-3 and HS-LS1-2, identified stored-fuel and muscle-braking cautions, and added licensed OpenStax 9.4 and 11.1 to the earlier source snapshot. The local library now contains 25 sections, 101,716 whitespace-delimited words, 418 glossary definitions and 114 figure descriptions. These remain author reference, not a student reading list. See the source index for the pinned license and retrieval limits.

### Fresh manuscript reviews

Two new independent reviewers read the school manuscript and active brief without earlier reviews or playtest records. One assessed age prerequisites and narrative; the other assessed physiology and combination relationships. Neither identified a blocking physiological defect; both found the school level plausible with prior basic biology. That is adult expert judgment, not demonstrated student accessibility.

Adopted fixes: replace “Air has to reach the arm” with “Oxygen has to reach the arm”; put the complete heart → lungs → heart → body → heart route in required text; explain the thin-walled meeting place between air and blood; define cells, tendons and nutrients in mandatory result paragraphs; replace “contract,” “levers” and “sensory information” with ordinary descriptions. The required food result explicitly mentions the delay in absorption and stored fuel. The ending now discovers that holding the glass still also requires muscle pulls and energy, reconnecting it to the first chapter.

The reviewers independently expected sight and meal preparation to be the weakest actions. Both serve explanatory contrasts, but their actual experienced value remains for the playtest to assess. No harder guessing or extra anatomy steps were added.

### School baseline assignment

Four chapters; three fresh Terra Medium players per chapter, twelve fresh Terra Medium independent graders, and one fresh Terra Medium synthesis reviewer per chapter. Actual adapter selection: `gpt-6.1-terra`, `model_reasoning_effort="medium"`, with shell, apps and web disabled. The CLI model label alone is not relied upon. Each invocation is ephemeral and receives only its public assignment packet; players retain their own chapter's exact public history through subsequent packets. Synthesis intentionally sees its three records and grades. No reviewer receives earlier findings or a future recipe.

Mode: `--fast`; fun is not measured. Guidance identifies grades 8–10 and familiar biology, excludes assumed specialist anatomy/cellular chemistry, and requests honest assessment. Its exact wording is retained in every chapter report. A three-worker completion-driven pipeline immediately schedules grading and synthesis when prerequisites complete, then mechanically assembles the report. Whole-story chapter coverage uses fresh participants at each checkpoint, not a single person's cumulative attachment.

Baseline manuscript SHA-256: `11efb33e980043fa16ed86e12de0a6d650a4599a0da481f5645bf49224fa07c0`. Verified outcomes follow below.

### School baseline outcomes and revision

[Baseline report](playtests/2026.11.11_09.33.43/report.md): all twelve chapter assignments completed and replay-verified; 42 gameplay actions in total. Three fresh records per chapter. Chapter synthesis credited the following average counts, using the standing either/or worthwhile definition; `--fast` does not measure fun.

| Chapter | Worthwhile | Hook judgments |
|---|---:|---|
| A muscle can only pull | 1.7/3 | 1 medium, 2 high |
| Where should the hand go? | 2/3 | 1 medium, 2 high |
| Oxygen has to reach the arm | 2.7/3 | 3 high |
| More than an arm | 5/5 | 3 medium |

The first chapter exposed an authoring defect: the three slot conditions were written within one prose block, so the parser treated them as literal text and showed all the muscle explanations when the empty arm was created. This made later fittings repetitive and could imply muscles were already fitted. Lint alone did not catch that semantic presentation mistake. Separate repeated `Arm` declarations now give each condition its own wonder block. Direct engine inspection confirms one unconditional reading and three correctly gated readings, and no tendon/muscle explanation on the initial joint construction.

All three air-chapter players identified the missing link between breathing muscles and changing chest space. The revised result explains the diaphragm pulling down, other muscles lifting ribs, lungs expanding, and passive recoil during quiet breathing. No additional anatomy operands or technical pathways were introduced.

The ending's holding-still discovery was valued by all three players. The supply/control join was predictable or repetitive for two, while still clarifying distinct jobs. Retain that necessary binary convergence and its explanation; do not add arbitrary choices simply to increase decision counts. Hook remained medium at the ending, so this is not evidence of a uniformly compelling story.

The second campaign repeats all four chapters with fresh participants because every later checkpoint includes the revised opening history, and chapters 3–4 also include the changed breathing explanation. This is a specific exposure change, not routine repeated testing. Revised manuscript SHA-256: `8defaa3a50ce43a0f2dd2f6f17097fed93eafe33a686a303f21a70190fa1532e`. Same guidance, models, mode and pipeline.


### School revision outcomes and current judgment

[Revised report](playtests/2026.11.11_09.38.22/report.md), matching the current manuscript: twelve completed, replay-verified chapter assignments and twelve independent grades, with four fresh chapter syntheses. Forty-two actions; three fresh players per chapter.

| Chapter | Baseline worthwhile | Revised worthwhile | Revised hook judgments |
|---|---:|---:|---|
| A muscle can only pull | 1.7/3 | 2/3 | 1 medium, 2 high |
| Where should the hand go? | 2/3 | 3/3 | 3 high |
| Oxygen has to reach the arm | 2.7/3 | 3/3 | 1 medium, 2 high |
| More than an arm | 5/5 | 5/5 | 3 medium |

These are averages of credited actions and total actions separately, not percentages or learning gains. All independent graders classified the recorded fast-menu decisions as non-meaningful; worthwhile credit comes from evidenced value in results. Fun is not measured by this mode. The changes in tiny independent samples do not isolate a causal effect of revision, and high hook in earlier chapters does not establish cumulative whole-story attachment. The ending retained medium, conditional interest despite its valued payoff.

The reveal-timing defect is gone. Bending-muscle installation now produces the explanation that all three opening players named most worthwhile. The straightening installation remains predictable and repeats the tendon definition, which is kept so either fitting order is understandable. The breathing result now explains muscular expansion and quiet recoil; this revision's players did not repeat the earlier missing-muscle-mechanism criticism. The gas-exchange convergence remained valued by all three.

All three final-chapter players valued the discovery that holding still takes continuing muscle effort. Digestion versus absorption and stored fuel also earned specific positive reactions. Remaining questions concern how position is sensed and how oxygen supports energy release. Keep those as known limits of this selective organ/system model; do not add microscopic mechanisms simply to satisfy adult curiosity. Required assembly remains predictable, particularly at the supply/control join.

**Current judgment:** retain this small, playable school-level prototype. Its connections and ordinary-action payoff justify trying it with the intended audience, but the AI evidence does not establish that it teaches or entertains students. It is a guided construction toy with worthwhile explanatory results, not yet a strong inference game. Further expansion, a full-body inventory, homeostasis episodes or artwork should depend on the user's response and target-age evidence, not these scores alone.

### Final independent review

A fresh final reviewer read only the revised manuscript, active brief, school scope and authoring criteria, without playtests or previous reviews. It found no blocking biological inaccuracy or causal gap at the intended scale and judged the four-part arc coherent. It identified holding still as the strongest ordinary-experience payoff and the school prerequisites as plausible with basic biology.

Its main limitation is consequential: successful assembly does not show that the learner can reconstruct the explanation. Its suggested next evidence is transfer to another familiar action. The organ–tissue–cell hierarchy is only partly stated; that remains outside this episode's learning target rather than becoming another required label sequence. These are expert judgments, not a target-age study.

### Final verification and retention

The current manuscript passes story lint with zero errors and one reviewed mixed-fate warning: the arm remains while muscles are fitted, then transforms into the guided arm. That is intentional identity progression. The analyzer finds four chapters, fourteen combinations, a fourteen-action completion route and at most six arriving items. Direct engine runs checked both muscle-fitting orders crossed with both breathing/circulation preparation orders; all four routes complete in fourteen actions with exactly one available result, `Body lifting a glass`.

A Chromium check at 390 × 844 loaded the draft and performed the opening drag combinations. The empty arm shows only its joint explanation, the first muscle shows its own result, and the second fitting shows the opposing-pair result. No browser errors occurred. No artwork or screenshots were produced.

Both school campaigns retain their requested original response arrays, independent chapter reports and mechanically assembled reports. All 24 response arrays were compared with their frozen session replies, including harness-owned look flags; 84 actions and all independent grading totals match. Each session completed and replay verification passed; hashes and identical guidance were checked, along with exact copying of the eight marked chapter syntheses into the two assembled reports. Detailed action tables support the displayed worthwhile averages. Runtime snapshots, packets, CLI adapters, raw logs and temporary reviews are disposable scratch and were removed after these checks. The licensed full source texts remain ignored under `sources/local/` for the ongoing development project.


### Saved-progress mismatch reported after the rewrite

On 2026-11-11 the user reported the continuation-removal error for the opening arm pair and brain/nerves, both offered together in chapter 1. They confirmed having opened an earlier draft at the same browser address and that **Restart story** resolved the error. The current manuscript's fresh initial inventory has only the arm construction; brain/nerves arrive in chapter 2.

Investigation checked every combination/advance transition in the fresh logical story (21 distinct logical states, 40 directed transitions, no failures) and a complete 14-combination Chromium playthrough (no errors). A small separate reproduction confirmed that `reconcileLiveStory` can preserve a consumed ingredient across a changed recipe, leaving an already-impossible saved position while still offering other compatible pairs. Those pairs then raise the generic continuation-removal error. The user's exact local snapshot was not inspected; their restart outcome and mixed inventory are consistent with this restoration path. This does not establish a defect in the current fresh manuscript, but exposes a browser restoration gap and a misleading error. No application code was changed during this diagnosis. The unresolved recovery work is tracked in the cross-project backlog. Disposable reproduction scripts were removed.
