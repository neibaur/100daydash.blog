---
title: "Day 77 - July 17, 2026: The Best QA Was Making Something"
description: "A Day 77 reflection on how Kai's first real Boo-Boo Design Studio session turned lost work, repetitive drawing, disconnected tools, and a hidden URL into focused engineering changes."
pubDate: "2026-07-17"
day: 77
dashboardSlug: "none"
dataSources:
  - "Kai's first working session with the Boo-Boo Design Studio"
  - "Boo-Boo Story PR #66 through PR #70 implementation and validation notes"
  - "Boo-Boo Design Studio and side-scroller browser-verification results"
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
  - scope-management
---

The most useful QA session for the Boo-Boo Design Studio did not begin with a
formal test plan.

It began when Kai sat down and tried to create something.

The designer already had a substantial feature set. Kai could draw characters,
tools, animations, and set pieces. He could save those creations to a local
shelf and use them in Boo-Boo Quest. The underlying formats were validated,
the game retained control of its own behavior, and the implementation had been
tested and reviewed.

Then the project's artist, collaborator, client, and actual user began working
with it.

A refresh erased most of a character. Animating a body part required erasing
and redrawing it in every frame. A physical drawing could travel through the
Python image-processing pipeline but could not enter the browser editor. The
designer existed, but Kai could not find it from the game. And a larger design
question remained unanswered: would his characters feel fun in a
Mario-Wonder-style side-scroller?

None of those problems had been as visible while the team was reasoning from
the implementation. They appeared when Kai tried to complete real creative
tasks.

That changed the priority order immediately.

## Lost Work Made Reliability Concrete

Kai lost most of a character when the page refreshed during his drawing
session.

The original refresh trigger could not be reproduced. The designer had not
previously installed keyboard handlers, so `Ctrl+Z` fell through to the
browser, but that is normally harmless in modern browsers. The historical
Backspace-as-browser-back behavior has also been gone from modern Chrome and
Firefox for years. An accidental `F5`, `Ctrl+R`, or pull-to-refresh action was
more plausible, but it was not proven.

That uncertainty mattered because it would have been easy to spend the day
trying to guard against one imagined cause.

