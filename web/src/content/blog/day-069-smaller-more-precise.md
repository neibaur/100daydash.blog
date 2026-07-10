---
title: "Day 69 - July 9, 2026: Smaller, Then More Precise"
description: "A Day 69 reflection on narrowing broad Boo-Boo Quest ideas through repository audits, deterministic enemy behavior, test-shaped design, stacked PR governance, and browser screenshot evidence."
pubDate: "2026-07-09"
day: 69
dashboardSlug: "none"
dataSources:
  - "Boo-Boo Quest Claude Opus ideation notes"
  - "Boo-Boo Quest Fable implementation summary"
  - "Boo-Boo Story PR #42 through PR #46 notes"
  - "Boo-Boo Quest test and CI results"
  - "Boo-Boo Quest browser screenshot verification notes"
status: "published"
tags:
  - ai-agents
  - agentic-engineering
  - governance
  - boo-boo-story
  - boo-boo-quest
  - game-design
  - pathfinding
  - testing
  - code-review
  - developer-experience
---

Day 69 started with questions that were much larger than the code that
eventually changed.

Boo-Boo Quest already had 12 explorable screens. Boo-boo could use a hammer,
stars, and a squirt gun to solve puzzles or defeat enemies. He could dance to
disorient them, create clones, and eventually encounter a dinosaur boss.

But the soundtrack and graphics still felt basic. The world was only four
screens wide and three screens tall. The enemies worked, but I wondered
whether they could have more autonomy. And behind all of those questions was
the more important one: what would make the game more engaging for a
ten-year-old boy and his friends?

Those are useful product questions.

They are also dangerously easy to turn into oversized implementation prompts.

I first worked through them with Claude Opus. Then Fable implemented the
selected ideas in VS Code. Between those two stages, the work kept becoming
smaller and more precise.

"Improve the soundtrack" became one missing hammer-swing sound after an audit
found that nearly the whole audio system already existed. "Give the enemies
AI" became deterministic state machines, breadth-first search pathfinding,
and reactions to Boo-boo's tools instead of runtime model calls. "Make the
world much larger" became a 6x5 scaffold rather than a 50x50 field of generic
rooms.

Then the repository narrowed the work again.

Existing tests shaped the enemy data model and the timing of state
transitions. The CI contract split the map expansion into a test-only baseline
PR and a later implementation PR. Browser screenshots found a clipped heading
after the unit tests were already green.

The broad ideas did not survive unchanged.

That was the success.

## A Large World Was Not The Same As A Better World

One of my first questions was whether the existing 4x3 map could become
something much larger, perhaps even 50x50.

Claude pushed back.

The technical limit was not the interesting constraint. Canvas could support
a larger world. The harder problem was producing enough authored content to
make that world worth exploring.

A 50x50 grid would contain 2,500 screens. If most of them were empty,
procedural, or only lightly differentiated, the game could feel less
interesting precisely because it was larger. The map would create distance
without creating discovery.

That reframed the question.

The goal was not to maximize coordinates. It was to create enough room for
Kai and me to keep designing the world without asking an agent to fabricate a
huge amount of filler.

The recommendation was a more modest 6x5 or 8x6 expansion. I selected the
smaller end of that range: 6x5.

That would make the main grid two and a half times its previous size while
keeping the new locations visibly unfinished. The agent could expand the
canvas and connect the systems. Kai and I could decide what belongs in the
new spaces later.

That was the first narrowing of the day.

The bigger number was technically possible. It was not the better product
decision.

## "AI Enemies" Did Not Need An LLM

The enemy question needed the same kind of pushback.

Could enemies or other characters use AI to behave with more autonomy and
originality?

The tempting answer would be to connect each enemy to a model. That would also
be a poor fit for this game.

Runtime LLM calls would introduce network dependence, latency, cost, and
unpredictability into something that should feel immediate and remain
playable offline. An enemy does not become more fun merely because its next
move came from an API.

The useful question was not whether a model could control an enemy.

