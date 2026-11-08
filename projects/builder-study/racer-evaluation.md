# Independent racer revision

## Scope and review instructions

Rebuild the former fixed racer as two chapters: assemble a mast/sail, then
construct two literal straw-and-two-wheel units, fit bearings and wheels beneath
a movable chassis, flip it upright and attach the sail. The pinwheel remains
independent; remove its aiming dependency and the starting gate. Follow the
[live brief](../../stories/builder/design-brief.md), including quiet instructions,
connected parts, flexible scale families and the new vintage material palette.

Fresh mechanical reviewers inspect the dimensioned model, actual evaluated
meshes, additive state subsets, attachment paths and wheel rotation. Fresh
visual reviewers inspect every opening step in real browser captures, including
short phones and alternate fitting orders. They check visible additions,
connected draggable parts, usable pickup areas, current goals, outlined processes,
picture references and continuity across flips. They must distinguish nominal
geometry and informed visual evaluation from manufactured performance or human
enjoyment. Revised candidates require fresh reviewers.

## Logical iteration

The [v33 one-player fast screen](playtests/2026.11.07_22.53.51/report.md) completed
both chapters, reporting medium hook and explicit satisfaction at the completed
sail and racer. It found the repeated second axle predictable. An author check
then replaced combined half-axle goals with separate front/rear instructions:
requiring both intermediate axles simultaneously could retain an obsolete half
assembly if the player finished one axle before starting the other. The two
straws and their axle stages now have short front/rear labels; any Wheel still
fits either Straw.

The [v34 three-player detailed trial](playtests/2026.11.07_22.58.43/report.md)
completed all six assignments. Sail: 1/4 worthwhile actions, 0/4 meaningful
decisions; chassis: 1.7/10 worthwhile actions, 0/10 meaningful decisions, with
medium hook in both chapters. All three players valued the final sail fitting
and final racer attachment. Repeated rear-wheel construction was less engaging.
One player found the raw Sail and completed Sail names confusing in text output.
The visual game uses their distinct pictures and deliberately short labels.

These are text-only results. They establish guided completion, not visual
satisfaction, touch quality or enjoyment by ten-year-olds. The requested literal
wheel construction is retained, rather than converted into a guessing puzzle or
collapsed into a token representing multiple separate parts. A human visual
playtest remains necessary to judge that tradeoff. v35 changes presentation from the v34 graph. v36 additionally lists loose parts
first in each symmetric recipe, so the canonical browser route fits parts onto
the workpiece; both actual drag directions remain legal. It also adjusts display
sizes after a crowded smallest-phone pilot. Neither changes the physical recipe
graph or the instructed sequence.

## Mechanical iteration

The first independent review rejected the original sail/connector overlap.
Moving the lower cloth corners outward and adding two integral tabs preserves
connected clips while clearing the connector. The revised nominal clearance is
about 0.53 mm. A separate fresh review then identified flat-ended locking barbs
as incompatible with the depicted straight-push insertion: a flat leading face
cannot supply the inward force component. The correction adds tapered lead-in
faces while retaining square locking shoulders. Neither review supplies an
acceptance of its subsequent revision.

## Graph verification

The shared-engine checker exhausts 23 sail states/46 transitions and 286 chassis
states/1,870 transitions, including latched-goal differences. Every terminal is
complete in four or ten successful actions respectively, with only its finished
movable assembly left. No unfinished terminal or duplicate retained part remains.
Both bearing orders, interleaved wheel-unit installation and all interchangeable
wheel choices are covered. The full 235-recipe, 31-chapter manuscript has a
195-combination completion route. These graph checks do not assess visual
recognition, real mechanics or enjoyment.

The [v36 fresh fast screen](playtests/2026.11.07_23.11.29/report.md) again completed
both chapters without interface confusion. Its one player per chapter reported
medium hook, 1/4 worthwhile sail actions and 1/10 worthwhile chassis actions.
The final attachment remained the payoff; repetition remained the limitation.
Fast mode does not measure meaningful decisions.

## Selected mechanical candidate

