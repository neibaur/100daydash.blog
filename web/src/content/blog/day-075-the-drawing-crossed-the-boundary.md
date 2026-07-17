---
title: "Day 75 - July 15, 2026: The Drawing Crossed the Boundary"
description: "A Day 75 reflection on building a deliberately constrained design studio that let Kai draw, animate, save, validate, and bring his own creations into Boo-Boo Quest."
pubDate: "2026-07-15"
day: 75
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story PR #58 through PR #65 implementation and validation notes"
  - "Boo-Boo Design Studio and Boo-Boo Quest architecture notes"
  - "Boo-Boo Quest browser-verification results"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - boo-boo-story
  - boo-boo-quest
  - game-development
  - creative-tools
  - pixel-art
  - animation
  - security
  - local-first
  - scope-management
---

On the previous day, more of Kai's drawings became official Boo-Boo Quest art.

The game learned which direction his characters faced, how their feet should
move, where the complete house belonged, and how two drawings of fire could
become one animation. But Kai still depended on an adult-facing asset pipeline
and development tools whenever he wanted to add something new.

The next question was larger.

Could Kai draw a character, tool, or piece of scenery himself, in the browser,
and then see that creation inside the game?

In child-facing terms, the loop was wonderfully small:

1. draw something
2. save it
3. play as it or find it in the world

The engineering work was not small. A drawing had to move from an editor into
a file, from the file into local storage, and from local storage into a game
that should never surrender its own behavioral rules to imported artwork.

During the July 15 work session, PRs #58 through #65 built that complete path.
Some pull-request timestamps extended into July 16 in UTC, but the continuous
implementation sequence belonged to the same July 15 session.

The feature became real only when the drawing crossed every boundary.

## The Smallest Useful Drawing Program