It was what behaviors would make the enemy _feel_ smarter.

The answer was much more concrete:

- patrol
- notice the player
- chase
- attack
- flee from the squirt gun
- become stunned or disoriented by Boo-boo's dance
- navigate around walls

Those behaviors are deterministic. They can still create the impression of
attention, intent, and reaction.

That distinction became the practical answer to my original AI question. The
game did not need machine learning or an LLM feature. It needed enemies whose
behavior responded more clearly to the player and the world.

The implementation prompt therefore carried two explicit boundaries: no new
runtime dependencies and no network calls.

Those constraints did not make the result less intelligent.

They clarified what intelligence meant in this context.

## Better Sound Started With Listening To The Repository

From the ideation session, I selected three concerns for Fable:

1. sound effects and music
2. smarter deterministic enemies
3. a modest map expansion

The implementation prompt asked for one concern per PR, approximately 400 or
fewer changed or new lines per PR, the `ai-assisted` label, green validation,
no new runtime dependencies, and no network calls.

At first glance, the audio concern looked substantial.

The request named hammer, squirt-gun, star-collection, damage,
heart-container, and dance sounds. It also asked for looping background music,
mute, and a session-persistent volume control.

An agent following that list too literally could have built a complete audio
system.

Fable audited the modularized game first.

That audit found a synthesized Web Audio sound-effect bank, two chiptune loops
for title and gameplay, a HUD mute button, and a volume dial. Almost the entire
requested feature already existed.

There was one real acceptance-criteria gap.

The hammer made a sound when it hit something, but swinging through empty
space was silent.

So PR #42 did not rebuild audio. It added a swing-start `Fx` event and a small
falling-triangle blip in the render layer. The implementation was roughly five
lines.

The PR description mapped the remaining requested criteria to the code that
already satisfied them.

That is one of the cleanest examples of repository-grounded implementation I
have seen in this project.

The prompt described a feature. The repository contained almost all of it.
The agent's job was not to produce enough code to match the size of the
request. It was to find the actual gap.

Audit before implementing.

That sentence sounds obvious. It is also a direct defense against duplicated
systems, unnecessary abstractions, and impressive-looking diffs that make the
repository worse.

## A Small State Machine Made The Enemies Feel Smarter

The enemy work was naturally large enough to split across two stacked PRs.

PR #43 introduced the state machine and pathfinding.

Each enemy now follows a deterministic behavior flow:

```text
patrol -> notice -> chase -> attack
```

The tuning values live in one exported `BEHAVIORS` table. That table holds
things such as radii in tiles and movement speed in pixels per second.

The design matters more than the table syntax.

Adding another enemy type should mainly mean adding another behavior
configuration row. It should not require inventing another unrelated movement
algorithm.

For chase movement, Fable added breadth-first search over the walkable tile
grid. The new `pathfind.ts` implementation was only around 55 lines. Enemy
paths refresh every 0.4 seconds, with straight-line steering retained as a
fallback.

Enemies can also leash back toward their patrol area, ignore a downed player,
and preserve the game's existing dance-confusion behavior.

None of that is a general game-AI platform.

It is a bounded set of behaviors for the game that exists.

That is why it is useful.

## The Existing Tests Designed Part Of The Feature

The enemy implementation also showed why tests are more than a final green
check.

Two existing expectations shaped the design directly.

First, old test fixtures construct `Enemy` objects as object literals. The
repository's batch-discipline governance prevents an implementation PR from
quietly rewriting existing tests alongside the production change.

Fable could not simply make several new required fields and then update the
fixtures to match.

Instead, the new AI state lives in one optional `brain` field. The field is
lazily initialized with `??=`.

That preserved compatibility with the existing object-literal fixtures while
still giving the behavior system somewhere to keep state.

Second, one existing test performs a single `0.1` second update and expects a
chasing enemy to have already moved closer.

A conventional state-machine implementation might spend one tick moving from
`patrol` to `notice`, another moving from `notice` to `chase`, and only begin
moving on a later update.