A new independent reviewer accepted model SHA-256
`d9057a28a9868460530a513c0424dce6cee01e9a20494f256b495981025d9c9d`
with plan `245e417540619c961ec8c954b2601c6e9db304c1573883c2063675ed6c91b6fd`
and palette `3b81148966748129688daf0e475c8b37b7f4080ed87abc31e2f9a118ed4e43d7`.
All 14 prepared parts are connected, every stage retains its installed geometry,
and the chassis flip is rigid. The ramps lead into the real openings. A continuous
1.56 mm inward displacement envelope per leg fits both sets of retaining barbs,
leaving at least 0.88 mm between opposing legs. The foot's conservative insertion
margin is approximately 0.042 mm. Both axle/wheel units clear all 72 sampled
five-degree orientations and continuous radial/axial envelopes throughout 360°.
The sail clips share a common fitting direction and their tabs keep the cloth
clear of the connector.

This acceptance concerns ideal nominal geometry. Compliant grip ribs and lining
have intentional interference; material strain, fitting force, manufacturing
tolerances, reliable retention, friction and wind performance remain unvalidated.
The narrow foot margin is not evidence of a reliable manufactured snap. The
pinwheel's geometry is unchanged from its earlier accepted version; this pass
changes its material colours, cover and identity image.

## Display iteration

The first smallest-phone pilot completed the route but its ten loose chassis
pieces crowded the goal. Loose wheel/straw/bearing views and the carried sail
were reduced, while retaining large assembly/finished-object views. The half and
complete axle now share camera, crop and magnification. Listing the loose supply
first in symmetric recipes makes the canonical checker exercise parts onto the
workpiece; either real drag direction still works. The follow-up 320×568 pilot
completed all 23 operations with readable current instructions. Completed toys
remain large enough to overlap some control-area space; actual continuation and
pickup accessibility are checked separately from rectangular image overlap.

## Final visual and production checks

A fresh independent visual reviewer accepted candidate v36 SHA-256
`67f58cd75314b17fb5013fbf35b7d36325cc561393318c8b090b116a97d4d40f`,
inspecting all 43 item assets, the icon and 108 actual browser captures. Both
construction families and alternative stages preserve connected components,
visible additions and coherent flip views. The new material palette reads
clearly on white. No hidden current goal text was found. Independent probes
confirmed reference enlargement at 320×568 and touch pickup six pixels outside
the slender handle's artwork box.

The deliberate desktop reverse-hub route can leave the enlarged pinwheel over
much of the required Flip drawing. The reviewer reproduced this and completed
an ordinary handle drag into open space, followed by Flip. This remains an
accepted, recoverable layout weakness with large movable objects, not evidence
that every arrangement leaves every process visually exposed. The review is
informed visual/interaction evidence, not a blind-recognition or child-enjoyment
study.

The compiled static game completed all 23 opening combinations at 390×844,
390×664, 320×568 and 1280×900. Phone runs used emulated touch. Checks cover every
result remaining movable, zero routine popups, minimum 44px touch areas (with
subpixel tolerance), free movement, the other bearing order, reverse-direction
hub attachment, reloads, chapter transitions and continuation into the original
marble-game chapter. There were no page errors, failed requests or undecodable
images. The complete shared-engine route and every one of the 43 new recipes
also passed; all selected asset/source/manuscript hashes agree. Type checking,
production build and diff checks pass. Application logic is unchanged, so this
pass did not repeat the previous full engine/browser regression suite.

Live lint has zero errors and four warnings. The existing rover mixed-fates and
20,000-state fixed-analysis-bound warnings remain. Two new pessimistic
opportunity warnings concern using Wheel 1 as the second wheel on either axle:
the analysis's chosen half-axle construction already uses that copy. Exhaustive
actual shared-engine traversal supplies execution witnesses for both recipes
by using another wheel first, as well as all other recipes. These are analysis
coverage limits, not absent playable branches; the warnings are retained.
The build retains its existing root-output and bundle-size advisories.

Selected artwork and the manuscript were promoted to `stories/builder`.
Obsolete gate, aiming, fixed-racer, carried-pinwheel and racer-reward assets were
removed. The source models, export settings, current brief and actual attributed
playtests remain in the study. Temporary masters, captures, logs, reviewer
packets and detailed geometry output were discarded after this outcome record.
Animation and migration of the later chapters remain separate work.
