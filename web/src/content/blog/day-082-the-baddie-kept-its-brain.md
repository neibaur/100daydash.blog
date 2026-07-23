---
title: "Day 82 - July 22, 2026: The Baddie Kept Its Brain"
description: "A Day 82 reflection on giving Kai more things to create while keeping appearance, gameplay behavior, and the two Boo-Boo Story game engines within clear boundaries."
pubDate: "2026-07-22"
day: 82
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story PR #80 through PR #84 implementation and validation notes"
  - "Boo-Boo Design Studio, Boo-Boo Quest, and side-scroller architecture notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - boo-boo-story
  - boo-boo-quest
  - creative-tools
  - pixel-art
  - game-development
  - testing
  - architecture
  - scope-management
---

Adding two buttons to a drawing tool sounds small.

One button says `Baddie`. The other says `Little prop`. Each gives Kai a
32-by-32-pixel canvas instead of the shapes already available for characters,
tools, and large set pieces.

But the buttons are only the visible edge of the change.

For a drawing to move from the Boo-Boo Design Studio into a game, the canvas,
file format, autosave system, shelf, import and export path, loaders, title
screen, animation logic, and renderer all need to agree about what the drawing
means. This time, two different games needed to agree without becoming one
game engine.

Across five pull requests on July 22, I expanded what Kai can create without
expanding what those creations are allowed to control.

