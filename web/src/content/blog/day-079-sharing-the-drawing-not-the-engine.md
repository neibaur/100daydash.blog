---
title: "Day 79 - July 19, 2026: Sharing the Drawing, Not the Engine"
description: "A Day 79 reflection on graduating Boo-Boo Story's side-scroller into a maintained game by sharing Kai's creation format while keeping its physics, enemies, progression, and game loop deliberately separate."
pubDate: "2026-07-19"
day: 79
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Story PR #76 through PR #79 implementation and validation notes"
  - "Boo-Boo Story side-scroller, Boo-Boo Quest, and Design Studio architecture notes"
  - "Kai's Boo-Boo Design Studio character creations and existing enemy artwork"
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
  - prototyping
  - architecture
  - scope-management
---

The side-scroller already ran.

Boo-Boo could move across a level, jump onto platforms, and reach a flag. The
original proof of concept had answered its first question: this kind of game
could feel at home inside Boo-Boo Story.

But movement and a finish line were not enough to make it a maintained game.

The prototype still lived as one isolated HTML experiment. It had one level,
hard-coded behavior, no place in the application's game listing, no connection
to the characters Kai made in the Boo-Boo Design Studio, and no durable
architectural status. It worked, but the project had not yet made a commitment
to keep working on it.

The previous day's [PR
#75](https://github.com/neibaur-labs/boo-boo-story/pull/75) began that
commitment by extracting typed level data and tested movement physics. It
intentionally stopped before adding a page or changing anything a player could
see.

On July 19, four focused pull requests completed the graduation and then built
a small but complete game on top of it.

