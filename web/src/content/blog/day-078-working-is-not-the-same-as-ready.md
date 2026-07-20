---
title: "Day 78 - July 18, 2026: Working Is Not the Same as Ready"
description: "A Day 78 reflection on how Kai's QA turned transparent margins into a stable flipbook transformation, while repository constraints turned a working side-scroller prototype into an intentionally incomplete but maintainable first slice."
pubDate: "2026-07-18"
day: 78
dashboardSlug: "none"
dataSources:
  - "Kai's Boo-Boo Design Studio QA feedback"
  - "Boo-Boo Story PR #74 and PR #75 implementation and validation notes"
  - "Boo-Boo Design Studio and side-scroller architecture notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - boo-boo-story
  - boo-boo-quest
  - user-driven-qa
  - creative-tools
  - pixel-art
  - game-development
  - testing
  - prototyping
  - architecture
  - scope-management
---

Kai had drawn a character successfully.

The designer had saved it successfully. The file was valid. The game could
load it. The renderer displayed the right pixels.

And the character still looked wrong.

It appeared tiny.

That was the first useful lesson of the day. A technical creation loop can be
complete while the experience it produces is still not usable. Every boundary
can accept the artifact, every schema can validate it, and every renderer can
do exactly what it was designed to do. Then the person making the thing can
show that the real requirement is still missing.

The second lesson arrived from a different part of Boo-Boo Story. The
side-scroller already worked as a self-contained HTML proof of concept. Boo-Boo
could run, jump, land on platforms, and reach the end of a level. But a working
experiment under `public/play/` was not yet maintained application code.

Moving it into the Astro application required more than relocating a file. It
required typed boundaries, pure logic, repeatable tests, and a responsible
answer when the complete graduation exceeded the repository's pull-request
size limit.

On July 18, those two gaps produced two focused pull requests.

