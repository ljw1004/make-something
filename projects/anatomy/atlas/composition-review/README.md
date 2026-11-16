# Chapter composition review

This revision applies the [composition review method](../../../../docs/icon-guide.md#review-the-construction-not-just-the-cutouts) to every playable chapter of [Anatomy](../../anatomy.md). The [active brief](../../design-brief.md) owns the story decisions. Selected artwork and its exact generation requests live in the corresponding specimen packages here; detailed reviewer transcripts and frozen packets are disposable under `runs/`.

Each chapter receives a new independent, ephemeral reviewer conversation. Each revision receives another new conversation. Producers never act as their own independent reviewers. Reviewers see the complete inventory, actual combination rules and operand/result strips at the same playing scale. They do not receive the user's flagged chapter list, earlier verdicts or production explanations. These are informed visual reviews, not blind recognition or measured learning outcomes.

The first pass preceded the user's explicit permission for synecdoche. Later reviews allow a representative cell or sample to stand for numerous instances; count-only objections are superseded. Physical continuity, comprehensible parts and a natural standalone whole remain required. Chapter 18 was independently accepted under the clarified rule without manufacturing a larger molecular inventory.

The loop is concrete: freeze the current chapter, obtain the independent diagnosis, repair its physical units or whole-and-parts artwork, integrate the actual playable assets, and send a new frozen packet to a fresh reviewer. Accepted chapters stay unchanged unless a shared asset or recipe changes. Registration checks alone never establish visual acceptance.

## Tools

Run from the repository root:

```sh
node projects/anatomy/atlas/integrate.ts
node projects/anatomy/atlas/composition-review/prepare.ts ROUND
python projects/anatomy/atlas/composition-review/render.py runs/anatomy-composition-review/ROUND
python3 projects/anatomy/atlas/composition-review/run-reviewers.py runs/anatomy-composition-review/ROUND CHAPTER_NUMBERS
python projects/anatomy/atlas/composition-review/verify-reviewed.py runs/anatomy-composition-review/ROUND
python3 projects/anatomy/atlas/composition-review/summarize.py runs/anatomy-composition-review/ROUND
```

Use a Python environment with Pillow for rendering and the individual package dependencies for extraction. Choose a new round name; the preparer rejects existing or previously retained round names. Never overwrite a packet while it is being reviewed. The runner refuses to overwrite an existing chapter verdict and uses the explicitly authorized local Codex executable, a read-only sandbox, no model override and one new process per chapter. It attaches the inventory and all operation strips directly, in addition to allowing inspection of frozen individual assets. `reviewer-instructions.md` is the exact neutral assignment; the structured response includes all three criteria, each operation and specific repair suggestions.

`apply-descriptions.py FILE.json` updates physical description braces after a selected artwork change. Semantic changes remain deliberate manuscript edits, followed by native lint, legal replay and graphical play. `integrate.ts` merges replacement maps after the original atlas and resolves the illustrated manuscript's identity aliases.

`verify-reviewed.py` compares the pixels, dimensions, object identities, fittings and actual operations of the final packets with independently accepted versions. This catches later shared-asset changes that would otherwise invalidate an earlier acceptance. Final accepted chapter fingerprints remain in the concise outcome record, so later reviews can compare against them after the raw packets are discarded. It does not certify prose or medical correctness. After final browser playback, pass the matching packet directory to `atlas/make-sheets.py` to retain the requested construction lists and ingredient/result strips alongside the contact sheets.

See [concise outcomes](outcomes.md) and [chapter findings](outcomes.json). These retain verdicts and evidence limits; raw captures, frozen source copies, prompts sent to reviewers and event logs stay in ignored scratch storage and are removed after the final verification record is written. Requested artwork, contact sheets, recipe illustrations and selected production sources are retained separately.