That would have broken the existing behavior contract.

So state transitions cascade within one tick. When an enemy has a zero notice
delay, it can move from patrol through notice to chase movement during the
same update.

That choice was not made after the feature was complete so the tests would
stop complaining.

The test described an observable timing requirement. The implementation
honored it.

The repository's existing evidence constrained both the data model and the
runtime semantics.

That is a stronger relationship than "the tests passed."

The tests participated in the design.

## Boo-boo's Tools Became Part Of The Enemy System

PR #44 built on the state-machine work by making the enemies react to
Boo-boo's existing tools.

A squirt-gun splash now causes an enemy to flee in a timed sprint. Fire
enemies can be doused and run away. The wiggle dance freezes enemies in place
for a configured duration.

Previously, the dance behavior relied on one hardcoded 4.5-second value. The
stun duration now belongs to each enemy type's behavior configuration.

That is a small architectural improvement, but the product effect is more
important.

The player already had a hammer, stars, a squirt gun, and a dance. Smarter
enemies should not only become better at chasing Boo-boo. They should make the
player's existing verbs matter in more interesting ways.

Flee and stun behavior did that.

The enemy work became more engaging by deepening the relationship with tools
that were already present, not by adding a model or another inventory system.

## The Map Had Hidden Coordinates

The world expansion uncovered a different kind of repository constraint.

The visible goal was simple: change the main world from 4x3 screens to 6x5.

The repository contained two assumptions that made that change less simple.

One world test explicitly hardcoded `WORLD_W = 4`.

More importantly, the cave and den interiors were stored at screen keys `4,0`
and `5,0`.

Those coordinates were safely outside the old four-wide world. They worked
as off-grid interior storage.

In a six-wide world, the same keys would become ordinary grid locations. A
player could potentially enter an interior simply by walking across a normal
screen boundary.

The map size was not only a pair of constants.

It was entangled with test expectations and the coordinate convention for
special interiors.

The obvious patch would update the tests and production world together.

The repository would not allow that sequence.

Its batch-discipline CI check rejects PRs that modify existing tests and
implementation in the same batch. That rule exists so an implementation
agent cannot silently weaken the baseline while changing production code to
make the new baseline pass.

Instead of bypassing the rule, Fable split the work.

The map expansion that looked like one feature became two PRs.

## PR #45 Changed The Specification Before The World

PR #45 was test-only.

It re-specified the world, screen, enemy, and combat expectations so they no
longer depended on accidental 4x3 coordinates.

The new specifications still pin the screen geometry exactly. They still
require the main world to remain at least 4x3. They require special interiors
to remain off-grid wherever their keys are placed. They find the cave and den
by display name instead of hardcoded coordinate literals.

Most importantly, the rewritten assertions remained valid against the
unchanged 4x3 production implementation.

That is the test of whether the baseline was being clarified or weakened.

PR #45 did not make a future implementation pass by lowering the bar. It
changed the bar from accidental coordinates to the architectural properties
the coordinates had been standing in for.

There was a useful failure in the middle of this work.

An initial grep missed one hardcoded coordinate literal in the combat spec.
The later expansion PR exposed it when the tests ran.

The missed assumption was corrected in the test-only baseline PR. It was not
patched around in the implementation.

That is the governance loop working as intended.

The CI rule did create another PR and another ordering constraint. But it also
forced the repository to say what was actually important before production
behavior moved.

## PR #46 Expanded The Canvas Without Filling It In

Once the test baseline was grid-agnostic, PR #46 expanded `WORLD_W` and
`WORLD_H` to 6x5.

The eighteen new locations share one deliberately obvious placeholder screen.
It is a tree-bordered empty meadow with exits on all four sides and a name
like:

```text
🚧 Build Me! x,y
```

The game did not generate eighteen filler levels.

That preserved the decision from the Claude ideation session. The system
could create reachable space. It did not need to pretend that generated
content was authored adventure.