[PR #74](https://github.com/neibaur-labs/boo-boo-story/pull/74) turned Kai's
observation into a careful multi-frame image transformation.

[PR #75](https://github.com/neibaur-labs/boo-boo-story/pull/75) began moving
the side-scroller from a successful sketch toward maintained software, then
stopped at an intentionally incomplete but honest boundary.

One change made a technically valid creation actually usable. The other made a
working prototype begin to belong to the application.

Both showed that working is not the same as ready.

## The Renderer Was Not The Problem

The tiny character initially looked like a rendering problem.

It was reasonable to inspect the game first. Perhaps the selected character
was being drawn at the wrong size. Perhaps the creation file declared the
wrong dimensions. Perhaps the import or shelf path had altered the frames.

None of those explanations fit the evidence.

The game was rendering the complete canvas correctly. The actual drawing only
occupied a small portion of that canvas. A large transparent margin surrounded
the character, so scaling the full frame preserved all that empty space. The
visible pixels remained small because the renderer had no reason to treat
transparent margins as accidental.

Kai's simple report—the character looks too small—therefore became a more
precise engineering question:

How should the designer find, scale, and reposition the painted content of an
entire animation without changing its proportions or making it jitter?

That question belonged in the creation tool, not in the game. The renderer
should not guess which transparent pixels an artist intended to keep. The
designer could instead offer an explicit operation before the creation crossed
the boundary.

## One Fit For The Whole Flipbook

PR #74 added a `Fit to canvas` action to the Boo-Boo Design Studio.

The operation finds the combined nontransparent bounding box across every
animation frame. It then calculates one proportional scale that fills the
available canvas while preserving aspect ratio, leaves two pixels of padding,
and centers the result.

The scaling uses nearest-neighbor sampling. That detail is important for
pixel art. A smoother interpolation method would invent blended edge colors
and make the enlarged drawing appear blurry. Nearest-neighbor scaling keeps
each source pixel crisp.

The more important decision was to calculate the transformation once for the
entire flipbook.

It would have been simpler to fit each frame independently. Each drawing could
find its own bounds, fill the canvas, and look appropriately large when viewed
alone.

Animation would reveal the failure.

A moving arm or foot can change a frame's bounds. If every frame received its
own scale and center, the character could grow, shrink, or shift position as
the animation advanced. The tool would solve the transparent-margin problem
by introducing visible jitter.

Using the combined bounds gives every frame the same scale and offset. Motion
inside the flipbook remains motion; the character's overall size and position
do not pulse around it.

The implementation also treats the fit as one edit across the whole creation.
A single undo restores every original frame. Redo reapplies the full
transformation symmetrically. The user does not have to undo once per frame or
recover a flipbook left half-fitted.

Two quieter cases received explicit behavior. An empty drawing produces a
message instead of pretending to change anything. A drawing already in its
fitted state does not add a useless entry to undo history.

Those details turned a button into a coherent editor operation. The visible
request was to make the character larger. The actual feature had to preserve
aspect ratio, pixel edges, animation stability, and document-level history.

## The User Found The Missing Requirement

The creation pipeline had already crossed several technical boundaries.

Kai could draw multiple frames, save a validated creation, store it on a local
shelf, and select it inside Boo-Boo Quest. That was a real accomplishment. It
was still possible to mistake the completed path for a completed experience.

Kai's QA session corrected that assumption.

The missing requirement was not another schema field or renderer branch. It
was an editing action that became obvious only after a real drawing traveled
through the whole system.

This is why creator-facing tools need creator-driven QA. Synthetic fixtures
can prove that a 32-by-48 frame loads correctly. They are much less likely to
reveal that a child naturally draws a small figure in the middle of a larger
canvas and expects the game to make that figure feel like the character.

The workflow was technically complete before PR #74. After Kai used it, the
team understood what complete needed to mean.

The pull request followed the repository's tests-first structure. Its first
commit added failing tests and a typed inert stub. Its second commit supplied
the implementation and interface wiring. The change covered 265 lines,
`pnpm validate` passed, and the repository reached 276 tests.

The sequence matters. The feedback was informal, but the response became a
bounded behavior with executable expectations.

## A Working Prototype Still Lived Outside The App

The side-scroller had a different kind of incompleteness.

As a proof of concept, it had already succeeded. The standalone experiment
answered an early product question: Boo-Boo could feel at home in a simple
side-scrolling world built around running, jumping, platforms, and a trailing
camera.

That success created the next question.

Should the experiment remain one HTML file, or should it become a maintained
part of the Astro application?

Graduation did not mean redesigning the game. It meant separating the logic
that the prototype had already proven from its browser wiring, giving that
logic types, and making its established behavior repeatable under tests.

PR #75 took the first slice.

It extracted typed level data through `SideScrollerLevel` and `PlatformRect`
while preserving the original first-level layout. It also extracted the pure
movement and camera behavior:

- running and gravity
- jumping
- coyote time
- the shorter jump produced by releasing the button early
- one-way platform collision
- the existing six-pixel landing margin
- fall clamping
- a trailing, bounded camera
- the original two-frame walking alternation

The goal was fidelity, not improvement. The prototype had already established
how the game felt. The port's job was to make that behavior legible and
testable without quietly redesigning it during the architectural move.

## Tests Can Be Wrong Too

One test expectation was corrected during the implementation.

The initial expectation accidentally triggered the prototype's existing
early-release jump cap. The observed result differed from what the test writer
expected, but the production logic was faithfully preserving established
behavior.

There are two easy but damaging reactions in that situation.

The implementation could be changed merely to make the new test green. That
would alter gameplay during a port whose stated purpose was behavior
preservation. Or the discrepancy could be waved away because the prototype
had never expressed the rule as a unit test.

The right response was to inspect the existing behavior and correct the
mistaken expectation.

Tests are evidence encoded by people. They can contain a wrong assumption just
as code can contain a defect. Tests-first development does not make every
initial assertion authoritative. It makes the disagreement visible early
enough to decide which contract the work is supposed to preserve.

Here, the prototype was the source of truth. The expectation changed, and the
gameplay did not.

## The Line Limit Defined The Honest Slice

The complete side-scroller graduation was larger than the logic extraction.

It also needed an Astro page, DOM and canvas wiring, a user-facing route, a
listing on the games page, navigation, and an amendment to the architectural
decision record.

Together, that work would have reached approximately 650 changed lines. The
repository limits pull requests to 400 lines.

The limit was not treated as decorative. The work split at a boundary that a
reviewer could understand:

1. level data, pure movement logic, and tests
2. the Astro page, browser glue, listing, navigation, and ADR amendment

PR #75 therefore ended in a state that was intentionally not user-facing. The
new modules existed and were tested, but no page imported them yet. There was
no final route to announce and no claim that the graduation was complete.

That can look awkward if progress is measured only by visible features. A
pull request added 409 total lines, including tests, with 163 lines of source
code, and the application still showed the old standalone experiment.

But the first slice established something the single-file prototype did not
have: a typed and tested foundation that the browser layer could consume next.
`pnpm validate` passed, and the separate change remained small enough to
review on its own terms.

An intentionally non-user-facing pull request can be meaningful progress when
it creates a stable seam for the next one.

## Separate Games Kept Separate Engines

The architectural move could also have become an excuse to merge the
side-scroller with Boo-Boo Quest.

Both games use Boo-Boo. Both need movement, collision, animation, and cameras.
Sharing an engine might sound like the natural destination.

The repository's explicit boundary said otherwise.

The new side-scroller modules did not import gameplay logic from `quest-kai`,
and Boo-Boo Quest did not depend on the side-scroller. PR #75 preserved the two
games as separate engines.

That constraint prevented a port from turning into an unplanned engine
unification project. Similar concepts were allowed to remain separate because
the games had different histories, contracts, and product questions.

Preserving the boundary was not duplicated effort accidentally overlooked. It
was part of graduating the prototype responsibly.

## Constraints Shaped The Work

Neither pull request was made smaller by ignoring complexity.

The fit operation accounted for every frame because per-frame convenience
would create animation jitter. It became one undoable document edit because a
partial transformation would be confusing. It used nearest-neighbor scaling
because generic image smoothing would damage the pixel-art result.

The side-scroller port preserved existing movement behavior because
architectural migration was not permission to tune the game. It corrected a
test when the test contradicted that behavior. It stopped before the page and
navigation layer because the line limit required a reviewable split.

Tests-first commits, separate-engine rules, and pull-request size limits can
look like overhead when the desired result is easy to describe: make the
character bigger; move the demo into the app.

In practice, the constraints translated those broad requests into changes
with clearer promises.

User feedback converted a visual complaint into one stable transformation for
an entire flipbook. Architectural governance converted a complete port into a
smaller first step with an explicit handoff. Tests made both behaviors
discussable, including the moment when a test itself was wrong.

The rails did not merely slow the work down. They gave it shape.

## Ready For The Next Slice, Not Finished

The July 18 work moved two parts of Boo-Boo Story closer to being tools and
games Kai could keep using rather than demonstrations that worked once.

The designer now had an answer for a real creation pattern that no schema test
had predicted. A small drawing surrounded by transparency could become a
large, crisp, stable animation without losing its proportions or undo history.

The side-scroller now had typed level data and tested gameplay logic outside
the standalone page. It did not yet have the final Astro page or user-facing
route. That incompleteness was named rather than hidden.

Later work would continue the graduation and expand the game. That work did
not belong to July 18. PRs #76 through #79 were opened on the morning of July
19 and remain part of the following day's story.

Day 78 ended with one workflow more usable and one prototype more maintainable.
Neither improvement required pretending that every next step was already
done.

Working was not the same as ready.

But real feedback and honest constraints showed exactly how to move closer.

## Outcome

Day 78 covered the July 18 Boo-Boo Story work represented by PRs #74 and #75.

PR #74 added `Fit to canvas` after Kai's QA revealed that valid, saved
characters could still render too small when their visible pixels occupied
only a small part of the frame. The operation finds one combined transparent
bounds across the whole flipbook, preserves aspect ratio, leaves two pixels of
padding, centers the artwork, and uses nearest-neighbor scaling. One shared
scale and offset prevents frame-to-frame jitter.

The complete flipbook transformation is one undoable edit. Empty drawings
produce feedback, and already-fitted drawings do not create unnecessary
history. The tests-first pull request used a failing-test and inert-stub commit
followed by implementation and interface wiring, changed 265 lines, passed
`pnpm validate`, and brought the repository to 276 tests.

PR #75 began graduating the standalone side-scroller into the maintained
Astro application. It extracted typed level data, running, gravity, jumping,
coyote time, early release, platform collision, fall clamping, camera
behavior, and walking animation without redesigning the prototype. One
mistaken test expectation was corrected when it unintentionally activated the
prototype's existing early-release cap.

The complete graduation would have reached approximately 650 changed lines,
so the repository's 400-line pull-request limit produced an explicit split.
PR #75 contained only pure modules and tests: 409 total changed lines,
including tests, and 163 source lines. It passed `pnpm validate` but added no
user-facing route. The side-scroller and Boo-Boo Quest remained separate
engines.

PRs #76 through #79 were opened on July 19 and are intentionally excluded from
the day's completed work.

## Definition Of Done

Day 78 reached the user-feedback and prototype-graduation checkpoint:

- followed Day 77 with the July 18, 2026 entry
- limited the completed work to Boo-Boo Story PRs #74 and #75
- excluded PRs #76 through #79 from the July 18 accomplishments
- connected Kai's hands-on QA to the missing fit operation
- distinguished transparent margins from a renderer or file-format defect
- described one combined nontransparent bounds across every animation frame
- recorded proportional scaling, aspect-ratio preservation, centering, and
  two pixels of padding
- identified nearest-neighbor scaling as the pixel-art-preserving method
- explained why one shared scale and offset prevents animation jitter
- treated the full flipbook transformation as one undoable and redoable edit
- recorded empty-drawing feedback and no-op history behavior
- documented PR #74's tests-first two-commit structure
- recorded 265 changed lines, passing `pnpm validate`, and 276 tests
- framed creator-driven QA as the source of a requirement missed by technical
  pipeline validation
- described PR #75 as the first slice of side-scroller graduation
- recorded typed level data and preservation of the first-level layout
- covered running, gravity, jumping, coyote time, and early jump release
- covered one-way platforms, the six-pixel landing margin, and fall clamping
- covered the trailing bounded camera and two-frame walking alternation
- treated behavior preservation as the port's priority
- explained why the mistaken test expectation was corrected
- preserved the prototype's early-release jump cap
- recorded the approximately 650-line complete graduation estimate
- explained the 400-line pull-request limit and the two-part split
- stated that PR #75 added no Astro page or user-facing route
- recorded 409 total changed lines, including tests, and 163 source lines
- recorded passing `pnpm validate` for PR #75
- kept the side-scroller separate from the Boo-Boo Quest engine
- treated an intentionally non-user-facing foundation as honest progress
- preserved the central lesson that real use and repository constraints reveal
  different distances between working and ready