[PR #58](https://github.com/neibaur-labs/boo-boo-story/pull/58) introduced the
`/design` page under the placeholder name "Boo-Boo Design Studio." Kai can
choose one of three kinds of creation: a character, a weapon or tool, or a set
piece.

Each kind begins on a canvas sized for the game rather than for a general
graphics program. Characters are 32 by 48 pixels, weapons are 64 by 48, and
set pieces are 64 by 64. The browser enlarges those true-resolution canvases
with pixelated rendering and places transparency over a checkerboard.

That decision made the editor honest. Kai sees large, touchable pixels, while
the underlying image is already the exact size the game expects. There is no
later resampling step quietly changing what he drew.

The first surface provided 1-, 2-, and 4-pixel pencils, preset colors, a full
color picker, an eraser, clear, undo, and redo. Pointer events gave mouse,
touch, and pen input one path through the editor. A capped history retained 20
pixel snapshots.

The code followed the same boundary used elsewhere in Boo-Boo Quest. Pure
modules owned sprite sizes, history, and RGBA pixel operations. The page entry
point remained responsible for DOM and pointer-event integration. The pure
parts received tests; the browser behavior received real interaction checks.

This first complete surface reached 752 changed lines, beyond the usual
400-line limit. The exception had been authorized in the task charter and was
documented directly rather than hidden. Much of the change was tests and page
styling, and splitting the canvas before it was usable would have delivered a
fragment instead of one coherent surface.

[PR #59](https://github.com/neibaur-labs/boo-boo-story/pull/59) added lines,
outline and filled rectangles, outline and filled ellipses, and a flood-fill
bucket.

These were bitmap tools, not vector tools. A shape appeared temporarily on a
pointer-transparent overlay while it was dragged, then rasterized into the
RGBA frame when released. It did not remain an object with handles, editable
dimensions, or a later resize operation.

That limitation was part of the design. Rectangles normalized their corners.
Ellipses fit the dragged bounds, with nearly flat drags safely degrading into
lines. Flood fill used exact RGBA matching and four-connected neighbors.
Outside-canvas drags clamped to an edge. A completed shape or effective fill
created one undo snapshot, while filling a region with its existing color
created none.

The editor was not becoming a graphics suite. It was becoming the smallest
drawing surface that produced pixels Boo-Boo Quest could use.

## Animation Without An Animation System

A single image was enough to enter the game, but movement was already part of
the visual language Kai had helped establish.

[PR #60](https://github.com/neibaur-labs/boo-boo-story/pull/60) made each
creation an ordered list of frames. Kai can create a blank frame, copy the
current one, delete one, or move one left or right. An animation contains at
least one frame and no more than eight.

The limit kept the interface and eventual file size understandable. It also
made frame thumbnails a workable navigation surface instead of the beginning
of a timeline editor.

A slider controls preview speed from 1 to 12 frames per second. The Play
preview uses `requestAnimationFrame` delta time and the same accumulated-time
and modulo idea already used by Boo-Boo Quest. A pure `frameIndexAt(t, fps,
count)` helper expresses the common lookup.

Pixel undo remained meaningful across frames. Each snapshot remembers which
frame it belongs to, so undoing an edit can select the frame where the edit
occurred. Structural changes are different. Adding, copying, deleting, or
moving frames resets pixel history rather than trying to reinterpret old
indices after the strip has changed.

That is a deliberate simplification, not an invisible failure of undo.

Onion skinning was also deliberately deferred. The PR was already 387 changed
lines. Adding composite rendering for a translucent previous frame would have
crossed the line cap and expanded the rendering model. Eight-frame flipbooks
were useful without requiring every expected animation-editor feature in the
same change.

## Saving Meant Accepting Untrusted Input

Until this point, the page was entirely local and ephemeral. There were no
network calls and no storage. Persistence changed the nature of the feature.

The moment a creation could leave the editor as a file and return through an
import control, the drawing became untrusted input.

[PR #61](https://github.com/neibaur-labs/boo-boo-story/pull/61) first declared
`zod@4.4.3` as an exact direct dependency of the site. Zod was already present
in the resolved lockfile through Astro, so the change did not introduce a new
package into the dependency graph. It made the site's reliance explicit
instead of treating a security boundary as an accidental benefit of a
transitive dependency.

The maintainer also chose that direct contract instead of Astro's `astro/zod`
re-export. Dependency governance was part of the design before the first
creation file could be accepted.

The persistence work had originally grown to roughly 450 changed lines. Rather
than force schema, storage, and UI into one oversized review, it split into two
single-concern changes.

[PR #62](https://github.com/neibaur-labs/boo-boo-story/pull/62) defined the
`.booboo.json` format and its validation layer. It did not yet add save, load,
import, or export controls.

The schema accepts exactly format version 1 and one of the three asset kinds.
Names contain 1 to 40 characters, authors at most 40, animation speed is an
integer from 1 to 12 fps, and each creation contains 1 to 8 PNG data-URL
frames. Unknown object keys are rejected.

The format also has physical limits. Each decoded frame can contain at most 64
KB, and the complete raw file at most 600 KB. Oversized input is rejected
before `JSON.parse` runs. Every PNG must have the exact dimensions declared by
its asset kind.

The validator reads those dimensions directly from the PNG IHDR header bytes.
It does not decode the image or require a browser DOM, so the same boundary can
run in Node tests and later wherever the editor or game consumes a creation.

`parseCreation(raw)` returns either a validated creation or a child-readable
error. A file with a newer format version receives its own message explaining
that the design came from a newer version and requires an update.

Versioning, byte limits, and dimensions might sound separate from user
experience. Here they are the conditions that let an imported drawing fail
early and explainably instead of destabilizing a child-facing tool.

## A Local Shelf, Not A Cloud Service

[PR #63](https://github.com/neibaur-labs/boo-boo-story/pull/63) completed the
persistence surface with a local shelf under the `bbs.designer.v1`
`localStorage` namespace.

The shelf holds at most 12 creations. Saving with an existing name replaces
that creation. Adding a new name to a full shelf identifies the oldest entry
through `wouldEvict()` so the UI can ask permission before removing anything.
Storage-quota failures return as values instead of escaping as exceptions.

Every stored entry passes through the strict schema again whenever the shelf
is read. Malformed or invalid entries are ignored rather than loaded into the
designer or game. An injected `StorageLike` contract keeps unit tests away
from a real browser store.

The interface adds creation and author names, saving, a "My shelf" dialog,
loading, `.booboo.json` export, and import. It confirms before replacing
unsaved artwork and before an oldest-first eviction. Empty names and storage
failures receive usable feedback.

There is no account, upload, server, cloud synchronization, or cross-device
library. There is not even a per-row delete control yet; at the limit, space
is reclaimed only by confirmed oldest-first eviction.

Local-only design simplified privacy and deployment. It did not make defensive
validation unnecessary. Browser storage and selected files still sit outside
the assumptions of the current page, and every read treats them that way.

## The Shelf Became A Bridge Into The Game

Saving a drawing was meaningful. Seeing it return after a reload was better.
But the original question was whether Kai could make something and then see
the game recognize it.

[PR #64](https://github.com/neibaur-labs/boo-boo-story/pull/64) let Boo-Boo
Quest read validated characters and weapons from the shared shelf.

Each saved character appears as another title-screen skin option beside stock
Boo-Boo and Boo-Boo-1. Selecting one replaces the hero's art for that session.
Frame zero appears while the hero stands, while walking loops the complete
flipbook at the creation's own frame rate. The game keeps its existing
accumulated delta-time clock and right-facing orientation behavior. The
creation supplies images, speed, and a display name; the game retains movement
and timing control.

The selection is intentionally session-only. It does not become another
persisted preference merely because the artwork already lives in local
storage.

Saved weapon creations appear in a custom fire-art picker. Choosing one changes
the Flame Thrower's appearance and nothing else. Reach, damage, timing, cone
behavior, and rotation remain the game's rules. An empty shelf hides the
custom row.

This was the clean separation the entire route needed:

- the creator controls appearance
- the game retains behavior

Browser verification seeded a two-frame character and exercised its title
button, standing frame, walking alternation, own-fps timing, stock-skin
selection, empty shelf, and corrupted-shelf startup.

The custom Flame Thrower picker wiring was verified, but the rendered weapon
was not driven all the way through game progression in the browser. That path
sits deep in the game. Its implementation uses the same image-swap pattern
that was pixel-verified for the hero, but that architectural similarity is not
being presented as a complete custom-flame gameplay journey.

## Scenery Without A Level Editor

Set pieces created a different question. Characters and weapons could enter
existing selection controls. Scenery needed a place in the world.

A general level editor would have multiplied the scope. Free placement would
need world-coordinate editing, movement, deletion, persistence rules,
collision decisions, invalid-position handling, and recovery when the map
changed.

Kai did not need all of that to see his drawing in the game.

[PR #65](https://github.com/neibaur-labs/boo-boo-story/pull/65) instead defined
four fixed, safe 2-by-2-tile slots:

- Home Meadow at `(2,4)`
- Open Field at `(10,3)`
- Flower Patch at `(2,2)`
- Quiet Grove at `(8,6)`

Validated set pieces fill those positions in shelf order. The first appears in
Home Meadow near the starting area, so Kai does not have to search the whole
world to learn whether his creation worked. Later pieces appear farther away,
and unused slots remain plain.

Each slot sits on a named screen, inside map bounds, over an existing walkable
2-by-2 area. The game reads the shelf but never writes to it. Each piece
renders at its native 64-by-64 size after map tiles and beneath actors.
Multi-frame pieces use their own fps on the game's clock, including during
screen-slide transitions.

Most importantly, no collision data changes. Set pieces are visual scenery.
The four fixed positions preserve that invariant without asking a child to
understand the map's solidity rules.

Fixed placement was not an incomplete level editor. It was the smaller
interface that completed the actual creative loop safely.

## More Boundaries Made The Tool More Complete

The visible feature was playful: a pixel canvas, a flipbook, a shelf, and a
game that could display what Kai made.

The implementation was a sequence of limits:

- three creation kinds with fixed dimensions
- bitmap drawing tools rather than a vector object model
- a 20-snapshot undo history
- no more than eight animation frames
- animation speeds from 1 to 12 fps
- a strict, versioned file format
- per-frame and total-file byte caps
- exact PNG dimension checks
- 12 local shelf slots
- no network, accounts, or uploads
- session-only character selection
- appearance-only custom weapons
- four fixed, non-solid scenery positions

Those limits are not evidence that the feature stopped early. They are what
allowed the work to travel all the way from pixels to gameplay.

Governance shaped the architecture along the route. The first complete canvas
received one documented line-cap exception. Shapes remained bitmap operations.
Onion skinning was deferred before it could overfill the animation PR. A
too-large persistence change split at the actual security boundary. Zod became
a declared dependency. Set pieces received fixed slots instead of pulling a
level editor into the final step.

Each constraint reduced the number of contracts the next boundary needed to
understand.

The editor always emits known dimensions. The schema always receives bounded
frames. The shelf always revalidates its contents. The game always receives
appearance data that fits places and timing systems it already controls.

The complete journey was therefore understandable:

1. pixels entered a true-resolution canvas
2. frames formed a bounded flipbook
3. the flipbook became a strict, versioned creation
4. the creation entered a validated local shelf
5. Boo-Boo Quest read that same shelf
6. the creation appeared as a character, tool skin, or piece of scenery

No cloud service was necessary. No general asset pipeline or animation suite
appeared. No level editor took control of the world.

The result was still expressive because every limit protected the one form of
expression the feature promised.

Kai could make a small piece of the game himself and watch the game recognize
it.

## Outcome

Day 75 completed the July 15 Boo-Boo Story designer session represented by PRs
#58 through #65, including work whose GitHub timestamps extended into July 16
UTC.

The new `/design` page provides true-resolution canvases for characters,
weapons or tools, and set pieces, enlarged with pixelated rendering. Pencil,
color, erase, clear, capped undo and redo, bitmap shape tools, and exact-color
flood fill support mouse, touch, and pen without introducing a vector object
model or editable committed shapes. The first complete canvas used one
documented, pre-authorized line-cap exception.

Creations can contain 1 to 8 independent frames, be reordered and previewed
from 1 to 12 fps, and use the same accumulated-time approach as the game.
Pixel undo can return to the edited frame, while structural frame changes
intentionally reset that history. Onion skinning remains deferred.

The version-1 `.booboo.json` contract rejects unknown keys, invalid kinds,
names and authors beyond their limits, invalid fps or frame counts, non-PNG
frames, incorrect dimensions, decoded frames over 64 KB, and raw files over
600 KB. Oversized files fail before parsing, and PNG dimensions are read from
IHDR bytes without decoding pixels. Zod became an explicit direct dependency;
it was already resolved transitively through Astro.

The `bbs.designer.v1` local shelf stores up to 12 validated creations, replaces
same-name entries, confirms oldest-first eviction, handles quota failure, and
revalidates every entry on read. Import and export use the same strict
contract. No network, account, upload, cloud synchronization, or per-row shelf
deletion was added.

Boo-Boo Quest reads the shared shelf without writing to it. Saved characters
become session-only skin choices whose flipbooks animate while walking. Saved
weapons change Flame Thrower artwork without changing behavior. The custom
weapon picker was wired and verified, but a complete browser journey through
deep game progression was not performed.

Saved set pieces fill four fixed, walkable, non-solid world positions in shelf
order. They render beneath actors, can animate on the game clock, and preserve
screen transitions and collision data. They cannot be freely placed.

## Definition Of Done

Day 75 reached the creator-to-game checkpoint:

- followed Day 74 with the July 15, 2026 entry
- treated PRs #58 through #65 as one continuous July 15 work session
- centered the narrative on a drawing crossing every boundary into the game
- described three fixed creation kinds and their true sprite dimensions
- distinguished enlarged display pixels from underlying canvas resolution
- recorded mouse, touch, and pen support through pointer events
- described the 20-snapshot undo and redo cap
- identified shape and fill tools as bitmap operations
- claimed no vector model, selection handles, or editable committed shapes
- recorded the one documented, pre-authorized line-cap exception
- limited animation to 1 through 8 frames and 1 through 12 fps
- explained cross-frame pixel undo and structural-history resets
- kept onion skinning explicitly deferred
- described Zod as a direct dependency already resolved through Astro
- separated the schema PR from the later persistence interface
- recorded format versioning, unknown-key rejection, byte caps, and dimensions
- explained pre-parse file-size rejection and PNG IHDR inspection
- described child-readable validation failures
- limited the local shelf to 12 creations
- recorded same-name replacement and confirmed oldest-first eviction
- stated that stored entries are revalidated on every read
- claimed no cloud, account, upload, or cross-device synchronization
- stated that per-row shelf deletion was not added
- made validated characters available as session-only skin choices
- kept custom character timing within the game's existing clock
- changed custom weapon appearance without changing weapon behavior
- preserved the honest custom-flame browser-verification boundary
- used four fixed set-piece slots instead of a level editor
- kept set pieces visual, walkable, non-solid, and read-only to the game
- linked every Boo-Boo Story pull request in the designer sequence
- preserved the central lesson that deliberate constraints completed the full
  creative loop