The cave and den interiors moved to off-grid keys `9,0` and `10,0`. Their
warps, boss spawn, interior enemies, heart container, and cave-darkness
overlay moved with them.

Doorways were opened in old border screens so the newly adjacent locations
are reachable. The minimap and full world-map overlay were resized for the
new dimensions.

Because the test baseline had been corrected first, one specification can now
verify that every adjacent pair across the full 6x5 world shares a valid
crossing.

That is better than changing an assertion from four to six.

The test now describes the topology that matters as the world grows.

## Green Tests Did Not Protect The Heading

The map expansion changed layout, so verification continued after the unit
suite passed.

Fable built the site, created auto-driven copies of the built game page in
`dist`, and used a script to click START and dispatch an `M` keypress. It
served the result through Astro preview and captured screenshots with headless
Microsoft Edge.

Those screenshots confirmed that the 6x5 minimap and full world map rendered.

They also found a regression the unit tests could not see.

The taller map overflowed the vertically centered flex overlay. The "World
Map" heading was clipped off-screen.

The topology was correct. The TypeScript was correct. The tests were green.
The rendered page was still wrong.

A small CSS change pinned the content toward the top and made the overlay
scrollable. Fable then repeated the screenshot check before committing the
fix.

That connects directly to the executable-evidence work from yesterday.

Screenshots did not replace unit tests. Each layer protected a different
property.

The tests protected enemy behavior, compatibility, state timing, interior
placement, and world topology. The browser screenshot protected the actual
user-visible layout.

The larger world created a presentation failure that did not exist in the
models the unit suite observed.

The lesson is not that every change needs a screenshot.

It is that a layout change needs evidence from the layout.

## Three Features Became Five PRs

The initial request named three concerns.

The implementation produced five PRs, #42 through #46.

That was not scope inflation.

It was the repository revealing the real seams in the work.

Audio collapsed into a tiny gap fill because the audit found existing
capability. Enemy behavior split naturally into state machine and pathfinding
first, then tool reactions. The map split into a test-only baseline
re-specification and the 6x5 implementation because the CI contract would not
allow the old tests and new world to be casually rewritten together.

The enemy PRs formed one stack:

```text
#43 -> #44
```

The map PRs formed another:

```text
#45 -> #46
```

Every PR began with a failing specification in a new test file. New test files
are exempt from the batch-discipline check, so the implementation could
follow in a second commit without rewriting the standing baseline.

All five PRs carried the `ai-assisted` label and co-author trailers required
by the Boo-Boo Story agent contract.

The session ended with roughly 600 lines of implementation and tests, 96
passing tests instead of 82, no new dependencies, and no existing test file
modified by an implementation PR.

Those numbers are useful, but they are not the main story.

The main story is that the governance did more than slow down the agent or
make the PRs smaller.

It exposed structure.

The approximate 400-line concern boundary encouraged the enemy work to split
at a coherent seam. The no-network constraint clarified what smarter enemies
should mean for this game. The batch-discipline check forced accidental map
coordinates to become explicit architectural specifications. Existing tests
shaped compatibility and timing. Screenshot verification found a failure
outside the unit suite's field of view.

The rails made the work tell the truth about itself.

## Why The Day Mattered

Day 69 mattered because the strongest decisions were reductions.

The soundtrack did not need to be rebuilt. It needed one missing swing sound.

The enemies did not need runtime LLM calls. They needed a small state machine,
BFS pathfinding, and meaningful reactions to the squirt gun and dance.

The world did not need 2,500 screens. It needed 30 reachable positions, with
18 of them honestly marked as unfinished.

The map change did not need a test rewrite hidden inside an implementation
PR. It needed a separate baseline clarification that continued to pass
against the old world.

Green tests did not need to be treated as the end of verification. The layout
needed to run in a browser where the clipped heading could become visible.

This is the kind of agentic engineering I want to keep practicing.

Start with the broad product question. Let review challenge the premise. Let
the repository show what already exists. Let tests reveal behavioral
contracts. Let CI expose boundaries. Let executable evidence cover the parts
the unit suite cannot see.

