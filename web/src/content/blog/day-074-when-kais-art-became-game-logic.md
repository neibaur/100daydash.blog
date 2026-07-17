---
title: "Day 74 - July 14, 2026: When Kai's Art Became Game Logic"
description: "A Day 74 reflection on turning Kai's drawings into Boo-Boo Quest behavior while preserving orientation, collision, timing, naming, and honest testing boundaries."
pubDate: "2026-07-14"
day: 74
dashboardSlug: "none"
dataSources:
  - "Kai Boo-Boo Quest gameplay feedback and supplied artwork"
  - "Boo-Boo Story PR #52 through PR #57 implementation and validation notes"
  - "Boo-Boo Quest CI and security-workflow results"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - boo-boo-story
  - boo-boo-quest
  - client-feedback
  - game-development
  - asset-pipeline
  - animation
  - testing
  - scope-management
---

Kai's bug report sounded visual and straightforward.

The new Boo-Boo-1 character faced the wrong way. Its legs needed to move. The
game should use the selected character's proper name. The house looked like a
small corner instead of his complete drawing. The circular and spiky enemies
should be replaced by his bad-guy character. The Flame Thrower should use both
of his fire drawings so the flame looked alive.

Each observation was precise.

None could be solved faithfully by dropping a PNG into a folder and calling
the work complete.

Every drawing carried a behavioral assumption that the game needed to
understand: which way the subject originally faced, how one image could appear
to walk, whether a larger picture should create a larger collision area, how
two fire frames should advance, and which words should change with the selected
skin.

During the July 14 work session, six narrow Boo-Boo Story pull requests turned
Kai's feedback into those rules. Some GitHub timestamps crossed midnight UTC,
but the sequence belonged to the same working session.

The drawings stopped being reference material.

They became part of the game's logic.

## The Art Had To Remain Kai's Art

The first task was not animation or rendering. It was preparing the supplied
phone photos and drawings for the game.