Instead, [PR #66](https://github.com/neibaur-labs/boo-boo-story/pull/66)
addressed the durable failure: a refresh, however it happens, should not erase
the artist's work.

The designer now autosaves two seconds after the most recent edit. One local
storage key, `bbs.designer.autosave.v1`, holds the complete working document:
every animation frame as a PNG data URL, the active frame, artwork kind, name,
author, and frames per second.

On the next load, the designer asks, `Restore your last session?` Kai can
restore the document or start fresh, which clears the saved session. Restored
data does not bypass the designer's existing trust boundary. It is validated
against the schema, and each PNG's dimensions are checked against its declared
artwork kind. Corrupt data is discarded rather than allowed to poison the
editor.

The timing edges received attention too. A `beforeunload` warning appears when
edits are newer than the last autosave. A synchronous `pagehide` flush captures
the latest strokes when the page leaves before the two-second debounce can
finish. Keyboard undo and redo now belong to the designer through `Ctrl+Z` and
`Ctrl+Y` rather than falling through to the browser.

The value of that work was not the cleverness of a storage key. It was that
Kai's lost drawing made the cost of data loss immediate. Autosave moved ahead
of hypothetical polish because real use established what mattered.

## Repetition Revealed The Missing Operation

The next problem appeared through motion rather than an error message.

To animate a character, Kai duplicated a frame, erased a body part, and drew it
again in a slightly different position. Then he repeated the process for the
next frame.

The designer could technically create animation. Its workflow still made a
simple leg movement unnecessarily destructive and repetitive.

[PR #67](https://github.com/neibaur-labs/boo-boo-story/pull/67) added a raster
marquee selection tool around the task Kai was actually performing. He can
drag a rectangle around a body part, lift those pixels into a floating patch,
and reposition it by dragging. Arrow keys nudge by one pixel; holding Shift
nudges by five.

The interaction remains predictable at its boundaries. Clicking outside the
selection, pressing Enter, or switching tools commits the move. Escape cancels
it and restores the original pixels. One complete movement becomes one undo
step.

Transparent pixels required a less visible but important rule. The floating
patch composites only its painted pixels when it is placed. Moving a leg does
not stamp a transparent rectangle over nearby artwork and punch a box-shaped
hole through the character.

The intended loop is now close to the gesture Kai was trying to express:

1. duplicate a frame
2. select the legs or another body part
3. drag or nudge the pixels
4. repeat when another pose is needed

That feature amended an architectural decision without discarding it.
`ADR-0008` explicitly allows raster pixel selection inside the designer's
bitmap-first model. It does not introduce layers, editable vector objects, or
a general composition system.

This was not architecture yielding to feature pressure without a boundary. It
was architecture learning one operation from the artist's workflow and naming
exactly where the expansion stopped.

## Two Existing Tools Needed A Connection

Kai's physical drawings already had a path into the computer.

The local Python tooling can scan and process a drawing into a transparent
sprite. The browser designer can edit transparent sprites as ordinary pixels.
Before this session, those two capabilities did not connect. The processed PNG
could reach the filesystem but not the active canvas.

[PR #68](https://github.com/neibaur-labs/boo-boo-story/pull/68) added an
`Add a picture` button and drag-and-drop PNG import. The imported image is
scaled to fit the active frame, centered, and kept at its original aspect
ratio. Transparency survives the operation, and the full import is recorded as
one undo step. Once placed, the imported image is not a special embedded
object. It becomes ordinary editable pixels that work with the pencil, eraser,
fill, shapes, and new selection tool.

The browser did not inherit the scan-cleanup logic.

Background removal, crop preparation, and the rest of the image processing
remain in Python. The designer accepts the finished transparent PNG and stays
focused on drawing and editing. That is an intentional boundary between two
tools, not an incomplete browser port.

Kai's session exposed a broken connection rather than a missing image pipeline.
The smallest useful change was a bridge between the systems already present.

## A Hidden Tool Was Not Fully Functional

The designer had another problem that no canvas test could reveal.

Kai could not reach it without manually typing its URL.

From an implementation perspective, `/design` existed and rendered. From the
user's perspective, the tool was absent from the place where he naturally
started: Boo-Boo Quest.

[PR #69](https://github.com/neibaur-labs/boo-boo-story/pull/69) solved that
with two links. The game's title screen now offers `Design Studio — draw your
own art`, styled with the existing hand-drawn splash controls. The designer's
header offers a link back to the game.

No router, navigation model, or new framework was introduced. Two destinations
needed to connect, so the solution remained two links.

Discoverability is part of functionality. A feature the intended user cannot
find is not made complete by the fact that a developer knows its URL.

## A Prototype Can Ask Instead Of Declare

The day's fifth pull request came from a different kind of uncertainty.

Kai and I can talk about whether Boo-Boo should run through a
Mario-Wonder-style side-scroller. That conversation becomes much more useful
when he has something he can play, feel, and react to.

[PR #70](https://github.com/neibaur-labs/boo-boo-story/pull/70) created a
self-contained proof of concept at `/play/side-scroller/`. Boo-Boo can run and
jump through one hardcoded level while the camera trails behind. A short
coyote-time window makes a jump still register just after leaving a platform,
and releasing the button early produces a shorter hop. The level has solid
ground all the way across, a goal flag, and a `You made it!` celebration.
Nothing bad can happen.

The sketch uses Kai's real Boo-Boo walking frames and the quest game's existing
two-frame visual cadence. An `art by Kai` credit stays visible on the canvas.

It does not share code with Boo-Boo Quest. It adds no library, tile-map system,
physics package, reusable engine, enemy model, or scoring system. The level is
an array of platform rectangles inside one deliberately isolated HTML demo.

Those omissions are the point.

The project has not committed to a second game engine or announced a new
roadmap. The prototype exists to give Kai a conversation prop: play this small
thing and tell me whether moving through this kind of world with your
characters feels fun.

If the answer is no, the sketch can remain a sketch. If the answer is yes, the
next decisions can be informed by his reaction instead of by assumptions made
before he touched it.

The demo is currently reachable only by its URL. Adding it to the `/play`
experiments list remains a known one-line follow-up; it was not completed in
this work.

## Small Changes Inside Deliberate Rails

The implementation was AI-assisted, but the agents did not own the product
decisions. Kai's observed experience established the problems. Repository
rules constrained the response. Human direction set the scope and reviewed
what each change was allowed to become.

PRs #66 through #69 were stacked in dependency order. Autosave came first,
selection built on that recovery behavior, import followed the new pixel
workflow, and navigation completed the path between game and designer. The
side-scroller in PR #70 remained independent because it was asking a separate
question.

Across the five pull requests, the work used ten commits and a tests-first
structure: a failing specification or test before its corresponding
implementation. Four new modules covered autosave, selection, import-fit math,
and the navigation specification. The changes added 27 tests and one ADR.

The batch added approximately 1,180 lines, but it was not one 1,180-line
feature branch. Every pull request stayed below the repository's
400-source-line cap. The largest contained 279 source lines. Each PR carried
the `ai-assisted` label and passed `pnpm validate`.

Those numbers matter because they describe the shape of the work. Specific
pain became bounded changes with executable expectations. The selection tool
did not become layers. Import did not absorb the Python pipeline. Navigation
did not become a framework. The side-scroller did not become an engine.

The rails made it possible to respond quickly without allowing one productive
QA session to silently redefine the whole project.

## Not Every Failure Was Product Code

One local failure briefly looked like the new pages had broken development.

Astro 7's `astro dev` process daemonizes. A stale orphaned instance was
preventing new development-server processes from starting. Running
`astro dev stop` cleared the stale process, after which the site served the
new pages normally.

That distinction is worth recording. The application did not need a code fix
for an environmental process failure. Diagnosing the runtime state kept an
unrelated cleanup out of the product changes.

## The User Changed The Backlog By Using The Tool

Before Kai's session, I could have made a reasonable list of improvements for
the designer. More brushes, more colors, richer animation controls, cloud
synchronization, or a larger asset-management surface could all sound useful
in the abstract.

Actual use produced a different and much sharper list.

Do not lose the drawing.

Let me move the legs I already drew.

Let this processed picture enter the editor.

Let me find the tool from the game.

Give me something playable so I can decide whether this other kind of game is
fun.

Each observation connected to a task Kai was trying to complete. That made it
possible to distinguish essential friction from imagined capability. It also
made the resulting engineering smaller. The goal was not to make the designer
more impressive on a feature matrix. It was to remove the next obstacle in
Kai's creative loop.

Good feedback does not always arrive as a formal bug report. Sometimes it is
lost artwork. Sometimes it is the same erasing motion repeated across several
frames. Sometimes it is a finished sprite stranded between two tools, or a URL
the user cannot find. Sometimes it is a collaborator deciding whether a rough
prototype feels fun.

The most useful QA session was not a formal test plan.

It was Kai making something and showing the software what it still needed to
learn.

## Outcome

Day 77 captured Kai's first real working session with the Boo-Boo Design
Studio and the five focused pull requests that followed from it.

Autosave and session recovery now protect the full working document without
claiming certainty about what triggered the original refresh. A debounced save,
page-exit flush, unsaved-change warning, validated restore path, and designer
keyboard history make recovery durable across plausible refresh causes.

A raster marquee selection now supports the duplicate-select-nudge animation
workflow while remaining explicitly inside the bitmap-first architecture.
Layers and vector objects remain outside the designer's scope.

Processed transparent PNGs can enter the active frame through a button or
drag-and-drop, preserving aspect ratio and transparency while becoming
ordinary editable pixels. Image preprocessing remains in the existing Python
tooling.

Two direct links connect Boo-Boo Quest and the designer without introducing a
navigation framework. An independent side-scroller sketch uses Kai's art to
ask whether that play style feels fun without committing the project to a
second engine. Its experiments-list link remains incomplete.

The five `ai-assisted` pull requests used small, tests-first changes, added 27
tests and one ADR, stayed within the source-line cap, and passed
`pnpm validate`. A stale daemonized Astro process was separately cleared with
`astro dev stop`; it was an environmental failure rather than broken product
code.

## Definition Of Done

Day 77 reached the user-driven QA checkpoint:

- followed Day 76 with the July 17, 2026 entry
- centered Kai as the artist, collaborator, client, and actual user
- treated real creative work as the source of the day's priorities
- stated that the original refresh trigger was not conclusively reproduced
- described autosave as the durable response regardless of refresh cause
- recorded the two-second debounce and full working-document payload
- identified the single `bbs.designer.autosave.v1` storage key
- described restore validation, PNG dimension checks, and corrupt-data removal
- recorded the `beforeunload` warning and synchronous `pagehide` flush
- connected keyboard undo and redo to the designer
- framed selection around Kai's repeated animation workflow
- described drag, one- and five-pixel nudges, commit, cancel, and undo behavior
- recorded transparent compositing without rectangular holes
- kept selection raster-only and layers and vectors out of scope
- identified `ADR-0008` as an amendment to the bitmap-first decision
- connected processed physical art to the browser through PNG import
- preserved scale, aspect ratio, centering, transparency, and one-step undo
- kept preprocessing in Python rather than porting it into browser JavaScript
- treated discoverability as part of the designer's functionality
- solved game-to-designer navigation with two links and no framework
- framed the side-scroller as a conversation prop rather than a roadmap
- recorded run, jump, coyote time, short hops, camera, goal, and safe ground
- credited Kai's art and reused the existing two-frame walking cadence
- stated that the demo shares no code with Boo-Boo Quest
- claimed no second engine, library, tile-map system, enemies, or scoring
- left the `/play` experiments-list link as an explicit incomplete follow-up
- recorded PRs #66 through #69 as stacked and PR #70 as independent
- recorded five pull requests, ten commits, about 1,180 added lines, 27 tests,
  four tested modules, and one ADR
- recorded that every PR stayed under 400 source lines and the largest had 279
- identified every PR as `ai-assisted` and locally validated with
  `pnpm validate`
- described agent assistance as constrained implementation, not product
  ownership
- separated the stale Astro daemon from product-code failure
- preserved the central lesson that actual use reordered the backlog