[PR #76](https://github.com/neibaur-labs/boo-boo-story/pull/76) connected the
tested modules to a maintained Astro page.

[PR #77](https://github.com/neibaur-labs/boo-boo-story/pull/77) let characters
from Kai's designer enter a second game.

[PR #78](https://github.com/neibaur-labs/boo-boo-story/pull/78) added three
levels, pits, hearts, progression, and a win state.

[PR #79](https://github.com/neibaur-labs/boo-boo-story/pull/79) added patrol
enemies, stomping, damage feedback, and a real game-over flow.

The important change was not that one prototype accumulated a list of
features. It was that the game accumulated boundaries: between experiment and
application, creation data and engine behavior, level promises and level
content, success and failure, and shared meaning and merely similar code.

The prototype became a game by accumulating boundaries, not abstractions.

## Graduation Before Expansion

PR #76 made zero gameplay changes.

That restraint was the point.

The new `/play/runs-and-jumps` route placed the side-scroller inside a real
Astro page. Browser and animation-loop wiring moved into
`src/lib/side-scroller/main.ts`, where keyboard and touch input, rendering,
and `requestAnimationFrame` could connect the tested logic from PR #75 to the
canvas.

The game appeared under the Games section on `/play`. It offered navigation
back to that listing and preserved the existing `art by Kai` credit. An
amendment to `ADR-0005` recorded that the side-scroller was no longer only an
experiment. It had become maintained application code.

The original prototype remained untouched at `public/play/side-scroller/`.

That followed the precedent already established by Boo-Boo Quest. Graduation
did not require rewriting history or erasing the artifact that made the next
decision possible. The old version could remain available for comparison and
experimentation while the maintained route evolved separately.

Separating the work also protected the migration from feature enthusiasm. If
the port and the first gameplay expansion had happened together, a movement
regression could have been confused with an intentional design change. By
connecting the existing physics to the application without altering them, PR
#76 made the architectural transition independently reviewable.

The split demonstrated the repository's line-cap governance in practice. The
complete port was too large for one pull request, so PR #75 contained pure
logic and tests while PR #76 contained the page, browser glue, listing, and
architecture documentation. The second slice changed 379 lines, including
approximately 325 lines in `src`, and passed `pnpm validate`.

The most consequential part of that pull request was not visible gameplay.
The game acquired a route, a listing, an ADR status, and a place inside the
maintained application. Architectural graduation made every later feature a
change to a product rather than another mutation of a disposable sketch.

## One Character Crossed Into Two Games

The next boundary connected the side-scroller to Kai's creative workflow.

Boo-Boo Quest could already load characters from the local designer shelf.
The creation file described the frames, author, dimensions, and selected
animation speed. The quest understood those semantics, but its loader lived
inside a quest-specific module.

It would have been easy to approach the second game in one of two unhealthy
ways.

The side-scroller could have copied the whole loader and allowed the two
implementations to drift. Or the games could have been pushed into a shared
engine because both happened to render characters.

PR #77 chose a narrower seam.

`src/lib/custom-characters.ts` became the one shared module responsible for
loading custom characters and weapons from the local shelf, selecting the
correct animation frame, and interpreting the designer-selected
frames-per-second value. The original quest module became a re-export shim, so
its imports and tests did not need to change.

That module shared creation-format meaning. It did not share game behavior.

The side-scroller gained a character-selection row matching the quest
experience: the default Boo-Boo character plus one button for every character
on the local shelf. Selection lasted only for the browser session. No new
persistence system was added.

While walking, a custom character used its own flipbook and its creator's
chosen animation speed. While standing or airborne, the game used frame zero.
That was an explicit limitation rather than an invented capability. The
creation format had no separate jump pose, so the side-scroller did not
pretend otherwise.

Character sizing followed the same height-normalized rendering rule as
Boo-Boo Quest. The game did not perform another automatic fit. That made the
prior fit-to-canvas work important in the end-to-end workflow: Kai controls the
drawing in the designer, explicitly fits it there when needed, and both games
interpret the resulting creation consistently.

By the end of PR #77, one of Kai's characters could travel from the designer
canvas into the validated `.booboo.json` format, onto the local shelf, through
character selection, and into a second maintained game.

The designer was no longer an isolated drawing tool or a companion to only one
game. The creative pipeline had become reusable because its artifact carried
stable meaning across product boundaries.

The pull request added 184 lines, followed the repository's tests-first
pattern, and passed `pnpm validate`.

## Sharing Meaning Without Sharing An Engine

The custom-character work clarified what the two games were allowed to share.

They shared Kai's static art. They shared the `.booboo.json` creation format.
They shared the rules for loading a creation and selecting its animation
frames.

They did not share physics, rendering loops, enemies, damage systems, game
state, or level progression.

That distinction matters because similar code is not automatically the same
concept.

Both games can make a character flicker after taking damage. Both can display
hearts. Both can move an enemy across the screen. But each behavior exists
inside a different engine with different timing, collision, camera, and state
contracts. Combining those systems merely because their screenshots look
related would couple two games before their shared structure had become
stable.

The creation format was different. A designer-selected frames-per-second value
meant the same thing wherever a creation appeared. Loading a local-shelf file
required the same validation regardless of the game. Those semantics were
already stable enough to centralize.

The code reused a concept where its meaning was genuinely identical and
reimplemented behavior where resemblance alone did not justify coupling.

Sometimes duplication is evidence that an abstraction is missing. Sometimes
it is the healthier price of letting two products develop independently. PR
#77 kept that decision local and precise.

## Three Handcrafted Levels Were Enough

Once the game had a maintained route and playable custom characters, PR #78
turned one layout into a short run.

The game received three levels as typed constants.

Level 1 preserved the original prototype without changing it. Level 2 added
pits, greater height differences, and longer jumps. Level 3 increased the
challenge again.

The implementation did not introduce a level-file loader, editor, procedural
generator, or generalized content framework. Three known levels did not yet
justify infrastructure for an imagined hundred.

Handcrafted constants were enough, but they were not ungoverned data.

Tests verified that platforms stayed inside the level boundaries, pits stayed
within the player's maximum full-speed jump range, and every pit had a rescue
platform above or nearby. They also encoded the design promise that Level 3
was measurably more difficult than the earlier levels.

Those tests were not only checking helper functions. They were checking
playability claims.

A level could be valid TypeScript and still contain an impossible jump. A
patrol definition could satisfy its type and still cross a hazard. Encoding
the intended geometry as invariants made the content reviewable in the same
way as code.

Pits entered the level model as optional horizontal ranges. The floor
collision skipped those ranges, allowing the player to fall through. After
falling 80 pixels below the normal floor line, the player lost one heart and
returned to the beginning of the current level.

The implementation deliberately chose level-start respawn instead of tracking
the last safe ground position. A more sophisticated checkpoint model could be
added if play showed it was needed. The initial rule was simple, predictable,
and sufficient for three short levels.

Optional `pits` data also allowed Level 1 and its existing tests to remain
stable. The first level did not need fake empty hazards or a rewritten schema
just because later levels introduced a new challenge.

## A Run Needed Success And Failure

Reaching a flag now advanced to the next level. Reaching the final flag opened
a win screen with a restart option.

The game stored only the current level index and remaining hearts, and that
state lived in memory. There was no save-game persistence to design, migrate,
or explain.

The hearts display borrowed the visual pattern from Boo-Boo Quest but was
implemented inside the side-scroller. Pits removed whole hearts, so the
quest's half-heart behavior was not copied merely for visual consistency.

At the end of PR #78, losing every heart still performed a temporary soft
reset. That placeholder allowed the level and progression work to remain one
concern. The next pull request would complete the failure state.

PR #78 changed 385 lines and passed `pnpm validate`.

The three levels made the game longer, but progression made them a run. Hearts
gave mistakes a cost. The final flag gave the sequence an ending. The feature
was not a general level system; it was just enough authored content and state
to establish a beginning, escalation, and success condition.

## Enemies Completed The Contrast

PR #79 added the first enemy type without importing the Boo-Boo Quest enemy
engine.

The enemy reused one of Kai's existing quest images. This was static-art
sharing only. The side-scroller did not support designer-created enemies, and
it did not claim that a custom character file also described enemy behavior.

That future possibility remained intentionally unresolved. Supporting
designer-created enemies would require deciding whether the format needs an
`enemy` asset kind, whether the existing `character` kind is sufficient, and
how enemy-specific animation and behavior should be represented. A borrowed
image did not justify making those format decisions early.

The enemy behavior stayed local to the side-scroller. Enemies walked along the
ground, patrolled between explicit bounds in the level data, turned at each
end, wobbled as they moved, bobbed vertically, and mirrored with their travel
direction.

Explicit patrol bounds won over platform-edge detection. They were easy to
author, easy to inspect, and appropriate for three handcrafted levels.

Level 1 remained enemy-free. Level 2 received two enemies. Level 3 received
three. Tests verified that each enemy stood on solid ground and that no patrol
range crossed a pit.

Again, the tests protected a design promise rather than only an implementation
detail. An enemy should not begin in empty space or walk through a hazard the
player must respect.

Contact created two distinct outcomes.

Touching an enemy from the side removed one heart, pushed the player away at
approximately 175 pixels per second for about 0.16 seconds, added a small
upward pop, and granted roughly 1.2 seconds of temporary invulnerability. The
character flickered during that protected period.

Those values mirrored the feel of Boo-Boo Quest's damage feedback, but the
side-scroller implemented them independently. Shared product language did not
require shared gameplay code.

Falling onto the upper portion of an enemy produced the opposite result. The
enemy was defeated and the player received a small bounce. Horizontal contact
caused damage; deliberate downward contact rewarded the player.

That contrast turned enemies from moving obstacles into a readable mechanic.

## Game Over Made Recovery Explicit

PR #79 also replaced the soft reset from the previous slice.

When the last heart disappeared, gameplay stopped and a game-over box appeared.
The player could restart the run, restoring the hearts and returning to the
beginning.

This was a small interface, but it completed the loop.

A game needs more than movement and hazards. It needs success, failure,
recovery, and a way to try again. Without the game-over state, running out of
hearts was only an internal number reaching zero before the program quietly
changed its mind. Naming the failure and offering a restart made the rules
legible to the player.

PR #79 added 323 lines, passed `pnpm validate`, and brought the repository to
330 tests.

Across the four pull requests, the progression was deliberate: first establish
the maintained page, then connect the creative pipeline, then author the run,
then add opposition and complete failure. Each pull request had one coherent
reason to exist. The project did not hide a large `finish the game` change
behind a single review.

## The Boundary Made The Game Bigger

It can seem paradoxical that keeping the engines separate helped the creative
system expand.

A generalized engine might appear to promise more reuse. But forcing Boo-Boo
Quest and the side-scroller into one model would have redirected the work from
Kai's experience toward reconciling physics, collision rules, render loops,
and state machines that had not asked to become the same.

The narrower boundary created a more useful kind of reuse.

Kai's creation could live in two games because both honored the same artifact.
Each game remained free to decide what standing, walking, jumping, taking
damage, and reaching the end meant in its own world.

The prototype also remained free to exist beside the maintained game. The
first level remained free to omit pits and enemies through optional data. The
level definitions remained free to be simple typed constants. The static
enemy image remained free not to imply an unfinished asset-format decision.

Those limits did not make the project smaller. They let it grow in several
directions without pretending the directions were identical.

On July 18, the side-scroller had tested movement modules waiting for a page.
By the end of July 19, it had an application route, architecture documentation,
designer-created characters, three governed levels, hazards, hearts,
progression, patrol enemies, a win state, and a game-over flow.

The meaningful transformation was not from few features to many features.

It was from an experiment that happened to run into a game with explicit
promises about where it lived, what it shared, what it kept separate, how a
player could succeed, how a player could fail, and how the project could
continue changing it.

The drawing crossed into another game.

The engine did not have to follow it.

## Outcome

Day 79 completed the July 19 Boo-Boo Story side-scroller work represented by
PRs #76 through #79.

PR #76 completed the graduation started by the prior day's PR #75. It added
the maintained `/play/runs-and-jumps` Astro route, browser and animation-loop
wiring, keyboard and touch input, a `/play` game listing, navigation, Kai's art
credit, and an `ADR-0005` amendment without changing gameplay. The original
prototype remained untouched under `public/play/side-scroller/`. The pull
request changed 379 lines, including approximately 325 in `src`, and passed
`pnpm validate`.

PR #77 extracted the stable custom-creation loading and animation semantics
into `src/lib/custom-characters.ts`, retained the quest's previous module as a
re-export shim, and added session-only side-scroller character selection.
Custom characters used their own flipbook speed while walking and frame zero
while standing or airborne. The games shared the creation format and loader,
not their engines. The tests-first pull request added 184 lines and passed
`pnpm validate`.

PR #78 added three handcrafted typed levels, reachable pits with rescue
platforms, whole-heart loss, level-start respawn, progression, and a final win
screen. Level and heart state stayed in memory. Level-layout tests protected
boundaries, jump reachability, rescue placement, and increasing difficulty.
The pull request changed 385 lines and passed `pnpm validate`.

PR #79 added locally implemented patrol enemies using one existing static
Kai-drawn image, side-contact damage, knockback, an upward pop, temporary
invulnerability, flicker, stomping, a bounce, and a proper game-over and
restart flow. Level 1 remained enemy-free, while Levels 2 and 3 received two
and three enemies. Tests kept enemies on solid ground and patrols away from
pits. The pull request added 323 lines, passed `pnpm validate`, and brought the
repository to 330 tests.

Designed enemies, a shared game engine, a jump-pose creation semantic, and
save-game persistence all remained outside the completed work.

## Definition Of Done

Day 79 reached the maintained side-scroller game checkpoint:

- followed Day 78 with the July 19, 2026 entry
- limited the completed work to Boo-Boo Story PRs #76 through #79
- treated PR #75 only as the July 18 prerequisite
- framed the work as one connected graduation and game-loop story
- recorded `/play/runs-and-jumps` as the maintained Astro route
- preserved the original prototype under `public/play/side-scroller/`
- recorded keyboard, touch, rendering, and animation-loop wiring
- included the `/play` listing, back navigation, Kai's art credit, and ADR
  amendment
- stated that PR #76 made zero gameplay changes
- explained the logic-and-tests then page-and-wiring line-cap split
- recorded PR #76's 379 changed lines, approximate 325 `src` lines, and passing
  validation
- described the shared custom-character loader and quest re-export shim
- limited sharing to shelf loading, weapon loading, frame selection, and
  creation-format animation speed
- kept side-scroller and Boo-Boo Quest physics, rendering, damage, enemies,
  state, and progression separate
- recorded default and local-shelf character selection as session-only
- stated that custom characters use frame zero while standing or airborne
- claimed no separate jump pose in the creation format
- connected height-normalized rendering to the prior fit-to-canvas workflow
- recorded PR #77's tests-first structure, 184 lines, and passing validation
- described three handcrafted typed levels without inventing a level framework
- preserved Level 1 and increased difficulty in Levels 2 and 3
- recorded level-boundary, pit-reachability, rescue-platform, and difficulty
  invariants
- described optional pit ranges and floor collision that skips them
- recorded whole-heart loss after falling 80 pixels below the floor
- chose level-start respawn instead of last-safe-ground tracking
- recorded in-memory level and heart state with no save persistence
- described progression, final victory, restart, and side-scroller-owned hearts
- recorded PR #78's 385 changed lines and passing validation
- described explicit enemy patrol bounds, direction mirroring, wobble, and bob
- kept Level 1 enemy-free and recorded two and three enemies in later levels
- recorded solid-ground and pit-free-patrol tests
- distinguished static-art reuse from enemy-engine sharing
- claimed no support for designer-created enemies
- left enemy asset-kind and behavior semantics as future design decisions
- recorded side contact, one-heart damage, approximate 175-pixel-per-second
  knockback, 0.16-second knockback duration, upward pop, 1.2-second
  invulnerability, and flicker
- distinguished damaging horizontal contact from rewarded downward stomping
- recorded the stomp bounce and enemy defeat
- described the final game-over, stopped gameplay, heart reset, and restart flow
- recorded PR #79's 323 added lines, passing validation, and 330-test total
- treated success, failure, recovery, and restart as the complete game loop
- preserved the central lesson that stable meaning can be shared without
  prematurely generalizing separate engines