[PR #80](https://github.com/neibaur-labs/boo-boo-story/pull/80) established
shared asset dimensions. [PR
#81](https://github.com/neibaur-labs/boo-boo-story/pull/81) added baddies and
little props to the Design Studio. [PR
#82](https://github.com/neibaur-labs/boo-boo-story/pull/82) brought designed
baddies into Boo-Boo Quest. [PR
#83](https://github.com/neibaur-labs/boo-boo-story/pull/83) brought the same
creation format into the side-scroller. [PR
#84](https://github.com/neibaur-labs/boo-boo-story/pull/84) created safe places
for decorative props in both games.

The central contract stayed simple:

> Kai's drawings can control how something looks, but the games continue to
> control how it behaves.

A designed baddie can look entirely different from the original. It can have
multiple animation frames, play them at Kai's chosen speed, and turn with its
direction of travel. It cannot rewrite the enemy's brain.

The baddie kept its AI, speed, health, collision, damage, patrol rules, spawn
position, combat shape, and every other gameplay rule its game already owned.

That boundary made the creative system more capable without making it
unpredictable.

## One Vocabulary Before Two Integrations

The first pull request did not put new art on screen. It established the
language that the Design Studio and both games would use when talking about
assets.

The shared types and canvas dimensions became:

- `character` at 32 by 48 pixels
- `weapon` at 64 by 48 pixels
- `setpiece` at 64 by 64 pixels
- `enemy` at 32 by 32 pixels
- `object-small` at 32 by 32 pixels

Those numbers came from the sizes and proportions the games already used for
Kai's artwork. The module did not invent a new visual system. It recorded the
existing contract in one place so the designer and the two consumers could
stop maintaining separate answers.

That made PR #80 more than a constants-file cleanup. It created one source of
truth for creation types and their canvases while leaving the game engines
otherwise independent.

The limits of that source of truth mattered.

Both games derive displayed width from an image's aspect ratio and apply their
own intentional presentation scales. Those are rendering decisions, not
creation-canvas dimensions. Forcing them into the shared module would have
made the abstraction broader than the meaning it actually shared.

The proposed large-object category also already existed under the name
`setpiece`. Renaming it might have made a new list look tidier, but it would
have changed the meaning of existing `.booboo.json` files. I preserved
`setpiece` as the large-object type instead.

Compatibility was more valuable than vocabulary churn.

This foundation passed 335 tests across 43 files.

## Two More Things Kai Can Draw

With the shared contract in place, the Design Studio could widen its existing
asset picker instead of gaining a second type-selection system.

The new choices were `👾 Baddie` and `🪴 Little prop`, both using 32-by-32
canvases. The schema, designer, autosave path, shelf, and import and export
flow all learned the same five asset types.

Each saved frame is now checked against the dimensions belonging to its type.
A character file still needs character-sized frames. An enemy file needs
enemy-sized frames. A label in the picker cannot disagree with the pixels in
the creation.

The schema also preserved two different compatibility behaviors
intentionally.

Older files with no `kind` field still load as characters, which keeps
existing creations usable. A file with an unrecognized `kind` still rejects.
Missing old information has a known historical meaning; unknown new
information does not. Silently treating both cases as characters would turn a
compatibility feature into data corruption.

Enemy creations were also excluded deliberately from the character and weapon
loaders. A baddie drawing should not accidentally appear as a playable hero or
a tool merely because all three creations happen to share a shelf.

The real Design Studio page was exercised in a headless browser. Every picker
was clicked and every resulting canvas was measured: character at 32 by 48,
enemy and little prop at 32 by 32, set piece at 64 by 64, and weapon at 64 by 48.

At this point, 345 tests across 44 files passed.

The drawing tool could describe more of Kai's world. The next question was how
much authority those descriptions should receive inside a game.

## A New Face For The Same Quest Baddie

Boo-Boo Quest already had title-screen pickers for Kai's characters and fire
looks. PR #82 followed that established interaction with a baddie picker.

Kai's original baddie art remained the default. Saved enemy creations appeared
as additional choices, and the row stayed hidden when the shelf contained no
enemies. The choice lasted for the current session rather than creating
another permanent preference.

Once selected, a designed enemy used its own flipbook frames and
designer-selected frames-per-second value. It faced its direction of travel
and continued to receive the quest's existing visual treatment: bobbing,
shadow, damage flash, burning, and dousing.

If one of its saved frames could not be decoded, the quest drew Kai's original
baddie instead of leaving a blank space where an enemy should be.

Everything in that paragraph concerns presentation.

The quest still owned chasing, attacking, health, speed, collision, spawn
tables, and the round-versus-spiky combat distinction. A different drawing did
not make an enemy gentler, stronger, faster, or differently shaped for combat.
It replaced the skin, not the rules.

The end-to-end browser test made that distinction visible. It seeded an enemy
creation, selected it, started the game, and confirmed that the baddie still
chased and attacked Boo-Boo with its original behavior.

The work also introduced an empty `BUILTIN_ENEMIES` collection. That gives a
future Kai-created export a place to become a repo-committed game asset beside
session shelf creations. It does not mean a designed built-in enemy ships
today. The collection stays empty until Kai supplies an export that should
become part of the deployed game.

PR #82 finished with 349 passing tests across 45 files.

## The Creation Crossed Games, Not Engines

The side-scroller needed the same creative asset but not the same integration.

PR #83 reused only the pieces whose meaning was genuinely common: asset
constants, the creation schema and loader, the built-in list, and flipbook
frame selection. The side-scroller added its own picker and connected the
selected image to its own renderer.

A designed enemy can therefore replace the artwork for a patrol enemy and
animate at its own speed. Patrol movement, stomp rules, contact damage,
knockback, enemy locations, pits, and level data stay exactly where they were.

This repeated a project principle that has become more useful each time the
creative pipeline grows. The games can share Kai's creation format and small
data utilities without sharing physics, combat, rendering loops, or gameplay
state.

Verification had a real limitation.

Headless browser testing confirmed the picker, selection wiring, and absence
of console errors. It did not capture a screenshot of the designed enemy
beyond the first pit because automated pit crossing was unreliable. The
renderer used the same proven image-decoding and drawing pattern as the quest
integration, but structural equivalence is not the same as direct visual
evidence. I recorded the missing screenshot as a test-harness limitation
instead of pretending the browser had demonstrated something it had not.

The work also exposed an unrelated thumbnail-sizing problem in the quest
picker. I left it out of PR #83. Fixing a nearby issue would have been easy,
but one-concern-per-PR discipline mattered more than making the current diff
look comprehensive.

The side-scroller integration brought the total to 351 passing tests across 46
files.

## Places For Art That Does Not Exist Yet

The final pull request moved from actors to the environment.

Small decorative objects needed a different contract from enemies. They could
appear and animate, but they could not acquire collision, physics, pickups,
interactions, or gameplay effects simply because they were visible.

In Boo-Boo Quest, saved `object-small` creations can fill fixed one-tile
slots. I added two provisional slots on open grass in Home Meadow. Props render
beneath actors. A one-frame prop stays still, while a multi-frame prop follows
its own animation speed. Boo-Boo can walk across either because both are
visual only.

The fixed slots are engineering defaults, not final art direction. Kai still
decides which artwork belongs in the world and where it should ultimately
live.

The quest path was verified end to end with two seeded props: an animated
crate and a static sign. Both appeared at one-tile size beneath the actors,
remained non-colliding, and produced no console errors.

The side-scroller received a similarly narrow capability expressed in its own
level model. A level can declare an optional decorative object by asset name
and world position, then place it behind or in front of actors. Unknown names
are dropped safely instead of becoming blank images. Animation uses a
free-running scene clock, so the environment does not need a gameplay event to
keep moving.

Resolver and layering behavior were unit-tested. No live side-scroller prop
was demonstrated because the repository does not yet contain a committed
object or a level placement for one.

That empty state is intentional.

Like the enemy list, `BUILTIN_OBJECTS` ships empty. The pipeline is ready, but
the deployed game's appearance should not change until Kai provides the art
and helps decide its placement. Engineering supplied a safe route into the
world; it did not fill that route with substitute creative decisions.

PR #84 did not add collisions, physics, interactions, pickups, an
object-placement editor, or arbitrary abstractions across the two engines.
Final validation passed 364 tests across 48 files. The pull request changed
290 lines, remaining under the repository's 400-line cap.

## Creativity Needs A Predictable Contract

It can sound limiting to say that a child's drawing is not allowed to change
the game.

I found the opposite.

Kai can draw a new baddie without needing to understand collision geometry,
enemy state machines, damage balancing, spawn tables, or two different game
engines. He can draw a little object without accidentally creating an
invisible wall or a pickup the game does not know how to process.

The clear boundary removes questions that should not burden the act of
drawing.

Within the visual contract, the creative range is meaningful. Kai chooses the
shape, colors, frames, and animation speed. His work can replace a familiar
enemy in two different games. It can make a meadow or a side-scrolling level
feel more like his world.

Outside that contract, the games remain dependable. Their rules do not change
because a file was imported. Their separate engines do not become coupled
because they display the same creation.

A child-facing creative system does not become powerful only by making every
creation programmable. It can become more powerful by making the promise
around creation clear, safe, and predictable.

The five pull requests built that promise in order. First define the shared
vocabulary. Then teach the studio to produce it. Then let each game interpret
the visual artifact without surrendering gameplay authority. Finally, prepare
places for creative work that has not been made yet.

Those empty built-in lists and provisional meadow slots are part of the
success.

The infrastructure is ready. The games have kept their rules. The remaining
space belongs to Kai.

## Outcome

Day 82 completed the July 22 Boo-Boo Story creative-asset work represented by
PRs #80 through #84.

PR #80 established one shared source of truth for five creation types and
their canvas dimensions while preserving `setpiece` compatibility and keeping
engine-specific rendering scales out of the shared contract. Validation passed
335 tests across 43 files.

PR #81 added Baddie and Little prop choices to the existing Design Studio
picker and carried those types through validation, autosave, the shelf, and
import and export. Missing kinds remain backward-compatible characters;
unknown kinds reject. Browser checks confirmed all five canvas sizes.
Validation passed 345 tests across 44 files.

PR #82 added session-only designed-baddie selection to Boo-Boo Quest, including
custom flipbook speed, travel-direction facing, visual effects, and safe
fallback to the original art. Enemy behavior and combat remained unchanged,
and the built-in enemy list remained empty. Validation passed 349 tests across
45 files.

PR #83 added the corresponding capability to the side-scroller through its own
picker and renderer. It shared creation semantics without sharing a game
engine. Browser testing confirmed selection and wiring without console errors;
the unreliable automated pit crossing prevented a direct screenshot beyond
the first pit. Validation passed 351 tests across 46 files.

PR #84 added non-interactive decorative-object infrastructure to both games.
Quest props were demonstrated end to end, while side-scroller resolution and
layering were unit-tested against intentionally empty committed asset and
placement data. The built-in object list remained empty. Final validation
passed 364 tests across 48 files, with 290 changed lines under the 400-line
cap.

Across all five changes, Kai gained more ways to shape how Boo-Boo Story looks.
The games retained complete authority over how Boo-Boo Story behaves.

## Definition Of Done

Day 82 reached the creative-asset-boundary checkpoint:

- followed Day 81 with the July 22, 2026 entry
- treated Boo-Boo Story PRs #80 through #84 as one connected work session
- linked every source pull request
- recorded all five shared asset types and their canonical canvas dimensions
- preserved `setpiece` as the compatible large-object category
- kept engine-specific aspect-ratio and presentation scaling outside the
  shared dimension module
- described the existing Design Studio picker extension rather than a new
  selection system
- preserved missing-kind compatibility and unknown-kind rejection
- kept enemy creations out of character and weapon loaders
- recorded direct browser confirmation of all five picker canvas sizes
- described quest designed enemies as session-only visual replacements
- preserved original quest enemy behavior, combat rules, and fallback art
- kept `BUILTIN_ENEMIES` empty pending a Kai-supplied export
- shared creation semantics with the side-scroller without sharing engines
- recorded the side-scroller browser evidence and the pit-crossing screenshot
  limitation separately
- left the unrelated quest thumbnail issue outside PR #83
- described quest props as fixed-slot, animated, beneath-actor, non-colliding
  visuals
- treated the Home Meadow slots as provisional defaults awaiting Kai's
  direction
- described side-scroller asset resolution, layering, and scene-clock
  animation
- recorded direct quest prop evidence separately from unit-tested
  side-scroller behavior
- kept `BUILTIN_OBJECTS` empty pending Kai's art and placement decisions
- claimed no collision, physics, interaction, pickup, gameplay effect, object
  editor, or cross-engine abstraction
- recorded the final 364-test, 48-file validation and 290-line PR size
- preserved the central boundary that Kai's drawings control appearance while
  each game controls behavior