Then implement the smallest thing that still answers the real question.

The result is not always fewer pull requests.

Sometimes narrowing the work produces more PRs because the correct seams only
become visible after the repository has a chance to answer back.

That happened today.

Three concerns became five PRs, but the code stayed more focused. The audio
system stayed intact. Enemy behavior remained deterministic and offline. The
test baseline became more architectural. The world became larger without
pretending to be full.

That last part is the most personal outcome.

The 6x5 map now contains eighteen `🚧 Build Me!` locations for Kai and me.
An agent could have generated forests, caves, puzzles, enemies, and names for
all of them. The map would have looked complete sooner.

It would also have removed some of the reason to make the game together.

Fable expanded the canvas and improved the systems around it. The unfinished
screens preserve the part that should still come from Kai's imagination.

That is not missing work.

It is the boundary that makes the work ours.

## Outcome

Day 69 connected a Claude Opus product-ideation session with a Fable
implementation session for Boo-Boo Quest.

The starting questions were intentionally broad: how to improve basic sound
and graphics, whether the 4x3 world should become as large as 50x50, whether
enemies should use AI for greater autonomy, and what could make the game more
engaging for a ten-year-old boy and his friends.

Claude pushed back on the largest interpretations. A 50x50 world was
technically possible but created a 2,500-screen content problem. Runtime LLM
calls for enemies would add network dependence, latency, cost, and
unpredictability to an immediate offline game. The selected direction was a
modest map scaffold, deterministic enemy behavior, and high-impact sound and
feedback improvements.

Fable then implemented the three selected concerns across five PRs, #42
through #46. The audio audit found that the synthesized effects bank, title
and gameplay chiptunes, mute button, and volume dial already existed. PR #42
therefore filled only the missing empty-space hammer-swing sound with a new
swing-start `Fx` event and falling-triangle blip.

PR #43 added the deterministic `patrol -> notice -> chase -> attack` behavior
flow, centralized tuning in the exported `BEHAVIORS` table, and BFS
shortest-path movement over walkable tiles. Paths refresh every 0.4 seconds,
with straight-line steering as fallback. Enemies can leash toward patrol,
ignore a downed player, and preserve dance confusion.

Existing tests shaped that design. New state was stored in one optional,
lazily initialized `brain` field so object-literal fixtures remained valid.
State transitions cascade within one update so a zero-delay enemy still moves
during the existing test's first `0.1` second tick.

PR #44 added tool reactions. Squirt-gun splashes trigger timed fleeing, fire
enemies can be doused and run away, and the wiggle dance freezes enemies for
a per-type configured duration instead of one hardcoded 4.5-second value.

The 6x5 map expansion exposed a hardcoded four-wide test and off-grid cave and
den keys at `4,0` and `5,0` that would become ordinary grid coordinates. The
batch-discipline CI rule prevented changing those existing tests and the
implementation together.

PR #45 therefore changed only the baseline specifications. It kept exact
screen geometry, required a world of at least 4x3, required interiors to stay
off-grid, located the cave and den by display name, and remained green against
the unchanged 4x3 implementation. A missed hardcoded coordinate in the combat
spec was found by the later expansion test run and corrected in this test-only
PR.

PR #46 expanded the world to 6x5, moved the cave and den to off-grid keys
`9,0` and `10,0`, updated their warps and associated gameplay, opened old
border screens, and resized the minimap and world-map overlay. The eighteen
new locations share a deliberately obvious tree-bordered placeholder named
`🚧 Build Me! x,y` instead of generated filler.

Browser verification caught the final regression. After the site build and
unit tests passed, an auto-driven built game page opened START and dispatched
`M` under Astro preview. Headless Edge screenshots showed that the taller map
clipped the "World Map" heading in the vertically centered overlay. A small
CSS change top-aligned the content and made the overlay scrollable, and the
page was re-screenshot before commit.