[PR #52](https://github.com/neibaur-labs/boo-boo-story/pull/52) created archival
and 256-pixel transparent PNGs for the bad guy, both fire drawings, and the
complete house. The phone photos needed their EXIF orientation corrected.
Their backgrounds needed to disappear without removing the marker and ink
texture that made the drawings Kai's.

The outputs were RGBA images with transparent alpha channels. Each `-256`
derivative had a longest edge of exactly 256 pixels. Orientation,
transparency, crop boundaries, and retained detail were checked visually, and
the reported validation completed with 21 test files and 138 tests passing.

One implementation detail mattered because it established an honest boundary.

The repository's existing `process_scan.py` script did not expose the
value-and-saturation command-line mode referenced by the task. Rather than
pretending it did, or expanding a shared pipeline to justify one immediate
need, the photographed assets received a focused HSV segmentation treatment
matching the existing gold-marker artwork.

No processing-pipeline code changed. No dependency was added.

That was not a failure to automate. It was a decision to tell the truth about
what the current tool supported and keep an asset-specific treatment
asset-specific.

Processing also did not redraw the pictures into a cleaner house style. The
goal was to make Kai's marks usable in the game while preserving the evidence
that they came from his hand.

## A Drawing's Direction Is Data

The facing bug exposed an assumption hidden inside the images.

The default Boo-Boo art was drawn facing right. Boo-Boo-1 was drawn facing
left. The game had one shared mirroring rule, so applying that rule to both
skins made one of them look away from the direction of travel.

[PR #54](https://github.com/neibaur-labs/boo-boo-story/pull/54) added a pure
`spriteFlip(skin, facing)` helper. The helper accounts for the original
orientation of each drawing and is used in both gameplay and the title-screen
playground.

The image itself did not contain a machine-readable label saying "I face
left." Once the drawing entered an interactive system, that orientation
became data the renderer needed in order to behave correctly.

The same pull request repaired the missing walk effect. Boo-Boo-1 had been
rendered as one static image outside the normal walk-frame path. Every player
skin now uses the shared `walkFrameIndex()` cadence.

Kai had supplied one Boo-Boo-1 drawing, not a newly drawn animation set. The
alternate pose is therefore a mirrored version of the same image. That small
shift makes the feet visibly alternate without inventing skin-specific
animation configuration. If new walk art arrives later, it can replace the
generated alternate while leaving the timing rule intact.

Naming followed the same principle. A pure `heroName(state)` helper now lets
existing player-facing messages say `Boo-Boo-1` when that skin is selected.
Respawn, heart-container, boss-victory, cave, dance-cooldown, and accessibility
text follow the selected hero. Clone messages intentionally still say
`Boo-Boo`, because the clones still use the original Boo-Boo art.

The change did not add a permanent name label to the HUD. Kai's bug concerned
existing player-facing uses of the name. A new display would have been a
separate product feature.

The reported local validation passed with 145 tests. More importantly, the
fix gave the two drawings parity through small shared rules rather than a new
skin framework.

## The House Was Larger Than Its Collision

The old house was technically visible. It was also only a procedural corner-like
approximation of the place Kai had drawn.

[PR #55](https://github.com/neibaur-labs/boo-boo-story/pull/55) replaced that
approximation with the complete house image. The roof, door, and "car shop"
sign became visible, and the artwork was centered over the existing two-by-two
house tile block.

Making the picture larger raised a gameplay question: should the collision
area grow with it?

The answer was no. The visual representation changed, but the level's geometry
did not. The original four solid tiles remained the collision footprint, and
the surrounding ring stayed walkable.

Tests pinned those tile rules so a future rendering change cannot silently
turn the larger house into a larger invisible wall. The old box-and-roof
doodle remained only as an image-loading fallback.

This was also a useful boundary around the evidence.

The repository did not have a canvas-rendering test harness. The tests did not
prove that every pixel of the house appeared correctly. They proved the
important gameplay invariant available to unit testing: replacing the image
did not change where the player could walk.

Visual inspection covered the rendered art. Unit tests covered collision.
Neither kind of evidence was described as the other, and the reported local
validation passed with 140 tests.

## Two Fire Drawings Needed One Small Clock

Kai supplied two drawings for the Flame Thrower. The game needed to alternate
between them, but it did not need a generalized animation architecture.

[PR #53](https://github.com/neibaur-labs/boo-boo-story/pull/53) introduced a
pure `flameFrameIndex(t)` function and one timing control,
`FLAME_FRAME_MS = 120`. The frame is derived from the accumulated flame timer
the game already maintained.

There is no `setTimeout`, `setInterval`, `Date.now()`, sprite-sheet system, or
animation framework. Existing game time selects one of two drawings.

That choice also made pause behavior correct without additional state. When
gameplay pauses, its timer stops advancing, so the current flame frame freezes
naturally. The old procedural cone remains only as an image-loading fallback.

The reported local validation passed with 142 tests.

A richer visual result came from one small deterministic rule. The code did
not need to become more general than the feedback.

## The Bad Guys Joined The Same Motion Language

The placeholder enemies had different procedural appearances: circles and
spiky doodles. Kai wanted both to become the bad-guy character from his
drawing.

[PR #56](https://github.com/neibaur-labs/boo-boo-story/pull/56) removed the
placeholder drawing code and used `boo-boos-256.png` for both wanderers and
chasers. Unlike the house and flame, the old enemy doodles were not retained
as a fallback.

The art changed. Enemy behavior did not.

AI, movement, hit points, damage, collision, knockback, fire state, and the
water and fire dressing all remained intact. The gameplay still classifies
the two enemy types as round and spiky, including their different interaction
with the Flame Thrower.

The enemies reuse the player's `walkFrameIndex()` cadence. Because Kai
supplied one bad-guy image, a mirrored version supplies the second step. A
walking render hint advances that shuffle only while an enemy is moving. The
animation freezes when an enemy stops or is dance-stunned, and the renderer
accounts for the drawing's original left-facing orientation.

The reported local validation passed with 143 tests.

This reuse gives the characters a common motion language without a sprite
sheet or enemy-animation framework. It also leaves an honest imperfection.

Wanderers and chasers now share the same drawing even though their gameplay
classification remains different. Their visual distinction is less obvious,
especially because fire affects the types differently. The asset replacement
made the game more faithful to Kai's world, but it did not fully solve enemy
differentiation.

That is a clear follow-up question, not a reason to claim more than the change
delivered.

## The Red Check Was Not The Feature

During PRs #53 through #56, the GitHub security check began failing while the
implementation, lint, typecheck, tests, and other checks were green.

The same failure appeared across several unrelated feature branches.
Investigation found that `pnpm audit --audit-level high` under pnpm 10.33.0 was
receiving HTTP 410 responses from the npm audit endpoints it used. The npm
registry transition occurred between the last green `main` run and these PR
runs.

Gitleaks, Semgrep, forbidden-pattern checks, invisible-Unicode checks,
batch-discipline checks, and the other validations were passing.

That evidence did not support the statement "the feature introduced a
vulnerability." It supported a narrower statement: the shared audit step
could no longer complete with the pinned package manager.

The feature branches also respected the repository's ownership boundary.
They did not edit the maintainer-controlled workflow while trying to make
their own checks green. The failure was diagnosed, options were proposed, and
a dedicated infrastructure change handled the repair.

[PR #57](https://github.com/neibaur-labs/boo-boo-story/pull/57) updated the
root package-manager declaration to pnpm 11.13.0 and added the required trust
policy and build settings. It merged before the affected feature pull requests
were finalized and restored the security workflow.

This infrastructure repair was secondary to the day's art and gameplay work,
but its lesson was related.

Claims need to match evidence.

"CI is red" and "this code is broken" are not equivalent statements.

## Kai's Feedback Was Already Technical

Kai did not describe orientation models, render transforms, delta-time-driven
animation, collision invariants, or state-derived copy.

He did not need to.

"Facing the wrong way" identified that the renderer assumed every drawing
began with the same orientation.

"Make the legs move" identified that one skin had bypassed the shared walk
cadence.

"The house is only a corner" identified that the visual object was incomplete
and that replacing it should not accidentally redefine collision.

"The bad guys should be Boo-Boos" identified where placeholder art still
separated the game from his world.

Using two fire drawings identified the smallest animation the weapon needed
to feel alive.

The engineering work was translation: preserve the specificity of those
observations while making the smallest rules that let the game honor them.

That meant recognizing orientation as data, deriving animation from existing
time, reusing one walk cadence, separating rendering from collision, changing
existing names without inventing a new HUD feature, and keeping gameplay
classification even when two enemies shared one image.

It also meant stopping.

No generic sprite system was needed. No canvas test harness was fabricated.
No scan pipeline feature was claimed. No new Boo-Boo-1 frames were invented.
No promise was made that the enemies were now visually distinct enough.

Kai's drawings became executable game rules because the code learned the
specific things those drawings meant.

The art did not have to become generic before it could become alive.

## Outcome

Day 74 completed the July 14 Boo-Boo Story work session represented by PRs
#52 through #57.

Kai's bad-guy, two fire, and complete-house drawings were converted into
archival and 256-pixel transparent assets with corrected phone orientation,
preserved marker texture, and visually checked crops and transparency. The
focused HSV treatment remained asset-only because the existing scan script
did not truthfully expose the referenced mode.

Boo-Boo-1 gained correct skin-aware facing, a visible mirrored walk shift
through the shared cadence, and proper naming in existing player-facing text.
No newly drawn walk frames or permanent HUD name display were added.

The complete house replaced the procedural approximation while preserving its
two-by-two collision footprint and walkable surrounding tiles. Unit tests
covered that gameplay geometry, not canvas pixels.

Kai's two fire drawings became a 120-millisecond animation driven by the
existing gameplay timer. Both enemy types now use Kai's bad-guy image and the
shared walk cadence while retaining their prior AI and gameplay differences.
Wanderers and chasers still share one image, leaving visual differentiation as
an honest follow-up opportunity.

The feature pull requests reported successful local validations. A shared
security-check failure was traced to pnpm 10.33.0 receiving HTTP 410 responses
from npm audit endpoints, not to vulnerabilities introduced by the feature
code. A separate package-manager update restored that workflow without
crossing protected-file boundaries from the feature branches.

## Definition Of Done

Day 74 reached the living-drawings checkpoint:

- followed Day 73 with the July 14, 2026 entry
- treated PRs #52 through #57 as one July 14 work session despite UTC rollover
- began with Kai's direct visual and character feedback
- preserved Kai's marker and ink texture during asset preparation
- distinguished archival assets from 256-pixel game derivatives
- recorded EXIF correction, transparency, crop, and dimension checks
- kept HSV segmentation asset-only rather than claiming a pipeline feature
- represented original sprite orientation as a skin-aware rendering rule
- reused the shared player walk cadence for Boo-Boo-1
- stated that Boo-Boo-1's alternate step mirrors one supplied drawing
- updated existing player-facing names without adding a new HUD feature
- preserved clone naming because clones retain the default Boo-Boo art
- rendered the complete house without changing collision geometry
- described collision tests without claiming canvas-pixel unit coverage
- animated two fire drawings from the existing gameplay timer
- avoided timers, sprite sheets, frameworks, and generalized animation systems
- replaced both enemy placeholder styles with one supplied bad-guy drawing
- preserved enemy AI, damage, collision, and type-specific gameplay
- animated enemies only while they move
- stated that wanderers and chasers still share the same artwork
- left enemy visual differentiation as an explicit follow-up opportunity
- distinguished a shared audit-tool failure from a feature-code vulnerability
- respected protected workflow ownership from the feature branches
- recorded the dedicated pnpm repair without letting infrastructure dominate
- linked each Boo-Boo Story pull request covered by the session
- preserved the central lesson that visual feedback can identify precise game
  rules without using engineering vocabulary