The session ended with five `ai-assisted` PRs carrying the required co-author
trailers, roughly 600 lines of implementation and tests, 96 passing tests up
from 82, zero new dependencies, and zero existing test files modified by any
implementation PR.

## Definition Of Done

Day 69 reached the Boo-Boo Quest focused-enhancement checkpoint:

- confirmed Day 69 follows Day 68 for July 8, 2026
- assigned the July 9, 2026 work to Day 69
- connected Claude Opus ideation to Fable implementation
- framed the work as progressive narrowing rather than five release notes
- started from the existing 12-screen Boo-Boo Quest game
- preserved hammer, stars, squirt gun, dance, clones, and dinosaur boss context
- included the sound, graphics, world-size, enemy-autonomy, and engagement questions
- explained why a 50x50 map was a content problem rather than a Canvas limit
- selected a modest 6x5 scaffold
- preserved Kai and me as the future level designers
- rejected runtime LLM calls for individual enemies
- avoided calling deterministic behavior machine learning
- kept the game offline and free of network calls
- kept the implementation free of new runtime dependencies
- translated "AI enemies" into observable deterministic behavior
- selected sound, smarter enemies, and map expansion as the three concerns
- required one concern per PR and approximately 400 changed lines per PR
- audited the audio implementation before adding code
- found the existing Web Audio effects bank
- found the title and gameplay chiptune loops
- found the existing mute and volume controls
- identified empty-space hammer swings as the only audio gap
- kept PR #42 to a small `Fx` event and render-layer blip
- added the deterministic enemy behavior flow in PR #43
- centralized behavior tuning in `BEHAVIORS`
- added BFS shortest-path navigation in `pathfind.ts`
- kept the pathfinding implementation around 55 lines
- refreshed paths every 0.4 seconds
- retained straight-line fallback steering
- preserved leash, downed-player, and dance-confusion behavior
- used one optional lazily initialized `brain` field
- preserved object-literal test-fixture compatibility
- cascaded zero-delay state transitions within one update
- honored the existing `0.1` second movement expectation
- treated tests as design constraints rather than only validation
- added squirt-gun flee behavior in PR #44
- allowed fire enemies to be doused and flee
- moved dance stun duration into per-enemy configuration
- split enemy state/pathfinding and tool reactions into stacked PRs
- identified the hardcoded `WORLD_W = 4` test assumption
- identified `4,0` and `5,0` as off-grid interiors that would become on-grid
- respected the batch-discipline restriction on existing tests plus implementation
- created PR #45 as a test-only baseline re-specification
- kept the new baseline green against the unchanged 4x3 world
- preserved exact screen geometry and the at-least-4x3 requirement
- required interiors to remain off-grid
- located cave and den interiors by display name
- corrected the missed combat-spec coordinate in the baseline PR
- created PR #46 as the 6x5 implementation
- moved interiors to off-grid keys `9,0` and `10,0`
- updated warps, boss spawn, enemies, heart container, and darkness overlay
- opened old border screens to make new locations reachable
- resized the minimap and world-map overlay
- verified every adjacent pair has a valid crossing
- created eighteen deliberately unfinished locations
- used the obvious `🚧 Build Me! x,y` placeholder
- avoided generating filler levels
- built and served the resulting site
- auto-drove START and the `M` key in a built game copy
- captured headless Edge screenshots
- found the clipped World Map heading after unit tests passed
- top-aligned the overlay content and made it scrollable
- repeated screenshot verification after the CSS fix
- kept tests and screenshots responsible for different evidence
- produced five PRs, #42 through #46
- used the stacked #43-to-#44 enemy sequence
- used the stacked #45-to-#46 map sequence
- began every PR with a failing specification in a new test file
- labeled every PR `ai-assisted`
- included the required co-author trailers
- finished with roughly 600 lines of implementation and tests
- finished with 96 passing tests, up from 82
- added zero dependencies
- modified zero existing test files in implementation PRs
- preserved the central lesson: broad ideas became better work by becoming smaller and more precise
- left eighteen world locations open for Kai's imagination
